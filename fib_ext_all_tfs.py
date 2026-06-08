#!/usr/bin/env python3
"""FIB_EXT — test on EVERY single timeframe, ALL coins"""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")
OUT = os.path.expanduser("~/multi_agent_bot/FIB_EXT_ALL_TFS.json")

def ema(s, n): return s.ewm(span=n, adjust=False).mean()

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
        dn=(-delta.where(delta<0,0)).rolling(14).mean(); self.rsi=(100-100/(1+up/dn)).values
        self.e50=ema(pd.Series(c),50).values; self.e200=ema(pd.Series(c),200).values

def simulate(trades, d):
    if not trades: return {"n":0,"wins":0,"wr":0,"total_pnl":0,"total_r":0,"avg_r":0,"pf":0,"max_win":0,"max_loss":0}
    c=d.c;h=d.h;l=d.l;win_sum=0.0;loss_sum=0.0
    results=[]
    max_win=0.0; max_loss=0.0
    for t in trades:
        idx=t["idx"];side=t["side"];entry=t["entry"];tp=t["tp"];sl=t["sl"]
        tr_p=0.008;tr_d=0.008;active=False;outcome=None;exit_p=None;j=idx+1
        while j<min(idx+480,d.n):
            if side=="long":
                if l[j]<=sl:outcome="L";exit_p=sl;break
                if h[j]>=tp:outcome="W";exit_p=tp;break
                if not active and c[j]>=entry*(1+tr_p):active=True
                if active:
                    ns=c[j]*(1-tr_d)
                    if ns>sl:sl=ns
                    if l[j]<=sl:outcome="W";exit_p=sl;break
            else:
                if h[j]>=sl:outcome="L";exit_p=sl;break
                if l[j]<=tp:outcome="W";exit_p=tp;break
                if not active and c[j]<=entry*(1-tr_p):active=True
                if active:
                    ns=c[j]*(1+tr_d)
                    if ns<sl:sl=ns
                    if h[j]>=sl:outcome="W";exit_p=sl;break
            j+=1
        if outcome is None:outcome="L";exit_p=c[min(idx+480,d.n-1)]
        pnl=((exit_p-entry)/entry if side=="long" else (entry-exit_p)/entry)-0.0004
        risk=abs(entry-t["sl"])/entry; rr=pnl/risk if risk>0 else 0
        if outcome=="W":win_sum+=abs(rr)
        else:loss_sum+=abs(rr)
        pnl_dollars=pnl*100
        if pnl_dollars>max_win:max_win=pnl_dollars
        if pnl_dollars<max_loss:max_loss=pnl_dollars
        results.append({"pnl":pnl_dollars,"r":rr})
    nn=len(results);w=sum(1 for x in results if x["pnl"]>0)
    pf=win_sum/loss_sum if loss_sum>0 else 99
    total_pnl=sum(x["pnl"] for x in results)
    total_r=sum(x["r"] for x in results)
    return {"n":nn,"wins":w,"wr":round(w/nn*100,1) if nn else 0,
            "total_pnl":round(total_pnl,2),"total_r":round(total_r,2),
            "avg_r":round(total_r/nn,4) if nn else 0,"pf":round(pf,2),
            "max_win":round(max_win,2),"max_loss":round(max_loss,2)}

def fib_ext(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(100,d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=max(0,i-100);sh=np.max(h[lo:i]);sll=np.min(l[lo:i])
        if sh==sll: continue
        df_=sh-sll;ext=sll+1.272*df_;ext_s=sh-1.272*df_
        last=c[i];vr=v[i]/vma[i] if vma[i]>0 else 0
        if last>ext and vr>1.5:
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*1.99,"sl":ext*0.98})
        elif last<ext_s and vr>1.5:
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":ext_s*1.02})
    return tr

# Get all unique timeframes
files = os.listdir(CACHE)
all_tfs = set()
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2:
        tf=parts[1]
        sym=parts[0].replace('_','-')
        all_tfs.add(tf)
        coin_tfs[sym].add(tf)

