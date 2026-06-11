#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
Multi-Agent Backtest Runner v2
==============================
Tests all 11 enabled trading agents across 9 timeframes on BloFin historical data.
30+ days of data per symbol, proper point-in-time walkthrough.

Usage:
    cd /Users/saad/multi_agent_bot
    ./backtest_all.py

Strategy:
    For each (agent, timeframe, symbol) combination, walk through the 5m data
    bar-by-bar (with 200 warmup), building MarketContext from partial
    data windows, calling agent.analyze(), and simulating trades on forward bars.
    
    Uses 1000 candles of 5m (= 3.5 days) for bar-by-bar walk-through AND
    1000 candles of 1H (= 41 days) for higher timeframe context.

Requires:
    - blofin pip package
    - pandas, numpy
    - .env with BLOFIN_API_KEY, BLOFIN_API_SECRET, BLOFIN_PASSPHRASE
"""

import os, sys, json, math, time, traceback
from datetime import datetime, timezone
from collections import defaultdict
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# Import directly from bot.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot

# BloFin client (env vars loaded by bot.py's _load_dotenv_once at import time)
bf = bot.BloFin()

# ──────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "HYPE-USDT"]

# The 11 enabled agents
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
]

# 9 timeframes to test
TIMEFRAMES = ["5m", "15m", "30m", "1H", "2H", "4H", "8H", "12H", "24H"]

# Use 1000 candles of 5m for bar-by-bar walk-through (3.5 days)
# AND 1000 candles of 1H for higher TF context (41 days)
# This gives us 41-day lookback for the higher TFs
CANDLES_5M = 1000
CANDLES_1H = 1000
WARMUP_5M = 200    # ~16h warmup for short-TF agents
WARMUP_1H = 200    # ~8 days warmup for long-TF agents

# Min confidence to consider a signal
MIN_CONFIDENCE = 6

# Max bars to hold a trade (500 5m bars = ~41 hours)
MAX_HOLD_BARS = 500

# TF map: 5m interval count for each TF
TF_5M_BARS = {"5m": 1, "15m": 3, "30m": 6, "1H": 12, "2H": 24,
              "4H": 48, "8H": 96, "12H": 144, "24H": 288}

# TF map for resample from 1H
TF_1H_BARS = {"2H": 2, "4H": 4, "8H": 8, "12H": 12, "24H": 24}

# Which agents use which primary DataFrames in their analyze() method
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
}

# Test timeframe for each agent (in 5m bar stride)
TF_STRIDES = {}
for tf_name, bars in TF_5M_BARS.items():
    TF_STRIDES[tf_name] = bars


# ──────────────────────────────────────────────────────────────────────
# DATA FETCHING & RESAMPLING
# ──────────────────────────────────────────────────────────────────────
def fetch_data(symbol: str) -> Dict[str, pd.DataFrame]:
    """Fetch 5m and 1H data, resample to all needed timeframes."""
    
    # Fetch 1H data for long-range context (41 days)
    df_1h = bf.candles(symbol, "1H", CANDLES_1H)
    if df_1h.empty:
        print(f"  ✗ No 1H data for {symbol}")
        return {}
    
    df_1h = df_1h.sort_values("ts").reset_index(drop=True)
    
    # Fetch 5m data for bar-by-bar walk-through (3.5 days)
    df_5m = bf.candles(symbol, "5m", CANDLES_5M)
    if df_5m.empty:
        print(f"  ✗ No 5m data for {symbol}")
        return {}
    
    df_5m = df_5m.sort_values("ts").reset_index(drop=True)
    
    data = {
        "5m": df_5m,
        "1H": df_1h,
    }
    
    # Resample 5m -> 15m, 30m
    data["15m"] = _resample_ohlcv(df_5m, 3)   # 3 x 5m bars = 15m
    data["30m"] = _resample_ohlcv(df_5m, 6)   # 6 x 5m bars = 30m
    
    # Resample 1H -> 2H, 4H, 8H, 12H, 24H
    for tf, chunks in TF_1H_BARS.items():
        data[tf] = _resample_ohlcv(df_1h, chunks)
    
    return data


def _resample_ohlcv(df_input: pd.DataFrame, chunk_size: int) -> pd.DataFrame:
    """
    Resample OHLCV by combining `chunk_size` consecutive bars.
    Works for both 5m->15m/30m and 1H->2H/4H/etc.
    """
    df = df_input.copy()
    df["_group"] = np.arange(len(df)) // chunk_size
    resampled = df.groupby("_group").agg({
        "ts": "first",
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }).dropna().reset_index(drop=True)
    return resampled


# ──────────────────────────────────────────────────────────────────────
# CONTEXT BUILDER
# ──────────────────────────────────────────────────────────────────────
def build_context(symbol: str, data: Dict[str, pd.DataFrame],
                  idx_5m: int) -> bot.MarketContext:
    """
    Build MarketContext from the index of the 5m DataFrame.
    Each higher TF is sliced to include only data up to the equivalent point in time.
    """
    df5 = data["5m"].iloc[:idx_5m+1].copy().reset_index(drop=True)
    ts_limit = df5["ts"].iloc[-1]

    def _slice(df_tf: pd.DataFrame) -> pd.DataFrame:
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
        trend = bot.TrendState()
    )
    
    # Compute trend state from sliced 1H data
    try:
        df_1h_slice = _slice(data.get("1H", pd.DataFrame()))
        if len(df_1h_slice) >= 20:
            trend = bot.compute_trend_state(df_1h_slice)
    except Exception:
        pass
    
    return bot.MarketContext(
        symbol=symbol,
        df_5m=df5,
        df_15m=_slice(data.get("15m", pd.DataFrame())),
        df_30m=_slice(data.get("30m", pd.DataFrame())),
        df_1h=_slice(data.get("1H", pd.DataFrame())),
        funding_rate=0.0,
        orderbook={"bids": [], "asks": []},
        news_sentiment={},
        trend=trend,
    )


# ──────────────────────────────────────────────────────────────────────
# TRADE SIMULATION
# ──────────────────────────────────────────────────────────────────────
def simulate_trade(signal: bot.Signal,
                   df_future_5m: pd.DataFrame,
                   entry_idx_5m: int) -> dict:
    """
    Simulate a trade from entry forward using 5m candles.
    Steps through each 5m bar checking for SL/TP hits.
    Respects limit_price from signal metadata if present (limit entry).
    """
    side = signal.side
    meta = signal.metadata or {}
    
    # Check if this is a limit entry
    limit_price = None
    if meta and "limit_price" in meta and meta["limit_price"] and float(meta["limit_price"]) > 0:
        limit_price = float(meta["limit_price"])
    
    # Find actual entry: walk forward until limit fills (or skip if never fills)
    entry_bar_idx = 0
    if limit_price:
        # Walk through bars to find when limit fills
        filled = False
        for i in range(len(df_future_5m)):
            bar = df_future_5m.iloc[i]
            hi = float(bar["high"])
            lo = float(bar["low"])
            if side == "long" and lo <= limit_price:
                # Limit buy filled at limit_price (we got the zone price)
                entry_price = limit_price
                entry_bar_idx = i
                filled = True
                break
            elif side == "short" and hi >= limit_price:
                # Limit short filled at limit_price
                entry_price = limit_price
                entry_bar_idx = i
                filled = True
                break
        if not filled:
            return None  # Never filled — skip this trade
        future_5m_entry = df_future_5m.iloc[entry_bar_idx:].copy().reset_index(drop=True)
    else:
        entry_price = float(df_future_5m.iloc[0]["open"])
        future_5m_entry = df_future_5m

    # Extract SL/TP from signal metadata or use 1:2 R:R from profile defaults
    if "atr_sl" in meta and meta["atr_sl"]:
        sl_price = float(meta["atr_sl"])
    else:
        profile = bot.PROFILES.get(signal.profile, {"sl": 2.0})
        sl_pct = profile.get("sl", 2.0) / 100.0
        sl_price = entry_price * (1 - sl_pct) if side == "long" else entry_price * (1 + sl_pct)

    if "atr_tp" in meta and meta["atr_tp"]:
        tp_price = float(meta["atr_tp"])
    else:
        if side == "long":
            tp_price = entry_price + 2 * (entry_price - sl_price)
        else:
            tp_price = entry_price - 2 * (sl_price - entry_price)

    pnl_pct = 0.0
    trade_bars = 0
    reason = "max_bars"

    for i in range(1, len(future_5m_entry)):
        bar = future_5m_entry.iloc[i]
        high = float(bar["high"])
        low = float(bar["low"])

        if side == "long":
            if high >= tp_price:
                pnl_pct = (tp_price / entry_price - 1) * 100
                reason = "tp"
                trade_bars = i
                break
            if low <= sl_price:
                pnl_pct = (sl_price / entry_price - 1) * 100
                reason = "sl"
                trade_bars = i
                break
        else:
            if low <= tp_price:
                pnl_pct = (1 - tp_price / entry_price) * 100
                reason = "tp"
                trade_bars = i
                break
            if high >= sl_price:
                pnl_pct = (1 - sl_price / entry_price) * 100
                reason = "sl"
                trade_bars = i
                break

    if reason == "max_bars":
        exit_price = float(future_5m_entry.iloc[-1]["close"])
        if side == "long":
            pnl_pct = (exit_price / entry_price - 1) * 100
        else:
            pnl_pct = (1 - exit_price / entry_price) * 100
        trade_bars = len(future_5m_entry) - 1

    return {
        "entry_price": entry_price,
        "sl_price": sl_price,
        "tp_price": tp_price,
        "exit_reason": reason,
        "pnl_pct": pnl_pct,
        "trade_bars": trade_bars,
        "side": side,
        "confidence": signal.confidence,
        "profile": signal.profile,
        "reason": signal.reason,
    }


# ──────────────────────────────────────────────────────────────────────
# BACKTEST ONE (AGENT x TF x SYMBOL)
# ──────────────────────────────────────────────────────────────────────
def backtest_one(agent_cls, agent_name: str, tf: str, symbol: str,
                 data: Dict[str, pd.DataFrame]) -> dict:
    """Backtest one agent on one timeframe for one symbol."""
    agent = agent_cls()
    df_5m = data["5m"]
    n_bars = len(df_5m)
    stride = TF_STRIDES.get(tf, 1)
    
    # Warmup: use enough bars so the primary TF has data
    primary_tf_name = AGENT_PRIMARY_TF.get(agent_name, "1H")
    primary_tf_stride = TF_STRIDES.get(primary_tf_name, 12)
    # Need primary_tf_stride * warmup bars of 5m data
    warmup_bars = min(WARMUP_5M + primary_tf_stride * 5, n_bars // 4)

    trades = []
    last_signal_reason = None
    last_signal_ts = 0
    min_signal_gap_5m = stride * 12  # At least 12 TF bars between same-type signals

    # Iterate through 5m bars
    for idx_5m in range(warmup_bars, n_bars):
        # Only check signals at TF bar boundaries (stride)
        if idx_5m % stride != 0:
            continue

        # Build context at this point in time
        ctx = build_context(symbol, data, idx_5m)

        try:
            signal = agent.analyze(symbol, ctx)
        except Exception as e:
            continue

        if signal is None:
            continue
        if signal.confidence <= MIN_CONFIDENCE:
            continue
            
        # Deduplicate: don't fire same signal repeatedly while still in that zone
        sig_reason = f"{signal.side}_{signal.reason}"
        if sig_reason == last_signal_reason and (idx_5m - last_signal_ts) < min_signal_gap_5m:
            continue
        last_signal_reason = sig_reason
        last_signal_ts = idx_5m

        # Simulate trade on forward 5m data
        future_5m = df_5m.iloc[idx_5m+1:min(idx_5m+1+MAX_HOLD_BARS, n_bars)].copy().reset_index(drop=True)
        if len(future_5m) < 2:
            continue

        result = simulate_trade(signal, future_5m, idx_5m)
        if result is None:
            continue  # Limit order never filled

        trades.append({
            "bar_idx": idx_5m,
            "entry_ts": int(df_5m.iloc[idx_5m]["ts"] / 1000),
            "entry_price": result["entry_price"],
            "exit_price": result.get("exit_price", 0),
            "sl_price": result["sl_price"],
            "tp_price": result["tp_price"],
            "side": result["side"],
            "confidence": result["confidence"],
            "pnl_pct": result["pnl_pct"],
            "exit_reason": result["exit_reason"],
            "trade_bars": result["trade_bars"],
            "profile": result["profile"],
            "reason": signal.reason,
        })

    # ── Aggregate stats ──
    total_trades = len(trades)
    if total_trades == 0:
        return {
            "agent": agent_name,
            "timeframe": tf,
            "symbol": symbol,
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "total_return_pct": 0.0,
            "avg_return_pct": 0.0,
            "max_drawdown_pct": 0.0,
            "profit_factor": 0.0,
            "max_loss_pct": 0.0,
            "trades": [],
        }

    pnls = [t["pnl_pct"] for t in trades]
    wins = sum(1 for p in pnls if p > 0)
    losses = sum(1 for p in pnls if p <= 0)
    total_return = sum(pnls)

    cumulative = np.cumsum(pnls)
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = running_max - cumulative
    max_dd = float(np.max(drawdowns)) if len(drawdowns) > 0 else 0.0

    gross_profit = sum(p for p in pnls if p > 0)
    gross_loss = abs(sum(p for p in pnls if p < 0))
    pf = gross_profit / gross_loss if gross_loss > 0 else (gross_profit if gross_profit > 0 else 0.0)
    max_loss = min(pnls) if pnls else 0.0

    return {
        "agent": agent_name,
        "timeframe": tf,
        "symbol": symbol,
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": round(wins / total_trades * 100, 2),
        "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(total_return / total_trades, 4),
        "max_drawdown_pct": round(max_dd, 2),
        "profit_factor": round(pf, 2),
        "max_loss_pct": round(max_loss, 2),
        "trades": trades,
    }


# ──────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print(f"MULTI-AGENT BACKTEST v2: {len(AGENT_SPECS)} agents × {len(TIMEFRAMES)} TFs × {len(SYMBOLS)} symbols")
    print(f"  5m: {CANDLES_5M} bars (3.5 days), 1H: {CANDLES_1H} bars (41 days)")
    print(f"  5m warmup: {WARMUP_5M} bars, 1H warmup: {WARMUP_1H} bars")
    print(f"  Min confidence: {MIN_CONFIDENCE}")
    print("=" * 70)
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print()

    all_results = []

    for symbol in SYMBOLS:
        print(f"\n{'─' * 60}")
        print(f"SYMBOL: {symbol}")
        sys.stdout.flush()
        
        data = fetch_data(symbol)
        if not data:
            print(f"  ✗ No data, skipping")
            continue

        df5 = data["5m"]
        df1h = data["1H"]
        print(f"  ✓ {len(df5)} 5m bars: "
              f"{datetime.fromtimestamp(df5['ts'].iloc[0]/1000).strftime('%m-%d %H:%M')} → "
              f"{datetime.fromtimestamp(df5['ts'].iloc[-1]/1000).strftime('%m-%d %H:%M')}")
        print(f"  ✓ {len(df1h)} 1H bars: "
              f"{datetime.fromtimestamp(df1h['ts'].iloc[0]/1000).strftime('%m-%d %H:%M')} → "
              f"{datetime.fromtimestamp(df1h['ts'].iloc[-1]/1000).strftime('%m-%d %H:%M')}")
        for tf in sorted(TF_5M_BARS.keys()):
            if tf in data:
                print(f"    {tf}: {len(data[tf])} bars")
        sys.stdout.flush()

        for agent_name, agent_cls in AGENT_SPECS:
            print(f"\n  Agent: {agent_name}")
            sys.stdout.flush()

            for tf in TIMEFRAMES:
                print(f"    [{tf:>4s}] ", end="", flush=True)
                result = backtest_one(agent_cls, agent_name, tf, symbol, data)
                all_results.append(result)
                n = result["total_trades"]
                r = result["total_return_pct"]
                w = result["win_rate"]
                dd = result["max_drawdown_pct"]
                e = len(result.get("errors", []))
                err_str = f" ({e} errs)" if e > 0 else ""
                print(f"{n:4d}t  ret={r:+.2f}%  WR={w:>5.1f}%  DD={dd:>5.2f}%{err_str}", flush=True)

    # ── Save full JSON ──
    output = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbols": SYMBOLS,
            "agents": [a[0] for a in AGENT_SPECS],
            "timeframes": TIMEFRAMES,
            "candles_5m": CANDLES_5M,
            "candles_1h": CANDLES_1H,
            "warmup_5m": WARMUP_5M,
            "warmup_1h": WARMUP_1H,
        },
        "results": all_results,
    }
    with open("/Users/saad/multi_agent_bot/backtest_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n{'=' * 70}")
    print(f"Saved full results to backtest_results.json")
    print(f"  {len(all_results)} entries ({len([r for r in all_results if r['total_trades'] > 0])} with trades)")

    # ── Print sorted summary table ──
    print(f"\n{'=' * 70}")
    print("SUMMARY — Sorted by total return (aggregated across all symbols)")
    print(f"{'=' * 70}")

    agg = defaultdict(lambda: {
        "total_return": 0.0, "wins": 0, "losses": 0,
        "total_trades": 0, "max_dd": 0.0, "pnls": []
    })

    for r in all_results:
        key = (r["agent"], r["timeframe"])
        agg[key]["total_return"] += r["total_return_pct"]
        agg[key]["wins"] += r["wins"]
        agg[key]["losses"] += r["losses"]
        agg[key]["total_trades"] += r["total_trades"]
        agg[key]["max_dd"] = max(agg[key]["max_dd"], r["max_drawdown_pct"])

    sorted_keys = sorted(agg.keys(), key=lambda k: agg[k]["total_return"], reverse=True)

    header = f"{'Agent':<22} {'TF':<6} {'Total Ret%':<12} {'WR%':<8} {'Trades':<8} {'MaxDD%':<8}"
    print(header)
    print("-" * len(header))

    for key in sorted_keys:
        d = agg[key]
        n = d["total_trades"]
        wr = d["wins"] / n * 100 if n > 0 else 0.0
        print(f"{key[0]:<22} {key[1]:<6} {d['total_return']:>+.2f}%   {wr:>5.1f}%   {n:>5d}   {d['max_dd']:>6.2f}%")

    # Per-agent best TF
    print(f"\n{'=' * 70}")
    print("BEST TF FOR EACH AGENT")
    print(f"{'=' * 70}")
    for agent_name, _ in AGENT_SPECS:
        agent_results = [r for r in all_results if r["agent"] == agent_name]
        if not agent_results:
            continue
        best = max(agent_results, key=lambda r: r["total_return_pct"])
        worst = min(agent_results, key=lambda r: r["total_return_pct"])
        print(f"  {agent_name:<20} BEST: {best['timeframe']:>4s}  {best['total_return_pct']:>+.2f}%  "
              f"WR={best['win_rate']:>5.1f}%  {best['total_trades']:>4d}t  "
              f"WORST: {worst['timeframe']:>4s}  {worst['total_return_pct']:+.2f}%")

    print(f"\nFinished: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
