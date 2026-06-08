#!/usr/bin/env python3
"""
DOCTOR AGENT v3 — bulletproof self-healing monitor.
Checks every 5 minutes. Kills ghosts, frees ports, restarts cleanly.
NEVER kills itself. Run via nohup so it survives terminal closure.
"""

import os, sys, time, subprocess, re
from datetime import datetime, timezone

WORK = os.path.expanduser("~/multi_agent_bot")
LOG_DIR = os.path.join(WORK, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
DOCTOR_LOG = os.path.join(LOG_DIR, "doctor.log")
PYTHON = "/opt/homebrew/Caskroom/miniconda/base/bin/python"

# My own PID so I never kill myself
MY_PID = os.getpid()


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(DOCTOR_LOG, "a") as f:
        f.write(line + "\n")


def check_bot():
    """
    Returns (count_of_real_bot_processes, [pid_list]).
    Filters out: doctor_agent, hyperliquid_bot, bash wrappers, grep, self.
    """
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        real = []
        for line in result.stdout.split("\n"):
            # Must contain bot.py
            if "bot.py" not in line:
                continue
            # Filter out non-bot entries
            if "doctor_agent" in line:
                continue
            if "hyperliquid" in line:
                continue
            if "grep" in line:
                continue
            # Extract PID
            parts = line.split()
            if len(parts) < 2:
                continue
            pid = int(parts[1])
            # Never count myself
            if pid == MY_PID:
                continue
            # Get the command
            cmd = " ".join(parts[10:]) if len(parts) > 10 else ""
            # Only count actual python bot.py processes, not bash wrappers
            # Check: command contains both "python" and "bot.py" (or the full path)
            if ("python" in cmd) and ("bot.py" in cmd):
                real.append(pid)
            else:
                # Bash wrapper — flag it as a zombie
                real.append(pid)
        return len(real), real
    except:
        return 0, []


def port_free():
    try:
        result = subprocess.run(["lsof", "-ti:8787"], capture_output=True, text=True, timeout=5)
        return not bool(result.stdout.strip())
    except:
        return True


def restart_bot():
    """Kill zombies, free port, start clean. Returns True if started.
    ONLY kills bot.py processes in ~/multi_agent_bot — NEVER hyperliquid_bot.
    """
    log("🔄 Killing all stale bot-related processes")

    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split("\n"):
            if "bot.py" not in line:
                continue
            if "doctor_agent" in line:
                continue
            if "hyperliquid" in line:
                continue
            if "grep" in line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            pid = int(parts[1])
            if pid == MY_PID:
                continue
            try:
                os.kill(pid, 9)
                log(f"  Killed PID {pid}")
            except:
                pass
    except:
        pass

    time.sleep(2)

    # Free port 8787
    subprocess.run("lsof -ti:8787 | xargs kill -9 2>/dev/null", shell=True, timeout=5)
    time.sleep(1)

    # Start fresh — no shell wrapper, directly with Popen
    proc = subprocess.Popen(
        [PYTHON, os.path.join(WORK, "bot.py")],
        cwd=WORK,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log(f"✅ Bot restarted — PID {proc.pid}")
    return True


def doctor():
    log("🩺 DOCTOR v3 active — checking every 5min")
    log(f"  My PID: {MY_PID}")
    log(f"  Python: {PYTHON}")

    while True:
        try:
            count, pids = check_bot()
            port_ok = port_free()

            if count == 0:
                log(f"🚨 Bot DEAD (count=0) — restarting")
                restart_bot()

            elif count >= 3:
                log(f"⚠️ {count} bot-like processes ({pids}) — killing all and restarting clean")
                restart_bot()
            elif count == 2:
                # One real bot + one zombie/bash wrapper
                log(f"⚠️ {count} processes — cleaning extra")
                # Kill the non-python one
                try:
                    result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
                    for line in result.stdout.split("\n"):
                        if "bot.py" not in line:
                            continue
                        if "doctor_agent" in line:
                            continue
                        if "grep" in line:
                            continue
                        parts = line.split()
                        if len(parts) < 2:
                            continue
                        pid = int(parts[1])
                        if pid == MY_PID:
                            continue
                        cmd = " ".join(parts[10:]) if len(parts) > 10 else ""
                        if PYTHON not in cmd and "bot.py" in cmd:
                            # Bash wrapper — kill it
                            try:
                                os.kill(pid, 9)
                                log(f"  Killed bash wrapper PID {pid}")
                            except:
                                pass
                except:
                    pass
            elif not port_ok:
                log("⚠️ Port 8787 stuck — freeing")
                subprocess.run("lsof -ti:8787 | xargs kill -9 2>/dev/null", shell=True, timeout=5)

            log(f"💤 Bot={count} process(es) | port={'free' if port_ok else 'stuck'} | PID list: {pids}")

        except Exception as e:
            log(f"⚠️ Doctor error: {e}")

        time.sleep(300)


if __name__ == "__main__":
    doctor()
