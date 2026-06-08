#!/usr/bin/env python3
"""Comprehensive backtest — all agents × timeframes × coins × 1 year with hourly analysis."""

import os, sys, json, time as _time, math
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")
ENV_PATH = os.path.join(WORK_DIR, ".env")
sys.path.insert(0, WORK_DIR)

if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

import importlib.util
spec = importlib.util.spec_from_file_location("bt", os.path.join(WORK_DIR, "backtest.py"))
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)

# ── Config ─────────────────────────────────────────────────────────────────
TIMEFRAMES = ["10m", "15m", "30m", "1h"]
DAYS = 365
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT","BNB-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT",
           "LTC-USDT","ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT",
           "INJ-USDT","TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT"]

def load_data(symbol, tf, days=DAYS):
    """Load candle data for a symbol+timeframe combo."""
    fname = f"{symbol.replace('-','_')}_{tf}_{days}d.parquet"
    path = os.path.join(CACHE_DIR, fname)
    if os.path.exists(path):
        return pd.read_parquet(path)
    return None

def get_interval_minutes(tf):
    return {"10m":10,"15m":15,"30m":30,"1h":60}.get(tf, 15)

def main():
    print("=" * 100)
    print(f"FULL RESEARCH BACKTEST — {len(SYMBOLS)} coins × {len(TIMEFRAMES)} TFs × 1 year")
    print("=" * 100)

    all_results = []

    for tf in TIMEFRAMES:
        bar_min = get_interval_minutes(tf)
        print(f"\n{'─'*100}")
        print(f"  TIMEFRAME: {tf} ({bar_min}min bars)")
        print(f"{'─'*100}")

        for sym in SYMBOLS:
            df = load_data(sym, tf)
            if df is None or len(df) < 100:
                print(f"  {sym:15s} → NO DATA")
                continue

            df = df.sort_values("ts").reset_index(drop=True)
            cutoff = df["ts"].max() - (DAYS * 24 * 3600 * 1000)
            df = df[df["ts"] >= cutoff].copy()

            if len(df) < 200:
                continue

            # Use the backtest engine for this symbol
            try:
                p = bt.PrecomputedData(df, df, df)  # simplified single-TF
            except Exception:
                continue

            trades = bt.simulate(p, symbol=sym, use_regime_filter=True)
            if not trades:
                continue

            # ── Per-symbol metrics ──
            agent_stats = defaultdict(lambda: {"wins":0,"losses":0,"pnl_r":0,"trades":0,"hours":defaultdict(int),"hour_pnl":defaultdict(float)})

            for t in trades:
                a = t["agent"]
                r = t["r_multiple"]
                agent_stats[a]["trades"] += 1
                agent_stats[a]["pnl_r"] += r
                if r > 0: agent_stats[a]["wins"] += 1
                elif r < 0: agent_stats[a]["losses"] += 1

                # Hour analysis
                try:
                    ts = t.get("open_ts", 0)
                    hour = datetime.fromtimestamp(ts/1000, tz=timezone.utc).hour
                except:
                    hour = -1
                agent_stats[a]["hours"][hour] += 1
                agent_stats[a]["hour_pnl"][hour] += r

            for agent, stats in agent_stats.items():
                t_count = stats["trades"]
                wr = stats["wins"] / t_count * 100 if t_count else 0
                avg_r = stats["pnl_r"] / t_count if t_count else 0

                # Best hour
                best_hour = max(stats["hours"], key=stats["hours"].get) if stats["hours"] else -1
                best_hour_pnl = max(stats["hour_pnl"], key=lambda h: stats["hour_pnl"][h]) if stats["hour_pnl"] else -1

                all_results.append({
                    "tf": tf,
                    "symbol": sym,
                    "agent": agent,
                    "trades": t_count,
                    "wr": wr,
                    "avg_r": avg_r,
                    "total_r": stats["pnl_r"],
                    "best_hour": best_hour,
                    "best_hour_pnl": best_hour_pnl,
                })

        # Progress
        n_agents = len(set(r["agent"] for r in all_results if r["tf"]==tf))
        n_syms = len(set(r["symbol"] for r in all_results if r["tf"]==tf))
        print(f"  → {n_agents} agents × {n_syms} symbols processed")

    # ── AGGREGATE RESULTS ──────────────────────────────────────────────────
    print(f"\n{'='*100}")
    print("RESULTS BY AGENT × TIMEFRAME")
    print(f"{'='*100}")

    by_agent_tf = defaultdict(lambda: {"trades":0,"wins":0,"losses":0,"total_r":0,"best_coin":"","best_coin_r":-999})
    for r in all_results:
        key = (r["agent"], r["tf"])
        by_agent_tf[key]["trades"] += r["trades"]
        by_agent_tf[key]["wins"] += int(r["wr"]/100 * r["trades"])
        by_agent_tf[key]["losses"] += r["trades"] - int(r["wr"]/100 * r["trades"])
        by_agent_tf[key]["total_r"] += r["total_r"]
        if r["avg_r"] > by_agent_tf[key]["best_coin_r"]:
            by_agent_tf[key]["best_coin"] = r["symbol"]
            by_agent_tf[key]["best_coin_r"] = r["avg_r"]

    print(f"\n{'Agent':25s} {'TF':6s} {'Trades':7s} {'WR':6s} {'AvgR':8s} {'TotalR':8s} {'BestCoin':12s} {'BestR':7s}")
    print("-"*95)

    ranked = []
    for (agent, tf), s in by_agent_tf.items():
        t = s["trades"]
        wr = s["wins"]/t*100 if t else 0
        avg_r = s["total_r"]/t if t else 0
        ranked.append((agent, tf, t, wr, avg_r, s["total_r"], s["best_coin"], s["best_coin_r"]))

    ranked.sort(key=lambda x: x[4], reverse=True)

    for agent, tf, t, wr, avg_r, total_r, best_coin, best_r in ranked:
        st = "🟢" if avg_r > 0.1 else ("🟡" if avg_r > 0 else "🔴")
        print(f"{st} {agent:23s} {tf:6s} {t:7d} {wr:5.1f}% {avg_r:+7.3f} {total_r:+7.1f} {best_coin:12s} {best_r:+6.3f}")

    # ── BEST HOUR BY AGENT ─────────────────────────────────────────────────
    print(f"\n{'='*100}")
    print("BEST TRADING HOURS (UTC) BY AGENT")
    print(f"{'='*100}")

    hour_r = defaultdict(lambda: defaultdict(float))
    hour_t = defaultdict(lambda: defaultdict(int))
    for r in all_results:
        if r["best_hour"] >= 0:
            hour_r[r["agent"]][r["best_hour"]] += r["best_hour_pnl"]
            hour_t[r["agent"]][r["best_hour"]] += 1

    for agent in sorted(hour_r.keys()):
        best_hr = max(hour_r[agent], key=lambda h: hour_r[agent][h]) if hour_r[agent] else -1
        print(f"  {agent:25s}: best hour {best_hr:02d}:00 UTC ({hour_t[agent][best_hr]} trades, R={hour_r[agent][best_hr]:+.2f})")

    # ── SAVE ───────────────────────────────────────────────────────────────
    out = {
        "run_ts": datetime.now(timezone.utc).isoformat(),
        "config": {"days": DAYS, "timeframes": TIMEFRAMES, "symbols": len(SYMBOLS)},
        "results": all_results,
        "ranking": [{"agent":a,"tf":tf,"trades":t,"wr":wr,"avg_r":avg_r} for a,tf,t,wr,avg_r,_,_,_ in ranked],
    }
    out_path = os.path.join(WORK_DIR, "FULL_RESEARCH_RESULTS.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved → {out_path}")

if __name__ == "__main__":
    main()
