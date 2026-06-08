#!/usr/bin/env python3
"""FAST 20-strategy backtest — 5 coins, stepped bars, capped trades."""
import os, sys, json, math, time as _time
from collections import defaultdict
import numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)

SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","DOGE-USDT","BNB-USDT"]
TFS = {"5m":5,"15m":15,"30m":30,"1H":60}
STEP = {"5m":6,"15m":3,"30m":2,"1H":1}
BAL = 100; LEV = 5; RISK = 0.02

def ema(s,n): return s.ewm(span=n,adjust=False).mean()
def rsi(c,p=14):
    d=c.diff();g=d.clip(lower=0);l=-d.clip(upper=0)
    return 100-(100/(1+g.ewm(span=p,adjust=False).mean()/l.ewm(span=p,adjust=False).mean().replace(0,1e-9)))
def adx(df,p=14):
    h,l,c=df["high"],df["low"],df["close"]
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    u=h.diff();d=l.shift()-l
    pdm=np.where((u>d)&(u>0),u,0);ndm=np.where((d>u)&(d>0),d,0)
    a=pd.Series(tr).ewm(span=p,adjust=False).mean()
    pdi=100*pd.Series(pdm).ewm(span=p,adjust=False).mean()/a.replace(0,1e-9)
    ndi=100*pd.Series(ndm).ewm(span=p,adjust=False).mean()/a.replace(0,1e-9)
    dx=100*abs(pdi-ndi)/(pdi+ndi+1e-9)
    return pd.Series(dx).ewm(span=p,adjust=False).mean(),pdi,ndi

def load():
    c={}
    for s in SYMBOLS:
        for tf,m in TFS.items():
            p=os.path.join(CACHE,f"{s.replace('-','_')}_{tf}_365d.parquet")
            if os.path.exists(p):
                df=pd.read_parquet(p).sort_values("ts").reset_index(drop=True)
                cut=df["ts"].max()-(365*24*3600*1000)
                df=df[df["ts"]>=cut].copy()
                if len(df)>=200: c[(s,tf)]=df
    return c

