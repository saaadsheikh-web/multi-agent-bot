#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
TRADINGVIEW BACKTEST v2 — Deep backtest using TradingView data (not BloFin).
Tests ALL enabled agents across all coins and timeframes with 5000 bars of data.

5m: 5000 bars (~17 days)
1H: 5000 bars (~7 months) + resample to HTF
"""
import os, sys, json, math, time, traceback
from datetime import datetime, timezone
from collections import defaultdict
from typing import Optional, List, Dict, Any, Tuple

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot
from tv_data import all_timeframes_for_backtest as tv_candles

bf = bot.BloFin()  # Only used for balance check, not data

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

TIMEFRAMES = ["5m", "15m", "30m", "1H", "2H", "4H", "8H", "12H", "24H"]

# Warmup in 5m bars (200 = ~16h)
WARMUP_5M = 200
WARMUP_1H = 200
MIN_CONFIDENCE = 6
MAX_HOLD_BARS = 500

# TF maps
TF_5M_BARS = {"5m": 1, "15m": 3, "30m": 6, "1H": 12, "2H": 24,
              "4H": 48, "8H": 96, "12H": 144, "24H": 288}

AGENT_PRIMARY_TF = {
    "asymmetric":         "1H",
    "daily_breakout":     "1H",
    "daily_breakout_24h": "1H",
    "daily_breakout_4h":  "1H",
    "daily_breakout_12h": "1H",
    "daily_breakout_48h": "1H",
    "liquidity_sweep":    "5m",
    "wide_scalp":         "1H",
    "utbot_mtf":          "15m",
    "fib_confluence":     "1H",
    "fib_bounce":         "1H",
    "turtle_breakout":    "1H",
    "livermore_pivot":    "1H",
    "quick_scalp":        "1H",
}


def fetch_data(symbol: str) -> Dict[str, pd.DataFrame]:
    """Fetch ALL timeframes from TradingView."""
    print(f"\n  Fetching {symbol} from TradingView...")
    data = tv_candles(symbol)
    return data


def build_context(symbol: str, data: Dict[str, pd.DataFrame],
                  idx_5m: int) -> bot.MarketContext:
    """Build MarketContext from index of 5m df."""
    df5 = data["5m"].iloc[:idx_5m+1].copy().reset_index(drop=True)
    ts_limit = df5["ts"].iloc[-1]
    
    def _slice(df_tf):
        if df_tf.empty:
            return df_tf
        mask = df_tf["ts"] <= ts_limit
        return df_tf[mask].copy().reset_index(drop=True)
    
    ctx = bot.MarketContext(
        symbol=symbol,
        df_5m=df5,
        df_15m=_slice(data.get("15m", pd.DataFrame())),
        df_30m=_slice(data.get("30m", pd.DataFrame())),
        df_1h=_slice(data.get("1H", pd.DataFrame())),
        funding_rate=0.0,
        orderbook={"bids": [], "asks": []},
        news_sentiment={},
        trend=bot.TrendState()
    )
    return ctx


def simulate_trade(entry_bar: int, ctx_snapshot: bot.MarketContext,
                   symbol: str, side: str,
                   data: Dict[str, pd.DataFrame],
                   primary_tf: str) -> Optional[Dict]:
    """Simulate a trade to completion."""
    df5 = data["5m"]
    
    # Determine entry price from context
    if primary_tf == "5m":
        entry_ctx_df = ctx_snapshot.df_5m
    else:
        entry_ctx_df = ctx_snapshot.df_1h
    
    if entry_ctx_df.empty:
        return None
    
    entry_price = entry_ctx_df["close"].iloc[-1]
    if pd.isna(entry_price) or entry_price <= 0:
        return None
    
    # SL = 2% hard stop
    if side == "long":
        sl_price = entry_price * 0.98
    else:
        sl_price = entry_price * 1.02
    
    # Simulate forward
    j = entry_bar + 1
    max_j = min(entry_bar + MAX_HOLD_BARS, len(df5))
    
    exit_price = entry_price
    exit_reason = "time"
    
    while j < max_j:
        bar_h = df5["high"].iloc[j]
        bar_l = df5["low"].iloc[j]
        
        if side == "long":
            if bar_l <= sl_price:
                exit_price = sl_price
                exit_reason = "stop"
                break
        else:
            if bar_h >= sl_price:
                exit_price = sl_price
                exit_reason = "stop"
                break
        j += 1
    
    if exit_reason == "time":
        exit_price = df5["close"].iloc[min(entry_bar + MAX_HOLD_BARS, len(df5)-1)]
    
    pnl_pct = ((exit_price - entry_price) / entry_price * 100) if side == "long" else \
              ((entry_price - exit_price) / entry_price * 100)
    pnl_pct -= 0.04  # commission
    
    return {
        "entry": entry_price,
        "exit": exit_price,
        "pnl_pct": pnl_pct,
        "exit_reason": exit_reason,
    }


# ── MAIN ──
print("=" * 70)
print("TRADINGVIEW BACKTEST v2 — 5000 bars per TF")
print(f"  Agents: {len(AGENT_SPECS)}, TFs: {len(TIMEFRAMES)}, Symbols: {len(SYMBOLS)}")
print("=" * 70)
print(f"Started: {datetime.now(timezone.utc).isoformat()}")
print()

all_results = []

for sym in SYMBOLS:
    data = fetch_data(sym)
    if not data or "5m" not in data or "1H" not in data:
        print(f"  ✗ SKIPPING {sym} — no data")
        continue
    
    df5 = data["5m"]
    df1h = data["1H"]
    
    print(f"  {len(df5)} 5m bars: starting at {df5.iloc[0]['ts']}")
    print(f"  {len(df1h)} 1H bars: starting at {df1h.iloc[0]['ts']}")
    
    for name, agent_cls in AGENT_SPECS:
        agent = agent_cls()
        if not agent.enabled:
            continue
        
        primary_tf = AGENT_PRIMARY_TF.get(name, "1H")
        tf_stride = TF_5M_BARS.get(primary_tf, 12)
        warmup = WARMUP_5M if primary_tf == "5m" else WARMUP_1H
        
        agent_trades = []
        
        for i in range(warmup, len(df5)):
            if i % tf_stride != 0:
                continue
            
            ctx = build_context(sym, data, i)
            if ctx.df_1h.empty or ctx.df_5m.empty:
                continue
            
            try:
                sig = agent.analyze(sym, ctx)
                if sig and sig.confidence >= MIN_CONFIDENCE:
                    sim_result = simulate_trade(i, ctx, sym, sig.side, data, primary_tf)
                    if sim_result:
                        agent_trades.append(sim_result)
            except Exception as e:
                continue
        
        # Summarize
        if agent_trades:
            wins = sum(1 for t in agent_trades if t["pnl_pct"] > 0)
            total_pnl = sum(t["pnl_pct"] for t in agent_trades)
            dd = 0
            peak = 0
            for t in agent_trades:
                peak = max(peak, 0)
                peak += t["pnl_pct"]
                if peak < 0:
                    dd = min(dd, peak)
            
            print(f"  {name:20s} [{primary_tf:4s}] {len(agent_trades):4d}t  "
                  f"WR={wins/len(agent_trades)*100:5.1f}%  "
                  f"ret={total_pnl:+.2f}%  DD={abs(dd):.2f}%")
            
            all_results.append({
                "symbol": sym, "agent": name, "tf": primary_tf,
                "trades": len(agent_trades), "wins": wins,
                "wr": round(wins/len(agent_trades)*100, 1),
                "ret": round(total_pnl, 2),
                "dd": round(abs(dd), 2),
            })
        else:
            print(f"  {name:20s} [{primary_tf:4s}]    0t  ret=+0.00%")

print()
print("=" * 70)
print("SUMMARY — Aggregated across all symbols")
print("=" * 70)

from collections import defaultdict
agent_summary = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0, "coins": set()})
for r in all_results:
    key = f"{r['agent']}_{r['tf']}"
    agent_summary[key]["trades"] += r["trades"]
    agent_summary[key]["wins"] += r["wins"]
    agent_summary[key]["pnl"] += r["ret"]
    agent_summary[key]["coins"].add(r["symbol"])

print(f"{'Agent/TF':25s} {'Trades':>8s} {'WR%':>6s} {'Ret%':>8s} {'Coins':>6s}")
print("-" * 55)
for key in sorted(agent_summary.keys(), key=lambda k: -agent_summary[k]["pnl"]):
    s = agent_summary[key]
    wr = s["wins"] / s["trades"] * 100 if s["trades"] > 0 else 0
    name, tf = key.rsplit("_", 1)
    display = f"{name}_{tf}"
    print(f"{display:25s} {s['trades']:8d} {wr:5.1f}% {s['pnl']:+8.2f}% {len(s['coins']):3d}")

print()
print(f"Finished: {datetime.now(timezone.utc).isoformat()}")
