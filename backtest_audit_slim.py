#!/usr/bin/env python3
"""SLIM AUDIT — out-of-sample wedge + statistical significance + slippage."""
import os, time
import pandas as pd, numpy as np
from scipy import stats

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT","AVAX-USDT","ADA-USDT","LINK-USDT"]
DAYS = 90

def load(sym):
    f = os.path.join(CACHE, f"{sym.replace('-','_')}_1H_365d.parquet")
    if not os.path.exists(f): return None
    df = pd.read_parquet(f); df.columns = [c.lower() for c in df.columns]
    return df.iloc[-DAYS*24:].reset_index(drop=True)

def find_pivots(h, l, w=3):
    highs, lows = [], []
    n = len(h)
    for k in range(w, n-w):
        if h[k] == max(h[k-w:k+w+1]): highs.append((k, h[k]))
        elif l[k] == min(l[k-w:k+w+1]): lows.append((k, l[k]))
    return highs, lows

def sim(df, i, side, slip=0.0, fee=0.04):
    e = df["close"].iloc[i]
    e *= (1+slip/100) if side=="long" else (1-slip/100)
    if side=="long": tp, sl = e*1.02, e*0.99
    else: tp, sl = e*0.98, e*1.01
    end = min(i+24, len(df)-1)
    for j in range(i+1, end+1):
        h, l = df["high"].iloc[j], df["low"].iloc[j]
        if side=="long":
            if l <= sl: ex = sl*(1-slip/100); break
            if h >= tp: ex = tp*(1-slip/100); break
        else:
            if h >= sl: ex = sl*(1+slip/100); break
            if l <= tp: ex = tp*(1+slip/100); break
    else:
        ex = float(df["close"].iloc[end])
        ex *= (1-slip/100) if side=="long" else (1+slip/100)
    p = (ex-e)/e*100 if side=="long" else (e-ex)/e*100
    return p - fee

def wedge_pcts(df, lookback, pw, bb, start=None, end=None, slip=0.0, fee=0.04):
    pcts = []
    last_fire = -100
    h, l = df["high"].values, df["low"].values
    fmin = max(lookback+10, start or 0)
    fmax = min(end or len(df), len(df)-5)
    for i in range(fmin, fmax):
        if i - last_fire < 24: continue
        ha, la = h[i-lookback:i], l[i-lookback:i]
        highs, lows = find_pivots(ha, la, pw)
        if len(highs)<3 or len(lows)<3: continue
        hx = np.array([p[0] for p in highs]); hy = np.array([p[1] for p in highs])
        lx = np.array([p[0] for p in lows]);  ly = np.array([p[1] for p in lows])
        hs, hi = np.polyfit(hx, hy, 1)
        ls, li = np.polyfit(lx, ly, 1)
        last = df["close"].iloc[i]
        side = None
        if hs > 0 and ls > 0 and hs < ls:
            if last < (ls*lookback + li) * (1-bb): side = "short"
        elif hs < 0 and ls < 0 and hs < ls:
            if last > (hs*lookback + hi) * (1+bb): side = "long"
        if side is None: continue
        pcts.append(sim(df, i, side, slip, fee))
        last_fire = i
    return pcts

def stats_summary(pcts):
    if not pcts: return None
    a = np.array(pcts); n = len(a)
    wr = (a>0).sum()/n*100; avg = a.mean(); std = a.std()
    se = std / np.sqrt(n) if n else 0
    t, p = stats.ttest_1samp(a, 0) if n > 1 else (0, 1)
    return {"n":n, "wr":wr, "avg":avg, "ci_lo":avg-1.96*se, "ci_hi":avg+1.96*se, "t":t, "p":p}

t0 = time.time()
print("="*70)
print("AUDIT — true OUT-OF-SAMPLE wedge test")
print("="*70)
print("Optimize on Days 1-60 → validate on Days 61-90 (UNSEEN)")
print()

train_end = 60*24; val_start = train_end; val_end = 90*24

