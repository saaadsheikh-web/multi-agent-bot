#!/usr/bin/env python3
"""
DOCTOR AGENT — Self-healing monitor. Checks every 2 hours.
Detects issues → auto-fixes → reports. Keeps the bot alive and printing money.
"""

import os, sys, time, json, subprocess, re
from datetime import datetime, timezone
from collections import defaultdict

WORK = os.path.expanduser("~/multi_agent_bot")
LOG_DIR = os.path.join(WORK, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

DOCTOR_LOG = os.path.join(LOG_DIR, "doctor.log")

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(DOCTOR_LOG, "a") as f:
        f.write(line + "\n")

def check_bot_running():
    """Is bot.py process alive?"""
    try:
        result = subprocess.run(["pgrep", "-f", "bot.py"], capture_output=True, text=True, timeout=5)
        pids = [p for p in result.stdout.strip().split("\n") if p]
        if len(pids) >= 1:
            return True, len(pids)
        return False, 0
    except:
        return False, 0

def check_port_8787():
    """Is the webhook port in use?"""
    try:
        result = subprocess.run(["lsof", "-ti:8787"], capture_output=True, text=True, timeout=5)
        return bool(result.stdout.strip())
    except:
        return False

def check_rate_limits():
    """Count 429 errors in recent bot output."""
    try:
        # Find latest bot output file
        tasks_dir = os.path.expanduser("~/.claude/projects/-Users-saad--hermes-hermes-agent")
        # Check last 200 lines of the latest output
        result = subprocess.run(
            f"find /private/tmp -name '*.output' -newer '{WORK}/bot.py' 2>/dev/null | head -1",
            shell=True, capture_output=True, text=True, timeout=5
        )
        output_file = result.stdout.strip()
        if not output_file:
            return 0
        result2 = subprocess.run(["tail", "-200", output_file], capture_output=True, text=True, timeout=5)
        return result2.stdout.count("429")
    except:
        return -1

def check_api_health():
    """Can we reach the BloFin API?"""
    try:
        import requests
        r = requests.get("https://openapi.blofin.com/api/v1/market/tickers?instType=SWAP", timeout=5)
        return r.status_code == 200
    except:
        return False

def check_disk_space():
    """Any disk issues?"""
    try:
        result = subprocess.run(["df", "-h", os.path.expanduser("~")], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            use_pct = int(lines[1].split()[-2].replace("%", ""))
            return use_pct < 90
        return True
    except:
        return True

def check_memory():
    """Is the bot using too much memory?"""
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split("\n"):
            if "bot.py" in line and "python" in line:
                mem = float(line.split()[3])
                if mem > 10.0:  # >10% memory
                    return False, mem
                return True, mem
        return True, 0
    except:
        return True, 0

def kill_stuck_processes():
    """Kill zombie bot processes (more than 2 is suspicious)."""
    alive, count = check_bot_running()
    if count > 3:
        log(f"⚠️ {count} bot processes found — killing zombies")
        subprocess.run(["pkill", "-f", "bot.py"], timeout=5)
        time.sleep(2)
        subprocess.run(["pkill", "-9", "-f", "bot.py"], timeout=5)
        time.sleep(2)
        return True
    return False

def restart_bot():
    """Restart the bot clean."""
    log("🔄 Restarting bot...")
    subprocess.run(["pkill", "-9", "-f", "bot.py"], timeout=5)
    time.sleep(3)
    # Clear port if stuck
    subprocess.run("lsof -ti:8787 | xargs kill -9 2>/dev/null", shell=True, timeout=5)
    time.sleep(1)
    subprocess.Popen(
        ["python3", "-u", os.path.join(WORK, "bot.py")],
        cwd=WORK,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log("✅ Bot restarted")

def log_status(checks):
    """Write health report."""
    report = f"""
{'='*60}
DOCTOR REPORT — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
{'='*60}
Bot running: {checks['bot_running']} ({checks['bot_processes']} processes)
Webhook port: {checks['port_8787']}
API health: {checks['api_health']}
Rate limits: {checks['rate_limits']} (last 200 lines)
Disk space: {checks['disk_space']}
Memory: {checks['memory']:.1f}%
{'='*60}
"""
    log(report.strip())
    with open(os.path.join(LOG_DIR, "doctor_report.txt"), "w") as f:
        f.write(report)

def main():
    log("🩺 DOCTOR AGENT STARTED — checking every 2 hours")

    issues_found = 0
    restarts_today = 0

    while True:
        # Run checks
        alive, processes = check_bot_running()
        checks = {
            "bot_running": alive,
            "bot_processes": processes,
            "port_8787": check_port_8787(),
            "api_health": check_api_health(),
            "rate_limits": check_rate_limits(),
            "disk_space": check_disk_space(),
        }
        ok, mem = check_memory()
        checks["memory"] = mem

        log_status(checks)

        # HEALING LOGIC

        # 1. Bot not running → restart
        if not alive:
            log("🚨 CRITICAL: Bot is DEAD — restarting!")
            restart_bot()
            issues_found += 1
            restarts_today += 1

        # 2. Too many processes → kill zombies
        elif processes > 3:
            if kill_stuck_processes():
                issues_found += 1
                # Re-check if bot still alive after zombie kill
                alive2, _ = check_bot_running()
                if not alive2:
                    restart_bot()
                    restarts_today += 1

        # 3. Rate limits piling up → restart with delay
        if checks["rate_limits"] > 100:
            log(f"⚠️ {checks['rate_limits']} rate limits — increasing scan interval recommended")
            issues_found += 1

        # 4. API down → wait and retry
        if not checks["api_health"]:
            log("🚨 API unreachable — Cloudflare block likely. Waiting 5 min.")
            time.sleep(300)
            # Retry after wait
            if not check_api_health():
                log("🚨 API still down after 5 min wait")

        # 5. Memory leak → restart
        if mem > 10.0:
            log(f"🚨 Memory at {mem:.1f}% — restarting to prevent crash")
            restart_bot()
            restarts_today += 1

        # Reset daily restart counter at midnight
        if datetime.now(timezone.utc).hour == 0:
            restarts_today = 0

        log(f"💤 Sleeping 2 hours. Issues fixed: {issues_found}. Restarts today: {restarts_today}")
        time.sleep(7200)  # 2 hours

if __name__ == "__main__":
    main()
