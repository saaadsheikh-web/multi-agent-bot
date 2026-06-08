#!/usr/bin/env python3
"""Comprehensive backtest — all agents × 4 timeframes × 20 coins × 1 year. Resamples from 5m."""
import os, sys, json, time, math
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

WORK = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
sys.path.insert(0, WORK)
ENV = os.path.join(WORK, ".env")
if os.path.exists(ENV):
    with open(ENV) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k,v = line.split("=",1)
                os.environ.setdefault(k.strip(), v.strip())

print("Loading backtest engine...")
import importlib.util
spec = importlib.util.spec_from_file_location("bt", os.path.join(WORK, "backtest.py"))
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
print("Loaded.")

SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT","BNB-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT",
           "LTC-USDT","ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT",
           "INJ-USDT","TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT"]
DAYS = 365
TIMEFRAMES = {"10m": 10, "15m": 15, "30m": 30, "1h": 60}

def resample_5m_to(df5, target_minutes):
    """Resample 5m ohlcv to target timeframe."""
    rules = {
        "ts": "first",
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }
    df5 = df5.set_index(pd.to_datetime(df5["ts"], unit="ms"))
    tf_str = f"{target_minutes}min"
    resampled = df5.resample(tf_str).agg(rules).dropna()
    resampled["ts"] = resampled["ts"].astype(np.int64)
    return resampled.reset_index(drop=True)

def analyze_results(trades, tf, sym):
    """Extract per-agent stats from trade list."""
    stats = {}
    for t in trades:
        a = t["agent"]
        if a not in stats:
            stats[a] = {"trades":0,"wins":0,"losses":0,"r_sum":0,"r_list":[],"hours":defaultdict(list)}
        stats[a]["trades"] += 1
        stats[a]["r_sum"] += t["r_multiple"]
        stats[a]["r_list"].append(t["r_multiple"])
        if t["r_multiple"] > 0: stats[a]["wins"] += 1
        elif t["r_multiple"] < 0: stats[a]["losses"] += 1
        try:
            hr = datetime.fromtimestamp(t.get("open_ts",0)/1000, tz=timezone.utc).hour
            stats[a]["hours"][hr].append(t["r_multiple"])
        except: pass
    return stats

