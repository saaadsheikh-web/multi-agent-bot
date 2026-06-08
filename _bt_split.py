#!/usr/bin/env python3
"""
Run backtest in two batches of 8 symbols, combine all_trades, compute leaderboard.
Writes results to /tmp/bt_leaderboard.json and prints the table.
"""
import os, sys, time, json, math, traceback
import numpy as np
import pandas as pd

os.environ['HOME'] = '/sessions/laughing-youthful-galileo/mnt'
os.path.getmtime = lambda path: time.time() - 60
os.chdir('/sessions/laughing-youthful-galileo/mnt/multi_agent_bot')

# Import backtest internals by exec-ing with a guard
_bt_code = open('backtest.py').read()
# Replace __name__ == "__main__" call so main() doesn't run
_bt_code = _bt_code.replace('if __name__ == "__main__":\n    main()', '# main() suppressed')
exec(_bt_code, globals())

UNIVERSE_BATCH1 = [
    "BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT",
    "BNB-USDT","DOGE-USDT","ADA-USDT","AVAX-USDT",
]
UNIVERSE_BATCH2 = [
    "DOT-USDT","LINK-USDT","LTC-USDT","ATOM-USDT",
    "NEAR-USDT","APT-USDT","SUI-USDT","INJ-USDT",
]
UNIVERSE_BATCH3 = [
    "TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT",
]

def run_batch(symbols, label):
    client = _client()
    all_trades = []
    for sym in symbols:
        try:
            df5  = load_or_fetch(client, sym, "5m",  365)
            df15 = load_or_fetch(client, sym, "15m", 365)
            df1h = load_or_fetch(client, sym, "1H",  365)
            if df15.empty or len(df15) < 200:
                print(f"  [{label}] {sym}: skipped (no data)")
                continue
            p = PrecomputedData(df5, df15, df1h)
            trades = simulate(p, symbol=sym)
            for t in trades:
                t["symbol"] = sym
            all_trades.extend(trades)
            by_agent = {}
            for t in trades:
                by_agent[t["agent"]] = by_agent.get(t["agent"], 0) + 1
            print(f"  [{label}] {sym}: {len(trades)} trades")
        except Exception as e:
            print(f"  [{label}] {sym}: ERROR {e}")
    return all_trades

BATCH = int(sys.argv[1]) if len(sys.argv) > 1 else 1
OUTFILE = f"/tmp/bt_batch{BATCH}.json"

if BATCH == 1:
    trades = run_batch(UNIVERSE_BATCH1, "B1")
elif BATCH == 2:
    trades = run_batch(UNIVERSE_BATCH2, "B2")
else:
    trades = run_batch(UNIVERSE_BATCH3, "B3")

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super().default(obj)

with open(OUTFILE, 'w') as f:
    json.dump(trades, f, cls=NpEncoder)
print(f"[done] {len(trades)} trades written to {OUTFILE}")
