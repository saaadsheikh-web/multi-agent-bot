#!/usr/bin/env python3
"""
Advanced Fibonacci backtest — test what the research said might work.

Tests:
  TEST 1: Less-common single ratios (0.236, 0.786, 0.886, 1.272)
  TEST 2: 0.786 + RSI<30 (deep retrace + oversold confluence)
  TEST 3: 0.236 momentum continuation (with-trend only)
  TEST 4: Multi-timeframe Fib confluence (1H + 4H from resampled bars)
  TEST 5: Anchored Fib from major period high/low (90-day anchor)
  TEST 6: Fibonacci EMA Ribbon stack (8/13/21/34/55/89 alignment)

Period: 90 days, 12 symbols, 1H bars. Fees 0.04% round-trip. TP 2.0%/SL 1.0%/24-bar timeout.
"""
import os
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

# ============================================================================
# TEST 1 — Less-common single ratios
# ============================================================================
def test_uncommon_ratios(df, lookback=50, proximity=0.003):
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    for i in range(lookback+5, len(df)-5):
        if i - last_fire < 12: continue
        wh = df["high"].iloc[i-lookback:i].max()
        wl = df["low"].iloc[i-lookback:i].min()
        if wh <= wl or (wh-wl)/wl < 0.02: continue
        sh_idx = df["high"].iloc[i-lookback:i].idxmax()
        sl_idx = df["low"].iloc[i-lookback:i].idxmin()
        upt = sh_idx > sl_idx
        move = wh - wl
        last = df["close"].iloc[i]
        # Test these levels
        for level in [0.236, 0.786, 0.886]:
            fp = (wh - move*level) if upt else (wl + move*level)
            if abs(last - fp)/fp < proximity:
                # Standard interpretation: bounce in trend
                side = "long" if upt else "short"
                _, ex = simulate(df, i, side, 2.0, 1.0)
                pct = pct_pnl(side, last, ex)
                k = f"{level:.3f}"
                res[k]["n"] += 1
                if pct > 0: res[k]["w"] += 1
                res[k]["pnl"] += pct
                last_fire = i; break
        # 1.272 extension — use as REVERSAL signal (overshoot of swing)
        for level in [1.272]:
            fp = (wh + (wh - wl)*(level - 1.0)) if upt else (wl - (wh - wl)*(level - 1.0))
            if abs(last - fp)/fp < proximity:
                side = "short" if upt else "long"
                _, ex = simulate(df, i, side, 2.0, 1.0)
                pct = pct_pnl(side, last, ex)
                k = f"{level:.3f}_rev"
                res[k]["n"] += 1
                if pct > 0: res[k]["w"] += 1
                res[k]["pnl"] += pct
                last_fire = i; break
    return res

# ============================================================================
# TEST 2 — 0.786 + RSI confluence
# ============================================================================
def test_786_rsi(df, lookback=50, proximity=0.004):
    res = {"786_oversold_long":{"n":0,"w":0,"pnl":0.0}, "786_overbought_short":{"n":0,"w":0,"pnl":0.0}}
    last_fire = -100
    for i in range(lookback+15, len(df)-5):
        if i - last_fire < 12: continue
        wh = df["high"].iloc[i-lookback:i].max()
        wl = df["low"].iloc[i-lookback:i].min()
        if wh <= wl or (wh-wl)/wl < 0.025: continue
        sh_idx = df["high"].iloc[i-lookback:i].idxmax()
        sl_idx = df["low"].iloc[i-lookback:i].idxmin()
        upt = sh_idx > sl_idx
        move = wh - wl
        fp_786 = (wh - move*0.786) if upt else (wl + move*0.786)
        last = df["close"].iloc[i]
        if abs(last - fp_786)/fp_786 >= proximity: continue
        r = rsi(df["close"].iloc[:i+1], 14).iloc[-1]
        if pd.isna(r): continue
        if upt and r < 30:
            _, ex = simulate(df, i, "long", 2.5, 1.5)
            pct = pct_pnl("long", last, ex)
            res["786_oversold_long"]["n"] += 1
            if pct > 0: res["786_oversold_long"]["w"] += 1
            res["786_oversold_long"]["pnl"] += pct
            last_fire = i
        elif not upt and r > 70:
            _, ex = simulate(df, i, "short", 2.5, 1.5)
            pct = pct_pnl("short", last, ex)
            res["786_overbought_short"]["n"] += 1
            if pct > 0: res["786_overbought_short"]["w"] += 1
            res["786_overbought_short"]["pnl"] += pct
            last_fire = i
    return res

