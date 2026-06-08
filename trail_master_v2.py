#!/usr/bin/env python3
"""
TRAIL MASTER v2 — Learns optimal trail for EVERY strategy on EVERY timeframe.
Tests: no trail, fixed %, ATR-based, step trail, percentage of max profit.
Finds the BEST trail for each strategy individually.
Uses our backtest winners: B4h 5m, B12h 1H, fib_ext 15m, breakouts.
"""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")
OUT = os.path.expanduser("~/multi_agent_bot/trail_master_v2_results.json")

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

# ===== STRATEGIES =====
def b4h_5m(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(34,d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-4; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.3: continue
        bo=c[i-1]; br=h[i]-l[i]
        if br<=0: continue
        last=c[i]
        if last>rh and last>bo:
            sr=bo+br*0.5; sf=last*(1-0.012)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*99,"sl":min(sr,sf)})
        elif last<rl and last<bo:
            sr=bo-br*0.5; sf=last*(1+0.012)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

def b12h_1h(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(42,d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-12; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.5: continue
        bo=c[i-1]; br=h[i]-l[i]
        if br<=0: continue
        last=c[i]
        if last>rh and last>bo:
            sr=bo+br*0.5; sf=last*(1-0.018)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*99,"sl":min(sr,sf)})
        elif last<rl and last<bo:
            sr=bo-br*0.5; sf=last*(1+0.018)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

def fib_ext_15m(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(100,d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=max(0,i-100);sh=np.max(h[lo:i]);sll=np.min(l[lo:i])
        if sh==sll: continue
        df_=sh-sll;ext=sll+1.272*df_;ext_s=sh-1.272*df_
        last=c[i];vr=v[i]/vma[i] if vma[i]>0 else 0
        if last>ext and vr>1.5: tr.append({"idx":i,"side":"long","entry":last,"tp":last*99,"sl":ext*0.98})
        elif last<ext_s and vr>1.5: tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":ext_s*1.02})
    return tr

def b24h_5m(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(54,d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-24; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.8: continue
        bo=c[i-1]; br=h[i]-l[i]
        if br<=0: continue
        last=c[i]
        if last>rh and last>bo:
            sr=bo+br*0.5; sf=last*(1-0.025)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*99,"sl":min(sr,sf)})
        elif last<rl and last<bo:
            sr=bo-br*0.5; sf=last*(1+0.025)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

def trend_pb_1h(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    e50=pd.Series(c).ewm(span=50,adjust=False).mean().values
    e200=pd.Series(c).ewm(span=200,adjust=False).mean().values
    delta=pd.Series(c).diff(); up=delta.where(delta>0,0).rolling(14).mean()
    dn=(-delta.where(delta<0,0)).rolling(14).mean()
    rsi=(100-100/(1+up/dn)).values
    for i in range(220,d.n):
        if np.isnan(e50[i]) or e50[i]<=0 or np.isnan(e200[i]): continue
        last=c[i]; vr=v[i]/vma[i] if vma[i]>0 else 0; r=rsi[i]; at=atr[i]
        mu=e50[i]>e200[i]*1.001 and last>e200[i]*1.005
        md=e50[i]<e200[i]*0.999 and last<e200[i]*0.995
        pb=abs(last-e50[i])/e50[i]<0.010 and last>=e50[i]*0.995
        ps=abs(last-e50[i])/e50[i]<0.010 and last<=e50[i]*1.005
        bg=last>(h[i]+l[i])/2
        if mu and pb and bg and 40<=r<=65 and vr>=1.2:
            sd=max(0.025*last,2.0*at)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*99,"sl":last-sd})
        elif md and ps and not bg and 35<=r<=60 and vr>=1.2:
            sd=max(0.025*last,2.0*at)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":last+sd})
    return tr

STRATEGIES = {
    "b4h_5m": (b4h_5m, "5m"),
    "b12h_1h": (b12h_1h, "1H"),
    "b24h_5m": (b24h_5m, "5m"),
    "fib_ext_15m": (fib_ext_15m, "15m"),
    "trend_pb_1h": (trend_pb_1h, "1H"),
}

# TRAIL TYPES TO TEST
TRAIL_TESTS = [
    ("no_trail", lambda d,trades: (1.0, 0)),  # never activates
    
    # Fixed % trails
    *[(f"fixed_{p}pct", lambda d,trades, p=p: (p/100, p/100)) for p in [0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]],
    
    # ATR-based trails
    *[(f"atr_x{atr_m}", lambda d,trades, am=atr_m: None) for atr_m in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]],
]

