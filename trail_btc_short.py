#!/usr/bin/env python3
"""Trail BTC short stop loss - run every 15 minutes"""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
sys.path.insert(0, here)
import bot

bf = bot.BloFin()
trading = bf.client.trading

# Get position
pos = bf.positions()
btc_pos = next((p for p in pos if 'BTC' in p.get('symbol','')), None)
if not btc_pos or abs(btc_pos['qty']) < 1:
    print("No BTC position - nothing to trail")
    sys.exit(0)

entry = btc_pos['avg_price']
qty = abs(btc_pos['qty'])
upnl = btc_pos['upnl']

# BTC price
tickers = bf.tickers()
btc_price = float(next((t for t in tickers if t.get('instId') == 'BTC-USDT'), None)['last'])

print(f"BTC: ${btc_price:,.2f} | Entry: ${entry:.2f} | Size: {qty} | uPnl: ${upnl:+.2f}")
print(f"Distance: {(btc_price-entry)/entry*100:+.2f}%")

# Calculate trail prices
# For short: TP trails DOWN (0.6% below current), SL trails DOWN too (0.5% above)
trail_pct = 0.5  # 0.5% trail distance
tp_pct = 0.6     # take profit at 0.6% below
tp_price = round(btc_price * (1 - tp_pct/100), 1)
sl_price = round(btc_price * (1 + trail_pct/100), 1)

print(f"Trail SL: ${sl_price:,.2f} ({(btc_price - sl_price)/btc_price*100:+.2f}% above)")
print(f"Trail TP: ${tp_price:,.2f} ({(tp_price - btc_price)/btc_price*100:+.2f}% below)")

# Check existing TP/SL
old_sl_price = None
try:
    stops = trading.get_active_tpsl_orders(inst_id='BTC-USDT')
    for o in stops.get('data', []):
        if o.get('side') == 'buy':  # buy to close short
            old_sl = o.get('slTriggerPrice')
            old_tp = o.get('tpTriggerPrice')
            if old_sl:
                old_sl_price = float(old_sl)
                print(f"\nExisting: SL=${old_sl:,.2f} TP=${old_tp:,.2f}")
except Exception as e:
    print(f"Check existing: {e}")
    old_sl_price = None

# Only update if price has moved enough to tighten the SL
if old_sl_price and sl_price < old_sl_price:
    # Price dropped - we can tighten the SL
    print(f"\nBTC dropped! SL can tighten from ${old_sl_price:,.2f} → ${sl_price:,.2f}")
    
    # Cancel old
    for o in stops.get('data', []):
        trading.cancel_tpsl_order(inst_id='BTC-USDT', tpsl_id=o['tpslId'])
    
    # Place new
    result = trading.place_tpsl_order(
        inst_id='BTC-USDT',
        margin_mode='isolated',
        position_side='net',
        side='buy',
        size=str(qty),
        tp_trigger_price=str(tp_price),
        tp_order_price=str(tp_price),
        sl_trigger_price=str(sl_price),
        sl_order_price=str(sl_price),
        sl_trigger_price_type='last',
        tp_trigger_price_type='last',
        reduce_only='true',
    )
    print(f"Updated: {json.dumps(result, indent=2)}")
    if result.get('code') == '0':
        print(f"✅ TRAIL UPDATED: SL=${sl_price:,.2f} TP=${tp_price:,.2f}")
    else:
        print(f"❌ Failed: {result.get('msg')}")
elif old_sl_price and sl_price >= old_sl_price:
    print(f"\nBTC didn't drop enough. SL stays at ${old_sl_price:,.2f}")
else:
    print(f"\nNo existing SL found. Setting initial: SL=${sl_price:,.2f} TP=${tp_price:,.2f}")
    result = trading.place_tpsl_order(
        inst_id='BTC-USDT',
        margin_mode='isolated',
        position_side='net',
        side='buy',
        size=str(qty),
        tp_trigger_price=str(tp_price),
        tp_order_price=str(tp_price),
        sl_trigger_price=str(sl_price),
        sl_order_price=str(sl_price),
        sl_trigger_price_type='last',
        tp_trigger_price_type='last',
        reduce_only='true',
    )
    print(f"Result: {json.dumps(result, indent=2)}")
