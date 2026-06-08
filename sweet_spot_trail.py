#!/usr/bin/env python3
"""Find optimal trail — lock profit without killing winners."""
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

def run_backtest(d, trades, trail_pct=0):
    """Simple backtest with configurable trail %"""
    c=d.c;h=d.h;l=d.l
    total_n=0; total_w=0; total_pnl=0
    max_runup_vals=[]; final_pnl_vals=[]
    for t in trades:
        idx=t["idx"];side=t["side"];entry=t["entry"];tp=t["tp"];sl=t["sl"]
        trail_active=False; outcome=None; exit_p=None
        best_price=entry; j=idx+1
        max_profit=0
        while j<min(idx+480,d.n):
            if side=="long":
                if l[j]<=sl: outcome="L"; exit_p=sl; break
                if h[j]>=tp: outcome="W"; exit_p=tp; break
                if h[j] > best_price: best_price = h[j]
                runup = (best_price-entry)/entry*100
                if runup > max_profit: max_profit = runup
                if trail_pct > 0:
                    if not trail_active and c[j] >= entry*(1+trail_pct/100):
                        trail_active = True
                    if trail_active:
                        ns = c[j]*(1-trail_pct/100)
                        if ns > sl: sl = ns
                        if l[j] <= sl: outcome="W-trail"; exit_p=sl; break
            else:
                if h[j]>=sl: outcome="L"; exit_p=sl; break
                if l[j]<=tp: outcome="W"; exit_p=tp; break
                if l[j] < best_price: best_price = l[j]
                runup = (entry-best_price)/entry*100
                if runup > max_profit: max_profit = runup
                if trail_pct > 0:
                    if not trail_active and c[j] <= entry*(1-trail_pct/100):
                        trail_active = True
                    if trail_active:
                        ns = c[j]*(1+trail_pct/100)
                        if ns < sl: sl = ns
                        if h[j]>=sl: outcome="W-trail"; exit_p=sl; break
            j+=1
        if outcome is None: outcome="L-time"; exit_p=c[min(idx+480,d.n-1)]
        pnl=((exit_p-entry)/entry if side=="long" else (entry-exit_p)/entry)-0.0004
        total_n+=1
        if pnl>0: total_w+=1
        total_pnl+=pnl*100
        max_runup_vals.append(max_profit)
        final_pnl_vals.append(pnl*100)
    
    avg_max_runup = sum(max_runup_vals)/len(max_runup_vals) if max_runup_vals else 0
    wr = total_w/total_n*100 if total_n else 0
    return {"n":total_n,"wins":total_w,"wr":round(wr,1),"total_pnl":round(total_pnl,2),
            "avg_max_runup":round(avg_max_runup,2)}

def get_trades(strategy_name, d):
    """Generate trades for different strategies"""
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    if strategy_name == "b4h_5m":
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
    elif strategy_name == "fib_ext_15m":
        for i in range(100,d.n):
            if np.isnan(atr[i]) or atr[i]<=0: continue
            lo=max(0,i-100);sh=np.max(h[lo:i]);sll=np.min(l[lo:i])
            if sh==sll: continue
            df_=sh-sll;ext=sll+1.272*df_;ext_s=sh-1.272*df_
            last=c[i];vr=v[i]/vma[i] if vma[i]>0 else 0
            if last>ext and vr>1.5: tr.append({"idx":i,"side":"long","entry":last,"tp":last*99,"sl":ext*0.98})
            elif last<ext_s and vr>1.5: tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":ext_s*1.02})
    elif strategy_name == "b12h_1h":
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

# Get coins
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])

# Test B4h 5m with different trail %
print("B4h 5m — FINDING THE SWEET SPOT")
print(f"{'Trail%':8s} {'Trades':7s} {'WR':6s} {'Total$':9s} {'AvgRunup':9s}")
print("-"*45)

SYMS = sorted([s for s in coin_tfs if "5m" in coin_tfs[s]])
for tr in [0, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]:
    tn=0; tw=0; tp=0; ar=0
    for sym in SYMS:
        df=load(sym,"5m"); 
        if df is None: continue
        d=Data(df); trades=get_trades("b4h_5m",d); st=run_backtest(d,trades,tr)
        tn+=st["n"]; tw+=st["wins"]; tp+=st["total_pnl"]; ar+=st["avg_max_runup"]
    if tn:
        print(f"{tr:5.1f}%: {tn:6d}  {tw/tn*100:5.1f}% ${tp:7.2f} ${ar/len(SYMS):.1f}")

print(f"\n\nB12h 1H — FINDING THE SWEET SPOT")
SYMS_1H = sorted([s for s in coin_tfs if "1H" in coin_tfs[s] or "1h" in coin_tfs[s]])
for tr in [0, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0]:
    tn=0; tw=0; tp=0; ar=0
    for sym in SYMS_1H:
        df=load(sym,"1H"); 
        if df is None: continue
        d=Data(df); trades=get_trades("b12h_1h",d); st=run_backtest(d,trades,tr)
        tn+=st["n"]; tw+=st["wins"]; tp+=st["total_pnl"]; ar+=st["avg_max_runup"]
    if tn:
        print(f"{tr:5.1f}%: {tn:6d}  {tw/tn*100:5.1f}% ${tp:7.2f} ${ar/len(SYMS_1H):.2f}")

print(f"\n\nFib_ext 15m — FINDING THE SWEET SPOT")
SYMS_15 = sorted([s for s in coin_tfs if "15m" in coin_tfs[s]])
for tr in [0, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0]:
    tn=0; tw=0; tp=0; ar=0
    for sym in SYMS_15:
        df=load(sym,"15m"); 
        if df is None: continue
        d=Data(df); trades=get_trades("fib_ext_15m",d); st=run_backtest(d,trades,tr)
        tn+=st["n"]; tw+=st["wins"]; tp+=st["total_pnl"]; ar+=st["avg_max_runup"]
    if tn:
        print(f"{tr:5.1f}%: {tn:6d}  {tw/tn*100:5.1f}% ${tp:7.2f} ${ar/len(SYMS_15):.2f}")
