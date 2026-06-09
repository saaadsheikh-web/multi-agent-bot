#!/usr/bin/env python3
"""Fetch 365 days of OHLCV data from Hyperliquid for all coins, all TFs"""
import os, json, time
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
os.makedirs(CACHE, exist_ok=True)

# Top 20 liquid coins on Hyperliquid
SYMBOLS = [
    "BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "BNB-USDT",
    "DOGE-USDT", "ADA-USDT", "AVAX-USDT", "DOT-USDT", "LINK-USDT",
    "LTC-USDT", "ATOM-USDT", "NEAR-USDT", "APT-USDT", "SUI-USDT",
    "INJ-USDT", "TAO-USDT", "ARB-USDT", "OP-USDT", "TIA-USDT",
]

TIMEFRAMES = {
    "5m": 5, "15m": 15, "30m": 30, "1H": 60
}

def fetch_hl_candles(sym, tf_minutes, days=365):
    """Fetch candles from Hyperliquid API"""
    sym_hl = sym.replace("-USDT", "")
    end_ms = int(datetime.now().timestamp() * 1000)
    start_ms = end_ms - (days * 24 * 3600 * 1000)
    
    all_candles = []
    resolution = tf_minutes
    current_end = end_ms
    
    while current_end > start_ms:
        url = f"https://api.hyperliquid.xyz/info"
        payload = {
            "type": "candleSnapshot",
            "req": {
                "coin": sym_hl,
                "interval": f"{resolution}m" if resolution < 60 else f"{resolution//60}h",
                "startTime": max(start_ms, current_end - 200 * resolution * 60 * 1000),
                "endTime": current_end
            }
        }
        
        try:
            r = requests.post(url, json=payload, timeout=10)
            data = r.json()
            if not data:
                break
            for c in data:
                all_candles.append({
                    "ts": c["t"],
                    "open": float(c["o"]),
                    "high": float(c["h"]),
                    "low": float(c["l"]),
                    "close": float(c["c"]),
                    "volume": float(c["v"])
                })
            current_end = data[0]["t"] - 1 if data else current_end - (resolution * 60 * 1000)
            time.sleep(0.1)  # Rate limit
        except Exception as e:
            print(f"  Error {sym} {tf_minutes}m: {e}")
            time.sleep(1)
            break
    
    if all_candles:
        df = pd.DataFrame(all_candles)
        df = df.sort_values("ts").drop_duplicates(subset=["ts"]).reset_index(drop=True)
        return df
    return None

print("="*60)
print("  FETCHING 365 DAYS OF HYPERLIQUID DATA")
print("="*60)

total = len(SYMBOLS) * len(TIMEFRAMES)
done = 0

for sym in SYMBOLS:
    for tf_name, tf_min in TIMEFRAMES.items():
        fname = f"{sym.replace('-','_')}_{tf_name}_365d.parquet"
        fpath = os.path.join(CACHE, fname)
        
        if os.path.exists(fpath):
            done += 1
            continue
        
        print(f"[{done+1}/{total}] {sym} {tf_name}...", end=" ", flush=True)
        df = fetch_hl_candles(sym, tf_min, 365)
        
        if df is not None and len(df) > 100:
            df.to_parquet(fpath)
            print(f"✅ {len(df)} candles saved")
        else:
            print(f"❌ No data")
        
        done += 1
        time.sleep(0.2)

print(f"\nDone. {done}/{total} files checked.")
print(f"Cache: {CACHE}")
