#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 HERMES KNOWLEDGE ENGINE — scans your entire machine for trading intelligence
=============================================================================
 Connects to every data source on Saad's Mac:
   - Google Drive backup (strategy docs, backtest reports)
   - Chrome IndexedDB (BloFin, Binance, Hyperliquid, Polymarket, GoatFundedTrader)
   - Other trading bots (hyperliquid_bot, polymarket_bot, blofin, shams, clawbot)
   - Local logs, trade journals, backtest results
   - Firebase / cloud data

 Run: python3 hermes_knowledge.py  — scans everything and writes a master
 intelligence file that Hermes loads into context.
=============================================================================
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import defaultdict

HERE = Path(__file__).resolve().parent
HOME = Path.home()

# All known data sources
SOURCES = {
    "drive_backup": HERE / "drive_backup",
    "chrome_blofin": HOME / "Library/Application Support/Google/Chrome/Default/IndexedDB/https_blofin.com_0.indexeddb.leveldb",
    "chrome_binance": HOME / "Library/Application Support/Google/Chrome/Default/IndexedDB/https_www.binance.com_0.indexeddb.leveldb",
    "chrome_hyperliquid": HOME / "Library/Application Support/Google/Chrome/Default/IndexedDB/https_app.hyperliquid.xyz_0.indexeddb.leveldb",
    "chrome_polymarket": HOME / "Library/Application Support/Google/Chrome/Default/IndexedDB/https_polymarket.com_0.indexeddb.leveldb",
    "chrome_goatfunded": HOME / "Library/Application Support/Google/Chrome/Default/IndexedDB/https_www.goatfundedtrader.com_0.indexeddb.leveldb",
    "hyperliquid_bot": HOME / "hyperliquid_bot",
    "polymarket_bot": HOME / "polymarket_bot",
    "blofin_bot": HOME / "blofin_bot.py",
    "clawbot": HOME / "clawbot.py",
    "shams_bot": HOME / "shams_bot.py",
    "trading_bot": HOME / "trading_bot.py",
    "bot_brain": HOME / "bot_brain.py",
    "hermes_master": HOME / "hermes_master_brain.py",
    "backtests": HERE / "backtest_data",
    "trade_journal": HERE / "trade_journal.jsonl",
    "strategy_pool": HERE / "strategy_pool.json",
    "db": HERE / "bot.db",
    "hyperliquid_db": HOME / "hyperliquid_bot/state.json",
}

MASTER_KNOWLEDGE_PATH = HERE / "HERMES_KNOWLEDGE.md"


def scan_filesystem() -> Dict[str, Any]:
    """Scan all known data sources and report what's available."""
    results = {"available": [], "missing": [], "size_mb": {}, "last_modified": {}}

    for name, path in SOURCES.items():
        p = Path(path)
        if p.exists():
            results["available"].append(name)
            try:
                size = 0
                if p.is_dir():
                    for f in p.rglob("*"):
                        if f.is_file():
                            size += f.stat().st_size
                else:
                    size = p.stat().st_size
                results["size_mb"][name] = round(size / (1024 * 1024), 2)
                results["last_modified"][name] = datetime.fromtimestamp(
                    p.stat().st_mtime, tz=timezone.utc
                ).isoformat()
            except Exception:
                pass
        else:
            results["missing"].append(name)

    return results


def scan_other_bots() -> Dict[str, Any]:
    """Read state from other trading bots on the machine."""
    bots = {}

    # Hyperliquid bot
    hl_state = HOME / "hyperliquid_bot/state.json"
    if hl_state.exists():
        try:
            bots["hyperliquid"] = json.loads(hl_state.read_text())
        except Exception:
            bots["hyperliquid"] = {"error": "unreadable"}

    # Hyperliquid bot log tail
    hl_log = HOME / "hyperliquid_bot/bot.log"
    if hl_log.exists():
        try:
            tail = hl_log.read_text(errors="ignore").splitlines()[-10:]
            bots["hyperliquid_log_tail"] = tail
        except Exception:
            pass

    # Polymarket bot
    pm_dir = HOME / "polymarket_bot"
    if pm_dir.exists():
        pm_files = list(pm_dir.glob("*"))
        bots["polymarket"] = {"files": [f.name for f in pm_files]}

    # Other bots
    for name in ["blofin_bot", "clawbot", "shams_bot", "trading_bot"]:
        path = HOME / f"{name}.py"
        if path.exists():
            try:
                content = path.read_text(errors="ignore")
                # Extract first 500 chars for overview
                bots[name] = {"size_kb": len(content) // 1024,
                              "preview": content[:500]}
            except Exception:
                pass

    return bots


