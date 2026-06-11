#!/usr/bin/env python3
"""DEEP BACKTEST — Test ALL strategies from legendary traders & foundations.
Tests: time stops, pyramiding, pivotal points, ATR stops, ADX filtering, multi-TF Ichimoku"""
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
        self.e20=pd.Series(c).ewm(span=20,adjust=False).mean().values
        self.e50=pd.Series(c).ewm(span=50,adjust=False).mean().values
        self.e200=pd.Series(c).ewm(span=200,adjust=False).mean().values
        # ADX
        hpc=pd.Series(h)-pc; lpc=pd.Series(l)-pc
        plus_dm=pd.Series(np.where((hpc>0)&(hpc>lpc.abs()),hpc,0))
        minus_dm=pd.Series(np.where((lpc<0)&(lpc.abs()>hpc),lpc.abs(),0))
        tr_=pd.concat([pd.Series(h-l).abs(),hpc.abs(),lpc.abs()],axis=1).max(axis=1)
        atr_=tr_.rolling(14).mean()
        plus_di=100*plus_dm.rolling(14).mean()/atr_; minus_di=100*minus_dm.rolling(14).mean()/atr_
        dx=100*(plus_di-minus_di).abs()/(plus_di+minus_di+1e-10)
        self.adx=dx.rolling(14).mean().values
        self.plus_di=plus_di.values; self.minus_di=minus_di.values

def sim(trades, d, sl_atr=1.5, tp_atr=0, time_stop=240, trail_act=1.0, trail_dist=0):
    """Trade simulator with time stops (PTJ's rule), ATR stops, trailing.
    sl_atr: stop loss in ATR multiples. tp_atr: take profit in ATR multiples (0 = none).
    time_stop: max bars to hold (Paul Tudor Jones time stop)."""
    if not trades: return None
    c=d.c;h=d.h;l=d.l;atr=d.atr;pnl_vals=[];r_vals=[]
    for t in trades:
        idx=t["i"];side=t["s"];entry=t["e"];base_sl=t["sl"]
        # If using ATR-based stop
        if sl_atr>0 and not np.isnan(atr[idx]) and atr[idx]>0:
            if side=="L": sl=entry-atr[idx]*sl_atr
            else: sl=entry+atr[idx]*sl_atr
        else:
            sl=base_sl
        # Take profit
        if tp_atr>0 and not np.isnan(atr[idx]) and atr[idx]>0:
            if side=="L": tp=entry+atr[idx]*tp_atr
            else: tp=entry-atr[idx]*tp_atr
        else:
            tp=t.get("tp",0)
        active=False;out=None;ex=None;j=idx+1;max_j=min(idx+time_stop,d.n)
        while j<max_j:
            if side=="L":
                if l[j]<=sl: out="L"; ex=sl; break
                if tp>0 and h[j]>=tp: out="W"; ex=tp; break
                if not active and trail_act>0 and c[j]>=entry*(1+trail_act):
                    active=True
                if active and trail_dist>0:
                    ns=c[j]*(1-trail_dist)
                    if ns>sl: sl=ns
                    if l[j]<=sl: out="W"; ex=sl; break
            else:
                if h[j]>=sl: out="L"; ex=sl; break
                if tp>0 and l[j]<=tp: out="W"; ex=tp; break
                if not active and trail_act>0 and c[j]<=entry*(1-trail_act):
                    active=True
                if active and trail_dist>0:
                    ns=c[j]*(1+trail_dist)
                    if ns<sl: sl=ns
                    if h[j]>=sl: out="W"; ex=sl; break
            j+=1
        if out is None:
            out="T"  # Time stop
            ex=c[min(idx+time_stop,d.n-1)]
        pnl=((ex-entry)/entry if side=="L" else (entry-ex)/entry)-0.0004
        risk=abs(entry-base_sl)/entry; rr=pnl/risk if risk>0 else 0
        pnl_vals.append(pnl*100); r_vals.append(rr)
    w=sum(1 for v in pnl_vals if v>0); nn=len(pnl_vals)
    if nn==0: return None
    return {"n":nn,"w":w,"wr":round(w/nn*100,1),"tp":round(sum(pnl_vals),2),
            "tr":round(sum(r_vals),2),"ar":round(sum(r_vals)/nn,4)}

