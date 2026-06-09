#!/usr/bin/env python3
"""WATCHDOG — Check for errors every 5 minutes"""
import os
from datetime import datetime

WORK = os.path.expanduser("~/multi_agent_bot")

checks = []

# 1. Bot alive
bot_found = False
for line in os.popen("ps aux | grep 'python.*bot.py' | grep -v grep").readlines():
    bot_found = True
    parts = line.split()
    if len(parts) > 3:
        checks.append(f"✅ Bot running (PID {parts[1]})")
if not bot_found:
    checks.append("❌ BOT NOT RUNNING")

# 2. Recent errors
log = os.path.join(WORK, "bot_fixed.log")
if os.path.exists(log):
    with open(log) as f:
        content = f.read()
    recent = content[-200000:]
    errors = sum(1 for line in recent.split('\n') if 'ERROR' in line or 'CRITICAL' in line)
    checks.append(f"⚠️ {errors} errors in last logs")

# 3. Agents
for line in os.popen(f"grep 'agents enabled' {log} 2>/dev/null | tail -1").readlines():
    if 'agents enabled:' in line:
        agents = line.split(':')[1].strip().strip('[]').replace("'","").split(', ')
        checks.append(f"🤖 {len(agents)} agents: {', '.join(agents[:4])}...")

# 4. Equity
for line in os.popen(f"grep 'equity=' {log} 2>/dev/null | tail -1").readlines():
    try:
        eq = float(line.split('equity=$')[1].split()[0])
        checks.append(f"💰 Equity: ${eq:.0f}")
    except: pass

print(f"WATCHDOG — {datetime.now().strftime('%H:%M')}")
for c in checks:
    print(f"  {c}")
