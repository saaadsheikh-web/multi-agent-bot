#!/usr/bin/env python3
"""Per-agent PnL monitor — reports who's making/losing money live.
Run: python3 agent_monitor.py
Output: summary of all 12 BloFin winners + any trades on them."""

import sqlite3, json, os
from datetime import datetime, timezone

DB = os.path.expanduser("~/multi_agent_bot/bot.db")
LOG = os.path.expanduser("~/multi_agent_bot/bot.log")
BLOFIN_WINNERS = ["livermore_pivot", "daily_breakout_48h", "daily_breakout_7d", 
                  "wide_candle", "donchian", "daily_breakout_24h", "fib_786_oversold",
                  "fib_bounce", "daily_breakout_12h", "daily_breakout_2h", 
                  "williams_r", "volume_capitulation"]

def get_trade_stats():
    if not os.path.exists(DB):
        return {}
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # All closed trades per agent
    c.execute("""
        SELECT agent, 
               COUNT(*) as trades, 
               COALESCE(SUM(pnl), 0) as total_pnl,
               COALESCE(SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END), 0) as wins,
               COALESCE(SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END), 0) as losses,
               COALESCE(MAX(opened_at), 'never') as last_trade,
               COALESCE(MAX(closed_at), 'never') as last_closed
        FROM trades 
        WHERE status='closed' AND pnl IS NOT NULL
        GROUP BY agent 
        ORDER BY total_pnl DESC
    """)
    
    stats = {}
    for row in c.fetchall():
        stats[row['agent']] = dict(row)
    conn.close()
    return stats

def get_bot_status():
    if not os.path.exists(LOG):
        return "unknown"
    try:
        with open(LOG) as f:
            lines = f.readlines()
        for line in reversed(lines):
            if 'equity=' in line and 'today_pnl=' in line:
                eq = line.split('equity=')[1].split()[0] if 'equity=' in line else '?'
                tp = line.split('today_pnl=')[1].split()[0] if 'today_pnl=' in line else '?'
                return f"equity=${eq}  today=${tp}"
    except:
        pass
    return "no log data"

def get_open_positions():
    if not os.path.exists(DB):
        return 0
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM trades WHERE status='open'")
    n = c.fetchone()[0]
    conn.close()
    return n

print("=" * 80)
print(f"  AGENT MONITOR  —  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
print("=" * 80)

# Bot status
bs = get_bot_status()
open_pos = get_open_positions()
print(f"  Bot: {bs}  |  Open positions: {open_pos}")
print()

# Trade stats
stats = get_trade_stats()

print(f"{'Agent':>25s} | {'Trades':>6s} | {'Wins':>4s} | {'Loss':>4s} | {'WR%':>5s} | {'PnL $':>8s} | {'Last Trade':>16s}")
print("-" * 85)
no_trade_winners = []
for agent in BLOFIN_WINNERS:
    s = stats.get(agent)
    if s:
        wr = (s['wins'] / s['trades'] * 100) if s['trades'] > 0 else 0
        print(f"{agent:>25s} | {s['trades']:>6d} | {s['wins']:>4d} | {s['losses']:>4d} | {wr:>4.1f}% | ${s['total_pnl']:>+7.2f} | {s['last_closed'][:16]:>16s}")
    else:
        no_trade_winners.append(agent)

if no_trade_winners:
    print()
    print(f"  🔄 No trades yet: {', '.join(no_trade_winners)}")
    print(f"  (bots just restarted — waiting for signals)")

# Dead agents that still have losses
print()
print("LEGACY LOSSES (already disabled):")
for agent, s in sorted(stats.items(), key=lambda x: x[1]['total_pnl']):
    if agent not in BLOFIN_WINNERS and s['total_pnl'] < 0:
        wr = (s['wins'] / s['trades'] * 100) if s['trades'] > 0 else 0
        print(f"  ❌ {agent:>25s}: {s['trades']:>4d}t | ${s['total_pnl']:>+7.2f} | WR {wr:.0f}% | dead & disabled")

print()
print("=" * 80)
