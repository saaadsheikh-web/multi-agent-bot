#!/usr/bin/env python3
"""
MOMENTUM HUNTER — Finds coins about to EXPLODE UP or CRASH DOWN.

Two modes:
  🚀 LONGS:  Coins building momentum, breaking out, volume surging — about to go parabolic
  💥 SHORTS: Coins that pumped too hard, volume fading, distribution — about to dump

Uses: ADX acceleration, volume climax, RSI extremes, fib extensions,
      pullback depth, momentum divergence, whale activity signals
"""

import math
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional


# ═══════════════════════════════════════════════════════════════
# INDICATORS
# ═══════════════════════════════════════════════════════════════
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def rsi(c, period=14):
    delta = c.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))

def compute_adx(df, period=14):
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


# ═══════════════════════════════════════════════════════════════
# HUNTER SCORING
# ═══════════════════════════════════════════════════════════════

def hunt_long(df) -> dict:
    """Score a coin for LONG potential — about to explode up."""
    c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
    if len(c) < 100:
        return {"score": 0}

    scores = {}

    # 1. Momentum Score (0-25): Is price accelerating upward?
    try:
        mom_1d = (c.iloc[-1] - c.iloc[-24]) / c.iloc[-24] * 100 if len(c) >= 24 else 0
        mom_1w = (c.iloc[-1] - c.iloc[-168]) / c.iloc[-168] * 100 if len(c) >= 168 else 0
        mom_accel = mom_1d - (mom_1w / 7)  # short-term vs longer-term

        if mom_1d > 10 and mom_accel > 5:
            scores["momentum"] = 25
        elif mom_1d > 5 and mom_accel > 2:
            scores["momentum"] = 20
        elif mom_1d > 3 and mom_accel > 0:
            scores["momentum"] = 15
        elif mom_1d > 1:
            scores["momentum"] = 10
        elif mom_1d > 0:
            scores["momentum"] = 5
        else:
            scores["momentum"] = 0
    except:
        scores["momentum"] = 0

    # 2. Breakout Score (0-25): Is price breaking structure?
    try:
        h20 = h.iloc[-20:].max()
        h50 = h.iloc[-50:].max()
        near_high20 = c.iloc[-1] / h20 > 0.98
        near_high50 = c.iloc[-1] / h50 > 0.98
        broke_20 = c.iloc[-1] > h20

        if broke_20 and near_high50:
            scores["breakout"] = 25  # Breaking 20-bar, near 50-bar high
        elif broke_20:
            scores["breakout"] = 20
        elif near_high20:
            scores["breakout"] = 15  # Coiling below resistance
        elif c.iloc[-1] > ema(c, 50).iloc[-1]:
            scores["breakout"] = 10
        else:
            scores["breakout"] = 0
    except:
        scores["breakout"] = 0

    # 3. Volume Score (0-20): Is volume confirming?
    try:
        v_avg20 = v.iloc[-20:].mean()
        v_avg50 = v.iloc[-50:].mean() if len(v) >= 50 else v_avg20
        v_now = v.iloc[-1]
        v_ratio_20 = v_now / v_avg20 if v_avg20 > 0 else 1
        v_ratio_50 = v_now / v_avg50 if v_avg50 > 0 else 1
        v_trend = v_avg20 / v_avg50 if v_avg50 > 0 else 1

        if v_ratio_20 > 3.0 and v_trend > 1.5:
            scores["volume"] = 20  # Massive volume surge + trend
        elif v_ratio_20 > 2.0:
            scores["volume"] = 16
        elif v_ratio_20 > 1.5 and v_trend > 1.2:
            scores["volume"] = 12
        elif v_ratio_20 > 1.0:
            scores["volume"] = 8
        else:
            scores["volume"] = 0
    except:
        scores["volume"] = 0

    # 4. Trend Strength Score (0-15): ADX confirming trend?
    try:
        adx_val, plus_di, minus_di = compute_adx(df)
        adx_now = adx_val.iloc[-1]
        adx_rising = adx_val.iloc[-1] > adx_val.iloc[-5] if len(adx_val) >= 5 else False
        bull = plus_di.iloc[-1] > minus_di.iloc[-1]

        if adx_now > 35 and adx_rising and bull:
            scores["trend"] = 15  # Strong accelerating uptrend
        elif adx_now > 30 and bull:
            scores["trend"] = 12
        elif adx_now > 25 and bull:
            scores["trend"] = 10
        elif adx_now > 20 and bull:
            scores["trend"] = 5
        else:
            scores["trend"] = 0
    except:
        scores["trend"] = 0

    # 5. Not Overbought Score (0-15): Room to run?
    try:
        r = rsi(c).iloc[-1]
        if 45 <= r <= 65:
            scores["room_to_run"] = 15  # Sweet spot — trending but not exhausted
        elif 35 <= r <= 70:
            scores["room_to_run"] = 10
        elif r < 35:
            scores["room_to_run"] = 8  # Oversold bounce potential
        elif r > 80:
            scores["room_to_run"] = 0  # Overbought — be careful
        else:
            scores["room_to_run"] = 5
    except:
        scores["room_to_run"] = 0

    total = sum(scores.values())

    return {
        "direction": "LONG 🚀",
        "score": total,
        "scores": scores,
        "price": float(c.iloc[-1]),
        "change_24h": f"{(c.iloc[-1]/c.iloc[-24]-1)*100:+.1f}%" if len(c) >= 24 else "N/A",
        "signal": "STRONG_BUY" if total >= 80 else ("BUY" if total >= 60 else ("WEAK_BUY" if total >= 40 else "NEUTRAL")),
    }


