#!/usr/bin/env python3
"""
DEEP RESEARCH AGENT — Runs 24/7 in background.
Creates new strategies, backtests them on ALL timeframes ALL coins.
Only notifies when it finds something with 80%+ WR or game-changing profit.
Silent otherwise. No spam.
"""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime
import itertools, random, time

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")
OUT = os.path.expanduser("~/multi_agent_bot/RESEARCH_FINDINGS.json")

def load(sym, tf):
    f = os.path.join(CACHE, f"{sym.replace('-','_')}_{tf}_365d.parquet")
    if not os.path.exists(f): return None
    df = pd.read_parquet(f)
    df.columns = [c.lower() for c in df.columns]
    return df.sort_values("ts").reset_index(drop=True)

class Data:
    def __init__(self, df):
        c=df["close"].values; h=df["high"].values; l=df["low"].values; v=df["volume"].values
        self.c=c;self.h=h;self.l=l;self.v=v;self.ts=df["ts"].values;self.n=len(c)
        pc=pd.Series(c).shift(1)
        tr=pd.concat([(pd.Series(h)-pd.Series(l)).abs(),(pd.Series(h)-pc).abs(),(pd.Series(l)-pc).abs()],axis=1).max(axis=1)
        self.atr=tr.rolling(14).mean().values; self.vma=pd.Series(v).rolling(20).mean().values
        delta=pd.Series(c).diff(); up=delta.where(delta>0,0).rolling(14).mean()
        dn=(-delta.where(delta<0,0)).rolling(14).mean()
        self.rsi=(100-100/(1+up/dn)).values
        self.e50=pd.Series(c).ewm(span=50,adjust=False).mean().values
        self.e200=pd.Series(c).ewm(span=200,adjust=False).mean().values

def sim(trades, d):
    if not trades: return None
    c=d.c;h=d.h;l=d.h;pnl_vals=[];r_vals=[]
    for t in trades:
        idx=t["i"];side=t["s"];entry=t["e"];tp=t["tp"];sl=t["sl"]
        active=False;out=None;ex=None;j=idx+1
        while j<min(idx+480,d.n):
            if side=="L":
                if l[j]<=sl: out="L"; ex=sl; break
                if h[j]>=tp: out="W"; ex=tp; break
                if not active and c[j]>=entry*(1+0.008): active=True
                if active:
                    ns=c[j]*(1-0.008)
                    if ns>sl: sl=ns
                    if l[j]<=sl: out="W"; ex=sl; break
            else:
                if h[j]>=sl: out="L"; ex=sl; break
                if l[j]<=tp: out="W"; ex=tp; break
                if not active and c[j]<=entry*(1-0.008): active=True
                if active:
                    ns=c[j]*(1+0.008)
                    if ns<sl: sl=ns
                    if h[j]>=sl: out="W"; ex=sl; break
            j+=1
        if out is None: out="L"; ex=c[min(idx+480,d.n-1)]
        pnl=((ex-entry)/entry if side=="L" else (entry-ex)/entry)-0.0004
        pnl_vals.append(pnl*100)
    w=sum(1 for v in pnl_vals if v>0); nn=len(pnl_vals)
    return {"n":nn,"w":w,"wr":round(w/nn*100,1),"tp":round(sum(pnl_vals),2)}

