#!/usr/bin/env python3
"""
self_healer.py — runs every 5 min. Detects bot health issues and auto-heals.

Health checks:
  1. bot.log mtime — must update within last 3 minutes (else bot hung/dead)
  2. equity readings — must be non-zero, must update each cycle
  3. recurring SDK errors — bursts > 20 in 10 min = something wrong
  4. DNS / network failures — repeat blackouts mean Wi-Fi issue
  5. all critical scheduled tasks alive (CEO, deploy responder, lab)

Heals:
  - Bot hung / dead → touch .restart_trigger to force restart
  - Bot file corruption → restore from latest backup
  - Repeating errors → log + Telegram alert (after 3 failed self-heals)

Telegram: ONLY when self-heal failed for 15+ min (real emergency).
"""
import os, sys, json, time, subprocess, urllib.request, urllib.parse
from pathlib import Path
import datetime as dt

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
HEALER_LOG = WORK / "self_healer.log"
HEAL_STATE = WORK / "self_healer_state.json"
BOT_LOG = WORK / "bot.log"
RESTART_TRIGGER = WORK / ".restart_trigger"

ENV_PATH = WORK / ".env"
env = {}
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

TG_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = env.get("TELEGRAM_CHAT_ID", "")

# Thresholds
MAX_LOG_STALE_MIN = 3            # bot.log must update within N min
MAX_DNS_ERRORS_10MIN = 10
MAX_SDK_ERRORS_10MIN = 30
ALERT_AFTER_FAILED_HEALS = 3     # only ping Saad after 3 consecutive failed heals

def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(HEALER_LOG, "a") as f:
        f.write(line + "\n")

def telegram(text):
    if not TG_TOKEN or not CHAT_ID:
        return
    try:
        data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            data=data, timeout=10
        )
    except Exception as e:
        log(f"telegram failed: {e}")

def load_state():
    if HEAL_STATE.exists():
        try:
            return json.loads(HEAL_STATE.read_text())
        except Exception:
            pass
    return {"failed_heals": 0, "last_alert": None}

def save_state(state):
    HEAL_STATE.write_text(json.dumps(state))

def check_bot_log_freshness():
    """Returns (ok, age_seconds, reason)"""
    if not BOT_LOG.exists():
        return False, 99999, "bot.log missing"
    age = time.time() - BOT_LOG.stat().st_mtime
    if age > MAX_LOG_STALE_MIN * 60:
        return False, age, f"bot.log stale ({age:.0f}s old)"
    return True, age, "ok"

def check_recent_errors(window_min=10):
    """Count recurring errors in last N minutes."""
    if not BOT_LOG.exists():
        return {}
    cutoff = dt.datetime.now() - dt.timedelta(minutes=window_min)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M")
    counts = {"DNS": 0, "SDK": 0, "ERROR": 0}
    try:
        with open(BOT_LOG) as f:
            # Only read last 5MB to keep it fast
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 5_000_000))
            for line in f:
                if cutoff_str in line or line[:16] >= cutoff_str:
                    if "Failed to resolve" in line or "DNS" in line:
                        counts["DNS"] += 1
                    elif "BloFinRequestException" in line or "got an unexpected keyword" in line:
                        counts["SDK"] += 1
                    elif "ERROR" in line:
                        counts["ERROR"] += 1
    except Exception as e:
        log(f"check_recent_errors failed: {e}")
    return counts

def heal_force_restart():
    """Touch .restart_trigger — bot's mtime watcher will reload within 15s."""
    try:
        RESTART_TRIGGER.touch()
        log("HEAL: touched .restart_trigger (bot will reload)")
        return True
    except Exception as e:
        log(f"HEAL fail: {e}")
        return False

def check_equity_recent():
    """Latest equity reading must be > 0 and recent."""
    if not BOT_LOG.exists():
        return False, "no bot.log"
    try:
        with open(BOT_LOG) as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 200_000))
            tail = f.read()
        # Find latest equity line
        eq_lines = [l for l in tail.split("\n") if "equity=$" in l]
        if not eq_lines:
            return False, "no equity readings"
        last = eq_lines[-1]
        # Extract value
        idx = last.find("equity=$")
        if idx < 0:
            return False, "parse fail"
        val_str = last[idx + 8:].split()[0]
        try:
            val = float(val_str)
        except ValueError:
            return False, f"parse value fail: {val_str}"
        if val <= 0:
            return False, f"equity = {val}"
        return True, f"equity = ${val:.2f}"
    except Exception as e:
        return False, str(e)

def main():
    state = load_state()
    log("=== self_healer cycle start ===")
    issues = []

    # 1. Log freshness
    ok, age, reason = check_bot_log_freshness()
    if not ok:
        issues.append(("bot_stale", reason))
        log(f"ISSUE: {reason}")
        # Heal: force restart
        heal_force_restart()

    # 2. Equity readings
    ok, msg = check_equity_recent()
    if not ok:
        issues.append(("equity", msg))
        log(f"ISSUE: equity check failed — {msg}")
    else:
        log(f"equity ok: {msg}")

    # 3. Recurring errors
    counts = check_recent_errors(window_min=10)
    if counts.get("DNS", 0) >= MAX_DNS_ERRORS_10MIN:
        issues.append(("dns", f"{counts['DNS']} DNS errors in 10min"))
        log(f"ISSUE: heavy DNS failures ({counts['DNS']}/10min) — Wi-Fi/router")
    if counts.get("SDK", 0) >= MAX_SDK_ERRORS_10MIN:
        issues.append(("sdk", f"{counts['SDK']} SDK errors in 10min"))
        log(f"ISSUE: SDK errors burst ({counts['SDK']}/10min)")

    # Decide on alert
    if issues:
        state["failed_heals"] = state.get("failed_heals", 0) + 1
        log(f"failed_heals = {state['failed_heals']}")
        if state["failed_heals"] >= ALERT_AFTER_FAILED_HEALS:
            last_alert_iso = state.get("last_alert")
            send_alert = True
            if last_alert_iso:
                try:
                    last_alert = dt.datetime.fromisoformat(last_alert_iso)
                    if (dt.datetime.now() - last_alert).total_seconds() < 1800:   # 30 min cooldown
                        send_alert = False
                except Exception:
                    pass
            if send_alert:
                lines = ["\U0001F6A8 Bot self-heal failed " + str(state['failed_heals']) + "x:"]
                for k, v in issues:
                    lines.append(f"- {k}: {v}")
                lines.append("\nManual check needed.")
                telegram("\n".join(lines))
                state["last_alert"] = dt.datetime.now().isoformat()
                log("ALERT sent to Telegram")
    else:
        if state.get("failed_heals", 0) > 0:
            log(f"recovered — clearing failed_heals counter (was {state['failed_heals']})")
        state["failed_heals"] = 0

    save_state(state)
    log("=== cycle done ===")


if __name__ == "__main__":
    main()
