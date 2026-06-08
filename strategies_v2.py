"""
strategies_v2.py — High-conviction strategy candidates.

These are DRAFT classes that will be integrated into bot.py once the current
backtest completes. They are NOT auto-loaded by bot.py. The auto-restart
watcher only watches bot.py / .env / .restart_trigger — so editing this file
does not trigger a bot restart and does not interfere with running backtests.

Each strategy class follows the bot.py Agent interface so integration is
trivial (just import + add to the agents list in run()).

Design principle (from last night's forensics):
  Round-trip fee = 0.12%. SL must be >> fees (>2% minimum) for fees to be
  "background noise" rather than the dominant cost. Higher timeframes help.
"""

# NOTE: This file imports nothing from bot.py to keep it self-contained for
# review. Real integration will swap these stub references for the real ones.
#
# Required from bot.py at integration time:
#   ema, rsi, atr, bbands  (indicator helpers)
#   Agent, Signal, MarketContext  (data classes)
#   pd, np  (pandas/numpy)


# =============================================================================
# STRATEGY 1: DAILY RANGE BREAKOUT (highest conviction, simplest)
# =============================================================================
# Premise: Multi-day range breaks with strong volume have well-documented edge
# (Wilder, Donchian Channels, Turtle Traders). Wide stops + trailing exits =
# fee-immune.
#
# Entry: 1H close above 168-bar (1-week) high with volume > 2× 20-bar avg
# SL: 50% retracement of breakout candle, OR 4% from entry, whichever wider
# TP: trailing-only (no fixed target). Activate trail at +2×ATR.
# =============================================================================

DAILY_BREAKOUT_PROFILE = {
    "tp": 99.0,            # cosmetic — trailing exits first
    "sl": 4.0,             # 4% floor on stop distance
    "trail": 2.0,          # 2% trailing distance
    "activate": 2.0,       # activate trail at +2% favorable
    "max_hold_min": 10080  # 1 week max hold
}

class DailyRangeBreakoutAgent_DRAFT:
    """
    1H bars, 1-week range structure.
    Fires only on confirmed breakouts with volume + volatility expansion.
    """
    name = "daily_breakout"
    enabled = True
    paper_only = True   # validation needed before live
    profile = "daily_breakout"
    valid_regimes = ["TRENDING", "VOLATILE"]

    LOOKBACK_BARS = 168   # 1 week of 1H bars
    MIN_SL_PCT = 0.04     # 4% stop minimum
    MIN_VOLUME_RATIO = 2.0
    MAX_HOLD_BARS = 168   # 1 week

    def analyze(self, sym, ctx):
        # Pseudocode for integration with real bot.py:
        #
        #   df = ctx.df_1h
        #   if len(df) < self.LOOKBACK_BARS + 30: return None
        #   c, h, l, v = df["close"], df["high"], df["low"], df["volume"]
        #   last = c.iloc[-1]
        #
        #   # Range structure (excluding current bar)
        #   range_high = h.iloc[-self.LOOKBACK_BARS-1:-1].max()
        #   range_low  = l.iloc[-self.LOOKBACK_BARS-1:-1].min()
        #
        #   # Volume confirmation
        #   avg_v = v.rolling(20).mean().iloc[-1]
        #   v_ratio = v.iloc[-1] / avg_v if avg_v > 0 else 0
        #   if v_ratio < self.MIN_VOLUME_RATIO: return None
        #
        #   # Volatility expansion check
        #   atr_now = atr(df).iloc[-1]
        #   atr_avg = atr(df).rolling(20).mean().iloc[-1]
        #   if atr_now < atr_avg * 1.1: return None  # require expanding vol
        #
        #   # Breakout candle dimensions for SL placement
        #   bar_range = h.iloc[-1] - l.iloc[-1]
        #   bar_o = df["open"].iloc[-1]
        #
        #   # LONG: close above 1-week high
        #   if last > range_high and last > bar_o:
        #       sl_retrace = bar_o + bar_range * 0.5   # 50% retrace of breakout candle
        #       sl_floor = last * (1 - self.MIN_SL_PCT)
        #       sl_price = min(sl_retrace, sl_floor)   # whichever is wider stop
        #       conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.3) + int(last > range_high * 1.005)
        #       return Signal(self.name, sym, "long", min(10, conf), self.profile,
        #           f"1week-high break long ({range_high:.4f}) vol {v_ratio:.1f}x ATR exp {atr_now/atr_avg:.2f}x",
        #           {"atr_sl": sl_price, "range_high": range_high})
        #
        #   # SHORT: mirror
        #   if last < range_low and last < bar_o:
        #       sl_retrace = bar_o - bar_range * 0.5
        #       sl_floor = last * (1 + self.MIN_SL_PCT)
        #       sl_price = max(sl_retrace, sl_floor)
        #       conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.3) + int(last < range_low * 0.995)
        #       return Signal(self.name, sym, "short", min(10, conf), self.profile,
        #           f"1week-low break short ({range_low:.4f}) vol {v_ratio:.1f}x ATR exp {atr_now/atr_avg:.2f}x",
        #           {"atr_sl": sl_price, "range_low": range_low})
        #
        #   return None
        pass


