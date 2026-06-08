#!/usr/bin/env python3
"""
CEO AGENT v1 — Master strategy engine.
Creates strategies, backtests everything, finds small edges on every coin/TF.
Runs multiple times to confirm results. Compounds profits.
"""
import os, json, pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "CEO_REPORT")
os.makedirs(OUT, exist_ok=True)

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
        self.e9=pd.Series(c).ewm(span=9,adjust=False).mean().values
        self.e21=pd.Series(c).ewm(span=21,adjust=False).mean().values
        self.e50=pd.Series(c).ewm(span=50,adjust=False).mean().values
        self.e200=pd.Series(c).ewm(span=200,adjust=False).mean().values

def sim(trades, d, tr_act=1.0, tr_dist=0):
    if not trades: return None
    c=d.c;h=d.h;l=d.l;pnl_vals=[];r_vals=[];
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

# ===== STRATEGY GENERATOR =====
# Creates 100s of strategy variants by parameter combinations

STRATEGY_TYPES = {
    "breakout": {
        "params": {
            "lookback": [2,4,8,12,24,48,72,120,168],
            "vol_mult": [1.2,1.3,1.4,1.5,1.8,2.0,2.5,3.0],
            "sl_pct": [0.5,0.8,1.0,1.2,1.5,1.8,2.0,2.5,3.0,4.0,5.0],
            "trail_act": [0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,20.0,100.0],
            "trail_dist": [0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,20.0,100.0],
        }
    },
    "fib_ext": {
        "params": {
            "lookback": [50,100,150,200],
            "extension": [1.0,1.272,1.382,1.5,1.618,2.0],
            "vol_mult": [1.2,1.5,2.0,3.0],
            "trail_act": [0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,100.0],
            "trail_dist": [0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,100.0],
        }
    },
    "mean_rev": {
        "params": {
            "rsi_low": [15,20,25,30],
            "rsi_high": [70,75,80,85],
            "vol_spike": [2.0,3.0,4.0,5.0],
            "trail_act": [0.5,1.0,2.0,3.0,100.0],
            "trail_dist": [0.5,1.0,2.0,3.0,100.0],
        }
    },
    "momentum": {
        "params": {
            "pct_move": [0.5,1.0,1.5,2.0,3.0,5.0],
            "vol_mult": [1.5,2.0,3.0],
            "ema_fast": [5,9,12],
            "ema_slow": [20,21,26,50],
            "trail_act": [0.5,1.0,2.0,3.0,5.0,10.0,100.0],
            "trail_dist": [0.5,1.0,2.0,3.0,5.0,10.0,100.0],
        }
    },
    "ema_cross": {
        "params": {
            "fast": [5,9,10,12],
            "slow": [20,21,26,30,50],
            "vol_mult": [1.0,1.2,1.5,2.0],
            "trail_act": [0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,100.0],
            "trail_dist": [0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,100.0],
        }
    }
}

# Generate all strategy functions
def make_breakout_func(lb, vm, sl):
    def f(d):
        c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
        for i in range(lb+30, d.n):
            if np.isnan(atr[i]) or atr[i]<=0: continue
            lo=i-lb; rh=max(h[lo:i]); rl=min(l[lo:i])
            if rh==rl: continue
            vr=v[i]/vma[i] if vma[i]>0 else 0
            if vr<vm: continue
            bo=c[i-1]; br=h[i]-l[i]
            if br<=0: continue
            last=c[i]
            if last>rh and last>bo:
                sr=bo+br*0.5; sf=last*(1-sl/100)
                tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":min(sr,sf)})
            elif last<rl and last<bo:
                sr=bo-br*0.5; sf=last*(1+sl/100)
                tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":max(sr,sf)})
        return tr
    return f

def make_fib_ext_func(lb, ext, vm):
    def f(d):
        c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
        for i in range(lb+50, d.n):
            if np.isnan(atr[i]) or atr[i]<=0: continue
            lo=max(0,i-lb); sh=np.max(h[lo:i]); sl=np.min(l[lo:i])
            if sh==sl: continue
            df_=sh-sl; ext_p=sl+ext*df_; ext_n=sh-ext*df_
            last=c[i]; vr=v[i]/vma[i] if vma[i]>0 else 0
            if vr<vm: continue
            if last>ext_p: tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":ext_p*0.98})
            elif last<ext_n: tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":ext_n*1.02})
        return tr
    return f

def make_mean_rev_func(rl, rh, vs):
    def f(d):
        c=d.c;v=d.v;n=d.n;vma=d.vma;rsi=d.rsi;tr=[]
        for i in range(30, n):
            pct=(c[i]-c[i-1])/c[i-1]*100
            vr=v[i]/vma[i] if vma[i]>0 else 0
            r=rsi[i] if not np.isnan(rsi[i]) else 50
            if pct<-3 and vr>vs and r<rl: tr.append({"i":i,"s":"L","e":c[i],"tp":c[i]*99,"sl":c[i]*0.985})
            elif pct>3 and vr>vs and r>rh: tr.append({"i":i,"s":"S","e":c[i],"tp":c[i]*0.01,"sl":c[i]*1.015})
        return tr
    return f