def simulate_one(trade, d, tr_act, tr_dist):
    """Simulate one trade with given trail. Returns (pnl_pct, r_multiple, max_runup, was_trailed)"""
    idx=trade["idx"]; side=trade["side"]; entry=trade["entry"]; tp=trade["tp"]; sl=trade["sl"]
    c=d.c; h=d.h; l=d.l
    active=False; outcome=None; exit_p=None; j=idx+1
    best_price=entry; max_runup=0
    
    while j<min(idx+480,d.n):
        if side=="long":
            if l[j]<=sl: outcome="L"; exit_p=sl; break
            if h[j]>=tp: outcome="W"; exit_p=tp; break
            if h[j]>best_price: best_price=h[j]
            runup=(best_price-entry)/entry
            if runup>max_runup: max_runup=runup
            if tr_act<1.0:  # trail enabled
                if not active and c[j]>=entry*(1+tr_act): active=True
                if active:
                    ns=c[j]*(1-tr_dist)
                    if ns>sl: sl=ns
                    if l[j]<=sl: outcome="W-trail"; exit_p=sl; break
        else:
            if h[j]>=sl: outcome="L"; exit_p=sl; break
            if l[j]<=tp: outcome="W"; exit_p=tp; break
            if l[j]<best_price: best_price=l[j]
            runup=(entry-best_price)/entry
            if runup>max_runup: max_runup=runup
            if tr_act<1.0:
                if not active and c[j]<=entry*(1-tr_act): active=True
                if active:
                    ns=c[j]*(1+tr_dist)
                    if ns<sl: sl=ns
                    if h[j]>=sl: outcome="W-trail"; exit_p=sl; break
        j+=1
    
    if outcome is None: outcome="L-time"; exit_p=c[min(idx+480,d.n-1)]
    pnl=((exit_p-entry)/entry if side=="long" else (entry-exit_p)/entry)-0.0004
    risk=abs(entry-trade["sl"])/entry
    r_mult=pnl/risk if risk>0 else 0
    was_trailed = outcome == "W-trail"
    return pnl, r_mult, max_runup, was_trailed, outcome

# Get coins
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])

results = {}

for sname, (sfunc, stf) in STRATEGIES.items():
    print(f"\n{'='*70}")
    print(f"  {sname} (TF={stf})")
    print(f"{'='*70}")
    
    # Get all trades
    syms = sorted([s for s in coin_tfs if stf in coin_tfs[s]])
    all_trades = []
    for sym in syms:
        df = load(sym, stf)
        if df is None: continue
        d = Data(df)
        trades = sfunc(d)
        all_trades.append((sym, d, trades))
    
    total_trades = sum(len(t[2]) for t in all_trades)
    print(f"  {len(syms)} coins, {total_trades} total trades")
    
    trail_results = []
    
    for tname, tfunc in TRAIL_TESTS:
        if tname.startswith("atr_"):
            # ATR-based: trail distance = ATR * multiplier, activate at 2x ATR
            atr_m = float(tname.split("_x")[1])
            total_n=0; total_w=0; total_pnl=0; total_r=0; total_trailed=0
            for sym, d, trades in all_trades:
                for t in trades:
                    idx=t["idx"]; atr_v=d.atr[idx]
                    if np.isnan(atr_v) or atr_v<=0: continue
                    entry=t["entry"]
                    tr_dist = atr_v * atr_m / entry
                    tr_act = min(tr_dist * 2, 0.20)  # activate at 2x trail distance, cap at 20%
                    pnl, r_m, runup, trailed, outcome = simulate_one(t, d, tr_act, tr_dist)
                    total_n+=1
                    if pnl>0: total_w+=1
                    total_pnl+=pnl*100; total_r+=r_m
                    if trailed: total_trailed+=1
            if total_n:
                trail_results.append((tname, total_n, total_w/total_n*100, total_pnl, total_r, total_r/total_n, total_trailed/total_n*100))
                
        else:
            tr_act, tr_dist = tfunc(None, None)
            total_n=0; total_w=0; total_pnl=0; total_r=0; total_trailed=0
            for sym, d, trades in all_trades:
                for t in trades:
                    pnl, r_m, runup, trailed, outcome = simulate_one(t, d, tr_act, tr_dist)
                    total_n+=1
                    if pnl>0: total_w+=1
                    total_pnl+=pnl*100; total_r+=r_m
                    if trailed: total_trailed+=1
            if total_n:
                trail_results.append((tname, total_n, total_w/total_n*100, total_pnl, total_r, total_r/total_n, total_trailed/total_n*100))
    
    # Sort by total R (best profit)
    trail_results.sort(key=lambda x: x[4], reverse=True)
    
    print(f"{'Trail Type':20s} {'Trades':7s} {'WR':7s} {'Total$':10s} {'TotalR':10s} {'AvgR':8s} {'Trail%':7s}")
    print("-"*70)
    for tname, n, wr, pnl, tr, avg_r, tr_pct in trail_results[:15]:
        print(f"{tname:20s} {n:6d}  {wr:5.1f}% ${pnl:8.2f}  {tr:8.2f}R  {avg_r:+.4f}R  {tr_pct:5.1f}%")
    
    results[sname] = trail_results

# Summary - best trail per strategy
print(f"\n\n{'='*70}")
print(f"  TRAIL MASTER v2 — BEST TRAIL PER STRATEGY")
print(f"{'='*70}")
print(f"{'Strategy':16s} {'Best Trail':20s} {'Total$':10s} {'TotalR':10s} {'AvgR':8s} {'WR':7s}")
print("-"*72)
for sname in STRATEGIES:
    if sname in results and results[sname]:
        best = results[sname][0]
        print(f"{sname:16s} {best[0]:20s} ${best[3]:8.2f}  {best[4]:8.2f}R  {best[5]:+.4f}R  {best[2]:5.1f}%")

# Save
with open(OUT, "w") as f:
    json.dump({"results": results, "top_per_strategy": {s: results[s][0] if s in results and results[s] else None for s in STRATEGIES}}, f, indent=2)
print(f"\nSaved to {OUT}")
