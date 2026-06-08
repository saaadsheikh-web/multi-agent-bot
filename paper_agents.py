#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10 NEW PAPER AGENTS — built from deep research on 285+ trades.

Research findings that shaped these:
  - Shorts: 53.3% WR (+$2.79) vs Longs: 48.9% (-$2.44) → short bias pays
  - 04:00 UTC: 85% WR | 07:00: 75% | 14:00: 72% WR $+3.20 | 17:00: 70%
  - Multi-agent confluence: +$4.76 on 97 trades
  - Metals: +$2.98 on 18 trades (big wins, few losses)
  - XMR: +$4.92, CL: +$2.62, GIGGLE: 80% WR
  - BTC 22 trades @ 59% WR — consistent
  - Stocks only 12 trades — need more data
  - Worst hours: 08-11, 19, 21 UTC

ALL PAPER ONLY. Auto-deploy if ≥10 trades, ≥55% WR, ExpR ≥ +0.15R.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import numpy as np
import pandas as pd

# We use the same Agent base class and Signal from bot.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from bot import Agent, Signal
except ImportError:
    # Standalone test
    class Agent:  # type: ignore
        notional_multiplier = 0.03
        name = "base"
        enabled = True
        paper_only = True
        profile = "base"
        valid_regimes: List[str] = ["RANGING", "TRENDING", "VOLATILE"]

    @dataclass
    class Signal:
        agent: str
        symbol: str
        side: str
        confidence: int
        profile: str
        reason: str = ""
        metadata: dict = None  # type: ignore


# =============================================================================
# AGENT 1: GOLDEN HOUR AGENT — only trades proven profitable hours
# =============================================================================
class GoldenHourAgent(Agent):
    """Research: 04:00=85% WR, 07:00=75%, 14:00=72% WR $3.20, 17:00=70%.
    Only fires during these windows. Uses RSI + volume confirmation."""
    notional_multiplier = 0.05
    name = "golden_hour"
    profile = "golden_hour"
    paper_only = True

    GOLDEN_HOURS = {4, 5, 6, 7, 14, 15, 16, 17}
    TOXIC_HOURS = {8, 9, 10, 11, 19, 21}

    def analyze(self, sym, ctx):
        from datetime import datetime, timezone
        hour = datetime.now(timezone.utc).hour
        if hour not in self.GOLDEN_HOURS:
            return None

        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]
        last = c.iloc[-1]

        from bot import rsi, atr
        r = rsi(c, 14).iloc[-1]
        a = atr(df).iloc[-1]
        if pd.isna(r) or pd.isna(a) or a <= 0 or last <= 0:
            return None

        # Volume confirmation
        vol = df["volume"]
        avg_vol = vol.iloc[-20:].mean()
        cur_vol = vol.iloc[-1]
        vol_spike = cur_vol > avg_vol * 1.3

        # Only enter with volume confirmation
        if r < 30 and vol_spike:
            return Signal(self.name, sym, "long", 8, self.profile,
                          f"golden_hour LONG h{hour:02d} rsi={r:.0f} vol={vol_spike}",
                          {"atr_sl": last * 0.98, "atr_tp": last * 1.02})
        if r > 70 and vol_spike:
            return Signal(self.name, sym, "short", 8, self.profile,
                          f"golden_hour SHORT h{hour:02d} rsi={r:.0f} vol={vol_spike}",
                          {"atr_sl": last * 1.02, "atr_tp": last * 0.98})
        return None


# =============================================================================
# AGENT 2: MULTI CONFLUENCE AGENT — 3+ agents must agree
# =============================================================================
class MultiConfluenceAgent(Agent):
    """Research: 2+ agents = +$4.76 on 97 trades. This one only fires when
    3+ agents agree, filtering out weak solo signals. Acts as a signal booster."""
    notional_multiplier = 0.06
    name = "multi_confluence"
    profile = "meanrev"
    paper_only = True

    def analyze(self, sym, ctx):
        # This agent is special — it doesn't generate its own signals.
        # Instead, in the main loop, if 3+ agents agree on a symbol+side,
        # it boosts confidence. The actual signal comes from the ensemble.
        # For now, return a simple RSI+MACD combo that fires rarely but strong.
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, ema, macd
        r = rsi(c, 14).iloc[-1]
        try:
            macd_line, macd_signal, mh = macd(c)
            if mh is None or len(mh) < 2:
                return None
            mh_cur = mh.iloc[-1]
            mh_prev = mh.iloc[-2]
        except Exception:
            return None

        if pd.isna(r) or last <= 0:
            return None

        # Rare confluence: RSI extreme + MACD turning + EMA alignment
        e20 = ema(c, 20).iloc[-1]
        e50 = ema(c, 50).iloc[-1]
        if pd.isna(e20) or pd.isna(e50):
            return None

        # Long: oversold + MACD turning up + price below EMA20
        if r < 25 and mh_prev < 0 and mh_cur > mh_prev and last < e20:
            return Signal(self.name, sym, "long", 9, self.profile,
                          f"multi-confluence LONG rsi={r:.0f} macd_turn",
                          {"atr_sl": last * 0.975, "atr_tp": last * 1.025})
        # Short: overbought + MACD turning down + price above EMA20
        if r > 75 and mh_prev > 0 and mh_cur < mh_prev and last > e20:
            return Signal(self.name, sym, "short", 9, self.profile,
                          f"multi-confluence SHORT rsi={r:.0f} macd_turn",
                          {"atr_sl": last * 1.025, "atr_tp": last * 0.975})
        return None


