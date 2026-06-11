#!/usr/bin/env python3
"""Check SDK signatures"""
import inspect, os, sys
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
sys.path.insert(0, here)
import bot
client = bot.BloFin().client
print("place_algo_order params:")
for p in inspect.signature(client.trading.place_algo_order).parameters.values():
    print(f"  {p.name}: {p.default if p.default is not inspect.Parameter.empty else 'REQUIRED'}")
print()
print("place_tpsl_order params:")
for p in inspect.signature(client.trading.place_tpsl_order).parameters.values():
    print(f"  {p.name}: {p.default if p.default is not inspect.Parameter.empty else 'REQUIRED'}")
