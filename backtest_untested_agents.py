#!/usr/bin/env python3
"""Backtest just the 6 untested agents: B4h, B12h, B48h, B2h, asian_pump, fib_bounce"""
import os, sys, json, pandas as pd, numpy as np

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, WORK)

import importlib.util
spec = importlib.util.spec_from_file_location("bot", os.path.join(WORK, "bot.py"))
bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot)

SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","DOGE-USDT","BNB-USDT",
           "XRP-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT"]
TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
BAL=100; LEV=5; RISK=0.02
MAX_TRADES=200

def load_data():
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

def generate_signals(agent, df, sym, tf):
    signals = []
    class FCtx: pass
    step = {"5m":6,"15m":3,"30m":2,"1H":1,"4H":1}.get(tf,1)
    for i in range(100, len(df), step):
        window = df.iloc[i-100:i+1]
        ctx = FCtx()
        ctx.df_5m = window; ctx.df_15m = window; ctx.df_1h = window
        try:
            result = agent.analyze(sym, ctx)
            if result is not None:
                signals.append({"bar":i,"side":result.side,"time":df["ts"].iloc[i]})
        except: pass
    return signals[:MAX_TRADES]

def sim_trades(sigs, df, profile, tf_min):
    c=df["close"];h=df["high"];l=df["low"]
    sl=profile.get("sl",2.0)/100; trail=profile.get("trail",1.0)/100
    activate=profile.get("activate",1.0)/100
    max_hold=profile.get("max_hold_min",720)
    mb=max(int(max_hold/tf_min),12)
    tp=profile.get("tp",99)/100
    if tp>0.98: tp=None

    trades=[];active=None
    for sig in sigs:
        if active: continue
        bi=sig["bar"]
        if bi>=len(c)-5: continue
        ep=c.iloc[bi];sd=sig["side"]
        active={"sd":sd,"ep":ep,"bi":bi,"hw":ep,"lw":ep,"ta":False,"ts":None}
        for i in range(bi+1,len(df)):
            bh=i-bi
            if sd=="long": active["hw"]=max(active["hw"],h.iloc[i])
            else: active["lw"]=min(active["lw"],l.iloc[i])
            prof=(active["hw"]-ep)/ep if sd=="long" else (ep-active["lw"])/ep
            if not active["ta"] and prof>=activate:
                active["ta"]=True
                active["ts"]=active["hw"]*(1-trail) if sd=="long" else active["lw"]*(1+trail)
            if active["ta"]:
                if sd=="long": ns=active["hw"]*(1-trail);active["ts"]=max(active.get("ts",0),ns)
                else: ns=active["lw"]*(1+trail);active["ts"]=min(active.get("ts",float("inf")),ns)
            xp=None
            if sd=="long":
                esl=max(ep*(1-sl),active.get("ts",ep*(1-sl))) if active["ta"] else ep*(1-sl)
                if l.iloc[i]<=esl: xp=esl
                if tp and h.iloc[i]>=ep*(1+tp): xp=ep*(1+tp)
            else:
                esl=min(ep*(1+sl),active.get("ts",ep*(1+sl))) if active["ta"] else ep*(1+sl)
                if h.iloc[i]>=esl: xp=esl
                if tp and l.iloc[i]<=ep*(1-tp): xp=ep*(1-tp)
            if bh>=mb: xp=c.iloc[i]
            if xp:
                pnl=(xp-ep)/ep if sd=="long" else (ep-xp)/ep
                trades.append({"pnl":pnl,"bars":bh,"trailed":active["ta"]})
                active=None;break
    return trades

def stats(tr):
    if not tr: return None
    bal=BAL;pk=bal;dd=0;w=l=0
    for t in tr:
        m=bal*RISK;bal+=m*LEV*t["pnl"]
        if bal<=0: bal=0;break
        if t["pnl"]>0.0001: w+=1
        elif t["pnl"]<-0.0001: l+=1
        if bal>pk: pk=bal
        dd=max(dd,(pk-bal)/pk*100 if pk>0 else 0)
    tot=w+l
    if tot<5: return None
    return {"bal":round(bal,2),"ret":round((bal/BAL-1)*100,1),"tot":tot,"w":w,"l":l,
            "wr":round(w/tot*100,1),"dd":round(dd,1)}

# Target agents
targets = ["daily_breakout_4h", "daily_breakout_12h", "daily_breakout_48h",
           "daily_breakout_2h", "asian_pump", "fib_bounce"]

print("="*80)
print("UNTESTED AGENT BACKTEST")
print("="*80)

print(f"\nLoading data...", flush=True)
data = load_data()
print(f"Loaded {len(data)} datasets\n")

# Find the agents from the bot
# Walk SUBCLASSES recursively — some agents inherit from _DailyBreakoutBase not Agent directly
all_agents = []
seen = set()
skip = {"Agent","_DailyBreakoutBase","LearningAgent"}

def collect_agents(cls):
    """Recursively collect agent instances from a class hierarchy."""
    for subclass in cls.__subclasses__():
        if subclass.__name__ in skip:
            # Walk into the base to find its subclasses
            collect_agents(subclass)
            continue
        try:
            inst = subclass()
            if inst.name not in seen:
                seen.add(inst.name)
                all_agents.append(inst)
        except:
            pass

collect_agents(bot.Agent)

# Filter to targets
target_results = {}
for agent in all_agents:
    if agent.name not in targets:
        continue
    name = agent.name
    profile_key = agent.profile
    profile = bot.PROFILES.get(profile_key,
              bot.PROFILES.get("momentum",{"tp":3,"sl":1.2,"trail":1.0,"activate":0.8,"max_hold_min":360}))

    print(f"\n{'─'*60}")
    print(f"  {name} (profile={profile_key})")
    print(f"{'─'*60}")

    best_tf = None; best_ret = -999
    for tf, m in sorted(TFS.items()):
        all_tr = []
        for sym in SYMBOLS:
            df = data.get((sym,tf))
            if df is None: continue
            sigs = generate_signals(agent, df, sym, tf)
            all_tr.extend(sim_trades(sigs, df, profile, m))

        st = stats(all_tr)
        if st:
            ico = "🔥" if st["ret"] > 50 else ("✅" if st["ret"] > 0 else "❌")
            print(f"    {tf:4s}: {ico}  +{st['ret']:.1f}%  WR={st['wr']}%  Trades={st['tot']}  DD={st['dd']}%")
            if st["ret"] > best_ret:
                best_ret = st["ret"]
                best_tf = tf
        else:
            print(f"    {tf:4s}: ⚪ no trades")

    if best_tf:
        ico = "🔥" if best_ret > 50 else ("✅" if best_ret > 0 else "❌")
        print(f"  → BEST: {best_tf} {ico} +{best_ret:.1f}%")
        target_results[name] = {"best_tf": best_tf, "best_ret": best_ret}
    else:
        print(f"  → ❌ NO TRADES on any TF")
        target_results[name] = {"best_tf": "NONE", "best_ret": 0}

# Summary
print(f"\n{'='*80}")
print("SUMMARY: 6 UNTESTED AGENTS")
print(f"{'='*80}")
for name, res in sorted(target_results.items()):
    ico = "✅" if res["best_ret"] > 0 else ("❌" if res["best_tf"] != "NONE" else "⚪")
    print(f"  {ico} {name:25s} best={res['best_tf']:4s}  {res['best_ret']:+6.1f}%")

# Save
ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
json_p = os.path.join(OUT, f"untested_agents_{ts}.json")
with open(json_p,"w") as f:
    json.dump(target_results, f, indent=2)
print(f"\nSaved: {json_p}")
