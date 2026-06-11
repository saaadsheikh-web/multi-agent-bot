"""
TradingView data module for backtesting.
Replaces BloFin's candles() for backtests — much faster, more data, better quality.
"""
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import Dict, Optional

# Add tvDatafeed to path (installed in conda)
SITE_PKG = '/opt/homebrew/Caskroom/miniconda/base/lib/python3.13/site-packages'
if SITE_PKG not in sys.path:
    sys.path.insert(0, SITE_PKG)

from tvDatafeed import TvDatafeed, Interval

# Singleton
_tv: Optional[TvDatafeed] = None

def _get_tv():
    global _tv
    if _tv is None:
        _tv = TvDatafeed()
    return _tv

# Interval map
_INTERVAL_MAP = {
    "5m":  Interval.in_5_minute,
    "15m": Interval.in_15_minute,
    "30m": Interval.in_30_minute,
    "1H":  Interval.in_1_hour,
    "2H":  Interval.in_2_hour,
    "3H":  Interval.in_3_hour,
    "4H":  Interval.in_4_hour,
    "1D":  Interval.in_daily,
    "1W":  Interval.in_weekly,
    "1M":  Interval.in_monthly,
}

# Exchange map — BINANCE works for all major crypto
EXCHANGE = "BINANCE"

# Symbol name fix: BTC-USDT -> BTCUSDT
def _fix_symbol(symbol: str) -> str:
    return symbol.replace("-", "").upper()

def candles(symbol: str, tf: str, n_bars: int = 1000) -> pd.DataFrame:
    """Get OHLCV candles from TradingView. Same interface as BloFin.candles()."""
    tv = _get_tv()
    tv_symbol = _fix_symbol(symbol)
    interval = _INTERVAL_MAP.get(tf)
    
    if interval is None:
        return pd.DataFrame()
    
    # Clamp to max 5000
    n_bars = min(n_bars, 5000)
    
    try:
        df = tv.get_hist(symbol=tv_symbol, exchange=EXCHANGE,
                        interval=interval, n_bars=n_bars)
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Convert to our format: columns = open, high, low, close, volume, ts
        result = pd.DataFrame()
        result["open"] = df["open"].values
        result["high"] = df["high"].values
        result["low"] = df["low"].values
        result["close"] = df["close"].values
        result["volume"] = df["volume"].values
        result["ts"] = df.index.astype(np.int64) // 10**6  # convert to ms
        
        return result.sort_values("ts").reset_index(drop=True)
    
    except Exception as e:
        print(f"  [TvDatafeed] {symbol} {tf}: {e}")
        return pd.DataFrame()

def all_timeframes_for_backtest(symbol: str) -> Dict[str, pd.DataFrame]:
    """Fetch all timeframes needed for backtesting (5m, 1H). Returns dict of DataFrames."""
    data = {}
    
    # 5m: up to 5000 bars (~17 days)
    df_5m = candles(symbol, "5m", 5000)
    if not df_5m.empty:
        data["5m"] = df_5m
        print(f"  ✓ {symbol} 5m: {len(df_5m)} bars")
    else:
        print(f"  ✗ {symbol} 5m: empty")
    
    # 1H: up to 5000 bars (~208 days = 7 months)
    df_1h = candles(symbol, "1H", 5000)
    if not df_1h.empty:
        data["1H"] = df_1h
        print(f"  ✓ {symbol} 1H: {len(df_1h)} bars")
    else:
        print(f"  ✗ {symbol} 1H: empty")
    
    # Resample 5m -> 15m, 30m
    if "5m" in data:
        data["15m"] = _resample_ohlcv(data["5m"], 3)
        data["30m"] = _resample_ohlcv(data["5m"], 6)
    
    # Resample 1H -> 2H, 4H, 8H, 12H, 24H
    if "1H" in data:
        for tf, chunks in [("2H", 2), ("4H", 4), ("8H", 8), ("12H", 12), ("24H", 24)]:
            resampled = _resample_ohlcv(data["1H"], chunks)
            if not resampled.empty:
                data[tf] = resampled
    
    return data

def _resample_ohlcv(df_input: pd.DataFrame, chunk_size: int) -> pd.DataFrame:
    """Resample OHLCV by combining chunk_size consecutive bars."""
    if len(df_input) < chunk_size:
        return pd.DataFrame()
    
    df = df_input.copy()
    df["_group"] = np.arange(len(df)) // chunk_size
    resampled = df.groupby("_group").agg({
        "ts": "first",
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }).dropna().reset_index(drop=True)
    return resampled