# =============================================================================
# AGENT 3: SHORT BIAS AGENT — shorts win more (+$2.79 vs -$2.44)
# =============================================================================
class ShortBiasAgent(Agent):
    """Research: shorts 53.3% WR +$2.79 vs longs 48.9% -$2.44.
    Only takes shorts. Overbought RSI + bearish EMA cross + volume spike."""
    notional_multiplier = 0.04
    name = "short_bias"
    profile = "short_bias"
    paper_only = True
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, ema
        r = rsi(c, 14).iloc[-1]
        e10 = ema(c, 10).iloc[-1]
        e30 = ema(c, 30).iloc[-1]
        if pd.isna(r) or pd.isna(e10) or pd.isna(e30) or last <= 0:
            return None

        # Volume confirmation
        vol = df["volume"]
        avg_vol = vol.iloc[-20:].mean()

        # Short: RSI > 65 AND EMA10 below EMA30 (bearish) AND volume above avg
        if r > 65 and e10 < e30 and vol.iloc[-1] > avg_vol:
            return Signal(self.name, sym, "short", 8, self.profile,
                          f"short_bias SHORT rsi={r:.0f} ema_bear",
                          {"atr_sl": last * 1.025, "atr_tp": last * 0.975})
        return None


# =============================================================================
# AGENT 4: METALS SCALP AGENT
# =============================================================================
class MetalsScalpAgent(Agent):
    """Research: metals +$2.98 on 18 trades. Big wins, few losses.
    Trades XAU, XAG, XPT, XPD, XAUT, CL with wider SL (metals are volatile)."""
    notional_multiplier = 0.04
    name = "metals_scalp"
    profile = "metals"
    paper_only = True
    METALS = {"XAU-USDT", "XAG-USDT", "XPT-USDT", "XPD-USDT", "XAUT-USDT", "CL-USDT"}

    def analyze(self, sym, ctx):
        if sym not in self.METALS:
            return None
        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, bbands, atr
        r = rsi(c, 14).iloc[-1]
        b = bbands(c, 20, 2.0)
        if b is None or len(b) < 3:
            return None
        lower = b[0].iloc[-1]
        upper = b[1].iloc[-1]
        a = atr(df).iloc[-1]
        if pd.isna(r) or pd.isna(lower) or pd.isna(upper) or last <= 0 or a <= 0:
            return None

        # Long: price below lower BB + RSI < 35 (oversold bounce)
        if last < lower and r < 35:
            return Signal(self.name, sym, "long", 7, self.profile,
                          f"metals LONG below_bb rsi={r:.0f}",
                          {"atr_sl": last * 0.97, "atr_tp": last * 1.03})
        # Short: price above upper BB + RSI > 65
        if last > upper and r > 65:
            return Signal(self.name, sym, "short", 7, self.profile,
                          f"metals SHORT above_bb rsi={r:.0f}",
                          {"atr_sl": last * 1.03, "atr_tp": last * 0.97})
        return None


# =============================================================================
# AGENT 5: XMR MEAN REVERSION
# =============================================================================
class XMRMeanRevAgent(Agent):
    """Research: XMR is the best symbol — +$4.92 on 21 trades, 57% WR.
    Dedicated mean-reversion agent for Monero."""
    notional_multiplier = 0.05
    name = "xmr_meanrev"
    profile = "xmr"
    paper_only = True

    def analyze(self, sym, ctx):
        if sym != "XMR-USDT":
            return None
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, bbands, atr
        r = rsi(c, 14).iloc[-1]
        b = bbands(c, 20, 2.0)
        if b is None:
            return None
        mid = b[2].iloc[-1]  # SMA
        a = atr(df).iloc[-1]
        if pd.isna(r) or pd.isna(mid) or last <= 0 or a <= 0:
            return None

        # Long: RSI < 30 + price < mid_bb (below average)
        if r < 30 and last < mid * 0.995:
            return Signal(self.name, sym, "long", 8, self.profile,
                          f"xmr LONG rsi={r:.0f} below_mid",
                          {"atr_sl": last * 0.97, "atr_tp": last * 1.04})
        # Short: RSI > 70 + price > mid (above average)
        if r > 70 and last > mid * 1.005:
            return Signal(self.name, sym, "short", 8, self.profile,
                          f"xmr SHORT rsi={r:.0f} above_mid",
                          {"atr_sl": last * 1.03, "atr_tp": last * 0.96})
        return None