def main():
    print("=" * 100)
    print(f"FULL BACKTEST — {len(SYMBOLS)} coins × {len(TIMEFRAMES)} TFs × 365 days × all agents")
    print("=" * 100)

    master = {}  # (agent, tf) → aggregated stats
    all_raw = []

    for tf_name, tf_min in TIMEFRAMES.items():
        print(f"\n{'─'*100}")
        print(f"  {tf_name} ({tf_min}min)")
        print(f"{'─'*100}")

        for si, sym in enumerate(SYMBOLS):
            # Load base data
            if tf_name == "15m":
                fpath = os.path.join(CACHE, f"{sym.replace('-','_')}_15m_365d.parquet")
                df = pd.read_parquet(fpath) if os.path.exists(fpath) else None
            elif tf_name == "1h":
                fpath = os.path.join(CACHE, f"{sym.replace('-','_')}_1H_365d.parquet")
                df = pd.read_parquet(fpath) if os.path.exists(fpath) else None
            else:
                # Resample from 5m
                fpath5 = os.path.join(CACHE, f"{sym.replace('-','_')}_5m_365d.parquet")
                if not os.path.exists(fpath5): continue
                df5 = pd.read_parquet(fpath5).sort_values("ts")
                cutoff = df5["ts"].max() - DAYS * 24 * 3600 * 1000
                df5 = df5[df5["ts"] >= cutoff]
                if len(df5) < 500: continue
                df = resample_5m_to(df5, tf_min)

            if df is None or len(df) < 100: continue
            df = df.sort_values("ts").reset_index(drop=True).dropna(subset=["close"])
            if len(df) < 100: continue

            try:
                # Uses simplified single-TF PrecomputedData
                p = bt.PrecomputedData(df, df, df)
                trades = bt.simulate(p, symbol=sym, use_regime_filter=True)
            except Exception as e:
                continue

            if not trades: continue

            stats = analyze_results(trades, tf_name, sym)
            n_agents = len(stats)
            n_trades = sum(s["trades"] for s in stats.values())

            for agent, s in stats.items():
                key = (agent, tf_name)
                if key not in master:
                    master[key] = {"trades":0,"wins":0,"losses":0,"r_total":0,"r_list":[],
                                   "best_sym":"","best_sym_r":-999,"hours":defaultdict(lambda: {"r":0,"n":0})}
                m = master[key]
                m["trades"] += s["trades"]
                m["wins"] += s["wins"]
                m["losses"] += s["losses"]
                m["r_total"] += s["r_sum"]
                m["r_list"].extend(s["r_list"])
                avg_r = s["r_sum"]/s["trades"] if s["trades"] else 0
                if avg_r > m["best_sym_r"]:
                    m["best_sym"] = sym
                    m["best_sym_r"] = avg_r
                for hr, rs in s["hours"].items():
                    m["hours"][hr]["r"] += sum(rs)
                    m["hours"][hr]["n"] += len(rs)

                all_raw.append({"agent":agent,"tf":tf_name,"symbol":sym,"trades":s["trades"],
                               "wr":s["wins"]/s["trades"]*100 if s["trades"] else 0,
                               "avg_r":avg_r})

            pct = (si+1)/len(SYMBOLS)*100
            print(f"  [{pct:3.0f}%] {sym:15s} → {n_agents:2d} agents, {n_trades:5d} trades")

    # ── RANKING ────────────────────────────────────────────────────────────
    print(f"\n{'='*100}")
    print("RANKING — By Avg R (all symbols combined)")
    print(f"{'='*100}")

    ranked = []
    for (agent, tf), m in master.items():
        t = m["trades"]
        wr = m["wins"]/t*100 if t else 0
        avg_r = m["r_total"]/t if t else 0
        best_hr = max(m["hours"], key=lambda h: m["hours"][h]["r"]) if m["hours"] else -1
        ranked.append((agent, tf, t, wr, avg_r, m["r_total"], m["best_sym"], m["best_sym_r"], best_hr))

    ranked.sort(key=lambda x: x[4], reverse=True)

    print(f"\n{'#':3s} {'Agent':22s} {'TF':5s} {'Trades':7s} {'WR':6s} {'AvgR':8s} {'TotalR':8s} {'BestSym':12s} {'BestHr':7s}")
    print("-"*100)
    for i, (agent, tf, t, wr, avg_r, total_r, best_sym, best_sr, best_hr) in enumerate(ranked):
        st = "🟢" if avg_r > 0.1 else ("🟡" if avg_r > 0 else "🔴")
        print(f"{st} {i+1:2d} {agent:22s} {tf:5s} {t:7d} {wr:5.1f}% {avg_r:+7.3f} {total_r:+7.1f} {best_sym:12s} {best_hr:02d}:00")

    # ── BEST AGENT PER TIMEFRAME ──────────────────────────────────────────
    print(f"\n{'='*100}")
    print("BEST AGENT PER TIMEFRAME")
    for tf in TIMEFRAMES:
        tf_agents = [(a,t,w,ar,tr,bs) for a,tf2,t,w,ar,tr,bs,_,_ in ranked if tf2==tf]
        if tf_agents:
            best = tf_agents[0]
            print(f"  {tf}: {best[0]} — {best[3]:.0f} trades, {best[2]:.0f}% WR, {best[3]:+.3f} AvgR — best on {best[5]}")

    # ── SAVE ────────────────────────────────────────────────────────────────
    out_path = os.path.join(WORK, "FULL_BACKTEST_RESULTS.json")
    with open(out_path, "w") as f:
        json.dump({
            "ts": datetime.now(timezone.utc).isoformat(),
            "config": {"days": DAYS, "timeframes": list(TIMEFRAMES.keys()), "symbols": len(SYMBOLS)},
            "ranking": [{"rank":i+1,"agent":a,"tf":tf,"trades":t,"wr":round(wr,1),"avg_r":round(ar,4),
                         "total_r":round(tr,2),"best_symbol":bs,"best_hour":bh}
                        for i,(a,tf,t,wr,ar,tr,bs,_,bh) in enumerate(ranked)],
        }, f, indent=2, default=str)
    print(f"\nSaved → {out_path}")

if __name__ == "__main__":
    main()
