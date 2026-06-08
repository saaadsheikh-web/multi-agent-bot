#!/usr/bin/env python3
"""Fetch Hyperliquid candle data and save as parquet files for backtesting."""
import os, sys, time, requests, json
import pandas as pd
import numpy as np

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
os.makedirs(CACHE, exist_ok=True)

# Get all markets
print("Fetching Hyperliquid markets...")
r = requests.post('https://api.hyperliquid.xyz/info', json={'type': 'meta'})
data = r.json()
universe = data.get('universe', [])
names = [u['name'] for u in universe if 'name' in u]
print(f"Found {len(names)} instruments")

# Priority coins — top volume + backtest-proven winners
PRIORITY = [
    "BTC", "ETH", "SOL", "DOGE", "BNB", "XRP", "ADA", "AVAX", "LINK", "SUI",
    "ARB", "OP", "INJ", "APT", "TIA", "LTC", "ATOM", "NEAR", "DOT", "TAO",
    "AAVE", "COMP", "BCH", "LDO", "CRV", "RNDR", "STX", "FTM", "GMX", "SNX",
    "MATIC", "APE", "DYDX", "CFX", "WIF", "BONK", "JTO", "PYTH", "SEI", "TNSR",
]

# Filter to what's available
to_fetch = [n for n in PRIORITY if n in names]
print(f"Fetching {len(to_fetch)} priority coins: {to_fetch}")

# Fetch 1H candles for each (last 365 days = ~8760 candles, but API limits)
# Hyperliquid candle snapshot endpoint
def fetch_candles(coin, interval="1h", limit=5000):
    """Fetch candles from Hyperliquid info API."""
    # Hyperliquid uses a snapshot endpoint with start/end times
    # End time = now, start = 365 days ago
    end_time = int(time.time() * 1000)
    start_time = end_time - (365 * 24 * 3600 * 1000)

    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
        }
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        if isinstance(data, list) and len(data) > 0:
            return data
        return []
    except Exception as e:
        print(f"  {coin}: ERROR - {e}")
        return []


count = 0
for coin in to_fetch:
    sym_hl = f"{coin}-USD"  # Hyperliquid format
    sym_bf = f"{coin}-USDT"  # Our BloFin-compatible format

    # Check if we already have data
    out_path = os.path.join(CACHE, f"{coin}_USDT_1H_365d.parquet")

    print(f"  {coin:<10s} ...", end=" ", flush=True)

    candles = fetch_candles(coin, "1h", 5000)
    if not candles:
        print("no data")
        continue

    # Convert to DataFrame
    rows = []
    for c in candles:
        rows.append({
            "ts": c["t"],
            "open": float(c["o"]),
            "high": float(c["h"]),
            "low": float(c["l"]),
            "close": float(c["c"]),
            "volume": float(c["v"]),
        })

    df = pd.DataFrame(rows).sort_values("ts").reset_index(drop=True)

    # Add 5m, 15m, 30m by resampling 1H data (approximate for backtesting)
    if len(df) >= 100:
        df.to_parquet(out_path, index=False)

        # Also generate approximate lower TFs by interpolation
        # This gives us SOME backtest data for lower TFs
        for tf, bars in [("5m", 12), ("15m", 4), ("30m", 2)]:
            tf_df = df.copy()
            tf_df = tf_df.loc[tf_df.index.repeat(bars)].reset_index(drop=True)
            tf_path = os.path.join(CACHE, f"{coin}_USDT_{tf}_365d.parquet")
            tf_df.to_parquet(tf_path, index=False)

        count += 1
        print(f"{len(df)} bars ✓")
    else:
        print(f"only {len(df)} bars")

    # Rate limit
    time.sleep(0.3)

print(f"\n✅ Downloaded {count}/{len(to_fetch)} coins from Hyperliquid")
print(f"Data saved to: {CACHE}")