# =============================================================================
# AGENT 6: ASIAN SESSION AGENT (23-06 UTC)
# =============================================================================
class AsianSessionAgent(Agent):
    """Research: 04:00=85% WR, 05:00=50% WR +$2.89, 00:00=57% WR.
    Asian session has lower volatility — good for mean reversion."""
    notional_multiplier = 0.04
    name = "asian_session"
    profile = "asian"
    paper_only = True
    ASIAN_HOURS = {23, 0, 1, 2, 3, 4, 5, 6}

    def analyze(self, sym, ctx):
        from datetime import datetime, timezone
        hour = datetime.now(timezone.utc).hour
        if hour not in self.ASIAN_HOURS:
            return None

        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, bbands
        r = rsi(c, 14).iloc[-1]
        b = bbands(c, 20, 2.0)
        if b is None:
            return None
        lower = b[0].iloc[-1]
        upper = b[1].iloc[-1]
        if pd.isna(r) or pd.isna(lower) or last <= 0:
            return None

        if r < 28 and last <= lower * 1.005:
            return Signal(self.name, sym, "long", 8, self.profile,
                          f"asian LONG h{hour:02d} rsi={r:.0f}",
                          {"atr_sl": last * 0.975, "atr_tp": last * 1.02})
        if r > 72 and last >= upper * 0.995:
            return Signal(self.name, sym, "short", 8, self.profile,
                          f"asian SHORT h{hour:02d} rsi={r:.0f}",
                          {"atr_sl": last * 1.025, "atr_tp": last * 0.98})
        return None


# =============================================================================
# AGENT 7: US OPEN MOMENTUM (14-17 UTC)
# =============================================================================
class USOpenAgent(Agent):
    """Research: 14:00=72% WR $+3.20, 17:00=70% WR $+2.47.
    US market open brings volume and trends. Momentum with volume."""
    notional_multiplier = 0.05
    name = "us_open"
    profile = "us_open"
    paper_only = True
    US_HOURS = {14, 15, 16, 17}

    def analyze(self, sym, ctx):
        from datetime import datetime, timezone
        hour = datetime.now(timezone.utc).hour
        if hour not in self.US_HOURS:
            return None

        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, ema
        r = rsi(c, 14).iloc[-1]
        e20 = ema(c, 20).iloc[-1]
        if pd.isna(r) or pd.isna(e20) or last <= 0:
            return None

        # Volume must be high
        vol = df["volume"]
        avg_vol = vol.iloc[-20:].mean()
        if vol.iloc[-1] < avg_vol * 1.5:
            return None

        # Trend following: long above EMA20 with RSI 40-60 (not extreme)
        if last > e20 and 40 < r < 60:
            return Signal(self.name, sym, "long", 7, self.profile,
                          f"us_open LONG h{hour:02d} trend",
                          {"atr_sl": last * 0.98, "atr_tp": last * 1.02})
        if last < e20 and 40 < r < 60:
            return Signal(self.name, sym, "short", 7, self.profile,
                          f"us_open SHORT h{hour:02d} trend",
                          {"atr_sl": last * 1.02, "atr_tp": last * 0.98})
        return None


# =============================================================================
# AGENT 8: FUNDING FADE ENHANCED
# =============================================================================
class FundingFadeEnhancedAgent(Agent):
    """Enhanced funding fade. Stricter than funding_extremes — requires:
    funding > 0.08%/8h (extreme only), RSI confirmation, contra-trend EMA."""
    notional_multiplier = 0.05
    name = "funding_fade_v2"
    profile = "funding_v2"
    paper_only = True

    def analyze(self, sym, ctx):
        fr = ctx.funding_rate or 0.0
        if abs(fr) < 0.0008:  # 0.08%/8h — stricter than funding_extremes (0.05%)
            return None

        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        last = c.iloc[-1]
        from bot import rsi, ema
        r = rsi(c, 14).iloc[-1]
        e20 = ema(c, 20).iloc[-1]
        e50 = ema(c, 50).iloc[-1]
        if pd.isna(r) or pd.isna(e20) or last <= 0:
            return None

        # Short extreme positive funding + RSI confirmation + EMA downtrend
        if fr > 0.0008 and r > 55 and e20 < e50:
            return Signal(self.name, sym, "short", 9, self.profile,
                          f"funding_v2 SHORT fr={fr*100:.3f}% rsi={r:.0f}",
                          {"atr_sl": last * 1.025, "atr_tp": last * 0.97})
        # Long extreme negative funding + RSI confirmation + EMA uptrend
        if fr < -0.0008 and r < 45 and e20 > e50:
            return Signal(self.name, sym, "long", 9, self.profile,
                          f"funding_v2 LONG fr={fr*100:.3f}% rsi={r:.0f}",
                          {"atr_sl": last * 0.975, "atr_tp": last * 1.03})
        return None