# ============================================================================
# TEST 3 — 0.236 momentum continuation (shallow retrace = strong trend)
# ============================================================================
def test_236_continuation(df, lookback=30, proximity=0.003):
    res = {"236_with_trend":{"n":0,"w":0,"pnl":0.0}}
    last_fire = -100
    for i in range(lookback+50, len(df)-5):
        if i - last_fire < 12: continue
        wh = df["high"].iloc[i-lookback:i].max()
        wl = df["low"].iloc[i-lookback:i].min()
        if wh <= wl or (wh-wl)/wl < 0.02: continue
        sh_idx = df["high"].iloc[i-lookback:i].idxmax()
        sl_idx = df["low"].iloc[i-lookback:i].idxmin()
        upt = sh_idx > sl_idx
        move = wh - wl
        fp = (wh - move*0.236) if upt else (wl + move*0.236)
        last = df["close"].iloc[i]
        if abs(last - fp)/fp >= proximity: continue
        # Confirm trend with EMA50
        e50 = ema(df["close"].iloc[:i+1], 50).iloc[-1]
        if pd.isna(e50): continue
        if upt and last > e50:
            _, ex = simulate(df, i, "long", 1.5, 0.8)
            pct = pct_pnl("long", last, ex)
            res["236_with_trend"]["n"] += 1
            if pct > 0: res["236_with_trend"]["w"] += 1
            res["236_with_trend"]["pnl"] += pct
            last_fire = i
        elif not upt and last < e50:
            _, ex = simulate(df, i, "short", 1.5, 0.8)
            pct = pct_pnl("short", last, ex)
            res["236_with_trend"]["n"] += 1
            if pct > 0: res["236_with_trend"]["w"] += 1
            res["236_with_trend"]["pnl"] += pct
            last_fire = i
    return res

# ============================================================================
# TEST 4 — Multi-timeframe Fib confluence (1H + pseudo-4H)
# ============================================================================
def test_mtf_confluence(df, proximity=0.003, cluster_pct=0.003):
    """Compute Fibs from 1H last-50-bar swing AND pseudo-4H last-50-bar swing.
    If a 1H Fib and a 4H Fib are within 0.3% of each other AND price is within 0.3% of
    that cluster, simulate. This is true MTF confluence."""
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    fib_levels = [0.236, 0.382, 0.500, 0.618, 0.786]
    # Build pseudo-4H by sampling every 4 bars
    df4 = df.iloc[::4].reset_index(drop=True)
    for i in range(250, len(df)-5):
        if i - last_fire < 12: continue
        # 1H Fibs (last 50 bars)
        wh1 = df["high"].iloc[i-50:i].max(); wl1 = df["low"].iloc[i-50:i].min()
        if wh1 <= wl1 or (wh1-wl1)/wl1 < 0.02: continue
        sh1 = df["high"].iloc[i-50:i].idxmax(); sl1_ = df["low"].iloc[i-50:i].idxmin()
        upt1 = sh1 > sl1_; m1 = wh1 - wl1
        fibs1h = [(wh1 - m1*f) if upt1 else (wl1 + m1*f) for f in fib_levels]
        # pseudo-4H Fibs (last 50 4H-bars from df4)
        i4 = i // 4
        if i4 < 50: continue
        wh4 = df4["high"].iloc[i4-50:i4].max() if i4-50 >= 0 else None
        wl4 = df4["low"].iloc[i4-50:i4].min() if i4-50 >= 0 else None
        if wh4 is None or wl4 is None or wh4 <= wl4 or (wh4-wl4)/wl4 < 0.025: continue
        sh4 = df4["high"].iloc[i4-50:i4].idxmax(); sl4_ = df4["low"].iloc[i4-50:i4].idxmin()
        upt4 = sh4 > sl4_; m4 = wh4 - wl4
        fibs4h = [(wh4 - m4*f) if upt4 else (wl4 + m4*f) for f in fib_levels]
        last = df["close"].iloc[i]
        # Find 1H/4H pairs within cluster_pct of each other AND price within proximity
        for f1 in fibs1h:
            for f4 in fibs4h:
                if abs(f1 - f4)/f4 < cluster_pct:
                    cluster_mean = (f1 + f4) / 2
                    if abs(last - cluster_mean)/cluster_mean < proximity:
                        # MTF cluster confirmed at this price
                        side = "long" if last > cluster_mean else "short"
                        # Use 1H trend direction for side
                        side = "long" if upt1 else "short"
                        _, ex = simulate(df, i, side, 2.5, 1.5)
                        pct = pct_pnl(side, last, ex)
                        k = "MTF_2tf_cluster"
                        res[k]["n"] += 1
                        if pct > 0: res[k]["w"] += 1
                        res[k]["pnl"] += pct
                        last_fire = i
                        break
            if i == last_fire: break
    return res

# ============================================================================
# TEST 5 — Anchored Fibonacci (90-day period high/low)
# ============================================================================
def test_anchored(df, proximity=0.003):
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    fib_levels = [0.236, 0.382, 0.500, 0.618, 0.786]
    for i in range(50, len(df)-5):
        if i - last_fire < 12: continue
        # Anchor: highest high and lowest low in ENTIRE period before bar i
        anchor_high = df["high"].iloc[:i].max()
        anchor_low = df["low"].iloc[:i].min()
        if anchor_high <= anchor_low: continue
        if (anchor_high - anchor_low)/anchor_low < 0.05: continue   # need meaningful range
        m = anchor_high - anchor_low
        last = df["close"].iloc[i]
        # Test bounce at each fib level (anchored)
        for level in fib_levels:
            fp_up = anchor_high - m * level    # retracement from anchored high
            if abs(last - fp_up)/fp_up < proximity:
                # This is "price retraced 38.2% from the period high" → bounce play
                _, ex = simulate(df, i, "long", 2.5, 1.5)
                pct = pct_pnl("long", last, ex)
                k = f"anchored_{level:.3f}"
                res[k]["n"] += 1
                if pct > 0: res[k]["w"] += 1
                res[k]["pnl"] += pct
                last_fire = i; break
    return res

