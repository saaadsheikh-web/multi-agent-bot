#!/usr/bin/env python3
"""Set tight stop-loss on BTC short (no trailing, just tight SL)"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
sys.path.insert(0, here)
import bot

bf = bot.BloFin()
trading = bf.client.trading

# BTC price
tickers = bf.tickers()
btc_price = float(next((t for t in tickers if t.get('instId') == 'BTC-USDT'), None)['last'])
print(f"BTC current: ${btc_price:,.2f}")

pos = bf.positions()
btc_pos = next((p for p in pos if 'BTC' in p.get('symbol','')), None)
entry = btc_pos['avg_price']
qty = abs(btc_pos['qty'])
print(f"BTC short: entry=${entry:.2f}, size={qty}, uPnl=${btc_pos['upnl']:+.2f}")

# Try place_tpsl_order with valid TPs
# TP far away at $30k (won't hit, just to satisfy the API)
tp_far = 30000
# SL tight: 0.5% above current
sl_price = btc_price * 1.005

print(f"SL: trigger=${sl_price:,.2f}")
print(f"TP: ${tp_far:,.2f} (far away, won't hit)")

# Try different format
for tp_order_price in [str(tp_far), '-1', '0']:
    try:
        result = trading.place_tpsl_order(
            inst_id='BTC-USDT',
            margin_mode='isolated',
            position_side='net',
            side='buy',
            size=str(qty),
            tp_trigger_price=str(tp_far),
            tp_order_price=tp_order_price,
            sl_trigger_price=str(round(sl_price, 1)),
            sl_order_price=str(round(sl_price * 1.001, 1)),
            sl_trigger_price_type='last',
            sl_order_price_type='last',
            reduce_only='true',
        )
        print(f"With tp_order_price={tp_order_price}: {json.dumps(result, indent=2)}")
        if result.get('code') == '0':
            print("✅ SL SET!")
            break
    except Exception as e:
        print(f"With tp_order_price={tp_order_price}: {e}")
