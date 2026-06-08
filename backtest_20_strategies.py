#!/usr/bin/env python3
"""
20 STRATEGIES × 5 TIMEFRAMES × 10 COINS — Iterative Backtest
Finds the absolute best strategy/TF/coin combinations.
Explains WHY winners work and HOW to improve them.
"""

import os, sys, json, math, time as _time
from collections import defaultdict
import numpy as np
import pandas as pd

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")
OUTPUT_DIR = os.path.join(WORK_DIR, "backtest_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════
DAYS = 365
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT"]
TFS = ["5m","15m","30m","1H","4H"]
TF_MINUTES = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
STARTING_BALANCE = 100.0
LEVERAGE = 5
RISK_FRACTION = 0.10

# ═══════════════════════════════════════════════════════════════
# INDICATORS
# ═══════════════════════════════════════════════════════════════
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def sma(s, n):
    return s.rolling(n).mean()

def rsi(c, period=14):
    delta = c.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))

def adx(df, period=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr1 = h - l
    tr2 = (h - c.shift()).abs()
    tr3 = (l - c.shift()).abs()
    tr = pd.concat([tr1,tr2,tr3], axis=1).max(axis=1)
    up = h.diff(); down = l.shift() - l
    plus_dm = np.where((up > down) & (up > 0), up, 0)
    minus_dm = np.where((down > up) & (down > 0), down, 0)
    atr = pd.Series(tr).ewm(span=period, adjust=False).mean()
    plus_di = 100 * pd.Series(plus_dm).ewm(span=period, adjust=False).mean() / atr.replace(0, 1e-9)
    minus_di = 100 * pd.Series(minus_dm).ewm(span=period, adjust=False).mean() / atr.replace(0, 1e-9)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 1e-9)
    return pd.Series(dx).ewm(span=period, adjust=False).mean(), plus_di, minus_di

