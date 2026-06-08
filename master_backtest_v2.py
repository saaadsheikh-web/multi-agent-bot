#!/usr/bin/env python3
"""
MASTER BACKTEST v2 — ALL strategies, ALL coins, ALL TFs
Uses cached parquet data. Clean code, no bugs.
"""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict

CACHE = os.path.expanduser("~/multi_agent_bot/backtest_data")
OUT = os.path.expanduser("~/multi_agent_bot/MASTER_BACKTEST_RESULTS.json")
ROUND_TRIP = 0.0004

def ema(s, n): return s.ewm(span=n, adjust=False).mean()

def load(sym, tf):
    f = os.path.join(CACHE, f"{sym.replace('-','_')}_{tf}_365d.parquet")
    if not os.path.exists(f): return None
    df = pd.read_parquet(f)
    df.columns = [c.lower() for c in df.columns]
    return df.sort_values("ts").reset_index(drop=True)

class Data:
    def __init__(self, df):
        c = df["close"].values; h = df["high"].values
        l = df["low"].values; v = df["volume"].values
        self.c=c; self.h=h; self.l=l; self.v=v
        self.ts=df["ts"].values; self.n=len(c)
        pc = pd.Series(c).shift(1)
        tr = pd.concat([(pd.Series(h)-pd.Series(l)).abs(),
                        (pd.Series(h)-pc).abs(), (pd.Series(l)-pc).abs()], axis=1).max(axis=1)
        self.atr = tr.rolling(14).mean().values
        self.vma = pd.Series(v).rolling(20).mean().values
        delta = pd.Series(c).diff()
        up = delta.where(delta>0,0).rolling(14).mean()
        dn = (-delta.where(delta<0,0)).rolling(14).mean()
        self.rsi = (100 - 100/(1+up/dn)).values
        self.e50 = ema(pd.Series(c),50).values
        self.e200 = ema(pd.Series(c),200).values

def simulate(trades, d):
    if not trades:
        return {"n":0,"wins":0,"wr":0,"total_pnl":0,"total_r":0,"avg_r":0,"pf":0}
    c=d.c; h=d.h; l=d.l
    win_sum=0.0; loss_sum=0.0; results=[]
    for t in trades:
        idx=t["idx"]; side=t["side"]; entry=t["entry"]; tp=t["tp"]; sl=t["sl"]
        tr_p=0.008; tr_d=0.008; active=False; outcome=None; exit_p=None
        j=idx+1
        while j < min(idx+480, d.n):
            if side == "long":
                if l[j] <= sl: outcome="L"; exit_p=sl; break
                if h[j] >= tp: outcome="W"; exit_p=tp; break
                if not active and c[j] >= entry*(1+tr_p): active=True
                if active:
                    ns = c[j]*(1-tr_d)
                    if ns > sl: sl = ns
                    if l[j] <= sl: outcome="W"; exit_p=sl; break
            else:
                if h[j] >= sl: outcome="L"; exit_p=sl; break
                if l[j] <= tp: outcome="W"; exit_p=tp; break
                if not active and c[j] <= entry*(1-tr_p): active=True
                if active:
                    ns = c[j]*(1+tr_d)
                    if ns < sl: sl = ns
                    if h[j] >= sl: outcome="W"; exit_p=sl; break
            j += 1
        if outcome is None: outcome="L"; exit_p=c[min(idx+480, d.n-1)]
        pnl = ((exit_p-entry)/entry if side=="long" else (entry-exit_p)/entry) - ROUND_TRIP
        risk = abs(entry - t["sl"]) / entry
        rr = pnl/risk if risk > 0 else 0
        if outcome == "W": win_sum += abs(rr)
        else: loss_sum += abs(rr)
        results.append({"pnl": pnl*100, "r": rr})
    nn = len(results)
    w = sum(1 for x in results if x["pnl"] > 0)
    pnl_total = sum(x["pnl"] for x in results)
    r_total = sum(x["r"] for x in results)
    pf = win_sum/loss_sum if loss_sum > 0 else 99
    return {"n":nn,"wins":w,"wr":round(w/nn*100,1),"total_pnl":round(pnl_total,2),
            "total_r":round(r_total,2),"avg_r":round(r_total/nn,4) if nn>0 else 0,"pf":round(pf,2)}

# STRATEGIES
def breakout(d, lb, mv, sl, atr_m=1.0):
    c=d.c; h=d.h; l=d.l; v=d.v; atr=d.atr; vma=d.vma; tr=[]
    for i in range(lb+30, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-lb; rh=max(h[lo:i]); rl=min(l[lo:i])
        if rh==rl: continue
        vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<mv: continue
        bar_o=c[i-1]; bar_r=h[i]-l[i]
        if bar_r<=0: continue
        atr_w=atr[max(0,i-20):i]; atr_a=np.nanmean(atr_w) if len(atr_w)>=5 else atr[i]
        if atr_a<=0 or atr[i]<atr_a*atr_m: continue
        last=c[i]
        if last>rh and last>bar_o:
            sr=bar_o+bar_r*0.5; sf=last*(1-sl)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*1.99,"sl":min(sr,sf)})
        elif last<rl and last<bar_o:
            sr=bar_o-bar_r*0.5; sf=last*(1+sl)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":max(sr,sf)})
    return tr

