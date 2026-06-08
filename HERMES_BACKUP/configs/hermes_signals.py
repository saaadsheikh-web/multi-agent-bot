#!/usr/bin/env python3
"""
HERMES CUSTOM SIGNAL ENGINE — creates high-probability composite signals.
Combines RSI+MACD+BB+EMA+FIB+VOLUME into weighted consensus.
Only fires when 4+ out of 6 agree with high conviction.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
import pandas as pd
import numpy as np

@dataclass
class CustomSignal:
    symbol: str
    side: str  # long/short
    confidence: int  # 0-10
    score: float  # 0-100 weighted consensus
    reasons: List[str]


def generate_signals(sym: str, df_1h: pd.DataFrame,
                     funding_rate: float = 0.0) -> Optional[CustomSignal]:
    """Generate a high-quality custom signal. Only fires with 4+/6 agreement."""

    # 2026-06-07: Hard block only worst hours (4,6 UTC)
    from datetime import datetime, timezone
    bad_hours = {4, 6}
    current_hour = datetime.now(timezone.utc).hour
    if current_hour in bad_hours:
        return None

    if df_1h is None or len(df_1h) < 60:
        return None

    c = df_1h["close"]; h = df_1h["high"]; l = df_1h["low"]; v = df_1h["volume"]
    last = c.iloc[-1]
    if last <= 0:
        return None

    try:
        from bot import rsi, ema, bbands, atr, macd
    except ImportError:
        return None

    # ===== 1. RSI (momentum) =====
    r = rsi(c, 14).iloc[-1]
    if pd.isna(r): return None
    rsi_score_long = max(0, min(100, (40 - r) * 5))  # 0 at RSI=40, 100 at RSI=20
    rsi_score_short = max(0, min(100, (r - 60) * 5))  # 0 at RSI=60, 100 at RSI=80

    # ===== 2. MACD (crypto 24/52/18) =====
    macd_line, macd_sig, macd_hist = macd(c, 24, 52, 18)
    ml = macd_line.iloc[-1]; ms = macd_sig.iloc[-1]
    mh = macd_hist.iloc[-1]; mh_prev = macd_hist.iloc[-2]
    macd_bull = ml > ms and mh > mh_prev
    macd_bear = ml < ms and mh < mh_prev
    macd_score_long = 100 if macd_bull else 0
    macd_score_short = 100 if macd_bear else 0

    # ===== 3. Bollinger Bands =====
    bbu, bbm, bbl = bbands(c, 20, 2.0)
    bb_pos = (last - bbl.iloc[-1]) / (bbu.iloc[-1] - bbl.iloc[-1]) if bbu.iloc[-1] > bbl.iloc[-1] else 0.5
    bb_score_long = max(0, min(100, (1 - bb_pos) * 200))  # near bottom band
    bb_score_short = max(0, min(100, bb_pos * 200))  # near top band

    # ===== 4. EMA Stack =====
    e20 = ema(c, 20).iloc[-1]; e50 = ema(c, 50).iloc[-1]; e200 = ema(c, 200).iloc[-1]
    ema_bull = e20 > e50 > e200
    ema_bear = e20 < e50 < e200
    ema_score_long = 100 if ema_bull else (50 if e20 > e50 else 0)
    ema_score_short = 100 if ema_bear else (50 if e20 < e50 else 0)

    # ===== 5. Fibonacci =====
    swing_high = h.iloc[-50:].max(); swing_low = l.iloc[-50:].min()
    swing_range = swing_high - swing_low
    fib_score_long = fib_score_short = 0
    if swing_range > 0:
        fib_618 = swing_high - swing_range * 0.618
        fib_786 = swing_high - swing_range * 0.786
        proximity_618 = abs(last - fib_618) / last
        proximity_786 = abs(last - fib_786) / last
        near_fib = proximity_618 < 0.01 or proximity_786 < 0.01
        fib_score_long = 100 if near_fib and last < swing_high * 0.99 else 0
        fib_score_short = 100 if near_fib and last > swing_low * 1.01 else 0

    # ===== 6. Volume =====
    avg_v = v.rolling(20).mean().iloc[-1]
    vol_ratio = v.iloc[-1] / avg_v if avg_v > 0 else 1.0
    vol_score = min(100, vol_ratio * 50)  # 1x = 50, 2x = 100

    # ===== WEIGHTED CONSENSUS =====
    weights = {"rsi": 1.0, "macd": 1.5, "bb": 1.0, "ema": 1.2, "fib": 1.3, "vol": 0.8}
    reasons_long = []
    reasons_short = []

    # Composite score (weighted)
    long_score = (
        rsi_score_long * weights["rsi"] +
        macd_score_long * weights["macd"] +
        bb_score_long * weights["bb"] +
        ema_score_long * weights["ema"] +
        fib_score_long * weights["fib"] +
        vol_score * weights["vol"]
    ) / sum(weights.values())
    short_score = (
        rsi_score_short * weights["rsi"] +
        macd_score_short * weights["macd"] +
        bb_score_short * weights["bb"] +
        ema_score_short * weights["ema"] +
        fib_score_short * weights["fib"] +
        vol_score * weights["vol"]
    ) / sum(weights.values())

    # Count agreements
    long_agrees = sum([rsi_score_long > 50, macd_score_long > 50,
                      bb_score_long > 50, ema_score_long > 50,
                      fib_score_long > 50, vol_score > 50])
    short_agrees = sum([rsi_score_short > 50, macd_score_short > 50,
                       bb_score_short > 50, ema_score_short > 50,
                       fib_score_short > 50, vol_score > 50])

    # ===== DECISION =====
    # 2026-06-07: Balanced — 3+/6 with score>=55 (was 4+/6=too strict, was 3+/6+50=too loose)
    if long_score >= 55 and long_agrees >= 3 and long_score > short_score:
        reasons = []
        if rsi_score_long > 50: reasons.append(f"RSI={r:.0f}")
        if macd_score_long > 50: reasons.append("MACD=bull")
        if bb_score_long > 50: reasons.append(f"BB=low({bb_pos:.0%})")
        if ema_score_long > 50: reasons.append("EMA=stack")
        if fib_score_long > 50: reasons.append("FIB=zone")
        if vol_score > 50: reasons.append(f"VOL={vol_ratio:.1f}x")
        conf = min(10, long_agrees + int(long_score > 80))
        return CustomSignal(sym, "long", conf, long_score, reasons)

    if short_score >= 55 and short_agrees >= 3 and short_score > long_score:
        reasons = []
        if rsi_score_short > 50: reasons.append(f"RSI={r:.0f}")
        if macd_score_short > 50: reasons.append("MACD=bear")
        if bb_score_short > 50: reasons.append(f"BB=high({bb_pos:.0%})")
        if ema_score_short > 50: reasons.append("EMA=stack")
        if fib_score_short > 50: reasons.append("FIB=zone")
        if vol_score > 50: reasons.append(f"VOL={vol_ratio:.1f}x")
        conf = min(10, short_agrees + int(short_score > 80))
        return CustomSignal(sym, "short", conf, short_score, reasons)

    return None


def signal_to_dict(sig: CustomSignal) -> dict:
    return {
        "symbol": sig.symbol,
        "side": sig.side,
        "confidence": sig.confidence,
        "score": sig.score,
        "reasons": sig.reasons,
    }
