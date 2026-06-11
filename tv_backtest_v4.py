#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
TRADINGVIEW BACKTEST v4 — DEFINITIVE.
All agents, 5 coins, 5000 bars TV data, proper position simulation.
"""
import os, sys, json
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot
from tv_data import candles

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

MIN_CONFIDENCE = 6
MAX_HOLD = 120  # 1H bars

class TradeSim:
    """Proper position simulation with trailing stop."""
    def __init__(self, entry_bar, side, entry_price, ctx):
        self.entry_bar = entry_bar
        self.side = side
        self.entry = entry_price
        self.sl = entry_price * 0.96 if side == "long" else entry_price * 1.04
        self.active_trail = False
    
    def update(self, high, low, close):
        if self.side == "long":
            # Hit SL?
            if low <= self.sl:
                return "stop", self.sl
            # Activate trailing after +1.5%
            if not self.active_trail and close >= self.entry * 1.015:
                self.active_trail = True
            if self.active_trail:
                new_sl = close * 0.985
                if new_sl > self.sl:
                    self.sl = new_sl
                if low <= self.sl:
                    return "trail", self.sl
        else:
            if high >= self.sl:
                return "stop", self.sl
            if not self.active_trail and close <= self.entry * 0.985:
                self.active_trail = True
            if self.active_trail:
                new_sl = close * 1.015
                if new_sl < self.sl:
                    self.sl = new_sl
                if high >= self.sl:
                    return "trail", self.sl
        return None, None

print("=" * 70)
print("TRADINGVIEW BACKTEST v4 — DEFINITIVE (5000 bars, proper sim)")
print(f"  Agents: {len(AGENT_SPECS)}, Symbols: {len(SYMBOLS)}")
print("=" * 70)

all_data = {sym: {} for sym in SYMBOLS}

for sym in SYMBOLS:
    print(f"\n{'─'*60}")
    print(f"  {sym}")
    print(f"{'─'*60}")
    
    df = candles(sym, "1H", 5000)
    if df.empty:
        print(f"  ✗ No data")
        continue
    
    print(f"  {len(df)} bars")
    
    for name, agent_cls in AGENT_SPECS:
        agent = agent_cls()
        if not agent.enabled:
            continue
        
        c = df["close"].values; h = df["high"].values
        l = df["low"].values; v = df["volume"].values
        n = len(df)
        
        trades = []
        
        for i in range(120, n - 10):
            ctx_df = df.iloc[:i+1].copy().reset_index(drop=True)
            ctx = bot.MarketContext(
                symbol=sym,
                df_5m=pd.DataFrame(), df_15m=pd.DataFrame(), df_30m=pd.DataFrame(),
                df_1h=ctx_df, funding_rate=0.0,
                orderbook={"bids":[],"asks":[]}, news_sentiment={},
                trend=bot.TrendState())
            
            try:
                sig = agent.analyze(sym, ctx)
            except:
                continue
            
            if sig and sig.confidence >= MIN_CONFIDENCE:
                t = TradeSim(i, sig.side, c[i], ctx)
                # Simulate forward
                for j in range(i+1, min(i+MAX_HOLD, n)):
                    reason, ex = t.update(h[j], l[j], c[j])
                    if reason:
                        pnl = ((ex - t.entry)/t.entry*100 - 0.04) if t.side == "long" else \
                              ((t.entry - ex)/t.entry*100 - 0.04)
                        trades.append({"entry":t.entry,"exit":ex,"pnl":pnl,"bars":j-i,"reason":reason})
                        break
                    elif j == min(i+MAX_HOLD, n) - 1:
                        pnl = ((c[j] - t.entry)/t.entry*100 - 0.04) if t.side == "long" else \
                              ((t.entry - c[j])/t.entry*100 - 0.04)
                        trades.append({"entry":t.entry,"exit":c[j],"pnl":pnl,"bars":j-i,"reason":"time"})
        
        if trades:
            pnls = [t["pnl"] for t in trades]
            wins = sum(1 for p in pnls if p > 0)
            tot = sum(pnls)
            wr = wins/len(trades)*100
            all_data[sym][name] = {"n":len(trades),"w":wins,"wr":round(wr,1),"ret":round(tot,2)}
            print(f"  {name:20s} {len(trades):4d}t  WR={wr:5.1f}%  ret={tot:+7.2f}%")

# SUMMARY
print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")

summary = defaultdict(lambda: {"trades":0,"wins":0,"pnl":0,"coins":0})
for sym, agents in all_data.items():
    for name, d in agents.items():
        summary[name]["trades"] += d["n"]
        summary[name]["wins"] += d["w"]
        summary[name]["pnl"] += d["ret"]
        summary[name]["coins"] += 1

ranked = sorted(summary.items(), key=lambda x: -x[1]["pnl"])
print(f"\n{'Agent':20s} {'Trades':>7s} {'WR%':>6s} {'Ret%':>8s} {'Coins':>5s}")
print("-" * 48)
for name, s in ranked:
    wr = s["wins"]/s["trades"]*100 if s["trades"] else 0
    print(f"{name:20s} {s['trades']:7d} {wr:5.1f}% {s['pnl']:+8.2f}% {s['coins']:4d}")

print(f"\n{'='*70}")
print("WINNERS ✅")
for name, s in ranked:
    if s["pnl"] > 0 and s["trades"] >= 5:
        wr = s["wins"]/s["trades"]*100
        print(f"  ✅ {name:20s} {s['trades']:4d}t  +{s['pnl']:6.2f}%  WR={wr:.1f}%  {s['coins']}coins")

print(f"\nLOSERS ❌")
for name, s in ranked:
    if s["pnl"] <= 0 and s["trades"] >= 5:
        wr = s["wins"]/s["trades"]*100
        print(f"  ❌ {name:20s} {s['trades']:4d}t  {s['pnl']:7.2f}%  WR={wr:.1f}%")

# Save to JSON
output = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "config": {"symbols": SYMBOLS, "agents": len(AGENT_SPECS), "bars": 5000},
    "summary": {k: dict(v) for k, v in summary.items()},
    "detail": all_data
}
with open("tv_backtest_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\n✅ Saved to tv_backtest_results.json")
print(f"Finished: {datetime.now(timezone.utc).isoformat()}")