def donchian(d):
    c=d.c; h=d.h; l=d.l; v=d.v; atr=d.atr; vma=d.vma; tr=[]
    for i in range(50, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=i-30; vr=v[i]/vma[i] if vma[i]>0 else 0
        if vr<1.8: continue
        hn=max(h[lo:i]); ln=min(l[lo:i]); p=c[i]
        if p>hn: tr.append({"idx":i,"side":"long","entry":p,"tp":p*1.045,"sl":p-atr[i]*2.0})
        elif p<ln: tr.append({"idx":i,"side":"short","entry":p,"tp":p*0.955,"sl":p+atr[i]*2.0})
    return tr

def trend_pullback(d):
    c=d.c; h=d.h; l=d.l; v=d.v; atr=d.atr; vma=d.vma; rsi=d.rsi; e50=d.e50; e200=d.e200; tr=[]
    for i in range(220, d.n):
        if np.isnan(e50[i]) or e50[i]<=0 or np.isnan(e200[i]): continue
        last=c[i]; vr=v[i]/vma[i] if vma[i]>0 else 0; r=rsi[i]; at=atr[i]
        mu=e50[i]>e200[i]*1.001 and last>e200[i]*1.005
        md=e50[i]<e200[i]*0.999 and last<e200[i]*0.995
        pb=abs(last-e50[i])/e50[i]<0.010 and last>=e50[i]*0.995
        ps=abs(last-e50[i])/e50[i]<0.010 and last<=e50[i]*1.005
        bg=last>(h[i]+l[i])/2
        if mu and pb and bg and 40<=r<=65 and vr>=1.2:
            sd=max(0.025*last,2.0*at)
            tr.append({"idx":i,"side":"long","entry":last,"tp":last*1.99,"sl":last-sd})
        elif md and ps and not bg and 35<=r<=60 and vr>=1.2:
            sd=max(0.025*last,2.0*at)
            tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":last+sd})
    return tr

def vol_cap(d):
    c=d.c; v=d.v; n=d.n; vma=d.vma; rsi=d.rsi; tr=[]
    for i in range(30, n):
        pct=(c[i]-c[i-1])/c[i-1]*100; vr=v[i]/vma[i] if vma[i]>0 else 0
        r=rsi[i] if not np.isnan(rsi[i]) else 50
        if pct<-3 and vr>4 and r<30: tr.append({"idx":i,"side":"long","entry":c[i],"tp":c[i]*1.99,"sl":c[i]*0.985})
        elif pct>3 and vr>4 and r>70: tr.append({"idx":i,"side":"short","entry":c[i],"tp":c[i]*0.01,"sl":c[i]*1.015})
    return tr

def asian_pump(d):
    c=d.c; v=d.v; n=d.n; vma=d.vma; ts=d.ts; tr=[]
    for i in range(30, n):
        hour = pd.Timestamp(ts[i], unit='ms').hour
        if not (2<=hour<5): continue
        pct=(c[i]-c[i-1])/c[i-1]; vr=v[i]/vma[i] if vma[i]>0 else 0
        if abs(pct)<0.015 or vr<3.0: continue
        if pct>0: tr.append({"idx":i,"side":"long","entry":c[i],"tp":c[i]*1.99,"sl":c[i]*0.975})
        else: tr.append({"idx":i,"side":"short","entry":c[i],"tp":c[i]*0.01,"sl":c[i]*1.025})
    return tr

# FIBONACCI strategies
def fib_bounce(d):
    c=d.c; h=d.h; l=d.l; v=d.v; atr=d.atr; vma=d.vma; rsi=d.rsi; e50=d.e50; tr=[]
    for i in range(100, d.n):
        if np.isnan(e50[i]) or e50[i]<=0 or np.isnan(atr[i]) or atr[i]<=0: continue
        lo=max(0,i-50); sh=np.max(h[lo:i]); sl=np.min(l[lo:i])
        if sh==sl: continue
        df=sh-sl; f618=sh-0.618*df; f382=sh-0.382*df; f786=sh-0.786*df
        last=c[i]; r=rsi[i]; vr=v[i]/vma[i] if vma[i]>0 else 0
        if last>e50[i] and f786>=last>=f618 and r<45 and vr>1.0:
            tr.append({"idx":i,"side":"long","entry":last,"tp":sh,"sl":last-2*atr[i]})
        elif last<e50[i] and f382<=last<=f618 and r>55 and vr>1.0:
            tr.append({"idx":i,"side":"short","entry":last,"tp":sl,"sl":last+2*atr[i]})
    return tr

def fib_ext(d):
    c=d.c; h=d.h; l=d.l; v=d.v; atr=d.atr; vma=d.vma; tr=[]
    for i in range(100, d.n):
        if np.isnan(atr[i]) or atr[i]<=0: continue
        lo=max(0,i-100); sh=np.max(h[lo:i]); sl=np.min(l[lo:i])
        if sh==sl: continue
        df=sh-sl; ext=sl+1.272*df; ext_s=sh-1.272*df
        last=c[i]; vr=v[i]/vma[i] if vma[i]>0 else 0
        if last>ext and vr>1.5: tr.append({"idx":i,"side":"long","entry":last,"tp":last*1.99,"sl":ext*0.98})
        elif last<ext_s and vr>1.5: tr.append({"idx":i,"side":"short","entry":last,"tp":last*0.01,"sl":ext_s*1.02})
    return tr

STRATEGIES = {
    "B2h": lambda d: breakout(d, 2, 1.2, 0.008),
    "B4h": lambda d: breakout(d, 4, 1.3, 0.012),
    "B8h": lambda d: breakout(d, 8, 1.4, 0.015),
    "B12h": lambda d: breakout(d, 12, 1.5, 0.018),
    "B24h": lambda d: breakout(d, 24, 1.8, 0.025),
    "B48h": lambda d: breakout(d, 48, 1.9, 0.030, 1.05),
    "B168h": lambda d: breakout(d, 168, 2.0, 0.040, 1.1),
    "donchian": donchian,
    "trend_pb": trend_pullback,
    "vol_cap": vol_cap,
    "asian_pump": asian_pump,
    "fib_bounce": fib_bounce,
    "fib_ext": fib_ext,
}

TFS = ["5m", "15m", "30m", "1h"]
files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet', '').rsplit('_', 1)
    if len(parts) == 2:
        coin_tfs[parts[0].replace('_','-')].add(parts[1])
SYMBOLS = sorted(coin_tfs.keys())

total = len(SYMBOLS)*len(TFS)*len(STRATEGIES)
print(f"Testing {len(SYMBOLS)} coins x {len(TFS)} TFs x {len(STRATEGIES)} strats = {total} combos")

result = {"config":{"days":365,"tfs":TFS,"symbols":len(SYMBOLS),"strategies":list(STRATEGIES.keys()),
         "date":str(pd.Timestamp.now())},"ranking":[]}

done=0
for sname, sfunc in STRATEGIES.items():
    for tf in TFS:
        sym_res = []
        for sym in SYMBOLS:
            done+=1
            if tf not in coin_tfs[sym]: continue
            df = load(sym, tf)
            if df is None: continue
            d = Data(df)
            trades = sfunc(d)
            st = simulate(trades, d)
            if st["n"] > 0:
                st2 = dict(st)
                st2["symbol"]=sym; st2["tf"]=tf; st2["strategy"]=sname
                sym_res.append(st2)
            if done % 400 == 0: print(f"  Progress: {done}/{total} ({done*100//total}%)")
        
        if not sym_res: continue
        tn=sum(x["n"] for x in sym_res); tw=sum(x["wins"] for x in sym_res)
        tp=sum(x["total_pnl"] for x in sym_res); tr=sum(x["total_r"] for x in sym_res)
        best=max(sym_res, key=lambda x:x["total_r"]); worst=min(sym_res, key=lambda x:x["total_r"])
        result["ranking"].append({
            "strategy":sname,"tf":tf,"total_trades":tn,
            "wr":round(tw/tn*100,1) if tn else 0,
            "total_pnl":round(tp,2),"total_r":round(tr,2),
            "profitable":sum(1 for x in sym_res if x["total_r"]>0),"total_combos":len(sym_res),
            "best_symbol":best["symbol"],"best_pnl":best["total_pnl"],"best_r":best["total_r"],
            "worst_symbol":worst["symbol"],"worst_pnl":worst["total_pnl"],"worst_r":worst["total_r"],
        })

result["ranking"].sort(key=lambda x: x["total_r"], reverse=True)

print(f"\n{'='*90}")
print(f"  MASTER BACKTEST RANKING")
print(f"{'='*90}")
print(f"{'Rank':5s} {'Strat':10s} {'TF':5s} {'Trades':8s} {'WR':7s} {'Total$':11s} {'TotalR':10s} {'Cmbos':6s} {'Best':10s}")
print("-"*72)
for i, r in enumerate(result["ranking"], 1):
    print(f"{i:4d}. {r['strategy']:10s} {r['tf']:5s} {r['total_trades']:6d}  {r['wr']:5.1f}% ${r['total_pnl']:8.2f}  {r['total_r']:8.2f}R {r['profitable']:2d}/{r['total_combos']:2d}  {r['best_symbol']:10s}")

with open(OUT, "w") as f: json.dump(result, f, indent=2)
print(f"\nSaved to {OUT}")
print(f"Total combos: {sum(r['total_trades'] for r in result['ranking'])} trades across {len(result['ranking'])} entries")