def signals(name,df):
    c=df["close"];h=df["high"];l=df["low"];v=df["volume"]
    e9,e21,e50=ema(c,9),ema(c,21),ema(c,50)
    r=rsi(c);ax,pdi,ndi=adx(df)
    vr=v/v.rolling(20).mean().replace(0,1e-9)
    lo,sh=pd.Series(False,index=df.index),pd.Series(False,index=df.index)

    if name=="1_BREAKOUT":
        h20=h.rolling(20).max().shift(1);l20=l.rolling(20).min().shift(1)
        lo=(ax>25)&(pdi>ndi)&(c>h20)&(vr>1.2)
        sh=(ax>25)&(ndi>pdi)&(c<l20)&(vr>1.2)
    elif name=="2_VOL_SURGE":
        lo=(vr>2)&(c>c.shift(1)*1.005)
        sh=(vr>2)&(c<c.shift(1)*0.995)
    elif name=="3_EMA_STACK":
        lo=(e9>e21)&(e21>e50)&(c>e9)&(vr>0.8)
        sh=(e9<e21)&(e21<e50)&(c<e9)&(vr>0.8)
    elif name=="4_PULLBACK":
        lo=(c.shift(3)>e50)&(abs(c-e21)/c<0.015)&(c>c.shift(1))&(vr>0.8)
        sh=(c.shift(3)<e50)&(abs(c-e21)/c<0.015)&(c<c.shift(1))&(vr>0.8)
    elif name=="5_ADX_RSI":
        lo=(ax>25)&(r>40)&(r<65)&(e9>e21)&(c>e9)&(vr>1)
        sh=(ax>25)&(r>40)&(r<65)&(e9<e21)&(c<e9)&(vr>1)
    elif name=="6_VOL_CLIMAX":
        lo=(vr>3)&(r<35)&(c>c.shift(1))
        sh=(vr>3)&(r>65)&(c<c.shift(1))
    elif name=="7_OPEN_RANGE":
        hr=h.rolling(24).max().shift(1);lr=l.rolling(24).min().shift(1)
        lo=(c>hr)&(vr>1.5);sh=(c<lr)&(vr>1.5)
    elif name=="8_MACD_CROSS":
        ml=e9-e21;ms=ema(pd.Series(e9-e21),9)
        lo=(ml>ms)&(ml.shift(1)<=ms.shift(1))&(c>e50)
        sh=(ml<ms)&(ml.shift(1)>=ms.shift(1))&(c<e50)
    elif name=="9_BB_SQUEEZE":
        bb_u,bb_l=ema(c,20)+2*c.rolling(20).std(),ema(c,20)-2*c.rolling(20).std()
        bw=(bb_u-bb_l)/ema(c,20).replace(0,1e-9)
        lo=(bw<0.05)&(c>bb_u.shift(1))&(vr>1.5)
        sh=(bw<0.05)&(c<bb_l.shift(1))&(vr>1.5)
    elif name=="10_TREND_FOLLOW":
        lo=(h>h.shift(1))&(h.shift(1)>h.shift(2))&(l>l.shift(1))&(e9>e21)&(vr>1)
        sh=(l<l.shift(1))&(l.shift(1)<l.shift(2))&(h<h.shift(1))&(e9<e21)&(vr>1)
    elif name=="11_FIB_BOUNCE":
        h50=h.rolling(50).max();l50=l.rolling(50).min();rng=h50-l50
        f382=l50+0.382*rng;f618=l50+0.618*rng
        n382=abs(c-f382)/f382.replace(0,1e-9)<0.012
        n618=abs(c-f618)/f618.replace(0,1e-9)<0.012
        lo=(n382|n618)&(c>c.shift(1))&(c.shift(1)<c.shift(2))
        sh=pd.Series(False,index=df.index)
    elif name=="12_MOM_BURST":
        mom=(c-c.shift(3))/c.shift(3).replace(0,1e-9)
        lo=(mom>0.02)&(vr>1.5)&(e9>e50)
        sh=(mom<-0.02)&(vr>1.5)&(e9<e50)
    elif name=="13_RANGE_EXP":
        atr=(pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)).ewm(span=14,adjust=False).mean()
        lo=(atr>atr.shift(20)*1.5)&(c>e21)&(vr>1.3)
        sh=(atr>atr.shift(20)*1.5)&(c<e21)&(vr>1.3)
    elif name=="14_PIVOT_BREAK":
        ph=pd.Series(False,index=df.index);pl=pd.Series(False,index=df.index)
        for i in range(5,len(h)-5):
            if h.iloc[i]==h.iloc[i-5:i+6].max(): ph.iloc[i]=True
            if l.iloc[i]==l.iloc[i-5:i+6].min(): pl.iloc[i]=True
        rph=h[ph].reindex(df.index).fillna(method='ffill').rolling(50,min_periods=1).max()
        rpl=l[pl].reindex(df.index).fillna(method='ffill').rolling(50,min_periods=1).min()
        lo=(c>rph.shift(1))&(vr>1.3)&(ax>20)
        sh=(c<rpl.shift(1))&(vr>1.3)&(ax>20)
    elif name=="15_DUAL_CONF":
        c1=ax>25;c2=vr>1.5;c3=(e9>e21)&(e21>e50);c4=(r>40)&(r<60)
        sc=c1.astype(int)+c2.astype(int)+c3.astype(int)+c4.astype(int)
        lo=(sc>=3)&c3;sh=(sc>=3)&(~c3)
    elif name=="16_VWAP_REV":
        vp=(c*v).rolling(48).sum()/v.rolling(48).sum().replace(0,1e-9)
        dv=(c-vp)/vp.replace(0,1e-9)
        lo=(dv<-0.02)&(r<30)&(c>c.shift(1))
        sh=(dv>0.02)&(r>70)&(c<c.shift(1))
    elif name=="17_ATR_BURST":
        o=df["open"]
        atr=(pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)).ewm(span=14,adjust=False).mean()
        lo=(c-o>2*atr)&(e9>e50)&(vr>1.5)
        sh=(o-c>2*atr)&(e9<e50)&(vr>1.5)
    elif name=="18_EMA_CROSS":
        cross_up=(e9>e21)&(e9.shift(1)<=e21.shift(1))
        cross_down=(e9<e21)&(e9.shift(1)>=e21.shift(1))
        lo=cross_up&(e21>e50)&(vr>0.8)
        sh=cross_down&(e21<e50)&(vr>0.8)
    elif name=="19_SUPP_RESIST":
        l50=l.rolling(50).min();h50=h.rolling(50).max()
        lo=(abs(c-l50)/l50.replace(0,1e-9)<0.01)&(c>c.shift(1))&(vr>1)
        sh=(abs(c-h50)/h50.replace(0,1e-9)<0.01)&(c<c.shift(1))&(vr>1)
    elif name=="20_ENSEMBLE":
        s1=(ax>25)&(pdi>ndi)&(c>h.rolling(20).max().shift(1))
        s2=(vr>2)&(c>c.shift(5))
        s3=(e9>e21)&(e21>e50)&(c>e9)
        s4=(r>40)&(r<65)&(c>e21)
        sc_long=s1.astype(int)+s2.astype(int)+s3.astype(int)+s4.astype(int)
        s1s=(ax>25)&(ndi>pdi)&(c<l.rolling(20).min().shift(1))
        s2s=(vr>2)&(c<c.shift(5))
        s3s=(e9<e21)&(e21<e50)&(c<e9)
        sc_short=s1s.astype(int)+s2s.astype(int)+s3s.astype(int)
        lo=sc_long>=3;sh=sc_short>=2
    return lo,sh

