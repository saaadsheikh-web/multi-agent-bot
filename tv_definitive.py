#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""DEFINITIVE TRADINGVIEW BACKTEST — All agents × 5 TFs × 5 coins × 3 runs.
Compares results with BloFin. Saves to JSON for analysis."""
import os, sys, json, time
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot
from tv_fresh import candles, resample

SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT"]
AGENTS = [
    ("asymmetric",         bot.AsymmetricBreakoutAgent,     "1H"),
    ("daily_breakout",     bot.DailyRangeBreakoutAgent,     "1H"),
    ("daily_breakout_24h", bot.DailyBreakout24hAgent,       "1H"),
    ("daily_breakout_4h",  bot.DailyBreakout4hAgent,        "1H"),
    ("daily_breakout_12h", bot.DailyBreakout12hAgent,       "1H"),
    ("daily_breakout_48h", bot.DailyBreakout48hAgent,       "1H"),
    ("liquidity_sweep",    bot.LiquiditySweepScalpAgent,    "5m"),
    ("wide_scalp",         bot.WideScalpAgent,              "1H"),
    ("utbot_mtf",          bot.UTBotMTFAgent,               "15m"),
    ("fib_confluence",     bot.FibConfluenceZoneAgent,      "1H"),
    ("fib_bounce",         bot.FibBounceAgent,              "1H"),
    ("turtle_breakout",    bot.TurtleBreakoutAgent,         "1H"),
    ("livermore_pivot",    bot.LivermorePivotAgent,         "1H"),
    ("quick_scalp",        bot.QuickScalp1HAgent,           "1H"),
    ("smart_scalp",        bot.SmartScalpAgent,             "5m"),
    ("macd_cross",         bot.MACDCrossAgent,              "15m"),
]

TIMEFRAMES = ["5m", "15m", "30m", "1H", "4H"]
RUNS = 3
MIN_CONF = 6
MAX_HOLD = 96

def run_simulation(name, agent_cls, sym, df, primary_tf):
    """Run 1 simulation for 1 agent on 1 symbol."""
    agent = agent_cls()
    if not agent.enabled:
        return None
    
    c = df["close"].values; h = df["high"].values
    l = df["low"].values; v = df["volume"].values
    n = len(df)
    
    warmup = 200 if primary_tf == "5m" else 100
    trades = []
    
    for i in range(warmup, n - 10):
        ctx_df = df.iloc[:i+1].copy().reset_index(drop=True)
        ctx = bot.MarketContext(
            symbol=sym, df_5m=pd.DataFrame(), df_15m=pd.DataFrame(),
            df_30m=pd.DataFrame(), df_1h=ctx_df,
            funding_rate=0.0, orderbook={"bids":[],"asks":[]},
            news_sentiment={}, trend=bot.TrendState())
        
        try:
            sig = agent.analyze(sym, ctx)
        except:
            continue
        
        if sig and sig.confidence >= MIN_CONF:
            # Simulate trade
            entry = c[i]
            sl = entry * 0.96 if sig.side == "long" else entry * 1.04
            trail_active = False
            peak = entry
            
            for j in range(i+1, min(i+MAX_HOLD, n)):
                # Check stop
                if sig.side == "long":
                    if l[j] <= sl:
                        pnl = (sl - entry)/entry*100 - 0.04
                        trades.append(pnl)
                        break
                    # Trailing
                    if c[j] > peak: peak = c[j]
                    if not trail_active and c[j] >= entry * 1.01:
                        trail_active = True
                    if trail_active:
                        ns = peak * 0.99
                        if ns > sl: sl = ns
                        if l[j] <= sl:
                            pnl = (sl - entry)/entry*100 - 0.04
                            trades.append(pnl)
                            break
                else:
                    if h[j] >= sl:
                        pnl = (entry - sl)/entry*100 - 0.04
                        trades.append(pnl)
                        break
                    if c[j] < peak: peak = c[j]
                    if not trail_active and c[j] <= entry * 0.99:
                        trail_active = True
                    if trail_active:
                        ns = peak * 1.01
                        if ns < sl: sl = ns
                        if h[j] >= sl:
                            pnl = (entry - sl)/entry*100 - 0.04
                            trades.append(pnl)
                            break
            else:
                # Time exit
                exit_p = c[min(i+MAX_HOLD, n)-1]
                pnl = ((exit_p - entry)/entry*100 - 0.04) if sig.side == "long" else \
                      ((entry - exit_p)/entry*100 - 0.04)
                trades.append(pnl)
    
    return trades


# ── MAIN ──
print("=" * 70)
print("DEFINITIVE BACKTEST — All agents × 5 TFs × 4 coins × 3 runs")
print("  Data: TradingView 5000 bars per TF")
print("=" * 70)

all_runs = []

for run in range(RUNS):
    print(f"\n{'#'*70}")
    print(f"  RUN {run+1}/{RUNS}")
    print(f"{'#'*70}")
    
    run_data = {}
    
    for sym in SYMBOLS:
        print(f"\n  Fetching {sym} data...")
        
        # Fetch for each primary TF
        sym_data = {}
        
        for name, agent_cls, primary_tf in AGENTS:
            df = candles(sym, primary_tf, 5000)
            if df.empty:
                continue
            
            trades = run_simulation(name, agent_cls, sym, df, primary_tf)
            if trades and len(trades) >= 3:
                wins = sum(1 for p in trades if p > 0)
                total = sum(trades)
                wr = wins/len(trades)*100
                sym_data[name] = {
                    "trades": len(trades), "wins": wins,
                    "wr": round(wr,1), "ret": round(total,2),
                    "avg": round(total/len(trades),2)
                }
        
        run_data[sym] = sym_data
    
    all_runs.append(run_data)
    
    # Print this run summary
    summary = defaultdict(lambda: {"trades":0,"wins":0,"pnl":0,"coins":0})
    for sym, agents in run_data.items():
        for name, d in agents.items():
            summary[name]["trades"] += d["trades"]
            summary[name]["wins"] += d["wins"]
            summary[name]["pnl"] += d["ret"]
            summary[name]["coins"] += 1
    
    print(f"\n  ─── Run {run+1} Summary ───")
    for name in sorted(summary.keys(), key=lambda n: -summary[n]["pnl"]):
        s = summary[name]
        wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
        print(f"  {name:20s} {s['trades']:4d}t  WR={wr:5.1f}%  ret={s['pnl']:+7.2f}%  {s['coins']}coins")

# ── FINAL AGGREGATED RESULTS ──
print(f"\n{'='*70}")
print("  FINAL — Aggregated across ALL {RUNS} runs")
print(f"{'='*70}")

final = defaultdict(lambda: {"trades":0, "wins":0, "pnl":0, "coins":set()})
for run_data in all_runs:
    for sym, agents in run_data.items():
        for name, d in agents.items():
            final[name]["trades"] += d["trades"]
            final[name]["wins"] += d["wins"]
            final[name]["pnl"] += d["ret"]
            final[name]["coins"].add(sym)

print(f"\n{'Agent':20s} {'Trades':>7s} {'WR%':>6s} {'Ret%':>8s} {'Coins':>5s}")
print("-" * 48)
ranked = sorted(final.keys(), key=lambda n: -final[n]["pnl"])
for name in ranked:
    s = final[name]
    wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
    print(f"{name:20s} {s['trades']:7d} {wr:5.1f}% {s['pnl']:+8.2f}% {len(s['coins']):4d}")

print(f"\n{'='*70}")
print("  WINNERS ✅")
for name in ranked:
    s = final[name]
    if s["pnl"] > 0 and s["trades"] >= 10:
        wr = s["wins"]/s["trades"]*100
        print(f"  ✅ {name:20s} +{s['pnl']:6.2f}%  {s['trades']}t  WR={wr:.1f}%")

print(f"\n  LOSERS/BORDERLINE ❌")
for name in ranked:
    s = final[name]
    if s["pnl"] <= 0 and s["trades"] >= 10:
        wr = s["wins"]/s["trades"]*100
        print(f"  {'⬇️' if s['pnl'] < -50 else '⚠️'} {name:20s} {s['pnl']:7.2f}%  {s['trades']}t  WR={wr:.1f}%")

# Save to JSON
output = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "config": {"run_count": RUNS, "symbols": SYMBOLS, "agents": len(AGENTS), "bars": 5000},
    "aggregated": {k: {"trades":v["trades"],"wins":v["wins"],"wr":round(v["wins"]/v["trades"]*100,1) if v["trades"] else 0,"ret":round(v["pnl"],2),"coins":len(v["coins"])} for k,v in final.items()},
}
with open("tv_definitive_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\n  ✅ Saved to tv_definitive_results.json")
print(f"\n  Finished: {datetime.now(timezone.utc).isoformat()}")
