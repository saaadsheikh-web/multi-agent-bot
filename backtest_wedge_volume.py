#!/usr/bin/env python3
"""Does volume confirmation rescue wedge OOS edge?
Test wedge breaks with vs without volume filter, IS and OOS."""
import os, time
import pandas as pd, numpy as np
from scipy import stats

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT","AVAX-USDT","ADA-USDT","LINK-USDT"]
DAYS = 90; FEE = 0.04

def load(s):
    f = os.path.join(CACHE, f"{s.replace('-','_')}_1H_365d.parquet")
    if not os.path.exists(f): return None
    df = pd.read_parquet(f); df.columns = [c.lower() for c in df.columns]
    return df.iloc[-DAYS*24:].reset_index(drop=True)

def find_pivots(h, l, w=3):
    highs, lows = [], []; n = len(h)
    for k in range(w, n-w):
        if h[k] == max(h[k-w:k+w+1]): highs.append((k, h[k]))
        elif l[k] == min(l[k-w:k+w+1]): lows.append((k, l[k]))
    return highs, lows

def sim(df, i, side):
    e = df["close"].iloc[i]
    if side == "long": tp, sl = e*1.02, e*0.99
    else: tp, sl = e*0.98, e*1.01
    end = min(i+24, len(df)-1)
    for j in range(i+1, end+1):
        h, l = df["high"].iloc[j], df["low"].iloc[j]
        if side=="long":
            if l <= sl: return (sl - e)/e*100 - FEE
            if h >= tp: return (tp - e)/e*100 - FEE
        else:
            if h >= sl: return (e - sl)/e*100 - FEE
            if l <= tp: return (e - tp)/e*100 - FEE
    ex = float(df["close"].iloc[end])
    if side == "long": return (ex - e)/e*100 - FEE
    return (e - ex)/e*100 - FEE

def wedge_pcts(df, lookback=50, pw=3, bb=0.002, vol_min=1.0, start=None, end=None):
    pcts = []
    last_fire = -100
    h_full, l_full, v_full = df["high"].values, df["low"].values, df["volume"].values
    fmin = max(lookback+10, start or 0); fmax = min(end or len(df), len(df)-5)
    for i in range(fmin, fmax):
        if i - last_fire < 24: continue
        ha, la = h_full[i-lookback:i], l_full[i-lookback:i]
        highs, lows = find_pivots(ha, la, pw)
        if len(highs)<3 or len(lows)<3: continue
        hx = np.array([p[0] for p in highs]); hy = np.array([p[1] for p in highs])
        lx = np.array([p[0] for p in lows]);  ly = np.array([p[1] for p in lows])
        hs, hi = np.polyfit(hx, hy, 1)
        ls, li = np.polyfit(lx, ly, 1)
        last = df["close"].iloc[i]
        # Volume on break bar — must exceed avg by vol_min ratio
        avg_v = v_full[max(0,i-20):i].mean()
        if avg_v <= 0: continue
        v_ratio = v_full[i] / avg_v
        if v_ratio < vol_min: continue
        side = None
        if hs > 0 and ls > 0 and hs < ls:
            if last < (ls*lookback + li) * (1-bb): side = "short"
        elif hs < 0 and ls < 0 and hs < ls:
            if last > (hs*lookback + hi) * (1+bb): side = "long"
        if side is None: continue
        pcts.append(sim(df, i, side))
        last_fire = i
    return pcts

def stat(pcts):
    if not pcts: return None
    a = np.array(pcts); n = len(a)
    wr = (a>0).sum()/n*100; avg = a.mean(); std = a.std()
    se = std/np.sqrt(n) if n else 0
    t, p = stats.ttest_1samp(a, 0) if n>1 else (0, 1)
    return {"n":n, "wr":wr, "avg":avg, "ci_lo":avg-1.96*se, "ci_hi":avg+1.96*se, "t":t, "p":p}

t0 = time.time()
print("="*72)
print("DOES VOLUME CONFIRMATION RESCUE WEDGE OOS EDGE?")
print("="*72)
print("Test wedge break with vol_min ratio. Train Days 1-60, validate 61-90.")
print()

train_end = 60*24; val_start = train_end; val_end = 90*24

for vol_min in [1.0, 1.2, 1.5, 2.0]:
    is_pcts, oos_pcts = [], []
    for s in SYMBOLS:
        df = load(s)
        if df is None: continue
        is_pcts.extend(wedge_pcts(df, vol_min=vol_min, end=train_end))
        oos_pcts.extend(wedge_pcts(df, vol_min=vol_min, start=val_start, end=val_end))
    sIS = stat(is_pcts); sOOS = stat(oos_pcts)
    print(f"vol_min={vol_min}:")
    if sIS:
        print(f"  IN-SAMPLE  : n={sIS['n']:>3}  WR={sIS['wr']:.1f}%  avg={sIS['avg']:+.3f}%  p={sIS['p']:.3f}")
    if sOOS:
        verdict = "✅ SIGNIFICANT" if sOOS['p']<0.05 else ("⚠️ marginal" if sOOS['p']<0.10 else "❌ noise")
        print(f"  OUT-SAMPLE : n={sOOS['n']:>3}  WR={sOOS['wr']:.1f}%  avg={sOOS['avg']:+.3f}%  "
              f"95%CI=[{sOOS['ci_lo']:+.3f},{sOOS['ci_hi']:+.3f}]  p={sOOS['p']:.3f}  {verdict}")
    print()

print(f"Elapsed: {time.time()-t0:.1f}s")
