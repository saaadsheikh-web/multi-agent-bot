#!/usr/bin/env python3
"""Focused backtest for the 2 quant agents: hurst_regime and kalman_trend.

Tests each strategy on 8 major symbols × 365 days using cached data.
Fast (~1 min total) — no network. Outputs WR, ExpR, Sharpe, MaxDD per agent.
"""
import os, sys, math
from pathlib import Path
from statistics import mean, stdev

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
sys.path.insert(0, str(WORK))

from dotenv import load_dotenv
load_dotenv(WORK / ".env")

import pandas as pd
import numpy as np

from bot import ema, rsi, atr, hurst_exponent, kalman_filter_1d

TAKER_FEE = 0.0006
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "BNB-USDT",
           "DOGE-USDT", "AVAX-USDT", "LINK-USDT"]
DAYS = 365


def load_1h(sym):
    p = WORK / "backtest_data" / f"{sym.replace('-', '_')}_1H_365d.parquet"
    if not p.exists():
        return None
    return pd.read_parquet(p)


def hurst_signal(df, i):
    """Mirror of HurstRegimeAgent.analyze() at index i (1H bar)."""
    if i < 120: return None
    c = df["close"].iloc[:i+1]
    last = c.iloc[-1]
    H = hurst_exponent(c.iloc[-100:].values, max_lag=15)
    r = rsi(c).iloc[-1]
    e21 = ema(c, 21).iloc[-1]
    atr_val = atr(df.iloc[:i+1]).iloc[-1]
    if atr_val <= 0 or pd.isna(atr_val): return None

    if H < 0.42:
        if r < 28:
            sl = last * 0.985; tp = last * 1.020
            return ("long", last, sl, tp)
        if r > 72:
            sl = last * 1.015; tp = last * 0.980
            return ("short", last, sl, tp)
        return None

    if H > 0.58:
        if last > e21 and 50 < r < 70:
            sl = last - 1.5 * atr_val; tp = last * 1.99
            return ("long", last, sl, tp)
        if last < e21 and 30 < r < 50:
            sl = last + 1.5 * atr_val; tp = last * 0.01
            return ("short", last, sl, tp)
    return None


def kalman_signal(df, i):
    """Mirror of KalmanTrendAgent.analyze() at index i (1H bar)."""
    if i < 100: return None
    c = df["close"].iloc[:i+1]
    v = df["volume"].iloc[:i+1]
    last = c.iloc[-1]
    kf = kalman_filter_1d(c.iloc[-80:].values, q=0.0005, r=0.5)
    prev_slope = kf[-2] - kf[-7] if len(kf) > 7 else 0
    cur_slope  = kf[-1] - kf[-6] if len(kf) > 6 else 0
    if pd.isna(cur_slope) or pd.isna(prev_slope): return None
    bull = prev_slope <= 0 and cur_slope > 0
    bear = prev_slope >= 0 and cur_slope < 0
    if not (bull or bear): return None
    avg_v = v.rolling(20).mean().iloc[-1]
    if avg_v <= 0 or pd.isna(avg_v): return None
    v_ratio = v.iloc[-1] / avg_v
    if v_ratio < 1.2: return None
    atr_val = atr(df.iloc[:i+1]).iloc[-1]
    if atr_val <= 0 or pd.isna(atr_val): return None
    if bull:
        sl = last - 2.0 * atr_val; tp = last * 1.99
        return ("long", last, sl, tp)
    sl = last + 2.0 * atr_val; tp = last * 0.01
    return ("short", last, sl, tp)


