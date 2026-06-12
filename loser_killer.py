#!/usr/bin/env python3
"""Live loser-killer — checks if any BloFin winner bleeds live.
If an agent has >=5 trades and avg_pnl < -$2/trade, flag it.
If an agent has >=10 trades and total_pnl < 0, flag it.
Output is sent via cron to Saad."""

import sqlite3, os, json

DB = os.path.expanduser("~/multi_agent_bot/bot.db")
BLOFIN_WINNERS = ["livermore_pivot", "daily_breakout_48h", "daily_breakout_7d", 
                  "wide_candle", "donchian", "daily_breakout_24h", "fib_786_oversold",
                  "fib_bounce", "daily_breakout_12h", "daily_breakout_2h", 
                  "williams_r", "volume_capitulation"]

def check():
    if not os.path.exists(DB):
        print("⚠️ No DB yet — bot may not have traded")
        return

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("""
        SELECT agent, COUNT(*) as trades, 
               COALESCE(SUM(pnl), 0) as total_pnl
        FROM trades 
        WHERE status='closed' AND pnl IS NOT NULL
        GROUP BY agent 
        ORDER BY total_pnl ASC
    """)
    
    results = {r['agent']: r for r in c.fetchall()}
    conn.close()
    
    losers = []
    healthy = []
    no_trade = []
    
    for agent in BLOFIN_WINNERS:
        r = results.get(agent)
        if not r:
            no_trade.append(agent)
            continue
        trades = r['trades']
        pnl = r['total_pnl']
        
        if trades >= 5 and (pnl < 0 or (pnl / trades) < -2.0):
            losers.append((agent, trades, pnl))
        elif trades >= 10 and pnl < 0:
            losers.append((agent, trades, pnl))
        else:
            healthy.append((agent, trades, pnl))
    
    if losers:
        print("⚠️ LOSING AGENTS LIVE - RECOMMEND KILL:")
        print(f"  {'Agent':>25s} | {'Trades':>6s} | {'PnL $':>10s} | {'Avg/Trade':>10s}")
        print("  " + "-" * 55)
        for a, t, p in losers:
            print(f"  ❌ {a:>25s} | {t:>6d} | ${p:>+8.2f} | ${p/t:>+8.2f}")
        print()
        print("  ➡ Run: hermes says 'kill agent_name' to remove it from bot.py")
    else:
        print("✅ All active agents are profitable or have too few trades to judge.")
    
    if healthy:
        print(f"\n✅ Healthy agents: {', '.join(a for a,_,_ in healthy)}")
    
    if no_trade:
        print(f"\n🔄 Waiting for trades: {', '.join(no_trade)}")

check()
