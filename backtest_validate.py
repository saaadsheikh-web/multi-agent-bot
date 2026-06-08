#!/usr/bin/env python3
"""
VALIDATION re-run — does the wedge finding hold up at full scale?
+ parameter sensitivity tests on the top 3 setups.

Period: 90 days × 12 symbols × 1H bars. Faster (vectorized where possible).
"""
import os, sys, time
import pandas as pd
import numpy as np
from collections import defaultdict

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
ROUND_TRIP_PCT = 0.04
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

def rsi(s, n=14):
    d = s.diff()
    up = d.where(d>0,0).rolling(n).mean()
    dn = (-d.where(d<0,0)).rolling(n).mean()
    return 100 - 100/(1 + up/dn)

def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def simulate(df, i, side, tp_pct, sl_pct, max_bars=24):
    entry = df["close"].iloc[i]
    if side == "long":
        tp = entry * (1+tp_pct/100); sl = entry * (1-sl_pct/100)
    else:
        tp = entry * (1-tp_pct/100); sl = entry * (1+sl_pct/100)
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
    p = (exit_p - entry)/entry*100 if side=="long" else (entry - exit_p)/entry*100
    return p - ROUND_TRIP_PCT

def find_pivots_quick(h_arr, l_arr, window=3):
    """Return lists of (idx, price) for highs and lows."""
    highs = []; lows = []
    n = len(h_arr)
    for k in range(window, n - window):
        if h_arr[k] == max(h_arr[k-window:k+window+1]):
            highs.append((k, h_arr[k]))
        elif l_arr[k] == min(l_arr[k-window:k+window+1]):
            lows.append((k, l_arr[k]))
    return highs, lows

# ============================================================================
# WEDGE TEST — multiple parameter sets
# ============================================================================
def test_wedges_param(df, lookback, pivot_window, break_buffer):
    """Vary parameters to test robustness."""
    res = {"falling_long":{"n":0,"w":0,"pnl":0.0}, "rising_short":{"n":0,"w":0,"pnl":0.0}}
    last_fire = -100
    h_full = df["high"].values; l_full = df["low"].values
    for i in range(lookback + 10, len(df) - 5):
        if i - last_fire < 24: continue
        h_arr = h_full[i-lookback:i]
        l_arr = l_full[i-lookback:i]
        highs, lows = find_pivots_quick(h_arr, l_arr, pivot_window)
        if len(highs) < 3 or len(lows) < 3: continue
        hx = np.array([p[0] for p in highs]); hy = np.array([p[1] for p in highs])
        lx = np.array([p[0] for p in lows]);  ly = np.array([p[1] for p in lows])
        h_slope, h_int = np.polyfit(hx, hy, 1)
        l_slope, l_int = np.polyfit(lx, ly, 1)
        last = df["close"].iloc[i]
        wedge_age_idx = lookback
        if h_slope > 0 and l_slope > 0 and h_slope < l_slope:
            line_lo = l_slope * wedge_age_idx + l_int
            if last < line_lo * (1 - break_buffer):
                _, ex = simulate(df, i, "short", 2.0, 1.0)
                pct = pct_pnl("short", last, ex)
                res["rising_short"]["n"] += 1
                if pct > 0: res["rising_short"]["w"] += 1
                res["rising_short"]["pnl"] += pct
                last_fire = i
        elif h_slope < 0 and l_slope < 0 and h_slope < l_slope:
            line_hi = h_slope * wedge_age_idx + h_int
            if last > line_hi * (1 + break_buffer):
                _, ex = simulate(df, i, "long", 2.0, 1.0)
                pct = pct_pnl("long", last, ex)
                res["falling_long"]["n"] += 1
                if pct > 0: res["falling_long"]["w"] += 1
                res["falling_long"]["pnl"] += pct
                last_fire = i
    return res