def atr(df, period=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()

def bollinger(c, period=20, std=2):
    mb = sma(c, period)
    sd = c.rolling(period).std()
    return mb + std*sd, mb, mb - std*sd

def pivot_highs(h, n=5):
    """Find pivot highs - peaks surrounded by n lower bars."""
    pivots = pd.Series(False, index=h.index)
    for i in range(n, len(h)-n):
        if h.iloc[i] == h.iloc[i-n:i+n+1].max():
            pivots.iloc[i] = True
    return pivots

def pivot_lows(l, n=5):
    pivots = pd.Series(False, index=l.index)
    for i in range(n, len(l)-n):
        if l.iloc[i] == l.iloc[i-n:i+n+1].min():
            pivots.iloc[i] = True
    return pivots


# ═══════════════════════════════════════════════════════════════
# 20 STRATEGIES
# ═══════════════════════════════════════════════════════════════
# Each returns: (long_signal, short_signal) — boolean Series

def strategy_signals(name, df):
    """Return (longs, shorts) boolean arrays for a named strategy."""
    c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]

    # Pre-compute common indicators
    e9, e21, e50 = ema(c,9), ema(c,21), ema(c,50)
    r = rsi(c)
    adx_val, plus_di, minus_di = adx(df)
    atr_val = atr(df)
    bb_upper, bb_mid, bb_lower = bollinger(c)
    v_avg20 = v.rolling(20).mean()
    v_ratio = v / v_avg20.replace(0, 1e-9)

    longs = pd.Series(False, index=df.index)
    shorts = pd.Series(False, index=df.index)

    if name == "1_ADX_BREAKOUT":
        # ADX>25 + price breaks 20-bar high with volume
        h20 = h.rolling(20).max().shift(1)
        l20 = l.rolling(20).min().shift(1)
        longs = (adx_val > 25) & (plus_di > minus_di) & (c > h20) & (v_ratio > 1.2)
        shorts = (adx_val > 25) & (minus_di > plus_di) & (c < l20) & (v_ratio > 1.2)

    elif name == "2_VOLUME_SURGE":
        # Volume 2x + directional move > 1 ATR
        longs = (v_ratio > 2.0) & (c > c.shift(1) * 1.005) & (c - c.shift(5) > atr_val)
        shorts = (v_ratio > 2.0) & (c < c.shift(1) * 0.995) & (c.shift(5) - c > atr_val)

    elif name == "3_FIB_BOUNCE":
        # Price near fib retrace of recent swing + reversal signal
        h50 = h.rolling(50).max()
        l50 = l.rolling(50).min()
        rng = h50 - l50
        fib382 = l50 + 0.382 * rng
        fib618 = l50 + 0.618 * rng
        near382 = (abs(c - fib382) / fib382.replace(1e-9, 1e-9)) < 0.01
        near618 = (abs(c - fib618) / fib618.replace(1e-9, 1e-9)) < 0.01
        reversal_up = (c > c.shift(1)) & (c.shift(1) < c.shift(2))
        reversal_down = (c < c.shift(1)) & (c.shift(1) > c.shift(2))
        longs = (near382 | near618) & reversal_up & (v_ratio > 1.0)
        shorts = ((abs(c - (h50 - 0.382*rng)) / h50.replace(1e-9,1e-9) < 0.01) |
                  (abs(c - (h50 - 0.618*rng)) / h50.replace(1e-9,1e-9) < 0.01)) & reversal_down & (v_ratio > 1.0)

    elif name == "4_EMA_STACK":
        # 3 EMAs aligned + price above/below + volume
        longs = (e9 > e21) & (e21 > e50) & (c > e9) & (v_ratio > 0.8)
        shorts = (e9 < e21) & (e21 < e50) & (c < e9) & (v_ratio > 0.8)

    elif name == "5_RANGE_EXPANSION":
        # ATR expanding 50%+ vs 20 bars ago + directional
        atr_expanding = atr_val > atr_val.shift(20) * 1.5
        longs = atr_expanding & (c > e21) & (v_ratio > 1.3)
        shorts = atr_expanding & (c < e21) & (v_ratio > 1.3)

    elif name == "6_PULLBACK_EMA":
        # In trend (above/below EMA50), price pulls back to EMA21
        trend_up = c.shift(3) > e50.shift(3)
        trend_down = c.shift(3) < e50.shift(3)
        pullback_up = trend_up & (abs(c - e21) / c < 0.01) & (c > c.shift(1))
        pullback_down = trend_down & (abs(c - e21) / c < 0.01) & (c < c.shift(1))
        longs = pullback_up & (v_ratio > 0.8)
        shorts = pullback_down & (v_ratio > 0.8)

    elif name == "7_BREAKOUT_FIB_CONFLUENCE":
        # Breakout through multiple fib levels + volume surge
        h100 = h.rolling(100).max()
        l100 = l.rolling(100).min()
        rng100 = h100 - l100
        fib50 = l100 + 0.5 * rng100
        break_above = (c.shift(1) < fib50) & (c > fib50)
        break_below = (c.shift(1) > fib50) & (c < fib50)
        longs = break_above & (v_ratio > 1.5) & (adx_val > 20)
        shorts = break_below & (v_ratio > 1.5) & (adx_val > 20)

    elif name == "8_VOLUME_CLIMAX":
        # Extreme volume + doji/reversal candle + RSI extreme
        vol_climax = v_ratio > 3.0
        doji = abs(c - c.shift(1)) / c.shift(1).replace(1e-9,1e-9) < 0.003
        longs = vol_climax & (r < 35) & (c > c.shift(1))
        shorts = vol_climax & (r > 65) & (c < c.shift(1))

    elif name == "9_ADX_RSI_COMBO":
        # ADX>30 trending + RSI 40-60 (not extreme) + EMA aligned
        longs = (adx_val > 30) & (r > 40) & (r < 60) & (e9 > e21) & (c > e9)
        shorts = (adx_val > 30) & (r > 40) & (r < 60) & (e9 < e21) & (c < e9)

    elif name == "10_TREND_FOLLOWING":
        # Higher highs/lows for 3 bars + volume confirming
        hh = (h > h.shift(1)) & (h.shift(1) > h.shift(2))
        hl = (l > l.shift(1)) & (l.shift(1) > l.shift(2))
        lh = (l < l.shift(1)) & (l.shift(1) < l.shift(2))
        ll = (h < h.shift(1)) & (h.shift(1) < h.shift(2))
        longs = hh & hl & (v_ratio > 1.0) & (e9 > e21)
        shorts = lh & ll & (v_ratio > 1.0) & (e9 < e21)

    elif name == "11_BB_SQUEEZE":
        # BB width < 5% + breakout with volume
        bb_width = (bb_upper - bb_lower) / bb_mid.replace(1e-9,1e-9)
        squeeze = bb_width < 0.05
        longs = squeeze & (c > bb_upper.shift(1)) & (v_ratio > 1.5)
        shorts = squeeze & (c < bb_lower.shift(1)) & (v_ratio > 1.5)

    elif name == "12_PIVOT_BREAKOUT":
        # Break above recent pivot high / below pivot low
        ph = pivot_highs(h, 5)
        pl = pivot_lows(l, 5)
        # Most recent pivot high/low
        recent_ph = h[ph].rolling(50, min_periods=1).max()
        recent_pl = l[pl].rolling(50, min_periods=1).min()
        longs = (c > recent_ph.shift(1)) & (v_ratio > 1.3) & (adx_val > 20)
        shorts = (c < recent_pl.shift(1)) & (v_ratio > 1.3) & (adx_val > 20)

    elif name == "13_MACD_CROSS":
        # MACD line crosses signal + trend filter
        macd_line = e9 - e21
        macd_signal = ema(pd.Series(e9 - e21), 9)
        cross_up = (macd_line > macd_signal) & (macd_line.shift(1) <= macd_signal.shift(1))
        cross_down = (macd_line < macd_signal) & (macd_line.shift(1) >= macd_signal.shift(1))
        longs = cross_up & (c > e50) & (v_ratio > 0.8)
        shorts = cross_down & (c < e50) & (v_ratio > 0.8)

    elif name == "14_OPENING_RANGE":
        # First 4 bars set range, breakout after
        # Use 24-bar rolling "opening range" (1 day worth)
        h_range = h.rolling(24).max().shift(1)
        l_range = l.rolling(24).min().shift(1)
        longs = (c > h_range) & (v_ratio > 1.5)
        shorts = (c < l_range) & (v_ratio > 1.5)

    elif name == "15_VWAP_REVERSION":
        # Price deviates 2%+ from VWAP, reverts back
        vwap = (c * v).rolling(48).sum() / v.rolling(48).sum().replace(1e-9,1e-9)
        dev = (c - vwap) / vwap.replace(1e-9,1e-9)
        longs = (dev < -0.02) & (r < 30) & (c > c.shift(1))
        shorts = (dev > 0.02) & (r > 70) & (c < c.shift(1))

    elif name == "16_MOMENTUM_BURST":
        # 3-bar momentum > 1.5% + volume + trend
        mom = (c - c.shift(3)) / c.shift(3).replace(1e-9,1e-9)
        longs = (mom > 0.015) & (v_ratio > 1.5) & (e9 > e50)
        shorts = (mom < -0.015) & (v_ratio > 1.5) & (e9 < e50)

    elif name == "17_SUPPORT_RESISTANCE":
        # Price bounces off S/R level (recent pivot) + confirmation
        r_levels = h[ph]
        s_levels = l[pl]
        near_resistance = any(abs(c - lvl) / lvl < 0.005 for lvl in r_levels.iloc[-10:] if not pd.isna(lvl)) if len(r_levels) > 0 else False
        near_support = any(abs(c - lvl) / lvl < 0.005 for lvl in s_levels.iloc[-10:] if not pd.isna(lvl)) if len(s_levels) > 0 else False
        longs = pd.Series(near_support, index=df.index) & (c > c.shift(1)) & (v_ratio > 1.0)
        shorts = pd.Series(near_resistance, index=df.index) & (c < c.shift(1)) & (v_ratio > 1.0)

    elif name == "18_DUAL_CONFIRMATION":
        # 2+ of: ADX>25, Volume>1.5x, EMA aligned, RSI 40-60
        cond1 = adx_val > 25
        cond2 = v_ratio > 1.5
        cond3 = (e9 > e21) & (e21 > e50)
        cond4 = (r > 40) & (r < 60)
        score = cond1.astype(int) + cond2.astype(int) + cond3.astype(int) + cond4.astype(int)
        longs = (score >= 3) & cond3
        shorts = (score >= 3) & (~cond3)

    elif name == "19_ATR_TRAIL_SETUP":
        # Entry based on ATR: price moves 2 ATR from open + trend
        o = df["open"]
        atr2 = atr_val * 2
        longs = (c - o > atr2) & (e9 > e50) & (v_ratio > 1.5)
        shorts = (o - c > atr2) & (e9 < e50) & (v_ratio > 1.5)

    elif name == "20_ENSEMBLE":
        # At least 3 of the top strategies agree
        # Use a few fast strategies
        s1_long = (adx_val > 25) & (plus_di > minus_di) & (c > h.rolling(20).max().shift(1))
        s2_long = (v_ratio > 2.0) & (c > c.shift(5))
        s3_long = (e9 > e21) & (e21 > e50) & (c > e9)
        s4_long = (r > 40) & (r < 60) & (c > e21)
        score_long = s1_long.astype(int)+s2_long.astype(int)+s3_long.astype(int)+s4_long.astype(int)

        s1_short = (adx_val > 25) & (minus_di > plus_di) & (c < l.rolling(20).min().shift(1))
        s2_short = (v_ratio > 2.0) & (c < c.shift(5))
        s3_short = (e9 < e21) & (e21 < e50) & (c < e9)
        s4_short = (r > 40) & (r < 60) & (c < e21)
        score_short = s1_short.astype(int)+s2_short.astype(int)+s3_short.astype(int)+s4_short.astype(int)

        longs = score_long >= 3
        shorts = score_short >= 3

    return longs, shorts