def hunt_short(df) -> dict:
    """Score a coin for SHORT potential — about to crash down."""
    c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
    if len(c) < 100:
        return {"score": 0}

    scores = {}

    # 1. Exhaustion Score (0-25): Pumped too hard?
    try:
        mom_1d = (c.iloc[-1] - c.iloc[-24]) / c.iloc[-24] * 100 if len(c) >= 24 else 0
        mom_3d = (c.iloc[-1] - c.iloc[-72]) / c.iloc[-72] * 100 if len(c) >= 72 else 0
        from_high_1d = (c.iloc[-1] - h.iloc[-24:].max()) / h.iloc[-24:].max() * 100

        if mom_1d > 20:  # Parabolic
            scores["exhaustion"] = 25
        elif mom_1d > 15 and from_high_1d < -3:  # Pumped then pulling back
            scores["exhaustion"] = 22
        elif mom_1d > 10 and from_high_1d < -2:
            scores["exhaustion"] = 18
        elif mom_3d > 20 and mom_1d < 5:  # Pumped, now stalling
            scores["exhaustion"] = 15
        elif mom_3d > 10:
            scores["exhaustion"] = 10
        else:
            scores["exhaustion"] = 0
    except:
        scores["exhaustion"] = 0

    # 2. Distribution Score (0-25): Is volume fading on the way up?
    try:
        v_avg20 = v.iloc[-20:].mean()
        v_avg50 = v.iloc[-50:].mean() if len(v) >= 50 else v_avg20
        v_trend = v_avg20 / v_avg50 if v_avg50 > 0 else 1
        v_last = v.iloc[-1] / v_avg20 if v_avg20 > 0 else 1

        # Volume dying while price still high = distribution
        if v_trend < 0.7 and v_last < 0.5 and mom_1d > 5:
            scores["distribution"] = 25
        elif v_trend < 0.8 and v_last < 0.7:
            scores["distribution"] = 20
        elif v_last < 0.8 and mom_1d > 0:
            scores["distribution"] = 15
        elif v_trend < 1.0:
            scores["distribution"] = 8
        else:
            scores["distribution"] = 0
    except:
        scores["distribution"] = 0

    # 3. Reversal Signal Score (0-20): Bearish reversal patterns?
    try:
        r = rsi(c).iloc[-1]
        r_prev = rsi(c).iloc[-5] if len(c) >= 5 else r

        # Bearish divergence: price higher high, RSI lower high
        price_hh = c.iloc[-1] > c.iloc[-10] if len(c) >= 10 else False
        rsi_lh = r < r_prev

        # Overbought
        overbought = r > 75

        # Bearish engulfing / shooting star
        body = abs(c.iloc[-1] - df["open"].iloc[-1])
        upper_wick = h.iloc[-1] - max(c.iloc[-1], df["open"].iloc[-1])
        lower_wick = min(c.iloc[-1], df["open"].iloc[-1]) - l.iloc[-1]
        shooting_star = upper_wick > body * 2 and body > 0

        score = 0
        if overbought:
            score += 10
        if rsi_lh and price_hh:
            score += 8  # Bearish divergence
        if shooting_star:
            score += 7
        if r > 70:
            score += 5

        scores["reversal"] = min(score, 20)
    except:
        scores["reversal"] = 0

    # 4. Trend Weakening Score (0-15): Trend losing steam?
    try:
        adx_val, plus_di, minus_di = compute_adx(df)
        adx_now = adx_val.iloc[-1]
        adx_falling = adx_val.iloc[-1] < adx_val.iloc[-5] if len(adx_val) >= 5 else False
        di_cross = plus_di.iloc[-1] < minus_di.iloc[-1] and plus_di.iloc[-2] > minus_di.iloc[-2] if len(plus_di) >= 2 else False

        if adx_now > 35 and adx_falling and di_cross:
            scores["trend_weak"] = 15  # Strong trend reversing
        elif adx_falling and di_cross:
            scores["trend_weak"] = 12
        elif adx_falling:
            scores["trend_weak"] = 8
        elif plus_di.iloc[-1] < minus_di.iloc[-1]:
            scores["trend_weak"] = 5
        else:
            scores["trend_weak"] = 0
    except:
        scores["trend_weak"] = 0

    # 5. Crash Risk Score (0-15): How far can it fall?
    try:
        # Distance to support (fib levels, recent lows)
        l20 = l.iloc[-20:].min()
        l50 = l.iloc[-50:].min()
        dist_to_support = (c.iloc[-1] - l20) / c.iloc[-1] * 100
        dist_to_deep_support = (c.iloc[-1] - l50) / c.iloc[-1] * 100

        if dist_to_support > 15:
            scores["crash_risk"] = 15  # Lot of room to fall
        elif dist_to_support > 10:
            scores["crash_risk"] = 12
        elif dist_to_support > 5:
            scores["crash_risk"] = 8
        elif dist_to_support > 2:
            scores["crash_risk"] = 5
        else:
            scores["crash_risk"] = 0
    except:
        scores["crash_risk"] = 0

    total = sum(scores.values())

    return {
        "direction": "SHORT 💥",
        "score": total,
        "scores": scores,
        "price": float(c.iloc[-1]),
        "change_24h": f"{(c.iloc[-1]/c.iloc[-24]-1)*100:+.1f}%" if len(c) >= 24 else "N/A",
        "signal": "STRONG_SELL" if total >= 80 else ("SELL" if total >= 60 else ("WEAK_SELL" if total >= 40 else "NEUTRAL")),
    }


