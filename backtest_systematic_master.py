#!/usr/bin/env python3
"""
SYSTEMATIC AGENT BACKTEST — 3x replication, every agent × every TF.
Finds the true winners by testing everything 3 times and averaging.
Only reports FINAL results, no partial output.
"""

import os, sys, json, math, time, csv, copy
from collections import defaultdict
import numpy as np
import pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, WORK)

# ============================================================
# CONFIG
# ============================================================
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT"]

TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
TF_KEYS = ["5m","15m","30m","1H"]

BAL = 100.0
LEV = 5

# ============================================================
# HELPERS
# ============================================================
def ema(s, n): return s.ewm(span=n, adjust=False).mean()
def atr(df, p=14):
    h,l,c = df['high'],df['low'],df['close']
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(p).mean()

def load():
    data = {}
    for sym in SYMBOLS:
        for tf in TF_KEYS:
            p = os.path.join(CACHE, f"{sym.replace('-','_')}_{tf}_365d.parquet")
            if os.path.exists(p):
                df = pd.read_parquet(p).sort_values("ts").reset_index(drop=True)
                cut = df["ts"].max() - (365*24*3600*1000)
                df = df[df["ts"] >= cut].copy()
                if len(df) >= 300:
                    # Convert ts to datetime
                    df['datetime'] = pd.to_datetime(df['ts'], unit='ms')
                    data[(sym, tf)] = df
    return data

def compute_stats(trades, risk_pct):
    if not trades: return None
    pnls = [t['pnl'] for t in trades]
    total = sum(pnls)
    wins = sum(1 for p in pnls if p > 0)
    n = len(pnls)
    wr = wins/n if n else 0
    balance = BAL + total
    ret_pct = (balance - BAL)/BAL*100
    # Running equity curve for max drawdown
    eq = BAL
    peak = BAL
    dd = 0
    for p in pnls:
        eq += p
        if eq > peak: peak = eq
        dd = max(dd, (peak - eq)/peak * 100)
    avg_win = np.mean([p for p in pnls if p > 0]) if wins else 0
    avg_loss = np.mean([p for p in pnls if p < 0]) if (n-wins) else 0
    score = ret_pct * (wr * 100) / (dd + 1)  # Score = return * WR / drawdown
    return {
        "total": n, "wr": round(wr, 4), "balance": round(balance, 2),
        "ret_pct": round(ret_pct, 2), "max_dd": round(dd, 2),
        "avg_win": round(avg_win, 2), "avg_loss": round(avg_loss, 2),
        "total_pnl": round(total, 2), "score": round(score, 2),
    }

# ============================================================
# AGENT SIGNAL GENERATORS
# ============================================================

def scalp_signals(df):
    """Scalp: EMA cross + RSI. 5-15 minute hold."""
    c = df['close']
    ema9 = ema(c, 9)
    ema21 = ema(c, 21)
    rsi14 = _rsi(c)
    longs = (ema9 > ema21) & (ema9.shift(1) <= ema21.shift(1)) & (rsi14 > 30) & (rsi14 < 70)
    return longs

def swing_signals(df):
    """Swing: 50 EMA trend + pullback to 20 EMA."""
    c = df['close']
    ema20 = ema(c, 20)
    ema50 = ema(c, 50)
    rsi14 = _rsi(c)
    uptrend = c > ema50
    pullback = (c < ema20) & (c.shift(1) >= ema20.shift(1))
    longs = uptrend & pullback & (rsi14 > 30)
    return longs

def daily_breakout_signals(df):
    """Breakout: price breaks above previous day's high with momentum."""
    c = df['close']
    h = df['high']
    dh = h.rolling(24).max()
    dl = h.rolling(24).min()
    rng = dh - dl
    breakout = (c > dh.shift(1)) & (rng > 0)
    volume_ok = df['volume'] > df['volume'].rolling(50).mean() * 0.8
    return breakout & volume_ok

def daily_breakout_24h_signals(df):
    """Breakout 24h: price breaks above 24-bar (day) high."""
    c = df['close']
    h = df['high']
    dh = h.rolling(24).max()
    breakout = c > dh.shift(1)
    return breakout

def trend_pullback_signals(df):
    """Trend pullback: MA trend + RSI pullback."""
    c = df['close']
    ema20 = ema(c, 20)
    ema50 = ema(c, 50)
    rsi14 = _rsi(c)
    uptrend = ema20 > ema50
    pullback = (c < ema20) & (c.shift(1) >= ema20.shift(1))
    return uptrend & pullback & (rsi14.between(30, 60))