# ═══════════════════════════════════════════════════════════════
# TRADE SIMULATOR — with dynamic trail based on ATR
# ═══════════════════════════════════════════════════════════════
def sim_trades(signals, df, tf_min, sl_pct=0.03, trail_pct=None, tp_pct=None):
    """Walk forward simulation. trail_pct=None means use ATR-based trail."""
    if not signals:
        return []

    c = df["close"]; h = df["high"]; l = df["low"]

    # Dynamic trail: 2× ATR if not specified
    if trail_pct is None:
        atr_vals = atr(df, 14)

    trades = []
    in_trade = None

    for sig in signals:
        if in_trade:
            continue

        entry_bar = sig["bar"]
        if entry_bar >= len(c) - 5:
            continue

        entry_price = c.iloc[entry_bar]
        side = sig["side"]

        # Dynamic trail: 2× ATR at entry
        if trail_pct is None:
            trail_dist = 2 * (atr_vals.iloc[entry_bar] / entry_price)
            trail_dist = max(trail_dist, 0.01)  # min 1%
            trail_dist = min(trail_dist, 0.08)  # max 8%
            activate = trail_dist * 1.2
        else:
            trail_dist = trail_pct
            activate = trail_pct * 1.5

        max_bars = max(int((4 * 24 * 60) / tf_min), 24)

        in_trade = {
            "side": side, "entry": entry_price, "entry_bar": entry_bar,
            "high_water": entry_price, "low_water": entry_price,
            "trail_active": False, "trail_stop": None,
        }

        for i in range(entry_bar + 1, len(df)):
            bars_held = i - entry_bar

            if side == "long":
                in_trade["high_water"] = max(in_trade["high_water"], h.iloc[i])
                profit = (in_trade["high_water"] - entry_price) / entry_price
            else:
                in_trade["low_water"] = min(in_trade["low_water"], l.iloc[i])
                profit = (entry_price - in_trade["low_water"]) / entry_price

            if not in_trade["trail_active"] and profit >= activate:
                in_trade["trail_active"] = True
                if side == "long":
                    in_trade["trail_stop"] = in_trade["high_water"] * (1 - trail_dist)
                else:
                    in_trade["trail_stop"] = in_trade["low_water"] * (1 + trail_dist)

            if in_trade["trail_active"]:
                if side == "long":
                    new_stop = in_trade["high_water"] * (1 - trail_dist)
                    in_trade["trail_stop"] = max(in_trade.get("trail_stop", 0), new_stop)
                else:
                    new_stop = in_trade["low_water"] * (1 + trail_dist)
                    in_trade["trail_stop"] = min(in_trade.get("trail_stop", float("inf")), new_stop)

            exit_price = None; exit_reason = None

            if side == "long":
                hard_sl = entry_price * (1 - sl_pct)
                eff_sl = max(hard_sl, in_trade.get("trail_stop", hard_sl)) if in_trade["trail_active"] else hard_sl
                if tp_pct and h.iloc[i] >= entry_price * (1 + tp_pct):
                    exit_price = entry_price * (1 + tp_pct); exit_reason = "TP"
                elif l.iloc[i] <= eff_sl:
                    exit_price = eff_sl
                    exit_reason = "TRAIL" if in_trade["trail_active"] else "SL"
            else:
                hard_sl = entry_price * (1 + sl_pct)
                eff_sl = min(hard_sl, in_trade.get("trail_stop", hard_sl)) if in_trade["trail_active"] else hard_sl
                if tp_pct and l.iloc[i] <= entry_price * (1 - tp_pct):
                    exit_price = entry_price * (1 - tp_pct); exit_reason = "TP"
                elif h.iloc[i] >= eff_sl:
                    exit_price = eff_sl
                    exit_reason = "TRAIL" if in_trade["trail_active"] else "SL"

            if bars_held >= max_bars:
                exit_price = c.iloc[i]; exit_reason = "TIMEOUT"

            if exit_price is not None:
                pnl = (exit_price - entry_price) / entry_price if side == "long" else (entry_price - exit_price) / entry_price
                trades.append({
                    "side": side, "entry": entry_price, "exit": exit_price,
                    "pnl_pct": pnl, "exit_reason": exit_reason,
                    "bars_held": bars_held, "trailed": in_trade["trail_active"],
                    "entry_bar": entry_bar, "exit_bar": i,
                    "entry_time": int(df["ts"].iloc[entry_bar]),
                    "exit_time": int(df["ts"].iloc[i]),
                })
                in_trade = None
                break

    return trades


