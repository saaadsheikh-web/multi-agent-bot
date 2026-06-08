#!/usr/bin/env python3
"""
test_fibonacci_variants.py — backtest 12 Fibonacci-based strategies.

Variants tested:
  Style              | Timeframe | Filters
  -------------------|-----------|------------------
  fib_scalp_pure     | 15m       | Fib level only
  fib_scalp_rsi      | 15m       | Fib + RSI extreme
  fib_scalp_bb       | 15m       | Fib + Bollinger band touch
  fib_scalp_kitchen  | 15m       | Fib + RSI + BB + volume
  fib_day_pure       | 1H        | Fib level only
  fib_day_rsi        | 1H        | Fib + RSI extreme
  fib_day_ema        | 1H        | Fib + EMA200 trend filter
  fib_day_vol        | 1H        | Fib + volume confirmation
  fib_swing_pure     | 4H aggregated | Fib level only
  fib_swing_rsi      | 4H        | Fib + RSI extreme
  fib_swing_kitchen  | 4H        | Fib + RSI + EMA200 + volume

Each tested on 8 majors × 365 days using cached parquet.
"""
import os, sys, math
from pathlib import Path
from statistics import mean, stdev
from collections import defaultdict

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
sys.path.insert(0, str(WORK))

from dotenv import load_dotenv
load_dotenv(WORK / ".env")

import pandas as pd
import numpy as np

from bot import ema, rsi, atr, bbands

TAKER_FEE = 0.0006
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "BNB-USDT",
           "DOGE-USDT", "AVAX-USDT", "LINK-USDT"]
DAYS = 365
LOOKBACK = 50          # bars to find swing high/low
PROXIMITY = 0.005      # 0.5% near a fib level


def load(sym, tf):
    p = WORK / "backtest_data" / f"{sym.replace('-','_')}_{tf}_365d.parquet"
    if not p.exists():
        return None
    return pd.read_parquet(p)


