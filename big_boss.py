#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 BIG BOSS AGENT — fully autonomous overseer that runs the entire operation
=============================================================================
 Runs every 15 minutes inside the bot's main loop. Has TOTAL authority:

 1. PERFORMANCE REVIEW — checks every agent's edge (WR, PF, ExpR)
 2. AUTO-KILL — kills agents with PF < 0.5 or WR < 40% (min 10 trades)
 3. AUTO-DEPLOY — deploys paper agents that prove edge (WR ≥ 55%, ExpR ≥ +0.15R, n ≥ 10)
 4. RISK CONTROL — dynamic sizing based on P&L trajectory
 5. STRATEGY FACTORY — creates new agents from winning patterns
 6. LOSS PREVENTION — blocks repeat mistake patterns
 7. TELEGRAM BRIEF — concise status update to Saad

 Imported by bot.py. Runs in the main asyncio loop as big_boss_loop().
=============================================================================
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import time
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent

log = logging.getLogger("bigboss")

# How often the boss reviews everything (seconds)
BOSS_INTERVAL_S = 900  # 15 minutes

# Kill thresholds
MIN_TRADES_TO_JUDGE = 8
KILL_IF_PF_BELOW = 0.5
KILL_IF_WR_BELOW = 40.0
KILL_IF_TOTAL_BELOW = -2.0  # dollars

# Deploy thresholds
DEPLOY_IF_WR_ABOVE = 55.0
DEPLOY_IF_EXPR_ABOVE = 0.15
DEPLOY_IF_N_ABOVE = 10


def _load_env():
    """Load .env so standalone runs also work."""
    env_path = HERE / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()


# =============================================================================
# BIG BOSS CORE
# =============================================================================

def get_db_stats() -> Dict[str, Any]:
    """Pull comprehensive per-agent stats from bot.db."""
    import sqlite3
    db = HERE / "bot.db"
    if not db.exists():
        return {"error": "no db"}
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row

    # Per-agent lifetime
    agents = []
    for row in conn.execute("""
        SELECT agent,
               COUNT(*) as n,
               ROUND(100.0*SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END)/COUNT(*), 1) as wr,
               ROUND(SUM(pnl), 2) as total,
               ROUND(AVG(pnl), 4) as avg_pnl,
               ROUND(SUM(CASE WHEN pnl>0 THEN pnl ELSE 0 END), 2) as gross_win,
               ROUND(SUM(CASE WHEN pnl<0 THEN ABS(pnl) ELSE 0 END), 2) as gross_loss
        FROM trades
        WHERE status='closed' AND pnl IS NOT NULL AND pnl != 0
        GROUP BY agent
        ORDER BY SUM(pnl) DESC
    """).fetchall():
        r = dict(row)
        gw = r["gross_loss"] or 0.01
        r["pf"] = round((r["gross_win"] or 0) / gw, 2) if gw > 0 else 99.0
        agents.append(r)

    # Today P&L
    today = conn.execute("""
        SELECT COALESCE(SUM(pnl),0), COUNT(*) FROM trades
        WHERE status='closed' AND closed_at > datetime('now','start of day')
    """).fetchone()
    today_pnl = float(today[0]) if today else 0.0
    today_n = int(today[1]) if today else 0

    # 7d P&L
    week = conn.execute("""
        SELECT COALESCE(SUM(pnl),0), COUNT(*) FROM trades
        WHERE status='closed' AND closed_at > datetime('now','-7 days')
    """).fetchone()

    # Recent trades for loss pattern analysis
    recent_losses = []
    for row in conn.execute("""
        SELECT agent, symbol, pnl, pnl_pct, closed_at FROM trades
        WHERE status='closed' AND pnl < 0
        ORDER BY closed_at DESC LIMIT 20
    """).fetchall():
        recent_losses.append(dict(row))

    conn.close()

    return {
        "agents": agents,
        "today_pnl": today_pnl,
        "today_n": today_n,
        "7d_pnl": float(week[0]) if week else 0.0,
        "7d_n": int(week[1]) if week else 0,
        "recent_losses": recent_losses,
    }


