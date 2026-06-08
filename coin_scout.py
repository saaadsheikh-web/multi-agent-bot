#!/usr/bin/env python3
"""
Coin Scout — Finds coins where backtest-winning strategies will work.
Uses patterns extracted from comprehensive 44-agent backtest (2026-06-03).

Winner formula: 1H TF + ADX>25 + daily_range>3% + volume_trend>1.2x + fib_structure
Scoring based on empirical correlation with backtest profitability.
"""

import math
from typing import List, Tuple, Dict, Optional
import numpy as np
import pandas as pd


# ═══════════════════════════════════════════════════════════════════════════════
# SCORING WEIGHTS (derived from backtest regression)
# ═══════════════════════════════════════════════════════════════════════════════
WEIGHTS = {
    "daily_range":    25,   # % of day's range — breakout potential
    "adx_trend":      25,   # ADX > 25 = trending market
    "volume_health":  20,   # Volume increasing vs 7d avg
    "fib_structure":  15,   # Clear support/resistance levels
    "not_overbought": 10,   # RSI not extreme (room to run)
    "liquidity":       5,   # Tight spread = good execution
}

STRATEGY_MATCH = {
    "daily_breakout": {
        "min_score": 65,
        "required": ["daily_range", "adx_trend", "volume_health"],
        "tf": "1H",
    },
    "daily_breakout_24h": {
        "min_score": 60,
        "required": ["daily_range", "volume_health"],
        "tf": "1H",
    },
    "fib_confluence": {
        "min_score": 55,
        "required": ["fib_structure", "daily_range"],
        "tf": "15m",
    },
    "fibonacci": {
        "min_score": 55,
        "required": ["fib_structure", "adx_trend"],
        "tf": "1H",
    },
    "liquidity_sweep": {
        "min_score": 50,
        "required": ["daily_range", "volume_health"],
        "tf": "1H",
    },
    "wide_scalp": {
        "min_score": 50,
        "required": ["daily_range", "adx_trend"],
        "tf": "1H",
    },
    "volume_capitulation": {
        "min_score": 50,
        "required": ["volume_health"],
        "tf": "1H",
    },
    "fib_hotzone": {
        "min_score": 60,
        "required": ["fib_structure"],
        "tf": "15m",
    },
    "utbot_mtf": {
        "min_score": 50,
        "required": ["adx_trend"],
        "tf": "1H",
    },
    "asymmetric": {
        "min_score": 55,
        "required": ["daily_range", "adx_trend"],
        "tf": "1H",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# INDICATORS (lightweight, no pandas dependency for live use)
# ═══════════════════════════════════════════════════════════════════════════════
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()


def compute_adx(df, period=14):
    """Compute ADX from OHLC dataframe."""
    high, low, close = df["high"], df["low"], df["close"]
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    up = high - high.shift()
    down = low.shift() - low
    plus_dm = np.where((up > down) & (up > 0), up, 0)
    minus_dm = np.where((down > up) & (down > 0), down, 0)

    atr = tr.ewm(span=period, adjust=False).mean()
    plus_di = 100 * pd.Series(plus_dm, index=df.index).ewm(span=period, adjust=False).mean() / atr
    minus_di = 100 * pd.Series(minus_dm, index=df.index).ewm(span=period, adjust=False).mean() / atr

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 0.0001)
    adx = dx.ewm(span=period, adjust=False).mean()
    return adx, plus_di, minus_di


def find_fib_levels(df, lookback=100):
    """Count how many times price respected fib levels (simplified)."""
    c = df["close"].iloc[-lookback:]
    high = c.max()
    low = c.min()
    rng = high - low
    if rng <= 0:
        return 0

    levels = {
        "0.382": low + 0.382 * rng,
        "0.500": low + 0.500 * rng,
        "0.618": low + 0.618 * rng,
        "0.786": low + 0.786 * rng,
    }

    touches = 0
    for label, level in levels.items():
        # Count how many bars came within 0.5% of this level
        nearby = (abs(c - level) / level < 0.005).sum()
        if nearby >= 2:
            touches += 1
    return touches


# ═══════════════════════════════════════════════════════════════════════════════
# SCORING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
def score_coin(sym: str, df_1h: pd.DataFrame, df_15m: Optional[pd.DataFrame] = None,
               ticker_info: Optional[dict] = None) -> dict:
    """
    Score a coin against the backtest-proven winner patterns.
    Returns dict with total score, breakdown, and matched strategies.
    """
    if df_1h is None or len(df_1h) < 100:
        return {"symbol": sym, "total_score": 0, "error": "insufficient_data"}

    scores = {}
    c = df_1h["close"]
    h = df_1h["high"]
    l = df_1h["low"]
    v = df_1h["volume"]

    # 1. Daily Range Score (breakout potential)
    try:
        last_24h = c.iloc[-24:] if len(c) >= 24 else c
        daily_range_pct = ((h.iloc[-24:].max() - l.iloc[-24:].min()) / c.iloc[-1]) * 100
        if daily_range_pct > 5:
            scores["daily_range"] = WEIGHTS["daily_range"]
        elif daily_range_pct > 3:
            scores["daily_range"] = int(WEIGHTS["daily_range"] * 0.8)
        elif daily_range_pct > 1.5:
            scores["daily_range"] = int(WEIGHTS["daily_range"] * 0.5)
        else:
            scores["daily_range"] = 0
    except Exception:
        scores["daily_range"] = 0

    # 2. ADX Trend Score
    try:
        adx, plus_di, minus_di = compute_adx(df_1h)
        adx_now = adx.iloc[-1]
        if adx_now > 30:
            scores["adx_trend"] = WEIGHTS["adx_trend"]  # Strong trend
        elif adx_now > 25:
            scores["adx_trend"] = int(WEIGHTS["adx_trend"] * 0.8)
        elif adx_now > 20:
            scores["adx_trend"] = int(WEIGHTS["adx_trend"] * 0.5)
        else:
            scores["adx_trend"] = 0
    except Exception:
        scores["adx_trend"] = 0

    # 3. Volume Health Score
    try:
        vol_7d_avg = v.iloc[-168:].mean() if len(v) >= 168 else v.mean()
        vol_1d_avg = v.iloc[-24:].mean() if len(v) >= 24 else v.mean()
        vol_ratio = vol_1d_avg / vol_7d_avg if vol_7d_avg > 0 else 1.0
        if vol_ratio > 1.5:
            scores["volume_health"] = WEIGHTS["volume_health"]
        elif vol_ratio > 1.2:
            scores["volume_health"] = int(WEIGHTS["volume_health"] * 0.8)
        elif vol_ratio > 1.0:
            scores["volume_health"] = int(WEIGHTS["volume_health"] * 0.5)
        else:
            scores["volume_health"] = 0
    except Exception:
        scores["volume_health"] = 0

    # 4. Fib Structure Score
    try:
        fib_touches = find_fib_levels(df_1h)
        if fib_touches >= 3:
            scores["fib_structure"] = WEIGHTS["fib_structure"]
        elif fib_touches >= 2:
            scores["fib_structure"] = int(WEIGHTS["fib_structure"] * 0.7)
        elif fib_touches >= 1:
            scores["fib_structure"] = int(WEIGHTS["fib_structure"] * 0.4)
        else:
            scores["fib_structure"] = 0
    except Exception:
        scores["fib_structure"] = 0

    # 5. Not Overbought Score
    try:
        # Simple RSI approximation using 14-period
        delta = c.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(span=14, adjust=False).mean().iloc[-1]
        avg_loss = loss.ewm(span=14, adjust=False).mean().iloc[-1]
        if avg_loss > 0:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        else:
            rsi = 100
        if 40 <= rsi <= 60:
            scores["not_overbought"] = WEIGHTS["not_overbought"]  # Neutral = room to run
        elif 30 <= rsi <= 70:
            scores["not_overbought"] = int(WEIGHTS["not_overbought"] * 0.5)
        else:
            scores["not_overbought"] = 0
    except Exception:
        scores["not_overbought"] = 0

    # 6. Liquidity Score (from ticker if available)
    try:
        if ticker_info:
            bid = float(ticker_info.get("bidPrice") or ticker_info.get("bid") or 0)
            ask = float(ticker_info.get("askPrice") or ticker_info.get("ask") or 0)
            if bid > 0 and ask > 0:
                spread_pct = (ask - bid) / ask * 100
                if spread_pct < 0.05:
                    scores["liquidity"] = WEIGHTS["liquidity"]
                elif spread_pct < 0.1:
                    scores["liquidity"] = int(WEIGHTS["liquidity"] * 0.7)
                else:
                    scores["liquidity"] = 0
            else:
                scores["liquidity"] = WEIGHTS["liquidity"] // 2  # assume OK if no data
        else:
            scores["liquidity"] = WEIGHTS["liquidity"] // 2
    except Exception:
        scores["liquidity"] = WEIGHTS["liquidity"] // 2

    total = sum(scores.values())

    # Match to strategies
    matched = []
    for strategy, config in STRATEGY_MATCH.items():
        if total >= config["min_score"]:
            required_ok = all(scores.get(r, 0) > 0 for r in config["required"])
            if required_ok:
                matched.append(strategy)

    return {
        "symbol": sym,
        "total_score": total,
        "scores": scores,
        "matched_strategies": matched,
        "daily_range_pct": round(daily_range_pct, 1) if 'daily_range_pct' in dir() else None,
        "adx": round(adx_now, 1) if 'adx_now' in dir() else None,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# BATCH SCOUT
# ═══════════════════════════════════════════════════════════════════════════════
def scout_all(data_provider, tickers: List[dict], top_n: int = 30,
              min_score: int = 40) -> List[dict]:
    """
    Score all USDT pairs from tickers, return top N ranked.

    data_provider: object with .candles(sym, tf, bars) method
    tickers: list of ticker dicts from exchange
    """
    results = []
    usdt_pairs = []

    for t in tickers:
        sym = t.get("instId") or ""
        if not sym.endswith("-USDT"):
            continue
        # Skip stablecoins and weird pairs
        base = sym.split("-")[0]
        if base in ("USDC", "DAI", "BUSD", "TUSD", "USDP", "FDUSD"):
            continue
        if "1000" in base or "10000" in base:
            continue  # skip leveraged tokens / weird denominations
        usdt_pairs.append((sym, t))

    print(f"Scouting {len(usdt_pairs)} USDT pairs...")

    for sym, ticker in usdt_pairs:
        try:
            df_1h = data_provider.candles(sym, "1H", 200)
            if df_1h is None or len(df_1h) < 100:
                continue
            result = score_coin(sym, df_1h, ticker_info=ticker)
            if result["total_score"] >= min_score:
                results.append(result)
        except Exception as e:
            continue

    results.sort(key=lambda x: -x["total_score"])
    return results[:top_n]


# ═══════════════════════════════════════════════════════════════════════════════
# STRATEGY ASSIGNMENT
# ═══════════════════════════════════════════════════════════════════════════════
def assign_strategies(scouted_coins: List[dict]) -> Dict[str, List[str]]:
    """
    Given scouted coins with matched_strategies, return:
    {strategy_name: [list of symbols to trade]}
    """
    assignments = {}
    for coin in scouted_coins:
        for strategy in coin.get("matched_strategies", []):
            assignments.setdefault(strategy, []).append(coin["symbol"])
    return assignments


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════════════════════════════════
def print_report(results: List[dict]):
    """Print a formatted scout report."""
    print(f"\n{'='*80}")
    print(f"COIN SCOUT REPORT — Top {len(results)} Coins")
    print(f"{'='*80}")
    print(f"{'Rank':<6} {'Symbol':<15} {'Score':<8} {'Range%':<8} {'ADX':<8} {'Strategies'}")
    print(f"{'─'*6} {'─'*15} {'─'*8} {'─'*8} {'─'*8} {'─'*40}")

    for i, coin in enumerate(results, 1):
        sym = coin["symbol"]
        score = coin["total_score"]
        dr = coin.get("daily_range_pct") or 0
        adx = coin.get("adx") or 0
        strats = ", ".join(coin.get("matched_strategies", [])[:4])
        print(f"{i:<6} {sym:<15} {score:<8} {dr:<8.1f} {adx:<8.1f} {strats}")

    # Strategy assignments
    assignments = assign_strategies(results)
    print(f"\n{'─'*80}")
    print("STRATEGY ASSIGNMENTS")
    print(f"{'─'*80}")
    for strategy, symbols in sorted(assignments.items(), key=lambda x: -len(x[1])):
        print(f"  {strategy:<25s}: {len(symbols)} coins — {', '.join(symbols[:5])}{'...' if len(symbols)>5 else ''}")


if __name__ == "__main__":
    print("Coin Scout module loaded.")
    print(f"Strategies tracked: {len(STRATEGY_MATCH)}")
    print(f"Scoring dimensions: {list(WEIGHTS.keys())}")
    print("\nTo use with bot: from coin_scout import score_coin, scout_all, assign_strategies")
