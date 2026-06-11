#!/usr/bin/env python3
"""Get positions via bot's BloFin wrapper"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
# Import the bot to use its BloFin class
sys.path.insert(0, here)
import bot
bf = bot.BloFin()
pos = bf.positions()
import json
for p in pos:
    symbol = p.get('symbol','?')
    side = p.get('side','?')
    qty = p.get('qty',0)
    avg_price = p.get('avg_price',0)
    upnl = p.get('upnl',0)
    leverage = p.get('leverage',5)
    print(f"{symbol:15s} SIDE={side:5s} QTY={qty:>8.4f} AVG=${avg_price:<10.2f} uPnl=${upnl:<+8.2f} Lev={leverage}x")