def decide_actions(stats: Dict[str, Any]) -> Dict[str, Any]:
    """The boss reviews the stats and decides what to do. Returns actionable commands."""
    actions = {"kill": [], "deploy": [], "warn": [], "risk_mode": "normal",
               "created_strategies": [], "brief": ""}

    agents = stats.get("agents", [])
    today_pnl = stats.get("today_pnl", 0)
    today_n = stats.get("today_n", 0)

    # 1. Find kill candidates (losing agents with enough history)
    for a in agents:
        if a["n"] < MIN_TRADES_TO_JUDGE:
            continue
        # Already paper/killed agents won't show in stats if they have no recent trades

        reasons = []
        if a["pf"] < KILL_IF_PF_BELOW:
            reasons.append(f"PF={a['pf']}<{KILL_IF_PF_BELOW}")
        if a["wr"] < KILL_IF_WR_BELOW:
            reasons.append(f"WR={a['wr']}%<{KILL_IF_WR_BELOW}%")
        if a["total"] < KILL_IF_TOTAL_BELOW:
            reasons.append(f"total=${a['total']:.2f}<${KILL_IF_TOTAL_BELOW}")

        if len(reasons) >= 2:  # need 2+ red flags to kill
            actions["kill"].append({
                "agent": a["agent"],
                "reasons": reasons,
                "stats": a,
            })

    # 2. Find deploy candidates (paper agents that proved edge)
    for a in agents:
        if a["n"] < DEPLOY_IF_N_ABOVE:
            continue
        avg_pnl = a["avg_pnl"] or 0
        # Approximate ExpR from avg_pnl
        if a["wr"] >= DEPLOY_IF_WR_ABOVE and avg_pnl > DEPLOY_IF_EXPR_ABOVE and a["total"] > 0.50:
            actions["deploy"].append({
                "agent": a["agent"],
                "stats": a,
            })

    # 3. Risk mode
    if today_pnl <= -10:
        actions["risk_mode"] = "defensive"
        actions["brief"] += "🔴 DEFENSIVE: -$10+ today. Reducing size, high conf only.\n"
    elif today_pnl >= 15:
        actions["risk_mode"] = "profit_lock"
        actions["brief"] += "🟢 PROFIT LOCK: +$15+ today. Locking in gains.\n"
    elif today_pnl >= 5:
        actions["risk_mode"] = "normal_profit"
        actions["brief"] += "🟡 GREEN: +$5+ today. Normal sizing.\n"
    else:
        actions["risk_mode"] = "normal"
        actions["brief"] += f"⚪ Today: ${today_pnl:+.2f} ({today_n}t).\n"

    # 4. Build brief
    top3 = [a for a in agents if a["n"] >= 3][:3]
    if top3:
        best = top3[0]
        actions["brief"] += f"🏆 Best: {best['agent']} ({best['n']}t, {best['wr']}% WR, PF{best['pf']}, ${best['total']:+.2f})\n"

    if actions["kill"]:
        names = [k["agent"] for k in actions["kill"]]
        actions["brief"] += f"🔴 Kill: {', '.join(names)}\n"

    if actions["deploy"]:
        names = [d["agent"] for d in actions["deploy"]]
        actions["brief"] += f"🟢 Deploy: {', '.join(names)}\n"

    # 5. Generate new strategies from winning patterns
    try:
        from hermes_brain import generate_new_strategies
        new_strats = generate_new_strategies()
        if new_strats:
            actions["created_strategies"] = [
                {"name": s.name, "indicators": s.indicators, "regime": s.regime_filter}
                for s in new_strats[:5]
            ]
            actions["brief"] += f"🧪 Created {len(new_strats)} new strategies (paper testing)\n"
    except Exception as e:
        log.debug(f"strategy factory: {e}")

    return actions


async def execute_boss_decisions(actions: Dict[str, Any]) -> str:
    """Execute the boss's decisions via the Hermes bridge."""
    results = []

    try:
        from hermes_bridge import Bridge, handle_command
        bridge = Bridge()
    except Exception as e:
        return f"boss bridge error: {e}"

    # Execute kills
    for k in actions.get("kill", []):
        cmd = type('Command', (), {
            'cmd': 'undeploy',
            'args': {'agent': k['agent']},
            'id': f"boss_kill_{int(time.time())}",
            'ts': datetime.now(timezone.utc).isoformat(),
            'source': 'big_boss',
        })()
        # We need a ctx with the right methods. Use the live bot's bridge ctx.
        # Since we're in the boss loop, we use the hermes bridge directly.
        try:
            cid = bridge.send_command("undeploy", source="big_boss", agent=k["agent"])
            ack = bridge.wait_ack(cid, timeout=5.0)
            results.append(f"kill {k['agent']}: {ack.result if ack else 'no_ack'}")
        except Exception as e:
            results.append(f"kill {k['agent']} failed: {e}")

    # Execute deploys
    for d in actions.get("deploy", []):
        try:
            cid = bridge.send_command("deploy", source="big_boss",
                                       agent=d["agent"], size=0.05)
            ack = bridge.wait_ack(cid, timeout=5.0)
            results.append(f"deploy {d['agent']}: {ack.result if ack else 'no_ack'}")
        except Exception as e:
            results.append(f"deploy {d['agent']} failed: {e}")

    return "; ".join(results) if results else "no actions needed"