def scan_backtest_knowledge() -> Dict[str, Any]:
    """Extract insights from backtest data and strategy pool."""
    knowledge = {}

    # Strategy pool
    sp = HERE / "strategy_pool.json"
    if sp.exists():
        try:
            pool = json.loads(sp.read_text())
            if isinstance(pool, list):
                knowledge["strategy_count"] = len(pool)
                # Summarize
                by_agent = defaultdict(lambda: {"count": 0, "best_wr": 0, "best_pf": 0})
                for s in pool:
                    if isinstance(s, dict):
                        agent = s.get("agent", "?")
                        by_agent[agent]["count"] += 1
                        wr = s.get("win_rate", s.get("wr", 0))
                        pf = s.get("profit_factor", s.get("pf", 0))
                        if wr and wr > by_agent[agent]["best_wr"]:
                            by_agent[agent]["best_wr"] = wr
                        if pf and pf > by_agent[agent]["best_pf"]:
                            by_agent[agent]["best_pf"] = pf
                knowledge["by_agent"] = dict(by_agent)
        except Exception:
            pass

    # Backtest data
    bt_dir = HERE / "backtest_data"
    if bt_dir.exists():
        csvs = list(bt_dir.glob("*.csv"))
        knowledge["backtest_csvs"] = len(csvs)
        knowledge["backtest_size_mb"] = round(
            sum(f.stat().st_size for f in csvs) / (1024 * 1024), 2
        )

    return knowledge


def scan_drive_docs() -> Dict[str, Any]:
    """Read Google Drive backup documents."""
    docs = {}
    drive = HERE / "drive_backup"
    if not drive.exists():
        return docs

    for md_file in sorted(drive.glob("*.md")):
        try:
            content = md_file.read_text(errors="ignore")
            docs[md_file.name] = {
                "size": len(content),
                "preview": content[:2000],
            }
        except Exception:
            pass

    return docs


def build_knowledge_report() -> str:
    """Build the master knowledge report for Hermes."""
    lines = [
        f"# HERMES KNOWLEDGE SCAN — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## 📁 FILESYSTEM SCAN",
        "",
    ]

    fs = scan_filesystem()
    lines.append(f"**{len(fs['available'])} sources available, "
                 f"{len(fs['missing'])} missing**")
    lines.append("")
    for name in fs["available"]:
        size = fs["size_mb"].get(name, 0)
        lines.append(f"- ✅ **{name}** ({size} MB)")
    if fs["missing"]:
        lines.append("")
        for name in fs["missing"]:
            lines.append(f"- ❌ {name} (not found)")

    # Other bots
    lines.append("")
    lines.append("## 🤖 OTHER TRADING BOTS")
    lines.append("")
    bots = scan_other_bots()
    for name, info in bots.items():
        lines.append(f"### {name}")
        if isinstance(info, dict):
            if "error" in info:
                lines.append(f"  Error: {info['error']}")
            elif "files" in info:
                lines.append(f"  Files: {', '.join(info['files'])}")
            elif "size_kb" in info:
                lines.append(f"  Size: {info['size_kb']} KB")
            elif "positions" in info:
                lines.append(f"  Positions: {info.get('positions', [])}")
        lines.append("")

    # Drive docs
    lines.append("## 📄 GOOGLE DRIVE DOCUMENTS")
    lines.append("")
    docs = scan_drive_docs()
    for name, info in docs.items():
        lines.append(f"### {name}")
        lines.append(f"```\n{info['preview']}\n```")
        lines.append("")

    # Backtests
    lines.append("## 📊 BACKTEST KNOWLEDGE")
    lines.append("")
    bt = scan_backtest_knowledge()
    lines.append(f"- Strategy pool: {bt.get('strategy_count', 0)} variants")
    lines.append(f"- Backtest CSV files: {bt.get('backtest_csvs', 0)} "
                 f"({bt.get('backtest_size_mb', 0)} MB)")
    if "by_agent" in bt:
        lines.append("")
        lines.append("| Agent | Variants | Best WR | Best PF |")
        lines.append("|-------|----------|---------|---------|")
        for agent, stats in sorted(bt["by_agent"].items()):
            lines.append(f"| {agent} | {stats['count']} | "
                        f"{stats['best_wr']:.0f}% | {stats['best_pf']:.1f} |")

    # DB quick stats
    lines.append("")
    lines.append("## 💾 DATABASE SNAPSHOT")
    lines.append("")
    db = HERE / "bot.db"
    if db.exists():
        try:
            conn = sqlite3.connect(str(db))
            total_trades = conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0]
            closed = conn.execute(
                "SELECT COUNT(*) FROM trades WHERE status='closed'"
            ).fetchone()[0]
            total_pnl = conn.execute(
                "SELECT COALESCE(SUM(pnl),0) FROM trades WHERE status='closed'"
            ).fetchone()[0]
            best_agent = conn.execute("""
                SELECT agent, SUM(pnl) as t FROM trades
                WHERE status='closed' GROUP BY agent ORDER BY t DESC LIMIT 1
            """).fetchone()
            conn.close()
            lines.append(f"- Total trades: {total_trades}")
            lines.append(f"- Closed: {closed}")
            lines.append(f"- Lifetime P&L: ${total_pnl:+.2f}")
            if best_agent:
                lines.append(f"- Best agent: {best_agent[0]} (${best_agent[1]:+.2f})")
        except Exception as e:
            lines.append(f"DB error: {e}")

    report = "\n".join(lines)
    MASTER_KNOWLEDGE_PATH.write_text(report)
    return report


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    print("🔍 Scanning your entire machine for trading intelligence...")
    print()
    report = build_knowledge_report()
    print(report)
    print(f"\n✅ Knowledge saved to: {MASTER_KNOWLEDGE_PATH}")