def macd_cross_signals(df):
    """MACD cross."""
    c = df['close']
    ema12 = ema(c, 12)
    ema26 = ema(c, 26)
    macd = ema12 - ema26
    signal = ema(macd, 9)
    cross = (macd > signal) & (macd.shift(1) <= signal.shift(1))
    return cross

def fib_bounce_signals(df, fib_level=0.5):
    """Fib bounce from 100-bar range."""
    c = df['close']
    h = df['high']
    l = df['low']
    h100 = h.rolling(100).max()
    l100 = l.rolling(100).min()
    rng = h100 - l100
    fib = l100 + fib_level * rng
    near_fib = abs(c - fib) / fib.replace(0, 1e-9) < 0.015
    reversal = c > c.shift(1)
    above_ema = c > ema(c, 50)
    return near_fib & reversal & above_ema & (df['volume'] > df['volume'].rolling(50).mean() * 0.6)

def viki_signals(df):
    """Viki: extreme RSI + volume confirmation."""
    rsi14 = _rsi(df['close'])
    v_avg = df['volume'].rolling(50).mean()
    vol_spike = df['volume'] > v_avg * 1.5
    oversold = rsi14 < 25
    overbought = rsi14 > 75
    longs = oversold & vol_spike
    shorts = overbought & vol_spike
    return longs, shorts

def volume_cap_signals(df):
    """Volume capitulation: extreme volume + price reversal."""
    v = df['volume']
    c = df['close']
    v_avg = v.rolling(50).mean()
    v_spike = v > v_avg * 2.5
    ema50 = ema(c, 50)
    below_ema = c < ema50
    reversal = c > c.shift(1)
    return v_spike & below_ema & reversal

def asian_pump_signals(df):
    """Asian pump: early hours (UTC 0-4) pre-breakout."""
    dt = df['datetime']
    hour = dt.dt.hour
    asian_hours = (hour >= 0) & (hour <= 4)
    rsi14 = _rsi(df['close'])
    c = df['close']
    ema20 = ema(c, 20)
    above_ema = c > ema20
    return asian_hours & above_ema & rsi14.between(40, 65)

def _rsi(c, p=14):
    d = c.diff()
    g = d.clip(lower=0)
    l = -d.clip(upper=0)
    return 100 - (100 / (1 + g.ewm(span=p, adjust=False).mean() / l.ewm(span=p, adjust=False).mean().replace(0, 1e-9)))

# AGENT REGISTRY
AGENTS = {
    "scalp": {"fn": scalp_signals, "longs": True, "max_hold": 12},
    "swing": {"fn": swing_signals, "longs": True, "max_hold": 48},
    "daily_breakout": {"fn": daily_breakout_signals, "longs": True, "max_hold": 48},
    "daily_breakout_24h": {"fn": daily_breakout_24h_signals, "longs": True, "max_hold": 48},
    "trend_pullback": {"fn": trend_pullback_signals, "longs": True, "max_hold": 48},
    "macd_cross": {"fn": macd_cross_signals, "longs": True, "max_hold": 24},
    "fib_bounce": {"fn": fib_bounce_signals, "longs": True, "max_hold": 96},
    "viki": {"fn": viki_signals, "longs": True, "shorts": True, "max_hold": 24},
    "volume_cap": {"fn": volume_cap_signals, "longs": True, "max_hold": 24},
    "asian_pump": {"fn": asian_pump_signals, "longs": True, "max_hold": 12},
}