# ============================================================================
# 0.786 + EMA200 — re-validate at 90d full scope
# ============================================================================
def test_786_ema(df, ema_period=200):
    res = {"786_ema_long_with":{"n":0,"w":0,"pnl":0.0}, "786_ema_short_with":{"n":0,"w":0,"pnl":0.0}}
    last_fire = -100
    for i in range(ema_period + 60, len(df) - 5):
        if i - last_fire < 12: continue
        wh = df["high"].iloc[i-50:i].max(); wl = df["low"].iloc[i-50:i].min()
        if wh <= wl or (wh-wl)/wl < 0.025: continue
        sh_idx = df["high"].iloc[i-50:i].idxmax(); sl_idx = df["low"].iloc[i-50:i].idxmin()
        upt = sh_idx > sl_idx
        move = wh - wl
        fp_786 = (wh - move*0.786) if upt else (wl + move*0.786)
        last = df["close"].iloc[i]
        if abs(last - fp_786)/fp_786 >= 0.004: continue
        e = ema(df["close"].iloc[:i+1], ema_period).iloc[-1]
        if pd.isna(e): continue
        with_trend = (upt and last > e) or (not upt and last < e)
        if not with_trend: continue
        side = "long" if upt else "short"
        _, ex = simulate(df, i, side, 2.5, 1.5)
        pct = pct_pnl(side, last, ex)
        if side == "long":
            res["786_ema_long_with"]["n"] += 1
            if pct > 0: res["786_ema_long_with"]["w"] += 1
            res["786_ema_long_with"]["pnl"] += pct
        else:
            res["786_ema_short_with"]["n"] += 1
            if pct > 0: res["786_ema_short_with"]["w"] += 1
            res["786_ema_short_with"]["pnl"] += pct
        last_fire = i
    return res

# ============================================================================
# RUN VALIDATION
# ============================================================================
def run():
    t0 = time.time()
    print("Loading data + running tests...")

    # Aggregate results
    wedge_grids = {}  # (lookback, pivot_window, break_buffer) -> {falling_long, rising_short}
    ema_grid = {}     # ema_period -> {long_with, short_with}

    # Parameter grid for wedges
    wedge_params = [
        (40, 3, 0.001),
        (50, 3, 0.002),  # baseline that worked at 60d
        (60, 3, 0.002),
        (50, 4, 0.002),
        (50, 3, 0.003),
        (70, 4, 0.002),
    ]
    for params in wedge_params:
        wedge_grids[params] = {"falling_long":{"n":0,"w":0,"pnl":0.0},
                                "rising_short":{"n":0,"w":0,"pnl":0.0}}
    for ep in [50, 100, 200]:
        ema_grid[ep] = {"786_ema_long_with":{"n":0,"w":0,"pnl":0.0},
                        "786_ema_short_with":{"n":0,"w":0,"pnl":0.0}}

    for sym in SYMBOLS:
        df = load(sym)
        if df is None or len(df) < 300: continue
        # Wedge tests
        for params in wedge_params:
            r = test_wedges_param(df, *params)
            for k in ("falling_long","rising_short"):
                for kk in ("n","w","pnl"):
                    wedge_grids[params][k][kk] += r[k][kk]
        # EMA tests
        for ep in [50, 100, 200]:
            r = test_786_ema(df, ep)
            for k in ("786_ema_long_with","786_ema_short_with"):
                for kk in ("n","w","pnl"):
                    ema_grid[ep][k][kk] += r[k][kk]
        print(f"  {sym}: done")

    print(f"\nElapsed: {time.time()-t0:.1f}s")

    # ===== REPORT WEDGES =====
    print()
    print("="*80)
    print("WEDGE PARAMETER ROBUSTNESS — 90d × 12 symbols")
    print("="*80)
    print(f"{'lookback':<10}{'pivot_w':<10}{'break_buf':<10}{'side':<14}{'n':>5}{'WR%':>7}{'avg %':>10}")
    print("-"*80)
    for params, results in wedge_grids.items():
        lb, pw, bb = params
        for k in ("falling_long","rising_short"):
            d = results[k]
            if d["n"] == 0:
                print(f"{lb:<10}{pw:<10}{bb:<10}{k:<14}  no signals"); continue
            wr = d["w"]/d["n"]*100
            avg = d["pnl"]/d["n"]
            print(f"{lb:<10}{pw:<10}{bb:<10}{k:<14}{d['n']:>5}{wr:>6.1f}%{avg:>+9.3f}%")

    # ===== REPORT 0.786 + EMA =====
    print()
    print("="*80)
    print("0.786 + EMA TREND ROBUSTNESS")
    print("="*80)
    print(f"{'ema_period':<14}{'side':<25}{'n':>6}{'WR%':>7}{'sum %':>9}{'avg %':>10}")
    print("-"*80)
    for ep, results in ema_grid.items():
        for k in ("786_ema_long_with","786_ema_short_with"):
            d = results[k]
            if d["n"] == 0:
                print(f"{ep:<14}{k:<25}  no signals"); continue
            wr = d["w"]/d["n"]*100
            avg = d["pnl"]/d["n"]
            print(f"{ep:<14}{k:<25}{d['n']:>6}{wr:>6.1f}%{d['pnl']:>+8.1f}%{avg:>+9.3f}%")

if __name__ == "__main__":
    run()
