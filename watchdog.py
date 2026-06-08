#!/usr/bin/env python3
"""
ERROR WATCHDOG — Runs every 5 minutes.
Scans all bot logs for errors, rate limits, position issues.
Alerts if anything needs attention.
"""
import os, json, time
from datetime import datetime, timedelta

WORK = os.path.expanduser("~/multi_agent_bot")
LOG_FILES = ["bot.log", "bot_final.log", "stdout.log", "stderr.log"]
STATE_FILE = os.path.join(WORK, "WATCHDOG_STATE.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_check": "", "errors_found": [], "alerts_sent": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def check_logs():
    """Check all log files for issues in the last 10 minutes."""
    now = datetime.now()
    cutoff = now - timedelta(minutes=10)
    
    issues = []
    
    # Check bot process is alive
    bot_alive = False
    for line in os.popen("ps aux | grep 'python.*bot.py' | grep -v grep").readlines():
        bot_alive = True
        break
    
    if not bot_alive:
        issues.append({"type": "CRITICAL", "msg": "Bot process is DOWN! Not running.", "time": str(now)})
    
    # Check each log file for errors
    for log_file in LOG_FILES:
        path = os.path.join(WORK, log_file)
        if not os.path.exists(path):
            continue
        
        size = os.path.getsize(path)
        # Only check last 500KB for recent issues
        if size > 500000:
            f = open(path)
            f.seek(max(0, size - 500000))
            recent = f.read()
            f.close()
        else:
            with open(path) as f:
                recent = f.read()
        
        # Check for critical errors
        for pattern, severity in [
            ("CRITICAL", "CRITICAL"),
            ("ERROR", "ERROR"),
            ("Traceback", "ERROR"),
            ("rate limit", "WARNING"),
            ("429", "WARNING"),
            ("could not determine price", "WARNING"),
            ("telegram 409", "WARNING"),
            ("connection refused", "ERROR"),
            ("timeout", "WARNING"),
            ("liquidat", "CRITICAL"),
            ("margin", "WARNING"),
            ("insufficient", "WARNING"),
        ]:
            if pattern.lower() in recent.lower():
                # Find the actual log line
                for line in recent.split('\n'):
                    if pattern.lower() in line.lower():
                        # Check if it's from the last 10 minutes
                        try:
                            ts_str = line[:23] if len(line) > 23 else ""
                            line_time = datetime.strptime(ts_str[:19], "%Y-%m-%d %H:%M:%S") if ts_str else None
                            if line_time and line_time > cutoff:
                                # Deduplicate - don't report same error twice
                                err_key = line[:100]
                                state = load_state()
                                if err_key not in [e.get("key","") for e in state.get("errors_found", [])]:
                                    issues.append({
                                        "type": severity,
                                        "msg": line.strip()[:200],
                                        "time": str(line_time),
                                        "file": log_file,
                                        "key": err_key
                                    })
                        except:
                            pass
                        break
    
    # Check equity trend
    for log_file in ["bot.log"]:
        path = os.path.join(WORK, log_file)
        if not os.path.exists(path): continue
        with open(path) as f:
            content = f.read()
        equity_lines = []
        for line in content.split('\n'):
            if "equity=" in line:
                try:
                    eq = float(line.split("equity=$")[1].split()[0])
                    equity_lines.append((line[:19], eq))
                except: pass
        
        if len(equity_lines) >= 2:
            latest = equity_lines[-1][1]
            earliest = equity_lines[0][1]
            change = latest - earliest
            if change < -50:
                issues.append({"type": "WARNING", "msg": f"Equity DOWN ${abs(change):.0f} in last session", "time": str(now)})
    
    return issues

# Run check
state = load_state()
issues = check_logs()

if issues:
    print(f"WATCHDOG: {len(issues)} issues found at {datetime.now()}")
    for issue in issues:
        print(f"  [{issue['type']}] {issue['msg'][:150]}")
    
    # Update state
    for issue in issues:
        if issue.get("key"):
            state["errors_found"].append({"key": issue["key"], "time": str(datetime.now())})
            # Keep last 100 errors
            if len(state["errors_found"]) > 100:
                state["errors_found"] = state["errors_found"][-100:]
    
    state["last_check"] = str(datetime.now())
    save_state(state)
else:
    print(f"WATCHDOG: All clear at {datetime.now()} — no issues found")
