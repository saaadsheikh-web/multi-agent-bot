#!/usr/bin/env python3
"""
PURE THESIS BACKTEST — does the IDEA actually work, stripped of all filters?

Three tests:
  TEST 1: Single Fib level — bounce at 0.382 / 0.500 / 0.618 retracement
  TEST 2: Hot zones — 2+ Fib levels overlapping (multi-swing confluence)
  TEST 3: Trend lines — linear regression through swing pivots, touch + bounce

For each: walk every bar, find the setup, simulate forward, measure WR and avg PnL.
NO additional filters (no RSI, no volume, no trend bias) — just the thesis itself.
This tells us: does the LEVEL alone have edge?
"""
import os
import pandas as pd
import numpy as np
from collections import defaultdict

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
MAKER_FEE = 0.0002
ROUND_TRIP = MAKER_FEE * 2  # 0.04%

SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
           "AVAX-USDT","ADA-USDT","LINK-USDT","TAO-USDT","INJ-USDT",
           "APT-USDT","ARB-USDT"]
DAYS = 90

def load(sym, tf="1H"):
    f = os.path.join(CACHE, f"{sym.replace('-','_')}_{tf}_365d.parquet")
    if not os.path.exists(f): return None
    df = pd.read_parquet(f)
    df.columns = [c.lower() for c in df.columns]
    return df.iloc[-DAYS*24:].reset_index(drop=True)

def simulate(df, i, side, tp_pct, sl_pct, max_bars=24):
    """Walk forward, find first hit. SL checked first conservatively."""
    entry = df["close"].iloc[i]
    if side == "long":
        tp = entry * (1 + tp_pct/100)
        sl = entry * (1 - sl_pct/100)
    else:
        tp = entry * (1 - tp_pct/100)
        sl = entry * (1 + sl_pct/100)
    end = min(i + max_bars, len(df) - 1)
    for j in range(i+1, end+1):
        h, l = df["high"].iloc[j], df["low"].iloc[j]
        if side == "long":
            if l <= sl: return ("SL", sl)
            if h >= tp: return ("TP", tp)
        else:
            if h >= sl: return ("SL", sl)
            if l <= tp: return ("TP", tp)
    return ("TIME", df["close"].iloc[end])

def pct_pnl(side, entry, exit_p):
    if side == "long":
        return (exit_p - entry) / entry * 100 - ROUND_TRIP * 100
    return (entry - exit_p) / entry * 100 - ROUND_TRIP * 100

# ============================================================================
# TEST 1 — Single Fib level
# ============================================================================
def test_single_fib(df, lookback=50, fib_proximity=0.003, tp_pct=2.0, sl_pct=1.0):
    """At each bar, check if price is within 0.3% of a 0.382/0.500/0.618 retracement
    of the recent lookback-bar swing. If yes, simulate the bounce/rejection trade."""
    results = defaultdict(lambda: {"n":0, "w":0, "pnl":0.0})
    last_fire = -100
    for i in range(lookback + 5, len(df) - 5):
        if i - last_fire < 12: continue   # 12-bar cooldown
        win_h = df["high"].iloc[i-lookback:i]
        win_l = df["low"].iloc[i-lookback:i]
        sh = win_h.max(); sl_ = win_l.min()
        if sh <= sl_ or (sh - sl_) / sl_ < 0.02: continue
        sh_idx = win_h.idxmax(); sl_idx = win_l.idxmin()
        uptrend = sh_idx > sl_idx
        move = sh - sl_
        last = df["close"].iloc[i]
        for level in [0.382, 0.500, 0.618]:
            fib_p = (sh - move * level) if uptrend else (sl_ + move * level)
            if abs(last - fib_p) / fib_p < fib_proximity:
                side = "long" if uptrend else "short"
                outcome, exit_p = simulate(df, i, side, tp_pct, sl_pct)
                pct = pct_pnl(side, last, exit_p)
                key = f"{level:.3f}"
                results[key]["n"] += 1
                if pct > 0: results[key]["w"] += 1
                results[key]["pnl"] += pct
                last_fire = i
                break
    return results

