#!/usr/bin/env python3
"""Check BTC short SL + fix trail script"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
sys.path.insert(0, here)
import bot

bf = bot.BloFin()
trading = bf.client.trading

pos = bf.positions()
btc_pos = next((p for p in pos if 'BTC' in p.get('symbol','')), None)
entry = btc_pos['avg_price']
qty = abs(btc_pos['qty'])
upnl = btc_pos['upnl']

tickers = bf.tickers()
btc_price = float(next((t for t in tickers if t.get('instId') == 'BTC-USDT'), None)['last'])
print(f"BTC: ${btc_price:,.2f} | Entry: ${entry:.2f} | Size: {qty} | uPnl: ${upnl:+.2f}")

# Check TP/SL orders
print("\n=== TP/SL Orders ===")
stops = trading.get_active_tpsl_orders(inst_id='BTC-USDT')
for o in stops.get('data', []):
    sid = o.get('side')
    sl = o.get('slTriggerPrice')
    tp = o.get('tpTriggerPrice')
    sz = o.get('size')
    # The script looks for side='buy' but this stores side as buy/sell for short close
    print(f"  id={o.get('tpslId')} side={sid} size={sz} SL={sl} TP={tp}")
    print(f"    raw: {json.dumps(o)[:200]}")

# The issue: format string error - existing check fails because of formatting
# Fix the trail script
print("\nPrice direction check:")
new_sl = round(btc_price * 1.005, 1)
new_tp = round(btc_price * 0.994, 1)
print(f"Would set: SL=${new_sl:,.2f} TP=${new_tp:,.2f}")