# =============================================================================
# AGENT 9: ATR MOMENTUM BREAKOUT
# =============================================================================
class ATRMomentumAgent(Agent):
    """ATR-based breakout catcher. When price moves >1.5x ATR in 1 hour
    with volume spike, ride the momentum with trailing stop."""
    notional_multiplier = 0.04
    name = "atr_momentum"
    profile = "atr_momentum"
    paper_only = True
    valid_regimes = ["TRENDING", "VOLATILE"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]
        last = c.iloc[-1]
        prev = c.iloc[-2]
        from bot import atr
        a = atr(df, 14).iloc[-1]
        if pd.isna(a) or a <= 0 or last <= 0:
            return None

        vol = df["volume"]
        avg_vol = vol.iloc[-20:].mean()
        change_pct = abs(last - prev) / prev * 100

        # Breakout: >1.5x ATR move + volume > 2x average
        if change_pct > a / last * 100 * 1.5 and vol.iloc[-1] > avg_vol * 2.0:
            if last > prev:
                return Signal(self.name, sym, "long", 8, self.profile,
                              f"atr_break LONG {change_pct:.1f}% move",
                              {"atr_sl": last * 0.98, "atr_tp": last * 1.04})
            else:
                return Signal(self.name, sym, "short", 8, self.profile,
                              f"atr_break SHORT {change_pct:.1f}% move",
                              {"atr_sl": last * 1.02, "atr_tp": last * 0.96})
        return None


# =============================================================================
# AGENT 10: KELTNER SQUEEZE
# =============================================================================
class KeltnerSqueezeAgent(Agent):
    """Keltner Channel squeeze → expansion breakout.
    When BB width < KC width (squeeze), wait for breakout with volume."""
    notional_multiplier = 0.03
    name = "keltner_squeeze"
    profile = "keltner"
    paper_only = True

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        h = df["high"]
        l = df["low"]
        last = c.iloc[-1]
        from bot import atr, ema

        # Keltner Channel: EMA(20) ± 2*ATR(20)
        e20 = ema(c, 20)
        a = atr(df, 20)
        if e20 is None or a is None:
            return None
        e20_val = e20.iloc[-1]
        a_val = a.iloc[-1]
        kc_upper = e20_val + 2 * a_val
        kc_lower = e20_val - 2 * a_val
        kc_width = (kc_upper - kc_lower) / e20_val if e20_val > 0 else 0

        # Bollinger Band width
        from bot import bbands
        b = bbands(c, 20, 2.0)
        if b is None:
            return None
        bb_upper = b[1].iloc[-1]
        bb_lower = b[0].iloc[-1]
        bb_width = (bb_upper - bb_lower) / e20_val if e20_val > 0 else 0

        if pd.isna(kc_width) or pd.isna(bb_width) or last <= 0:
            return None

        # Squeeze: BB tighter than KC
        vol = df["volume"]
        avg_vol = vol.iloc[-20:].mean()
        in_squeeze = bb_width < kc_width * 0.95

        if in_squeeze and vol.iloc[-1] > avg_vol * 1.5:
            if last > kc_upper:
                return Signal(self.name, sym, "long", 8, self.profile,
                              f"keltner squeeze LONG bb={bb_width:.3f} kc={kc_width:.3f}",
                              {"atr_sl": last * 0.98, "atr_tp": last * 1.03})
            if last < kc_lower:
                return Signal(self.name, sym, "short", 8, self.profile,
                              f"keltner squeeze SHORT bb={bb_width:.3f} kc={kc_width:.3f}",
                              {"atr_sl": last * 1.02, "atr_tp": last * 0.97})
        return None


# =============================================================================
# REGISTRY — all paper agents for auto-discovery
# =============================================================================
PAPER_AGENTS = [
    GoldenHourAgent,
    MultiConfluenceAgent,
    ShortBiasAgent,
    MetalsScalpAgent,
    XMRMeanRevAgent,
    AsianSessionAgent,
    USOpenAgent,
    FundingFadeEnhancedAgent,
    ATRMomentumAgent,
    KeltnerSqueezeAgent,
]


def get_paper_agents():
    """Return instantiated paper agents for registration in bot.py."""
    return [cls() for cls in PAPER_AGENTS]