# ============================================================================
# TEST 6 — Fib EMA Ribbon stack alignment
# ============================================================================
def test_fib_ema_stack(df):
    """When 8 > 13 > 21 > 34 > 55 > 89 EMAs (ascending stack) = strong uptrend.
    Pullback to 21-EMA = entry. Reverse for downtrend."""
    res = {"fib_ema_uptrend_pullback":{"n":0,"w":0,"pnl":0.0},
           "fib_ema_downtrend_pullback":{"n":0,"w":0,"pnl":0.0}}
    last_fire = -100
    c = df["close"]
    e8 = ema(c, 8); e13 = ema(c, 13); e21 = ema(c, 21)
    e34 = ema(c, 34); e55 = ema(c, 55); e89 = ema(c, 89)
    for i in range(150, len(df)-5):
        if i - last_fire < 12: continue
        v8 = e8.iloc[i]; v13 = e13.iloc[i]; v21 = e21.iloc[i]
        v34 = e34.iloc[i]; v55 = e55.iloc[i]; v89 = e89.iloc[i]
        if any(pd.isna([v8,v13,v21,v34,v55,v89])): continue
        last = c.iloc[i]
        # Strong uptrend: fully ascending stack
        if v8 > v13 > v21 > v34 > v55 > v89:
            # Pullback to 21-EMA (within 0.4%) = entry
            if abs(last - v21)/v21 < 0.004:
                _, ex = simulate(df, i, "long", 2.0, 1.0)
                pct = pct_pnl("long", last, ex)
                res["fib_ema_uptrend_pullback"]["n"] += 1
                if pct > 0: res["fib_ema_uptrend_pullback"]["w"] += 1
                res["fib_ema_uptrend_pullback"]["pnl"] += pct
                last_fire = i
        elif v8 < v13 < v21 < v34 < v55 < v89:
            if abs(last - v21)/v21 < 0.004:
                _, ex = simulate(df, i, "short", 2.0, 1.0)
                pct = pct_pnl("short", last, ex)
                res["fib_ema_downtrend_pullback"]["n"] += 1
                if pct > 0: res["fib_ema_downtrend_pullback"]["w"] += 1
                res["fib_ema_downtrend_pullback"]["pnl"] += pct
                last_fire = i
    return res

# ============================================================================
# RUN
# ============================================================================
def run():
    g1 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g2 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g3 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g4 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g5 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g6 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    for sym in SYMBOLS:
        df = load(sym)
        if df is None or len(df) < 300: continue
        for src, tgt in [(test_uncommon_ratios(df), g1),
                          (test_786_rsi(df), g2),
                          (test_236_continuation(df), g3),
                          (test_mtf_confluence(df), g4),
                          (test_anchored(df), g5),
                          (test_fib_ema_stack(df), g6)]:
            for k, v in src.items():
                for kk in ("n","w","pnl"):
                    tgt[k][kk] += v[kk]
        print(f"  {sym}: done")

    def report(title, results):
        print()
        print("="*72)
        print(title)
        print("="*72)
        print(f"{'setup':<28}{'n':>6}{'WR%':>7}{'sum %':>9}{'avg %':>10}{'$/100':>9}")
        print("-"*72)
        for k in sorted(results.keys()):
            d = results[k]
            if d["n"] == 0:
                print(f"  {k:<26} no signals"); continue
            wr = d["w"]/d["n"]*100
            avg = d["pnl"]/d["n"]
            verdict = "✅" if avg > 0.05 else ("⚠️" if avg > 0 else "❌")
            print(f"  {k:<26}{d['n']:>6}{wr:>6.1f}%{d['pnl']:>+8.1f}%{avg:>+9.3f}%{avg:>+9.3f} {verdict}")

    report("TEST 1 — UNCOMMON RATIOS (0.236, 0.786, 0.886, 1.272-rev)", g1)
    report("TEST 2 — 0.786 + RSI EXTREME", g2)
    report("TEST 3 — 0.236 MOMENTUM CONTINUATION (with EMA50 trend)", g3)
    report("TEST 4 — MULTI-TIMEFRAME FIB CONFLUENCE (1H + pseudo-4H)", g4)
    report("TEST 5 — ANCHORED FIB (90-day period high/low)", g5)
    report("TEST 6 — FIB EMA RIBBON STACK PULLBACK (8/13/21/34/55/89)", g6)

if __name__ == "__main__":
    run()