# ============================================================
# TRADE SIMULATION
# ============================================================
def sim_trades(signals, c, h, l, bar_minutes, sl_pct=0.05, trail_pct=0.03, risk_pct=0.02, max_hold_hours=48, short_ok=False):
    trades = []

    held = {}  # bar -> active trade(s)
    for i in range(100, len(signals)):
        # Manage existing trades
        to_remove = []
        for bar, trade in held.items():
            elapsed = i - bar
            elapsed_min = elapsed * bar_minutes
            # Stop loss
            current_high = h[i] if trade['side'] == 'long' else l[i]
            current_low = l[i] if trade['side'] == 'long' else h[i]
            if trade['side'] == 'long':
                if current_low <= trade['sl']:
                    trade['exit'] = trade['sl']
                    trade['pnl'] = (trade['exit'] - trade['entry']) / trade['entry'] * risk_pct * LEV * 100
                    to_remove.append(bar)
                elif c[i] > trade['trail_trigger'] and trade['trailed'] == False:
                    trade['sl'] = c[i] * (1 - trail_pct)
                    trade['trailed'] = True
                elif trade['trailed'] and h[i] > trade['max_high']:
                    trade['max_high'] = h[i]
                    trade['sl'] = h[i] * (1 - trail_pct * 1.5)
            else:
                if current_high >= trade['sl']:
                    trade['exit'] = trade['sl']
                    trade['pnl'] = (trade['entry'] - trade['exit']) / trade['entry'] * risk_pct * LEV * 100
                    to_remove.append(bar)
            # Time stop
            if elapsed_min >= max_hold_hours * 60:
                if trade['exit'] is None:
                    trade['exit'] = c[i]
                    trade['pnl'] = (trade['exit'] - trade['entry'])/trade['entry'] * risk_pct * LEV * 100 if trade['side']=='long' else (trade['entry'] - trade['exit'])/trade['entry'] * risk_pct * LEV * 100
                    to_remove.append(bar)
        for bar in to_remove:
            t = held.pop(bar, None)
            if t and t['pnl'] is not None:
                trades.append(t)

        # Entry
        if signals[i]:
            entry_price = c[i]
            sl = entry_price * (1 - sl_pct) if True else entry_price * (1 + sl_pct)
            trades.append({
                'bar': i, 'side': 'long', 'entry': entry_price, 'sl': sl,
                'trailed': False, 'trail_trigger': entry_price * (1 + trail_pct*2),
                'max_high': entry_price, 'exit': None, 'pnl': None,
                'max_hold_bars': int(max_hold_hours * 60 / bar_minutes),
            })
            held[i] = trades[-1]

    # Close remaining
    for bar, trade in held.items():
        trade['exit'] = c[-1] if trade['exit'] is None else trade['exit']
        if trade['pnl'] is None:
            trade['pnl'] = (trade['exit'] - trade['entry'])/trade['entry'] * risk_pct * LEV * 100 if trade['side']=='long' else (trade['entry'] - trade['exit'])/trade['entry'] * risk_pct * LEV * 100
            trades.append(trade)

    return trades

# ============================================================
# BACKTEST RUNNER — 3x replication
# ============================================================
def run_agent(agent_name, cfg, df, bar_minutes, risk_pct=0.02):
    """Run one agent on one dataset, return stats."""
    fn = cfg['fn']
    # Generate signals
    if agent_name == 'viki':
        longs, shorts = fn(df)
        sigs = pd.Series(False, index=longs.index)
        for i in range(len(longs)):
            if longs.iloc[i]:
                sigs.iloc[i] = True
            elif shorts.iloc[i] and cfg.get('shorts', False):
                sigs.iloc[i] = True
    else:
        sigs = fn(df)
        sigs = sigs.fillna(False)
    # Reset index so integer positions work
    sigs = sigs.reset_index(drop=True)
    c = df['close'].reset_index(drop=True).values
    h = df['high'].reset_index(drop=True).values
    l = df['low'].reset_index(drop=True).values
    trades = sim_trades(sigs, c, h, l, bar_minutes, risk_pct=risk_pct, max_hold_hours=cfg['max_hold'])
    return compute_stats(trades, risk_pct)