# Param grids — small to be honest
LONG_GRID = [(40,3,0.001),(50,3,0.002),(60,3,0.002)]
SHORT_GRID = [(50,3,0.002),(60,3,0.002),(70,4,0.002)]

print("--- TRAIN scan (Days 1-60) ---")
best_long, best_long_avg = None, -999
best_short, best_short_avg = None, -999
for params in LONG_GRID:
    pcts = []
    for s in SYMBOLS:
        df = load(s)
        if df is None: continue
        pcts.extend(wedge_pcts(df, *params, end=train_end))
    sm = stats_summary(pcts)
    if sm:
        print(f"  long {params}: n={sm['n']} WR={sm['wr']:.1f}% avg={sm['avg']:+.3f}%")
        if sm["avg"] > best_long_avg:
            best_long_avg = sm["avg"]; best_long = params

for params in SHORT_GRID:
    pcts = []
    for s in SYMBOLS:
        df = load(s)
        if df is None: continue
        pcts.extend(wedge_pcts(df, *params, end=train_end))
    sm = stats_summary(pcts)
    if sm:
        print(f"  short {params}: n={sm['n']} WR={sm['wr']:.1f}% avg={sm['avg']:+.3f}%")
        if sm["avg"] > best_short_avg:
            best_short_avg = sm["avg"]; best_short = params

print(f"\n  Selected best LONG params: {best_long} (train avg {best_long_avg:+.3f}%)")
print(f"  Selected best SHORT params: {best_short} (train avg {best_short_avg:+.3f}%)")

print("\n--- OUT-OF-SAMPLE VALIDATION (Days 61-90, UNSEEN) ---")
oos_long_pcts, oos_short_pcts = [], []
for s in SYMBOLS:
    df = load(s)
    if df is None: continue
    oos_long_pcts.extend(wedge_pcts(df, *best_long, start=val_start, end=val_end))
    oos_short_pcts.extend(wedge_pcts(df, *best_short, start=val_start, end=val_end))
sL = stats_summary(oos_long_pcts)
sS = stats_summary(oos_short_pcts)

def verdict(s):
    if not s: return "no signals"
    sig = "✅ SIGNIFICANT" if s["p"] < 0.05 else ("⚠️ marginal" if s["p"] < 0.10 else "❌ noise")
    return (f"n={s['n']}  WR={s['wr']:.1f}%  avg={s['avg']:+.3f}%  "
            f"95%CI=[{s['ci_lo']:+.3f},{s['ci_hi']:+.3f}]  p={s['p']:.3f}  {sig}")

print(f"  LONG  OOS:  {verdict(sL)}")
print(f"  SHORT OOS:  {verdict(sS)}")

print("\n--- SLIPPAGE STRESS (full 90d, validated params) ---")
for slip in [0.0, 0.05, 0.10]:
    L_pcts, S_pcts = [], []
    for s in SYMBOLS:
        df = load(s)
        if df is None: continue
        L_pcts.extend(wedge_pcts(df, *best_long, slip=slip))
        S_pcts.extend(wedge_pcts(df, *best_short, slip=slip))
    sL = stats_summary(L_pcts); sS = stats_summary(S_pcts)
    print(f"  slip={slip:.2f}%  LONG: n={sL['n']:>3} avg={sL['avg']:+.3f}%   SHORT: n={sS['n']:>3} avg={sS['avg']:+.3f}%")

print("\n--- FEE STRESS (taker scenario 0.12% round-trip) ---")
for fee in [0.04, 0.08, 0.12]:
    L_pcts, S_pcts = [], []
    for s in SYMBOLS:
        df = load(s)
        if df is None: continue
        L_pcts.extend(wedge_pcts(df, *best_long, fee=fee))
        S_pcts.extend(wedge_pcts(df, *best_short, fee=fee))
    sL = stats_summary(L_pcts); sS = stats_summary(S_pcts)
    print(f"  fee={fee:.2f}%  LONG: n={sL['n']:>3} avg={sL['avg']:+.3f}%   SHORT: n={sS['n']:>3} avg={sS['avg']:+.3f}%")

print(f"\nElapsed: {time.time()-t0:.1f}s")
