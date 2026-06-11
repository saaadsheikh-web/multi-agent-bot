#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""BACKTEST COMPARISON — BloFin results vs TradingView results.
Uses PROPER ATR-based stops matching the real bot's execution."""
import os, sys, json
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

MIN_CONF = 6
MAX_HOLD = 120

def run_atr(name, agent_cls, sym, df, primary_tf):
    """Simulate with PROPER ATR-based stop (matches real bot)."""
    agent = agent_cls()
    if not agent.enabled:
        return None
    
    c = df["close"].values; h = df["high"].values
    l = df["low"].values; v = df["volume"].values
    n = len(df)
    
    # Calculate ATR
    pc = pd.Series(c).shift(1)
    tr = pd.concat([
        (pd.Series(h) - pd.Series(l)).abs(),
        (pd.Series(h) - pc).abs(),
        (pd.Series(l) - pc).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().values
    
    warmup = 200 if primary_tf == "5m" else 120
    trades = []
    
    for i in range(warmup, n - 10, 3):  # Check every 3 bars
        if np.isnan(atr[i]) or atr[i] <= 0:
            continue
        
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
            entry = c[i]
            # ATR-based stop (1.5× ATR)
            sl_dist = atr[i] * 1.5
            sl = entry - sl_dist if sig.side == "long" else entry + sl_dist
            
            # Also add a tight 2% stop as backup
            tight_sl = entry * 0.98 if sig.side == "long" else entry * 1.02
            sl = max(sl, tight_sl) if sig.side == "long" else min(sl, tight_sl)
            
            # TP = 3× ATR
            tp_dist = atr[i] * 4.5
            tp = entry + tp_dist if sig.side == "long" else entry - tp_dist
            
            # Simulate
            trail_active = False
            peak = entry
            
            for j in range(i+1, min(i+MAX_HOLD, n)):
                if sig.side == "long":
                    if l[j] <= sl:
                        pnl = (sl - entry)/entry*100 - 0.04
                        trades.append({"pnl":pnl, "reason":"sl", "bars":j-i})
                        break
                    if h[j] >= tp:
                        pnl = (tp - entry)/entry*100 - 0.04
                        trades.append({"pnl":pnl, "reason":"tp", "bars":j-i})
                        break
                    if c[j] > peak: peak = c[j]
                    if not trail_active and c[j] >= entry * (1 + atr[i]/entry):
                        trail_active = True
                    if trail_active:
                        ns = peak - atr[i]
                        if ns > sl: sl = ns
                        if l[j] <= sl:
                            pnl = (sl - entry)/entry*100 - 0.04
                            trades.append({"pnl":pnl, "reason":"trail", "bars":j-i})
                            break
                else:
                    if h[j] >= sl:
                        pnl = (entry - sl)/entry*100 - 0.04
                        trades.append({"pnl":pnl, "reason":"sl", "bars":j-i})
                        break
                    if l[j] <= tp:
                        pnl = (entry - tp)/entry*100 - 0.04
                        trades.append({"pnl":pnl, "reason":"tp", "bars":j-i})
                        break
                    if c[j] < peak: peak = c[j]
                    if not trail_active and c[j] <= entry * (1 - atr[i]/entry):
                        trail_active = True
                    if trail_active:
                        ns = peak + atr[i]
                        if ns < sl: sl = ns
                        if h[j] >= sl:
                            pnl = (entry - sl)/entry*100 - 0.04
                            trades.append({"pnl":pnl, "reason":"trail", "bars":j-i})
                            break
            else:
                exit_p = c[min(i+MAX_HOLD, n)-1]
                pnl = ((exit_p - entry)/entry*100 - 0.04) if sig.side == "long" else \
                      ((entry - exit_p)/entry*100 - 0.04)
                trades.append({"pnl":pnl, "reason":"time", "bars":MAX_HOLD})
    
    return trades

# ── MAIN ──
print("=" * 70)
print("COMPARISON BACKTEST — ATR-based stops (matches real bot)")
print(f"  {len(AGENTS)} agents × {len(SYMBOLS)} symbols")
print("=" * 70)

results = {}

for sym in SYMBOLS:
    print(f"\n{'─'*50}")
    print(f"  {sym}")
    print(f"{'─'*50}")
    
    for name, agent_cls, primary_tf in AGENTS:
        df = candles(sym, primary_tf, 5000)
        if df.empty:
            continue
        
        trades = run_atr(name, agent_cls, sym, df, primary_tf)
        if trades and len(trades) >= 3:
            pnls = [t["pnl"] for t in trades]
            wins = sum(1 for p in pnls if p > 0)
            total = sum(pnls)
            wr = wins/len(pnls)*100
            
            # Breakdown by exit reason
            reasons = defaultdict(list)
            for t in trades:
                reasons[t["reason"]].append(t["pnl"])
            
            reason_str = " ".join(f"{k}={len(v)}" for k, v in reasons.items())
            
            results[(name, sym)] = {
                "trades": len(pnls), "wins": wins, "wr": round(wr,1),
                "ret": round(total,2), "avg": round(total/len(pnls),2),
                "reasons": {k: len(v) for k, v in reasons.items()}
            }
            
            print(f"  {name:20s} {len(pnls):4d}t  WR={wr:5.1f}%  ret={total:+7.2f}%  avg={total/len(pnls):+.2f}%  [{reason_str}]")
        else:
            print(f"  {name:20s}    0t (no signals)")

# FINAL SUMMARY
print(f"\n{'='*70}")
print("  FINAL SUMMARY — Aggregated across all symbols")
print(f"{'='*70}")

summary = defaultdict(lambda: {"trades":0,"wins":0,"pnl":0,"coins":0})
for (name, sym), d in results.items():
    summary[name]["trades"] += d["trades"]
    summary[name]["wins"] += d["wins"]
    summary[name]["pnl"] += d["ret"]
    summary[name]["coins"] += 1

ranked = sorted(summary.keys(), key=lambda n: -summary[n]["pnl"])
print(f"\n{'Agent':20s} {'Trades':>7s} {'WR%':>6s} {'Ret%':>8s} {'Coins':>5s}")
print("-" * 48)
for name in ranked:
    s = summary[name]
    wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
    print(f"{name:20s} {s['trades']:7d} {wr:5.1f}% {s['pnl']:+8.2f}% {s['coins']:4d}")

print(f"\n{'='*70}")
print("  WINNERS ✅ (profitable with ATR stops)")
for name in ranked:
    s = summary[name]
    if s["pnl"] > 0:
        wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
        print(f"  ✅ {name:20s} +{s['pnl']:6.2f}%  {s['trades']}t  WR={wr:.1f}%  {s['coins']}coins")

print(f"\n  BORDERLINE ⚠️ (small loss, may work with tuning)")
for name in ranked:
    s = summary[name]
    if 0 >= s["pnl"] > -100 and s["trades"] >= 5:
        wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
        print(f"  ⚠️ {name:20s} {s['pnl']:7.2f}%  {s['trades']}t  WR={wr:.1f}%")

print(f"\n  LOSERS ❌ (big loss — disable)")
for name in ranked:
    s = summary[name]
    if s["pnl"] <= -100:
        wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
        print(f"  ❌ {name:20s} {s['pnl']:7.2f}%  {s['trades']}t  WR={wr:.1f}%")

# Save
output = {
    "timestamp": __import__('datetime').datetime.now().isoformat(),
    "results": {(k[0],k[1]):v for k,v in results.items()},
    "summary": {k:dict(v) for k,v in summary.items()},
}
with open("tv_comparison_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\n  ✅ Saved to tv_comparison_results.json")