# ============================================================================
# TEST 2 — Hot zone (multi-swing confluence)
# ============================================================================
def test_hot_zone(df, tp_pct=2.0, sl_pct=1.0, min_strength=2):
    """Compute Fibs from multiple swing windows, find clusters where 2+ Fibs overlap
    within 0.4%. If price within 0.6% of cluster, simulate."""
    results = defaultdict(lambda: {"n":0, "w":0, "pnl":0.0})
    last_fire = -100
    fib_levels = [0.236, 0.382, 0.500, 0.618, 0.786]
    for i in range(250, len(df) - 5):
        if i - last_fire < 12: continue
        all_fibs = []
        for w in [30, 60, 120, 240]:
            if i < w + 5: continue
            wh = df["high"].iloc[i-w:i].max()
            wl = df["low"].iloc[i-w:i].min()
            if wh <= wl or (wh - wl) / wl < 0.015: continue
            sh_idx = df["high"].iloc[i-w:i].idxmax()
            sl_idx = df["low"].iloc[i-w:i].idxmin()
            upt = sh_idx > sl_idx
            move = wh - wl
            for f in fib_levels:
                all_fibs.append((wh - move * f) if upt else (wl + move * f))
        if len(all_fibs) < 4: continue
        # Cluster
        sp = sorted(all_fibs)
        clusters = [[sp[0]]]
        for p in sp[1:]:
            cm = sum(clusters[-1]) / len(clusters[-1])
            if abs(p - cm) / cm <= 0.004:
                clusters[-1].append(p)
            else:
                clusters.append([p])
        zones = sorted([(sum(c)/len(c), len(c)) for c in clusters if len(c) >= min_strength],
                       key=lambda x: -x[1])
        if not zones: continue
        last = df["close"].iloc[i]
        zones.sort(key=lambda z: abs(z[0] - last))
        nearest, strength = zones[0]
        dist = (last - nearest) / nearest
        if abs(dist) > 0.006: continue
        side = "long" if dist > 0 else "short"   # bounce off support / rejection at resistance
        outcome, exit_p = simulate(df, i, side, tp_pct, sl_pct)
        pct = pct_pnl(side, last, exit_p)
        key = f"strength={strength}"
        results[key]["n"] += 1
        if pct > 0: results[key]["w"] += 1
        results[key]["pnl"] += pct
        last_fire = i
    return results

# ============================================================================
# TEST 3 — Trend line touches
# ============================================================================
def find_pivots(df, window=5):
    """Return list of (idx, price, kind) where kind in {'high','low'}."""
    pivots = []
    h = df["high"]; l = df["low"]
    for i in range(window, len(df) - window):
        if h.iloc[i] == h.iloc[i-window:i+window+1].max():
            pivots.append((i, h.iloc[i], "high"))
        elif l.iloc[i] == l.iloc[i-window:i+window+1].min():
            pivots.append((i, l.iloc[i], "low"))
    return pivots

def test_trend_lines(df, lookback_pivots=8, touch_proximity=0.004, tp_pct=2.0, sl_pct=1.0):
    """Fit a linear regression through last N low pivots = uptrend support.
    Through last N high pivots = downtrend resistance. When current price touches
    the line within 0.4%, simulate bounce/rejection."""
    results = {"uptrend_support": {"n":0,"w":0,"pnl":0.0},
               "downtrend_resist": {"n":0,"w":0,"pnl":0.0}}
    pivots = find_pivots(df, window=5)
    if len(pivots) < lookback_pivots * 2: return results
    last_fire = -100
    for i in range(50, len(df) - 5):
        if i - last_fire < 12: continue
        # Recent pivots before bar i
        recent = [p for p in pivots if p[0] < i - 2][-lookback_pivots*2:]
        if len(recent) < lookback_pivots: continue
        lows  = [(idx, pr) for idx, pr, k in recent if k == "low"]
        highs = [(idx, pr) for idx, pr, k in recent if k == "high"]
        last = df["close"].iloc[i]
        # Test uptrend support line (3+ low pivots, positive slope)
        if len(lows) >= 3:
            xs = np.array([p[0] for p in lows[-lookback_pivots:]])
            ys = np.array([p[1] for p in lows[-lookback_pivots:]])
            if len(xs) >= 3:
                # Linear fit
                slope, intercept = np.polyfit(xs, ys, 1)
                # R² check
                pred = slope * xs + intercept
                ss_res = np.sum((ys - pred)**2)
                ss_tot = np.sum((ys - ys.mean())**2)
                r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
                if slope > 0 and r2 > 0.5:
                    line_at_i = slope * i + intercept
                    if line_at_i > 0 and abs(last - line_at_i) / line_at_i < touch_proximity:
                        # Touch: simulate long bounce
                        outcome, exit_p = simulate(df, i, "long", tp_pct, sl_pct)
                        pct = pct_pnl("long", last, exit_p)
                        results["uptrend_support"]["n"] += 1
                        if pct > 0: results["uptrend_support"]["w"] += 1
                        results["uptrend_support"]["pnl"] += pct
                        last_fire = i
                        continue
        # Test downtrend resistance line (3+ high pivots, negative slope)
        if len(highs) >= 3:
            xs = np.array([p[0] for p in highs[-lookback_pivots:]])
            ys = np.array([p[1] for p in highs[-lookback_pivots:]])
            if len(xs) >= 3:
                slope, intercept = np.polyfit(xs, ys, 1)
                pred = slope * xs + intercept
                ss_res = np.sum((ys - pred)**2)
                ss_tot = np.sum((ys - ys.mean())**2)
                r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
                if slope < 0 and r2 > 0.5:
                    line_at_i = slope * i + intercept
                    if line_at_i > 0 and abs(last - line_at_i) / line_at_i < touch_proximity:
                        outcome, exit_p = simulate(df, i, "short", tp_pct, sl_pct)
                        pct = pct_pnl("short", last, exit_p)
                        results["downtrend_resist"]["n"] += 1
                        if pct > 0: results["downtrend_resist"]["w"] += 1
                        results["downtrend_resist"]["pnl"] += pct
                        last_fire = i
    return results

