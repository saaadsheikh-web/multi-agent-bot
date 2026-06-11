#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
ONE YEAR BACKTEST — ~365 days of 1H data, all 12 enabled agents × 9 TFs × 5 coins
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

AGENT_SPECS = [
    ("asymmetric",         bot.AsymmetricBreakoutAgent),
    ("daily_breakout",      bot.DailyRangeBreakoutAgent),
    ("daily_breakout_24h",  bot.DailyBreakout24hAgent),
    ("daily_breakout_4h",   bot.DailyBreakout4hAgent),
    ("daily_breakout_12h",  bot.DailyBreakout12hAgent),
    ("daily_breakout_48h",  bot.DailyBreakout48hAgent),
    ("liquidity_sweep",     bot.LiquiditySweepScalpAgent),
    ("wide_scalp",          bot.WideScalpAgent),
    ("utbot_mtf",           bot.UTBotMTFAgent),
    ("fib_confluence",      bot.FibConfluenceZoneAgent),
    ("fib_bounce",          bot.FibBounceAgent),
    ("macd_cross",          bot.MACDCrossAgent),
]

TIMEFRAMES = ["1H", "2H", "4H", "8H", "12H", "24H", "48H", "72H", "168H"]

MAX_BARS = 8760     # ~365 days of 1H
WARMUP = 480        # 20 days warmup

MIN_CONFIDENCE = 6
MAX_HOLD_BARS = 720

TF_CHUNKS = {
    "1H": 1, "2H": 2, "4H": 4, "8H": 8,
    "12H": 12, "24H": 24, "48H": 48, "72H": 72, "168H": 168,
}

AGENT_PRIMARY = {
    "asymmetric": "1H", "daily_breakout": "1H", "daily_breakout_24h": "1H",
    "daily_breakout_4h": "1H", "daily_breakout_12h": "1H", "daily_breakout_48h": "1H",
    "liquidity_sweep": "1H", "wide_scalp": "1H", "utbot_mtf": "1H",
    "fib_confluence": "1H", "fib_bounce": "1H", "macd_cross": "15m",
}


def resample_to_tf(df, chunk_size):
    df = df.copy()
    df["_g"] = np.arange(len(df)) // chunk_size
    return df.groupby("_g").agg({
        "ts": "first", "open": "first", "high": "max",
        "low": "min", "close": "last", "volume": "sum",
    }).dropna().reset_index(drop=True)


def fetch_data(symbol):
    # BloFin caps at ~1000 per call, so paginate using before/after
    CHUNK = 1000
    all_chunks = []
    after = str(int((datetime.now(timezone.utc).timestamp() - 366 * 86400) * 1000))
    
    for i in range(20):  # max 20k bars
        try:
            params = {"inst_id": symbol, "bar": "1H", "limit": CHUNK, "after": after}
            r = bf.client.public.get_candlesticks(**params)
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
        
        # Data comes newest-first. Sorted ascending: iloc[0] = oldest
        oldest_ts_raw = int(rows[-1][0])  # last raw row = oldest
        
        all_chunks.append(df_chunk)
        print(f"  ✓ Fetched {len(df_chunk)} bars: "
              f"{datetime.fromtimestamp(df_chunk['ts'].iloc[0]/1000).strftime('%Y-%m-%d')} → "
              f"{datetime.fromtimestamp(df_chunk['ts'].iloc[-1]/1000).strftime('%Y-%m-%d')} "
              f"(total: {sum(len(c) for c in all_chunks)})")
        
        after = str(int(oldest_ts_raw - 1))
        
        if sum(len(c) for c in all_chunks) >= MAX_BARS:
            break

    if not all_chunks:
        print(f"  ✗ No 1H data for {symbol}")
        return None

    df_1h = pd.concat(all_chunks, ignore_index=True)
    df_1h = df_1h.sort_values("ts").drop_duplicates(subset=["ts"]).reset_index(drop=True)
    if len(df_1h) > MAX_BARS:
        df_1h = df_1h.iloc[-MAX_BARS:].reset_index(drop=True)

    data = {"1H": df_1h}
    for tf, chunk in TF_CHUNKS.items():
        if tf == "1H":
            continue
        data[tf] = resample_to_tf(df_1h, chunk)
    return data


def build_context(symbol, all_data, idx_1h):
    dfh = all_data["1H"].iloc[:idx_1h+1].copy().reset_index(drop=True)
    ts_limit = dfh["ts"].iloc[-1]

    def _slice(name):
        df = all_data.get(name)
        if df is None or df.empty:
            return pd.DataFrame()
        return df[df["ts"] <= ts_limit].copy().reset_index(drop=True)

    trend = bot.TrendState()
    try:
        if len(dfh) >= 20:
            trend = bot.compute_trend_state(dfh)
    except Exception:
        pass

    return bot.MarketContext(
        symbol=symbol,
        df_5m=pd.DataFrame(), df_15m=pd.DataFrame(), df_30m=pd.DataFrame(),
        df_1h=dfh, funding_rate=0.0,
        orderbook={"bids": [], "asks": []}, news_sentiment={}, trend=trend,
    )


def simulate_trade(signal, df_future_1h, entry_idx):
    side = signal.side
    meta = signal.metadata or {}
    entry_price = float(df_future_1h.iloc[0]["open"])

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

    for i in range(1, len(df_future_1h)):
        bar = df_future_1h.iloc[i]
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
        exit_price = float(df_future_1h.iloc[-1]["close"])
        pnl_pct = (exit_price / entry_price - 1) * 100 if side == "long" else (1 - exit_price / entry_price) * 100
        trade_bars = len(df_future_1h) - 1

    return {
        "entry_price": entry_price, "sl_price": sl_price, "tp_price": tp_price,
        "exit_reason": reason, "pnl_pct": pnl_pct, "trade_bars": trade_bars,
        "side": side, "confidence": signal.confidence,
        "profile": signal.profile, "reason": signal.reason,
    }