def sim(sigs,df,tf_min,sl=0.05):
    c=df["close"];h=df["high"];l=df["low"]
    trail_atr=(pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)).ewm(span=14,adjust=False).mean()
    trades=[]
    active=None
    for sig in sigs[:200]:  # CAP at 200 — quality over quantity
        if active: continue
        bi=sig["bar"]
        if bi>=len(c)-5: continue
        ep=c.iloc[bi];sd=sig["side"]
        mb=max(int(4*24*60/tf_min),12)
        active={"sd":sd,"ep":ep,"bi":bi,"hw":ep,"lw":ep,"ta":False,"ts":None}
        for i in range(bi+1,len(df)):
            bh=i-bi
            if sd=="long": active["hw"]=max(active["hw"],h.iloc[i])
            else: active["lw"]=min(active["lw"],l.iloc[i])
            prof=(active["hw"]-ep)/ep if sd=="long" else (ep-active["lw"])/ep
            td=min(max(4*trail_atr.iloc[bi]/ep,0.03),0.10)  # WIDER: 3-10% trail
            if not active["ta"] and prof>=td*1.3:
                active["ta"]=True
                active["ts"]=active["hw"]*(1-td) if sd=="long" else active["lw"]*(1+td)
            if active["ta"]:
                if sd=="long":
                    ns=active["hw"]*(1-td);active["ts"]=max(active.get("ts",0),ns)
                else:
                    ns=active["lw"]*(1+td);active["ts"]=min(active.get("ts",float("inf")),ns)
            xp=None;rs=None
            if sd=="long":
                esl=max(ep*(1-sl),active.get("ts",ep*(1-sl))) if active["ta"] else ep*(1-sl)
                if l.iloc[i]<=esl: xp=esl;rs="TRAIL" if active["ta"] else "SL"
            else:
                esl=min(ep*(1+sl),active.get("ts",ep*(1+sl))) if active["ta"] else ep*(1+sl)
                if h.iloc[i]>=esl: xp=esl;rs="TRAIL" if active["ta"] else "SL"
            if bh>=mb: xp=c.iloc[i];rs="TIME"
            if xp:
                pnl=(xp-ep)/ep if sd=="long" else (ep-xp)/ep
                trades.append({"pnl":pnl,"bars":bh,"trailed":active["ta"],"reason":rs})
                active=None;break;break
    return trades

def stats(tr):
    if not tr: return None
    bal=BAL;pk=bal;dd=0;w=0;l=0;tw=0;st=0;mx=0
    for t in sorted(tr,key=lambda x:len(str(x)))[:]:  # just use all
        m=bal*RISK;pnl_usd=m*LEV*t["pnl"]
        bal+=pnl_usd
        if bal<=0: bal=0;break
        if t["pnl"]>0.0001: w+=1;st=0;tw+=t["trailed"]
        elif t["pnl"]<-0.0001: l+=1;st+=1;mx=max(mx,st)
        if bal>pk: pk=bal
        dd=max(dd,(pk-bal)/pk*100 if pk>0 else 0)
    tot=w+l
    if tot==0: return None
    wr=w/tot*100
    return {"bal":round(bal,2),"ret":round((bal/BAL-1)*100,1),"tot":tot,"w":w,"l":l,
            "wr":round(wr,1),"dd":round(dd,1),"tw":tw,"mx_strk":mx}

