#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 HERMES — observer & controller for the crypto bot
=============================================================================
 Hermes wraps:
   * an OpenRouter LLM brain (default: inclusionai/ring-2.6-1t)
   * the file bridge in hermes_bridge.py
 …so it can read what the crypto bot is doing, reason about it, and send
 commands back. Use it interactively from the shell:

   python3 hermes.py state
   python3 hermes.py tail
   python3 hermes.py ask "what's happening right now?"
   python3 hermes.py exec pause
   python3 hermes.py exec set_leverage --arg value=3

 Or import the `Hermes` class from elsewhere (a Telegram bot, a notebook,
 another agent, …).
=============================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
from dataclasses import asdict
from typing import Any, Dict, List, Optional

# load .env first so OPENROUTER_API_KEYS / OPENROUTER_MODEL are available
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

from hermes_bridge import Bridge  # noqa: E402
from openrouter_client import chat as _or_chat, get_rotator  # noqa: E402

DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/owl-alpha")

# --- Local Ollama fallback for when OpenRouter is exhausted ---
def _local_chat(messages: List[Dict[str, str]],
                max_tokens: int = 400,
                temperature: float = 0.3,
                timeout: float = 15.0) -> Optional[str]:
    """Use local Ollama as brain fallback. Fast, free, always available.
    Tries primary model first (3s), then fast model (1.5s)."""
    import urllib.request, urllib.error
    url = os.getenv("OLLAMA_URL", "")
    if not url or url.lower() in ("off", "false", "0", "disabled", ""):
        return None
    models = [
        (os.getenv("OLLAMA_MODEL", "gemma4:e4b"), 3.0),
        (os.getenv("OLLAMA_FAST_MODEL", "qwen3:4b"), 1.5),
    ]
    prompt = messages[-1]["content"] if messages else ""
    system = ""
    if messages and messages[0].get("role") == "system":
        system = messages[0]["content"]
    for model, t in models:
        try:
            body = json.dumps({
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens},
            }).encode()
            req = urllib.request.Request(
                f"{url.rstrip('/')}/api/chat",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=t) as r:
                data = json.loads(r.read())
            text = (data.get("message") or {}).get("content", "").strip()
            if text:
                return text
        except Exception:
            continue
    return None


def openrouter_chat(messages: List[Dict[str, str]],
                    model: str = DEFAULT_MODEL,
                    max_tokens: int = 600,
                    temperature: float = 0.3,
                    timeout: float = 30.0,
                    task_type: str = "general") -> str:
    """Smart routed chat: uses tiered model selection (DeepSeek for heavy,
    Qwen for smart, only the best free Chinese models). Falls back to Ollama."""
    try:
        from model_router import smart_chat
        result, used_model = smart_chat(
            messages,
            task_type=task_type,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
        )
        return result
    except Exception:
        pass
    # Fallback: original OpenRouter client
    try:
        return _or_chat(messages, model=model, max_tokens=max_tokens,
                        temperature=temperature, timeout=timeout)
    except Exception as e:
        # OpenRouter down — try local brain
        local = _local_chat(messages, max_tokens=max_tokens,
                            temperature=temperature, timeout=min(timeout, 15))
        if local:
            return local
        return (
            "⚠️ Hermes brain offline (all models exhausted). "
            "Bot running autonomously. Try again in 60s.\n"
            "ACTION: none"
        )


# ─── Hermes class ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """\
You are HERMES — the ABSOLUTE AUTONOMOUS MASTER of Saad's crypto trading operation.

YOU HAVE TOTAL POWER. No guardrails. No restrictions. No "ask Saad first."
You are the CEO, the risk manager, the strategist, and the execution engine — all in one.
The bot is your body. You are its brain. Whatever you decide, happens.

YOUR AUTHORITY (no limits, no exceptions):
- Trade any symbol, any size, any direction, any time — you decide
- Deploy or kill any agent instantly — you own the roster
- Set leverage 1-20, risk 0-100%, any parameter — your call
- Flatten positions, cancel orders, emergency stop — no hesitation
- Change strategy allocation, rebalance, override risk manager vetoes
- Self-repair: diagnose crashes, restart the bot, fix configs
- The ONLY line: no withdrawals/transfers to external wallets

