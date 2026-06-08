#!/usr/bin/env python3
"""Wrapper: run backtest using cached data (no network needed), write leaderboard to bt_results.json"""
import os, sys, time, json

os.environ['HOME'] = '/sessions/laughing-youthful-galileo/mnt'
sys.argv = ['backtest.py', '--days', '365', '--symbols', 'all']

# Patch getmtime so cache always looks fresh (avoids re-fetch attempts)
os.path.getmtime = lambda path: time.time() - 60

os.chdir('/sessions/laughing-youthful-galileo/mnt/multi_agent_bot')
exec(open('backtest.py').read())
