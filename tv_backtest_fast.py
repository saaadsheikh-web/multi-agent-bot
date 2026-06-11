#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
TRADINGVIEW BACKTEST v3 — FAST version.
Tests ALL 14 agents on 1H data directly (not bar-by-bar 5m walking).
Uses TradingView data — 5000 1H bars per symbol.
"""
import os, sys, json, math, time
from datetime import datetime, timezone
from collections import defaultdict
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot
from tv_data import candles

# ── CONFIG ──
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "HYPE-USDT"]

AGENT_SPECS = [
    ("asymmetric",         bot.AsymmetricBreakoutAgent),
    ("daily_breakout",     bot.DailyRangeBreakoutAgent),
    ("daily_breakout_24h", bot.DailyBreakout24hAgent),
    ("daily_breakout_4h",  bot.DailyBreakout4hAgent),
    ("daily_breakout_12h", bot.DailyBreakout12hAgent),
    ("daily_breakout_48h", bot.DailyBreakout48hAgent),
    ("liquidity_sweep",    bot.LiquiditySweepScalpAgent),
    ("wide_scalp",         bot.WideScalpAgent),
    ("utbot_mtf",          bot.UTBotMTFAgent),
    ("fib_confluence",     bot.FibConfluenceZoneAgent),
    ("fib_bounce",         bot.FibBounceAgent),
    ("turtle_breakout",    bot.TurtleBreakoutAgent),
    ("livermore_pivot",    bot.LivermorePivotAgent),
    ("quick_scalp",        bot.QuickScalp1HAgent),
]

TIMEFRAMES = ["1H", "2H", "4H", "8H", "12H", "24H"]
MIN_CONFIDENCE = 6
MAX_HOLD = 30  # Max 1H bars to hold

def resample(df, chunks):
    df = df.copy()
    df["_g"] = np.arange(len(df)) // chunks
    return df.groupby("_g").agg({"ts":"first","open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna().reset_index(drop=True)

def run_tf_agent(name, agent_cls, sym, df):
    """Test agent on one symbol at primary TF."""
    agent = agent_cls()
    if not agent.enabled:
        return None
    
    # Determine primary TF
    primary = "1H"
    if name in ("liquidity_sweep",): primary = "5m"
    elif name in ("utbot_mtf",): primary = "15m"
    
    if primary != "1H":
        return None  # Skip non-1H for now
    
    c = df["close"].values
    h = df["high"].values
    l = df["low"].values
    v = df["volume"].values
    n = len(df)
    
    trades = []
    # Walk through 1H bars
    for i in range(100, n - 5):
        ctx_df = df.iloc[:i+1].copy().reset_index(drop=True)
        
        # Build minimal MarketContext (only what analyze() uses)
        ctx = bot.MarketContext(
            symbol=sym,
            df_5m=pd.DataFrame(),  # Not used by 1H agents
            df_15m=pd.DataFrame(),
            df_30m=pd.DataFrame(),
            df_1h=ctx_df,
            funding_rate=0.0,
            orderbook={"bids":[],"asks":[]},
            news_sentiment={},
            trend=bot.TrendState()
        )
        
        try:
            sig = agent.analyze(sym, ctx)
        except Exception:
            continue
        
        if sig and sig.confidence >= MIN_CONFIDENCE:
            entry = c[i]
            sl = entry * 0.98 if sig.side == "long" else entry * 1.02
            
            # Simulate forward
            for j in range(i+1, min(i+MAX_HOLD, n)):
                if sig.side == "long" and l[j] <= sl:
                    trades.append((entry, sl, "stop", -2.04))
                    break
                elif sig.side == "short" and h[j] >= sl:
                    trades.append((entry, sl, "stop", -2.04))
                    break
                elif j == min(i+MAX_HOLD, n) - 1 or j == i+MAX_HOLD-1:
                    exit_p = c[j]
                    pnl = ((exit_p - entry) / entry * 100 - 0.04) if sig.side == "long" else \
                          ((entry - exit_p) / entry * 100 - 0.04)
                    trades.append((entry, exit_p, "close", pnl))
                    break
    
    if not trades:
        return None
    
    pnls = [t[3] for t in trades]
    wins = sum(1 for p in pnls if p > 0)
    tot = sum(pnls)
    
    return {"n": len(trades), "w": wins, "wr": round(wins/len(trades)*100, 1),
            "ret": round(tot, 2)}


# ── MAIN ──
print("=" * 70)
print("TRADINGVIEW BACKTEST v3 — FAST 1H mode (5000 bars)")
print(f"  Agents: {len(AGENT_SPECS)}, Symbols: {len(SYMBOLS)}")
print(f"  Data per symbol: 5000 1H bars from TradingView")
print("=" * 70)

all_data = []
for sym in SYMBOLS:
    print(f"\n{'─'*60}")
    print(f"  {sym}")
    print(f"{'─'*60}")
    
    df = candles(sym, "1H", 5000)
    if df.empty:
        print(f"  ✗ No data")
        continue
    
    print(f"  {len(df)} bars: {df.iloc[0]['ts']} → {df.iloc[-1]['ts']}")
    
    # Resample to other TFs
    tfs = {"1H": df}
    for tf, chunks in [("2H", 2), ("4H", 4), ("8H", 8), ("12H", 12), ("24H", 24)]:
        rd = resample(df, chunks)
        if len(rd) > 50:
            tfs[tf] = rd
    
    for name, agent_cls in AGENT_SPECS:
        result = run_tf_agent(name, agent_cls, sym, df)
        if result:
            all_data.append((sym, name, "1H", result))
            print(f"  {name:20s} [1H] {result['n']:4d}t  WR={result['wr']:5.1f}%  ret={result['ret']:+7.2f}%")

print(f"\n{'='*70}")
print("SUMMARY — All agents, all symbols, 5000 bars TV data")
print(f"{'='*70}")

summary = defaultdict(lambda: {"trades":0, "wins":0, "pnl":0, "coins":set(), "syms":[]})
for sym, name, tf, r in all_data:
    k = f"{name}_{tf}"
    summary[k]["trades"] += r["n"]
    summary[k]["wins"] += r["w"]
    summary[k]["pnl"] += r["ret"]
    summary[k]["coins"].add(sym)
    summary[k]["syms"].append(sym)

# Sort by pnl descending
ranked = sorted(summary.items(), key=lambda x: -x[1]["pnl"])
print(f"\n{'Agent':25s} {'Trades':>8s} {'WR%':>6s} {'Ret%':>8s} {'Coins':>6s}")
print("-" * 55)
for name, s in ranked:
    wr = s["wins"] / s["trades"] * 100 if s["trades"] else 0
    print(f"{name:25s} {s['trades']:8d} {wr:5.1f}% {s['pnl']:+8.2f}% {len(s['coins']):3d}")

print(f"\n{'='*70}")
print("WINNERS (keep):")
print(f"{'='*70}")
for name, s in ranked:
    if s["pnl"] > 0 and s["trades"] >= 5:
        wr = s["wins"] / s["trades"] * 100 if s["trades"] else 0
        print(f"  ✅ {name:20s} +{s['pnl']:6.2f}%  {s['trades']}t  WR={wr:.1f}%  {len(s['coins'])} coins")

print(f"\n{'='*70}")
print(f"LOSERS (disable):")
print(f"{'='*70}")
for name, s in ranked:
    if s["pnl"] < 0:
        wr = s["wins"] / s["trades"] * 100 if s["trades"] else 0
        print(f"  ❌ {name:20s} {s['pnl']:7.2f}%  {s['trades']}t  WR={wr:.1f}%  {len(s['coins'])} coins")

print(f"\nFinished: {datetime.now(timezone.utc).isoformat()}")