# ============================================================================
# RUN
# ============================================================================
def run():
    test1_global = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    test2_global = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    test3_global = {"uptrend_support":{"n":0,"w":0,"pnl":0.0},
                    "downtrend_resist":{"n":0,"w":0,"pnl":0.0}}
    for sym in SYMBOLS:
        df = load(sym)
        if df is None or len(df) < 300: continue
        # Test 1
        r1 = test_single_fib(df)
        for k, v in r1.items():
            for kk in ("n","w","pnl"): test1_global[k][kk] += v[kk]
        # Test 2
        r2 = test_hot_zone(df)
        for k, v in r2.items():
            for kk in ("n","w","pnl"): test2_global[k][kk] += v[kk]
        # Test 3
        r3 = test_trend_lines(df)
        for k in ("uptrend_support","downtrend_resist"):
            for kk in ("n","w","pnl"): test3_global[k][kk] += r3[k][kk]
        print(f"  {sym}: done")

    print()
    print("="*72)
    print(f"TEST 1 — SINGLE FIB LEVELS  ({DAYS}d, 12 syms, no filters)")
    print("="*72)
    print(f"{'level':<10}{'trades':>8}{'WR%':>7}{'sum %':>9}{'avg %':>9}{'$/trade@$100':>14}")
    print("-"*72)
    for level in ["0.382","0.500","0.618"]:
        d = test1_global[level]
        if d["n"] == 0: continue
        wr = d["w"]/d["n"]*100
        avg = d["pnl"]/d["n"]
        print(f"  {level:<8}{d['n']:>8}{wr:>6.1f}%{d['pnl']:>+8.1f}%{avg:>+8.3f}%{avg:>+12.3f}")

    print()
    print("="*72)
    print(f"TEST 2 — HOT ZONES (multi-swing Fib confluence)")
    print("="*72)
    print(f"{'zone strength':<18}{'trades':>8}{'WR%':>7}{'sum %':>9}{'avg %':>9}{'$/trade@$100':>14}")
    print("-"*72)
    for k in sorted(test2_global.keys()):
        d = test2_global[k]
        if d["n"] == 0: continue
        wr = d["w"]/d["n"]*100
        avg = d["pnl"]/d["n"]
        print(f"  {k:<16}{d['n']:>8}{wr:>6.1f}%{d['pnl']:>+8.1f}%{avg:>+8.3f}%{avg:>+12.3f}")

    print()
    print("="*72)
    print(f"TEST 3 — TREND LINE TOUCHES (linreg through swing pivots, R²>0.5)")
    print("="*72)
    print(f"{'kind':<22}{'trades':>8}{'WR%':>7}{'sum %':>9}{'avg %':>9}{'$/trade@$100':>14}")
    print("-"*72)
    for k in ("uptrend_support","downtrend_resist"):
        d = test3_global[k]
        if d["n"] == 0:
            print(f"  {k:<20}{'0':>8}  no signals")
            continue
        wr = d["w"]/d["n"]*100
        avg = d["pnl"]/d["n"]
        print(f"  {k:<20}{d['n']:>8}{wr:>6.1f}%{d['pnl']:>+8.1f}%{avg:>+8.3f}%{avg:>+12.3f}")

    print()
    print("="*72)
    print("INTERPRETATION GUIDE")
    print("="*72)
    print("WR>50% + avg%>+0.05% = real edge worth keeping")
    print("WR>55% + avg%>+0.10% = strong edge, worth scaling")
    print("WR<45% or avg%<0    = no edge alone, needs confluence/filters")
    print("Sample <50 trades   = noise, ignore")

if __name__ == "__main__":
    run()
