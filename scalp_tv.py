#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""
SCALP BACKTEST v2 — Uses TradingView data (5000 bars 5m) not BloFin.
Tests the actual scalping agents on their real timeframes.
"""
import os, sys, json, math, time
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bot
from tv_data import candles

SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "HYPE-USDT"]

SCALP_SPECS = [
    ("liquidity_sweep",  bot.LiquiditySweepScalpAgent),
    ("wide_scalp",       bot.WideScalpAgent),
    ("utbot_mtf",        bot.UTBotMTFAgent),
    ("macd_cross",       bot.MACDCrossAgent),
    ("smart_scalp",      bot.SmartScalpAgent),
    ("quick_scalp",      bot.QuickScalp1HAgent),
    ("fib_confluence",   bot.FibConfluenceZoneAgent),
    ("fib_bounce",       bot.FibBounceAgent),
    ("turtle_breakout",  bot.TurtleBreakoutAgent),
    ("livermore_pivot",  bot.LivermorePivotAgent),
]

TIMEFRAMES = ["5m", "15m", "30m", "1H"]
MAX_BARS = 5000
WARMUP = 500
MIN_CONFIDENCE = 6
MAX_HOLD = 96

TF_STRIDE = {"5m": 1, "15m": 3, "30m": 6, "1H": 12}

def resample(df, chunk):
    df = df.copy()
    df["_g"] = np.arange(len(df)) // chunk
    return df.groupby("_g").agg({"ts":"first","open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna().reset_index(drop=True)

class TradeSim:
    def __init__(self, entry_price, side):
        self.entry = entry_price
        self.side = side
        self.sl = entry_price * 0.98 if side == "long" else entry_price * 1.02
        self.peak = entry_price
        self.trailing = False
    
    def step(self, h, l, c):
        if self.side == "long":
            if l <= self.sl: return "stop", self.sl
            if c > self.peak: self.peak = c
            if not self.trailing and c >= self.entry * 1.01:
                self.trailing = True
            if self.trailing:
                ns = self.peak * 0.99
                if ns > self.sl: self.sl = ns
                if l <= self.sl: return "trail", self.sl
        else:
            if h >= self.sl: return "stop", self.sl
            if c < self.peak: self.peak = c
            if not self.trailing and c <= self.entry * 0.99:
                self.trailing = True
            if self.trailing:
                ns = self.peak * 1.01
                if ns < self.sl: self.sl = ns
                if h >= self.sl: return "trail", self.sl
        return None, None

def sim_agent_on_tf(agent, sym, df_tf, stride, tf_name):
    c = df_tf["close"].values; h = df_tf["high"].values
    l = df_tf["low"].values; v = df_tf["volume"].values
    n = len(df_tf)
    trades = []
    
    for i in range(WARMUP, n - 10, 3):
        ctx_df = df_tf.iloc[:i+1].copy().reset_index(drop=True)
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
            ts = TradeSim(c[i], sig.side)
            for j in range(i+1, min(i+MAX_HOLD, n)):
                reason, ex = ts.step(h[j], l[j], c[j])
                if reason:
                    pnl = ((ex - ts.entry)/ts.entry*100 - 0.04) if ts.side == "long" else \
                          ((ts.entry - ex)/ts.entry*100 - 0.04)
                    trades.append(pnl)
                    break
    
    return trades

print("=" * 70)
print("SCALP BACKTEST v2 — TradingView data (5000 bars)")
print(f"  Agents: {len(SCALP_SPECS)}, TFs: {len(TIMEFRAMES)}, Symbols: {len(SYMBOLS)}")
print("=" * 70)

# Per-agent best TF (from earlier analysis)
AGENT_TF = {
    "liquidity_sweep": "30m",
    "wide_scalp": "1H",
    "utbot_mtf": "5m",
    "macd_cross": "15m",
    "smart_scalp": "5m",
    "quick_scalp": "1H",
    "fib_confluence": "1H",
    "fib_bounce": "1H",
    "turtle_breakout": "1H",
    "livermore_pivot": "1H",
}

for name, agent_cls in SCALP_SPECS:
    agent = agent_cls()
    best_tf = AGENT_TF.get(name, "1H")
    
    print(f"\n{'─'*60}")
    print(f"  {name} [best TF: {best_tf}]")
    print(f"{'─'*60}")
    
    for sym in SYMBOLS:
        df = candles(sym, best_tf, MAX_BARS)
        if df.empty:
            print(f"  {sym:10s} ✗ No data")
            continue
        
        # Resample if needed
        stride = TF_STRIDE.get(best_tf, 12)
        
        trades = sim_agent_on_tf(agent, sym, df, stride, best_tf)
        
        if trades:
            wins = sum(1 for p in trades if p > 0)
            tot = sum(trades)
            wr = wins/len(trades)*100
            avg_r = tot/len(trades) if trades else 0
            print(f"  {sym:10s} {len(trades):4d}t  WR={wr:5.1f}%  ret={tot:+7.2f}%  avg={avg_r:+.2f}%")

print(f"\n{'='*70}")
print("DONE")
print(f"{'='*70}")
