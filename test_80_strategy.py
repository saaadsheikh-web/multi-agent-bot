#!/usr/bin/env python3
"""TEST THE 80% WR STRATEGY WITH MARKET ORDERS (simulating real execution)"""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")
OUT = os.path.expanduser("~/multi_agent_bot/STRATEGY_80_FINAL.json")

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
        self.n = len(c)
        # ADX
        plus_dm=np.zeros(self.n); minus_dm=np.zeros(self.n); tr2=np.zeros(self.n)
        for i in range(1,self.n):
            hi_m=h[i]-h[i-1]; lo_m=l[i-1]-l[i]
            tr2[i]=max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1]))
            plus_dm[i]=hi_m if hi_m>lo_m and hi_m>0 else 0
            minus_dm[i]=lo_m if lo_m>hi_m and lo_m>0 else 0
        atr2=pd.Series(tr2).rolling(14).mean().values
        pdi=100*pd.Series(plus_dm).rolling(14).mean().values/atr2
        mdi=100*pd.Series(minus_dm).rolling(14).mean().values/atr2
        dx=100*np.abs(pdi-mdi)/(pdi+mdi+1e-10)
        self.adx=pd.Series(dx).rolling(14).mean().values
        self.pdi=pdi; self.mdi=mdi

def sim_market(trades, d, sl_pct, use_market=True):
    """Simulate with MARKET orders (pay spread)"""
    if not trades: return None
    c=d.c;h=d.h;l=d.h;pnl_vals=[];r_vals=[]
    for t in trades:
        idx=t["i"]; side=t["s"]; entry=t["e"]
        tp=entry*99 if side=="L" else entry*0.01
        sl=entry*(1-sl_pct/100) if side=="L" else entry*(1+sl_pct/100)
        
        # Market order: pay 0.06% spread on entry + 0.06% on exit
        entry_cost = 0.0006
        out=None; ex=None; j=idx+1
        
        while j<min(idx+480,d.n):
            if side=="L":
                if l[j]<=sl: out="L"; ex=sl; break
                if h[j]>=tp: out="W"; ex=tp; break
            else:
                if h[j]>=sl: out="L"; ex=sl; break
                if l[j]<=tp: out="W"; ex=tp; break
            j+=1
        if out is None: out="L"; ex=c[min(idx+480,d.n-1)]
        
        pnl=((ex-entry)/entry if side=="L" else (entry-ex)/entry) - entry_cost*2
        pnl_vals.append(pnl*100)
    w=sum(1 for v in pnl_vals if v>0); nn=len(pnl_vals)
    return {"n":nn,"w":w,"wr":round(w/nn*100,1),"tp":round(sum(pnl_vals),2)}

# THE 80% STRATEGY: LB=2h, VM=2.0x, SL=5%
def strat_80(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;lb=2;tr=[]
    for i in range(lb+30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-lb; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<2.0: continue
        bo=c[i-1]; br=h[i]-l[i]; last=c[i]
        if br<=0: continue
        if last>rh and last>bo:
            sr=bo+br*0.5; sf=last*0.95
            tr.append({"i":i,"s":"L","e":last,"sl":min(sr,sf)})
        elif last<rl and last<bo:
            sr=bo-br*0.5; sf=last*1.05
            tr.append({"i":i,"s":"S","e":last,"sl":max(sr,sf)})
    return tr

# TEST WITH MARKET ORDERS
TFS = ["5m","15m","30m","1H"]
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMS = sorted(coin_tfs.keys())

print(f"TESTING 80% STRATEGY WITH MARKET ORDERS")
print(f"{'Symbol':12s} {'TF':5s} {'Trades':7s} {'WR':7s} {'PnL':10s}")
print("-"*42)

results = []
for tf in TFS:
    for sym in SYMS:
        if tf not in coin_tfs[sym]: continue
        df = load(sym, tf)
        if df is None: continue
        d = Data(df)
        trades = strat_80(d)
        if not trades: continue
        st = sim_market(trades, d, 5.0, use_market=True)
        if st and st["n"]>5:
            results.append({"sym":sym,"tf":tf,"n":st["n"],"wr":st["wr"],"pnl":st["tp"]})
            print(f"{sym:12s} {tf:5s} {st['n']:6d}  {st['wr']:5.1f}%  ${st['tp']:8.2f}")

total_n=sum(r["n"] for r in results); total_w=sum(int(r["n"]*r["wr"]/100) for r in results)
total_pnl=sum(r["pnl"] for r in results); prof=sum(1 for r in results if r["pnl"]>0)
print("-"*42)
print(f"{'TOTAL':12s} {'':5s} {total_n:6d}  {total_w/total_n*100:5.1f}%  ${total_pnl:8.2f}")
print(f"Profitable coins: {prof}/{len(results)}")

# Best TF
for tf in TFS:
    tf_r=[r for r in results if r["tf"]==tf]
    if tf_r:
        tn=sum(r["n"] for r in tf_r); tp=sum(r["pnl"] for r in tf_r); pr=sum(1 for r in tf_r if r["pnl"]>0)
        tw=sum(int(r["n"]*r["wr"]/100) for r in tf_r)
        print(f"\n{tf}: {tn}t, {tw/tn*100:.1f}%WR, ${tp:.2f}, {pr}/{len(tf_r)} profitable")

with open(OUT,"w") as f: json.dump(results,f,indent=2)
print(f"\nSaved to {OUT}")
