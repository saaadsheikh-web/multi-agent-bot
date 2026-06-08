#!/usr/bin/env python3
"""Backtest EVERY live agent across ALL timeframes to find optimal TF per agent."""
import os, sys, json, time, inspect
import numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, WORK)

# Load .env
env = os.path.join(WORK, ".env")
if os.path.exists(env):
    with open(env) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

import importlib.util
spec = importlib.util.spec_from_file_location("bot", os.path.join(WORK, "bot.py"))
bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot)

# ══════════════════════════════════════════
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

def get_live_agents():
    """Get all agents that are currently enabled in the bot."""
    agents = []
    seen = set()
    skip = {"Agent","_DailyBreakoutBase","LearningAgent"}
    for cls in bot.Agent.__subclasses__():
        if cls.__name__ in skip: continue
        try:
            inst = cls()
            if inst.name in seen: continue
            seen.add(inst.name)
            if inst.enabled:
                agents.append(inst)
        except: pass
    # Also get paper agents
    try:
        from paper_agents import get_paper_agents
        for a in get_paper_agents():
            if a.name not in seen and a.enabled:
                seen.add(a.name)
                agents.append(a)
    except: pass
    return agents

def generate_signals(agent, df, sym, tf):
    """Feed data to agent across all df slots."""
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

# ══════════════════════════════════════════
print("="*80)
print("LIVE AGENT TF OPTIMIZATION — Testing each agent at every TF")
print("="*80)

data = load_data()
print(f"Loaded {len(data)} datasets")

agents = get_live_agents()
print(f"Live agents: {len(agents)}\n")

all_results = []

for idx, agent in enumerate(agents):
    name = agent.name
    profile_key = agent.profile
    profile = bot.PROFILES.get(profile_key,
              bot.PROFILES.get("momentum",{"tp":3,"sl":1.2,"trail":1.0,"activate":0.8,"max_hold_min":360}))

    print(f"[{idx+1}/{len(agents)}] {name:28s} profile={profile_key}", end=" ", flush=True)

    best_tf = None; best_ret = -999

    for tf, m in TFS.items():
        all_tr = []
        for sym in SYMBOLS:
            df = data.get((sym,tf))
            if df is None: continue
            sigs = generate_signals(agent, df, sym, tf)
            all_tr.extend(sim_trades(sigs, df, profile, m))

        st = stats(all_tr)
        if st:
            all_results.append({**st, "agent":name, "tf":tf, "profile":profile_key})
            if st["ret"] > best_ret:
                best_ret = st["ret"]
                best_tf = tf

    if best_tf:
        ico = "🔥" if best_ret > 50 else ("✅" if best_ret > 0 else "❌")
        print(f"→ best={best_tf} {ico} {best_ret:+.0f}%")
    else:
        print("→ no trades")

# ══════════════════════════════════════════
# RANKINGS — Best TF per agent
print(f"\n{'='*80}")
print("BEST TIMEFRAME PER AGENT")
print(f"{'='*80}")
print(f"{'Agent':<30s} {'Best TF':<8s} {'Return':<10s} {'WR':<8s} {'Trades':<8s} {'DD':<8s} {'Profile':<20s}")
print(f"{'─'*30} {'─'*8} {'─'*10} {'─'*8} {'─'*8} {'─'*8} {'─'*20}")

# Group by agent, pick best TF
agent_best = {}
for r in all_results:
    n = r["agent"]
    if n not in agent_best or r["ret"] > agent_best[n]["ret"]:
        agent_best[n] = r

for name, r in sorted(agent_best.items(), key=lambda x: -x[1]["ret"]):
    ico = "🔥" if r["ret"] > 50 else ("✅" if r["ret"] > 0 else "❌")
    print(f"{ico} {name:<27s} {r['tf']:<8s} {r['ret']:+9.1f}% {r['wr']:5.1f}%  {r['tot']:5d}   {r['dd']:5.1f}%  {r['profile']:<20s}")

# Summary
profitable = [r for r in agent_best.values() if r["ret"] > 0]
print(f"\n{len(profitable)}/{len(agent_best)} agents profitable at their best TF")
print(f"Avg best return: {np.mean([r['ret'] for r in agent_best.values()]):+.0f}%")
print(f"Avg best WR: {np.mean([r['wr'] for r in agent_best.values()]):.0f}%")

# TF distribution
from collections import Counter
tf_dist = Counter(r["tf"] for r in agent_best.values())
print(f"Best TF distribution: {dict(tf_dist)}")

# Save
ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
json_p = os.path.join(OUT, f"live_agent_tf_optimization_{ts}.json")
with open(json_p,"w") as f:
    json.dump({"agent_best": {n:r for n,r in agent_best.items()}, "all": all_results}, f, indent=2, default=str)
print(f"\nSaved: {json_p}")