def backtest_one(agent_cls, agent_name, tf, symbol, all_data):
    agent = agent_cls()
    df_1h = all_data["1H"]
    n_bars = len(df_1h)
    stride = TF_CHUNKS[tf]

    warmup = min(WARMUP, n_bars // 3)

    trades = []
    last_sig = None
    last_sig_idx = -9999
    min_gap = stride * 48

    for idx in range(warmup, n_bars):
        if idx % stride != 0:
            continue

        ctx = build_context(symbol, all_data, idx)

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

        future = df_1h.iloc[idx+1:min(idx+1+MAX_HOLD_BARS, n_bars)].copy().reset_index(drop=True)
        if len(future) < 2:
            continue

        result = simulate_trade(signal, future, idx)

        trades.append({
            "bar_idx": idx,
            "entry_ts": int(df_1h.iloc[idx]["ts"] / 1000),
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
    print(f"1-YEAR BACKTEST: {len(AGENT_SPECS)} agents × {len(TIMEFRAMES)} TFs × {len(SYMBOLS)} symbols")
    print(f"  {MAX_BARS} 1H bars (~365 days), {WARMUP} bar warmup")
    print(f"  Min confidence: {MIN_CONFIDENCE}")
    print("=" * 70)
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")
    sys.stdout.flush()

    all_results = []

    for symbol in SYMBOLS:
        print(f"\n{'─' * 60}")
        print(f"SYMBOL: {symbol}")
        sys.stdout.flush()

        data = fetch_data(symbol)
        if data is None:
            continue

        dfh = data["1H"]
        print(f"  ✓ {len(dfh)} 1H bars: "
              f"{datetime.fromtimestamp(dfh['ts'].iloc[0]/1000).strftime('%Y-%m-%d %H:%M')} → "
              f"{datetime.fromtimestamp(dfh['ts'].iloc[-1]/1000).strftime('%Y-%m-%d %H:%M')}")
        for tf in TIMEFRAMES:
            if tf in data:
                print(f"    {tf:>5s}: {len(data[tf])} bars")
        sys.stdout.flush()

        for agent_name, agent_cls in AGENT_SPECS:
            print(f"\n  {agent_name}:")
            sys.stdout.flush()
            for tf in TIMEFRAMES:
                if len(data.get(tf, pd.DataFrame())) < 5:
                    print(f"    [{tf:>5s}] SKIP (too few bars)")
                    continue
                print(f"    [{tf:>5s}] ", end="", flush=True)
                try:
                    result = backtest_one(agent_cls, agent_name, tf, symbol, data)
                except Exception as e:
                    print(f"ERROR: {e}", flush=True)
                    continue
                all_results.append(result)
                n = result["total_trades"]
                r = result["total_return_pct"]
                w = result["win_rate"]
                dd = result["max_drawdown_pct"]
                print(f"{n:4d}t  ret={r:>+8.2f}%  WR={w:>5.1f}%  DD={dd:>5.2f}%", flush=True)

    output = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbols": SYMBOLS,
            "agents": [a[0] for a in AGENT_SPECS],
            "timeframes": TIMEFRAMES,
            "max_bars": MAX_BARS,
            "warmup": WARMUP,
        },
        "results": all_results,
    }
    out_path = "/Users/saad/multi_agent_bot/one_year_backtest_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n{'=' * 70}")
    print(f"Saved to {out_path}")
    print(f"  {len(all_results)} entries ({len([r for r in all_results if r['total_trades'] > 0])} with trades)")

    # ── SUMMARY ──
    print(f"\n{'=' * 70}")
    print("SUMMARY — aggregated across all symbols")
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

    # Best per agent
    print(f"\n{'=' * 70}")
    print("BEST TF PER AGENT")
    print(f"{'=' * 70}")
    for aname, _ in AGENT_SPECS:
        ar = [r for r in all_results if r["agent"] == aname and r["total_trades"] > 0]
        if not ar:
            print(f"  {aname:<22} 0 trades on any TF")
            continue
        best = max(ar, key=lambda r: r["total_return_pct"])
        worst = min(ar, key=lambda r: r["total_return_pct"])
        print(f"  {aname:<22} BEST: {best['timeframe']:>5s} {best['total_return_pct']:>+7.2f}% "
              f"WR={best['win_rate']:>5.1f}% {best['total_trades']:>4d}t "
              f"| WORST: {worst['timeframe']:>5s} {worst['total_return_pct']:+.2f}%")

    # Per-symbol breakdown for each agent's best TF
    print(f"\n{'=' * 70}")
    print("PER-SYMBOL BREAKDOWN (each agent's best TF)")
    print(f"{'=' * 70}")
    for aname, _ in AGENT_SPECS:
        ar = [r for r in all_results if r["agent"] == aname and r["total_trades"] > 0]
        if not ar:
            continue
        best_tf = max(ar, key=lambda r: r["total_return_pct"])["timeframe"]
        syms = [r for r in ar if r["timeframe"] == best_tf]
        print(f"\n  {aname:<22} [{best_tf}]")
        for s in sorted(syms, key=lambda r: r["symbol"]):
            print(f"    {s['symbol']:<12} {s['total_return_pct']:>+8.2f}%  "
                  f"WR={s['win_rate']:>5.1f}%  {s['total_trades']:>4d}t  DD={s['max_drawdown_pct']:>5.2f}%")

    print(f"\nEnd: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
