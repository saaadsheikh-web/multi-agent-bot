"""
RELIABLE TradingView data fetcher — fresh connection per call.
"""
import sys, time, json
import pandas as pd
import numpy as np
from typing import Dict, Optional

SITE_PKG = '/opt/homebrew/Caskroom/miniconda/base/lib/python3.13/site-packages'
if SITE_PKG not in sys.path:
    sys.path.insert(0, SITE_PKG)

INTERVAL_MAP = {
    "1m": "in_1_minute", "3m": "in_3_minute", "5m": "in_5_minute",
    "15m": "in_15_minute", "30m": "in_30_minute", "45m": "in_45_minute",
    "1H": "in_1_hour", "2H": "in_2_hour", "3H": "in_3_hour", "4H": "in_4_hour",
    "1D": "in_daily", "1W": "in_weekly"
}

def candles(symbol: str, tf: str, n_bars: int = 1000) -> pd.DataFrame:
    """Fresh TradingView connection per call. No stale WebSocket issues."""
    from tvDatafeed import TvDatafeed, Interval
    
    tv_symbol = symbol.replace("-", "").upper()
    interval_name = INTERVAL_MAP.get(tf, "in_1_hour")
    interval = getattr(Interval, interval_name)
    n_bars = min(n_bars, 5000)
    
    # Create FRESH instance each time
    tv = TvDatafeed()
    
    try:
        df = tv.get_hist(symbol=tv_symbol, exchange="BINANCE",
                        interval=interval, n_bars=n_bars)
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        result = pd.DataFrame()
        result["open"] = df["open"].values
        result["high"] = df["high"].values
        result["low"] = df["low"].values
        result["close"] = df["close"].values
        result["volume"] = df["volume"].values
        result["ts"] = df.index.astype(np.int64) // 10**6
        
        return result.sort_values("ts").reset_index(drop=True)
    
    except Exception as e:
        # Second attempt
        time.sleep(1)
        try:
            tv2 = TvDatafeed()
            df = tv2.get_hist(symbol=tv_symbol, exchange="BINANCE",
                            interval=interval, n_bars=n_bars)
            if df is not None and not df.empty:
                result = pd.DataFrame()
                result["open"] = df["open"].values
                result["high"] = df["high"].values
                result["low"] = df["low"].values
                result["close"] = df["close"].values
                result["volume"] = df["volume"].values
                result["ts"] = df.index.astype(np.int64) // 10**6
                return result.sort_values("ts").reset_index(drop=True)
        except:
            pass
        return pd.DataFrame()


def resample(df, chunks):
    """Resample OHLCV by combining chunks bars."""
    df = df.copy()
    df["_g"] = np.arange(len(df)) // chunks
    return df.groupby("_g").agg({
        "ts": "first", "open": "first", "high": "max",
        "low": "min", "close": "last", "volume": "sum"
    }).dropna().reset_index(drop=True)
