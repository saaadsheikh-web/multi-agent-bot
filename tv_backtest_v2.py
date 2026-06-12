#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
TRADINGVIEW BACKTEST V2 — 9 LIVE AGENTS × ALL TFs × 5 COINS.
Uses the same data pipeline as tv_full_backtest.py but only tests
the agents we actually have enabled (after the 2026-06-11 cleanup).

Output: tv_backtest_v2_results.json
"""
import os, sys, json, math, time, traceback
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot
from tv_data import candles, _resample_ohlcv

# ── CONFIG ──
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "HYPE-USDT"]

# Only the agents we actually have enabled (2026-06-11 cleanup)
ALL_AGENTS = [
    ("asymmetric",          bot.AsymmetricBreakoutAgent),
    ("daily_breakout_24h",  bot.DailyBreakout24hAgent),
    ("daily_breakout_12h",  bot.DailyBreakout12hAgent),
    ("daily_breakout_48h",  bot.DailyBreakout48hAgent),
    ("macd_cross",          bot.MACDCrossAgent),
    ("fib_confluence",      bot.FibConfluenceZoneAgent),
    ("fib_bounce",          bot.FibBounceAgent),
    ("livermore_pivot",     bot.LivermorePivotAgent),
    ("utbot_v3",            bot.UTBotV3Agent),
]

# TFs to test
TIMEFRAMES = ["5m", "15m", "30m", "1H", "2H", "4H", "8H", "12H", "24H"]

# Backtest params
MIN_CONFIDENCE = 3  # Match bot's MIN_CONFIDENCE (was 6 in v1 — too high)
MAX_HOLD_BARS = {
    "5m": 96, "15m": 48, "30m": 32,
    "1H": 48, "2H": 24, "4H": 12,
    "8H": 8, "12H": 6, "24H": 4
}
WARMUP = {"5m": 200, "15m": 100, "30m": 80, "1H": 60, "2H": 60,
          "4H": 60, "8H": 60, "12H": 60, "24H": 60}

# Fee per side
FEE = 0.0004  # 0.04% per side (limit order maker fee)


# ── TRADE SIM ──
class TradeSim:
    def __init__(self, entry_idx, side, entry_price):
        self.entry_idx = entry_idx
        self.side = side
        self.entry = entry_price
        self.sl = entry_price * 0.97 if side == "long" else entry_price * 1.03
        self.high = entry_price
        self.low = entry_price
        self.active = False

    def update(self, high, low, close):
        if self.side == "long":
            self.high = max(self.high, high)
            self.low = min(self.low, low)
            if not self.active and close >= self.entry * 1.005:
                self.active = True
                self.sl = self.entry * 0.998
            if self.active:
                new_sl = close * 0.992
                if new_sl > self.sl:
                    self.sl = new_sl
            if low <= self.sl:
                return "trail", self.sl, ((self.sl - self.entry) / self.entry * 100 - FEE * 2)
        else:
            self.high = max(self.high, high)
            self.low = min(self.low, low)
            if not self.active and close <= self.entry * 0.995:
                self.active = True
                self.sl = self.entry * 1.002
            if self.active:
                new_sl = close * 1.008
                if new_sl < self.sl:
                    self.sl = new_sl
            if high >= self.sl:
                return "trail", self.sl, ((self.entry - self.sl) / self.entry * 100 - FEE * 2)
        return None, None, None


# ── FETCH TV DATA ──
def fetch_tv_data(symbol):
    """Fetch 1H and 5m from TradingView, resample to all TFs."""
    data = {}
    print(f"  Fetching {symbol}...", flush=True)
    df1h = candles(symbol, "1H", 5000)
    if df1h.empty:
        print(f"  ✗ No 1H data for {symbol}", flush=True)
        return None
    data["1H"] = df1h
    print(f"    ✓ 1H: {len(df1h)} bars", flush=True)

    for tf, ch in [("2H", 2), ("4H", 4), ("8H", 8), ("12H", 12), ("24H", 24)]:
        data[tf] = _resample_ohlcv(df1h, ch)
        print(f"    ✓ {tf}: {len(data[tf])} bars", flush=True)

    df5m = candles(symbol, "5m", 5000)
    if df5m.empty:
        print(f"    ✗ No 5m data for {symbol}", flush=True)
    else:
        data["5m"] = df5m
        print(f"    ✓ 5m: {len(df5m)} bars", flush=True)
        data["15m"] = _resample_ohlcv(df5m, 3)
        data["30m"] = _resample_ohlcv(df5m, 6)
        print(f"    ✓ 15m: {len(data['15m'])} bars", flush=True)
        print(f"    ✓ 30m: {len(data['30m'])} bars", flush=True)
    return data


# ── BUILD MARKET CONTEXT ──
def build_ctx(symbol, data, tf, idx):
    df = data[tf].iloc[:idx+1].copy().reset_index(drop=True)

    df_5m = pd.DataFrame()
    df_15m = pd.DataFrame()
    df_30m = pd.DataFrame()
    df_1h = pd.DataFrame()

    if tf in ("5m", "15m", "30m"):
        df_5m = df if tf == "5m" else data.get("5m", pd.DataFrame()).iloc[:idx*3].copy().reset_index(drop=True) if "5m" in data else pd.DataFrame()
        df_15m = df if tf == "15m" else data.get("15m", pd.DataFrame())
        df_30m = df if tf == "30m" else data.get("30m", pd.DataFrame())
        df_1h = data.get("1H", pd.DataFrame()).iloc[:max(1, idx//12)].copy().reset_index(drop=True) if "1H" in data else pd.DataFrame()
    else:
        df_1h = df if tf == "1H" else data.get("1H", pd.DataFrame()).iloc[:idx*2].copy().reset_index(drop=True) if "1H" in data else pd.DataFrame()

    return bot.MarketContext(
        symbol=symbol,
        df_5m=df_5m, df_15m=df_15m, df_30m=df_30m,
        df_1h=df_1h if not df_1h.empty else df,
        funding_rate=0.0,
        orderbook={"bids": [], "asks": []},
        news_sentiment={},
        trend=bot.TrendState()
    )


# ── BACKTEST ONE (AGENT, TF, SYMBOL) ──
def backtest_one(agent_cls, name, tf, symbol, data):
    agent = agent_cls()
    df = data[tf]
    n = len(df)
    warmup = WARMUP.get(tf, 60)
    max_bars = MAX_HOLD_BARS.get(tf, 48)

    if n < warmup + 10:
        return {"agent": name, "timeframe": tf, "symbol": symbol,
                "total_trades": 0, "wins": 0, "losses": 0, "total_return_pct": 0,
                "win_rate": 0, "max_drawdown_pct": 0}

    trades = []
    equity = 1000.0
    peak = equity
    max_dd = 0.0

    for i in range(warmup, n - max_bars):
        try:
            ctx = build_ctx(symbol, data, tf, i)
            sig = agent.analyze(symbol, ctx)
        except Exception:
            continue

        if sig is None or sig.confidence < MIN_CONFIDENCE:
            continue

        entry_price = df.iloc[i]["close"]
        t = TradeSim(i, sig.side, entry_price)

        for j in range(i + 1, min(i + max_bars, n)):
            bar = df.iloc[j]
            reason, exit_price, pnl = t.update(bar["high"], bar["low"], bar["close"])
            if reason:
                trades.append({
                    "entry": entry_price,
                    "exit": exit_price,
                    "pnl": pnl,
                    "bars_held": j - i,
                    "reason": reason,
                    "side": sig.side
                })
                equity += pnl
                break

    if not trades:
        return {"agent": name, "timeframe": tf, "symbol": symbol,
                "total_trades": 0, "wins": 0, "losses": 0, "total_return_pct": 0,
                "win_rate": 0, "max_drawdown_pct": 0}

    returns = [t["pnl"] for t in trades]
    wins = sum(1 for r in returns if r > 0)
    total_return = sum(returns)

    running = 0.0
    peak_r = 0.0
    max_dd = 0.0
    for r in returns:
        running += r
        if running > peak_r:
            peak_r = running
        dd = peak_r - running
        if dd > max_dd:
            max_dd = dd

    return {
        "agent": name,
        "timeframe": tf,
        "symbol": symbol,
        "total_trades": len(trades),
        "wins": wins,
        "losses": len(trades) - wins,
        "total_return_pct": round(total_return, 2),
        "win_rate": round(wins / len(trades) * 100, 1) if trades else 0,
        "max_drawdown_pct": round(max_dd, 2),
    }


# ── MAIN ──
def main():
    print("=" * 70, flush=True)
    print("TRADINGVIEW BACKTEST V2 — 9 LIVE AGENTS × ALL TFs × 5 COINS", flush=True)
    print(f"  Agents: {len(ALL_AGENTS)}, TFs: {len(TIMEFRAMES)}, Symbols: {len(SYMBOLS)}", flush=True)
    print(f"  Total combos: {len(ALL_AGENTS) * len(TIMEFRAMES) * len(SYMBOLS)}", flush=True)
    print(f"  MIN_CONFIDENCE={MIN_CONFIDENCE} (matches bot runtime)", flush=True)
    print("=" * 70, flush=True)
    print(f"Start: {datetime.now(timezone.utc).isoformat()}", flush=True)

    all_results = []

    for symbol in SYMBOLS:
        print(f"\n{'─' * 60}", flush=True)
        print(f"SYMBOL: {symbol}", flush=True)
        print(f"{'─' * 60}", flush=True)

        data = fetch_tv_data(symbol)
        if data is None:
            print(f"  ✗ Skipping {symbol} — no data", flush=True)
            continue

        for name, agent_cls in ALL_AGENTS:
            print(f"\n  {name}:", flush=True)
            for tf in TIMEFRAMES:
                if tf not in data:
                    continue

                try:
                    result = backtest_one(agent_cls, name, tf, symbol, data)
                except Exception as e:
                    print(f"    ERROR {tf}: {e}", flush=True)
                    traceback.print_exc()
                    continue

                all_results.append(result)
                n = result["total_trades"]
                r = result["total_return_pct"]
                w = result["win_rate"]
                dd = result["max_drawdown_pct"]

                if n > 0:
                    print(f"    {tf:>5s}: {n:4d}t  ret={r:>+8.2f}%  WR={w:>5.1f}%  DD={dd:>5.2f}%", flush=True)

    # ── Save ──
    output = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbols": SYMBOLS,
            "agents": [a[0] for a in ALL_AGENTS],
            "timeframes": TIMEFRAMES,
            "source": "TradingView",
            "bars": 5000,
        },
        "results": all_results,
    }
    out_path = "/Users/saad/multi_agent_bot/tv_backtest_v2_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n{'=' * 70}", flush=True)
    print(f"Saved to {out_path}", flush=True)
    print(f"  {len(all_results)} entries", flush=True)

    # ── SUMMARY ──
    print(f"\n{'=' * 70}", flush=True)
    print("AGENT × TF SUMMARY (aggregated across 5 coins)", flush=True)
    print(f"{'=' * 70}", flush=True)

    agg = defaultdict(lambda: {"ret": 0.0, "w": 0, "l": 0, "n": 0, "dd": 0.0})
    for r in all_results:
        if r["total_trades"] == 0:
            continue
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
        wr = d["w"] / d["n"] * 100
        print(f"{k[0]:<22} {k[1]:>5s}  {d['ret']:>+7.2f}%  {wr:>5.1f}%  {d['n']:>5d}  {d['dd']:>5.2f}%")

    # ── WINNERS ──
    print(f"\n{'=' * 70}", flush=True)
    print("WINNERS ✅ (ret > 0, ≥10 trades)", flush=True)
    print(f"{'=' * 70}", flush=True)
    for k in sorted_k:
        d = agg[k]
        if d["ret"] > 0 and d["n"] >= 10:
            wr = d["w"] / d["n"] * 100
            print(f"  ✅ {k[0]:<22} {k[1]:>5s}  +{d['ret']:>6.2f}%  WR={wr:.1f}%  {d['n']:>4d}t  DD={d['dd']:.1f}%")

    # ── LOSERS ──
    print(f"\n{'=' * 70}", flush=True)
    print("LOSERS ❌ (ret ≤ 0, ≥10 trades)", flush=True)
    for k in sorted_k:
        d = agg[k]
        if d["ret"] <= 0 and d["n"] >= 10:
            wr = d["w"] / d["n"] * 100
            print(f"  ❌ {k[0]:<22} {k[1]:>5s}  {d['ret']:>+7.2f}%  WR={wr:.1f}%  {d['n']:>4d}t  DD={d['dd']:.1f}%")

    # ── PER-AGENT BEST TF ──
    print(f"\n{'=' * 70}", flush=True)
    print("PER-AGENT BEST TF — per-symbol breakdown", flush=True)
    print(f"{'=' * 70}", flush=True)
    for aname, _ in ALL_AGENTS:
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

    print(f"\nEnd: {datetime.now(timezone.utc).isoformat()}", flush=True)


if __name__ == "__main__":
    main()