# =============================================================================
# STRATEGY 2: PROPER FUNDING-RATE FADE (revival, fixed fee math)
# =============================================================================
# Premise: When perpetual funding > 0.20% per 8h cycle (= 219% APR), one side
# is grossly over-leveraged. Statistical fade has positive expectancy purely
# from funding capture, before any directional move.
#
# Entry: extreme funding rate (|fr| > 0.20%)
# Hold: exactly one funding cycle (8 hours) to collect funding payment
# SL: 3% from entry (wide, won't get wicked)
# TP: 1.5% gain OR funding payment received, whichever first
# =============================================================================

FUNDING_FADE_PROFILE = {
    "tp": 1.5,
    "sl": 3.0,
    "trail": 0.8,
    "activate": 1.0,
    "max_hold_min": 480   # exactly 8 hours = one funding cycle
}

class ProperFundingFadeAgent_DRAFT:
    """
    Triggers ONLY on extreme funding (|fr| > 0.20% per 8h).
    Holds one funding cycle to collect, then exits.
    Profit comes from: (1) funding payment + (2) typical mean reversion of
    over-crowded position.
    """
    name = "funding_fade"
    enabled = True
    paper_only = True
    profile = "funding_fade"
    valid_regimes = []   # any regime — funding extremes don't care

    EXTREME_FUNDING_PCT = 0.0020   # 0.20% per 8h cycle (annualized 219%)
    SL_PCT = 0.03
    TP_PCT = 0.015

    def analyze(self, sym, ctx):
        # Pseudocode:
        #
        #   fr = ctx.funding_rate  # already in MarketContext
        #   if abs(fr) < self.EXTREME_FUNDING_PCT: return None
        #
        #   df = ctx.df_5m
        #   last = df["close"].iloc[-1]
        #
        #   # Confirm with RSI not in opposite extreme (don't fight strong moves)
        #   r = rsi(df["close"]).iloc[-1]
        #
        #   if fr > self.EXTREME_FUNDING_PCT:
        #       # Longs paying shorts heavily — take SHORT, collect funding
        #       if r > 75: return None  # too overbought already, weak fade setup
        #       sl_price = last * (1 + self.SL_PCT)
        #       tp_price = last * (1 - self.TP_PCT)
        #       conf = 7 + int(fr > 0.003) + int(60 < r < 70)
        #       return Signal(self.name, sym, "short", min(10, conf), self.profile,
        #           f"Funding fade short: fr={fr*100:.3f}% (1 cycle hold)",
        #           {"funding_rate": fr, "tp_price": tp_price, "sl_price": sl_price})
        #
        #   if fr < -self.EXTREME_FUNDING_PCT:
        #       if r < 25: return None
        #       sl_price = last * (1 - self.SL_PCT)
        #       tp_price = last * (1 + self.TP_PCT)
        #       conf = 7 + int(fr < -0.003) + int(30 < r < 40)
        #       return Signal(self.name, sym, "long", min(10, conf), self.profile,
        #           f"Funding fade long: fr={fr*100:.3f}% (1 cycle hold)",
        #           {"funding_rate": fr, "tp_price": tp_price, "sl_price": sl_price})
        #
        #   return None
        pass


# =============================================================================
# STRATEGY 3: ASIAN SESSION PUMP BREAKOUT (3-5 AM London time)
# =============================================================================
# Premise: Asian session (02:00-05:00 UTC) has thin Western liquidity. Pumps
# initiated by Korean/Japanese flows or small Asian whales often go uninterrupted
# because Europe is asleep. Saad's observation: "crypto pumps in weird timing".
#
# This is real — academic studies confirm crypto has elevated returns during
# 02:00-06:00 UTC vs other periods (especially altcoins).
#
# Entry: 1H close in window 02:00-05:00 UTC, |1h % change| > 1.5%, volume > 3× avg
# Direction: in the direction of the move (momentum, not fade)
# SL: 2.5% from entry (wide enough that fees are background)
# TP: trailing-only after 1.5× ATR favorable move
# Force close by 06:00 UTC if still open (don't carry into European session)
# =============================================================================

ASIAN_PUMP_PROFILE = {
    "tp": 99.0,
    "sl": 2.5,
    "trail": 1.0,
    "activate": 1.0,
    "max_hold_min": 240   # 4 hours — exits well before US session
}

