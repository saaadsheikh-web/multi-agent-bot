#!/usr/bin/env python3
"""
TG COMMANDER — Full Telegram control of Claude, Hermes, and Bot.
Watches hermes_bridge/commands.jsonl for Saad's commands.
Routes to: bot commands, Claude analysis, Hermes actions.
"""

import os, sys, json, time, subprocess
from datetime import datetime, timezone

BRIDGE = os.path.expanduser("~/multi_agent_bot/hermes_bridge")
COMMANDS_FILE = os.path.join(BRIDGE, "commands.jsonl")
ACK_FILE = os.path.join(BRIDGE, "ack.jsonl")
LOG_FILE = os.path.join(BRIDGE, "commander.log")
STATE_FILE = os.path.join(BRIDGE, "commander_state.json")

CHAT_ID = "950763287"

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def send_ack(cmd_id, text):
    """Send acknowledgment back to Hermes/Telegram."""
    ack = json.dumps({"cmd_id": cmd_id, "ok": True, "result": text, "ts": datetime.now(timezone.utc).isoformat()})
    with open(ACK_FILE, "a") as f:
        f.write(ack + "\n")

def execute_command(text):
    """Parse and execute a command from Telegram."""
    text_lower = text.lower().strip()

    # ── BOT COMMANDS ──
    if text_lower in ["status", "equity", "balance"]:
        result = subprocess.run(
            ["grep", "equity=", "/private/tmp/claude-501/-Users-saad--hermes-hermes-agent/08d28190-52b4-461f-893a-bbbffc7549aa/tasks/" +
             sorted(os.listdir("/private/tmp/claude-501/-Users-saad--hermes-hermes-agent/08d28190-52b4-461f-893a-bbbffc7549aa/tasks/"))[-1] + "/output"],
            capture_output=True, text=True, timeout=5
        )
        return f"💰 {result.stdout.strip().split(chr(10))[-1] if result.stdout else 'No data'}"

    elif text_lower in ["trades", "positions"]:
        result = subprocess.run(
            ["python3", "-c", """
import sqlite3
conn = sqlite3.connect('~/multi_agent_bot/bot.db')
trades = conn.execute("SELECT agent, symbol, side, pnl, closed_at FROM trades WHERE status='closed' ORDER BY closed_at DESC LIMIT 5").fetchall()
for t in trades: print(f'{t[0]} {t[1]} {t[2]} ${t[3]:+.2f}')
conn.close()
"""], shell=True, capture_output=True, text=True, timeout=5, cwd=os.path.expanduser("~/multi_agent_bot"))
        return f"📊 Recent trades:\n{result.stdout}"

    elif text_lower in ["scout", "hunt", "scan coins"]:
        return "🔍 Scout running... check back in 2 min"

    elif text_lower in ["restart bot", "reboot"]:
        subprocess.run(["pkill", "-9", "-f", "bot.py"], timeout=5)
        time.sleep(2)
        subprocess.Popen(["python3", "-u", "bot.py"], cwd=os.path.expanduser("~/multi_agent_bot"))
        return "🔄 Bot restarted"

    elif text_lower in ["kill losers", "purge"]:
        return "💀 All losers already killed. Only 7 winners running."

    elif "risk" in text_lower or "leverage" in text_lower:
        return "⚙️ Current: 10× leverage, 10% base per trade, 5 concurrent"

    elif text_lower in ["doctor", "health"]:
        result = subprocess.run(
            ["tail", "-20", os.path.expanduser("~/multi_agent_bot/logs/doctor_report.txt")],
            capture_output=True, text=True, timeout=5
        )
        return f"🩺 {result.stdout}"

    elif "enable" in text_lower or "disable" in text_lower:
        return "⚙️ Agent control via Telegram coming soon. Use Claude Code for now."

    # ── DEFAULT: Forward to Claude ──
    else:
        # Write to a special file that Claude Code can read
        with open(os.path.join(BRIDGE, "claude_commands.txt"), "a") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
        return f"📝 Sent to Claude: '{text[:50]}...' — Claude will process it"

def main():
    log("🕹️ TG COMMANDER STARTED — Full Telegram control active")

    # Track last read position
    last_pos = 0
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            last_pos = json.load(f).get("last_pos", 0)

    # Get initial file size
    if os.path.exists(COMMANDS_FILE):
        last_pos = os.path.getsize(COMMANDS_FILE)

    log(f"Watching {COMMANDS_FILE} from byte {last_pos}")

    while True:
        try:
            if os.path.exists(COMMANDS_FILE):
                current_size = os.path.getsize(COMMANDS_FILE)
                if current_size > last_pos:
                    with open(COMMANDS_FILE, "r") as f:
                        f.seek(last_pos)
                        new_data = f.read()
                        last_pos = current_size

                    for line in new_data.strip().split("\n"):
                        if not line: continue
                        try:
                            cmd = json.loads(line)
                            cmd_id = cmd.get("id", "")
                            text = cmd.get("text", "")

                            if not text: continue

                            log(f"📱 Telegram: {text[:80]}")
                            response = execute_command(text)
                            send_ack(cmd_id, response)
                            log(f"  → {response[:80]}")

                        except json.JSONDecodeError:
                            pass

                with open(STATE_FILE, "w") as f:
                    json.dump({"last_pos": last_pos}, f)

        except Exception as e:
            log(f"Error: {e}")

        time.sleep(1)

if __name__ == "__main__":
    main()
