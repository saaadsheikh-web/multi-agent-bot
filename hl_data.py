#!/usr/bin/env python3
"""Hyperliquid data connector — pull candles, save as parquet for backtests."""

import os, sys, time, json
import requests
import pandas as pd
import numpy as np
from pathlib import Path

WORK_DIR = Path(os.path.expanduser("~")) / "multi_agent_bot"
CACHE_DIR = WORK_DIR / "backtest_data"
CACHE_DIR.mkdir(exist_ok=True)

INFO_URL = "https://api.hyperliquid.xyz/info"
BATCH_LIMIT = 5000  # candles per request

# Symbols we care about (matching BloFin naming)
SYMBOLS = [
    "BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","DOGE-USDT",
    "ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT","LTC-USDT",
    "ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT","INJ-USDT",
    "TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT","XRP-USDT",
]

def bf_to_hl(symbol: str) -> str:
    """Convert BloFin symbol to Hyperliquid coin name."""
    return symbol.split("-")[0]

def fetch_candles(coin: str, interval: str, days: int) -> pd.DataFrame:
    """Fetch candle history from Hyperliquid."""
    end_time = int(time.time() * 1000)
    start_time = end_time - days * 24 * 3600 * 1000

    all_rows = []
    cursor = end_time

    while cursor > start_time:
        payload = {
            "type": "candleSnapshot",
            "req": {
                "coin": coin,
                "interval": interval,
                "startTime": start_time,
                "endTime": cursor,
            }
        }
        try:
            resp = requests.post(INFO_URL, json=payload, timeout=30)
            data = resp.json()
        except Exception as e:
            print(f"  {coin} {interval}: {e}")
            break

        if not isinstance(data, list) or not data:
            break

        all_rows.extend(data)
        # Move cursor before the oldest candle we got
        oldest_ts = min(r["t"] for r in data)
        if oldest_ts <= start_time:
            break
        cursor = oldest_ts - 1
        time.sleep(0.15)  # rate limit

    if not all_rows:
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(all_rows)
    df = df.rename(columns={
        "t": "ts", "T": "end_ts", "s": "coin",
        "o": "open", "c": "close", "h": "high", "l": "low", "v": "volume", "n": "trades"
    })
    for col in ["ts","open","high","low","close","volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["close"]).sort_values("ts").reset_index(drop=True)
    return df[["ts","open","high","low","close","volume"]]


def download_all(interval: str = "15m", days: int = 365):
    """Download candles for all tracked symbols. Saves as {SYM}_{interval}_{days}d.parquet."""
    print(f"Downloading {interval} candles ({days}d) from Hyperliquid...")
    for bf_sym in SYMBOLS:
        coin = bf_to_hl(bf_sym)
        fname = f"{bf_sym.replace('-','_')}_{interval}_{days}d.parquet"
        path = CACHE_DIR / fname

        # Skip if cached and fresh (< 12h old)
        if path.exists() and time.time() - path.stat().st_mtime < 43200:
            print(f"  {bf_sym:15s} → cached")
            continue

        print(f"  {bf_sym:15s} → {coin} ...", end=" ", flush=True)
        df = fetch_candles(coin, interval, days)
        if df.empty:
            print("no data")
            continue

        df.to_parquet(path, index=False)
        print(f"{len(df)} candles saved")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", default="15m", help="Candle interval (5m, 15m, 1h)")
    ap.add_argument("--days", type=int, default=365, help="Days of history")
    args = ap.parse_args()
    download_all(args.interval, args.days)
