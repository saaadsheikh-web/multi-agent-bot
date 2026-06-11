#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
SCALP BACKTEST — 5m/15m data, short holds, tight stops
Tests: LiquiditySweep, WideScalp, UTBotMTF, MACDCross, SmartScalp
       across 5m, 15m, 30m, 1H on 5 coins
Goal: 100+ trades per combo to see real edge
"""
import os, sys, json, math, time
from datetime import datetime, timezone
from collections import defaultdict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot

bf = bot.BloFin()

SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "HYPE-USDT"]

# Scalping agents only (small TF, tight stops)
SCALP_SPECS = [
    ("liquidity_sweep",  bot.LiquiditySweepScalpAgent),
    ("wide_scalp",       bot.WideScalpAgent),
    ("utbot_mtf",        bot.UTBotMTFAgent),
    ("macd_cross",       bot.MACDCrossAgent),
    ("smart_scalp",      bot.SmartScalpAgent),
]

# Test on small TFs that scalpers actually use
TIMEFRAMES = ["5m", "15m", "30m", "1H"]

# Fetch ~90 days of 5m data (26280 bars), resample up
MAX_BARS_5M = 17280    # ~60 days of 5m (BloFin has less history for some coins)
WARMUP_5M = 2000       # ~7 days warmup

MIN_CONFIDENCE = 6
MAX_HOLD_BARS = 96     # max ~8 hours hold (96 * 5m)

# TF map: 5m interval count
TF_5M_BARS = {"5m": 1, "15m": 3, "30m": 6, "1H": 12}


def resample_to_tf(df, chunk_size):
    df = df.copy()
    df["_g"] = np.arange(len(df)) // chunk_size
    return df.groupby("_g").agg({
        "ts": "first", "open": "first", "high": "max",
        "low": "min", "close": "last", "volume": "sum",
    }).dropna().reset_index(drop=True)


def fetch_scalp_data(symbol):
    """Fetch 5m data with pagination, resample to all scalp TFs."""
    CHUNK = 1000
    all_chunks = []
    
    # Start from ~91 days ago
    after = str(int((datetime.now(timezone.utc).timestamp() - 92 * 86400) * 1000))
    
    for i in range(30):
        try:
            r = bf.client.public.get_candlesticks(
                inst_id=symbol, bar="5m", limit=CHUNK, after=after
            )
        except Exception as e:
            print(f"  ✗ Error fetching {symbol}: {e}")
            return None
        
        rows = (r or {}).get("data") or []
        if not rows:
            break
        
        cols = ["ts", "open", "high", "low", "close", "volume", "vc", "vcq", "confirm"]
        width = min(len(rows[0]), len(cols))
        df_chunk = pd.DataFrame([row[:width] for row in rows], columns=cols[:width])
        for c in ["ts", "open", "high", "low", "close", "volume"]:
            if c in df_chunk.columns:
                df_chunk[c] = pd.to_numeric(df_chunk[c], errors="coerce")
        df_chunk = df_chunk.sort_values("ts").dropna(subset=["close"]).reset_index(drop=True)
        
        oldest_raw = int(rows[-1][0])
        all_chunks.append(df_chunk)
        total = sum(len(c) for c in all_chunks)
        print(f"  ✓ Chunk {i}: {len(df_chunk)} bars from "
              f"{datetime.fromtimestamp(df_chunk['ts'].iloc[0]/1000).strftime('%m-%d')} "
              f"to {datetime.fromtimestamp(df_chunk['ts'].iloc[-1]/1000).strftime('%m-%d')} "
              f"(total: {total})")
        
        after = str(int(oldest_raw - 1))
        if total >= MAX_BARS_5M:
            break
    
    if not all_chunks:
        print(f"  ✗ No data for {symbol}")
        return None
    
    df_5m = pd.concat(all_chunks, ignore_index=True)
    df_5m = df_5m.sort_values("ts").drop_duplicates(subset=["ts"]).reset_index(drop=True)
    if len(df_5m) > MAX_BARS_5M:
        df_5m = df_5m.iloc[-MAX_BARS_5M:].reset_index(drop=True)
    
    data = {"5m": df_5m}
    for tf, chunk in TF_5M_BARS.items():
        if tf == "5m":
            continue
        data[tf] = resample_to_tf(df_5m, chunk)
    
    return data


def build_scalp_context(symbol, all_data, idx_5m):
    """Build MarketContext at 5m index with all resampled TFs up to current bar."""
    df_5m = all_data["5m"].iloc[:idx_5m+1].copy().reset_index(drop=True)
    ts_limit = df_5m["ts"].iloc[-1]
    
    def _slice(name):
        df = all_data.get(name)
        if df is None or df.empty:
            return pd.DataFrame()
        return df[df["ts"] <= ts_limit].copy().reset_index(drop=True)
    
    trend = bot.TrendState()
    try:
        if len(df_5m) >= 240:
            df_1h_slice = df_5m.iloc[-240:]
            dfh_resampled = resample_to_tf(df_1h_slice, 12)
            if len(dfh_resampled) >= 20:
                trend = bot.compute_trend_state(dfh_resampled)
    except Exception:
        pass
    
    df_1h = _slice("1H")
    df_15m = _slice("15m")
    df_30m = _slice("30m")
    
    return bot.MarketContext(
        symbol=symbol,
        df_5m=df_5m,
        df_15m=df_15m,
        df_30m=df_30m,
        df_1h=df_1h,
        funding_rate=0.0,
        orderbook={"bids": [], "asks": []},
        news_sentiment={},
        trend=trend,
    )


def scalp_simulate(signal, df_future_5m, entry_idx):
    """Simulate trade on forward 5m data with SL/TP from signal metadata."""
    side = signal.side
    meta = signal.metadata or {}
    entry_price = float(df_future_5m.iloc[0]["open"])
    
    # Use signal's ATR-based SL/TP if available
    if meta and "atr_sl" in meta and meta["atr_sl"]:
        sl_price = float(meta["atr_sl"])
    else:
        profile = bot.PROFILES.get(signal.profile, {"sl": 2.0})
        sl_pct = profile.get("sl", 2.0) / 100.0
        sl_price = entry_price * (1 - sl_pct) if side == "long" else entry_price * (1 + sl_pct)
    
    if meta and "atr_tp" in meta and meta["atr_tp"]:
        tp_price = float(meta["atr_tp"])
    else:
        if side == "long":
            tp_price = entry_price + 2 * (entry_price - sl_price)
        else:
            tp_price = entry_price - 2 * (sl_price - entry_price)
    
    pnl_pct = 0.0
    reason = "max_bars"
    trade_bars = 0
    
    for i in range(1, len(df_future_5m)):
        bar = df_future_5m.iloc[i]
        high = float(bar["high"])
        low = float(bar["low"])
        
        if side == "long":
            if high >= tp_price:
                pnl_pct = (tp_price / entry_price - 1) * 100
                reason = "tp"; trade_bars = i; break
            if low <= sl_price:
                pnl_pct = (sl_price / entry_price - 1) * 100
                reason = "sl"; trade_bars = i; break
        else:
            if low <= tp_price:
                pnl_pct = (1 - tp_price / entry_price) * 100
                reason = "tp"; trade_bars = i; break
            if high >= sl_price:
                pnl_pct = (1 - sl_price / entry_price) * 100
                reason = "sl"; trade_bars = i; break
    
    if reason == "max_bars":
        exit_price = float(df_future_5m.iloc[-1]["close"])
        pnl_pct = (exit_price / entry_price - 1) * 100 if side == "long" else (1 - exit_price / entry_price) * 100
        trade_bars = len(df_future_5m) - 1
    
    return {
        "entry_price": entry_price, "sl_price": sl_price, "tp_price": tp_price,
        "exit_reason": reason, "pnl_pct": pnl_pct, "trade_bars": trade_bars,
        "side": side, "confidence": signal.confidence,
        "profile": signal.profile, "reason": signal.reason,
    }


def backtest_scalp(agent_cls, agent_name, tf, symbol, all_data):
    """Backtest one scalper on one timeframe for one symbol."""
    agent = agent_cls()
    df_5m = all_data["5m"]
    n_bars = len(df_5m)
    stride = TF_5M_BARS[tf]
    
    warmup = min(WARMUP_5M, n_bars // 4)
    
    trades = []
    last_sig = None
    last_sig_idx = -9999
    min_gap = stride * 24  # at least 2 hours between same signal
    
    for idx in range(warmup, n_bars):
        if idx % stride != 0:
            continue
        
        ctx = build_scalp_context(symbol, all_data, idx)
        
        try:
            signal = agent.analyze(symbol, ctx)
        except Exception:
            continue
        
        if signal is None or signal.confidence <= MIN_CONFIDENCE:
            continue
        
        sig_key = f"{signal.side}_{signal.reason}"
        if sig_key == last_sig and (idx - last_sig_idx) < min_gap:
            continue
        last_sig = sig_key
        last_sig_idx = idx
        
        future = df_5m.iloc[idx+1:min(idx+1+MAX_HOLD_BARS, n_bars)].copy().reset_index(drop=True)
        if len(future) < 2:
            continue
        
        result = scalp_simulate(signal, future, idx)
        
        trades.append({
            "bar_idx": idx,
            "entry_ts": int(df_5m.iloc[idx]["ts"] / 1000),
            "entry_price": result["entry_price"],
            "sl_price": result["sl_price"],
            "tp_price": result["tp_price"],
            "side": result["side"],
            "confidence": result["confidence"],
            "pnl_pct": result["pnl_pct"],
            "exit_reason": result["exit_reason"],
            "trade_bars": result["trade_bars"],
        })
    
    n = len(trades)
    if n == 0:
        return {"agent": agent_name, "timeframe": tf, "symbol": symbol,
                "total_trades": 0, "wins": 0, "losses": 0, "win_rate": 0.0,
                "total_return_pct": 0.0, "avg_return_pct": 0.0,
                "max_drawdown_pct": 0.0, "profit_factor": 0.0,
                "max_loss_pct": 0.0, "trades": []}
    
    pnls = [t["pnl_pct"] for t in trades]
    wins = sum(1 for p in pnls if p > 0)
    losses = sum(1 for p in pnls if p <= 0)
    total_ret = sum(pnls)
    
    cum = np.cumsum(pnls)
    rmax = np.maximum.accumulate(cum)
    dd = float(np.max(rmax - cum)) if len(cum) > 0 else 0.0
    
    gp = sum(p for p in pnls if p > 0)
    gl = abs(sum(p for p in pnls if p < 0))
    pf = gp / gl if gl > 0 else (gp if gp > 0 else 0.0)
    
    return {
        "agent": agent_name, "timeframe": tf, "symbol": symbol,
        "total_trades": n, "wins": wins, "losses": losses,
        "win_rate": round(wins / n * 100, 2),
        "total_return_pct": round(total_ret, 2),
        "avg_return_pct": round(total_ret / n, 4),
        "max_drawdown_pct": round(dd, 2),
        "profit_factor": round(pf, 2),
        "max_loss_pct": round(min(pnls), 2),
        "trades": trades,
    }


def main():
    print("=" * 70)
    print(f"SCALP BACKTEST: {len(SCALP_SPECS)} agents × {len(TIMEFRAMES)} TFs × {len(SYMBOLS)} symbols")
    print(f"  {MAX_BARS_5M} 5m bars (~91 days), {WARMUP_5M} bar warmup")
    print(f"  Min confidence: {MIN_CONFIDENCE}, Max hold: {MAX_HOLD_BARS} bars")
    print("=" * 70)
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")
    sys.stdout.flush()
    
    all_results = []
    
    for symbol in SYMBOLS:
        print(f"\n{'─' * 60}")
        print(f"SYMBOL: {symbol}")
        sys.stdout.flush()
        
        data = fetch_scalp_data(symbol)
        if data is None:
            continue
        
        df5 = data["5m"]
        print(f"  ✓ {len(df5)} 5m bars: "
              f"{datetime.fromtimestamp(df5['ts'].iloc[0]/1000).strftime('%Y-%m-%d')} → "
              f"{datetime.fromtimestamp(df5['ts'].iloc[-1]/1000).strftime('%Y-%m-%d')}")
        for tf in TIMEFRAMES:
            if tf in data:
                print(f"    {tf:>5s}: {len(data[tf])} bars")
        sys.stdout.flush()
        
        for agent_name, agent_cls in SCALP_SPECS:
            print(f"\n  {agent_name}:")
            sys.stdout.flush()
            for tf in TIMEFRAMES:
                if len(data.get(tf, pd.DataFrame())) < 10:
                    print(f"    [{tf:>5s}] SKIP (too few bars)")
                    continue
                print(f"    [{tf:>5s}] ", end="", flush=True)
                try:
                    result = backtest_scalp(agent_cls, agent_name, tf, symbol, data)
                except Exception as e:
                    print(f"ERROR: {e}", flush=True)
                    continue
                all_results.append(result)
                n = result["total_trades"]
                r = result["total_return_pct"]
                w = result["win_rate"]
                dd = result["max_drawdown_pct"]
                print(f"{n:4d}t  ret={r:>+8.2f}%  WR={w:>5.1f}%  DD={dd:>5.2f}%", flush=True)
    
    # ── Save ──
    output = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbols": SYMBOLS,
            "agents": [a[0] for a in SCALP_SPECS],
            "timeframes": TIMEFRAMES,
            "max_bars_5m": MAX_BARS_5M,
            "warmup": WARMUP_5M,
        },
        "results": all_results,
    }
    out_path = "/Users/saad/multi_agent_bot/scalp_backtest_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n{'=' * 70}")
    print(f"Saved to {out_path}")
    print(f"  {len(all_results)} entries ({len([r for r in all_results if r['total_trades'] > 0])} with trades)")
    
    # ── SUMMARY ──
    print(f"\n{'=' * 70}")
    print("SCALP SUMMARY — aggregated across 5 coins")
    print(f"{'=' * 70}")
    
    agg = defaultdict(lambda: {"ret": 0.0, "w": 0, "l": 0, "n": 0, "dd": 0.0})
    for r in all_results:
        k = (r["agent"], r["timeframe"])
        agg[k]["ret"] += r["total_return_pct"]
        agg[k]["w"] += r["wins"]
        agg[k]["l"] += r["losses"]
        agg[k]["n"] += r["total_trades"]
        agg[k]["dd"] = max(agg[k]["dd"], r["max_drawdown_pct"])
    
    sorted_k = sorted(agg.keys(), key=lambda k: agg[k]["ret"], reverse=True)
    print(f"{'Agent':<22} {'TF':<6} {'Ret%':<9} {'WR%':<7} {'Trades':<7} {'DD%':<7}")
    print("-" * 55)
    for k in sorted_k:
        d = agg[k]
        if d["n"] == 0:
            continue
        wr = d["w"] / d["n"] * 100
        print(f"{k[0]:<22} {k[1]:>5s}  {d['ret']:>+7.2f}%  {wr:>5.1f}%  {d['n']:>5d}  {d['dd']:>5.2f}%")
    
    # Per-symbol breakdown for each agent's best TF
    print(f"\n{'=' * 70}")
    print("PER-AGENT BEST TF — per-symbol breakdown")
    print(f"{'=' * 70}")
    for aname, _ in SCALP_SPECS:
        ar = [r for r in all_results if r["agent"] == aname and r["total_trades"] > 0]
        if not ar:
            continue
        best = max(ar, key=lambda r: r["total_return_pct"])
        best_tf = best["timeframe"]
        syms = [r for r in ar if r["timeframe"] == best_tf]
        total_ret = sum(s["total_return_pct"] for s in syms)
        print(f"\n  {aname:<22} [{best_tf}] combined: {total_ret:>+7.2f}%")
        for s in sorted(syms, key=lambda r: r["symbol"]):
            print(f"    {s['symbol']:<12} {s['total_return_pct']:>+8.2f}%  "
                  f"WR={s['win_rate']:>5.1f}%  {s['total_trades']:>4d}t  DD={s['max_drawdown_pct']:>5.2f}%")
    
    print(f"\nEnd: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
