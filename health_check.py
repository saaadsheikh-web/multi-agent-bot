#!/usr/bin/env python3
"""HEALTH CHECK — Reports everything cleanly every 5 minutes"""
import os, json, subprocess
from datetime import datetime

WORK = os.path.expanduser("~/multi_agent_bot")
LOG = os.path.join(WORK, "bot.log")

checks = []

# 1. Bot process
for line in os.popen("ps aux | grep 'python.*bot.py' | grep -v grep").readlines():
    parts = line.split()
    if len(parts) > 10:
        pid = parts[1]
        cpu = parts[2]
        mem = parts[3]
        uptime_sec = parts[9] if len(parts) > 9 else "?"
        checks.append(f"✅ Bot: PID {pid}, CPU {cpu}%, MEM {mem}%")

if not checks:
    checks.append("❌ Bot: NOT RUNNING!")

# 2. Equity from logs
equity_lines = []
if os.path.exists(LOG):
    with open(LOG) as f:
        for line in f:
            if "equity=" in line:
                try:
                    eq = float(line.split("equity=$")[1].split()[0])
                    equity_lines.append((line[:19], eq))
                except: pass

if equity_lines:
    latest = equity_lines[-1][1]
    change = latest - equity_lines[0][1] if len(equity_lines) > 10 else 0
    direction = "+" if change >= 0 else ""
    checks.append(f"💰 Equity: ${latest:.0f} ({direction}${change:.2f} today)")
else:
    checks.append("💰 Equity: Unknown (no log data)")

# 3. Agents
for line in os.popen(f"grep 'agents enabled' {LOG} 2>/dev/null | tail -1").readlines():
    if "agents enabled:" in line:
        agents = line.split("agents enabled:")[1].strip().strip("[]").replace("'","").split(", ")
        checks.append(f"🤖 Agents ({len(agents)}): {', '.join(agents[:5])}...")

# 4. Telegram
for line in os.popen("ps aux | grep 'gateway.*run' | grep -v grep | grep -v openclaw").readlines():
    parts = line.split()
    if len(parts) > 1:
        checks.append(f"📱 Telegram: active (PID {parts[1]})")

if not os.popen("ps aux | grep 'gateway.*run' | grep -v grep | grep -v openclaw").read():
    checks.append("❌ Telegram: NOT RUNNING")

# 5. Watchdog
for line in os.popen("hermes cron list 2>/dev/null | grep -i watch").readlines():
    checks.append(f"🔔 Watchdog: active")

# 6. Doctor
for line in os.popen("ps aux | grep doctor_agent | grep -v grep").readlines():
    parts = line.split()
    if len(parts) > 1:
        checks.append(f"🏥 Doctor: active (PID {parts[1]})")

# 7. GitHub
for line in os.popen("cd ~/multi_agent_bot && git log --oneline -1 2>/dev/null").readlines():
    checks.append(f"📦 GitHub: {line.strip()[:50]}")

# 8. Backtest data
data_count = len(os.listdir(os.path.join(WORK, "backtest_data"))) if os.path.exists(os.path.join(WORK, "backtest_data")) else 0
checks.append(f"📊 Backtest data: {data_count} files")

# 9. Errors in last hour
if os.path.exists(LOG):
    with open(LOG) as f:
        content = f.read()
    recent = content[-500000:] if len(content) > 500000 else content
    errors = sum(1 for line in recent.split('\n') if 'ERROR' in line or 'CRITICAL' in line)
    checks.append(f"⚠️ Recent errors: {errors} (last 500KB of logs)")

# 10. Mac sleep
for line in os.popen("pmset -g | grep sleep 2>/dev/null").readlines():
    checks.append(f"💻 Mac: {line.strip()}")

print(f"\n{'='*50}")
print(f"  HEALTH CHECK — {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*50}")
for c in checks:
    print(f"  {c}")
print(f"{'='*50}")