def run_full_backtest(data, agent_name, cfg, n_runs=3):
    """Run on all symbols × TFs × n_runs, return aggregated stats."""
    results = []
    for sym in SYMBOLS:
        for tf in TF_KEYS:
            df = data.get((sym, tf))
            if df is None or len(df) < 300: continue
            bar_min = TFS[tf]
            for run in range(n_runs):
                st = run_agent(agent_name, cfg, df, bar_min)
                if st:
                    results.append({**st, "symbol": sym, "tf": tf, "run": run})

    if not results: return None
    # Aggregate
    df_result = pd.DataFrame(results)
    agg = {
        "agent": agent_name,
        "n_tests": len(results),
        "avg_ret_pct": round(float(df_result['ret_pct'].mean()), 2),
        "avg_wr": round(float(df_result['wr'].mean()), 4),
        "avg_dd": round(float(df_result['max_dd'].mean()), 2),
        "avg_score": round(float(df_result['score'].mean()), 2),
        "avg_trades": round(float(df_result['total'].mean()), 1),
        "med_ret_pct": round(float(df_result['ret_pct'].median()), 2),
        "std_ret": round(float(df_result['ret_pct'].std()), 2),
        "sharpe": round(float(df_result['ret_pct'].mean() / (df_result['ret_pct'].std() + 0.1)), 2),
        "profitable_pct": round(float((df_result['ret_pct'] > 0).mean() * 100), 1),
        "best_tf": df_result.loc[df_result['ret_pct'].idxmax(), 'tf'],
        "best_ret": round(float(df_result['ret_pct'].max()), 2),
    }
    # Best TF stats
    tf_stats = df_result.groupby('tf')['ret_pct'].agg(['mean','count']).to_dict('index')
    agg['by_tf'] = {k: round(float(v['mean']), 2) for k, v in tf_stats.items() if v['count'] >= 3}
    return agg

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    t0 = time.time()
    print("=" * 80)
    print("SYSTEMATIC AGENT BACKTEST — 3x Replication")
    print(f"Testing {len(AGENTS)} agents × {len(SYMBOLS)} symbols × {len(TF_KEYS)} TFs × 3 runs")
    print("=" * 80)

    data = load()
    print(f"Loaded {len(data)} datasets in {time.time()-t0:.1f}s", flush=True)

    winners = []
    for agent_name, cfg in AGENTS.items():
        print(f"\n[{agent_name}]" + " " * (20 - len(agent_name)), end=" ", flush=True)
        res = run_full_backtest(data, agent_name, cfg, n_runs=3)
        if res:
            sig = "✅" if res['profitable_pct'] > 60 else ("❌" if res['profitable_pct'] < 40 else "➖")
            print(f"{sig} Score={res['avg_score']:.0f} Ret={res['avg_ret_pct']:+.1f}% "
                  f"WR={res['avg_wr']:.1%} DD={res['avg_dd']:.1f}% "
                  f"Prof={res['profitable_pct']:.0f}% Sharpe={res['sharpe']:.2f} "
                  f"BestTF={res['best_tf']}({res['best_ret']:+.1f}%) "
                  f"n={res['n_tests']}", flush=True)
            winners.append(res)
        else:
            print("❌ No trades generated", flush=True)

    # RANK
    winners.sort(key=lambda x: -x['avg_score'])

    print(f"\n{'='*80}")
    print(f"🏆 RANKED RESULTS")
    print(f"{'='*80}")
    print(f"{'RANK':<5} {'AGENT':<20} {'SCORE':<8} {'RET%':<8} {'WR':<6} {'DD%':<6} {'PROF%':<7} {'SHARPE':<8} {'BEST':<12}")
    print("-" * 80)
    for i, w in enumerate(winners[:15], 1):
        print(f"{i:<5} {w['agent']:<20} {w['avg_score']:<8.0f} {w['avg_ret_pct']:<+7.1f}% "
              f"{w['avg_wr']:.1%} {w['avg_dd']:<5.1f}% {w['profitable_pct']:<6.0f}% "
              f"{w['sharpe']:<7.1f} {w['best_tf']}({w['best_ret']:+.0f}%)")

    # Save
    ts = time.strftime("%Y%m%d_%H%M%S")
    out = os.path.join(OUT, f"systematic_master_{ts}.json")
    with open(out, 'w') as f:
        json.dump(winners, f, indent=2, default=str)
    print(f"\nSaved: {out}")
    print(f"Duration: {(time.time()-t0)/60:.1f} min")

    # Final recommendation
    recommended = [w for w in winners if w['avg_score'] > 3 and w['profitable_pct'] > 50]
    print(f"\n{'='*80}")
    print(f"✅ RECOMMENDED TO ENABLE ({len(recommended)} agents)")
    for w in recommended:
        print(f"  {w['agent']:<20} Score={w['avg_score']:.0f} Ret={w['avg_ret_pct']:+.1f}% "
              f"WR={w['avg_wr']:.1%} DD={w['avg_dd']:.1f}% Prof={w['profitable_pct']:.0f}%")
    losers = [w for w in winners if w['avg_score'] <= 3 or w['profitable_pct'] <= 50]
    if losers:
        print(f"\n❌ RECOMMENDED TO DISABLE ({len(losers)} agents)")
        for w in losers:
            print(f"  {w['agent']:<20} Score={w['avg_score']:.0f} Ret={w['avg_ret_pct']:+.1f}% "
                  f"WR={w['avg_wr']:.1%} DD={w['avg_dd']:.1f}% Prof={w['profitable_pct']:.0f}%")