def main():
    t0=_time.time()
    print("="*80)
    print("20 STRATEGIES × 4 TFs × 5 COINS — FAST BACKTEST")
    print("="*80)

    data=load()
    print(f"Loaded {len(data)} datasets in {_time.time()-t0:.1f}s")

    strategies=[f"{i}_{n}" for i,n in enumerate([
        "BREAKOUT","VOL_SURGE","EMA_STACK","PULLBACK","ADX_RSI",
        "VOL_CLIMAX","OPEN_RANGE","MACD_CROSS","BB_SQUEEZE","TREND_FOLLOW",
        "FIB_BOUNCE","MOM_BURST","RANGE_EXP","PIVOT_BREAK","DUAL_CONF",
        "VWAP_REV","ATR_BURST","EMA_CROSS","SUPP_RESIST","ENSEMBLE"
    ],1)]

    all_res=[]

    for sn in strategies:
        print(f"\n{'─'*60}\n  {sn}\n{'─'*60}")
        for tf,m in TFS.items():
            stp=STEP[tf]
            all_tr=[]
            for sym in SYMBOLS:
                df=data.get((sym,tf))
                if df is None: continue
                lo,sh=signals(sn,df)
                sigs=[]
                for i in range(60,len(df),stp):
                    if lo.iloc[i]: sigs.append({"bar":i,"side":"long"})
                    elif sh.iloc[i]: sigs.append({"bar":i,"side":"short"})
                if not sigs: continue
                for sl in [0.03,0.05]:
                    tr=sim(sigs,df,m,sl)
                    all_tr.extend(tr)
            if not all_tr: continue
            st=stats(all_tr)
            if st and st["tot"]>=5:
                st["strategy"]=sn;st["tf"]=tf
                all_res.append(st)
                ico="🔥" if st["ret"]>30 else ("✅" if st["ret"]>0 else "❌")
                print(f"  {tf:4s} {ico} ret={st['ret']:+6.1f}% WR={st['wr']:.0f}% tr={st['tot']} DD={st['dd']:.0f}%")

    # RANKINGS
    all_res.sort(key=lambda x:-x["ret"])
    print(f"\n{'='*80}")
    print("🏆 TOP 15 STRATEGIES")
    print(f"{'='*80}")
    print(f"{'Rank':<5} {'Strategy':<22s} {'TF':<5s} {'Return':<8s} {'WR':<6s} {'Tr':<5s} {'DD':<6s} {'TrailW':<7s}")
    print(f"{'─'*5} {'─'*22} {'─'*5} {'─'*8} {'─'*6} {'─'*5} {'─'*6} {'─'*7}")
    for i,r in enumerate(all_res[:15],1):
        ico="🔥" if r["ret"]>30 else ("✅" if r["ret"]>0 else "❌")
        print(f"{i:<5} {ico} {r['strategy']:<19s} {r['tf']:<5s} {r['ret']:+7.1f}% {r['wr']:5.1f}% {r['tot']:4d}  {r['dd']:5.1f}% {r['tw']:5d}w")

    # Best per TF
    print(f"\n{'─'*60}\nBEST PER TF\n{'─'*60}")
    for tf in TFS:
        tf_r=[r for r in all_res if r["tf"]==tf and r["ret"]>0]
        if tf_r:
            b=max(tf_r,key=lambda x:x["ret"])
            print(f"  {tf:4s}: {b['strategy']:<20s} {b['ret']:+.1f}% ({b['tot']}t, {b['wr']:.0f}% WR, {b['dd']:.0f}% DD)")

    # Winner patterns
    top=[r for r in all_res if r["ret"]>20]
    bot=[r for r in all_res if r["ret"]<-80]
    print(f"\n{'─'*60}\nWINNER vs LOSER PATTERNS\n{'─'*60}")
    if top:
        print(f"  WINNERS (>20%): avg ret={np.mean([r['ret'] for r in top]):+.0f}%, avg WR={np.mean([r['wr'] for r in top]):.0f}%, avg trades={np.mean([r['tot'] for r in top]):.0f}, avg DD={np.mean([r['dd'] for r in top]):.0f}%")
        tfs=defaultdict(int)
        for r in top: tfs[r["tf"]]+=1
        print(f"  TF distribution: {dict(tfs)}")
    if bot:
        print(f"  LOSERS (<-80%): avg ret={np.mean([r['ret'] for r in bot]):+.0f}%, avg WR={np.mean([r['wr'] for r in bot]):.0f}%, avg trades={np.mean([r['tot'] for r in bot]):.0f}, avg DD={np.mean([r['dd'] for r in bot]):.0f}%")

    # Save
    ts=pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    json_p=os.path.join(OUT,f"backtest_20fast_{ts}.json")
    csv_p=os.path.join(OUT,f"backtest_20fast_{ts}.csv")
    with open(json_p,"w") as f: json.dump(all_res,f,indent=2,default=str)
    with open(csv_p,"w") as f:
        f.write("strategy,tf,return_pct,wr,total,max_dd\n")
        for r in all_res: f.write(f"{r['strategy']},{r['tf']},{r['ret']},{r['wr']},{r['tot']},{r['dd']}\n")
    print(f"\n✅ Saved: {json_p}\n✅ Saved: {csv_p}")
    print(f"Total: {(_time.time()-t0)/60:.1f} min | {len(all_res)} results")

if __name__=="__main__":
    main()
