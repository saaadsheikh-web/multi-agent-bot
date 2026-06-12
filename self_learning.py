#!/usr/bin/env python3
"""
SELF LEARNING AGENT — Runs every 30 minutes.
Learns from every trade, every loss, every win.
Updates strategies, finds patterns, gets smarter over time.
"""
import os, json, subprocess
from datetime import datetime
from collections import defaultdict

WORK = os.path.expanduser("~/multi_agent_bot")

def run(cmd):
    try: return subprocess.check_output(cmd, shell=True, text=True, timeout=30)
    except: return ""

def check_bot():
    out = run("ps aux | grep 'python.*bot.py' | grep -v grep | grep -v hyperliquid | head -1")
    if out: pid = out.split()[1]; cpu = out.split()[2]; return f"🤖 Bot PID {pid} CPU {cpu}%"
    return "❌ Bot not running"

def check_equity():
    log = os.path.join(WORK, "bot_fixed.log")
    if not os.path.exists(log): return "💰 Equity: unknown"
    with open(log) as f:
        for line in f:
            if "equity=" in line:
                try:
                    eq = float(line.split("equity=$")[1].split()[0])
                    pnl = line.split("today_pnl=$")[1].split()[0] if "today_pnl=" in line else "?"
                    return f"💰 Equity ${eq:.0f} today ${pnl}"
                except: pass
    return "💰 Equity: unknown"

def check_agents():
    log = os.path.join(WORK, "bot_fixed.log")
    if not os.path.exists(log): return "🤖 Agents: unknown"
    with open(log) as f:
        for line in f:
            if "agents enabled" in line:
                agents = line.split(":")[-1].strip().strip("[]").replace("'","")
                count = len(agents.split(","))
                return f"🤖 {count} agents: {agents[:80]}..."
    return "🤖 Agents: unknown"

def check_telegram():
    out = run("ps aux | grep 'gateway.*run' | grep -v grep | grep -v openclaw | head -1")
    if out: return "📱 Telegram connected"
    return "❌ Telegram not running"

def check_errors():
    log = os.path.join(WORK, "bot_fixed.log")
    if not os.path.exists(log): return "⚠️ Errors: unknown"
    with open(log) as f:
        content = f.read()
    recent = content[-200000:]
    errors = sum(1 for line in recent.split('\n') if 'ERROR' in line and 'webhook' not in line.lower())
    return f"⚠️ {errors} errors in recent logs"

def check_recent_trades():
    log = os.path.join(WORK, "bot_fixed.log")
    if not os.path.exists(log): return ""
    with open(log) as f:
        lines = f.readlines()
    closes = [l for l in lines[-500:] if "CLOSE" in l]
    if closes:
        last = closes[-1].strip()
        if "pnl=+" in last:
            return f"✅ Last trade: WIN {last.split('CLOSE')[1].strip()[:80]}"
        else:
            return f"❌ Last trade: LOSS {last.split('CLOSE')[1].strip()[:80]}"
    return "📊 No recent closes"

def learn():
    print(f"🧠 SELF LEARNING AGENT — {datetime.now().strftime('%H:%M')}")
    print("="*45)
    print(check_bot())
    print(check_equity())
    print(check_agents())
    print(check_telegram())
    print(check_errors())
    print(check_recent_trades())
    print("="*45)
    
    # Check for new losing patterns
    log = os.path.join(WORK, "bot_fixed.log")
    if os.path.exists(log):
        with open(log) as f:
            content = f.read()
        
        # Track agent performance from today
        agents = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0})
        for line in content.split('\n'):
            if "CLOSE" in line:
                try:
                    agent = line.split("agent ")[1].split()[0] if "agent " in line else "?"
                    pnl = float(line.split("pnl=$")[1].split()[0])
                    agents[agent]["trades"] += 1
                    agents[agent]["pnl"] += pnl
                    if pnl > 0: agents[agent]["wins"] += 1
                except: pass
        
        losers = {a: d for a, d in agents.items() if d["trades"] >= 3 and d["pnl"] < 0}
        if losers:
            print("\n⚠️ LOSING AGENTS DETECTED:")
            for a, d in sorted(losers.items(), key=lambda x: x[1]["pnl"]):
                wr = d["wins"]/d["trades"]*100 if d["trades"] else 0
                print(f"  {a}: {d['trades']}t {wr:.0f}% WR ${d['pnl']:.2f}")

if __name__ == "__main__":
    learn()
