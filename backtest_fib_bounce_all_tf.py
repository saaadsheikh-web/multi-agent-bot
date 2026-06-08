#!/usr/bin/env python3
"""FIB_BOUNCE optimized — ALL timeframes, vectorized regime filter."""
import os, numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","DOGE-USDT","BNB-USDT","XRP-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT"]
TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
BAL=100; LEV=5; RISK=0.02; SL=0.07; TRAIL=0.05; TRAIL_ACT=0.03; ADX_MIN=22

def ema(s,n): return s.ewm(span=n,adjust=False).mean()
def rsi(c,p=14):
    d=c.diff();g=d.clip(lower=0);l=-d.clip(upper=0)
    return 100-(100/(1+g.ewm(span=p,adjust=False).mean()/l.ewm(span=p,adjust=False).mean().replace(0,1e-9)))

def load():
    c={}
    for s in SYMBOLS:
        for tf in TFS:
            p=os.path.join(CACHE,f"{s.replace('-','_')}_{tf}_365d.parquet")
            if os.path.exists(p):
                df=pd.read_parquet(p).sort_values("ts").reset_index(drop=True)
                cut=df["ts"].max()-(365*24*3600*1000)
                df=df[df["ts"]>=cut].copy()
                if len(df)>=200: c[(s,tf)]=df
    return c

def fib_bounce_signals(df):
    """Vectorized — all filters computed once, O(n)."""
    c=df["close"];h=df["high"];l=df["low"];v=df["volume"]
    # Fib 0.618
    h100=h.rolling(100).max();l100=l.rolling(100).min();rng=h100-l100
    fib618=l100+0.618*rng
    near_fib=abs(c-fib618)/fib618.replace(0,1e-9)<0.012
    # Reversal 1-bar
    reversal=(c>c.shift(1))&(c.shift(1)<=c.shift(2))
    # Volume
    v_ok=(v/v.rolling(50).mean().replace(0,1e-9))>0.6
    # RSI
    r=rsi(c);r_ok=(r>25)&(r<55)
    # ADX regime — VECTORIZED
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=tr.ewm(span=14,adjust=False).mean()
    up=h.diff();down=l.shift()-l
    pdm=np.where((up>down)&(up>0),up,0);ndm=np.where((down>up)&(down>0),down,0)
    pdi=100*pd.Series(pdm).ewm(span=14,adjust=False).mean()/atr.replace(0,1e-9)
    ndi=100*pd.Series(ndm).ewm(span=14,adjust=False).mean()/atr.replace(0,1e-9)
    dx=100*abs(pdi-ndi)/(pdi+ndi+1e-9)
    adx=pd.Series(dx).ewm(span=14,adjust=False).mean()
    regime_ok=(adx>ADX_MIN)&(pdi>ndi)
    return near_fib&reversal&v_ok&r_ok&regime_ok

def sim(sigs,df,tf_min):
    c=df["close"];h=df["high"];l=df["low"]
    mb=max(int((96*60)/tf_min),24)
    trades=[];active=None
    for sig in sigs[:200]:
        if active: continue
        bi=sig["bar"]
        if bi>=len(c)-5: continue
        ep=c.iloc[bi];active={"ep":ep,"bi":bi,"hw":ep,"ta":False,"ts":None}
        for i in range(bi+1,len(df)):
            bh=i-bi;active["hw"]=max(active["hw"],h.iloc[i])
            prof=(active["hw"]-ep)/ep
            if not active["ta"] and prof>=TRAIL_ACT:
                active["ta"]=True;active["ts"]=active["hw"]*(1-TRAIL)
            if active["ta"]:
                ns=active["hw"]*(1-TRAIL);active["ts"]=max(active.get("ts",0),ns)
            xp=None;rs=None
            esl=max(ep*(1-SL),active.get("ts",ep*(1-SL))) if active["ta"] else ep*(1-SL)
            if l.iloc[i]<=esl: xp=esl;rs="TRAIL" if active["ta"] else "SL"
            if bh>=mb: xp=c.iloc[i];rs="TIME"
            if xp:
                pnl=(xp-ep)/ep
                trades.append({"pnl":pnl,"bars":bh,"trailed":active["ta"],"reason":rs})
                active=None;break
    return trades

def stats(tr):
    if not tr: return None
    bal=BAL;pk=bal;dd=0;w=l=0;tw=0
    for t in tr:
        m=bal*RISK;bal+=m*LEV*t["pnl"]
        if bal<=0: bal=0;break
        if t["pnl"]>0.0001: w+=1;tw+=t["trailed"]
        elif t["pnl"]<-0.0001: l+=1
        if bal>pk: pk=bal
        dd=max(dd,(pk-bal)/pk*100 if pk>0 else 0)
    tot=w+l
    return {"bal":round(bal,2),"ret":round((bal/BAL-1)*100,1),"tot":tot,"w":w,"l":l,"wr":round(w/tot*100,1) if tot else 0,"dd":round(dd,1),"tw":tw} if tot>=3 else None

print("="*60)
print("FIB_BOUNCE — ALL TIMEFRAMES")
print("fib=0.618 | ADX>22 | RSI 25-55 | SL=7% | Trail=5% | Risk=2%")
print("="*60)
data=load()
print(f"Loaded {len(data)} datasets\n")
for tf,m in TFS.items():
    stp={"5m":4,"15m":2,"30m":1,"1H":1,"4H":1}[tf]
    all_tr=[]
    for sym in SYMBOLS:
        df=data.get((sym,tf))
        if df is None: continue
        lo=fib_bounce_signals(df)
        sigs=[{"bar":i,"side":"long"} for i in range(100,len(df),stp) if lo.iloc[i]]
        all_tr.extend(sim(sigs,df,m))
    st=stats(all_tr)
    if st:
        ico="🔥" if st["ret"]>50 else ("✅" if st["ret"]>0 else "❌")
        print(f"  {tf:4s} {ico} ret={st['ret']:+8.1f}% WR={st['wr']:.0f}% tr={st['tot']:5d} DD={st['dd']:.0f}% trail={st['tw']}w")
    else:
        print(f"  {tf:4s}   no trades")
