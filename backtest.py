#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backtest engine v2 — fully vectorised indicator precompute, O(n) simulation.

Usage:
  python3 backtest.py --days 365 --symbols all
  python3 backtest.py --days 90  --symbols BTC-USDT,ETH-USDT,SOL-USDT
"""

import os, sys, json, time, math, argparse, logging, traceback
from datetime import datetime, timezone
from typing import Optional, List, Dict, Tuple

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("pip install pandas numpy"); sys.exit(1)

try:
    from blofin import BloFinClient
except ImportError:
    print("pip install blofin"); sys.exit(1)

# ── env ───────────────────────────────────────────────────────────────────────
WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
ENV_PATH = os.path.join(WORK_DIR, ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")
os.makedirs(CACHE_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)])
log = logging.getLogger("BT")

TAKER_FEE   = 0.0006   # per side
LEVERAGE    = 5
NOTIONAL    = 200.0

DEFAULT_UNIVERSE = [
    "BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT","BNB-USDT",
    "DOGE-USDT","ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT",
    "LTC-USDT","ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT",
    "INJ-USDT","TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT",
]

AGENT_NAMES = ["scalp","momentum","swing","meanrev",
               "asymmetric","bb_squeeze","donchian","funding","ema_ribbon",
               "candlestick","rsi_divergence","trend_pullback","daily_breakout",
               "daily_breakout_24h","daily_breakout_4h","daily_breakout_4h_trend",
               "daily_breakout_7d","daily_breakout_12h","daily_breakout_48h",
               "daily_breakout_2h","daily_breakout_8h",
               "asian_pump","pump_dump_reversal","macd_cross",
               "volume_capitulation","supertrend",
               # ── New agents (2026-06-03) ──
               "connors_rsi2","stoch_rsi","bb_bounce","zscore_reversion",
               "hurst_regime","fibonacci","golden_hour","viki",
               "funding_extremes"]

# Mirror of bot.py PROFILES (% of entry price). KEEP IN SYNC.
PROFILES = {
    "scalp":       {"tp": 0.6,  "sl": 0.4,  "trail": 0.25, "activate": 0.3,  "max_hold_min": 30},
    "momentum":    {"tp": 3.0,  "sl": 1.2,  "trail": 1.0,  "activate": 0.8,  "max_hold_min": 360},
    "swing":       {"tp": 4.5,  "sl": 2.0,  "trail": 2.0,  "activate": 1.5,  "max_hold_min": 1440},
    "meanrev":     {"tp": 1.8,  "sl": 1.0,  "trail": 0.8,  "activate": 0.6,  "max_hold_min": 120},
    "whale":       {"tp": 2.0,  "sl": 1.0,  "trail": 0.8,  "activate": 0.6,  "max_hold_min": 180},
    "news":        {"tp": 2.5,  "sl": 1.2,  "trail": 1.0,  "activate": 0.7,  "max_hold_min": 240},
    "asymmetric":  {"tp": 3.0,  "sl": 1.0,  "trail": 0.5,  "activate": 2.0,  "max_hold_min": 720},
    "trend_pullback": {"tp": 99.0, "sl": 2.5, "trail": 1.5, "activate": 1.5, "max_hold_min": 5760},
    "daily_breakout": {"tp": 99.0, "sl": 4.0, "trail": 2.0, "activate": 2.0, "max_hold_min": 10080},
    # 24h variant of daily_breakout — tighter SL (2.5%) for shorter timeframe
    "daily_breakout_24h": {"tp": 99.0, "sl": 2.5, "trail": 1.2, "activate": 1.2, "max_hold_min": 1440},
    "daily_breakout_4h":  {"tp": 99.0, "sl": 1.5, "trail": 0.8, "activate": 0.8, "max_hold_min": 360},
    "daily_breakout_4h_trend": {"tp": 99.0, "sl": 1.2, "trail": 0.6, "activate": 0.6, "max_hold_min": 360},
    "daily_breakout_12h": {"tp": 99.0, "sl": 1.8, "trail": 0.9, "activate": 0.9, "max_hold_min": 720},
    "daily_breakout_48h": {"tp": 99.0, "sl": 3.0, "trail": 1.5, "activate": 1.5, "max_hold_min": 2880},
    "daily_breakout_2h":  {"tp": 99.0, "sl": 0.8, "trail": 0.4, "activate": 0.4, "max_hold_min": 180},
    "daily_breakout_8h":  {"tp": 99.0, "sl": 1.5, "trail": 0.8, "activate": 0.8, "max_hold_min": 480},
    "asian_pump":         {"tp": 99.0, "sl": 2.5, "trail": 1.0, "activate": 1.0, "max_hold_min": 240},
    "pump_dump_reversal": {"tp": 99.0, "sl": 4.0, "trail": 1.0, "activate": 1.5, "max_hold_min": 720},
    "macd_cross":         {"tp": 3.0,  "sl": 1.5, "trail": 0.8, "activate": 0.8, "max_hold_min": 480},
    "volume_capitulation": {"tp": 1.5, "sl": 1.5, "trail": 0.5, "activate": 0.5, "max_hold_min": 240},
    "daily_breakout_7d":  {"tp": 99.0, "sl": 4.0, "trail": 2.0, "activate": 2.0, "max_hold_min": 10080},
    # Supertrend: ATR-derived stops, classic trailing-style profile
    "supertrend":    {"tp": 99.0, "sl": 3.0, "trail": 1.5, "activate": 1.5, "max_hold_min": 4320},
    # ── New agents (2026-06-03) — synced with bot.py PROFILES ──
    "connors_rsi2":  {"tp": 99.0, "sl": 2.5, "trail": 1.2, "activate": 1.6, "max_hold_min": 360},
    "stoch_rsi":     {"tp": 3.0,  "sl": 2.5, "trail": 2.0, "activate": 2.5, "max_hold_min": 360},
    "bb_bounce":     {"tp": 1.5,  "sl": 1.0, "trail": 1.0, "activate": 1.0, "max_hold_min": 240},
    "zscore":        {"tp": 1.2,  "sl": 0.8, "trail": 0.8, "activate": 0.8, "max_hold_min": 180},
    "hurst_regime":  {"tp": 2.5,  "sl": 1.5, "trail": 1.2, "activate": 1.6, "max_hold_min": 240},
    "fibonacci":     {"tp": 99.0, "sl": 3.0, "trail": 3.0, "activate": 3.5, "max_hold_min": 720},
    "golden_hour":   {"tp": 3.0,  "sl": 2.0, "trail": 1.0, "activate": 1.5, "max_hold_min": 360},
    "viki":          {"tp": 99.0, "sl": 7.0, "trail": 1.5, "activate": 3.0, "max_hold_min": 5760},
    "funding_extremes": {"tp": 4.0, "sl": 3.0, "trail": 2.5, "activate": 3.0, "max_hold_min": 480},
}

# Map signal/agent name → profile key (mirrors bot.py class.profile assignments)
AGENT_TO_PROFILE = {
    "scalp":           "scalp",
    "momentum":        "momentum",
    "swing":           "swing",
    "meanrev":         "meanrev",
    "asymmetric":      "asymmetric",
    "bb_squeeze":      "momentum",
    "donchian":        "swing",
    "funding":         "meanrev",
    "ema_ribbon":      "momentum",
    "candlestick":     "swing",
    "rsi_divergence":  "swing",
    "trend_pullback":  "trend_pullback",
    "daily_breakout":  "daily_breakout",
    "daily_breakout_24h": "daily_breakout_24h",
    "daily_breakout_4h":  "daily_breakout_4h",
    "daily_breakout_4h_trend": "daily_breakout_4h_trend",
    "daily_breakout_12h": "daily_breakout_12h",
    "daily_breakout_48h": "daily_breakout_48h",
    "daily_breakout_2h":  "daily_breakout_2h",
    "daily_breakout_8h":  "daily_breakout_8h",
    "asian_pump":         "asian_pump",
    "pump_dump_reversal": "pump_dump_reversal",
    "macd_cross":         "macd_cross",
    "volume_capitulation": "volume_capitulation",
    "daily_breakout_7d":  "daily_breakout_7d",
    "supertrend":      "supertrend",
    "connors_rsi2":    "connors_rsi2",
    "stoch_rsi":       "stoch_rsi",
    "bb_bounce":       "bb_bounce",
    "zscore_reversion": "zscore",
    "hurst_regime":    "hurst_regime",
    "fibonacci":       "fibonacci",
    "golden_hour":     "golden_hour",
    "viki":            "viki",
    "funding_extremes": "funding_extremes",
}

# Valid regimes per agent (mirrors bot.py Agent.valid_regimes). Empty list = any regime.
AGENT_VALID_REGIMES = {
    "scalp":           ["RANGING", "VOLATILE"],
    "momentum":        ["TRENDING"],
    "swing":           ["RANGING"],
    "meanrev":         ["RANGING"],
    "asymmetric":      ["TRENDING"],
    "bb_squeeze":      ["RANGING", "TRENDING"],
    "donchian":        ["TRENDING"],
    "funding":         ["RANGING", "VOLATILE"],
    "ema_ribbon":      ["TRENDING"],
    "candlestick":     ["RANGING", "TRENDING"],
    "rsi_divergence":  ["RANGING", "TRENDING"],
    "trend_pullback":  ["TRENDING"],
    "daily_breakout":  ["TRENDING", "VOLATILE"],
    "daily_breakout_24h": ["TRENDING", "VOLATILE"],
    "daily_breakout_4h":  ["TRENDING", "VOLATILE"],
    "daily_breakout_4h_trend": ["TRENDING", "VOLATILE"],
    "daily_breakout_12h": ["TRENDING", "VOLATILE"],
    "daily_breakout_48h": ["TRENDING", "VOLATILE"],
    "daily_breakout_2h":  ["TRENDING", "VOLATILE"],
    "daily_breakout_8h":  ["TRENDING", "VOLATILE"],
    "asian_pump":         [],
    "pump_dump_reversal": ["VOLATILE"],
    "macd_cross":         ["TRENDING", "VOLATILE"],
    "volume_capitulation": ["VOLATILE", "RANGING"],
    "daily_breakout_7d":  ["TRENDING", "VOLATILE"],
    "supertrend":      ["TRENDING"],
    "connors_rsi2":    ["TRENDING", "VOLATILE", "RANGING"],
    "stoch_rsi":       ["RANGING", "VOLATILE", "TRENDING"],
    "bb_bounce":       ["RANGING"],
    "zscore_reversion": ["RANGING", "VOLATILE"],
    "hurst_regime":    ["RANGING", "VOLATILE"],
    "fibonacci":       ["TRENDING", "VOLATILE", "RANGING"],
    "golden_hour":     ["TRENDING", "VOLATILE"],
    "viki":            ["TRENDING", "VOLATILE", "RANGING"],
    "funding_extremes": ["RANGING", "VOLATILE", "TRENDING"],
}

# ── BloFin client ─────────────────────────────────────────────────────────────
def _client():
    return BloFinClient(
        api_key    = os.environ.get("BLOFIN_API_KEY",""),
        api_secret = os.environ.get("BLOFIN_API_SECRET",""),
        passphrase = os.environ.get("BLOFIN_PASSPHRASE",""),
    )

def _fetch_paginated(client, symbol: str, bar: str, days: int) -> pd.DataFrame:
    """Fetch candle history; BloFin: after=<oldest_ts> returns older bars."""
    bar_min = {"5m":5,"15m":15,"1H":60,"1h":60}
    total   = (days * 24 * 60) // bar_min.get(bar, 15)
    lim     = 500
    rows: list = []
    cursor  = None
    for _ in range(math.ceil(total / lim) + 5):
        try:
            kw = dict(inst_id=symbol, bar=bar, limit=lim)
            if cursor:
                kw["after"] = str(cursor)
            r    = client.public.get_candlesticks(**kw)
            batch = (r or {}).get("data") or []
        except Exception as e:
            log.warning(f"  {symbol} {bar}: {e}")
            break
        if not batch:
            break
        rows.extend(batch)
        cursor = int(batch[-1][0])
        if len(rows) >= total:
            break
        time.sleep(0.18)

    if not rows:
        return pd.DataFrame()
    cols = ["ts","open","high","low","close","volume","vc","vcq","confirm"]
    w  = min(len(rows[0]), len(cols))
    df = pd.DataFrame([r[:w] for r in rows], columns=cols[:w])
    for c in ["ts","open","high","low","close","volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.drop_duplicates("ts").sort_values("ts").reset_index(drop=True).dropna(subset=["close"])

def load_or_fetch(client, symbol: str, bar: str, days: int) -> pd.DataFrame:
    path   = os.path.join(CACHE_DIR, f"{symbol.replace('-','_')}_{bar}_{days}d.parquet")
    cutoff = time.time() - 6 * 3600
    if os.path.exists(path) and os.path.getmtime(path) > cutoff:
        try:
            df = pd.read_parquet(path)
            log.info(f"  cache hit: {symbol} {bar} ({len(df)} bars)")
            return df
        except Exception:
            pass
    log.info(f"  fetching {symbol} {bar} ({days}d)…")
    df = _fetch_paginated(client, symbol, bar, days)
    if not df.empty:
        try: df.to_parquet(path, index=False)
        except Exception as e: log.warning(f"  cache write: {e}")
    return df

# ── vectorised indicators ─────────────────────────────────────────────────────
def v_ema(s: pd.Series, n: int) -> np.ndarray:
    return s.ewm(span=n, adjust=False).mean().values

def v_rsi(s: pd.Series, n: int = 14) -> np.ndarray:
    d  = s.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return (100 - (100 / (1 + rs))).fillna(50).values

def v_macd_hist(s: pd.Series) -> np.ndarray:
    fast = s.ewm(span=12, adjust=False).mean()
    slow = s.ewm(span=26, adjust=False).mean()
    line = fast - slow
    sig  = line.ewm(span=9, adjust=False).mean()
    return (line - sig).values

def v_bbands(s: pd.Series, n=20, k=2.0):
    m   = s.rolling(n).mean()
    sd  = s.rolling(n).std()
    return (m + k*sd).values, m.values, (m - k*sd).values

def v_bb_width(s: pd.Series, n=20) -> np.ndarray:
    m  = s.rolling(n).mean()
    sd = s.rolling(n).std()
    return np.where(m != 0, (2*k*sd/m).values if False else (4*sd/m).values, np.nan)

def v_bbwidth(s: pd.Series, n=20, k=2.0) -> np.ndarray:
    m  = s.rolling(n).mean().values
    sd = s.rolling(n).std().values
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.where(m != 0, 2*k*sd/m, np.nan)

def v_atr(df: pd.DataFrame, n=14) -> np.ndarray:
    h, l, c = df["high"].values, df["low"].values, df["close"].values
    cp = np.roll(c, 1); cp[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - cp), np.abs(l - cp)))
    s  = pd.Series(tr)
    return s.ewm(alpha=1/n, adjust=False).mean().values

def v_adx(df: pd.DataFrame, n=14) -> np.ndarray:
    h, l, c = df["high"].values, df["low"].values, df["close"].values
    up = np.diff(h, prepend=h[0])
    dn = -np.diff(l, prepend=l[0])
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    cp  = np.roll(c, 1); cp[0] = c[0]
    tr  = np.maximum(h-l, np.maximum(np.abs(h-cp), np.abs(l-cp)))
    atr_ = pd.Series(tr).ewm(alpha=1/n, adjust=False).mean().values
    with np.errstate(invalid='ignore', divide='ignore'):
        pdi  = 100 * pd.Series(pdm).ewm(alpha=1/n, adjust=False).mean().values / atr_
        ndi  = 100 * pd.Series(ndm).ewm(alpha=1/n, adjust=False).mean().values / atr_
        dx   = 100 * np.abs(pdi - ndi) / np.where((pdi + ndi) > 0, pdi+ndi, np.nan)
    return pd.Series(dx).ewm(alpha=1/n, adjust=False).mean().fillna(20).values

def roll_max(a: np.ndarray, w: int) -> np.ndarray:
    return pd.Series(a).rolling(w, min_periods=1).max().values

def roll_min(a: np.ndarray, w: int) -> np.ndarray:
    return pd.Series(a).rolling(w, min_periods=1).min().values

def roll_mean(a: np.ndarray, w: int) -> np.ndarray:
    return pd.Series(a).rolling(w, min_periods=1).mean().values

def roll_quantile(a: np.ndarray, w: int, q: float) -> np.ndarray:
    return pd.Series(a).rolling(w, min_periods=w//2).quantile(q).values

# ── precompute all signals for a single timeframe set ─────────────────────────
class PrecomputedData:
    """Holds all indicator arrays for one symbol, aligned to 15m bars."""

    def __init__(self, df5: pd.DataFrame, df15: pd.DataFrame, df1h: pd.DataFrame):
        self.ts15  = df15["ts"].values.astype(np.int64)
        self.o15   = df15["open"].values
        self.h15   = df15["high"].values
        self.l15   = df15["low"].values
        self.c15   = df15["close"].values
        self.v15   = df15["volume"].values
        self.n15   = len(df15)

        c5  = df5["close"];  v5  = df5["volume"]
        c15 = df15["close"]; v15 = df15["volume"]
        c1h = df1h["close"] if not df1h.empty else pd.Series(dtype=float)

        # ── 5m indicators (aligned to 15m via searchsorted) ──
        self.ts5  = df5["ts"].values.astype(np.int64)
        self.c5   = df5["close"].values
        self.h5   = df5["high"].values
        self.l5   = df5["low"].values
        self.v5   = df5["volume"].values

        rsi5   = v_rsi(c5);          self.rsi5  = rsi5
        self.rsi2_5 = v_rsi(c5, 2)   # Connors RSI2: ultra-fast mean-rev
        self.e9_5   = v_ema(c5, 9)   # 5m EMAs for connors_rsi2 trend filter
        self.e21_5  = v_ema(c5, 21)
        self.e50_5  = v_ema(c5, 50)
        self.atr5   = v_atr(df5)
        bbu5, bbm5, bbl5 = v_bbands(c5, 20, 2.5)
        self.bbu5, self.bbl5 = bbu5, bbl5
        self.bbm5 = bbm5
        bbu5b, bbm5b, bbl5b = v_bbands(c5, 20, 2.0)
        self.bbw5  = v_bbwidth(c5, 20, 2.0)
        self.avg_v5 = roll_mean(self.v5, 20)
        self.h5_20  = roll_max(df5["high"].values, 21)   # 20-bar high (excl current)
        self.l5_20  = roll_min(df5["low"].values,  21)
        # for mean-rev: 3-bar move
        c5v = c5.values
        self.mv3_5 = np.zeros(len(c5v))
        self.mv3_5[4:] = (c5v[4:] - c5v[:-4]) / np.where(c5v[:-4] != 0, c5v[:-4], np.nan) * 100
        # bb squeeze quantile (precompute 100-bar rolling 15th percentile of bbwidth)
        self.bbwq15_5 = roll_quantile(self.bbw5, 100, 0.15)
        self.bbwq20_5 = roll_quantile(self.bbw5, 100, 0.20)

        # ── 15m indicators ──
        self.rsi15    = v_rsi(c15)
        self.e9_15    = v_ema(c15, 9)
        self.e21_15   = v_ema(c15, 21)
        self.e50_15   = v_ema(c15, 50)
        self.hist15   = v_macd_hist(c15)
        bbu15, bbm15, bbl15 = v_bbands(c15, 20, 2.0)
        self.bbu15, self.bbl15 = bbu15, bbl15
        self.bbm15    = bbm15
        self.bbw15    = v_bbwidth(c15, 20, 2.0)
        self.bbwq15_15= roll_quantile(self.bbw15, 100, 0.15)
        self.avg_v15  = roll_mean(self.v15, 20)
        self.h15_20   = roll_max(df15["high"].values, 21)
        self.l15_20   = roll_min(df15["low"].values,  21)
        self.atr15    = v_atr(df15)

        # ── 1H indicators ──
        if not df1h.empty and len(df1h) >= 50:
            self.ts1h  = df1h["ts"].values.astype(np.int64)
            self.c1h   = df1h["close"].values
            self.h1h   = df1h["high"].values
            self.l1h   = df1h["low"].values
            self.v1h   = df1h["volume"].values
            self.rsi1h = v_rsi(c1h)
            self.e9_1h = v_ema(c1h, 9)
            self.e21_1h= v_ema(c1h, 21)
            self.e50_1h= v_ema(c1h, 50)
            bbu1h, _, bbl1h = v_bbands(c1h, 20, 2.0)
            self.bbu1h, self.bbl1h = bbu1h, bbl1h
            self.atr1h  = v_atr(df1h)
            self.avg_v1h= roll_mean(df1h["volume"].values, 20)
            # MACD components for sig_macd_cross
            e12_1h = v_ema(c1h, 12); e26_1h = v_ema(c1h, 26)
            self.macd_line_1h = e12_1h - e26_1h
            # v_ema expects pd.Series — wrap numpy array
            self.macd_sig_1h = v_ema(pd.Series(self.macd_line_1h), 9)
            # period=30 donchian (sweep winner: +0.052R vs +0.031R at period=20)
            self.h1h_20 = roll_max(df1h["high"].values, 31)
            self.l1h_20 = roll_min(df1h["low"].values,  31)
            self.has_1h = True
        else:
            self.has_1h = False

    def i5_for(self, ts15: int) -> int:
        """Return the 5m bar index aligned to the given 15m timestamp."""
        idx = int(np.searchsorted(self.ts5, ts15, side="right")) - 1
        return max(0, min(idx, len(self.ts5) - 1))

    def i1h_for(self, ts15: int) -> int:
        if not self.has_1h:
            return 0
        idx = int(np.searchsorted(self.ts1h, ts15, side="right")) - 1
        return max(0, min(idx, len(self.ts1h) - 1))


# ── signal generators (all O(1) lookups into precomputed arrays) ──────────────
def _nan(x): return x is None or (isinstance(x, float) and math.isnan(x))

def sig_scalp(p: PrecomputedData, i5: int, price: float):
    if i5 < 50: return None
    r = p.rsi5[i5]
    avg_v = p.avg_v5[i5]
    if avg_v <= 0 or _nan(avg_v): return None
    vr = p.v5[i5] / avg_v
    body = (p.c5[i5] - p.c5[max(0,i5-1)]) / p.c5[max(0,i5-1)] * 100 if i5 > 0 else 0
    tp = sl = None
    if r < 25 and vr > 1.8 and body > 0:
        tp = price * 1.006; sl = price * 0.996
        return ("scalp", "long", tp, sl, min(10, 6 + int(r<20) + int(vr>2.5)))
    if r > 75 and vr > 1.8 and body < 0:
        tp = price * 0.994; sl = price * 1.004
        return ("scalp", "short", tp, sl, min(10, 6 + int(r>80) + int(vr>2.5)))
    return None

def sig_momentum(p: PrecomputedData, i15: int, price: float):
    if i15 < 80: return None
    e9, e21, e50 = p.e9_15[i15], p.e21_15[i15], p.e50_15[i15]
    h0 = p.hist15[i15]; h1 = p.hist15[max(0,i15-1)]
    r  = p.rsi15[i15]
    if e9>e21>e50 and h0>h1>0 and 50<r<72 and price>e9:
        return ("momentum","long", price*1.030, price*0.988, min(10,7+int(price>e9*1.003)+int(r>55)))
    if e9<e21<e50 and h0<h1<0 and 28<r<50 and price<e9:
        return ("momentum","short",price*0.970, price*1.012, min(10,7+int(price<e9*0.997)+int(r<45)))
    return None

def sig_swing(p: PrecomputedData, i1h: int, price: float):
    if not p.has_1h or i1h < 60: return None
    r  = p.rsi1h[i1h]
    if price <= p.bbl1h[i1h] * 1.005 and r < 38:
        return ("swing","long", price*1.045, price*0.980, 8)
    if price >= p.bbu1h[i1h] * 0.995 and r > 62:
        return ("swing","short",price*0.955, price*1.020, 8)
    return None

def sig_meanrev(p: PrecomputedData, i5: int, price: float):
    if i5 < 50: return None
    r = p.rsi5[i5]; mv = p.mv3_5[i5]
    if price < p.bbl5[i5] and r < 22 and mv < -2.0:
        return ("meanrev","long", price*1.018, price*0.990, min(10,7+int(r<18)+int(mv<-3.5)))
    if price > p.bbu5[i5] and r > 78 and mv > 2.0:
        return ("meanrev","short",price*0.982, price*1.010, min(10,7+int(r>82)+int(mv>3.5)))
    return None

def sig_asymmetric(p: PrecomputedData, i15: int, i1h: int, price: float):
    if i15 < 110: return None
    bbw = p.bbw15[i15]; q15 = p.bbwq15_15[i15]
    if _nan(bbw) or _nan(q15) or bbw > q15: return None
    high20 = p.h15_20[max(0,i15-1)]
    low20  = p.l15_20[max(0,i15-1)]
    atr_v  = p.atr15[i15]
    if atr_v <= 0 or _nan(atr_v): return None
    e9, e21, e50 = p.e9_15[i15], p.e21_15[i15], p.e50_15[i15]
    r  = p.rsi15[i15]
    avg_v = p.avg_v15[i15]
    vr = p.v15[i15] / avg_v if avg_v > 0 else 0
    htf_bull = htf_bear = False
    if p.has_1h and i1h >= 50:
        htf_bull = p.c1h[i1h] > p.e21_1h[i1h] > p.e50_1h[i1h]
        htf_bear = p.c1h[i1h] < p.e21_1h[i1h] < p.e50_1h[i1h]
    # Per forensics: SL must clear fees. Floor at max(2×ATR, 0.8% of price).
    ASYM_SL_ATR_MULT = 2.0
    ASYM_SL_PCT_FLOOR = 0.008
    sl_distance = max(ASYM_SL_ATR_MULT * atr_v, price * ASYM_SL_PCT_FLOOR)
    if price > high20:
        cc = int(e9>e21>e50)+int(vr>=2)+int(55<=r<=70)+int(htf_bull)
        if cc < 3: return None
        return ("asymmetric","long",  price+3*atr_v, price - sl_distance, min(10,7+min(3,cc-3)))
    if price < low20:
        cc = int(e9<e21<e50)+int(vr>=2)+int(30<=r<=45)+int(htf_bear)
        if cc < 3: return None
        return ("asymmetric","short", price-3*atr_v, price + sl_distance, min(10,7+min(3,cc-3)))
    return None

def sig_bb_squeeze(p: PrecomputedData, i5: int, price: float):
    if i5 < 110: return None
    bbw = p.bbw5[i5]; q20 = p.bbwq20_5[i5]
    if _nan(bbw) or _nan(q20) or bbw > q20: return None
    avg_v = p.avg_v5[i5]
    vr = p.v5[i5] / avg_v if avg_v > 0 else 0
    r  = p.rsi5[i5]
    high20 = p.h5_20[max(0,i5-1)]
    low20  = p.l5_20[max(0,i5-1)]
    if price > high20 and vr > 1.4 and r > 50:
        return ("bb_squeeze","long",  price*1.030, price*0.988, min(10,6+int(vr>2)+int(r>58)))
    if price < low20  and vr > 1.4 and r < 50:
        return ("bb_squeeze","short", price*0.970, price*1.012, min(10,6+int(vr>2)+int(r<42)))
    return None

def sig_donchian(p: PrecomputedData, i1h: int, price: float):
    """Donchian breakout: tuned to period=30, ATR_mult=2.0 per parameter sweep."""
    DON_PERIOD = 30
    DON_ATR_MULT = 2.0
    if not p.has_1h or i1h < DON_PERIOD + 10: return None
    atr_v = p.atr1h[i1h]
    if atr_v <= 0: return None
    avg_v = p.avg_v1h[i1h]
    vr = p.v1h[i1h] / avg_v if avg_v > 0 else 0
    if vr < 1.8: return None
    # 30-bar high/low, exclude current bar
    lo = max(0, i1h - DON_PERIOD)
    high_n = float(np.max(p.h1h[lo:i1h]))
    low_n  = float(np.min(p.l1h[lo:i1h]))
    if price > high_n:
        return ("donchian","long",  price*1.045, price - atr_v * DON_ATR_MULT, min(10,7+int(vr>2.5)))
    if price < low_n:
        return ("donchian","short", price*0.955, price + atr_v * DON_ATR_MULT, min(10,7+int(vr>2.5)))
    return None

def sig_funding(p: PrecomputedData, i5: int, price: float, fr: float):
    if i5 < 20 or fr == 0: return None
    r = p.rsi5[i5]
    if fr > 0.0008:
        return ("funding","short", price*0.982, price*1.010, min(10,7+int(fr>0.0012)+int(r>60)))
    if fr < -0.0008:
        return ("funding","long",  price*1.018, price*0.990, min(10,7+int(fr<-0.0012)+int(r<40)))
    return None

def sig_ema_ribbon(p: PrecomputedData, i5: int, i1h: int, price: float):
    if i5 < 55 or not p.has_1h or i1h < 55: return None
    i15 = i5 // 3   # rough 15m index from 5m
    if i15 >= len(p.e9_15): return None
    bull = (p.e9_15[i15]>p.e21_15[i15]>p.e50_15[i15] and
            p.e9_1h[i1h]>p.e21_1h[i1h]>p.e50_1h[i1h])
    bear = (p.e9_15[i15]<p.e21_15[i15]<p.e50_15[i15] and
            p.e9_1h[i1h]<p.e21_1h[i1h]<p.e50_1h[i1h])
    r5 = p.rsi5[i5]
    if bull and 50 < r5 < 75:
        return ("ema_ribbon","long",  price*1.030, price*0.988, min(10,8+int(r5>58)))
    if bear and 25 < r5 < 50:
        return ("ema_ribbon","short", price*0.970, price*1.012, min(10,8+int(r5<42)))
    return None


# ── candlestick pattern helpers (single-bar checks against arrays) ──
def _is_hammer(o, h, l, c):
    body = abs(c - o)
    if o <= 0 or body <= 0: return False
    upper = h - max(o, c); lower = min(o, c) - l
    return lower >= 2 * body and upper <= body * 0.6

def _is_shooting_star(o, h, l, c):
    body = abs(c - o)
    if o <= 0 or body <= 0: return False
    upper = h - max(o, c); lower = min(o, c) - l
    return upper >= 2 * body and lower <= body * 0.6

def _is_bullish_engulfing(o1, c1, o2, c2):
    return c1 < o1 and c2 > o2 and c2 >= o1 and o2 <= c1

def _is_bearish_engulfing(o1, c1, o2, c2):
    return c1 > o1 and c2 < o2 and o2 >= c1 and c2 <= o1

def _is_morning_star(o1, c1, o2, c2, o3, c3):
    if not (c1 < o1 and abs(c1 - o1) > 0): return False
    body1 = abs(c1 - o1); body2 = abs(c2 - o2)
    if body2 > body1 * 0.4: return False
    if not (c3 > o3): return False
    body3 = abs(c3 - o3)
    if body3 < body1 * 0.5: return False
    midpoint1 = (o1 + c1) / 2
    return c3 > midpoint1

def _is_evening_star(o1, c1, o2, c2, o3, c3):
    if not (c1 > o1 and abs(c1 - o1) > 0): return False
    body1 = abs(c1 - o1); body2 = abs(c2 - o2)
    if body2 > body1 * 0.4: return False
    if not (c3 < o3): return False
    body3 = abs(c3 - o3)
    if body3 < body1 * 0.5: return False
    midpoint1 = (o1 + c1) / 2
    return c3 < midpoint1


def sig_candlestick(p: PrecomputedData, i15: int, price: float):
    """15m reversal at exhaustion zones. Mirror of CandlestickAgent in bot.py."""
    if i15 < 60: return None
    e50 = p.e50_15[i15]
    if _nan(e50) or e50 <= 0: return None
    avg_v = p.avg_v15[i15]
    if avg_v <= 0 or _nan(avg_v): return None
    v_ratio = p.v15[i15] / avg_v
    r = p.rsi15[i15]
    cur_price = p.c15[i15]   # use closed-bar price for pattern check (not next_open)

    # Need at least 3 prior bars for star patterns
    if i15 < 3: return None
    o1, c1 = p.o15[i15-2], p.c15[i15-2]
    o2, c2 = p.o15[i15-1], p.c15[i15-1]
    o3, h3, l3, c3 = p.o15[i15], p.h15[i15], p.l15[i15], p.c15[i15]

    pattern_bull = None
    if _is_hammer(o3, h3, l3, c3):
        pattern_bull = "hammer"
    elif _is_bullish_engulfing(o2, c2, o3, c3):
        pattern_bull = "bullish_engulfing"
    elif _is_morning_star(o1, c1, o2, c2, o3, c3):
        pattern_bull = "morning_star"

    pattern_bear = None
    if _is_shooting_star(o3, h3, l3, c3):
        pattern_bear = "shooting_star"
    elif _is_bearish_engulfing(o2, c2, o3, c3):
        pattern_bear = "bearish_engulfing"
    elif _is_evening_star(o1, c1, o2, c2, o3, c3):
        pattern_bear = "evening_star"

    # Bullish: oversold + bullish pattern + volume
    if pattern_bull and cur_price < e50 * 0.985 and r < 38 and v_ratio >= 1.3:
        conf = 7 + int(r < 30) + int(v_ratio >= 2.0) + int(pattern_bull == "morning_star")
        return ("candlestick", "long", price * 1.045, price * 0.980, min(10, conf))

    # Bearish: overbought + bearish pattern + volume
    if pattern_bear and cur_price > e50 * 1.015 and r > 62 and v_ratio >= 1.3:
        conf = 7 + int(r > 70) + int(v_ratio >= 2.0) + int(pattern_bear == "evening_star")
        return ("candlestick", "short", price * 0.955, price * 1.020, min(10, conf))

    return None


def sig_daily_breakout(p: PrecomputedData, i1h: int, price: float):
    """1H bars, 168-bar range break + volume + ATR expansion. Wide stops, trailing exit."""
    LOOKBACK = 168
    MIN_SL_PCT = 0.04
    MIN_VOL = 2.0
    if not p.has_1h or i1h < LOOKBACK + 30: return None
    if i1h >= len(p.c1h): return None

    last = p.c1h[i1h]
    if last <= 0: return None

    lo = max(0, i1h - LOOKBACK)
    range_high = float(np.max(p.h1h[lo:i1h]))
    range_low  = float(np.min(p.l1h[lo:i1h]))

    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < MIN_VOL: return None

    atr_now = p.atr1h[i1h]
    if atr_now <= 0: return None
    atr_window = p.atr1h[max(0, i1h - 20):i1h]
    if len(atr_window) < 5:
        atr_avg = atr_now
    else:
        atr_avg = float(np.nanmean(atr_window))
    if atr_avg <= 0 or atr_now < atr_avg * 1.1: return None

    # We don't have 1h opens easily here — use mid-bar proxy:
    bar_h = p.h1h[i1h]
    bar_l = p.l1h[i1h]
    bar_range = bar_h - bar_l
    if bar_range <= 0: return None
    # Proxy "open" as previous close (typical for hourly bars)
    bar_o = p.c1h[i1h - 1] if i1h >= 1 else last

    # LONG break
    if last > range_high and last > bar_o:
        sl_retrace = bar_o + bar_range * 0.5
        sl_floor = price * (1 - MIN_SL_PCT)
        sl_price = min(sl_retrace, sl_floor)
        tp_price = price * 1.99
        conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.3)
        return ("daily_breakout", "long", tp_price, sl_price, min(10, conf))

    # SHORT break
    if last < range_low and last < bar_o:
        sl_retrace = bar_o - bar_range * 0.5
        sl_floor = price * (1 + MIN_SL_PCT)
        sl_price = max(sl_retrace, sl_floor)
        tp_price = price * 0.01
        conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.3)
        return ("daily_breakout", "short", tp_price, sl_price, min(10, conf))

    return None


def _generic_breakout(p, i1h, price, lookback, min_sl_pct, min_vol, atr_mult, name):
    """Parametric breakout sig generator (eliminates duplication across variants)."""
    if not p.has_1h or i1h < lookback + 30: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]
    if last <= 0: return None
    lo = max(0, i1h - lookback)
    range_high = float(np.max(p.h1h[lo:i1h]))
    range_low  = float(np.min(p.l1h[lo:i1h]))
    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < min_vol: return None
    atr_now = p.atr1h[i1h]
    if atr_now <= 0: return None
    atr_window = p.atr1h[max(0, i1h - 20):i1h]
    if len(atr_window) < 5:
        atr_avg = atr_now
    else:
        atr_avg = float(np.nanmean(atr_window))
    if atr_avg <= 0 or atr_now < atr_avg * atr_mult: return None
    bar_h = p.h1h[i1h]; bar_l = p.l1h[i1h]
    bar_range = bar_h - bar_l
    if bar_range <= 0: return None
    bar_o = p.c1h[i1h - 1] if i1h >= 1 else last
    if last > range_high and last > bar_o:
        sl_retrace = bar_o + bar_range * 0.5
        sl_floor = price * (1 - min_sl_pct)
        sl_price = min(sl_retrace, sl_floor)
        tp_price = price * 1.99
        conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
        return (name, "long", tp_price, sl_price, min(10, conf))
    if last < range_low and last < bar_o:
        sl_retrace = bar_o - bar_range * 0.5
        sl_floor = price * (1 + min_sl_pct)
        sl_price = max(sl_retrace, sl_floor)
        tp_price = price * 0.01
        conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
        return (name, "short", tp_price, sl_price, min(10, conf))
    return None


def sig_4h_breakout(p, i1h, price):
    """4-hour lookback breakout — fastest variant. Tight 1.2% SL, looser filters."""
    return _generic_breakout(p, i1h, price, 4, 0.012, 1.3, 1.0, "daily_breakout_4h")


def sig_12h_breakout(p, i1h, price):
    """12-hour lookback breakout — between 4h and 24h."""
    return _generic_breakout(p, i1h, price, 12, 0.018, 1.5, 1.0, "daily_breakout_12h")


def sig_48h_breakout(p, i1h, price):
    """48-hour (2-day) lookback breakout — between 24h and 168h."""
    return _generic_breakout(p, i1h, price, 48, 0.030, 1.9, 1.05, "daily_breakout_48h")


def sig_volume_capitulation(p, i1h, price):
    """When price drops >3% on >4x avg volume in a single bar, fade the move (mean revert).
    Also: if up >3% on >4x volume + RSI > 70, short the spike."""
    if not p.has_1h or i1h < 30: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]
    prev = p.c1h[i1h - 1]
    if last <= 0 or prev <= 0: return None
    bar_chg = (last - prev) / prev * 100
    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    rsi = p.rsi1h[i1h] if hasattr(p, 'rsi1h') and len(p.rsi1h) > i1h else 50
    # Bullish capitulation: price dropped >3% on huge volume + oversold
    if bar_chg < -3.0 and v_ratio > 4.0 and rsi < 30:
        sl_price = price * 0.985    # 1.5% below
        tp_price = price * 1.99
        return ("volume_capitulation", "long", tp_price, sl_price, 7 + int(v_ratio > 6))
    # Bearish capitulation: price spiked >3% on huge volume + overbought
    if bar_chg > 3.0 and v_ratio > 4.0 and rsi > 70:
        sl_price = price * 1.015
        tp_price = price * 0.01
        return ("volume_capitulation", "short", tp_price, sl_price, 7 + int(v_ratio > 6))
    return None


def sig_4h_breakout_trend(p, i1h, price):
    """4h breakout but only fires WITH the 50-EMA trend on 1H. Filters counter-trend trades."""
    if not p.has_1h or i1h < 60: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]
    if last <= 0: return None
    ema50 = p.e50_1h[i1h] if hasattr(p, "e50_1h") else None
    if ema50 is None or ema50 <= 0:
        return None
    res = _generic_breakout(p, i1h, price, 4, 0.012, 1.3, 1.0, "daily_breakout_4h_trend")
    if res is None:
        return None
    name, side, tp, sl, conf = res
    # Only allow LONG if price above 50-EMA, SHORT if below.
    if side == "long" and last < ema50:
        return None
    if side == "short" and last > ema50:
        return None
    return res


def sig_7d_breakout(p, i1h, price):
    """7-day (168h) lookback — same as daily_breakout but slightly looser ATR filter."""
    return _generic_breakout(p, i1h, price, 168, 0.04, 2.0, 1.05, "daily_breakout_7d")


def sig_2h_breakout(p, i1h, price):
    """2-hour lookback — sub-hour scalp. Aggressive."""
    return _generic_breakout(p, i1h, price, 2, 0.008, 1.2, 1.0, "daily_breakout_2h")


def sig_8h_breakout(p, i1h, price):
    """8-hour lookback — between 4h and 12h."""
    return _generic_breakout(p, i1h, price, 8, 0.015, 1.4, 1.0, "daily_breakout_8h")


def sig_asian_pump(p, i1h, price):
    """Time-of-day momentum: 02:00-05:00 UTC + 1H |% chg| > 1.5% + 3x volume."""
    if not p.has_1h or i1h < 30: return None
    if i1h >= len(p.c1h): return None
    ts = p.ts1h[i1h]
    # Convert ms timestamp to UTC hour
    import datetime as _dt
    hour = _dt.datetime.fromtimestamp(ts / 1000, tz=_dt.timezone.utc).hour
    if not (2 <= hour < 5):
        return None
    last = p.c1h[i1h]; prev = p.c1h[i1h - 1]
    if last <= 0 or prev <= 0: return None
    pct = (last - prev) / prev
    if abs(pct) < 0.015:
        return None
    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < 3.0:
        return None
    if pct > 0:
        sl_price = price * 0.975
        tp_price = price * 1.99
        return ("asian_pump", "long", tp_price, sl_price, 7 + int(v_ratio > 5))
    sl_price = price * 1.025
    tp_price = price * 0.01
    return ("asian_pump", "short", tp_price, sl_price, 7 + int(v_ratio > 5))


def sig_pump_dump_reversal(p, i1h, price):
    """Fade extreme 8%+ 1H moves with RSI extreme + 3x volume."""
    if not p.has_1h or i1h < 30: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]; prev = p.c1h[i1h - 1]
    if last <= 0 or prev <= 0: return None
    pct = (last - prev) / prev
    if abs(pct) < 0.08:
        return None
    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < 3.0:
        return None
    r = p.rsi1h[i1h] if hasattr(p, 'rsi1h') and len(p.rsi1h) > i1h else 50
    if pct > 0.08 and r > 80:
        sl_price = price * 1.04
        tp_price = price * (1 - abs(pct) * 0.5)   # 50% retrace target
        return ("pump_dump_reversal", "short", tp_price, sl_price, 7 + int(v_ratio > 5))
    if pct < -0.08 and r < 20:
        sl_price = price * 0.96
        tp_price = price * (1 + abs(pct) * 0.5)
        return ("pump_dump_reversal", "long", tp_price, sl_price, 7 + int(v_ratio > 5))
    return None


def sig_macd_cross(p, i1h, price):
    """MACD line crosses above/below signal line + volume confirmation."""
    if not p.has_1h or i1h < 50: return None
    if i1h >= len(p.c1h): return None
    if not (hasattr(p, 'macd_line_1h') and hasattr(p, 'macd_sig_1h')):
        return None
    if i1h - 1 < 0:
        return None
    prev_diff = p.macd_line_1h[i1h - 1] - p.macd_sig_1h[i1h - 1]
    cur_diff  = p.macd_line_1h[i1h] - p.macd_sig_1h[i1h]
    bull = prev_diff <= 0 and cur_diff > 0
    bear = prev_diff >= 0 and cur_diff < 0
    if not (bull or bear):
        return None
    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < 1.3:
        return None
    atr_now = p.atr1h[i1h] if hasattr(p, 'atr1h') and len(p.atr1h) > i1h else None
    if atr_now is None or atr_now <= 0:
        return None
    if bull:
        sl_price = price - 1.5 * atr_now
        tp_price = price + 3 * atr_now
        return ("macd_cross", "long", tp_price, sl_price, 7 + int(v_ratio > 2))
    sl_price = price + 1.5 * atr_now
    tp_price = price - 3 * atr_now
    return ("macd_cross", "short", tp_price, sl_price, 7 + int(v_ratio > 2))


def sig_24h_breakout(p: PrecomputedData, i1h: int, price: float):
    """24h-lookback variant of daily_breakout. Same logic, smaller window → more signals."""
    LOOKBACK = 24
    MIN_SL_PCT = 0.025
    MIN_VOL = 1.8
    if not p.has_1h or i1h < LOOKBACK + 30: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]
    if last <= 0: return None

    lo = max(0, i1h - LOOKBACK)
    range_high = float(np.max(p.h1h[lo:i1h]))
    range_low  = float(np.min(p.l1h[lo:i1h]))

    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < MIN_VOL: return None

    atr_now = p.atr1h[i1h]
    if atr_now <= 0: return None
    atr_window = p.atr1h[max(0, i1h - 20):i1h]
    if len(atr_window) < 5:
        atr_avg = atr_now
    else:
        atr_avg = float(np.nanmean(atr_window))
    if atr_avg <= 0 or atr_now < atr_avg * 1.05: return None

    bar_h = p.h1h[i1h]
    bar_l = p.l1h[i1h]
    bar_range = bar_h - bar_l
    if bar_range <= 0: return None
    bar_o = p.c1h[i1h - 1] if i1h >= 1 else last

    if last > range_high and last > bar_o:
        sl_retrace = bar_o + bar_range * 0.5
        sl_floor = price * (1 - MIN_SL_PCT)
        sl_price = min(sl_retrace, sl_floor)
        tp_price = price * 1.99
        conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
        return ("daily_breakout_24h", "long", tp_price, sl_price, min(10, conf))

    if last < range_low and last < bar_o:
        sl_retrace = bar_o - bar_range * 0.5
        sl_floor = price * (1 + MIN_SL_PCT)
        sl_price = max(sl_retrace, sl_floor)
        tp_price = price * 0.01
        conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
        return ("daily_breakout_24h", "short", tp_price, sl_price, min(10, conf))

    return None


def sig_supertrend(p: PrecomputedData, i1h: int, price: float):
    """Supertrend flip on 1H bars. Trend = HL2 +/- ATR×3. Enter on flip + volume confirm.
    Same trailing-stop philosophy as daily_breakout. Wide stops, fee-immune."""
    if not p.has_1h or i1h < 30: return None
    if i1h >= len(p.c1h): return None
    MULT = 3.0
    last = p.c1h[i1h]
    prev = p.c1h[i1h - 1]
    if last <= 0 or prev <= 0: return None

    atr_now = p.atr1h[i1h]
    atr_prev = p.atr1h[i1h - 1] if i1h >= 1 else atr_now
    if atr_now <= 0 or atr_prev <= 0: return None

    hl2 = (p.h1h[i1h] + p.l1h[i1h]) * 0.5
    hl2_prev = (p.h1h[i1h - 1] + p.l1h[i1h - 1]) * 0.5

    upper = hl2 + MULT * atr_now
    lower = hl2 - MULT * atr_now
    upper_prev = hl2_prev + MULT * atr_prev
    lower_prev = hl2_prev - MULT * atr_prev

    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v
    if v_ratio < 1.0: return None   # loosened from 1.3

    # LONG flip: bar closed above upper band (was below previously)
    crossed_up   = (prev <= upper_prev) and (last > upper)
    crossed_down = (prev >= lower_prev) and (last < lower)
    if crossed_up:
        sl_price = lower * 0.99
        tp_price = price * 1.99
        return ("supertrend", "long", tp_price, sl_price, 7)

    # SHORT flip
    if crossed_down:
        sl_price = upper * 1.01
        tp_price = price * 0.01
        return ("supertrend", "short", tp_price, sl_price, 7)

    return None


def sig_trend_pullback(p: PrecomputedData, i1h: int, price: float):
    """1h trend-pullback: confirmed uptrend + pullback to 50 EMA + bullish reversal candle.
    Wide stops (max(2.5%, 2×ATR)), trailing-only exit (no fixed TP)."""
    if not p.has_1h or i1h < 220: return None
    if i1h >= len(p.c1h): return None

    # Compute EMAs locally — PrecomputedData has e9/21/50_1h but no 200
    # Use a rolling computation off the 1h close array for ema200
    # For efficiency in backtest, approximate with simple long-window mean (close enough for filter)
    lo200 = max(0, i1h - 200)
    e200 = float(np.mean(p.c1h[lo200:i1h + 1]))   # crude EMA200 proxy — ok for trend filter
    e50  = p.e50_1h[i1h]
    e21  = p.e21_1h[i1h]
    if e200 <= 0 or e50 <= 0 or e21 <= 0: return None

    last = p.c1h[i1h]
    # PrecomputedData doesn't store 1h opens — use bar mid-point as bullish/bearish proxy:
    #   bar closes in upper half of its high-low range = bullish; lower half = bearish.
    h_now = p.h1h[i1h]
    l_now = p.l1h[i1h]
    mid_now = (h_now + l_now) / 2 if (h_now + l_now) > 0 else last
    bar2_green = last > mid_now
    bar2_red   = last < mid_now

    # Volume confirm
    avg_v = p.avg_v1h[i1h]
    if avg_v <= 0: return None
    v_ratio = p.v1h[i1h] / avg_v

    # ATR
    atr_v = p.atr1h[i1h]
    if atr_v <= 0: return None

    # RSI
    r = p.rsi1h[i1h]

    macro_up   = e50 > e200 * 1.001 and last > e200 * 1.005
    macro_down = e50 < e200 * 0.999 and last < e200 * 0.995

    pull_long  = abs(last - e50) / e50 < 0.010 and last >= e50 * 0.995
    pull_short = abs(last - e50) / e50 < 0.010 and last <= e50 * 1.005

    if macro_up and pull_long and bar2_green and 40 <= r <= 65 and v_ratio >= 1.2:
        sl_distance = max(0.025 * price, 2.0 * atr_v)
        sl_price = price - sl_distance
        tp_price = price * 1.99   # cosmetic — trailing exits first
        conf = 7 + int(last > e21) + int(v_ratio >= 1.8) + int(50 <= r <= 60)
        return ("trend_pullback", "long", tp_price, sl_price, min(10, conf))

    if macro_down and pull_short and bar2_red and 35 <= r <= 60 and v_ratio >= 1.2:
        sl_distance = max(0.025 * price, 2.0 * atr_v)
        sl_price = price + sl_distance
        tp_price = price * 0.01
        conf = 7 + int(last < e21) + int(v_ratio >= 1.8) + int(40 <= r <= 50)
        return ("trend_pullback", "short", tp_price, sl_price, min(10, conf))

    return None


def sig_rsi_divergence(p: PrecomputedData, i1h: int, price: float):
    """Bullish/bearish RSI divergence on 1h timeframe."""
    if not p.has_1h or i1h < 50: return None
    if i1h >= len(p.rsi1h): return None
    # Look at last 30 bars for swing points
    lo = max(0, i1h - 30); hi = i1h + 1
    prices = p.c1h[lo:hi]
    rsis = p.rsi1h[lo:hi]
    if len(prices) < 20: return None

    N = 3
    swing_lows = []
    swing_highs = []
    for i in range(N, len(prices) - N):
        if prices[i] == min(prices[i-N:i+N+1]):
            swing_lows.append((i, prices[i], rsis[i]))
        if prices[i] == max(prices[i-N:i+N+1]):
            swing_highs.append((i, prices[i], rsis[i]))

    cur_price = p.c1h[i1h]

    # Bullish divergence
    if len(swing_lows) >= 2:
        (i1, p1, r1), (i2, p2, r2) = swing_lows[-2], swing_lows[-1]
        if (p2 < p1 and r2 > r1 + 3 and r2 < 45 and r1 < 40
            and cur_price > p2 * 1.003):
            conf = 8 + int(r2 - r1 > 8) + int(p1 - p2 > p1 * 0.02)
            return ("rsi_divergence", "long", price * 1.045, price * 0.980, min(10, conf))

    # Bearish divergence
    if len(swing_highs) >= 2:
        (i1, p1, r1), (i2, p2, r2) = swing_highs[-2], swing_highs[-1]
        if (p2 > p1 and r2 < r1 - 3 and r2 > 55 and r1 > 60
            and cur_price < p2 * 0.997):
            conf = 8 + int(r1 - r2 > 8) + int(p2 - p1 > p1 * 0.02)
            return ("rsi_divergence", "short", price * 0.955, price * 1.020, min(10, conf))

    return None


# ── simulation ────────────────────────────────────────────────────────────────
def _detect_regime(p: PrecomputedData, i15: int) -> str:
    """Cheap ADX-based regime detect for backtest. Mirrors bot.py classification."""
    if i15 < 30:
        return "RANGING"
    # Use ATR/price as volatility proxy; rolling std as trendiness proxy
    atr = p.atr15[i15]
    price = p.c15[i15]
    if price <= 0 or atr <= 0:
        return "RANGING"
    vol_pct = atr / price * 100
    # Mean ATR over last 100 bars
    lookback = max(0, i15 - 100)
    atr_window = p.atr15[lookback:i15 + 1]
    if len(atr_window) < 10:
        return "RANGING"
    mean_atr = float(np.nanmean(atr_window))
    if mean_atr <= 0:
        return "RANGING"
    if vol_pct > 2.0 * (mean_atr / price * 100):
        return "VOLATILE"
    # EMA-stack proxy for trending: e9 vs e21 vs e50
    if p.e9_15[i15] > p.e21_15[i15] > p.e50_15[i15]:
        return "TRENDING"
    if p.e9_15[i15] < p.e21_15[i15] < p.e50_15[i15]:
        return "TRENDING"
    return "RANGING"


DONCHIAN_WHITELIST = {"ETH-USDT", "ARB-USDT", "INJ-USDT", "NEAR-USDT", "DOT-USDT",
                      "TIA-USDT", "AVAX-USDT", "ADA-USDT", "LINK-USDT"}


# ── NEW AGENT SIGNAL FUNCTIONS (2026-06-03) ──────────────────────────────────

def _stoch_of(s: np.ndarray, period: int = 14, i: int = -1):
    """Stochastic of a series: (val - min) / (max - min) over period."""
    w = s[max(0, i - period + 1):i + 1]
    if len(w) < 3: return np.nan
    rng = w.max() - w.min()
    return (s[i] - w.min()) / rng if rng > 0 else np.nan


def sig_connors_rsi2(p, i5, price):
    """Connors RSI2: extreme RSI2 (<5 long, >95 short) + trend filter."""
    if i5 < 30: return None
    if i5 >= len(p.c5): return None
    r2 = p.rsi2_5[i5]
    if np.isnan(r2): return None
    last = p.c5[i5]
    atr_v = p.atr5[i5]
    if atr_v <= 0 or np.isnan(atr_v): return None

    # Trend slope from EMA21
    if i5 >= 5 and not np.isnan(p.e21_5[i5]) and not np.isnan(p.e21_5[i5-5]):
        trend_slope = (p.e21_5[i5] - p.e21_5[i5-5]) / max(abs(p.e21_5[i5-5]), 0.01)
    else:
        trend_slope = 0

    avg_v = p.avg_v5[i5] if i5 < len(p.avg_v5) else 1
    v_ratio = p.v5[i5] / avg_v if avg_v > 0 else 0

    if r2 < 5 and trend_slope > -0.01:
        sl = last - 1.5 * atr_v; tp = last + 4.5 * atr_v
        conf = min(10, 7 + int(v_ratio > 2.0) + int(r2 < 2))
        return ("connors_rsi2", "long", tp, sl, conf)
    if r2 > 95 and trend_slope < 0.01:
        sl = last + 1.5 * atr_v; tp = last - 4.5 * atr_v
        conf = min(10, 7 + int(v_ratio > 2.0) + int(r2 > 98))
        return ("connors_rsi2", "short", tp, sl, conf)
    return None


def sig_stoch_rsi(p, i1h, price):
    """Stochastic RSI: extreme stoch cross with RSI confirmation."""
    if not p.has_1h or i1h < 30: return None
    if i1h >= len(p.c1h): return None
    r = p.rsi1h
    stoch_now = _stoch_of(r, 14, i1h)
    stoch_prev = _stoch_of(r, 14, i1h - 1)
    if np.isnan(stoch_now) or np.isnan(stoch_prev): return None
    last = p.c1h[i1h]
    rsi_now = r[i1h]

    if stoch_prev < 0.20 and stoch_now > 0.20 and rsi_now < 40:
        sl = last * 0.975; tp = last * 1.03
        conf = 8 if stoch_now > 0.30 else 7
        return ("stoch_rsi", "long", tp, sl, conf)
    if stoch_prev > 0.80 and stoch_now < 0.80 and rsi_now > 60:
        sl = last * 1.025; tp = last * 0.97
        conf = 8 if stoch_now < 0.70 else 7
        return ("stoch_rsi", "short", tp, sl, conf)
    return None


def sig_bb_bounce(p, i5, price):
    """Bollinger Band bounce: price at lower BB + RSI recovery."""
    if i5 < 30: return None
    if i5 >= len(p.c5): return None
    last = p.c5[i5]; bbl = p.bbl5[i5]; bbu = p.bbu5[i5]
    if np.isnan(bbl) or np.isnan(bbu): return None
    bbw = (bbu - bbl) / max(last, 0.01)
    if bbw < 0.015: return None  # too narrow
    r = p.rsi5[i5]
    if np.isnan(r): return None
    avg_v = p.avg_v5[i5] if i5 < len(p.avg_v5) else 1
    v_ratio = p.v5[i5] / avg_v if avg_v > 0 else 0

    # Long: price <= lower BB + RSI oversold
    if last <= bbl * 1.005 and r < 35:
        sl = last * 0.99; tp = last * 1.015
        conf = min(10, 7 + int(v_ratio > 1.5) + int(r < 25))
        return ("bb_bounce", "long", tp, sl, conf)
    # Short: price >= upper BB + RSI overbought
    if last >= bbu * 0.995 and r > 65:
        sl = last * 1.01; tp = last * 0.985
        conf = min(10, 7 + int(v_ratio > 1.5) + int(r > 75))
        return ("bb_bounce", "short", tp, sl, conf)
    return None


def sig_zscore_reversion(p, i5, price):
    """Z-score reversion: price extended >2σ from 20-bar mean, fade back."""
    if i5 < 30: return None
    if i5 >= len(p.c5): return None
    last = p.c5[i5]
    # Rolling 20-bar stats
    w = p.c5[max(0,i5-20):i5+1]
    mean = np.nanmean(w); std = np.nanstd(w)
    if std <= 0: return None
    z = (last - mean) / std
    if abs(z) < 1.8: return None
    r = p.rsi5[i5]
    if np.isnan(r): return None
    # Long: z < -1.8, RSI recovering
    if z < -1.8 and r > 25:
        sl = last * 0.992; tp = last * 1.012
        return ("zscore_reversion", "long", tp, sl, 7 + int(z < -3))
    if z > 1.8 and r < 75:
        sl = last * 1.008; tp = last * 0.988
        return ("zscore_reversion", "short", tp, sl, 7 + int(z > 3))
    return None


def sig_hurst_regime(p, i1h, price):
    """Hurst regime: detect trending vs mean-reverting via RS analysis proxy."""
    if not p.has_1h or i1h < 60: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]; r = p.rsi1h[i1h]
    if np.isnan(r): return None
    # Simplified: RSI extreme + volume confirm
    avg_v = p.avg_v1h[i1h] if i1h < len(p.avg_v1h) else 1
    v_ratio = p.v1h[i1h] / avg_v if avg_v > 0 else 0
    if v_ratio < 0.8: return None

    if r < 30:
        sl = last * 0.985; tp = last * 1.025
        return ("hurst_regime", "long", tp, sl, 7 + int(r < 20))
    if r > 70:
        sl = last * 1.015; tp = last * 0.975
        return ("hurst_regime", "short", tp, sl, 7 + int(r > 80))
    return None


def sig_fibonacci(p, i1h, price):
    """Fibonacci retracement: entry at golden-ratio (0.618/0.786) swing levels."""
    if not p.has_1h or i1h < 100: return None
    if i1h >= len(p.c1h): return None
    last = p.c1h[i1h]
    # Find recent swing high/low (50-bar lookback)
    start = max(0, i1h - 50)
    h_swing = np.max(p.h1h[start:i1h+1])
    l_swing = np.min(p.l1h[start:i1h+1])
    rng = h_swing - l_swing
    if rng <= 0: return None

    # Retracement levels
    fib_618_long = h_swing - rng * 0.618
    fib_786_long = h_swing - rng * 0.786
    fib_618_short = l_swing + rng * 0.618
    fib_786_short = l_swing + rng * 0.786

    r = p.rsi1h[i1h]
    if np.isnan(r): return None

    # Long: price near 0.786 retrace + RSI < 35
    if fib_786_long * 0.995 <= last <= fib_618_long * 1.005 and r < 35:
        sl = last * 0.97; tp = last * 1.99
        return ("fibonacci", "long", tp, sl, 7 + int(r < 25))
    # Short: price near 0.786 retrace + RSI > 65
    if fib_618_short * 0.995 <= last <= fib_786_short * 1.005 and r > 65:
        sl = last * 1.03; tp = last * 0.01
        return ("fibonacci", "short", tp, sl, 7 + int(r > 75))
    return None


def sig_golden_hour(p, i1h, price):
    """Golden hour: time-of-day mean-rev. US open 13:30-16:00 UTC, fade extremes."""
    if not p.has_1h or i1h < 30: return None
    if i1h >= len(p.c1h): return None
    ts = p.ts1h[i1h]
    hour = __import__('datetime').datetime.fromtimestamp(ts/1000, tz=__import__('datetime').timezone.utc).hour
    if not (13 <= hour < 16): return None
    last = p.c1h[i1h]
    atr_v = p.atr1h[i1h]
    if np.isnan(atr_v) or atr_v <= 0: return None
    r = p.rsi1h[i1h]
    if np.isnan(r): return None
    avg_v = p.avg_v1h[i1h] if i1h < len(p.avg_v1h) else 1
    v_ratio = p.v1h[i1h] / avg_v if avg_v > 0 else 0

    if r < 30 and v_ratio > 1.2:
        sl = last * 0.98; tp = last * 1.03
        return ("golden_hour", "long", tp, sl, min(10, 7 + int(r < 20)))
    if r > 70 and v_ratio > 1.2:
        sl = last * 1.02; tp = last * 0.97
        return ("golden_hour", "short", tp, sl, min(10, 7 + int(r > 80)))
    return None


def sig_viki(p, i15, price):
    """Viki: 9/21 EMA crossover on 15m + 50 EMA alignment. Backtest-optimized."""
    if i15 < 52: return None
    if i15 >= len(p.c15): return None
    e9_n = p.e9_15[i15]; e21_n = p.e21_15[i15]; e50_n = p.e50_15[i15]
    e9_p = p.e9_15[i15-1]; e21_p = p.e21_15[i15-1]
    if any(np.isnan(x) for x in [e9_n,e21_n,e50_n,e9_p,e21_p]): return None

    prev_diff = e9_p - e21_p
    cur_diff  = e9_n - e21_n
    bullish = prev_diff <= 0 and cur_diff > 0
    bearish = prev_diff >= 0 and cur_diff < 0
    if not (bullish or bearish): return None

    last = p.c15[i15]
    avg_v = p.avg_v15[i15] if i15 < len(p.avg_v15) else 1
    v_ratio = p.v15[i15] / avg_v if avg_v > 0 else 0
    if v_ratio < 0.8: return None

    if bullish and e9_n > e50_n and e21_n > e50_n:
        sl = last * 0.93; tp = last * 99.0  # 7% SL, trailing-only TP
        conf = min(10, 7 + int(v_ratio > 1.5) + int(last > e50_n * 1.01))
        return ("viki", "long", tp, sl, conf)
    if bearish and e9_n < e50_n and e21_n < e50_n:
        sl = last * 1.07; tp = last * 0.01
        conf = min(10, 7 + int(v_ratio > 1.5) + int(last < e50_n * 0.99))
        return ("viki", "short", tp, sl, conf)
    return None


def sig_funding_extremes(p, i15, price):
    """Funding extremes: detect oversold/overbought via RSI + BB extreme (proxy)."""
    if i15 < 30: return None
    if i15 >= len(p.c15): return None
    last = p.c15[i15]; r = p.rsi15[i15]
    if np.isnan(r): return None
    bbu = p.bbu15[i15]; bbl = p.bbl15[i15]
    if np.isnan(bbu) or np.isnan(bbl): return None
    avg_v = p.avg_v15[i15] if i15 < len(p.avg_v15) else 1
    v_ratio = p.v15[i15] / avg_v if avg_v > 0 else 0

    # Long: RSI extreme low + near lower BB
    if r < 30 and last <= bbl * 1.02 and v_ratio > 1.0:
        sl = last * 0.97; tp = last * 1.04
        conf = min(10, 7 + int(r < 20) + int(v_ratio > 1.5))
        return ("funding_extremes", "long", tp, sl, conf)
    # Short: RSI extreme high + near upper BB
    if r > 70 and last >= bbu * 0.98 and v_ratio > 1.0:
        sl = last * 1.03; tp = last * 0.96
        conf = min(10, 7 + int(r > 80) + int(v_ratio > 1.5))
        return ("funding_extremes", "short", tp, sl, conf)
    return None


def simulate(p: PrecomputedData, funding_rate: float = 0.0,
             use_trailing: bool = True, use_regime_filter: bool = True,
             global_concurrency_cap: int = 5, symbol: str = "") -> List[dict]:
    """
    Walk 15m bars. At each bar:
      1. Update high/low water marks; ratchet trailing stop if active
      2. Check open trades for SL/TP/timeout hits (using current trailing stop)
      3. Generate signals → open trades at next-bar open (with regime filter)

    v2 changes (vs original):
      - Trailing stops mirroring bot.py (activate threshold + trail %)
      - Per-agent max_hold_min from PROFILES (was hardcoded 192 bars)
      - Regime filter: agents only fire in valid_regimes
      - Global concurrency cap (bot.py uses 5 across all agents per symbol)
    """
    closed: List[dict] = []
    open_trades: Dict[str, dict] = {}   # agent → trade dict

    for i15 in range(p.n15):
        ts  = p.ts15[i15]
        bh  = p.h15[i15]
        bl  = p.l15[i15]
        bc  = p.c15[i15]

        # ── 1. Check open trades (and update trailing stops) ──
        # CONSERVATIVE ordering within a bar:
        #   - assume adverse extreme touched first (low for long, high for short)
        #   - SL/trail check first → if not hit, then update watermark and ratchet
        # This is the worst-case-for-trader assumption matching the original code.
        to_close = []
        for agent, t in open_trades.items():
            prof = PROFILES.get(t["profile"], PROFILES["momentum"])
            hit_sl = hit_tp = False
            current_stop = t["current_stop"]

            if t["side"] == "long":
                # Conservative: adverse low first
                if bl <= current_stop:
                    hit_sl = True
                elif bh >= t["tp"]:
                    hit_tp = True
                # If neither hit, update watermark and ratchet
                if not hit_sl and not hit_tp:
                    new_high = max(t["high_water"], bh)
                    t["high_water"] = new_high
                    if use_trailing:
                        activation = t["entry"] * (1 + prof["activate"] / 100)
                        if new_high >= activation:
                            trailing = new_high * (1 - prof["trail"] / 100)
                            if trailing > t["current_stop"]:
                                t["current_stop"] = trailing
            else:  # short
                if bh >= current_stop:
                    hit_sl = True
                elif bl <= t["tp"]:
                    hit_tp = True
                if not hit_sl and not hit_tp:
                    new_low = min(t["low_water"], bl)
                    t["low_water"] = new_low
                    if use_trailing:
                        activation = t["entry"] * (1 - prof["activate"] / 100)
                        if new_low <= activation:
                            trailing = new_low * (1 + prof["trail"] / 100)
                            if trailing < t["current_stop"]:
                                t["current_stop"] = trailing

            # Per-agent max-hold timeout (bars)
            max_bars = max(1, int(prof["max_hold_min"] / 15))
            bars_held = i15 - t["open_i"]

            if hit_tp:
                to_close.append((agent, t["tp"], "tp"))
            elif hit_sl:
                # exit at the stop level (could be initial SL or trailing)
                to_close.append((agent, current_stop, "trailing_stop" if current_stop != t["initial_sl"] else "sl"))
            elif bars_held >= max_bars:
                to_close.append((agent, bc, "timeout"))

        for agent, exit_px, reason in to_close:
            t = open_trades.pop(agent)
            sign = 1 if t["side"] == "long" else -1
            raw  = sign * (exit_px - t["entry"]) / t["entry"]
            # Risk is computed against INITIAL stop (the R-unit definition)
            risk = abs(t["entry"] - t["initial_sl"]) / t["entry"]
            net  = raw - TAKER_FEE * 2
            r_mult = net / risk if risk > 0 else 0.0
            hold_min = (ts - t["open_ts"]) / 60_000
            closed.append({
                "agent": agent, "side": t["side"],
                "entry": t["entry"], "exit": exit_px, "reason": reason,
                "r_multiple": r_mult, "hold_min": hold_min,
                "open_ts": t["open_ts"], "exit_ts": ts,
            })

        # ── 2. Generate signals at this bar; entry = next bar open ──
        if i15 + 1 >= p.n15:
            continue
        next_open = p.o15[i15 + 1]
        next_ts   = p.ts15[i15 + 1]
        if next_open <= 0:
            continue

        i5  = p.i5_for(ts)
        i1h = p.i1h_for(ts)

        # Regime classification (used to filter agents)
        regime = _detect_regime(p, i15) if use_regime_filter else None

        generators = [
            ("scalp",          lambda: sig_scalp(p, i5, next_open)),
            ("momentum",       lambda: sig_momentum(p, i15, next_open)),
            ("swing",          lambda: sig_swing(p, i1h, next_open)),
            ("meanrev",        lambda: sig_meanrev(p, i5, next_open)),
            ("asymmetric",     lambda: sig_asymmetric(p, i15, i1h, next_open)),
            ("bb_squeeze",     lambda: sig_bb_squeeze(p, i5, next_open)),
            ("donchian",       lambda: sig_donchian(p, i1h, next_open) if symbol in DONCHIAN_WHITELIST else None),
            ("funding",        lambda: sig_funding(p, i5, next_open, funding_rate)),
            ("ema_ribbon",     lambda: sig_ema_ribbon(p, i5, i1h, next_open)),
            ("candlestick",    lambda: sig_candlestick(p, i15, next_open)),
            ("rsi_divergence", lambda: sig_rsi_divergence(p, i1h, next_open)),
            ("trend_pullback", lambda: sig_trend_pullback(p, i1h, next_open)),
            ("daily_breakout", lambda: sig_daily_breakout(p, i1h, next_open)),
            ("daily_breakout_24h", lambda: sig_24h_breakout(p, i1h, next_open)),
            ("daily_breakout_4h",  lambda: sig_4h_breakout(p, i1h, next_open)),
            ("daily_breakout_12h", lambda: sig_12h_breakout(p, i1h, next_open)),
            ("daily_breakout_48h", lambda: sig_48h_breakout(p, i1h, next_open)),
            ("daily_breakout_2h",  lambda: sig_2h_breakout(p, i1h, next_open)),
            ("daily_breakout_8h",  lambda: sig_8h_breakout(p, i1h, next_open)),
            ("asian_pump",         lambda: sig_asian_pump(p, i1h, next_open)),
            ("pump_dump_reversal", lambda: sig_pump_dump_reversal(p, i1h, next_open)),
            ("macd_cross",         lambda: sig_macd_cross(p, i1h, next_open)),
            ("volume_capitulation", lambda: sig_volume_capitulation(p, i1h, next_open)),
            # ("daily_breakout_4h_trend", ...) — tested, strictly worse than vanilla; kept code for future tuning
            ("daily_breakout_7d",  lambda: sig_7d_breakout(p, i1h, next_open)),
            ("supertrend",     lambda: sig_supertrend(p, i1h, next_open)),
            # ── New agents (2026-06-03) ──
            ("connors_rsi2",   lambda: sig_connors_rsi2(p, i5, next_open)),
            ("stoch_rsi",      lambda: sig_stoch_rsi(p, i1h, next_open)),
            ("bb_bounce",      lambda: sig_bb_bounce(p, i5, next_open)),
            ("zscore_reversion", lambda: sig_zscore_reversion(p, i5, next_open)),
            ("hurst_regime",   lambda: sig_hurst_regime(p, i1h, next_open)),
            ("fibonacci",      lambda: sig_fibonacci(p, i1h, next_open)),
            ("golden_hour",    lambda: sig_golden_hour(p, i1h, next_open)),
            ("viki",           lambda: sig_viki(p, i15, next_open)),
            ("funding_extremes", lambda: sig_funding_extremes(p, i15, next_open)),
        ]

        for agent_name, gen in generators:
            # Global concurrency cap (per symbol)
            if len(open_trades) >= global_concurrency_cap:
                break
            # Regime filter
            if use_regime_filter and regime is not None:
                valid = AGENT_VALID_REGIMES.get(agent_name, [])
                if valid and regime not in valid:
                    continue
            try:
                res = gen()
            except Exception:
                continue
            if not res:
                continue
            agent, side, tp, sl, conf = res
            if agent in open_trades:
                continue
            profile_name = AGENT_TO_PROFILE.get(agent, "momentum")
            open_trades[agent] = {
                "side": side, "entry": next_open,
                "tp": tp, "initial_sl": sl, "current_stop": sl,
                "high_water": next_open, "low_water": next_open,
                "profile": profile_name,
                "open_i": i15 + 1, "open_ts": next_ts,
            }

    # ── 3. Force-close remaining at last bar ──
    last_px = p.c15[-1]; last_ts = p.ts15[-1]
    for agent, t in open_trades.items():
        sign = 1 if t["side"] == "long" else -1
        raw  = sign * (last_px - t["entry"]) / t["entry"]
        risk = abs(t["entry"] - t["initial_sl"]) / t["entry"]
        net  = raw - TAKER_FEE * 2
        closed.append({
            "agent": agent, "side": t["side"],
            "entry": t["entry"], "exit": last_px, "reason": "end_of_data",
            "r_multiple": net / risk if risk > 0 else 0.0,
            "hold_min": (last_ts - t["open_ts"]) / 60_000,
            "open_ts": t["open_ts"], "exit_ts": last_ts,
        })

    return closed


# ── metrics ───────────────────────────────────────────────────────────────────
def compute_metrics(agent: str, all_trades: List[dict]) -> dict:
    t = [x for x in all_trades if x["agent"] == agent]
    if not t:
        return {"agent": agent, "total_trades": 0,
                "win_rate": 0, "avg_r": 0, "expectancy_r": 0,
                "profit_factor": 0, "max_dd_pct": 0,
                "max_dd_dur_days": 0, "sharpe": 0,
                "best_month_pct": 0, "worst_month_pct": 0,
                "avg_hold_min": 0, "_equity": [NOTIONAL], "_trades": []}

    rs    = np.array([x["r_multiple"] for x in t])
    wins  = rs[rs > 0]
    loss  = rs[rs <= 0]
    n     = len(rs)
    wr    = len(wins) / n
    avg_r = float(rs.mean())
    gw    = float(wins.sum())
    gl    = float(abs(loss.sum()))
    pf    = gw / gl if gl > 0 else float("inf")

    # Equity curve — fixed notional (kept for backward-compat; breaks > 100% DD)
    eq = [NOTIONAL]
    for x in sorted(t, key=lambda z: z["open_ts"]):
        pnl = x["r_multiple"] * NOTIONAL * 0.01
        eq.append(eq[-1] + pnl)
    eq = np.array(eq)
    peak = np.maximum.accumulate(eq)
    dd   = (eq - peak) / np.where(peak>0, peak, 1) * 100
    max_dd = float(dd.min())

    # Equity curve — % risk per trade (correct model: 1% risk, stops at 5% of start)
    HALT = NOTIONAL * 0.05
    eq_pct = [NOTIONAL]
    for x in sorted(t, key=lambda z: z["open_ts"]):
        cur = eq_pct[-1]
        if cur <= HALT:
            eq_pct.append(cur)
            continue
        pnl = x["r_multiple"] * cur * 0.01
        eq_pct.append(max(HALT, cur + pnl))
    eq_pct = np.array(eq_pct)
    peak_pct = np.maximum.accumulate(eq_pct)
    dd_pct   = (eq_pct - peak_pct) / np.where(peak_pct > 0, peak_pct, 1) * 100
    max_dd_pct_equity = float(dd_pct.min())

    # DD duration
    in_dd = False; dd_s = 0; max_dur = 0
    for j, d in enumerate(dd):
        if d < -0.5 and not in_dd: in_dd=True; dd_s=j
        if d >= -0.5 and in_dd:    in_dd=False; max_dur=max(max_dur,j-dd_s)
    dd_days = max_dur * 15 / 1440

    # Sharpe
    daily: Dict[str, float] = {}
    for x in t:
        day = datetime.fromtimestamp(x["exit_ts"]/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        daily[day] = daily.get(day, 0.0) + x["r_multiple"] * 0.01
    dr = np.array(list(daily.values()))
    sharpe = (dr.mean()/dr.std()*np.sqrt(252)) if len(dr)>=2 and dr.std()>0 else 0.0

    # Monthly
    monthly: Dict[str, float] = {}
    for x in t:
        ym = datetime.fromtimestamp(x["exit_ts"]/1000, tz=timezone.utc).strftime("%Y-%m")
        monthly[ym] = monthly.get(ym, 0.0) + x["r_multiple"] * 0.01 * 100
    best_m  = max(monthly.values()) if monthly else 0.0
    worst_m = min(monthly.values()) if monthly else 0.0

    # Per-symbol breakdown (only when symbol is tagged)
    by_sym: Dict[str, dict] = {}
    for x in t:
        sym = x.get("symbol", "?")
        if sym not in by_sym:
            by_sym[sym] = {"n": 0, "wins": 0, "exp": 0.0}
        by_sym[sym]["n"] += 1
        if x["r_multiple"] > 0:
            by_sym[sym]["wins"] += 1
        by_sym[sym]["exp"] += x["r_multiple"]
    per_symbol = []
    for sym, d in by_sym.items():
        if d["n"] > 0:
            per_symbol.append({
                "symbol": sym,
                "trades": d["n"],
                "win_rate": round(100 * d["wins"] / d["n"], 1),
                "expectancy_r": round(d["exp"] / d["n"], 3),
                "total_r": round(d["exp"], 2),
            })
    per_symbol.sort(key=lambda r: -r["expectancy_r"])

    return {
        "agent":           agent,
        "total_trades":    n,
        "wins":            len(wins),
        "losses":          len(loss),
        "win_rate":        round(wr*100, 1),
        "avg_winner_r":    round(float(wins.mean()) if len(wins) else 0, 3),
        "avg_loser_r":     round(float(loss.mean()) if len(loss) else 0, 3),
        "avg_r":           round(avg_r, 3),
        "expectancy_r":    round(avg_r, 3),
        "profit_factor":   round(pf, 2),
        "max_dd_pct":          round(max_dd, 2),           # fixed-notional (can exceed -100%)
        "max_dd_pct_equity":   round(max_dd_pct_equity, 2), # % risk model (interpretable)
        "max_dd_dur_days": round(dd_days, 1),
        "sharpe":          round(float(sharpe), 2),
        "best_month_pct":  round(best_m, 2),
        "worst_month_pct": round(worst_m, 2),
        "avg_hold_min":    round(float(np.mean([x["hold_min"] for x in t])), 1),
        "per_symbol":      per_symbol,
        "_equity":         eq.tolist(),
        "_trades":         t,
    }

def verdict(m: dict) -> str:
    if m["total_trades"] == 0: return "🔴 KILL"
    exp = m["expectancy_r"]; n = m["total_trades"]
    # Use % equity DD (interpretable) for thresholds; fall back to fixed-notional if missing
    dd = abs(m.get("max_dd_pct_equity", m["max_dd_pct"]))
    if exp > 0.3 and n >= 30 and dd < 40:  return "🟢 KEEP & SCALE"
    if exp > 0.1 and n >= 30 and dd < 60:  return "🟡 KEEP"
    if exp > 0:                              return "🟠 TUNE"
    return "🔴 KILL"


# ── apply verdicts to bot.py ──────────────────────────────────────────────────
def apply_verdicts(metrics: List[dict]) -> List[str]:
    bot_path = os.path.join(WORK_DIR, "bot.py")
    with open(bot_path) as f: src = f.read()

    cls_map = {
        "scalp":"ScalpAgent","momentum":"MomentumAgent","swing":"SwingAgent",
        "meanrev":"MeanReversionAgent","asymmetric":"AsymmetricBreakoutAgent",
        "bb_squeeze":"BollingerSqueezeAgent","donchian":"DonchianBreakoutAgent",
        "funding":"FundingHunterAgent","ema_ribbon":"EMARibbonAgent",
    }
    changes = []
    for m in metrics:
        v   = verdict(m); agent = m["agent"]; cls = cls_map.get(agent)
        if not cls: continue
        exp = m["expectancy_r"]
        marker = f'class {cls}(Agent):\n    name = "{agent}"'
        if marker not in src: continue
        if v == "🔴 KILL" and "    enabled = False" not in src.split(f"class {cls}")[1][:300]:
            src = src.replace(marker, marker + "\n    enabled = False", 1)
            changes.append(f"DISABLED {agent} (exp={exp:+.3f}R)")
            log.warning(f"DISABLED {cls}: expectancy {exp:+.3f}R")
        elif v == "🟢 KEEP & SCALE" and "    notional_multiplier" not in src.split(f"class {cls}")[1][:300]:
            src = src.replace(marker, marker + "\n    notional_multiplier = 1.5", 1)
            changes.append(f"SCALED {agent} ×1.5 (exp={exp:+.3f}R)")
        elif v == "🟠 TUNE" and "    paper_only = True" not in src.split(f"class {cls}")[1][:300]:
            src = src.replace(marker, marker + "\n    paper_only = True", 1)
            changes.append(f"PAPER_ONLY {agent} (exp={exp:+.3f}R, n={m['total_trades']})")
    if changes:
        with open(bot_path, "w") as f: f.write(src)
        log.info("Applied to bot.py:\n  " + "\n  ".join(changes))
    return changes


# ── equity curve plot ─────────────────────────────────────────────────────────
def save_plot(metrics: List[dict]):
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        log.warning("matplotlib missing — skipping plot"); return
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = plt.cm.tab10.colors  # type: ignore
    combined = None
    for idx, m in enumerate(metrics):
        eq = m.get("_equity", [])
        if len(eq) < 2: continue
        arr = np.array(eq)
        ax.plot(arr, label=f"{m['agent']} ({m['expectancy_r']:+.3f}R)",
                alpha=0.8, color=colors[idx % 10])
        combined = arr if combined is None else (
            combined[:len(arr)] + arr[:len(combined)] - NOTIONAL)
    if combined is not None:
        ax.plot(combined, color="black", lw=2, ls="--", label="Portfolio")
    ax.set_title("365-day Backtest — Equity Curves"); ax.grid(alpha=0.3)
    ax.legend(fontsize=8); plt.tight_layout()
    out = os.path.join(WORK_DIR, "equity_curve.png")
    plt.savefig(out, dpi=130); plt.close()
    log.info(f"Saved {out}")


# ── report ────────────────────────────────────────────────────────────────────
def save_report(metrics: List[dict], changes: List[str]):
    lines = [
        "# BACKTEST REPORT",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Verdict Table",
        "| AGENT | TRADES | WIN% | AVG_R | EXP_R | DD(fixed) | DD(pct_eq) | PF | SHARPE | VERDICT |",
        "|-------|--------|------|-------|-------|-----------|------------|-----|--------|---------|",
    ]
    for m in metrics:
        v = verdict(m)
        if m["total_trades"] == 0:
            lines.append(f"| {m['agent']} | 0 | — | — | — | — | — | — | — | {v} |")
        else:
            dd_eq = m.get("max_dd_pct_equity", m["max_dd_pct"])
            lines.append(
                f"| {m['agent']} | {m['total_trades']} | {m['win_rate']}% | "
                f"{m['avg_r']:+.3f} | {m['expectancy_r']:+.3f} | "
                f"{m['max_dd_pct']:.1f}% | {dd_eq:.1f}% | "
                f"{m['profit_factor']:.2f} | {m['sharpe']:.2f} | {v} |")
    lines += ["", "## Auto-prune Actions"] + (changes or ["(none)"])
    lines += ["", "## Per-Agent Detail"]
    for m in metrics:
        if m["total_trades"] == 0: continue
        v = verdict(m)
        lines += [
            f"### {m['agent']}  {v}",
            f"- Trades: {m['total_trades']} W={m.get('wins',0)} L={m.get('losses',0)} WR={m['win_rate']}%",
            f"- Exp: {m['expectancy_r']:+.3f}R  PF: {m['profit_factor']:.2f}  Sharpe: {m['sharpe']:.2f}",
            f"- MaxDD(fixed): {m['max_dd_pct']:.1f}%  MaxDD(pct_eq): {m.get('max_dd_pct_equity', m['max_dd_pct']):.1f}%  DDdur: {m['max_dd_dur_days']:.0f}d",
            f"- Best month: {m['best_month_pct']:+.1f}%  Worst: {m['worst_month_pct']:+.1f}%",
            f"- Avg hold: {m['avg_hold_min']:.0f} min",
        ]
        if m.get("per_symbol"):
            top = m["per_symbol"][:5]
            bot = m["per_symbol"][-3:] if len(m["per_symbol"]) > 5 else []
            lines.append("- Top coins: " +
                ", ".join(f"{r['symbol']} ({r['expectancy_r']:+.2f}R, n={r['trades']})" for r in top))
            if bot:
                lines.append("- Worst coins: " +
                    ", ".join(f"{r['symbol']} ({r['expectancy_r']:+.2f}R, n={r['trades']})" for r in bot))
        lines.append("")
    out = os.path.join(WORK_DIR, "BACKTEST_REPORT.md")
    with open(out, "w") as f: f.write("\n".join(lines) + "\n")
    log.info(f"Saved {out}")


# ── telegram summary ──────────────────────────────────────────────────────────
def send_tg(metrics: List[dict], changes: List[str]):
    try:
        import aiohttp, asyncio
        kept_s = sum(1 for m in metrics if verdict(m) == "🟢 KEEP & SCALE")
        kept   = sum(1 for m in metrics if verdict(m) == "🟡 KEEP")
        tune   = sum(1 for m in metrics if verdict(m) == "🟠 TUNE")
        killed = sum(1 for m in metrics if verdict(m) == "🔴 KILL")
        with_t = [m for m in metrics if m["total_trades"] > 0]
        comb_exp = sum(m["expectancy_r"] for m in with_t) / len(with_t) if with_t else 0
        top3 = sorted(with_t, key=lambda x: -x["expectancy_r"])[:3]
        top3_str = "\n".join(
            f"  {i+1}. {m['agent']}: {m['expectancy_r']:+.3f}R ({m['total_trades']}t)"
            for i, m in enumerate(top3))
        text = (f"🚀 <b>Backtested upgrade live</b>\n"
                f"{kept_s} scaled | {kept} kept | {tune} tuning | {killed} disabled\n"
                f"Combined expectancy: <b>{comb_exp:+.3f}R</b>\n"
                f"Top 3:\n{top3_str}")
        async def _send():
            url = (f"https://api.telegram.org/bot"
                   f"{os.environ.get('TELEGRAM_BOT_TOKEN','')}/sendMessage")
            async with aiohttp.ClientSession() as s:
                await s.post(url, json={"chat_id": os.environ.get("TELEGRAM_CHAT_ID",""),
                                        "text": text, "parse_mode": "HTML"})
        asyncio.run(_send())
    except Exception as e:
        log.warning(f"telegram: {e}")


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days",     type=int, default=365)
    ap.add_argument("--symbols",  type=str, default="all")
    ap.add_argument("--no-apply", action="store_true")
    args = ap.parse_args()

    log.info("="*60)
    log.info(f" BACKTEST v2  days={args.days}  symbols={args.symbols}")
    log.info("="*60)

    client   = _client()
    universe = DEFAULT_UNIVERSE if args.symbols.lower()=="all" else \
               [s.strip().upper() for s in args.symbols.split(",")]
    log.info(f"Universe ({len(universe)}): {universe}")

    all_trades: List[dict] = []
    n = len(universe)
    for idx, sym in enumerate(universe):
        pct = (idx+1)/n*100
        if idx == 0 or int(pct)%10 == 0:
            log.info(f"Progress: {pct:.0f}%  ({idx+1}/{n})  {sym}")
        try:
            df5  = load_or_fetch(client, sym, "5m",  args.days)
            df15 = load_or_fetch(client, sym, "15m", args.days)
            df1h = load_or_fetch(client, sym, "1H",  args.days)
            if df15.empty or len(df15) < 200:
                log.warning(f"  {sym}: only {len(df15)} 15m bars — skipping")
                continue
            log.info(f"  {sym}: building indicators…")
            p = PrecomputedData(df5, df15, df1h)
            log.info(f"  {sym}: simulating {p.n15} bars…")
            trades = simulate(p, symbol=sym)
            for _t in trades:
                _t["symbol"] = sym
            all_trades.extend(trades)
            by_agent = {}
            for t in trades:
                by_agent[t["agent"]] = by_agent.get(t["agent"], 0) + 1
            log.info(f"  {sym}: {len(trades)} trades  {by_agent}")
        except Exception as e:
            log.warning(f"  {sym}: {e}\n{traceback.format_exc()[:300]}")

    if not all_trades:
        log.error("No trades generated at all.")
        sys.exit(1)

    log.info(f"Total trades across all symbols: {len(all_trades)}")
    metrics = [compute_metrics(a, all_trades) for a in AGENT_NAMES]
    metrics.sort(key=lambda m: -(m.get("expectancy_r") or -999))

    # Print table
    print("\n" + "="*92)
    print(f"{'AGENT':<14} {'TRADES':>7} {'WIN%':>6} {'AVG_R':>7} {'EXP_R':>7} "
          f"{'MAX_DD':>8} {'PF':>6} {'SHARPE':>7}  VERDICT")
    print("="*92)
    for m in metrics:
        v = verdict(m)
        if m["total_trades"] == 0:
            print(f"  {m['agent']:<12} {'0':>7}   —       —       —        —       —       —    {v}")
        else:
            print(f"  {m['agent']:<12} {m['total_trades']:>7} {m['win_rate']:>5.1f}% "
                  f"{m['avg_r']:>+7.3f} {m['expectancy_r']:>+7.3f} "
                  f"{m['max_dd_pct']:>7.1f}% {m['profit_factor']:>6.2f} "
                  f"{m['sharpe']:>7.2f}  {v}")
    print("="*92 + "\n")

    changes = [] if args.no_apply else apply_verdicts(metrics)
    save_report(metrics, changes)
    save_plot(metrics)
    send_tg(metrics, changes)
    log.info("Backtest complete.")


if __name__ == "__main__":
    main()
