#!/usr/bin/env python3
"""Focused backtest for the wide_candle agent.

Tests only the wide_candle strategy on 8 major symbols × 365 days. Fast (~2 min)
because it skips all other agents. Outputs WR, ExpR, Sharpe, MaxDD.
"""
import os, sys, math, time
from pathlib import Path
from statistics import mean, stdev

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
sys.path.insert(0, str(WORK))

from dotenv import load_dotenv
load_dotenv(WORK / ".env")

import pandas as pd
import numpy as np

# Import indicators from bot.py
sys.path.insert(0, str(WORK))
from bot import ema, rsi, atr

TAKER_FEE = 0.0006   # per side, 0.0012 round-trip
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "BNB-USDT",
           "DOGE-USDT", "AVAX-USDT", "LINK-USDT"]
DAYS = 365

def load_1h(sym, days):
    """Load cached 1H parquet from backtest_data/."""
    p = WORK / "backtest_data" / f"{sym.replace('-', '_')}_1H_365d.parquet"
    if not p.exists():
        return None
    df = pd.read_parquet(p)
    return df

def aggregate_4h(df1h):
    """Aggregate 1H bars to 4H bars."""
    n = len(df1h)
    n_aligned = (n // 4) * 4
    df = df1h.iloc[-n_aligned:].copy().reset_index(drop=True)
    df["g"] = df.index // 4
    agg = df.groupby("g").agg(
        ts=("ts", "first"), open=("open", "first"), high=("high", "max"),
        low=("low", "min"), close=("close", "last"), volume=("volume", "sum")
    ).reset_index(drop=True)
    return agg

def detect_wide_candle_signal(df4h, i):
    """Mirror of WideCandleAgent.analyze() at index i."""
    if i < 50: return None
    c_window = df4h["close"].iloc[:i+1]
    o_window = df4h["open"].iloc[:i+1]
    v_window = df4h["volume"].iloc[:i+1]
    last = c_window.iloc[-1]; prev = c_window.iloc[-2]
    last_o = o_window.iloc[-1]; prev_o = o_window.iloc[-2]
    last_h = df4h["high"].iloc[i]; last_l = df4h["low"].iloc[i]
    e21 = ema(c_window, 21).iloc[-1]
    e50 = ema(c_window, 50).iloc[-1]
    if pd.isna(e50) or pd.isna(e21): return None
    r = rsi(c_window).iloc[-1]
    avg_v = v_window.rolling(20).mean().iloc[-1]
    if avg_v <= 0 or pd.isna(avg_v): return None
    v_ratio = v_window.iloc[-1] / avg_v
    if v_ratio < 1.5: return None
    body = abs(last - last_o)
    bar_range = last_h - last_l
    if bar_range <= 0: return None
    prev_body = abs(prev - prev_o)
    bullish_engulf = prev < prev_o and last > last_o and last > prev_o and last_o < prev and body > prev_body
    lower_wick = min(last_o, last) - last_l
    upper_wick = last_h - max(last_o, last)
    hammer = lower_wick > body * 2 and upper_wick < body * 0.5 and last > last_o
    bullish_at_extreme = bullish_engulf and last < e50 * 0.97 and r < 35
    bullish_hammer = hammer and last < e50 * 0.97 and r < 35
    bearish_engulf = prev > prev_o and last < last_o and last < prev_o and last_o > prev and body > prev_body
    shooting_star = upper_wick > body * 2 and lower_wick < body * 0.5 and last < last_o
    bearish_at_extreme = bearish_engulf and last > e50 * 1.03 and r > 65
    bearish_shooting = shooting_star and last > e50 * 1.03 and r > 65
    if bullish_at_extreme or bullish_hammer:
        sl_price = last * 0.96
        return ("long", last, sl_price)
    if bearish_at_extreme or bearish_shooting:
        sl_price = last * 1.04
        return ("short", last, sl_price)
    return None

def simulate(df4h):
    """Walk forward through 4H bars, applying wide_candle rules with trailing exit."""
    trades = []
    open_trade = None
    for i in range(50, len(df4h) - 1):
        last = df4h["close"].iloc[i]
        if last <= 0: continue
        # Manage open trade
        if open_trade:
            sign = 1 if open_trade["side"] == "long" else -1
            adv = sign * (last - open_trade["entry"]) / open_trade["entry"]
            risk = abs(open_trade["entry"] - open_trade["sl"]) / open_trade["entry"]
            # Update high water mark and trailing stop
            if adv > open_trade["best"]:
                open_trade["best"] = adv
            # SL hit (initial or trailing)
            stop_breach = (open_trade["side"] == "long" and last <= open_trade["sl"]) or \
                          (open_trade["side"] == "short" and last >= open_trade["sl"])
            if stop_breach:
                # Compute realized R
                actual_pct = sign * (open_trade["sl"] - open_trade["entry"]) / open_trade["entry"]
                r = (actual_pct - TAKER_FEE * 2) / risk
                trades.append(r)
                open_trade = None
                continue
            # Trailing stop activation
            if open_trade["best"] >= 0.02:   # 2% activate
                trail_dist = 0.015           # 1.5% trail
                if open_trade["side"] == "long":
                    new_sl = last * (1 - trail_dist)
                    if new_sl > open_trade["sl"]:
                        open_trade["sl"] = new_sl
                else:
                    new_sl = last * (1 + trail_dist)
                    if new_sl < open_trade["sl"]:
                        open_trade["sl"] = new_sl
            # Max hold (10080 min = 7 days = 42 4h bars)
            if i - open_trade["open_i"] > 42:
                actual_pct = sign * (last - open_trade["entry"]) / open_trade["entry"]
                r = (actual_pct - TAKER_FEE * 2) / risk
                trades.append(r)
                open_trade = None
                continue
        if open_trade: continue
        # Open new
        sig = detect_wide_candle_signal(df4h, i)
        if sig is None: continue
        side, entry, sl = sig
        open_trade = {"side": side, "entry": entry, "sl": sl, "open_i": i, "best": 0.0}
    return trades

def main():
    print("=" * 60)
    print("  wide_candle BACKTEST — 365 days, 8 symbols, 4H bars")
    print("=" * 60)
    all_trades = []
    per_sym = {}
    for sym in SYMBOLS:
        df1h = load_1h(sym, DAYS)
        if df1h is None:
            print(f"  {sym}: NO CACHED DATA — skipping")
            continue
        df4h = aggregate_4h(df1h)
        trades = simulate(df4h)
        per_sym[sym] = trades
        all_trades.extend(trades)
        print(f"  {sym}: {len(trades)} trades")

    if not all_trades:
        print("\n❌ No trades generated. Strategy may be too strict, or no qualifying setups in data.")
        return

    wins = [t for t in all_trades if t > 0]
    losses = [t for t in all_trades if t <= 0]
    wr = len(wins) / len(all_trades) * 100
    expR = mean(all_trades)
    s = stdev(all_trades) if len(all_trades) > 1 else 0
    sharpe = (expR / s * math.sqrt(252)) if s > 0 else 0
    avg_win = mean(wins) if wins else 0
    avg_loss = mean(losses) if losses else 0
    eq = []; cum = 0
    for t in all_trades: cum += t; eq.append(cum)
    peak = eq[0]; max_dd = 0
    for x in eq:
        peak = max(peak, x)
        max_dd = max(max_dd, peak - x)

    breakeven_wr = (abs(avg_loss) + 0.12 / 4.0) / (avg_win + abs(avg_loss) + 0.24 / 4.0) * 100 if avg_win else 0

    print()
    print("=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"  Total trades:   {len(all_trades)}")
    print(f"  Win rate:       {wr:.1f}%")
    print(f"  Avg win:        {avg_win:+.2f}R")
    print(f"  Avg loss:       {avg_loss:+.2f}R")
    print(f"  R:R realized:   {avg_win/abs(avg_loss):.2f}:1" if avg_loss else "  R:R: N/A")
    print(f"  ExpR per trade: {expR:+.4f}R")
    print(f"  Sharpe:         {sharpe:.2f}")
    print(f"  Max DD:         {max_dd:.2f}R")
    print(f"  Total return:   {sum(all_trades):+.2f}R")
    print(f"  Breakeven WR:   ~{breakeven_wr:.1f}% (you got {wr:.1f}%)")
    print()
    if expR >= 0.20 and sharpe >= 2.0 and len(all_trades) >= 50:
        print("  🟢 PASSES validation thresholds — recommend deploying small (0.05x)")
    elif expR > 0:
        print("  🟡 Profitable but below validation bar — paper for now")
    else:
        print("  🔴 NEGATIVE EDGE — do not deploy. Tune filters or kill.")

if __name__ == "__main__":
    main()
