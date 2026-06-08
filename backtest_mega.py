#!/usr/bin/env python3
"""
MEGA BACKTEST — 4-5 hours, all timeframes, Hyperliquid + BloFin.
Tests winning strategies across 250+ coins.
Finds the absolute optimal configuration for max profit.
"""
import os, sys, json, time, math
from collections import defaultdict
import numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
HL_CACHE = os.path.join(WORK, "market_data_cache")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)
os.makedirs(HL_CACHE, exist_ok=True)

# ═══════════════════════════════
SYMBOLS_BLOFIN = ["BTC-USDT","ETH-USDT","SOL-USDT","DOGE-USDT","BNB-USDT",
                   "XRP-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT",
                   "LTC-USDT","DOT-USDT","ATOM-USDT","NEAR-USDT","APT-USDT",
                   "ARB-USDT","OP-USDT","INJ-USDT","TAO-USDT","TIA-USDT"]
TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
BAL=100; LEV=10; RISK=0.10

def ema(s,n): return s.ewm(span=n,adjust=False).mean()
def rsi(c,p=14):
    d=c.diff();g=d.clip(lower=0);l=-d.clip(upper=0)
    return 100-(100/(1+g.ewm(span=p,adjust=False).mean()/l.ewm(span=p,adjust=False).mean().replace(0,1e-9)))

def load_blofin():
    c={}
    for s in SYMBOLS_BLOFIN:
        for tf in TFS:
            p=os.path.join(CACHE,f"{s.replace('-','_')}_{tf}_365d.parquet")
            if os.path.exists(p):
                df=pd.read_parquet(p).sort_values("ts").reset_index(drop=True)
                cut=df["ts"].max()-(365*24*3600*1000)
                df=df[df["ts"]>=cut].copy()
                if len(df)>=200: c[(s,tf)]=df
    return c

def load_hyperliquid():
    """Load cached Hyperliquid data."""
    c={}
    for f in os.listdir(HL_CACHE):
        if f.endswith(".parquet") and "1h" in f.lower():
            coin = f.split("_")[0]
            sym = f"{coin}-USD"
            try:
                df=pd.read_parquet(os.path.join(HL_CACHE,f)).sort_values("ts").reset_index(drop=True)
                if len(df)>=100: c[(sym,"1H")]=df
            except: pass
    return c

def fib_bounce_strategy(df, sl_pct=0.07, trail_pct=0.05, activate_pct=0.03,
                         adx_min=22, fib_level=0.618):
    """The proven winning strategy with configurable parameters."""
    c=df["close"];h=df["high"];l=df["low"];v=df["volume"]

    # Fib level
    h100=h.rolling(100).max();l100=l.rolling(100).min()
    rng=h100-l100
    target=l100+fib_level*rng
    near_fib=abs(c-target)/target.replace(0,1e-9)<0.012

    # Reversal
    reversal=(c>c.shift(1))&(c.shift(1)<=c.shift(2))

    # Volume
    v_ok=(v/v.rolling(50).mean().replace(0,1e-9))>0.6

    # RSI
    r=rsi(c);r_ok=(r>25)&(r<55)

    # ADX regime
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=tr.ewm(span=14,adjust=False).mean()
    up=h.diff();down=l.shift()-l
    pdm=np.where((up>down)&(up>0),up,0);ndm=np.where((down>up)&(down>0),down,0)
    pdi=100*pd.Series(pdm).ewm(span=14,adjust=False).mean()/atr.replace(0,1e-9)
    ndi=100*pd.Series(ndm).ewm(span=14,adjust=False).mean()/atr.replace(0,1e-9)
    dx=100*abs(pdi-ndi)/(pdi+ndi+1e-9)
    adx=pd.Series(dx).ewm(span=14,adjust=False).mean()
    regime=(adx>adx_min)&(pdi>ndi)

    longs=near_fib&reversal&v_ok&r_ok&regime
    return longs

def sim_trades(signals, df, tf_min, sl_pct, trail_pct, activate_pct):
    c=df["close"];h=df["high"];l=df["low"]
    mb=max(int((96*60)/tf_min),24)
    trades=[];active=None
    for sig in signals[:200]:
        if active: continue
        bi=sig["bar"]
        if bi>=len(c)-5: continue
        ep=c.iloc[bi];active={"ep":ep,"hw":ep,"ta":False,"ts":None}
        for i in range(bi+1,len(df)):
            active["hw"]=max(active["hw"],h.iloc[i])
            prof=(active["hw"]-ep)/ep
            if not active["ta"] and prof>=activate_pct:
                active["ta"]=True;active["ts"]=active["hw"]*(1-trail_pct)
            if active["ta"]: active["ts"]=max(active["ts"],active["hw"]*(1-trail_pct))
            esl=max(ep*(1-sl_pct),active.get("ts",ep*(1-sl_pct))) if active["ta"] else ep*(1-sl_pct)
            if l.iloc[i]<=esl: trades.append({"pnl":(esl-ep)/ep,"bars":i-bi,"trailed":active["ta"]});active=None;break
            if i-bi>=mb: trades.append({"pnl":(c.iloc[i]-ep)/ep,"bars":mb,"trailed":False});active=None;break
    return trades

