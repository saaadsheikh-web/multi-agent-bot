#!/usr/bin/env python3
"""Test new combined strategies — FIB + BREAKOUT, RSI EXTREME, VOLCAP + BREAKOUT"""
import os, json, pandas as pd
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
        delta=pd.Series(c).diff(); up=delta.where(delta>0,0).rolling(14).mean()
        dn=(-delta.where(delta<0,0)).rolling(14).mean()
        self.rsi=(100-100/(1+up/dn)).values
        self.e50=pd.Series(c).ewm(span=50,adjust=False).mean().values
        self.e200=pd.Series(c).ewm(span=200,adjust=False).mean().values

def sim(trades, d, tr_act=1.0, tr_dist=0):
    if not trades: return None
    c=d.c;h=d.h;l=d.l;pnl_vals=[];r_vals=[]
    for t in trades:
        idx=t["i"];side=t["s"];entry=t["e"];tp=t["tp"];sl=t["sl"]
        active=False;out=None;ex=None;j=idx+1
        while j<min(idx+480,d.n):
            if side=="L":
                if l[j]<=sl: out="L"; ex=sl; break
                if h[j]>=tp: out="W"; ex=tp; break
                if not active and c[j]>=entry*(1+tr_act): active=True
                if active:
                    ns=c[j]*(1-tr_dist)
                    if ns>sl: sl=ns
                    if l[j]<=sl: out="W"; ex=sl; break
            else:
                if h[j]>=sl: out="L"; ex=sl; break
                if l[j]<=tp: out="W"; ex=tp; break
                if not active and c[j]<=entry*(1-tr_act): active=True
                if active:
                    ns=c[j]*(1+tr_dist)
                    if ns<sl: sl=ns
                    if h[j]>=sl: out="W"; ex=sl; break
            j+=1
        if out is None: out="L"; ex=c[min(idx+480,d.n-1)]
        pnl=((ex-entry)/entry if side=="L" else (entry-ex)/entry)-0.0004
        risk=abs(entry-t["sl"])/entry; rr=pnl/risk if risk>0 else 0
        pnl_vals.append(pnl*100); r_vals.append(rr)
    w=sum(1 for v in pnl_vals if v>0); nn=len(pnl_vals)
    return {"n":nn,"w":w,"wr":round(w/nn*100,1),"tp":round(sum(pnl_vals),2),"tr":round(sum(r_vals),2),"ar":round(sum(r_vals)/nn,4)if nn else 0}

# STRATEGY 1: FIB EXTENSION + BREAKOUT = double confirmation
def fib_breakout(d, lb, vm, sl):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(max(lb,100)+30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-lb; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vm: continue
        bo=c[i-1]; br=h[i]-l[i]
        if br<=0: continue
        last=c[i]
        fib_lo=max(0,i-100); sh=np.max(h[fib_lo:i]); sll=np.min(l[fib_lo:i])
        if sh==sll: continue
        df_=sh-sll; ext=sll+1.272*df_; ext_s=sh-1.272*df_
        if last>rh and last>bo and last>ext:
            sr=bo+br*0.5; sf=last*(1-sl/100)
            tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":min(sr,sf)})
        elif last<rl and last<bo and last<ext_s:
            sr=bo-br*0.5; sf=last*(1+sl/100)
            tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

# STRATEGY 2: RSI <15 or >85 with trend filter + volume
def rsi_extreme(d):
    c=d.c;v=d.v;n=d.n;vma=d.vma;rsi=d.rsi;e50=d.e50;e200=d.e200;tr=[]
    for i in range(100, n):
        vr=v[i]/vma[i] if vma[i]>0 else 0
        r=rsi[i] if not np.isnan(rsi[i]) else 50
        last=c[i]
        up=last>e50[i]>e200[i]; dn=last<e50[i]<e200[i]
        if r<15 and vr>1.5 and up:
            tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":last*0.985})
        elif r>85 and vr>1.5 and dn:
            tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":last*1.015})
    return tr

# STRATEGY 3: Volume capitulation + breakout confirmation
def volcap_breakout(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;rsi=d.rsi;tr=[]
    for i in range(100, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        last=c[i]; prev=c[i-1]; pct=(last-prev)/prev*100
        r=rsi[i] if not np.isnan(rsi[i]) else 50
        if abs(pct)>2 and vr>3:
            if pct<-2 and r<30:
                lo=i-24; rh=max(h[lo:i])
                if last>rh: tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":last-atr[i]*2})
            elif pct>2 and r>70:
                lo=i-24; rl=min(l[lo:i])
                if last<rl: tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":last+atr[i]*2})
    return tr

# STRATEGY 4: Quick scalp - 2 bar breakout + RSI + volume
def quick_scalp(d):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;rsi=d.rsi;tr=[]
    for i in range(30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.5: continue
        last=c[i]; prev=c[i-1]
        r=rsi[i] if not np.isnan(rsi[i]) else 50
        range_h=max(h[i-2:i]); range_l=min(l[i-2:i])
        if last>range_h and last>prev and r>50:
            tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":last-atr[i]*1.5})
        elif last<range_l and last<prev and r<50:
            tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":last+atr[i]*1.5})
    return tr

STRATEGIES = {
    "fib_break_12h": lambda d: fib_breakout(d, 12, 1.5, 1.8),
    "fib_break_24h": lambda d: fib_breakout(d, 24, 1.8, 2.5),
    "rsi_extreme": rsi_extreme,
    "volcap_break": volcap_breakout,
    "quick_scalp": quick_scalp,
}

TFS = ["5m","15m","30m","1H"]
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMS = sorted(coin_tfs.keys())

print("TESTING NEW COMBINED STRATEGIES")
print(f"Coins: {len(SYMS)}, TFs: {len(TFS)}, Strats: {len(STRATEGIES)}")

for sname, sfunc in STRATEGIES.items():
    for tf in TFS:
        total=0; wins=0; pnl=0; tr=0; prof=0; tot=0
        for sym in SYMS:
            if tf not in coin_tfs[sym]: continue
            df = load(sym, tf)
            if df is None: continue
            d = Data(df)
            trades = sfunc(d)
            st = sim(trades, d, 1.0, 0)
            if st and st["n"]>0:
                tot+=1; total+=st["n"]; wins+=st["w"]; pnl+=st["tp"]; tr+=st["tr"]
                if st["tr"]>0: prof+=1
        if total>0:
            wr=wins/total*100 if total else 0
            print(f"  {sname:20s} {tf:5s} {total:6d}t  {wr:5.1f}%  ${pnl:8.2f}  {tr:8.2f}R  {prof}/{tot}")

print(f"\nALL DONE")