def compute_stats(trades):
    """Compounding P&L simulation."""
    if not trades:
        return None

    balance = STARTING_BALANCE
    peak = balance; dd = 0
    wins = 0; losses = 0
    max_losers = 0; streak = 0
    trailed_wins = 0

    for t in sorted(trades, key=lambda x: x["entry_time"]):
        margin = balance * RISK_FRACTION
        notional = margin * LEVERAGE
        pnl_usd = notional * t["pnl_pct"]
        balance += pnl_usd
        if balance <= 0: balance = 0; break

        if t["pnl_pct"] > 0.0001:
            wins += 1; streak = 0
            if t["trailed"]: trailed_wins += 1
        elif t["pnl_pct"] < -0.0001:
            losses += 1; streak += 1
            max_losers = max(max_losers, streak)

        if balance > peak: peak = balance
        dd = max(dd, (peak - balance) / peak * 100 if peak > 0 else 0)

    total = len(trades)
    wr = wins / total * 100 if total else 0
    avg_w = sum(t["pnl_pct"] for t in trades if t["pnl_pct"] > 0) / max(wins, 1) * 100
    avg_l = sum(t["pnl_pct"] for t in trades if t["pnl_pct"] < 0) / max(losses, 1) * 100
    avg_bars = sum(t["bars_held"] for t in trades) / total
    ret = (balance / STARTING_BALANCE - 1) * 100

    # Sharpe-like ratio (simplified)
    pnls = [t["pnl_pct"] * 100 for t in trades]
    sharpe = (np.mean(pnls) / np.std(pnls) * math.sqrt(365 / max(total, 1))) if len(pnls) > 1 and np.std(pnls) > 0 else 0

    # Expectancy R
    exp_r = (wr/100 * avg_w - (1-wr/100) * abs(avg_l)) / abs(avg_l) if avg_l != 0 else 0

    return {
        "balance": round(balance, 2), "return_pct": round(ret, 1),
        "total": total, "wins": wins, "losses": losses,
        "wr": round(wr, 1), "max_dd": round(dd, 1),
        "avg_win_pct": round(avg_w, 2), "avg_loss_pct": round(avg_l, 2),
        "max_losers": max_losers, "avg_bars": round(avg_bars, 1),
        "trailed_wins": trailed_wins,
        "sharpe": round(sharpe, 2), "exp_r": round(exp_r, 2),
    }