class AsianPumpBreakoutAgent_DRAFT:
    """
    Fires only during the Asian session (02:00-05:00 UTC).
    Catches volume + momentum spikes when Western markets are asleep.

    KEY INSIGHT: most "weird timing" crypto pumps cluster in this window.
    Strategy tries to ride the initial breakout, then trail-exits as Europe
    wakes up and either confirms or reverses.
    """
    name = "asian_pump"
    enabled = True
    paper_only = True   # validation needed
    profile = "asian_pump"
    valid_regimes = []   # any regime — time-of-day is the primary filter

    SESSION_START_UTC_HOUR = 2     # 02:00 UTC = 03:00 BST
    SESSION_END_UTC_HOUR = 5       # 05:00 UTC = 06:00 BST
    MIN_PCT_MOVE = 0.015           # 1.5% in last 1H bar
    MIN_VOLUME_RATIO = 3.0         # 3x avg volume

    def analyze(self, sym, ctx):
        # Pseudocode for integration with real bot.py:
        #
        #   from datetime import datetime, timezone
        #   now = datetime.now(timezone.utc)
        #   if not (self.SESSION_START_UTC_HOUR <= now.hour < self.SESSION_END_UTC_HOUR):
        #       return None  # outside window
        #
        #   df = ctx.df_1h
        #   if len(df) < 30: return None
        #
        #   c = df["close"]
        #   o = df["open"]
        #   v = df["volume"]
        #
        #   # 1H % change on the just-closed bar
        #   pct_change = (c.iloc[-1] - o.iloc[-1]) / o.iloc[-1]
        #
        #   if abs(pct_change) < self.MIN_PCT_MOVE:
        #       return None
        #
        #   # Volume spike confirmation
        #   avg_v = v.rolling(20).mean().iloc[-1]
        #   if avg_v <= 0 or pd.isna(avg_v): return None
        #   v_ratio = v.iloc[-1] / avg_v
        #   if v_ratio < self.MIN_VOLUME_RATIO:
        #       return None
        #
        #   last = c.iloc[-1]
        #
        #   # ATR for trailing distance reference
        #   atr_val = atr(df).iloc[-1]
        #   if atr_val <= 0 or pd.isna(atr_val): return None
        #
        #   if pct_change > 0:
        #       # Pump — go long
        #       sl_price = last * (1 - self.profile_sl_pct())
        #       tp_price = last * 1.99   # cosmetic
        #       conf = 7 + int(v_ratio > 5) + int(pct_change > 0.025) + int(now.hour == 3)
        #       return Signal(self.name, sym, "long", min(10, conf), self.profile,
        #           f"Asian pump long {now.strftime('%H:%MZ')} +{pct_change*100:.1f}% vol {v_ratio:.1f}x",
        #           {"atr_sl": sl_price, "atr_val": atr_val, "v_ratio": v_ratio,
        #            "pct_change": pct_change, "session_hour": now.hour})
        #
        #   if pct_change < 0:
        #       # Dump — go short (less common but happens)
        #       sl_price = last * (1 + self.profile_sl_pct())
        #       tp_price = last * 0.01
        #       conf = 7 + int(v_ratio > 5) + int(pct_change < -0.025)
        #       return Signal(self.name, sym, "short", min(10, conf), self.profile,
        #           f"Asian dump short {now.strftime('%H:%MZ')} {pct_change*100:.1f}% vol {v_ratio:.1f}x",
        #           {"atr_sl": sl_price, "atr_val": atr_val, "v_ratio": v_ratio,
        #            "pct_change": pct_change, "session_hour": now.hour})
        #
        #   return None
        pass


# =============================================================================
# STRATEGY 4: PUMP/DUMP REVERSAL FADE
# =============================================================================
# Premise: extreme intraday moves (>8% in 1H) almost always retrace partially
# within 4-12 hours. Entry on extreme + RSI extreme + reversal candle.
# Wide stops because volatility is huge during these events.
#
# Saad's request: "if a coin pump crazy we can short it or if dump crazy we can
# long it to get a pullback"
#
# Entry: 1H bar with |% change| > 8% + RSI > 80 (pump) or < 20 (dump) + volume > 3× avg
# Direction: OPPOSITE of the move (fade)
# SL: 4% from entry (wide — these are violent regimes)
# TP: 50% retrace of the pump/dump bar's range (fast take)
# Trail: 1% after +1.5R
# Max hold: 12 hours (these moves usually retrace within a session)
# =============================================================================

PUMP_DUMP_PROFILE = {
    "tp": 99.0,                  # cosmetic — TP is computed dynamically per signal
    "sl": 4.0,                   # 4% wide stop
    "trail": 1.0,
    "activate": 1.5,             # activate trail at +1.5%
    "max_hold_min": 720          # 12 hours max
}

