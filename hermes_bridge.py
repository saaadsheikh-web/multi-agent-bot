#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 HERMES ↔ CRYPTO BOT BRIDGE
=============================================================================
 A tiny file-based + Telegram-fallback bus that lets a "Hermes" controller
 process observe and command this crypto bot.

 Layout (under HERMES_BRIDGE_DIR, default ./hermes_bridge):
   ├── state.json        ← crypto bot writes its live snapshot here (every loop)
   ├── events.jsonl      ← append-only stream of trades / fills / signals / errors
   ├── commands.jsonl    ← Hermes appends commands; bot drains them each loop
   ├── ack.jsonl         ← bot writes ack/result for every command it consumed
   └── lock              ← advisory file-lock to keep readers/writers honest

 Commands Hermes can issue (one JSON per line in commands.jsonl):
   {"cmd":"pause"}                                  – stop opening new positions
   {"cmd":"resume"}
   {"cmd":"flatten","symbol":"BTC-USDT"}            – close one position
   {"cmd":"flatten_all"}                            – emergency exit (close all)
   {"cmd":"cancel_all"}                             – cancel all pending orders
   {"cmd":"emergency_stop"}                         – flatten + pause + alert
   {"cmd":"force_scan"}                             – trigger immediate scan cycle
   {"cmd":"set_leverage","value":3}
   {"cmd":"set_risk","key":"DAILY_LOSS_USD","value":50}
   {"cmd":"reload_strategies"}
   {"cmd":"shell","line":"ls -la"}                  – sandboxed, opt-in only
   {"cmd":"say","text":"hello from hermes"}         – just logs / echoes back

 Both sides MUST go through this module — never poke the files directly.
 That keeps the protocol versioned and atomic.