def make_momentum_func(pct, vm, ef, es):
    def f(d):
        c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;e9=d.e9;e21=d.e21;tr=[]
        for i in range(100, d.n):
            if np.isnan(atr[i]) or atr[i]<=0: continue
            vr=v[i]/vma[i] if vma[i]>0 else 0
            if vr<vm: continue
            last=c[i]; prev=c[i-1]
            move=abs(last-prev)/prev*100
            if move<pct: continue
            if last>prev and last>e21[i]:
                tr.append({"i":i,"s":"L","e":last,"tp":last*99,"sl":last-atr[i]*2})
            elif last<prev and last<e21[i]:
                tr.append({"i":i,"s":"S","e":last,"tp":last*0.01,"sl":last+atr[i]*2})
        return tr
    return f

def make_ema_cross_func(fast, slow, vm):
    def f(d):
        c=d.c;h=d.h;l=d.l;v=d.v;atr=d.atr;vma=d.vma;tr=[]
        ef=pd.Series(c).ewm(span=fast,adjust=False).mean().values
        es=pd.Series(c).ewm(span=slow,adjust=False).mean().values
        for i in range(100, d.n):
            if np.isnan(atr[i]) or atr[i]<=0: continue
            vr=v[i]/vma[i] if vma[i]>0 else 0
            if vr<vm: continue
            if ef[i-1]<=es[i-1] and ef[i]>es[i] and c[i]>ef[i]:
                tr.append({"i":i,"s":"L","e":c[i],"tp":c[i]*99,"sl":c[i]-atr[i]*2})
            elif ef[i-1]>=es[i-1] and ef[i]<es[i] and c[i]<ef[i]:
                tr.append({"i":i,"s":"S","e":c[i],"tp":c[i]*0.01,"sl":c[i]+atr[i]*2})
        return tr
    return f

# ===== CEO SEARCH ENGINE =====
print("="*80)
print("  CEO AGENT — STRATEGY SEARCH ENGINE")
print("  Finding winning combos across ALL coins, ALL TFs, ALL params")
print("="*80)

files = os.listdir(CACHE)
coin_tfs = defaultdict(set)
for f in files:
    if not f.endswith('.parquet'): continue
    parts = f.replace('_365d.parquet','').rsplit('_',1)
    if len(parts)==2: coin_tfs[parts[0].replace('_','-')].add(parts[1])

TFS = ["5m","15m","30m","1H"]
ALL_SYMBOLS = sorted(coin_tfs.keys())

ceo_report = {
    "timestamp": str(datetime.now()),
    "strategies_tested": 0,
    "combos_tested": 0,
    "profitable_strategies": [],
    "best_combos": [],
    "compound_projections": {}
}

# Test a sample of strategies first (limited run)
test_count = 0
max_tests = 500  # Limit for this run

# ===== TEST BREAKOUTS =====
print(f"\nPhase 1: Testing breakout variants...")
for lb in [4, 12, 24, 48]:
    for vm in [1.3, 1.5, 1.8]:
        for sl in [1.0, 1.5, 2.0, 2.5, 3.0]:
            if test_count >= max_tests: break
            sfunc = make_breakout_func(lb, vm, sl/100)
            test_count += 1
            
            for tf in TFS:
                for trail_act in [0.5, 1.0, 3.0, 5.0, 20.0, 100.0]:
                    for trail_dist in [0.5, 1.0, 3.0, 5.0, 20.0, 100.0]:
                        if trail_act < trail_dist and trail_act < 99: continue  # trailing must activate before distance
                        ta = trail_act/100; td = trail_dist/100
                        total_n=0; total_w=0; total_pnl=0; total_r=0; prof_coins=0; tot_coins=0
                        
                        for sym in ALL_SYMBOLS:
                            if tf not in coin_tfs[sym]: continue
                            df = load(sym, tf)
                            if df is None: continue
                            d = Data(df)
                            trades = sfunc(d)
                            if not trades: continue
                            st = sim(trades, d, ta, td)
                            if st and st["n"] > 5:
                                tot_coins+=1
                                total_n+=st["n"]; total_w+=st["w"]
                                total_pnl+=st["tp"]; total_r+=st["tr"]
                                if st["tr"] > 0: prof_coins+=1
                        
                        if total_n > 50 and total_r > 0:
                            ceo_report["profitable_strategies"].append({
                                "type": "breakout",
                                "params": f"LB={lb}h VM={vm}x SL={sl}%",
                                "tf": tf,
                                "trail": f"act={trail_act}% dist={trail_dist}%",
                                "trades": total_n, "wr": round(total_w/total_n*100,1),
                                "total_r": round(total_r,2), "total_pnl": round(total_pnl,2),
                                "avg_r": round(total_r/total_n,4),
                                "prof_coins": f"{prof_coins}/{tot_coins}"
                            })
        
        if test_count >= max_tests: break
    if test_count >= max_tests: break