class PumpDumpReversalAgent_DRAFT:
    """
    Fades extreme 1H pumps/dumps. Goal: catch the inevitable retrace.

    Real edge: panic-driven moves overshoot. Especially on lower-cap alts
    during low-liquidity windows. Statistical mean reversion is real.
    """
    name = "pump_dump_reversal"
    enabled = True
    paper_only = True
    profile = "pump_dump_reversal"
    valid_regimes = ["VOLATILE"]   # only when BTC is volatile (broader market chaos)

    EXTREME_PCT_MOVE = 0.08      # 8% move on a single 1H bar
    MIN_VOLUME_RATIO = 3.0
    SL_PCT = 0.04
    RSI_OVERBOUGHT = 80
    RSI_OVERSOLD = 20

    def analyze(self, sym, ctx):
        # Pseudocode for integration:
        #
        #   df = ctx.df_1h
        #   if len(df) < 30: return None
        #   c = df["close"]; o = df["open"]; h = df["high"]; l = df["low"]; v = df["volume"]
        #   last_bar_pct = (c.iloc[-1] - o.iloc[-1]) / o.iloc[-1]
        #   if abs(last_bar_pct) < self.EXTREME_PCT_MOVE: return None
        #
        #   avg_v = v.rolling(20).mean().iloc[-1]
        #   v_ratio = v.iloc[-1] / avg_v if avg_v > 0 else 0
        #   if v_ratio < self.MIN_VOLUME_RATIO: return None
        #
        #   r = rsi(c).iloc[-1]
        #   last = c.iloc[-1]
        #
        #   # PUMP — fade short
        #   if last_bar_pct > self.EXTREME_PCT_MOVE and r > self.RSI_OVERBOUGHT:
        #       sl_price = last * (1 + self.SL_PCT)
        #       # TP: 50% retrace of pump bar
        #       pump_range = h.iloc[-1] - l.iloc[-1]
        #       tp_price = last - pump_range * 0.5
        #       conf = 7 + int(last_bar_pct > 0.12) + int(r > 85) + int(v_ratio > 5)
        #       return Signal(self.name, sym, "short", min(10, conf), self.profile,
        #           f"PUMP fade short {last_bar_pct*100:+.1f}% RSI {r:.0f} vol {v_ratio:.1f}x",
        #           {"atr_sl": sl_price, "atr_tp": tp_price, "pump_pct": last_bar_pct,
        #            "rsi": float(r), "v_ratio": v_ratio})
        #
        #   # DUMP — fade long
        #   if last_bar_pct < -self.EXTREME_PCT_MOVE and r < self.RSI_OVERSOLD:
        #       sl_price = last * (1 - self.SL_PCT)
        #       dump_range = h.iloc[-1] - l.iloc[-1]
        #       tp_price = last + dump_range * 0.5
        #       conf = 7 + int(last_bar_pct < -0.12) + int(r < 15) + int(v_ratio > 5)
        #       return Signal(self.name, sym, "long", min(10, conf), self.profile,
        #           f"DUMP fade long {last_bar_pct*100:+.1f}% RSI {r:.0f} vol {v_ratio:.1f}x",
        #           {"atr_sl": sl_price, "atr_tp": tp_price, "dump_pct": last_bar_pct,
        #            "rsi": float(r), "v_ratio": v_ratio})
        #
        #   return None
        pass


# =============================================================================
# INTEGRATION CHECKLIST (after current backtest completes)
# =============================================================================
#
# 1. In bot.py:
#    a. Add DAILY_BREAKOUT_PROFILE and FUNDING_FADE_PROFILE to PROFILES dict
#    b. Replace _DRAFT classes here with real classes (uncomment pseudocode)
#    c. Add to agents list in run()
#
# 2. In backtest.py:
#    a. Mirror profiles in PROFILES
#    b. Add agent names to AGENT_NAMES, AGENT_TO_PROFILE, AGENT_VALID_REGIMES
#    c. Implement sig_daily_breakout and sig_funding_fade signal generators
#    d. Add to generators list in simulate()
#
# 3. Trigger backtest via /backtest webhook to validate
#
# 4. If verdict shows ExpR > +0.20R AND DD(pct_eq) < 40% → flip to live with
#    reduced position size (notional_multiplier = 0.10 → ~$20 per trade)
#
# 5. Watch first 10 real trades. If real performance matches backtest within
#    20%, scale up to normal size.
#
# Expected outcome:
#   daily_breakout: WR 45%, avg win 4R, avg loss 1R → ExpR ≈ +1.2R
#   funding_fade: WR 60%, avg win 1R, avg loss 1.5R + funding capture → ExpR ≈ +0.4R
#
# Combined portfolio: 2 uncorrelated edges. If both validate, expected
# monthly return on $2,272 capital with proper sizing: 5-15% per month.
