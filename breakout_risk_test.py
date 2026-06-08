#!/usr/bin/env python3
"""Test breakout_12h 1H with different trail settings (from bot's proven strategy)."""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")

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
    return {"n":nn,"wins":w,"wr":round(w/nn*100,1) if nn else 0,
            "total_pnl":round(sum(pnl_vals),2),"total_r":round(sum(r_vals),2),
            "avg_r":round(sum(r_vals)/nn,4) if nn else 0,"pf":round(pf,2)}

def breakout_12h(d):
    """Exact bot's logic: 12h lookback, 1.8% SL, 1.5x volume"""
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;lb=12
    tr=[]
    for i in range(lb+30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-lb; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.5: continue
        bar_o=c[i-1]; bar_r=h[i]-l[i]
        if bar_r<=0: continue
        last=c[i]
        if last>rh and last>bar_o:
            sr=bar_o+bar_r*0.5; sf=last*(1-0.018)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*1.99,"sl":min(sr,sf)})
        elif last<rl and last<bar_o:
            sr=bar_o-bar_r*0.5; sf=last*(1+0.018)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

# Get coins with 1H data
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMS = sorted([s for s in coin_tfs if "1H" in coin_tfs[s] or "1h" in coin_tfs[s]])

print(f"BREAKOUT_12h 1H — Testing on {len(SYMS)} coins")
print(f"{'Trail':15s} {'Trades':7s} {'WR':7s} {'Total$':10s} {'TotalR':10s} {'AvgR':8s} {'PF':6s} {'Prof':5s}")
print("-"*65)

for tr_pct in [0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0]:
    tval = tr_pct / 100.0
    total_n=0; total_w=0; total_pnl=0; total_r=0; prof_c=0; tot_c=0
    for sym in SYMS:
        df = load(sym, "1H")
        if df is None: continue
        d = Data(df)
        trades = breakout_12h(d)
        st = simulate(trades, d, tr_act=tval, tr_dist=tval)
        if st["n"] > 0:
            tot_c+=1; total_n+=st["n"]; total_w+=st["wins"]
            total_pnl+=st["total_pnl"]; total_r+=st["total_r"]
            if st["total_r"]>0: prof_c+=1
    if total_n:
        print(f"  {tr_pct:.1f}% trail: {total_n:6d}  {total_w/total_n*100:5.1f}%  ${total_pnl:8.2f}  {total_r:8.2f}R  {total_r/total_n:+.4f}R  {total_r/total_n:6.2f}  {prof_c}/{tot_c}")

# Also test no trail with fixed TP
print(f"\n{'No trail (fixed TP)':15s}")
for sl_m in [0.5, 1.0, 1.5, 2.0]:
    total_n=0; total_w=0; total_pnl=0; total_r=0; prof_c=0; tot_c=0
    for sym in SYMS:
        df = load(sym, "1H")
        if df is None: continue
        d = Data(df)
        trades = breakout_12h(d)
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
        print(f"  No trail SLx{sl_m:.1f}: {total_n:6d}  {total_w/total_n*100:5.1f}%  ${total_pnl:8.2f}  {total_r:8.2f}R  {total_r/total_n:+.4f}R  {total_r/total_n:6.2f}  {prof_c}/{tot_c}")