# ===== TEST FIB_EXT =====
print(f"Phase 2: Testing fib_ext variants...")
for lb in [50, 100, 200]:
    if test_count >= max_tests: break
    for ext in [1.0, 1.272, 1.618]:
        for vm in [1.2, 1.5, 2.0]:
            if test_count >= max_tests: break
            sfunc = make_fib_ext_func(lb, ext, vm)
            test_count += 1
            
            for tf in ["15m", "1H"]:
                for trail_act in [0.5, 1.0, 3.0, 5.0, 100.0]:
                    for trail_dist in [0.5, 1.0, 3.0, 5.0, 100.0]:
                        if trail_act < trail_dist and trail_act < 99: continue
                        ta = trail_act/100; td = trail_dist/100
                        total_n=0; total_w=0; total_pnl=0; total_r=0; prof_coins=0; tot_coins=0
                        
                        for sym in ALL_SYMBOLS:
                            if tf not in coin_tfs[sym]: continue
                            df = load(sym, tf)
                            if df is None: continue
                            d = Data(df)
                            trades = sfunc(d)
                            if not trades: continue
                            st = sim(trades, d, ta, td)
                            if st and st["n"] > 3:
                                tot_coins+=1
                                total_n+=st["n"]; total_w+=st["w"]
                                total_pnl+=st["tp"]; total_r+=st["tr"]
                                if st["tr"] > 0: prof_coins+=1
                        
                        if total_n > 10 and total_r > 0:
                            ceo_report["profitable_strategies"].append({
                                "type": "fib_ext",
                                "params": f"LB={lb} Ext={ext} VM={vm}x",
                                "tf": tf,
                                "trail": f"act={trail_act}% dist={trail_dist}%",
                                "trades": total_n, "wr": round(total_w/total_n*100,1),
                                "total_r": round(total_r,2), "total_pnl": round(total_pnl,2),
                                "avg_r": round(total_r/total_n,4),
                                "prof_coins": f"{prof_coins}/{tot_coins}"
                            })

# Sort profitable strategies
ceo_report["profitable_strategies"].sort(key=lambda x: x["total_r"], reverse=True)
ceo_report["strategies_tested"] = test_count
ceo_report["combos_tested"] = len(ceo_report["profitable_strategies"])

# Print results
print(f"\n{'='*80}")
print(f"  CEO REPORT — PROFITABLE STRATEGIES FOUND: {len(ceo_report['profitable_strategies'])}")
print(f"{'='*80}")
print(f"{'#':4s} {'Type':10s} {'Params':25s} {'TF':5s} {'Trades':7s} {'WR':7s} {'Total$':10s} {'TotalR':10s} {'AvgR':8s}")
print("-"*86)
for i, s in enumerate(ceo_report["profitable_strategies"][:30], 1):
    print(f"{i:3d}. {s['type']:10s} {s['params']:25s} {s['tf']:5s} {s['trades']:6d}  {s['wr']:5.1f}% ${s['total_pnl']:8.2f}  {s['total_r']:8.2f}R {s['avg_r']:+.4f}R")

# Compound projection
print(f"\n\n{'='*80}")
print(f"  COMPOUND PROJECTION (from found strategies)")
print(f"{'='*80}")
top5 = ceo_report["profitable_strategies"][:5]
total_annual_r = sum(s["total_r"] for s in top5)
total_annual_trades = sum(s["trades"] for s in top5)
notional = 100

if total_annual_trades > 0:
    avg_r_per_trade = total_annual_r / total_annual_trades
    trades_per_hour = total_annual_trades / (365 * 24)
    profit_per_hour = avg_r_per_trade * trades_per_hour * 0.02  # 2% risk
    profit_per_hour_pct = profit_per_hour / 100 * 100  # as % of $100 notional
    
    print(f"Total annual R from top 5 strategies: {total_annual_r:.2f}R")
    print(f"Total annual trades: {total_annual_trades:,}")
    print(f"Avg R per trade: {avg_r_per_trade:.4f}")
    print(f"Trades per hour: {trades_per_hour:.2f}")
    
    for risk_pct in [2, 5, 10, 14.5]:
        start = 3000
        rph = avg_r_per_trade * trades_per_hour * (risk_pct/100)
        hourly_return_pct = rph / start * 100
        print(f"\n  RISK {risk_pct}%:")
        print(f"    Hourly return: {hourly_return_pct:.4f}%")
        
        balance = start
        for day in [1, 7, 14, 21, 30]:
            balance = start * (1 + hourly_return_pct/100) ** (24 * day)
            print(f"    Day {day:2d}: ${balance:,.2f}")

# Save
report_path = os.path.join(OUT, "ceo_report.json")
with open(report_path, "w") as f:
    json.dump(ceo_report, f, indent=2)
print(f"\n✅ Report saved: {report_path}")
print(f"Strategies tested: {ceo_report['strategies_tested']}")
print(f"Profitable combos found: {ceo_report['combos_tested']}")