# ===== STRATEGY GENERATOR =====
def test_breakout_variant(d, lb, vm, sl, trail_act, trail_dist):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(lb+30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-lb; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vm: continue
        bo=c[i-1]; br=h[i]-l[i]; last=c[i]
        if br<=0: continue
        if last>rh and last>bo:
            sr=bo+br*0.5; sf=last*(1-sl/100)
            tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":min(sr,sf)})
        elif last<rl and last<bo:
            sr=bo-br*0.5; sf=last*(1+sl/100)
            tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

def test_rsi_strategy(d, rsi_low, rsi_high, vol_min, trend_filter=True):
    c=d.c;v=d.v;n=d.n;vma=d.vma;rsi=d.rsi;e50=d.e50;e200=d.e200;tr=[]
    for i in range(100, n):
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vol_min: continue
        r=rsi[i] if not np.isnan(rsi[i]) else 50
        last=c[i]
        if trend_filter:
            up=last>e50[i]>e200[i]; dn=last<e50[i]<e200[i]
        else: up=dn=True
        if r<rsi_low and up:
            tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":last*0.985})
        elif r>rsi_high and dn:
            tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":last*1.015})
    return tr

def test_ema_cross(d, fast, slow, vol_min):
    c=d.c;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    ef=pd.Series(c).ewm(span=fast,adjust=False).mean().values
    es=pd.Series(c).ewm(span=slow,adjust=False).mean().values
    for i in range(100, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vol_min: continue
        if ef[i-1]<=es[i-1] and ef[i]>es[i] and c[i]>ef[i]:
            tr.append({"i":i,"s":"L","e":c[i],"tp":c[i]*99,"sl":c[i]-atr[i]*2})
        elif ef[i-1]>=es[i-1] and ef[i]<es[i] and c[i]<ef[i]:
            tr.append({"i":i,"s":"S","e":c[i],"tp":c[i]*0.01,"sl":c[i]+atr[i]*2})
    return tr

TFS = ["5m","15m","30m","1H"]
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMS = sorted(coin_tfs.keys())

print(f"🧪 DEEP RESEARCH STARTED — {datetime.now()}")
print(f"Testing on {len(SYMS)} coins x {len(TFS)} TFs")

findings = []
batch = 0

# BREAKOUT SWEEP — all combos
for lb in [2,4,8,12,24,48,72,120]:
    for vm in [1.2,1.5,2.0]:
        for sl in [0.5,1.0,1.5,2.0,3.0,5.0]:
            batch += 1
            for tf in TFS:
                total=0; wins=0; pnl=0; prof=0; tot=0
                for sym in SYMS[:10]:  # Test on top 10 coins first
                    if tf not in coin_tfs[sym]: continue
                    df = load(sym, tf)
                    if df is None: continue
                    d = Data(df)
                    trades = test_breakout_variant(d, lb, vm, sl, 0.008, 0.008)
                    st = sim(trades, d)
                    if st and st["n"]>5:
                        tot+=1; total+=st["n"]; wins+=st["w"]; pnl+=st["tp"]
                        if st["wr"]>50: prof+=1
                if total>50:
                    wr=wins/total*100 if total else 0
                    if wr >= 80 or pnl > 500:
                        findings.append({"type":"breakout","params":f"LB={lb}h VM={vm}x SL={sl}%","tf":tf,"trades":total,"wr":round(wr,1),"pnl":round(pnl,2),"prof":f"{prof}/{tot}"})

# RSI SWEEP
for rl in [10,15,20,25]:
    for rh in [75,80,85,90]:
        for vm in [1.2,1.5,2.0]:
            batch += 1
            for tf in ["15m","1H"]:
                total=0; wins=0; pnl=0; prof=0; tot=0
                for sym in SYMS[:10]:
                    if tf not in coin_tfs[sym]: continue
                    df = load(sym, tf)
                    if df is None: continue
                    d = Data(df)
                    trades = test_rsi_strategy(d, rl, rh, vm)
                    st = sim(trades, d)
                    if st and st["n"]>5:
                        tot+=1; total+=st["n"]; wins+=st["w"]; pnl+=st["tp"]
                        if st["wr"]>50: prof+=1
                if total>20:
                    wr=wins/total*100 if total else 0
                    if wr >= 80:
                        findings.append({"type":"rsi","params":f"RSI<{rl} >{rh} Vol>{vm}x","tf":tf,"trades":total,"wr":round(wr,1),"pnl":round(pnl,2),"prof":f"{prof}/{tot}"})

print(f"\n{'='*65}")
print(f"  RESEARCH COMPLETE — {len(findings)} game-changing findings")
print(f"{'='*65}")
findings.sort(key=lambda x: x["wr"], reverse=True)
for f in findings[:20]:
    print(f"  🏆 {f['type']:10s} {f['params']:30s} {f['tf']:5s} {f['trades']:6d}t {f['wr']:5.1f}% ${f['pnl']:8.2f} ({f['prof']})")

with open(OUT,"w") as f: json.dump(findings,f,indent=2)
print(f"\nSaved to {OUT}")
