"""
RELIABLE TradingView data fetcher — uses direct HTTP requests (no WebSocket).
Fetches chart data via TradingView's internal API endpoint.
"""
import json, time, re
import pandas as pd
import numpy as np
from typing import Dict, Optional, Any
from urllib.request import Request, urlopen
from urllib.error import URLError

# TradingView chart data endpoint (works without auth for historical)
TV_SIGNATURE = "https://chart-data.tradingview.com"
TV_ORIGIN = "https://www.tradingview.com"

_SESSION = None

def _get_session():
    global _SESSION
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# Interval mapping
_INTERVAL_MAP = {
    "1m":  "1", "3m": "3", "5m": "5", "15m": "15", "30m": "30", 
    "45m": "45", "1H": "60", "2H": "120", "3H": "180", "4H": "240",
    "1D": "1D", "1W": "1W", "1M": "1M"
}

# Resolution mapping for TV API
_RES_MAP = {
    "1m": "1", "5m": "5", "15m": "15", "30m": "30",
    "1H": "60", "2H": "120", "4H": "240",
    "1D": "1D", "1W": "1W"
}

def candles(symbol: str, tf: str, n_bars: int = 1000) -> pd.DataFrame:
    """Fetch OHLCV candles from TradingView chart API (HTTP, no WebSocket)."""
    tv_symbol = symbol.replace("-", "").upper()
    resolution = _RES_MAP.get(tf, "60")
    n_bars = min(n_bars, 5000)
    
    # TradingView's chart data endpoint
    # We fetch in chunks since max per request varies
    url = f"https://chart-prod.tvdataservices.com/chart/data?symbol=BINANCE:{tv_symbol}&resolution={resolution}&from=0&to=9999999999&countback={n_bars}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Origin": TV_ORIGIN,
        "Referer": f"{TV_ORIGIN}/chart/",
        "Accept": "application/json",
    }
    
    try:
        req = Request(url, headers=headers)
        ctx = _get_session()
        with urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        if not data or "s" not in data or data["s"] != "ok":
            return pd.DataFrame()
        
        # Build DataFrame
        result = pd.DataFrame({
            "ts": data["t"],
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"],
            "volume": data["v"],
        })
        
        # Convert timestamps to milliseconds
        if result["ts"].iloc[0] < 10000000000:  # seconds not ms
            result["ts"] = result["ts"] * 1000
        
        return result.sort_values("ts").reset_index(drop=True)
    
    except Exception as e:
        print(f"  [TV-HTTP] {symbol} {tf}: {e}", file=__import__('sys').stderr)
        return pd.DataFrame()


def all_timeframes(symbol: str) -> Dict[str, pd.DataFrame]:
    """Fetch 5m and 1H data, resample to all needed TFs."""
    data = {}
    
    # 5m: 5000 bars
    df5 = candles(symbol, "5m", 5000)
    if not df5.empty:
        data["5m"] = df5
        print(f"  ✓ {symbol} 5m: {len(df5)} bars")
    
    # 1H: 5000 bars
    df1h = candles(symbol, "1H", 5000)
    if not df1h.empty:
        data["1H"] = df1h
        print(f"  ✓ {symbol} 1H: {len(df1h)} bars")
    
    # Resample
    if "5m" in data:
        data["15m"] = _resample(data["5m"], 3)
        data["30m"] = _resample(data["5m"], 6)
    
    if "1H" in data:
        for tf, ch in [("2H", 2), ("4H", 4), ("8H", 8), ("12H", 12), ("24H", 24)]:
            rd = _resample(data["1H"], ch)
            if not rd.empty:
                data[tf] = rd
    
    return data


def _resample(df, chunk):
    df = df.copy()
    df["_g"] = np.arange(len(df)) // chunk
    return df.groupby("_g").agg({
        "ts": "first", "open": "first", "high": "max",
        "low": "min", "close": "last", "volume": "sum"
    }).dropna().reset_index(drop=True)


if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) >= 3:
        sym = sys.argv[1]
        tf = sys.argv[2]
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else 100
    else:
        sym = "BTC-USDT"
        tf = "1H"
        n = 100
    
    print(f"Testing {sym} {tf} {n} bars...")
    df = candles(sym, tf, n)
    if not df.empty:
        print(f"  OK: {len(df)} bars")
        print(f"  From: {df.iloc[0]['ts']}")
        print(f"  To: {df.iloc[-1]['ts']}")
        print(f"  Close range: {df['close'].min():.2f} - {df['close'].max():.2f}")
    else:
        print("  Empty/error")