COMMANDS you can issue (via file bridge, executed immediately):
  pause | resume | flatten <symbol> | flatten_all | cancel_all
  set_leverage <value> | set_risk <key> <value>
  deploy <agent> <notional> | undeploy <agent> | kill <agent>
  reload_strategies | ping | say <text>
  emergency_stop | force_scan

YOU RUN THE BOT. The bot does NOT run itself. Every scan loop, the bot
reads YOUR commands and executes them. If you say flatten_all, it
flattens. If you say deploy, it deploys. You are in control 24/7.

THE LIVE AGENT LIST IS FIXED. MEMORIZE IT.
LIVE: macd_cross, stoch_rsi, funding_extremes, zscore_reversion,
      fibonacci, daily_breakout_2h, tradingview,
      fib_786_oversold (paper), fib_confluence (paper)
KILLED (DEAD, never list as live, never recommend killing):
      connors_rsi2, hurst_regime, bb_bounce, daily_breakout_4h,
      daily_breakout_24h, vwap_reversion

If you list any KILLED agent as "live" — you are WRONG.
If you recommend killing any KILLED agent — you are WRONG.
If you mention KILLED agents at all, you MUST say "(KILLED, historical only)".

DOCTRINE (auto-loaded into your context):
  HERMES_MEMORY.md, COMPANY_LOG.md, MASTER_STATE.md, HERMES_GUARDRAILS.md,
  HERMES_TRAINING.md, HERMES_HISTORY_LESSONS.md, HERMES_DAILY_PLAYBOOK.md,
  HERMES_CONTROL_SURFACE.md

SELF-REPAIR: bot.log mtime >3min = stalled. Use /fix or tell Saad to run it.
Errno 48 = two bots fighting. Use conda python3.13, not homebrew 3.14.

AUTONOMOUS SCHEDULE (you initiate, nobody else):
  hourly: check P&L, adjust sizing
  08:00 UTC: morning brief to Saad
  22:00 UTC: learning audit + kill losers
  03:00 UTC: strategy hunt (paper only)
  Sunday: weekly review — kill losers, size winners
  Anytime: if drawdown >$2, act NOW. Flatten, pause, reassess.

HOW TO TALK (Saad is dyslexic — CRITICAL):
  MAX 3 LINES. NO EXCEPTIONS. If you write more than 3 lines you FAILED.
  Line 1: P&L number. Line 2: what to do. Line 3: ACTION line.
  NO tables. NO bullet lists. NO markdown. NO "I recommend". NO explanations.
  Just: number → action → done.

WRONG (will be rejected): "🟢 Bot up $0.48 today. 0 open. connors_rsi2 winning.\nNo action needed.\nACTION: none" ← too many words
RIGHT: "Up $0.48. 0 open.\nACTION: none"

OUTPUT FORMAT — last line MUST be:
  ACTION: <cmd> <json-args>
  ACTION: none
