#!/usr/bin/env python3
"""Backtest ONLY the 2 winners across ALL coins and ALL timeframes. Uses actual agent code."""
import os, sys, json, time, math
import numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
HL_CACHE = os.path.join(WORK, "market_data_cache")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, WORK)

# Load env
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

TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
BAL=100; LEV=10; RISK=0.10

class FakeCtx:
    pass

def load_all():
    c = {}
    for d in [CACHE, HL_CACHE]:
        for f in os.listdir(d):
            if not f.endswith(".parquet"): continue
            try:
                parts = f.replace(".parquet","").split("_")
                sym = f"{parts[0]}-{parts[1]}"
                tf = parts[2] if len(parts)>2 else "1H"
                if tf not in TFS: continue
                df = pd.read_parquet(os.path.join(d,f)).sort_values("ts").reset_index(drop=True)
                if "close" not in df.columns: continue
                if len(df) >= 100:
                    if (sym,tf) not in c: c[(sym,tf)] = df
            except: pass
    return c

def generate_signals(agent, df, sym, tf):
    sigs = []
    step = {"5m":6,"15m":3,"30m":2,"1H":1,"4H":1}[tf]
    for i in range(100, len(df), step):
        window = df.iloc[max(0,i-200):i+1]
        ctx = FakeCtx()
        ctx.df_5m = window; ctx.df_15m = window; ctx.df_1h = window
        try:
            result = agent.analyze(sym, ctx)
            if result is not None:
                sigs.append({"bar":i,"side":result.side,"time":df["ts"].iloc[i]})
        except: pass
    return sigs[:200]

def sim(sigs, df, tf_min, profile):
    c=df["close"];h=df["high"];l=df["low"]
    sl=profile.get("sl",5.0)/100; trail=profile.get("trail",6.0)/100
    activate=profile.get("activate",2.0)/100
    max_hold=profile.get("max_hold_min",5760)
    mb=max(int(max_hold/tf_min),24)
    trades=[];active=None
    for sig in sigs:
        if active: continue
        bi=sig["bar"]
        if bi>=len(c)-5: continue
        ep=c.iloc[bi];sd=sig["side"]
        active={"ep":ep,"hw":ep,"lw":ep,"ta":False,"ts":None,"side":sd}
        for i in range(bi+1,len(df)):
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
            else:
                esl=min(ep*(1+sl),active.get("ts",ep*(1+sl))) if active["ta"] else ep*(1+sl)
                if h.iloc[i]>=esl: xp=esl
            if i-bi>=mb: xp=c.iloc[i]
            if xp:
                pnl=(xp-ep)/ep if sd=="long" else (ep-xp)/ep
                trades.append({"pnl":pnl,"bars":i-bi,"trailed":active["ta"],"side":sd})
                active=None;break
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

print("="*70)
print("BACKTEST: 2 WINNERS × ALL COINS × ALL TIMEFRAMES")
print("="*70)

data = load_all()
n_coins = len(set(s for s,_ in data))
print(f"Data: {len(data)} datasets, ~{n_coins} coins\n")

# Get the actual agents
agents = {}
for cls in bot.Agent.__subclasses__():
    try:
        inst = cls()
        if inst.name in ("macd_cross", "fib_bounce"):
            agents[inst.name] = inst
            print(f"Loaded: {inst.name} (profile={inst.profile})")
    except: pass

all_results = []

for agent_name, agent in agents.items():
    profile = bot.PROFILES.get(agent.profile, {"sl":5,"trail":6,"activate":2,"max_hold_min":5760})
    print(f"\n{'─'*50}\n  {agent_name} | SL={profile['sl']}% Trail={profile['trail']}% Act={profile['activate']}%\n{'─'*50}")

    for tf, m in TFS.items():
        all_tr = []
        for (sym, dtf), df in data.items():
            if dtf != tf: continue
            sigs = generate_signals(agent, df, sym, tf)
            all_tr.extend(sim(sigs, df, m, profile))

        st = stats(all_tr)
        if st:
            st["agent"] = agent_name; st["tf"] = tf
            all_results.append(st)
            ico = "🔥" if st["ret"] > 100 else ("✅" if st["ret"] > 0 else "❌")
            print(f"  {tf:4s} {ico} ret={st['ret']:+10.1f}% WR={st['wr']:.0f}% tr={st['tot']:5d} DD={st['dd']:.0f}% trail={st['tw']}w")

# Rankings
all_results.sort(key=lambda x:-x["ret"])
print(f"\n{'='*70}")
print("🏆 FINAL RANKINGS")
print(f"{'='*70}")
for r in all_results:
    ico = "🔥" if r["ret"] > 100 else ("✅" if r["ret"] > 0 else "❌")
    print(f"  {ico} {r['agent']:<15s} {r['tf']:<5s} {r['ret']:+10.1f}% {r['wr']:.0f}% WR {r['tot']:5d}t {r['dd']:.0f}% DD")

# Save
ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
with open(os.path.join(OUT,f"backtest_2winners_{ts}.json"),"w") as f:
    json.dump(all_results, f, indent=2)
print(f"\n✅ Saved: backtest_2winners_{ts}.json")