TFS = sorted(all_tfs)
SYMBOLS = sorted(coin_tfs.keys())

print(f"Testing fib_ext on ALL timeframes: {TFS}")
print(f"Coins: {len(SYMBOLS)}")
print(f"Total combos: {len(SYMBOLS) * len(TFS)}")

result = {"config":{"strategy":"fib_ext","tfs":TFS,"symbols":len(SYMBOLS)},"ranking":[]}

for tf in TFS:
    sym_results = []
    for sym in SYMBOLS:
        if tf not in coin_tfs[sym]: continue
        df = load(sym, tf)
        if df is None: continue
        d = Data(df)
        trades = fib_ext(d)
        st = simulate(trades, d)
        if st["n"] > 0:
            st2 = dict(st)
            st2["symbol"]=sym; st2["tf"]=tf
            sym_results.append(st2)
    
    if not sym_results: continue
    tn=sum(x["n"] for x in sym_results); tw=sum(x["wins"] for x in sym_results)
    tp=sum(x["total_pnl"] for x in sym_results); tr=sum(x["total_r"] for x in sym_results)
    best=max(sym_results, key=lambda x:x["total_r"])
    worst=min(sym_results, key=lambda x:x["total_r"])
    profitable=sum(1 for x in sym_results if x["total_r"]>0)
    
    result["ranking"].append({
        "tf":tf,"total_trades":tn,"wr":round(tw/tn*100,1) if tn else 0,
        "total_pnl":round(tp,2),"total_r":round(tr,2),
        "profitable":profitable,"total_combos":len(sym_results),
        "best_symbol":best["symbol"],"best_pnl":best["total_pnl"],"best_r":best["total_r"],
        "worst_symbol":worst["symbol"],"worst_pnl":worst["total_pnl"],"worst_r":worst["total_r"]
    })

result["ranking"].sort(key=lambda x: x["total_r"], reverse=True)

print(f"\n{'='*90}")
print(f"  FIB_EXT — ALL TIMEFRAMES RANKING")
print(f"{'='*90}")
print(f"{'Rank':5s} {'TF':5s} {'Trades':8s} {'WR':7s} {'Total$':11s} {'TotalR':10s} {'Prof':6s} {'BestSym':10s} {'Best$':9s}")
print("-"*71)
for i, r in enumerate(result["ranking"], 1):
    print(f"{i:4d}. {r['tf']:5s} {r['total_trades']:6d}  {r['wr']:5.1f}% ${r['total_pnl']:8.2f}  {r['total_r']:8.2f}R {r['profitable']:2d}/{r['total_combos']:2d}  {r['best_symbol']:10s} ${r['best_pnl']:6.2f}")

# All profitable combos detail
print(f"\n\n{'='*90}")
print(f"  ALL PROFITABLE COMBOS (sorted by total R)")
print(f"{'='*90}")
all_details = []
for r in result["ranking"]:
    for sym in SYMBOLS:
        if r['tf'] not in coin_tfs[sym]: continue
        df = load(sym, r['tf'])
        if df is None: continue
        d = Data(df)
        trades = fib_ext(d)
        st = simulate(trades, d)
        if st["n"] > 0 and st["total_r"] > 0:
            all_details.append((st["total_r"], st["total_pnl"], st["wr"], st["n"], sym, r["tf"], st["pf"]))

all_details.sort(reverse=True)
print(f"Total profitable combos: {len(all_details)}")
print(f"{'Rank':5s} {'Sym':10s} {'TF':5s} {'Trades':6s} {'WR':6s} {'Total$':8s} {'TotalR':8s} {'PF':5s}")
print("-"*53)
for i, (tr, pnl, wr, n, sym, tf, pf) in enumerate(all_details[:50], 1):
    print(f"{i:4d}. {sym:10s} {tf:5s} {n:5d}  {wr:5.1f}% ${pnl:6.2f}  {tr:6.2f}R {pf:5.2f}")

with open(OUT, "w") as f: json.dump(result, f, indent=2)
print(f"\nSaved to {OUT}")