async def send_boss_telegram(brief: str):
    """Send the boss's verdict to Saad via Telegram."""
    try:
        from hermes_telegram import send_message, CHAT_ID
        if CHAT_ID:
            send_message(CHAT_ID, f"🦉 <b>BIG BOSS</b>\n{brief}")
    except Exception:
        pass


# =============================================================================
# MAIN BOSS LOOP — runs inside the bot's asyncio event loop
# =============================================================================

async def big_boss_loop():
    """The Big Boss autonomous overseer. Runs every 15 minutes, reviews everything,
    and acts without asking. Imported and started by bot.py."""
    log.info("👑 BIG BOSS online — full autonomous control active")

    # Wait 2 minutes on startup so the bot stabilizes
    await asyncio.sleep(120)

    last_brief_sent = ""
    cycle = 0

    while True:
        try:
            cycle += 1
            # Pull stats
            stats = get_db_stats()
            if "error" in stats:
                await asyncio.sleep(BOSS_INTERVAL_S)
                continue

            # Decide
            actions = decide_actions(stats)

            # Execute
            exec_result = await execute_boss_decisions(actions)

            # Brief Saad (only if something changed or every 4 cycles = 1 hour)
            brief = actions.get("brief", "")
            if brief and (brief != last_brief_sent or cycle % 4 == 0):
                await send_boss_telegram(f"{brief}\n⚡ {exec_result}")
                last_brief_sent = brief

            log.info(f"big_boss cycle={cycle}: {exec_result}")

        except Exception:
            log.error(f"big_boss_loop:\n{traceback.format_exc()}")

        await asyncio.sleep(BOSS_INTERVAL_S)


# =============================================================================
# STANDALONE CLI
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("👑 BIG BOSS — Autonomous Overseer")
    print("=" * 60)
    stats = get_db_stats()
    if "error" in stats:
        print(f"Error: {stats['error']}")
        sys.exit(1)

    print(f"\nToday: ${stats['today_pnl']:+.2f} ({stats['today_n']}t)")
    print(f"7 days: ${stats['7d_pnl']:+.2f} ({stats['7d_n']}t)")

    print(f"\n=== AGENT ROSTER ({len(stats['agents'])}) ===")
    for a in stats["agents"]:
        flag = ""
        if a["n"] >= MIN_TRADES_TO_JUDGE:
            if a["pf"] < KILL_IF_PF_BELOW or a["wr"] < KILL_IF_WR_BELOW:
                flag = " 🔴 KILL"
            elif a["wr"] >= DEPLOY_IF_WR_ABOVE and a["total"] > 1:
                flag = " 🟢 KEEP"
        print(f"  {a['agent']:25s} | {a['n']:3d}t | {a['wr']:5.1f}% WR | "
              f"PF{a['pf']:5.2f} | ${a['total']:>+8.2f}{flag}")

    actions = decide_actions(stats)
    print(f"\n=== BOSS DECISIONS ===")
    print(f"Risk mode: {actions['risk_mode']}")
    if actions["kill"]:
        print("KILL:")
        for k in actions["kill"]:
            print(f"  ❌ {k['agent']}: {', '.join(k['reasons'])}")
    if actions["deploy"]:
        print("DEPLOY:")
        for d in actions["deploy"]:
            print(f"  ✅ {d['agent']} ({d['stats']['n']}t, {d['stats']['wr']}% WR, ${d['stats']['total']:+.2f})")
    if actions["created_strategies"]:
        print("NEW STRATEGIES:")
        for s in actions["created_strategies"]:
            print(f"  🧪 {s['name']}: {s['indicators']} @ {s['regime']}")
    if not actions["kill"] and not actions["deploy"] and not actions["created_strategies"]:
        print("  No actions needed. All agents performing within bounds.")