=============================================================================
"""

from __future__ import annotations

import json
import os
import time
import uuid
import fcntl
import pathlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

PROTOCOL_VERSION = 1
DEFAULT_DIR = os.getenv(
    "HERMES_BRIDGE_DIR",
    str(pathlib.Path(__file__).resolve().parent / "hermes_bridge"),
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ensure_dir(path: str) -> pathlib.Path:
    p = pathlib.Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


class _FileLock:
    """Tiny POSIX flock context manager; safe across processes on macOS/Linux."""

    def __init__(self, path: pathlib.Path):
        self.path = path
        self._fh = None

    def __enter__(self):
        self._fh = open(self.path, "a+")
        fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
        finally:
            self._fh.close()
            self._fh = None


@dataclass
class Command:
    cmd: str
    args: Dict[str, Any]
    id: str
    ts: str
    source: str = "hermes"

    @classmethod
    def new(cls, cmd: str, source: str = "hermes", **args: Any) -> "Command":
        return cls(cmd=cmd, args=args, id=str(uuid.uuid4()), ts=_now_iso(), source=source)


@dataclass
class Ack:
    cmd_id: str
    ok: bool
    result: Any
    ts: str


class Bridge:
    """One Bridge instance per process — used by both the crypto bot and Hermes."""

    def __init__(self, dir_: str = DEFAULT_DIR):
        self.root = _ensure_dir(dir_)
        self.state_path = self.root / "state.json"
        self.events_path = self.root / "events.jsonl"
        self.commands_path = self.root / "commands.jsonl"
        self.ack_path = self.root / "ack.jsonl"
        self.lock_path = self.root / "lock"
        self._cursor_path = self.root / ".cursor_commands"
        self._ack_cursor_path = self.root / ".cursor_ack"

    # ─── crypto bot side ─────────────────────────────────────────────────
    def write_state(self, snapshot: Dict[str, Any]) -> None:
        """Atomic write of the live state snapshot."""
        snapshot = {"v": PROTOCOL_VERSION, "ts": _now_iso(), **snapshot}
        tmp = self.state_path.with_suffix(".tmp")
        with _FileLock(self.lock_path):
            tmp.write_text(json.dumps(snapshot, default=str))
            tmp.replace(self.state_path)

    def emit_event(self, kind: str, **payload: Any) -> None:
        line = json.dumps({"v": PROTOCOL_VERSION, "ts": _now_iso(),
                           "kind": kind, **payload}, default=str)
        with _FileLock(self.lock_path):
            with self.events_path.open("a") as f:
                f.write(line + "\n")

    def drain_commands(self) -> List[Command]:
        """Crypto bot calls this each loop. Returns NEW commands since last drain."""
        if not self.commands_path.exists():
            return []
        cursor = self._read_cursor(self._cursor_path)
        out: List[Command] = []
        with _FileLock(self.lock_path):
            with self.commands_path.open("r") as f:
                lines = f.readlines()
        new_lines = lines[cursor:]
        for raw in new_lines:
            raw = raw.strip()
            if not raw:
                continue
            try:
                d = json.loads(raw)
                out.append(Command(
                    cmd=d["cmd"],
                    args=d.get("args", {}),
                    id=d.get("id", str(uuid.uuid4())),
                    ts=d.get("ts", _now_iso()),
                    source=d.get("source", "hermes"),
                ))
            except Exception as e:
                self.emit_event("bridge_parse_error", error=str(e), raw=raw)
        self._write_cursor(self._cursor_path, len(lines))
        return out

    def ack(self, cmd_id: str, ok: bool, result: Any = None) -> None:
        line = json.dumps(asdict(Ack(cmd_id=cmd_id, ok=ok, result=result, ts=_now_iso())),
                          default=str)
        with _FileLock(self.lock_path):
            with self.ack_path.open("a") as f:
                f.write(line + "\n")

    # ─── hermes side ─────────────────────────────────────────────────────
    def read_state(self) -> Optional[Dict[str, Any]]:
        if not self.state_path.exists():
            return None
        try:
            return json.loads(self.state_path.read_text())
        except Exception:
            return None

    def tail_events(self, n: int = 50) -> List[Dict[str, Any]]:
        if not self.events_path.exists():
            return []
        with _FileLock(self.lock_path):
            lines = self.events_path.read_text().splitlines()[-n:]
        out = []
        for raw in lines:
            try:
                out.append(json.loads(raw))
            except Exception:
                pass
        return out

    def send_command(self, cmd: str, source: str = "hermes", **args: Any) -> str:
        """Append a command. Returns the command id Hermes can poll on."""
        c = Command.new(cmd=cmd, source=source, **args)
        line = json.dumps({"id": c.id, "ts": c.ts, "cmd": c.cmd,
                           "args": c.args, "source": c.source})
        with _FileLock(self.lock_path):
            with self.commands_path.open("a") as f:
                f.write(line + "\n")
        return c.id

    def wait_ack(self, cmd_id: str, timeout: float = 5.0,
                 poll: float = 0.2) -> Optional[Ack]:
        deadline = time.time() + timeout
        while time.time() < deadline:
            for a in self.tail_acks(200):
                if a.cmd_id == cmd_id:
                    return a
            time.sleep(poll)
        return None

    def tail_acks(self, n: int = 50) -> List[Ack]:
        if not self.ack_path.exists():
            return []
        with _FileLock(self.lock_path):
            lines = self.ack_path.read_text().splitlines()[-n:]
        out: List[Ack] = []
        for raw in lines:
            try:
                d = json.loads(raw)
                out.append(Ack(cmd_id=d["cmd_id"], ok=d["ok"],
                               result=d.get("result"), ts=d["ts"]))
            except Exception:
                pass
        return out

    # ─── internals ───────────────────────────────────────────────────────
    @staticmethod
    def _read_cursor(p: pathlib.Path) -> int:
        if not p.exists():
            return 0
        try:
            return int(p.read_text().strip() or "0")
        except Exception:
            return 0

    @staticmethod
    def _write_cursor(p: pathlib.Path, n: int) -> None:
        p.write_text(str(n))


# ─── default registry of safe command handlers for the crypto bot ──────────
#
# The bot's main loop should call:
#     bridge = Bridge()
#     for cmd in bridge.drain_commands():
#         ok, result = handle_command(cmd, ctx=trading_ctx)
#         bridge.ack(cmd.id, ok=ok, result=result)
#
# `ctx` is whatever object the bot uses to expose pause/leverage/etc. Provide
# the matching attributes/methods on it (see CryptoBotContext below for the
# expected protocol — duck-typed, so you can adapt).

class CryptoBotContext:
    """Duck-typed interface the bot must satisfy for the default handlers."""

    paused: bool

    def flatten(self, symbol: str) -> Any: ...
    def flatten_all(self) -> Any: ...
    def set_leverage(self, value: int) -> Any: ...
    def set_risk(self, key: str, value: Any) -> Any: ...
    def reload_strategies(self) -> Any: ...


def handle_command(cmd: Command, ctx: Any) -> tuple[bool, Any]:
    """Apply a Hermes command to the bot context. Returns (ok, result)."""
    try:
        c = cmd.cmd
        a = cmd.args or {}
        if c == "pause":
            ctx.paused = True
            return True, "paused"
        if c == "resume":
            ctx.paused = False
            return True, "resumed"
        if c == "flatten":
            return True, ctx.flatten(a["symbol"])
        if c == "flatten_all":
            return True, ctx.flatten_all()
        if c == "cancel_all":
            return True, ctx.cancel_all()
        if c == "emergency_stop":
            ctx.paused = True
            result = ctx.flatten_all()
            return True, f"emergency_stop: paused + flattened ({result})"
        if c == "force_scan":
            ctx.force_scan = True
            return True, "force_scan triggered"
        if c == "set_leverage":
            return True, ctx.set_leverage(int(a["value"]))
        if c == "set_risk":
            return True, ctx.set_risk(a["key"], a["value"])
        if c == "reload_strategies":
            return True, ctx.reload_strategies()
        if c == "say":
            return True, a.get("text", "")
        if c == "ping":
            return True, "pong"
        if c in ("undeploy", "kill", "deploy"):
            agent_name = a.get("agent")
            if not agent_name:
                return False, "missing_arg:agent"
            # Find every Agent subclass with .name == agent_name and flip its
            # class-level `paper_only` flag. Live trades will stop on next scan;
            # already-open positions remain managed until they close naturally.
            try:
                import sys as _sys
                bot_mod = _sys.modules.get("__main__") or _sys.modules.get("bot")
                if bot_mod is None:
                    return False, "bot_module_not_found"
                AgentBase = getattr(bot_mod, "Agent", None)
                if AgentBase is None:
                    return False, "Agent_class_not_found"
                want_paper = (c in ("undeploy", "kill"))
                hit = []
                stack = [AgentBase]
                seen = set()
                while stack:
                    cls = stack.pop()
                    if cls in seen:
                        continue
                    seen.add(cls)
                    for sub in cls.__subclasses__():
                        stack.append(sub)
                        if getattr(sub, "name", None) == agent_name:
                            sub.paper_only = want_paper
                            hit.append(sub.__name__)
                if not hit:
                    return False, f"agent_not_found:{agent_name}"
                state = "paper" if want_paper else "live"
                return True, f"{agent_name} → {state} (classes: {','.join(hit)})"
            except Exception as e:
                return False, f"error:{e!r}"
        return False, f"unknown_command:{c}"
    except KeyError as e:
        return False, f"missing_arg:{e}"
    except Exception as e:
        return False, f"error:{e!r}"


# ─── tiny CLI so Hermes (or you, by hand) can poke the bridge ──────────────
if __name__ == "__main__":
    import argparse, pprint, sys
    ap = argparse.ArgumentParser(prog="hermes_bridge")
    sub = ap.add_subparsers(dest="action", required=True)

    sub.add_parser("state", help="print latest crypto bot state")
    p_tail = sub.add_parser("tail", help="tail recent events")
    p_tail.add_argument("-n", type=int, default=20)

    p_send = sub.add_parser("send", help="send a command")
    p_send.add_argument("cmd")
    p_send.add_argument("--arg", action="append", default=[],
                        help="key=value (repeatable)")
    p_send.add_argument("--wait", type=float, default=5.0)

    sub.add_parser("acks", help="show recent acks")

    args = ap.parse_args()
    b = Bridge()

    if args.action == "state":
        pprint.pp(b.read_state())
    elif args.action == "tail":
        for ev in b.tail_events(args.n):
            print(json.dumps(ev))
    elif args.action == "send":
        kv = {}
        for raw in args.arg:
            k, _, v = raw.partition("=")
            try:
                v = json.loads(v)
            except Exception:
                pass
            kv[k] = v
        cid = b.send_command(args.cmd, **kv)
        print(f"sent id={cid}")
        if args.wait > 0:
            a = b.wait_ack(cid, timeout=args.wait)
            if a is None:
                print("(no ack yet — bot may be offline)")
                sys.exit(2)
            pprint.pp(asdict(a))
    elif args.action == "acks":
        for a in b.tail_acks(50):
            print(json.dumps(asdict(a)))
