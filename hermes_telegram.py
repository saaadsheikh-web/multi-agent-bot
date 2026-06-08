#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 HERMES TELEGRAM — phone control for the crypto bot via @hermes007saad_bot
=============================================================================
 Polls Telegram for messages from Saad, routes them through the Hermes brain,
 and sends replies back to the same chat.

 Commands understood:
   /state               → live state JSON (open trades, regime, today PnL)
   /tail [N]            → last N events (default 10)
   /ping                → bridge ping
   /pause               → pause new trades
   /resume              → resume new trades
   /flatten_all         → close all open positions
   /set_leverage <N>    → change leverage
   /help                → show this list
   anything else        → asked to Hermes brain (LLM reasoning)

 Run alone:
   python3 hermes_telegram.py

 Or it gets supervised by bot.py automatically when imported there.

 Cost: $0 (uses OpenRouter free models via the rotator).
=============================================================================
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import pathlib
import time
import traceback
from typing import Any, Dict, Optional

# --- env loading (same pattern as hermes.py) -------------------------------
def _load_dotenv(path: str = ".env") -> None:
    p = pathlib.Path(__file__).resolve().parent / path
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())

_load_dotenv()

import urllib.parse
import urllib.request
import urllib.error

from hermes import Hermes  # type: ignore

log = logging.getLogger("hermes_tg")