# ═══════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════
def load_data():
    cache = {}
    for sym in SYMBOLS:
        for tf in TFS:
            fname = f"{sym.replace('-','_')}_{tf}_365d.parquet"
            path = os.path.join(CACHE_DIR, fname)
            if not os.path.exists(path):
                continue
            df = pd.read_parquet(path).sort_values("ts").reset_index(drop=True)
            cutoff = df["ts"].max() - (DAYS * 24 * 3600 * 1000)
            df = df[df["ts"] >= cutoff].copy()
            if len(df) >= 200:
                cache[(sym, tf)] = df
    return cache


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    STRATEGIES = [
        "1_ADX_BREAKOUT", "2_VOLUME_SURGE", "3_FIB_BOUNCE", "4_EMA_STACK",
        "5_RANGE_EXPANSION", "6_PULLBACK_EMA", "7_BREAKOUT_FIB_CONFLUENCE",
        "8_VOLUME_CLIMAX", "9_ADX_RSI_COMBO", "10_TREND_FOLLOWING",
        "11_BB_SQUEEZE", "12_PIVOT_BREAKOUT", "13_MACD_CROSS",
        "14_OPENING_RANGE", "15_VWAP_REVERSION", "16_MOMENTUM_BURST",
        "17_SUPPORT_RESISTANCE", "18_DUAL_CONFIRMATION", "19_ATR_TRAIL_SETUP",
        "20_ENSEMBLE",
    ]

    print("=" * 100)
    print("20 STRATEGIES × 5 TIMEFRAMES × 10 COINS — ITERATIVE BACKTEST")
    print("=" * 100)

    # Load data
    t0 = _time.time()
    data = load_data()
    print(f"\nLoaded {len(data)} datasets ({sum(len(v) for v in data.values()):,} bars) in {_time.time()-t0:.1f}s")

    all_results = []

    for strat_name in STRATEGIES:
        print(f"\n{'─'*80}")
        print(f"  {strat_name}")
        print(f"{'─'*80}")

        for tf in TFS:
            tf_min = TF_MINUTES[tf]
            all_trades = []

            for sym in SYMBOLS:
                df = data.get((sym, tf))
                if df is None:
                    continue

                # Generate signals
                longs, shorts = strategy_signals(strat_name, df)

                # Convert to signal list
                signals = []
                for i in range(60, len(df)):
                    if longs.iloc[i]:
                        signals.append({"bar": i, "side": "long", "time": df["ts"].iloc[i]})
                    elif shorts.iloc[i]:
                        signals.append({"bar": i, "side": "short", "time": df["ts"].iloc[i]})

                # Simulate with 2 different SL settings
                for sl_pct in [0.03, 0.05]:
                    trades = sim_trades(signals, df, tf_min, sl_pct=sl_pct)
                    if trades:
                        for t in trades:
                            t["sl_pct"] = sl_pct
                        all_trades.extend(trades)

            if not all_trades:
                continue

            # Group by SL
            for sl in [0.03, 0.05]:
                sl_trades = [t for t in all_trades if t.get("sl_pct") == sl]
                stats = compute_stats(sl_trades)
                if stats and stats["total"] >= 10:
                    stats["strategy"] = strat_name
                    stats["tf"] = tf
                    stats["tf_min"] = tf_min
                    stats["sl_pct"] = sl
                    all_results.append(stats)

                    tier = "🔥" if stats["return_pct"] > 50 else ("✅" if stats["return_pct"] > 0 else "❌")
                    print(f"    {tf:4s} SL={sl*100:.0f}% {tier} ret={stats['return_pct']:+7.1f}% "
                          f"WR={stats['wr']:.0f}% trades={stats['total']:4d} DD={stats['max_dd']:.0f}% "
                          f"sharpe={stats['sharpe']:.2f} expR={stats['exp_r']:.2f}")

    # ═══════════════════════════════════════════════════════════
    # RANKING & ANALYSIS
    # ═══════════════════════════════════════════════════════════
    all_results.sort(key=lambda x: x["return_pct"], reverse=True)

    print("\n" + "=" * 100)
    print("🏆 TOP 20 — BEST STRATEGY × TF × SL COMBOS")
    print("=" * 100)
    print(f"{'Rank':<5} {'Strategy':<28s} {'TF':<5s} {'SL%':<5s} {'Return':<9s} {'WR':<6s} {'Trades':<7s} {'DD':<6s} {'Sharpe':<8s} {'ExpR':<7s}")
    print(f"{'─'*5} {'─'*28} {'─'*5} {'─'*5} {'─'*9} {'─'*6} {'─'*7} {'─'*6} {'─'*8} {'─'*7}")

    for i, r in enumerate(all_results[:20], 1):
        tier = "🔥" if r["return_pct"] > 50 else ("✅" if r["return_pct"] > 0 else "❌")
        print(f"{i:<5} {tier} {r['strategy']:<25s} {r['tf']:<5s} {r['sl_pct']*100:.0f}%   "
              f"{r['return_pct']:+8.1f}% {r['wr']:5.1f}% {r['total']:5d}  {r['max_dd']:5.1f}% "
              f"{r['sharpe']:7.2f}  {r['exp_r']:6.2f}")

    # Best by TF
    print(f"\n{'─'*80}")
    print("BEST STRATEGY PER TIMEFRAME")
    print(f"{'─'*80}")
    for tf in TFS:
        tf_results = [r for r in all_results if r["tf"] == tf and r["return_pct"] > 0]
        if tf_results:
            best = max(tf_results, key=lambda x: x["return_pct"])
            print(f"  {tf:4s}: {best['strategy']:<25s} SL={best['sl_pct']*100:.0f}% → {best['return_pct']:+.1f}% "
                  f"({best['total']}t, {best['wr']:.0f}% WR, {best['max_dd']:.0f}% DD)")

    # Best by strategy (which TF works best for each)
    print(f"\n{'─'*80}")
    print("BEST TF PER STRATEGY")
    print(f"{'─'*80}")
    for strat in STRATEGIES:
        strat_results = [r for r in all_results if r["strategy"] == strat]
        if strat_results:
            best = max(strat_results, key=lambda x: x["return_pct"])
            worst = min(strat_results, key=lambda x: x["return_pct"])
            print(f"  {strat:<28s}: best={best['tf']:4s} SL={best['sl_pct']*100:.0f}% {best['return_pct']:+7.1f}% | "
                  f"worst={worst['tf']:4s} {worst['return_pct']:+7.1f}%")

    # Winner analysis: what do the best have in common?
    print(f"\n{'─'*80}")
    print("WINNER ANALYSIS — What Makes Strategies Profitable")
    print(f"{'─'*80}")
    top10 = all_results[:10]
    bottom10 = all_results[-10:]

    for label, group in [("🏆 TOP 10", top10), ("💀 BOTTOM 10", bottom10)]:
        avg_ret = np.mean([r["return_pct"] for r in group])
        avg_wr = np.mean([r["wr"] for r in group])
        avg_trades = np.mean([r["total"] for r in group])
        avg_dd = np.mean([r["max_dd"] for r in group])
        avg_sharpe = np.mean([r["sharpe"] for r in group])
        tf_counts = defaultdict(int)
        sl_counts = defaultdict(int)
        for r in group:
            tf_counts[r["tf"]] += 1
            sl_counts[r["sl_pct"]] += 1
        print(f"\n  {label}:")
        print(f"    Avg Return: {avg_ret:+.1f}% | Avg WR: {avg_wr:.0f}% | Avg Trades: {avg_trades:.0f}")
        print(f"    Avg DD: {avg_dd:.0f}% | Avg Sharpe: {avg_sharpe:.2f}")
        print(f"    TF distribution: {dict(tf_counts)}")
        print(f"    SL preference: {dict(sl_counts)}")

    # Save
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(OUTPUT_DIR, f"backtest_20_strategies_{ts}.json")
    csv_path = os.path.join(OUTPUT_DIR, f"backtest_20_strategies_{ts}.csv")

    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    csv_fields = ["strategy","tf","sl_pct","return_pct","wr","total","max_dd","sharpe","exp_r","avg_win_pct","avg_loss_pct","max_losers"]
    with open(csv_path, "w") as f:
        f.write(",".join(csv_fields) + "\n")
        for r in all_results:
            f.write(",".join(str(r.get(k,"")) for k in csv_fields) + "\n")

    print(f"\n✅ Saved: {json_path}")
    print(f"✅ Saved: {csv_path}")

    elapsed = _time.time() - t0
    print(f"\nTotal: {elapsed/60:.1f} min | {len(all_results)} results")


if __name__ == "__main__":
    main()