def simulate(df, sig_fn, profile_max_hold_bars: int):
    """Walk-forward sim: enter on signal, exit on TP/SL/trailing/max_hold."""
    trades = []
    open_t = None
    for i in range(len(df) - 1):
        last = df["close"].iloc[i]
        if last <= 0: continue
        if open_t:
            sign = 1 if open_t["side"] == "long" else -1
            adv = sign * (last - open_t["entry"]) / open_t["entry"]
            risk = abs(open_t["entry"] - open_t["sl"]) / open_t["entry"]
            if adv > open_t["best"]:
                open_t["best"] = adv
            stop_breach = (open_t["side"] == "long" and last <= open_t["sl"]) or \
                          (open_t["side"] == "short" and last >= open_t["sl"])
            if stop_breach:
                actual = sign * (open_t["sl"] - open_t["entry"]) / open_t["entry"]
                r = (actual - TAKER_FEE * 2) / risk
                trades.append(r); open_t = None; continue
            # Trailing: activate at +1%, trail by 0.8%
            if open_t["best"] >= 0.01:
                if open_t["side"] == "long":
                    new_sl = last * (1 - 0.008)
                    if new_sl > open_t["sl"]: open_t["sl"] = new_sl
                else:
                    new_sl = last * (1 + 0.008)
                    if new_sl < open_t["sl"]: open_t["sl"] = new_sl
            if i - open_t["open_i"] > profile_max_hold_bars:
                actual = sign * (last - open_t["entry"]) / open_t["entry"]
                r = (actual - TAKER_FEE * 2) / risk
                trades.append(r); open_t = None; continue
        if open_t: continue
        sig = sig_fn(df, i)
        if sig is None: continue
        side, entry, sl, tp = sig
        open_t = {"side": side, "entry": entry, "sl": sl, "tp": tp,
                  "open_i": i, "best": 0.0}
    return trades


def stats(trades):
    if not trades:
        return None
    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]
    wr = len(wins) / len(trades) * 100
    expR = mean(trades)
    s = stdev(trades) if len(trades) > 1 else 0
    sharpe = (expR / s * math.sqrt(252)) if s > 0 else 0
    avg_w = mean(wins) if wins else 0
    avg_l = mean(losses) if losses else 0
    eq = []; cum = 0
    for t in trades: cum += t; eq.append(cum)
    peak = eq[0]; mdd = 0
    for x in eq:
        peak = max(peak, x); mdd = max(mdd, peak - x)
    return dict(n=len(trades), wr=wr, expR=expR, sharpe=sharpe,
                avg_w=avg_w, avg_l=avg_l, mdd=mdd, total=sum(trades))


def report(name, all_trades):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    if not all_trades:
        print("  ❌ No trades generated — strategy too strict or no qualifying setups")
        return
    s = stats(all_trades)
    print(f"  Trades:          {s['n']}")
    print(f"  Win rate:        {s['wr']:.1f}%")
    print(f"  Avg win:         {s['avg_w']:+.2f}R")
    print(f"  Avg loss:        {s['avg_l']:+.2f}R")
    if s['avg_l']:
        print(f"  R:R realized:    {s['avg_w']/abs(s['avg_l']):.2f}:1")
    print(f"  ExpR per trade:  {s['expR']:+.4f}R")
    print(f"  Sharpe:          {s['sharpe']:.2f}")
    print(f"  Max DD:          {s['mdd']:.2f}R")
    print(f"  Total return:    {s['total']:+.2f}R")
    if s['expR'] >= 0.20 and s['sharpe'] >= 2.0 and s['n'] >= 50:
        print(f"  🟢 PASS — recommend deploy at 0.05x")
    elif s['expR'] >= 0.10 and s['sharpe'] >= 1.5:
        print(f"  🟡 OK — paper for now or deploy tiny (0.03x)")
    elif s['expR'] > 0:
        print(f"  🟡 marginal — paper")
    else:
        print(f"  🔴 NEGATIVE EDGE — kill")


def main():
    print("=" * 60)
    print(f"  QUANT BACKTEST — {DAYS} days, 8 symbols, 1H bars")
    print("=" * 60)
    hurst_all = []
    kalman_all = []
    for sym in SYMBOLS:
        df = load_1h(sym)
        if df is None:
            print(f"  {sym}: NO CACHED DATA")
            continue
        ht = simulate(df, hurst_signal, 8)
        kt = simulate(df, kalman_signal, 72)
        hurst_all.extend(ht)
        kalman_all.extend(kt)
        print(f"  {sym:14s} hurst={len(ht):3d}  kalman={len(kt):3d}")
    report("HURST_REGIME (Hurst exponent regime-switching)", hurst_all)
    report("KALMAN_TREND (Kalman-filtered trend follower)", kalman_all)


if __name__ == "__main__":
    main()
