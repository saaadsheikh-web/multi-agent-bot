#!/usr/bin/env python3
"""Check BTC short position details"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
for line in open(os.path.join(here, '.env')):
    line = line.strip()
    if line and '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        os.environ[k.strip()] = v.strip().strip("'\"")
from blofin import BloFinClient
bf = BloFinClient()
# Try getting all positions
pos = bf.get_positions() if hasattr(bf, 'get_positions') else bf.positions() if hasattr(bf, 'positions') else None
if pos is None:
    # Try balance endpoint
    bal = bf.get_balance() if hasattr(bf, 'get_balance') else bf.balance() if hasattr(bf, 'balance') else None
    print("Balance:", json.dumps(bal, indent=2, default=str)[:1000] if bal else "No balance method")
else:
    print("Positions:", json.dumps(pos, indent=2, default=str)[:2000])
# Try trade history
print("\n--- Methods ---")
print([m for m in dir(bf) if not m.startswith('_')])
