#!/usr/bin/env python3
"""Fib_ext 15m — no trail, different stops. Find optimal setup."""
import os, pandas as pd
import numpy as np
from collections import defaultdict

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")

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

def simulate(trades, d, tr_act=0.008, tr_dist=0.008):
    if not trades: return {"n":0,"wins":0,"wr":0,"total_pnl":0,"total_r":0,"avg_r":0,"pf":0}
    c=d.c;h=d.h;l=d.l;win_sum=0.0;loss_sum=0.0;pnl_vals=[];r_vals=[]
    for t in trades:
        idx=t["idx"];side=t["side"];entry=t["entry"];tp=t["tp"];sl=t["sl"]
        active=False;outcome=None;exit_p=None;j=idx+1
        while j<min(idx+480,d.n):
            if side=="long":
                if l[j]<=sl:outcome="L";exit_p=sl;break
                if h[j]>=tp:outcome="W";exit_p=tp;break
                if not active and c[j]>=entry*(1+tr_act):active=True
                if active:
                    ns=c[j]*(1-tr_dist)
                    if ns>sl:sl=ns
                    if l[j]<=sl:outcome="W";exit_p=sl;break
            else:
                if h[j]>=sl:outcome="L";exit_p=sl;break
                if l[j]<=tp:outcome="W";exit_p=tp;break
                if not active and c[j]<=entry*(1-tr_act):active=True
                if active:
                    ns=c[j]*(1+tr_dist)
                    if ns<sl:sl=ns
                    if h[j]>=sl:outcome="W";exit_p=sl;break
            j+=1
        if outcome is None:outcome="L";exit_p=c[min(idx+480,d.n-1)]
        pnl=((exit_p-entry)/entry if side=="long" else (entry-exit_p)/entry)-0.0004
        risk=abs(entry-t["sl"])/entry; rr=pnl/risk if risk>0 else 0
        if outcome=="W":win_sum+=abs(rr)
        else:loss_sum+=abs(rr)
        pnl_vals.append(pnl*100); r_vals.append(rr)
    nn=len(pnl_vals); w=sum(1 for v in pnl_vals if v>0)
    pf=win_sum/loss_sum if loss_sum>0 else 99
    total_pnl=sum(pnl_vals); total_r=sum(r_vals)
    return {"n":nn,"wins":w,"wr":round(w/nn*100,1) if nn else 0,
            "total_pnl":round(total_pnl,2),"total_r":round(total_r,2),
            "avg_r":round(total_r/nn,4) if nn else 0,"pf":round(pf,2)}

def fib_ext(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(100,d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=max(0,i-100);sh=np.max(h[lo:i]);sll=np.min(l[lo:i])
        if sh==sll: continue
        df_=sh-sll;ext=sll+1.272*df_;ext_s=sh-1.272*df_
        last=c[i];vr=v[i]/vma[i] if vma[i]>0 else 0
        if last>ext and vr>1.5: tr.append({"idx":i,"side":"long","entry":last,"tp":last*1.99,"sl":ext*0.98})
        elif last<ext_s and vr>1.5: tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":ext_s*1.02})
    return tr

files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMS = sorted([s for s in coin_tfs if "15m" in coin_tfs[s]])

print("FIB_EXT 15m — NO TRAIL, DIFFERENT STOP WIDTHS")
print(f"{'SL mult':10s} {'Trades':7s} {'WR':7s} {'Total$':10s} {'TotalR':10s} {'AvgR':8s} {'PF':6s} {'Prof':5s}")
print("-"*63)

for sl_m in [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
    total_n=0; total_w=0; total_pnl=0; total_r=0; prof_c=0; tot_c=0
    for sym in SYMS:
        df = load(sym, "15m")
        if df is None: continue
        d = Data(df)
        trades = fib_ext(d)
        for t in trades:
            entry = t["entry"]; orig_sl = t["sl"]
            if t["side"] == "long": t["sl"] = entry - abs(entry - orig_sl) * sl_m
            else: t["sl"] = entry + abs(entry - orig_sl) * sl_m
        st = simulate(trades, d, tr_act=1.0, tr_dist=0)
        if st["n"] > 0:
            tot_c+=1; total_n+=st["n"]; total_w+=st["wins"]
            total_pnl+=st["total_pnl"]; total_r+=st["total_r"]
            if st["total_r"]>0: prof_c+=1
    if total_n:
        wr=total_w/total_n*100
        print(f"SL x{sl_m:.1f} ({sl_m*2:.1f}%): {total_n:6d}  {wr:5.1f}%  ${total_pnl:8.2f}  {total_r:8.2f}R  {total_r/total_n:+.4f}R  {total_r/total_n:6.2f}  {prof_c}/{tot_c}")