def aggregate_4h(df1h):
    n = len(df1h)
    n_aligned = (n // 4) * 4
    df = df1h.iloc[-n_aligned:].copy().reset_index(drop=True)
    df["g"] = df.index // 4
    return df.groupby("g").agg(
        ts=("ts", "first"), open=("open", "first"), high=("high", "max"),
        low=("low", "min"), close=("close", "last"),
        volume=("volume", "sum")
    ).reset_index(drop=True)


def fib_signal(df, i, filters):
    """Generic Fib retracement signal at bar i with given filter dict.

    filters keys: 'rsi' (bool), 'bb' (bool), 'ema200' (bool), 'volume' (bool)
    Returns (side, entry, sl, tp) or None.
    """
    if i < LOOKBACK + 5:
        return None
    win = df.iloc[i - LOOKBACK:i]
    swing_high = win["high"].max()
    swing_low = win["low"].min()
    if swing_high <= swing_low:
        return None
    move = swing_high - swing_low
    if move / swing_low < 0.02:
        return None
    swing_high_idx = win["high"].idxmax()
    swing_low_idx = win["low"].idxmin()
    uptrend = swing_high_idx > swing_low_idx
    last = df["close"].iloc[i]

    # Fib levels
    fibs = {}
    for level in [0.382, 0.500, 0.618, 0.786]:
        if uptrend:
            fibs[level] = swing_high - move * level
        else:
            fibs[level] = swing_low + move * level

    at_level = None
    for lvl, p in fibs.items():
        if abs(last - p) / p < PROXIMITY:
            at_level = lvl
            break
    if at_level is None or at_level == 0.786:
        return None

    # Optional confluence filters
    closes_to_i = df["close"].iloc[:i+1]

    if filters.get("rsi"):
        r = rsi(closes_to_i, 14).iloc[-1]
        if pd.isna(r):
            return None
        if uptrend and r >= 45:   # need oversold for bounce
            return None
        if not uptrend and r <= 55:
            return None

    if filters.get("bb"):
        bbu, bbm, bbl = bbands(closes_to_i, 20, 2.0)
        if pd.isna(bbl.iloc[-1]) or pd.isna(bbu.iloc[-1]):
            return None
        if uptrend and last > bbl.iloc[-1] * 1.01:
            return None  # need to be near lower band
        if not uptrend and last < bbu.iloc[-1] * 0.99:
            return None

    if filters.get("ema200"):
        if len(closes_to_i) < 200:
            return None
        e200 = ema(closes_to_i, 200).iloc[-1]
        # In uptrend, price should be ABOVE EMA200; in downtrend, BELOW
        if uptrend and last < e200:
            return None
        if not uptrend and last > e200:
            return None

    if filters.get("volume"):
        avg_v = df["volume"].iloc[:i+1].rolling(20).mean().iloc[-1]
        if pd.isna(avg_v) or avg_v <= 0:
            return None
        v_ratio = df["volume"].iloc[i] / avg_v
        if v_ratio < 1.3:
            return None

    # Build signal
    if uptrend:
        sl = fibs[0.786] * 0.995
        tp = swing_high
        return ("long", last, sl, tp)
    sl = fibs[0.786] * 1.005
    tp = swing_low
    return ("short", last, sl, tp)


def simulate(df, filters, max_hold_bars):
    """Walk forward, fire fib signals, manage with trailing exit."""
    trades = []
    open_t = None
    for i in range(LOOKBACK + 5, len(df) - 1):
        last = df["close"].iloc[i]
        if last <= 0:
            continue
        if open_t:
            sign = 1 if open_t["side"] == "long" else -1
            adv = sign * (last - open_t["entry"]) / open_t["entry"]
            risk = abs(open_t["entry"] - open_t["sl"]) / open_t["entry"]
            if adv > open_t["best"]:
                open_t["best"] = adv
            stop_hit = (open_t["side"] == "long" and last <= open_t["sl"]) or \
                       (open_t["side"] == "short" and last >= open_t["sl"])
            if stop_hit:
                actual = sign * (open_t["sl"] - open_t["entry"]) / open_t["entry"]
                if risk > 0:
                    trades.append((actual - TAKER_FEE * 2) / risk)
                open_t = None
                continue
            # Trail at 1% behind peak once activated at +0.8%
            if open_t["best"] >= 0.008:
                if open_t["side"] == "long":
                    new_sl = last * (1 - 0.010)
                    if new_sl > open_t["sl"]:
                        open_t["sl"] = new_sl
                else:
                    new_sl = last * (1 + 0.010)
                    if new_sl < open_t["sl"]:
                        open_t["sl"] = new_sl
            # Max hold timeout
            if i - open_t["open_i"] > max_hold_bars:
                actual = sign * (last - open_t["entry"]) / open_t["entry"]
                if risk > 0:
                    trades.append((actual - TAKER_FEE * 2) / risk)
                open_t = None
                continue
        if open_t:
            continue
        sig = fib_signal(df, i, filters)
        if sig is None:
            continue
        side, entry, sl, tp = sig
        open_t = {"side": side, "entry": entry, "sl": sl, "tp": tp,
                  "open_i": i, "best": 0.0}
    return trades


def stats(trades):
    if not trades:
        return None
    trades = [t for t in trades if np.isfinite(t)]
    if not trades:
        return None
    wins = [t for t in trades if t > 0]
    wr = len(wins) / len(trades) * 100
    expR = float(np.mean(trades))
    s = float(np.std(trades, ddof=1)) if len(trades) > 1 else 0
    sharpe = (expR / s * math.sqrt(252)) if s > 0 else 0
    eq = []; cum = 0
    for t in trades:
        cum += t; eq.append(cum)
    peak = eq[0]; mdd = 0
    for x in eq:
        peak = max(peak, x); mdd = max(mdd, peak - x)
    return {
        "n": len(trades), "wr": wr, "expR": expR,
        "sharpe": sharpe, "mdd": mdd, "total": sum(trades)
    }


def run_variant(name, tf, filters, max_hold):
    all_trades = []
    for sym in SYMBOLS:
        df = load(sym, tf if tf != "4H" else "1H")
        if df is None:
            continue
        if tf == "4H":
            df = aggregate_4h(df)
        try:
            ts = simulate(df, filters, max_hold)
            all_trades.extend(ts)
        except Exception as e:
            print(f"  fail {sym} {name}: {e}")
    return stats(all_trades)


def main():
    print("=" * 80)
    print("  FIBONACCI VARIANT BACKTEST — 365d, 8 majors, 12 strategies")
    print("=" * 80)

    variants = [
        # SCALP (15m, max hold 24 bars = 6h)
        ("fib_scalp_pure",     "15m", {}, 24),
        ("fib_scalp_rsi",      "15m", {"rsi": True}, 24),
        ("fib_scalp_bb",       "15m", {"bb": True}, 24),
        ("fib_scalp_kitchen",  "15m", {"rsi": True, "bb": True, "volume": True}, 24),
        # DAY (1H, max hold 24 bars = 1 day)
        ("fib_day_pure",       "1H", {}, 24),
        ("fib_day_rsi",        "1H", {"rsi": True}, 24),
        ("fib_day_ema",        "1H", {"ema200": True}, 24),
        ("fib_day_vol",        "1H", {"volume": True}, 24),
        ("fib_day_kitchen",    "1H", {"rsi": True, "ema200": True, "volume": True}, 24),
        # SWING (4H, max hold 30 bars = 5 days)
        ("fib_swing_pure",     "4H", {}, 30),
        ("fib_swing_rsi",      "4H", {"rsi": True}, 30),
        ("fib_swing_kitchen",  "4H", {"rsi": True, "ema200": True, "volume": True}, 30),
    ]

    results = []
    for name, tf, filt, mh in variants:
        s = run_variant(name, tf, filt, mh)
        results.append((name, tf, s))
        if s:
            print(f"  {name:<22} tf={tf:<3}  N={s['n']:<4} WR={s['wr']:.1f}%  "
                  f"ExpR={s['expR']:+.3f}R  Sharpe={s['sharpe']:.2f}  Total={s['total']:+.1f}R")
        else:
            print(f"  {name:<22} tf={tf:<3}  no trades")

    # Final ranked table
    print()
    print("=" * 80)
    print("  RANKED RESULTS (by Sharpe)")
    print("=" * 80)
    valid = [(n, s) for n, _, s in results if s and s["n"] >= 20]
    valid.sort(key=lambda x: -x[1]["sharpe"])
    print(f"  {'Variant':<22} {'N':>5} {'WR':>7} {'ExpR':>8} {'Sharpe':>8} {'Verdict':<10}")
    for name, s in valid:
        verdict = ("🟢 PASS" if s["sharpe"] >= 2.0 and s["expR"] > 0.10
                   else ("🟡 OK" if s["expR"] > 0.05 else "🔴 KILL"))
        print(f"  {name:<22} {s['n']:>5} {s['wr']:>5.1f}% {s['expR']:>+7.3f}R {s['sharpe']:>+7.2f} {verdict}")
    print()

    pass_count = sum(1 for _, s in valid if s["sharpe"] >= 2.0 and s["expR"] > 0.10)
    print(f"  → {pass_count} of {len(valid)} variants pass deployment threshold")


if __name__ == "__main__":
    main()