# ═══════════════════════════════════════════════════════════════
# BATCH HUNTER
# ═══════════════════════════════════════════════════════════════

def hunt_all(data_provider, tickers: List[dict], min_score: int = 40) -> dict:
    """
    Scan all coins for both LONG and SHORT opportunities.
    Returns dict with 'longs' and 'shorts' lists sorted by score.
    """
    longs = []
    shorts = []

    for t in tickers:
        sym = t.get("instId") or ""
        if not sym.endswith("-USDT"):
            continue
        base = sym.split("-")[0]
        if base in ("USDC", "DAI", "BUSD", "TUSD", "USDP", "FDUSD"):
            continue

        try:
            df_1h = data_provider.candles(sym, "1H", 200)
            if df_1h is None or len(df_1h) < 100:
                continue

            # Hunt long
            long_result = hunt_long(df_1h)
            long_result["symbol"] = sym
            if long_result["score"] >= min_score:
                longs.append(long_result)

            # Hunt short
            short_result = hunt_short(df_1h)
            short_result["symbol"] = sym
            if short_result["score"] >= min_score:
                shorts.append(short_result)

        except Exception:
            continue

    longs.sort(key=lambda x: -x["score"])
    shorts.sort(key=lambda x: -x["score"])

    return {"longs": longs, "shorts": shorts}


def print_report(results: dict, top_n: int = 15):
    """Print a clean hunting report."""
    print(f"\n{'='*80}")
    print(f"🚀 MOMENTUM HUNTER — TOP {top_n} LONGS (About to Explode Up)")
    print(f"{'='*80}")
    print(f"{'Rank':<5} {'Symbol':<15} {'Score':<7} {'Signal':<14} {'24h Chg':<12} {'Price':<12} {'Key Factors'}")
    print(f"{'─'*5} {'─'*15} {'─'*7} {'─'*14} {'─'*12} {'─'*12} {'─'*30}")

    for i, coin in enumerate(results["longs"][:top_n], 1):
        sym = coin["symbol"]
        s = coin["scores"]
        factors = [k for k, v in sorted(s.items(), key=lambda x: -x[1]) if v >= 15][:3]
        print(f"{i:<5} {sym:<15} {coin['score']:<7} {coin['signal']:<14} "
              f"{coin['change_24h']:<12} ${coin['price']:<11.4f} {', '.join(factors)}")

    print(f"\n{'='*80}")
    print(f"💥 MOMENTUM HUNTER — TOP {top_n} SHORTS (About to Crash Down)")
    print(f"{'='*80}")
    print(f"{'Rank':<5} {'Symbol':<15} {'Score':<7} {'Signal':<14} {'24h Chg':<12} {'Price':<12} {'Key Factors'}")
    print(f"{'─'*5} {'─'*15} {'─'*7} {'─'*14} {'─'*12} {'─'*12} {'─'*30}")

    for i, coin in enumerate(results["shorts"][:top_n], 1):
        sym = coin["symbol"]
        s = coin["scores"]
        factors = [k for k, v in sorted(s.items(), key=lambda x: -x[1]) if v >= 15][:3]
        print(f"{i:<5} {sym:<15} {coin['score']:<7} {coin['signal']:<14} "
              f"{coin['change_24h']:<12} ${coin['price']:<11.4f} {', '.join(factors)}")

    print(f"\n  Total scanned: {len(results['longs']) + len(results['shorts'])} opportunities found")


if __name__ == "__main__":
    print("Momentum Hunter loaded.")
    print("  hunt_long(df)  — score for upside explosion")
    print("  hunt_short(df) — score for downside crash")
    print("  hunt_all(provider, tickers) — batch scan")