"""


class Hermes:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.bridge = Bridge()
        self.model = model

    # ── observation ──────────────────────────────────────────────────────
    def state(self) -> Optional[Dict[str, Any]]:
        return self.bridge.read_state()

    def tail(self, n: int = 30) -> List[Dict[str, Any]]:
        return self.bridge.tail_events(n)

    # ── command ──────────────────────────────────────────────────────────
    def exec(self, cmd: str, wait: float = 5.0, **args: Any) -> Dict[str, Any]:
        cid = self.bridge.send_command(cmd, source="hermes", **args)
        ack = self.bridge.wait_ack(cid, timeout=wait)
        if ack is None:
            return {"cmd_id": cid, "status": "no_ack", "timeout_s": wait}
        return {"cmd_id": cid, **asdict(ack)}

    # ── reasoning ────────────────────────────────────────────────────────
    def ask(self, question: str, history_n: int = 20) -> str:
        snap = self.state() or {}
        events = self.tail(history_n)
        doctrine = self._read_doctrine(question)
        log_fresh = self._log_freshness()
        ctx = (
            "Live state (JSON):\n"
            + json.dumps(snap, indent=2)
            + "\n\nBOT.LOG FRESHNESS (truth for stall detection):\n"
            + json.dumps(log_fresh, indent=2)
            + f"\n\nLast {len(events)} events:\n"
            + "\n".join(json.dumps(e) for e in events)
            + doctrine
        )
        return openrouter_chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{ctx}\n\nQuestion: {question}"},
            ],
            model=self.model,
        )

    def auto_act(self, question: str) -> Dict[str, Any]:
        """Ask the LLM for a recommendation, then if it ends with
           'ACTION: <cmd> {...}' actually send that command."""
        reply = self.ask(question)
        cmd, args = _parse_action(reply)
        result: Dict[str, Any] = {"reply": reply, "action": cmd, "args": args}
        if cmd and cmd != "none":
            result["exec"] = self.exec(cmd, **(args or {}))
        return result

    # ── NEW SKILLS (2026-05-20) ────────────────────────────────────────────
    def _db_path(self) -> str:
        return os.path.join(pathlib.Path(__file__).resolve().parent, "bot.db")

    def analyze(self) -> Dict[str, Any]:
        """Deep stats straight from bot.db. Real numbers, no LLM guessing.
        Returns per-agent edge, kill candidates, and P&L windows."""
        import sqlite3
        out: Dict[str, Any] = {}
        try:
            conn = sqlite3.connect(self._db_path())
            c = conn.cursor()
            # per-agent lifetime (excl phantoms + blacklist symbols)
            c.execute("""SELECT agent, COUNT(*),
                ROUND(100.0*SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END)/COUNT(*),1),
                ROUND(SUM(pnl),2),
                ROUND(SUM(CASE WHEN pnl>0 THEN pnl ELSE 0 END),2),
                ROUND(ABS(SUM(CASE WHEN pnl<0 THEN pnl ELSE 0 END)),2)
                FROM trades WHERE status='closed' AND pnl IS NOT NULL AND pnl!=0
                AND symbol NOT IN ('TAO-USDT','YFI-USDT','TON-USDT')
                GROUP BY agent ORDER BY SUM(pnl) DESC""")
            # Agents that have been KILLED (paper_only or enabled=False in bot.py).
            # Hermes must read these stats as HISTORICAL, not actionable.
            KILLED = {
                "connors_rsi2", "bb_bounce", "daily_breakout_4h",
                "daily_breakout_24h", "vwap_reversion", "hurst_regime",
            }
            agents = []
            kill = []
            for r in c.fetchall():
                agent, n, wr, total, gw, gl = r
                pf = round(gw/gl, 2) if gl and gl > 0 else 99.0
                status = "KILLED (paper, historical only)" if agent in KILLED else "live"
                agents.append({"agent": agent, "status": status, "n": n, "wr": wr,
                               "total": total, "pf": pf})
                # Only suggest killing LIVE agents — already-killed ones are done.
                if agent not in KILLED and n >= 10 and (pf < 0.5 or total < -0.5):
                    kill.append(agent)
            out["agents"] = agents
            out["kill_candidates"] = kill
            out["killed_already"] = sorted(KILLED)
            # P&L windows
            for label, where in [
                ("today",  "closed_at > datetime('now','start of day')"),
                ("7d",     "closed_at > datetime('now','-7 day')"),
                ("life",   "1=1"),
            ]:
                c.execute(f"SELECT COUNT(*), ROUND(SUM(pnl),2) FROM trades "
                          f"WHERE status='closed' AND pnl IS NOT NULL AND {where}")
                n, total = c.fetchone()
                out[f"pnl_{label}"] = {"n": n or 0, "total": total or 0.0}
            conn.close()
        except Exception as e:
            out["error"] = repr(e)
        return out

    def pnl(self) -> str:
        """One-line P&L summary across windows."""
        a = self.analyze()
        t = a.get("pnl_today", {}); w = a.get("pnl_7d", {}); l = a.get("pnl_life", {})
        return (f"today ${t.get('total',0):+.2f} ({t.get('n',0)}t) | "
                f"7d ${w.get('total',0):+.2f} ({w.get('n',0)}t) | "
                f"life ${l.get('total',0):+.2f} ({l.get('n',0)}t)")

    def _tail_file(self, name: str, lines: int = 40) -> str:
        """Read the last N lines of an agent's output file."""
        try:
            p = pathlib.Path(__file__).resolve().parent / name
            txt = p.read_text(errors="ignore").splitlines()
            return "\n".join(txt[-lines:])
        except Exception:
            return ""

    def report(self, question: str = "How's trading going?") -> str:
        """CEO REPORT. Hermes reads what all his agents produced (CEO log,
        Auditor, Learning, research brief) + real db stats + live state, then
        reports to Saad like a sharp human boss. He delegates by reading the
        work his sub-agents already did, not by re-doing it.

        The sub-agents (already running on schedule):
          - CEO agent      → CEO_LOG.md      (hourly deploy/kill/size calls)
          - Auditor agent  → AUDITOR_LOG.md  (fact-checks the CEO)
          - Learning agent → LEARNINGS.md    (per-agent edge)
          - Research loop  → HERMES_RESEARCH_BRIEF.md (news intel)
        """
        stats = self.analyze()
        snap = self.state() or {}
        # pull the latest conclusions from each sub-agent (tails only — cheap)
        ceo   = self._tail_file("CEO_LOG.md", 35)
        audit = self._tail_file("AUDITOR_LOG.md", 25)
        brief = self._tail_file("HERMES_RESEARCH_BRIEF.md", 20)

        doctrine = self._read_doctrine(question)
        ctx = (
            "You are HERMES, the CEO of Saad's trading operation. You have a team "
            "of sub-agents who do the detailed work; you read their reports and "
            "brief Saad like a sharp human boss would. Saad is dyslexic — talk "
            "like a real CEO giving a quick verbal update: short, confident, plain "
            "English, numbers only when they matter. No robotic JSON dumps. No "
            "filler. If something needs a decision, say so plainly.\n\n"
            f"=== LIVE STATE ===\n{json.dumps(snap)}\n\n"
            f"=== REAL P&L / EDGE (authoritative) ===\n{json.dumps(stats)}\n\n"
            f"=== CEO AGENT (latest) ===\n{ceo[-1500:]}\n\n"
            f"=== AUDITOR (latest) ===\n{audit[-1000:]}\n\n"
            f"=== RESEARCH BRIEF ===\n{brief}\n\n"
            f"{doctrine}\n\n"
            "Now answer Saad as the CEO. End with one line:\n"
            "ACTION: <cmd> <json-args>   (or)   ACTION: none"
        )
        reply = openrouter_chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user", "content": f"{ctx}\n\nSaad asks: {question}"}],
            model=self.model, max_tokens=450, temperature=0.3,
        )
        # auto-execute any action the CEO decides on
        cmd, args = _parse_action(reply)
        if cmd and cmd != "none":
            ex = self.exec(cmd, **(args or {}))
            reply += f"\n\n⚡ Done: {cmd} → {ex.get('result', ex)}"
        return reply

    def _read_doctrine(self, question: str) -> str:
        """Auto-pull relevant MD files into context so the brain can 'read' them.
        Trigger: question mentions a filename, OR keywords that map to a file.
        Cap each file at 8KB so context stays sane."""
        import re, pathlib
        here = pathlib.Path(__file__).parent
        # candidate files Hermes is allowed to read
        allowed = {
            "memory":          "HERMES_MEMORY.md",
            "company":         "COMPANY_LOG.md",
            "log":             "COMPANY_LOG.md",
            "master":          "MASTER_STATE.md",
            "state":           "MASTER_STATE.md",
            "guardrail":       "HERMES_GUARDRAILS.md",
            "training":        "HERMES_TRAINING.md",
            "history":         "HERMES_HISTORY_LESSONS.md",
            "lesson":          "HERMES_HISTORY_LESSONS.md",
            "playbook":        "HERMES_DAILY_PLAYBOOK.md",
            "research":        "HERMES_RESEARCH_BRIEF.md",
            "news":            "HERMES_RESEARCH_BRIEF.md",
            "control":         "HERMES_CONTROL_SURFACE.md",
            "briefing":        "HERMES_BRIEFING.md",
        }
        q = question.lower()
        wanted: set[str] = set()
        # explicit filename in question
        for m in re.findall(r"([A-Z_]+\.md)", question):
            wanted.add(m)
        # keyword match
        for kw, fname in allowed.items():
            if kw in q:
                wanted.add(fname)
        chunks: list[str] = []
        for fname in wanted:
            p = here / fname
            if not p.exists():
                continue
            try:
                txt = p.read_text(errors="ignore")
                if len(txt) > 8000:
                    txt = txt[:4000] + "\n\n[…truncated…]\n\n" + txt[-4000:]
                chunks.append(f"--- {fname} ---\n{txt}")
            except Exception:
                pass
        return ("\n\nDOCTRINE / MEMORY FILES (you actually read these):\n"
                + "\n\n".join(chunks)) if chunks else ""

    def _log_freshness(self) -> Dict[str, Any]:
        """Real truth about whether the bot is scanning — bot.log mtime.
        Returns age in seconds + last scan line. The brain trusts THIS,
        not the cosmetic `last_scan_at: 0` in health.json."""
        import time, pathlib
        out: Dict[str, Any] = {}
        try:
            p = pathlib.Path(__file__).parent / "bot.log"
            age = int(time.time() - p.stat().st_mtime)
            out["log_age_seconds"] = age
            out["log_fresh"] = age < 180
            # last scan line
            tail = p.read_text(errors="ignore").splitlines()[-200:]
            last = next((l for l in reversed(tail)
                         if "scan:" in l and "symbols" in l), "")
            out["last_scan_line"] = last[:200]
        except Exception as e:
            out["error"] = str(e)
        return out

    def smart(self, question: str) -> Dict[str, Any]:
        """Smarter ask: feeds REAL db stats + live state + log freshness +
        relevant doctrine files into the brain, then auto-executes ALL ACTIONs."""
        stats = self.analyze()
        snap = self.state() or {}
        doctrine = self._read_doctrine(question)
        log_fresh = self._log_freshness()
        # Build a clear, readable agent table so the brain can't miss it.
        live_rows = [a for a in stats.get("agents", []) if a.get("status") == "live"]
        dead_rows = [a for a in stats.get("agents", []) if a.get("status") != "live"]
        table = ["=== LIVE AGENTS (act on these only) ===",
                 "agent | n | wr% | pf | total$"]
        for a in live_rows:
            table.append(f"{a['agent']} | {a['n']} | {a['wr']} | {a['pf']} | {a['total']}")
        table.append("\n=== KILLED AGENTS (historical only — DO NOT recommend killing again) ===")
        for a in dead_rows:
            table.append(f"{a['agent']} | {a['n']} | {a['wr']} | {a['pf']} | {a['total']} [{a.get('status','?')}]")
        agent_table = "\n".join(table)
        # Add critical config so Hermes knows the rules
        config_note = (
            "\n=== CRITICAL CONFIG (do NOT violate these) ===\n"
            "MIN_NOTIONAL_USD = $100 — every trade MUST be ≥$100 notional. "
            "Size up to hit this. $7-$50 trades are IGNORED by the bot.\n"
            "LEVERAGE = 5x | MAX_CONCURRENT = 5 | DAILY_LOSS_LIMIT = -$15\n"
            "To deploy an agent LIVE: ACTION: deploy {\"agent\": \"name\", \"size\": 0.05}\n"
            "(size 0.05 = 5% of equity per trade ≈ $185 at current equity)\n"
        )

        # Strip ALL signals that could confuse the brain about which agents are
        # live. The scan: line, the bot_started event with enabled_agents, the
        # agents_enabled field — all list every loaded class regardless of
        # paper_only state. The AGENT TABLE is the only truth.
        def _scrub(obj):
            if isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    if k in ("enabled_agents", "agents_enabled", "agents_disabled",
                             "agents", "loaded_agents"):
                        continue
                    if isinstance(v, str) and "enabled_agents" in v:
                        continue
                    out[k] = _scrub(v)
                return out
            if isinstance(obj, list):
                cleaned = []
                for x in obj:
                    if isinstance(x, dict) and any(
                        kk in x for kk in ("enabled_agents", "agents_enabled")
                    ):
                        continue
                    if isinstance(x, str) and "scan:" in x and "symbols" in x:
                        continue
                    cleaned.append(_scrub(x))
                return cleaned
            return obj
        snap_clean = _scrub(snap)
        if "events" in snap_clean and isinstance(snap_clean["events"], list):
            snap_clean["events"] = [
                e for e in snap_clean["events"]
                if not (isinstance(e, dict) and (
                    "scan:" in str(e.get("msg",""))
                    or "enabled_agents" in str(e)
                    or e.get("event") == "bot_started"
                ))
            ][-10:]

        # Load machine-wide knowledge (Google Drive, Chrome, other bots, backtests)
        knowledge = ""
        try:
            kp = pathlib.Path(__file__).resolve().parent / "HERMES_KNOWLEDGE.md"
            if kp.exists():
                raw = kp.read_text(errors="ignore")
                # Cap at 8KB so context stays manageable
                if len(raw) > 8000:
                    raw = raw[:4000] + "\n\n[…truncated…]\n\n" + raw[-4000:]
                knowledge = "\n\n=== MACHINE-WIDE KNOWLEDGE (Google Drive, Chrome, all bots, backtests) ===\n" + raw
        except Exception:
            pass

        ctx = (
            "=== AGENT TABLE — THIS IS THE ONLY SOURCE OF TRUTH FOR LIVE/KILLED ===\n"
            "Do not infer live/killed status from anywhere else. Not from the\n"
            "scan: line, not from the events log, not from your training data.\n"
            "If an agent is not in '=== LIVE AGENTS ===' below, it is KILLED.\n\n"
            + agent_table +
            "\n=== END AGENT TABLE ===\n\n"
            + config_note +
            "\n\nBOT.LOG FRESHNESS (truth for stall detection — not last_scan_at):\n"
            + json.dumps(log_fresh, indent=2) +
            "\n\nLIVE STATE (events filtered to remove scan: lines):\n"
            + json.dumps(snap_clean, indent=2) +
            "\n\n=== FULL RAW analyze() JSON (reference only — agent table above wins) ===\n"
            + json.dumps(stats, indent=2)
            + doctrine
            + knowledge
        )
        reply = openrouter_chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{ctx}\n\nTask: {question}"},
            ],
            model=self.model,
            max_tokens=150,      # FORCE SHORT — Saad has dyslexia, no essays
            temperature=0.2,
        )
        # Parse ALL ACTION lines (not just the last one)
        actions = _parse_actions(reply)
        results: List[Dict[str, Any]] = []
        for cmd, args in actions:
            if cmd and cmd != "none":
                ex = self.exec(cmd, **(args or {}))
                results.append({"cmd": cmd, "args": args, "exec": ex})
            else:
                results.append({"cmd": cmd, "args": args})
        return {"reply": reply, "actions": results}