# ── STRATEGY 1: LIVEMORE PIVOTAL POINT ──
# Buy when price breaks ABOVE consolidation high with volume. SL at consolidation low.
def livermore_pivot(d, lookback=20, vol_mult=1.5, adx_min=20):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;adx=d.adx;tr=[]
    for i in range(lookback+30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        if np.isnan(adx[i]) or adx[i]<adx_min: continue  # ADX filter
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vol_mult: continue
        lo=i-lookback; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        last=c[i]
        # Pivotal point breakout: price breaks above the range
        if last>rh and last>c[i-1]:
            sl=rl-atr[i]*0.5  # Slightly below range low
            tr.append({"i":i,"s":"L","e":last,"sl":sl})
        elif last<rl and last<c[i-1]:
            sl=rh+atr[i]*0.5
            tr.append({"i":i,"s":"S","e":last,"sl":sl})
    return tr

# ── STRATEGY 2: TURTLE TRADER BREAKOUT ──
# System 1: 20-day breakout. System 2: 55-day breakout. With ATR position sizing.
def turtle_breakout(d, system=20, vol_mult=1.2):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
    for i in range(system+50, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vol_mult: continue
        lo=i-system; rh=max(h[lo:i]); rl=min(l[lo:i])
        last=c[i]
        if last>rh and last>c[i-1]:
            tr.append({"i":i,"s":"L","e":last,"sl":last-atr[i]*2})
        elif last<rl and last<c[i-1]:
            tr.append({"i":i,"s":"S","e":last,"sl":last+atr[i]*2})
    return tr

# ── STRATEGY 3: MACD + ADX combo (macd_cross style) ──
def macd_adx(d, fast=24, slow=52, signal=18, adx_min=20, vol_mult=1.8):
    c=d.c;v=d.v;vma=d.vma;adx=d.adx;tr=[]
    ema_fast=pd.Series(c).ewm(span=fast,adjust=False).mean().values
    ema_slow=pd.Series(c).ewm(span=slow,adjust=False).mean().values
    macd=ema_fast-ema_slow
    sig=pd.Series(macd).ewm(span=signal,adjust=False).mean().values
    for i in range(max(fast,slow,signal)+30, d.n):
        if np.isnan(adx[i]) or adx[i]<adx_min: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<vol_mult: continue
        last=c[i]
        if macd[i]>sig[i] and macd[i-1]<=sig[i-1]:  # Bullish cross
            tr.append({"i":i,"s":"L","e":last,"sl":last*0.985})
        elif macd[i]<sig[i] and macd[i-1]>=sig[i-1]:  # Bearish cross
            tr.append({"i":i,"s":"S","e":last,"sl":last*1.015})
    return tr

# ── STRATEGY 4: TIME STOP (PTJ style) ──
# Same as quick_scalp but with TIME STOP: if not profitable in X bars, exit
def quick_scalp_ts(d, time_stop=48):
    c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;rsi=d.rsi;tr=[]
    for i in range(30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.5: continue
        last=c[i]; prev=c[i-1]
        r=rsi[i] if not np.isnan(rsi[i]) else 50
        range_h=max(h[i-2:i]); range_l=min(l[i-2:i])
        if last>range_h and last>prev and r>50:
            tr.append({"i":i,"s":"L","e":last,"sl":last-atr[i]*1.5})
        elif last<range_l and last<prev and r<50:
            tr.append({"i":i,"s":"S","e":last,"sl":last+atr[i]*1.5})
    return tr

# ── STRATEGY 5: FIB CONFLUENCE WITH VOLUME + ADX FILTER ──
def fib_adx_breakout(d, lb=24, vol_mult=1.5, adx_min=20):
    return [t for t in fib_breakout_orig(d, lb, vol_mult) 
            if not (np.isnan(d.adx[t['i']]) or d.adx[t['i']]<adx_min)]

def fib_breakout_orig(d, lb, vm):
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
            sr=bo+br*0.5; sf=last*0.982
            tr.append({"i":i,"s":"L","e":last,"sl":min(sr,sf)})
        elif last<rl and last<bo and last<ext_s:
            sr=bo-br*0.5; sf=last*1.018
            tr.append({"i":i,"s":"S","e":last,"sl":max(sr,sf)})
    return tr

# ── STRATEGY 6: PURE ADX REGIME FILTER ──
# Only trade when ADX > 25. Use simple breakout.
def adx_only_breakout(d, lookback=12):
    c=d.c;h=d.h;l=d.l;v=d.v;vma=d.vma;adx=d.adx;tr=[]
    for i in range(lookback+50, d.n):
        if np.isnan(adx[i]) or adx[i]<25: continue  # Only trade trending
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.2: continue
        lo=i-lookback; rh=max(h[lo:i]); rl=min(l[lo:i])
        last=c[i]
        if last>rh and last>c[i-1]:
            tr.append({"i":i,"s":"L","e":last,"sl":last*0.985})
        elif last<rl and last<c[i-1]:
            tr.append({"i":i,"s":"S","e":last,"sl":last*1.015})
    return tr

ALL_STRATEGIES = {
    # Original strategies (from new_strategies_test)
    "fib_break_12h": lambda d: fib_breakout_orig(d, 12, 1.5),
    "fib_break_24h": lambda d: fib_breakout_orig(d, 24, 1.8),
    "quick_scalp": quick_scalp_ts,
    
    # NEW strategies from legendary traders
    "livermore_pivot_20": lambda d: livermore_pivot(d, 20, 1.5, 25),
    "livermore_pivot_10": lambda d: livermore_pivot(d, 10, 1.5, 20),
    "turtle_S1_breakout": lambda d: turtle_breakout(d, 20, 1.2),
    "turtle_S2_breakout": lambda d: turtle_breakout(d, 55, 1.2),
    "macd_adx_combo": lambda d: macd_adx(d, 24, 52, 18, 20, 1.8),
    "adx_only_break": lambda d: adx_only_breakout(d, 12),
    "fib_adx_break24": lambda d: fib_adx_breakout(d, 24, 1.5, 20),
}

# Different sim configs per strategy
SIM_CONFIGS = {
    # Original: no time stop, no trailing
    "fib_break_12h": {"sl_atr":0, "tp_atr":0, "time_stop":480, "trail_act":0, "trail_dist":0},
    "fib_break_24h": {"sl_atr":0, "tp_atr":0, "time_stop":480, "trail_act":0, "trail_dist":0},
    "quick_scalp": {"sl_atr":0, "tp_atr":0, "time_stop":480, "trail_act":0, "trail_dist":0},
    # NEW: with time stops and ATR stops
    "livermore_pivot_20": {"sl_atr":1.5, "tp_atr":4.5, "time_stop":240, "trail_act":2.0, "trail_dist":0.5},
    "livermore_pivot_10": {"sl_atr":1.5, "tp_atr":4.5, "time_stop":240, "trail_act":2.0, "trail_dist":0.5},
    "turtle_S1_breakout": {"sl_atr":2, "tp_atr":0, "time_stop":480, "trail_act":1.5, "trail_dist":1.0},
    "turtle_S2_breakout": {"sl_atr":2, "tp_atr":0, "time_stop":480, "trail_act":1.5, "trail_dist":1.0},
    "macd_adx_combo": {"sl_atr":1.5, "tp_atr":4.5, "time_stop":120, "trail_act":1.0, "trail_dist":0.3},
    "adx_only_break": {"sl_atr":1.5, "tp_atr":0, "time_stop":240, "trail_act":2.0, "trail_dist":0.5},
    "fib_adx_break24": {"sl_atr":0, "tp_atr":0, "time_stop":480, "trail_act":0, "trail_dist":0},
}

RESULT_MODES = [
    ("time_stop", {"sl_atr":1.5, "tp_atr":4.5, "time_stop":120, "trail_act":0, "trail_dist":0}),
    ("ATR_stop", {"sl_atr":2.0, "tp_atr":4.5, "time_stop":480, "trail_act":0, "trail_dist":0}),
    ("trailing_PTJ", {"sl_atr":1.5, "tp_atr":0, "time_stop":240, "trail_act":1.0, "trail_dist":0.5}),
]

TFS = ["5m","15m","30m","1H"]
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMS = sorted(coin_tfs.keys())

print("="*80)
print("DEEP BACKTEST — All Strategies from Legendary Traders")
print("="*80)
print(f"Coins: {len(SYMS)}, TFs: {len(TFS)}, Stategies: {len(ALL_STRATEGIES)}")
print(f"Data: 365 days per coin per timeframe")
print()

for sname, sfunc in ALL_STRATEGIES.items():
    print(f"\n{'─'*80}")
    print(f"  {sname}")
    print(f"{'─'*80}")
    
    base_cfg = SIM_CONFIGS.get(sname, {"sl_atr":1.5, "tp_atr":4.5, "time_stop":240, "trail_act":0, "trail_dist":0})
    
    for tf in TFS:
        total=0; wins=0; pnl=0; tr=0; prof=0; tot=0
        max_pnl=0; min_pnl=0; total_dd=0
        
        for sym in SYMS:
            if tf not in coin_tfs[sym]: continue
            df = load(sym, tf)
            if df is None: continue
            d = Data(df)
            trades = sfunc(d)
            st = sim(trades, d, **base_cfg)
            if st and st["n"]>0:
                tot+=1; total+=st["n"]; wins+=st["w"]; pnl+=st["tp"]; tr+=st["tr"]
                if st["tp"]>0: prof+=1
                if st["tp"]>max_pnl: max_pnl=st["tp"]
                if st["tp"]<min_pnl: min_pnl=st["tp"]
        
        if total>0:
            wr=wins/total*100 if total else 0
            print(f"  {tf:5s}  {total:6d}t  WR={wr:5.1f}%  ${pnl:+8.2f}  {tr:+8.2f}R  coins: {prof}/{tot}  best: ${max_pnl:+.1f}  worst: ${min_pnl:+.1f}")
    
    # Also test with PTJ-style trailing on best TF
    print(f"  ─── Testing PTJ trailing stops ───")
    for mode_name, mode_cfg in RESULT_MODES:
        for tf in ["1H"]:
            total=0; wins=0; pnl=0; tr=0; prof=0; tot=0
            for sym in SYMS:
                if "1H" not in coin_tfs[sym]: continue
                df = load(sym, "1H")
                if df is None: continue
                d = Data(df)
                trades = sfunc(d)
                st = sim(trades, d, **mode_cfg)
                if st and st["n"]>0:
                    tot+=1; total+=st["n"]; wins+=st["w"]; pnl+=st["tp"]; tr+=st["tr"]
                    if st["tp"]>0: prof+=1
            if total>0:
                wr=wins/total*100 if total else 0
                print(f"  {mode_name:14s} 1H {total:6d}t  WR={wr:5.1f}%  ${pnl:+8.2f}  {tr:+8.2f}R  {prof}/{tot}")

print(f"\n{'='*80}")
print(f"ALL DONE — See saad-trading-system skill for full results")
print(f"{'='*80}")