def compute_stats(trades):
    if not trades: return None
    bal=BAL;pk=bal;dd=0;w=l=tw=0
    for t in trades:
        m=bal*RISK;bal+=m*LEV*t["pnl"]
        if bal<=0: bal=0;break
        if t["pnl"]>0.0001: w+=1;tw+=t["trailed"]
        elif t["pnl"]<-0.0001: l+=1
        if bal>pk: pk=bal
        dd=max(dd,(pk-bal)/pk*100 if pk>0 else 0)
    tot=w+l
    if tot<5: return None
    return {"bal":round(bal,2),"ret":round((bal/BAL-1)*100,1),"tot":tot,"w":w,"l":l,
            "wr":round(w/tot*100,1),"dd":round(dd,1),"tw":tw,"avg_pnl":round(np.mean([t["pnl"]for t in trades])*100,3)}

def main():
    t0=time.time()
    print("="*80)
    print("MEGA BACKTEST — 4-5 Hours, All TFs, Hyperliquid + BloFin")
    print("="*80)

    data_blofin = load_blofin()
    data_hl = load_hyperliquid()
    all_data = {**data_blofin, **data_hl}

    n_coins = len(set(s for s,_ in all_data))
    print(f"Data: {len(all_data)} datasets across ~{n_coins} coins (BloFin + Hyperliquid)")

    # Parameter grid
    param_grid = [
        # (sl%, trail%, activate%, adx_min, fib_level)
        (0.05, 0.03, 0.02, 20, 0.618),
        (0.07, 0.05, 0.03, 22, 0.618),  # Current best
        (0.07, 0.05, 0.03, 25, 0.618),
        (0.10, 0.06, 0.04, 22, 0.618),
        (0.07, 0.04, 0.02, 22, 0.500),
        (0.05, 0.03, 0.02, 22, 0.500),
        (0.07, 0.05, 0.03, 22, 0.382),
        (0.05, 0.04, 0.02, 25, 0.618),  # Tighter trail, higher ADX
        (0.07, 0.06, 0.04, 22, 0.618),  # Wider trail
        (0.08, 0.05, 0.03, 20, 0.618),  # Wider SL
    ]

    all_results = []
    total_combos = len(param_grid) * len(TFS)

    for pi, (sl, trail, activate, adx_min, fib) in enumerate(param_grid):
        for tf, m in TFS.items():
            combo_name = f"SL={sl*100:.0f}% Trail={trail*100:.0f}% Act={activate*100:.0f}% ADX>{adx_min} Fib={fib:.3f} @ {tf}"
            print(f"\n[{pi*5+list(TFS.keys()).index(tf)+1}/{total_combos}] {combo_name}")

            step = {"5m":4,"15m":2,"30m":1,"1H":1,"4H":1}[tf]
            all_trades = []

            for (sym, dtf), df in all_data.items():
                if dtf != tf: continue
                longs = fib_bounce_strategy(df, sl, trail, activate, adx_min, fib)
                sigs = [{"bar":i,"side":"long"} for i in range(100,len(df),step) if longs.iloc[i]]
                all_trades.extend(sim_trades(sigs, df, m, sl, trail, activate))

            st = compute_stats(all_trades)
            if st:
                st["params"] = combo_name
                st["sl"] = sl; st["trail"] = trail; st["activate"] = activate
                st["adx_min"] = adx_min; st["fib"] = fib; st["tf"] = tf
                all_results.append(st)
                ico = "🔥" if st["ret"] > 100 else ("✅" if st["ret"] > 0 else "❌")
                print(f"  {ico} ret={st['ret']:+8.1f}% WR={st['wr']:.0f}% tr={st['tot']} DD={st['dd']:.0f}% trailW={st['tw']}")

    # Rankings
    all_results.sort(key=lambda x:-x["ret"])
    print(f"\n{'='*80}")
    print("🏆 TOP 20 CONFIGURATIONS")
    print(f"{'='*80}")
    for i,r in enumerate(all_results[:20],1):
        print(f"{i:2}. {r['params']}")
        print(f"    ret={r['ret']:+8.1f}% WR={r['wr']:.0f}% tr={r['tot']} DD={r['dd']:.0f}%")

    # Best by TF
    print(f"\n{'='*80}\nBEST PER TIMEFRAME\n{'='*80}")
    for tf in TFS:
        tf_r = [r for r in all_results if r["tf"]==tf]
        if tf_r:
            b = max(tf_r, key=lambda x:x["ret"])
            print(f"  {tf}: {b['params']} → {b['ret']:+.1f}% ({b['tot']}t, {b['wr']:.0f}% WR)")

    # Save
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(OUT,f"mega_backtest_{ts}.json"),"w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n✅ Saved mega_backtest_{ts}.json")
    print(f"Total: {(time.time()-t0)/60:.1f} min")

if __name__=="__main__":
    main()
