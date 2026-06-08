#!/usr/bin/env python3
"""
8-HOUR MEGA BACKTEST — BloFin + Hyperliquid, all TFs, exhaustive params.
Run overnight. Finds the absolute best configuration.
"""
import os, sys, json, time, math, itertools
import numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)

TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
BAL=100; LEV=10; RISK=0.10

def ema(s,n): return s.ewm(span=n,adjust=False).mean()
def rsi(c,p=14):
    d=c.diff();g=d.clip(lower=0);l=-d.clip(upper=0)
    return 100-(100/(1+g.ewm(span=p,adjust=False).mean()/l.ewm(span=p,adjust=False).mean().replace(0,1e-9)))

def load_all():
    c={}
    for f in os.listdir(CACHE):
        if not f.endswith(".parquet"): continue
        try:
            parts=f.replace(".parquet","").split("_")
            sym=f"{parts[0]}-{parts[1]}"
            tf=parts[2]
            if tf in TFS and len(parts)>=4:
                df=pd.read_parquet(os.path.join(CACHE,f)).sort_values("ts").reset_index(drop=True)
                if len(df)>=100: c[(sym,tf)]=df
        except: pass
    return c

def fib_bounce(df, sl, trail, activate, adx_min, fib_level):
    c=df["close"];h=df["high"];l=df["low"];v=df["volume"]
    h100=h.rolling(100).max();l100=l.rolling(100).min()
    target=l100+fib_level*(h100-l100)
    near=abs(c-target)/target.replace(0,1e-9)<0.012
    rev=(c>c.shift(1))&(c.shift(1)<=c.shift(2))
    vok=(v/v.rolling(50).mean().replace(0,1e-9))>0.6
    r=rsi(c);rok=(r>25)&(r<55)
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=tr.ewm(span=14,adjust=False).mean()
    up=h.diff();down=l.shift()-l
    pdm=np.where((up>down)&(up>0),up,0);ndm=np.where((down>up)&(down>0),down,0)
    pdi=100*pd.Series(pdm).ewm(span=14,adjust=False).mean()/atr.replace(0,1e-9)
    ndi=100*pd.Series(ndm).ewm(span=14,adjust=False).mean()/atr.replace(0,1e-9)
    dx=100*abs(pdi-ndi)/(pdi+ndi+1e-9)
    adx=pd.Series(dx).ewm(span=14,adjust=False).mean()
    regime=(adx>adx_min)&(pdi>ndi)
    return near&rev&vok&rok&regime

def sim(sigs,df,tf_min,sl,trail,activate):
    c=df["close"];h=df["high"];l=df["low"]
    mb=max(int((96*60)/tf_min),24)
    trades=[];active=None
    for sig in sigs[:200]:
        if active: continue
        bi=sig["bar"]
        if bi>=len(c)-5: continue
        ep=c.iloc[bi];active={"ep":ep,"hw":ep,"ta":False,"ts":None}
        for i in range(bi+1,len(df)):
            active["hw"]=max(active["hw"],h.iloc[i])
            prof=(active["hw"]-ep)/ep
            if not active["ta"] and prof>=activate: active["ta"]=True;active["ts"]=active["hw"]*(1-trail)
            if active["ta"]: active["ts"]=max(active["ts"],active["hw"]*(1-trail))
            esl=max(ep*(1-sl),active.get("ts",ep*(1-sl))) if active["ta"] else ep*(1-sl)
            if l.iloc[i]<=esl: trades.append({"pnl":(esl-ep)/ep,"bars":i-bi,"trailed":active["ta"]});active=None;break
            if i-bi>=mb: trades.append({"pnl":(c.iloc[i]-ep)/ep,"bars":mb,"trailed":False});active=None;break
    return trades

def stats(tr):
    if not tr or len(tr)<5: return None
    bal=BAL;pk=bal;dd=0;w=l=tw=0
    for t in tr:
        m=bal*RISK;bal+=m*LEV*t["pnl"]
        if bal<=0: bal=0;break
        if t["pnl"]>0.0001: w+=1;tw+=t["trailed"]
        elif t["pnl"]<-0.0001: l+=1
        if bal>pk: pk=bal
        dd=max(dd,(pk-bal)/pk*100 if pk>0 else 0)
    tot=w+l
    return {"bal":round(bal,2),"ret":round((bal/BAL-1)*100,1),"tot":tot,"w":w,"l":l,
            "wr":round(w/tot*100,1),"dd":round(dd,1),"tw":tw}

# Parameter grid — expanded for 8-hour run
SLS = [0.05, 0.07, 0.10]
TRAILS = [0.03, 0.04, 0.05, 0.06, 0.08]
ACTIVATES = [0.02, 0.03, 0.04]
ADX_MINS = [20, 22, 25]
FIBS = [0.382, 0.500, 0.618, 0.786]

# Generate combos (filter invalid ones)
combos = []
for sl, trail, act, adx, fib in itertools.product(SLS, TRAILS, ACTIVATES, ADX_MINS, FIBS):
    if act >= trail: continue
    if trail < sl * 0.3: continue  # Trail must be at least 30% of SL
    combos.append((sl, trail, act, adx, fib))

print(f"Testing {len(combos)} parameter combos × {len(TFS)} TFs = {len(combos)*len(TFS)} tests")
print(f"Across all available coins (BloFin + Hyperliquid)")
t0=time.time()

data = load_all()
n_coins = len(set(s for s,_ in data))
print(f"Data: {len(data)} datasets, ~{n_coins} coins")

all_results = []
total = len(combos) * len(TFS)
done = 0

for sl, trail, act, adx_min, fib in combos:
    for tf, m in TFS.items():
        done += 1
        step = {"5m":6,"15m":3,"30m":2,"1H":1,"4H":1}[tf]
        all_tr = []

        for (sym, dtf), df in data.items():
            if dtf != tf: continue
            longs = fib_bounce(df, sl, trail, act, adx_min, fib)
            sigs = [{"bar":i,"side":"long"} for i in range(100,len(df),step) if longs.iloc[i]]
            all_tr.extend(sim(sigs, df, m, sl, trail, act))

        st = stats(all_tr)
        if st:
            st.update({"sl":sl,"trail":trail,"act":act,"adx":adx_min,"fib":fib,"tf":tf})
            all_results.append(st)

        if done % 50 == 0:
            elapsed = time.time()-t0
            eta = (elapsed/done) * (total-done)
            print(f"  [{done}/{total}] {elapsed/60:.0f}min elapsed, ~{eta/60:.0f}min remaining | "
                  f"{len(all_results)} results so far", flush=True)

# Save partial
all_results.sort(key=lambda x:-x["ret"])
ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
with open(os.path.join(OUT,f"backtest_8hour_{ts}.json"),"w") as f:
    json.dump(all_results[:200], f, indent=2)

print(f"\n{'='*80}")
print(f"DONE — {(time.time()-t0)/60:.1f} min | {len(all_results)} results")
print(f"{'='*80}")
print(f"\n🏆 TOP 15:")
for i,r in enumerate(all_results[:15],1):
    print(f"{i:2}. SL={r['sl']*100:.0f}% Trail={r['trail']*100:.0f}% Act={r['act']*100:.0f}% "
          f"ADX>{r['adx']} Fib={r['fib']:.3f} @ {r['tf']}")
    print(f"    ret={r['ret']:+.1f}% WR={r['wr']:.0f}% tr={r['tot']} DD={r['dd']:.0f}%")

print(f"\nSaved: backtest_8hour_{ts}.json")
