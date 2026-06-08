#!/usr/bin/env python3
"""Fetch 10m and 30m native candles from BloFin for all 20 symbols."""
import os, sys, time
import pandas as pd
from blofin import BloFinClient

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE = os.path.join(WORK_DIR, "backtest_data")
ENV = os.path.join(WORK_DIR, ".env")
if os.path.exists(ENV):
    with open(ENV) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k,v = line.split("=",1)
                os.environ.setdefault(k.strip(), v.strip())

SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT","BNB-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT",
           "LTC-USDT","ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT",
           "INJ-USDT","TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT"]
TIMEFRAMES = ["10m","30m"]
DAYS = 365

client = BloFinClient(
    api_key=os.environ.get("BLOFIN_API_KEY",""),
    api_secret=os.environ.get("BLOFIN_API_SECRET",""),
    passphrase=os.environ.get("BLOFIN_PASSPHRASE",""),
)

def fetch(symbol, bar, days):
    fname = os.path.join(CACHE, f"{symbol.replace('-','_')}_{bar}_{days}d.parquet")
    if os.path.exists(fname) and time.time() - os.path.getmtime(fname) < 21600:
        print(f"  {symbol:15s} {bar} → cached")
        return

    bar_min = {"10m":10,"30m":30}[bar]
    total = (days * 24 * 60) // bar_min
    rows, cursor = [], None
    for attempt in range(min(total//500 + 5, 20)):
        try:
            kw = dict(inst_id=symbol, bar=bar, limit=500)
            if cursor: kw["after"] = str(cursor)
            r = client.public.get_candlesticks(**kw)
            batch = (r or {}).get("data") or []
        except Exception as e:
            print(f"  {symbol:15s} {bar} error: {e}")
            break
        if not batch: break
        rows.extend(batch)
        cursor = int(batch[-1][0])
        if len(rows) >= total: break
        time.sleep(0.25)

    if rows:
        cols = ["ts","open","high","low","close","volume","vc","vcq","confirm"]
        df = pd.DataFrame([r[:len(cols)] for r in rows], columns=cols)
        for c in ["ts","open","high","low","close","volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df.drop_duplicates("ts").sort_values("ts").dropna(subset=["close"])
        df[["ts","open","high","low","close","volume"]].to_parquet(fname, index=False)
        print(f"  {symbol:15s} {bar} → {len(df)} candles")
    else:
        print(f"  {symbol:15s} {bar} → no data")

for tf in TIMEFRAMES:
    print(f"\nFetching {tf} candles...")
    for sym in SYMBOLS:
        fetch(sym, tf, DAYS)

print("\nDone.")