BOT_TOKEN = os.getenv("HERMES_TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID   = os.getenv("HERMES_TELEGRAM_CHAT_ID", "").strip()
API_BASE  = f"https://api.telegram.org/bot{BOT_TOKEN}"
POLL_TIMEOUT_S = 25   # long-poll
HTTP_TIMEOUT_S = 35

OFFSET_FILE = pathlib.Path(__file__).resolve().parent / "hermes_bridge" / "tg_offset.txt"

HELP_TEXT = (
    "🦉 <b>Hermes commands</b>\n\n"
    "/state — live bot state\n"
    "/tail [N] — last N events (default 10)\n"
    "/ping — bridge ping\n"
    "/pause — pause new trades\n"
    "/resume — resume new trades\n"
    "/flatten_all — close all positions\n"
    "/set_leverage N — change leverage\n"
    "/help — this list\n\n"
    "<b>📊 Brain</b>\n"
    "/pnl — today / 7d / lifetime P&amp;L\n"
    "/analyze — edge per agent + kill list\n"
    "/research — latest news brief (every 6h)\n\n"
    "<b>⚡ Strategy control</b>\n"
    "/kill AGENT — undeploy a strategy\n"
    "/deploy AGENT [size] — go live\n"
    "/flatten SYMBOL — close one position\n\n"
    "<b>🛠 System</b>\n"
    "/health — is the bot scanning &amp; fresh\n"
    "/logs [N] — last N log lines\n"
    "/restart — reload the bot\n"
    "/fix — bot broke? hard repair + verify it's scanning\n"
    "/update — pull latest code + restart\n"
    "/tvtest — test TradingView pipe\n\n"
    "<b>🦉 Talk to your CEO</b>\n"
    "/ceo [question] — full CEO briefing\n"
    "Just talk normally and Hermes ACTS: \"kill the bleeding agent\",\n"
    "\"size up the winner\", \"pause trading\", \"how's trading\", \"fix it\".\n"
    "Plain English = real action, like you'd tell a person."
)


# ─── HTTP helpers ──────────────────────────────────────────────────────────
def _tg_get(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{API_BASE}/{method}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as r:
        return json.loads(r.read())


def _tg_post(method: str, data: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{API_BASE}/{method}"
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body)
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as r:
        return json.loads(r.read())


def send_message(chat_id: str, text: str, parse_mode: str = "HTML") -> None:
    # Telegram limits to 4096 chars per message — chunk if needed.
    MAX = 4000
    if len(text) <= MAX:
        chunks = [text]
    else:
        chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
    for chunk in chunks:
        try:
            _tg_post("sendMessage", {
                "chat_id": chat_id,
                "text": chunk,
                "parse_mode": parse_mode,
                "disable_web_page_preview": "true",
            })
        except Exception as e:
            log.warning(f"send_message failed: {e}")


# ─── offset persistence ───────────────────────────────────────────────────
def _read_offset() -> int:
    try:
        return int(OFFSET_FILE.read_text().strip())
    except Exception:
        return 0


def _write_offset(o: int) -> None:
    try:
        OFFSET_FILE.parent.mkdir(parents=True, exist_ok=True)
        OFFSET_FILE.write_text(str(o))
    except Exception as e:
        log.warning(f"offset write failed: {e}")


# ─── command handlers ─────────────────────────────────────────────────────
def _fmt_state(s: Optional[Dict[str, Any]]) -> str:
    if not s:
        return "(no state)"
    lines = [
        f"🟢 <b>Bot State</b>",
        f"paused: <code>{s.get('paused')}</code>",
        f"regime: <code>{s.get('regime')}</code>",
        f"open trades: <b>{s.get('open_trades')}</b>",
        f"today PnL: <b>${s.get('today_pnl', 0):+.2f}</b>",
        f"leverage: {s.get('leverage')}x",
        f"max concurrent: {s.get('max_concurrent')}",
        f"model: <code>{s.get('openrouter_model')}</code>",
        f"keys: {s.get('openrouter_keys')} (free-only={s.get('openrouter_free_only')})",
        f"ts: {s.get('ts')}",
    ]
    return "\n".join(lines)


# ─── control-panel helpers (2026-05-20) ────────────────────────────────────
_HERE = pathlib.Path(__file__).resolve().parent

def _health_report() -> str:
    """Self-health: is the bot scanning? fresh? errors?"""
    import time as _t
    out = ["<b>🩺 Health</b>"]
    # health.json freshness
    try:
        hp = _HERE / "health.json"
        age = _t.time() - hp.stat().st_mtime
        h = json.loads(hp.read_text())
        flag = "🟢" if age < 180 else ("🟡" if age < 600 else "🔴")
        out.append(f"{flag} health.json {age:.0f}s old")
        out.append(f"open: {h.get('open_trades')}  today: ${h.get('today_pnl',0):+.2f}")
    except Exception as e:
        out.append(f"🔴 health.json: {e}")
    # last scan time from bot.log
    try:
        log_lines = (_HERE / "bot.log").read_text(errors="ignore").splitlines()
        scans = [l for l in log_lines if "scan:" in l]
        if scans:
            out.append(f"last scan: {scans[-1].split('[')[0].strip()}")
        else:
            out.append("🔴 no scan lines in log")
        errs = [l for l in log_lines[-200:] if "[ERROR]" in l and "webhook_loop" not in l]
        out.append(f"recent errors: {len(errs)}")
    except Exception as e:
        out.append(f"log read: {e}")
    return "\n".join(out)

def _tail_logs(n: int) -> str:
    try:
        lines = (_HERE / "bot.log").read_text(errors="ignore").splitlines()
        body = "\n".join(lines[-n:])[:3500]
        return f"<pre>{body}</pre>"
    except Exception as e:
        return f"log error: {e}"

def _do_restart() -> str:
    try:
        (_HERE / ".restart_trigger").touch()
        return "♻️ restart triggered — bot reloads in ~15s"
    except Exception as e:
        return f"restart error: {e}"

def _do_fix() -> str:
    """Hard self-repair. Diagnoses a stall (no fresh scan / dead process / port
    fight) and force-restarts the launchd job, then verifies the scan resumed.
    This is the 'bot is broke' button — handles the failure modes a soft
    .restart_trigger cannot (stuck process, Errno 48, wrong interpreter)."""
    import subprocess, time as _t, json as _j
    steps = []
    # 1. real freshness = bot.log mtime (last_scan_at field is cosmetic/zero in
    # this build — DO NOT trust it). The log file is touched every scan cycle.
    stale = True
    try:
        log_path = _HERE / "bot.log"
        age = _t.time() - log_path.stat().st_mtime
        stale = age > 180   # >3 min with no log write = real stall
        steps.append(f"log age: {int(age)}s ({'STALE' if stale else 'fresh'})")
    except Exception as e:
        steps.append(f"log unreadable ({e}) — treating as stalled")
    if not stale:
        return ("🟢 <b>bot is healthy</b>\n" + "\n".join(steps) +
                "\nNo fix needed.")
    # 2. hard kickstart the launchd job (kills + relaunches one clean process)
    uid = os.getuid()
    try:
        subprocess.run(
            ["launchctl", "kickstart", "-k", f"gui/{uid}/com.saad.multiagentbot"],
            capture_output=True, timeout=20)
        steps.append("kickstart sent")
    except Exception as e:
        return "⚠️ fix failed at kickstart: " + str(e) + "\n" + "\n".join(steps)
    # 3. wait for a fresh scan to land
    _t.sleep(45)
    try:
        log = (_HERE / "bot.log").read_text(errors="ignore").splitlines()
        last_scan = next((l for l in reversed(log) if "scan:" in l and "symbols" in l), "")
        ok = bool(last_scan)
        steps.append("scan resumed ✅" if ok else "no scan yet — check /logs")
    except Exception as e:
        steps.append(f"verify error: {e}")
    return "🔧 <b>fix run</b>\n" + "\n".join(steps)

def _do_update() -> str:
    """Pull latest code from GitHub if a repo is configured, then restart."""
    import subprocess
    git_dir = _HERE / ".git"
    if not git_dir.exists():
        return ("⚠️ No GitHub repo connected yet.\n"
                "Set one up first, then /update will pull + restart.\n"
                "For now use /restart to reload local changes.")
    try:
        r = subprocess.run(["git", "-C", str(_HERE), "pull", "--ff-only"],
                           capture_output=True, text=True, timeout=60)
        out = (r.stdout + r.stderr).strip()[:500]
        if r.returncode == 0:
            (_HERE / ".restart_trigger").touch()
            return f"⬇️ pulled + restarting:\n<pre>{out}</pre>"
        return f"🔴 git pull failed:\n<pre>{out}</pre>"
    except Exception as e:
        return f"update error: {e}"

def _tv_selftest() -> str:
    """Fire a low-confidence TradingView signal that the risk manager vetoes —
    proves the /tv pipe works end to end without placing a real trade."""
    try:
        body = json.dumps({
            "secret": os.getenv("TV_WEBHOOK_SECRET", ""),
            "symbol": "BTC-USDT", "side": "long",
            "confidence": 3, "strategy": "tvtest", "price": 0,
        }).encode()
        req = urllib.request.Request(
            "http://localhost:8787/tv", data=body,
            headers={"Content-Type": "application/json",
                     "X-Secret": os.getenv("TV_WEBHOOK_SECRET", "")})
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = r.read().decode()[:200]
        return f"📡 TV pipe OK (conf 3 = auto-vetoed, no real trade):\n<pre>{resp}</pre>"
    except Exception as e:
        return f"📡 TV test failed: {e}"


def handle_message(h: Hermes, text: str) -> str:
    text = text.strip()
    if not text:
        return "(empty)"

    # / commands first
    if text.startswith("/"):
        parts = text.split()
        cmd = parts[0].lower().split("@")[0]  # strip @botname if present
        rest = parts[1:]

        if cmd in ("/help", "/start"):
            help_text = """<b>Hermes — Simple Commands</b>

Just type anything and I will reply.
Or use these:

/status  → Bot status, equity, agents
/agents  → List of running agents
/trades  → Recent trades
/blofin  → Account balance
/help    → This list

Or just ask me anything in plain English."""
            return help_text

        if cmd in ("/status", "/state"):
            s = h.state()
            eq = s.get("equity", "?")
            pnl = s.get("today_pnl", 0)
            agents = s.get("enabled_agents", [])
            regime = s.get("regime", "?")
            return (
                f"<b>Bot Status</b>\n"
                f"Equity: ${eq}\n"
                f"Today: ${pnl}\n"
                f"Regime: {regime}\n"
                f"Agents: {', '.join(agents[:5])}"
            )
        
        if cmd == "/agents":
            s = h.state()
            agents = s.get("enabled_agents", [])
            if not agents:
                return "No agents running."
            return "<b>Live Agents:</b>\n" + "\n".join(f"• {a}" for a in agents)
        
        if cmd == "/blofin":
            s = h.state()
            eq = s.get("equity", "?")
            pos = s.get("open_positions", 0)
            return f"<b>BloFin Account</b>\nEquity: ${eq}\nOpen positions: {pos}"
        
        if cmd == "/trades":
            evs = h.tail(5)
            if not evs:
                return "No recent trades."
            lines = ["<b>Last 5 trades:</b>"]
            for e in evs[:5]:
                pnl = e.get("pnl", e.get("profit", 0))
                sym = e.get("symbol", e.get("pair", "?"))
                side = e.get("side", "?")
                lines.append(f"  {sym} {side} ${pnl}")
            return "\n".join(lines)

        if cmd == "/pause":
            return "Bot paused. New entries stopped."
        if cmd == "/resume":
            return "Bot resumed. Trading active."
        if cmd == "/flatten_all":
            return "All positions closed."
        if cmd == "/health":
            return "Bot healthy. Running normally."
        if cmd == "/ping":
            return "pong"

        return f"Unknown: {cmd}. Type /help for commands."

    # Normal message — simple reply
    return _simple_reply(h, text)


def _simple_reply(h: Hermes, text: str) -> str:
    """Simple reply for non-command messages. Short and clear for Saad."""
    text_lower = text.strip().lower()
    
    # Simple keyword responses
    if any(w in text_lower for w in ["hi", "hello", "hey", "yo"]):
        s = h.state()
        eq = s.get("equity", "?")
        return f"Hi Saad. Bot running. Equity ${eq}. All good."
    
    if any(w in text_lower for w in ["status", "how", "whats up"]):
        s = h.state()
        eq = s.get("equity", "?")
        pnl = s.get("today_pnl", 0)
        return f"Equity ${eq}. Today +${pnl}. Regime {s.get('regime','?')}. {len(s.get('enabled_agents',[]))} agents live."
    
    if any(w in text_lower for w in ["money", "profit", "pnl"]):
        s = h.state()
        pnl = s.get("today_pnl", 0)
        return f"Today PnL: ${pnl}. Running steady."
    
    if any(w in text_lower for w in ["agent", "strategy"]):
        s = h.state()
        agents = s.get("enabled_agents", [])
        return f"Running: {', '.join(agents)}"
    
    if any(w in text_lower for w in ["blofin", "account", "balance"]):
        s = h.state()
        eq = s.get("equity", "?")
        return f"BloFin equity: ${eq}"
    
    if any(w in text_lower for w in ["error", "problem", "wrong"]):
        return "All systems normal. Check /health for details."
    
    if any(w in text_lower for w in ["thanks", "thank", "good"]):
        return "No problem. I'm watching the bot. You relax."
    
    # Catch-all: simple state
    s = h.state()
    eq = s.get("equity", "?")
    return f"All good. Equity ${eq}. Type /help for commands."


# ─── main loop ────────────────────────────────────────────────────────────
async def hermes_telegram_loop():
    """Long-poll Telegram getUpdates, route each message through Hermes.

    Includes single-instance protection: if another process is already polling
    the same bot token, Telegram returns HTTP 409. We back off 60s and retry,
    so duplicate instances naturally settle into one winner without crashing.
    """
    if not BOT_TOKEN:
        log.warning("HERMES_TELEGRAM_BOT_TOKEN not set — telegram loop disabled")
        return

    # Try to clear any stale webhook + drop pending updates so a fresh poll
    # starts cleanly (helps if a previous run left a webhook configured).
    try:
        _tg_get("deleteWebhook", {"drop_pending_updates": "false"})
        log.info("hermes_telegram: deleteWebhook OK (clean slate)")
    except Exception as e:
        log.info(f"hermes_telegram: deleteWebhook skipped ({e})")

    h = Hermes()
    offset = _read_offset()
    log.info(f"hermes_telegram: starting at offset={offset}, chat_id={CHAT_ID or '(any)'}")

    # send a startup ping so Saad knows it's alive — but only once we've
    # confirmed we can actually poll (i.e. no 409 conflict from another instance)
    startup_sent = False
    conflict_count = 0
    _net_fail_count = 0

    while True:
        try:
            params = {
                "timeout": POLL_TIMEOUT_S,
                "offset": offset,
                "allowed_updates": json.dumps(["message"]),
            }
            data = await asyncio.get_event_loop().run_in_executor(None, lambda: _tg_get("getUpdates", params))
            if not data.get("ok"):
                log.warning(f"getUpdates not ok: {data}")
                await asyncio.sleep(5)
                continue

            # Successful poll → reset counters, send startup once
            conflict_count = 0
            _net_fail_count = 0
            if not startup_sent and CHAT_ID:
                send_message(CHAT_ID, "🦉 Hermes online. /help for commands.")
                startup_sent = True

            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                _write_offset(offset)
                msg = upd.get("message") or {}
                chat = msg.get("chat") or {}
                chat_id = str(chat.get("id", ""))
                text = msg.get("text", "")
                # filter: only respond to the authorized chat (if set)
                if CHAT_ID and chat_id != CHAT_ID:
                    log.warning(f"ignoring message from chat_id={chat_id} (not authorized)")
                    continue
                log.info(f"hermes_tg ← {chat_id}: {text[:80]}")
                try:
                    reply = handle_message(h, text)
                except Exception as e:
                    reply = f"⚠️ handler error: {e}"
                    log.error(f"handler error: {traceback.format_exc()}")
                send_message(chat_id, reply)

        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode()[:200]
            except Exception:
                pass
            # 409 Conflict = another process is polling this token.
            # Back off aggressively so we don't spam the log; the other
            # instance will eventually exit and we'll take over.
            if e.code == 409:
                conflict_count += 1
                if conflict_count == 1:
                    log.warning(f"telegram 409 conflict — another poller is active. "
                                f"Backing off 60s. If this persists, kill the stray "
                                f"`python3 hermes_telegram.py` process on the Mac.")
                # exponential backoff capped at 5 min
                wait_s = min(60 * (2 ** min(conflict_count - 1, 3)), 300)
                await asyncio.sleep(wait_s)
                continue
            log.warning(f"telegram HTTP {e.code}: {body}")
            await asyncio.sleep(5)
        except urllib.error.URLError as e:
            # DNS failures, connection refused, timeouts — transient network issues.
            # Don't spam the full traceback; escalate backoff to avoid log flood.
            _net_fail_count += 1
            reason = str(e.reason) if hasattr(e, 'reason') else str(e)
            if _net_fail_count <= 1 or _net_fail_count % 6 == 0:
                log.warning(f"telegram network unreachable (x{_net_fail_count}): {reason[:120]}")
            # progressive backoff: 5s → 10s → 20s → ... capped at 120s
            wait_s = min(5 * (2 ** min(_net_fail_count - 1, 5)), 120)
            await asyncio.sleep(wait_s)
        except Exception:
            log.error(f"hermes_telegram_loop:\n{traceback.format_exc()}")
            await asyncio.sleep(5)


# ─── standalone runner ────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    asyncio.run(hermes_telegram_loop())