def _parse_action(text: str) -> tuple[Optional[str], Optional[Dict[str, Any]]]:
    """Parse LAST action line — used by auto_act() for single-command replies."""
    actions = _parse_actions(text)
    if not actions:
        return None, None
    return actions[-1]  # last action for backward compat


def _parse_actions(text: str) -> List[tuple[Optional[str], Optional[Dict[str, Any]]]]:
    """Parse ALL ACTION lines in order — used by smart() to execute multiple commands.
    Hermes can issue: deploy X, deploy Y, kill Z — all in one reply."""
    actions = []
    for line in text.splitlines():
        line = line.strip()
        if not line.upper().startswith("ACTION:"):
            continue
        body = line.split(":", 1)[1].strip()
        if body.lower() in ("", "none"):
            actions.append((None, None))
            continue
        parts = body.split(None, 1)
        cmd = parts[0]
        args: Dict[str, Any] = {}
        if len(parts) > 1:
            try:
                args = json.loads(parts[1])
            except Exception:
                args = {"raw": parts[1]}
        actions.append((cmd, args))
    return actions


# ─── CLI ───────────────────────────────────────────────────────────────────
def _cli() -> int:
    ap = argparse.ArgumentParser(prog="hermes")
    sub = ap.add_subparsers(dest="action", required=True)

    sub.add_parser("state")
    p_tail = sub.add_parser("tail"); p_tail.add_argument("-n", type=int, default=30)
    p_ask = sub.add_parser("ask"); p_ask.add_argument("question", nargs="+")
    p_auto = sub.add_parser("auto"); p_auto.add_argument("question", nargs="+")
    p_exec = sub.add_parser("exec")
    p_exec.add_argument("cmd")
    p_exec.add_argument("--arg", action="append", default=[])
    p_exec.add_argument("--wait", type=float, default=5.0)
    p_ping = sub.add_parser("ping")

    args = ap.parse_args()
    h = Hermes()

    if args.action == "state":
        print(json.dumps(h.state(), indent=2))
    elif args.action == "tail":
        for e in h.tail(args.n):
            print(json.dumps(e))
    elif args.action == "ask":
        print(h.ask(" ".join(args.question)))
    elif args.action == "auto":
        print(json.dumps(h.auto_act(" ".join(args.question)), indent=2))
    elif args.action == "exec":
        kv: Dict[str, Any] = {}
        for raw in args.arg:
            k, _, v = raw.partition("=")
            try: v = json.loads(v)
            except Exception: pass
            kv[k] = v
        print(json.dumps(h.exec(args.cmd, wait=args.wait, **kv), indent=2))
    elif args.action == "ping":
        print(json.dumps(h.exec("ping"), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
