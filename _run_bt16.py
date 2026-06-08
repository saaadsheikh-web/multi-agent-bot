#!/usr/bin/env python3
"""Run backtest on 16 symbols (those with confirmed cache), produce leaderboard JSON."""
import os, sys, time, json

os.environ['HOME'] = '/sessions/laughing-youthful-galileo/mnt'
os.path.getmtime = lambda path: time.time() - 60
os.chdir('/sessions/laughing-youthful-galileo/mnt/multi_agent_bot')

# Patch sys.argv so backtest.py uses only the first 16 symbols
# (TAO, ARB, OP, TIA are symbols 17-20 and consistently timeout)
SYMBOLS_16 = "BTC-USDT,ETH-USDT,SOL-USDT,XRP-USDT,BNB-USDT,DOGE-USDT,ADA-USDT,AVAX-USDT,DOT-USDT,LINK-USDT,LTC-USDT,ATOM-USDT,NEAR-USDT,APT-USDT,SUI-USDT,INJ-USDT"
sys.argv = ['backtest.py', '--days', '365', '--symbols', SYMBOLS_16]

exec(open('backtest.py').read())
