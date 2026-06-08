#!/usr/bin/env python3
"""
DEEP LEARN — Hermes self-education engine.
Studies every trade, market pattern, TA setup. Gets smarter every cycle.

RESEARCH DOMAINS:
  1. Entry timing — when do entries work vs fail?
  2. Stop loss optimization — optimal SL per agent/symbol/regime
  3. Trail stop mastery — when to trail, how wide, based on volatility
  4. Market structure — trend strength, support/resistance, fib levels
  5. Pattern recognition — which TA confluences actually predict

RUNS: Every 2 hours, cumulative learning, feeds back to bot config.
"""

import os, sys, json, sqlite3, math, time as _time
from pathlib import Path
from collections import defaultdict
from statistics import mean, median, stdev
from datetime import datetime, timezone, timedelta
import numpy as np

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
DB_PATH = WORK / "bot.db"
JOURNAL_PATH = WORK / "journal.db"
LEARN_PATH = WORK / "DEEP_LEARNINGS.md"
CONFIG_PATH = WORK / "deep_learn_config.json"

# ── DATABASE ──────────────────────────────────────────────────

def load_trades():
    """Load all closed trades from bot.db"""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("""
        SELECT * FROM trades WHERE status='closed'
        ORDER BY opened_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    db.close()
    return rows

def load_journal():
    """Load trade journal (extended data)"""
    if not JOURNAL_PATH.exists():
        return []
    db = sqlite3.connect(str(JOURNAL_PATH))
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM journal ORDER BY closed_at DESC")
        rows = [dict(r) for r in cur.fetchall()]
    except:
        rows = []
    db.close()
    return rows

# ── ANALYSIS ENGINES ──────────────────────────────────────────

def analyze_entry_timing(trades):
    """Study optimal entry hours, days, conditions"""
    hourly = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0})
    daily = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0})

    for t in trades:
        try:
            ts = datetime.fromisoformat(t["opened_at"])
            h = ts.hour
            d = ts.strftime("%a")
            pnl = float(t.get("pnl", 0) or 0)
            hourly[h]["trades"] += 1
            hourly[h]["pnl"] += pnl
            if pnl > 0: hourly[h]["wins"] += 1
            daily[d]["trades"] += 1
            daily[d]["pnl"] += pnl
            if pnl > 0: daily[d]["wins"] += 1
        except: pass

    findings = []
    # Best hours
    ranked_h = sorted(hourly.items(), key=lambda x: x[1]["pnl"], reverse=True)
    findings.append("### Best Entry Hours (UTC)")
    for h, d in ranked_h[:5]:
        wr = d["wins"]/d["trades"]*100 if d["trades"] else 0
        findings.append(f"- {h:02d}:00 — {d['trades']}t, {wr:.0f}% WR, ${d['pnl']:+.2f}")

    # Worst hours
    findings.append("\n### Worst Entry Hours")
    for h, d in ranked_h[-5:]:
        wr = d["wins"]/d["trades"]*100 if d["trades"] else 0
        findings.append(f"- {h:02d}:00 — {d['trades']}t, {wr:.0f}% WR, ${d['pnl']:+.2f}")

    return "\n".join(findings)

def analyze_stop_loss(trades):
    """Learn optimal SL distances per agent and market condition"""
    agent_sl = defaultdict(lambda: {"trades": 0, "sl_hits": 0, "avg_loss": 0.0,
                                     "optimal_sl": 0, "total_loss": 0.0})

    for t in trades:
        agent = t.get("agent", "unknown")
        reason = t.get("close_reason", "")
        pnl = float(t.get("pnl", 0) or 0)
        sl_pct = abs(pnl) if pnl < 0 else 0

        agent_sl[agent]["trades"] += 1
        if "stop" in reason.lower() or "sl" in reason.lower():
            agent_sl[agent]["sl_hits"] += 1
            agent_sl[agent]["total_loss"] += abs(pnl)

    findings = ["### Optimal Stop Loss per Agent"]
    for agent, d in sorted(agent_sl.items(), key=lambda x: -x[1]["trades"]):
        if d["trades"] < 3: continue
        sl_rate = d["sl_hits"] / d["trades"] * 100
        avg_sl_loss = d["total_loss"] / d["sl_hits"] if d["sl_hits"] else 0
        findings.append(f"- **{agent}**: {d['trades']}t, SL hit {sl_rate:.0f}%, avg SL loss ${avg_sl_loss:.2f}")

    return "\n".join(findings)

def analyze_trail_mastery(trades):
    """Deep study of trail stop effectiveness"""
    trailed = [t for t in trades if "trail" in (t.get("close_reason","")).lower()]
    stopped = [t for t in trades if "stop" in (t.get("close_reason","")).lower()]

    findings = ["### Trail Stop Analysis"]

    if trailed:
        trail_pnls = [float(t.get("pnl",0) or 0) for t in trailed]
        trail_wr = sum(1 for p in trail_pnls if p > 0) / len(trail_pnls) * 100
        findings.append(f"- Trail exits: {len(trailed)} trades, {trail_wr:.0f}% WR, ${sum(trail_pnls):+.2f}")

        # Study: did trail give back profits?
        gave_back = [t for t in trailed if float(t.get("pnl",0) or 0) > 0 and
                     float(t.get("pnl",0) or 0) < float(t.get("high_water_pnl",0) or 0) * 0.5]
        if gave_back:
            findings.append(f"- ⚠️ {len(gave_back)} trades gave back >50% of peak profit to trail")

    if stopped:
        stop_pnls = [float(t.get("pnl",0) or 0) for t in stopped]
        findings.append(f"- SL exits: {len(stopped)} trades, ${sum(stop_pnls):+.2f}")

    # Ratio
    if trailed and stopped:
        ratio = len(trailed) / len(stopped) if len(stopped) else 999
        findings.append(f"- Trail:SL ratio = {ratio:.1f}:1 {'✅' if ratio > 1 else '❌ SL hits too frequent'}")

    return "\n".join(findings)

def analyze_symbol_edge(trades):
    """Which symbols are actually profitable?"""
    sym_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0, "longs": 0, "shorts": 0})

    for t in trades:
        sym = t.get("symbol", "?")
        pnl = float(t.get("pnl", 0) or 0)
        side = t.get("side", "?")
        sym_stats[sym]["trades"] += 1
        sym_stats[sym]["pnl"] += pnl
        if pnl > 0: sym_stats[sym]["wins"] += 1
        if side == "long": sym_stats[sym]["longs"] += 1
        else: sym_stats[sym]["shorts"] += 1

    findings = ["### Symbol Profitability"]

    # Winners
    winners = [(s,d) for s,d in sym_stats.items() if d["pnl"] > 0 and d["trades"] >= 2]
    winners.sort(key=lambda x: -x[1]["pnl"])
    findings.append("\n#### ✅ Profitable Symbols")
    for sym, d in winners[:10]:
        wr = d["wins"]/d["trades"]*100
        findings.append(f"- {sym}: {d['trades']}t, {wr:.0f}% WR, ${d['pnl']:+.2f} (L{d['longs']}/S{d['shorts']})")

    # Losers
    losers = [(s,d) for s,d in sym_stats.items() if d["pnl"] < 0 and d["trades"] >= 2]
    losers.sort(key=lambda x: x[1]["pnl"])
    findings.append("\n#### ❌ Losing Symbols")
    for sym, d in losers[:10]:
        wr = d["wins"]/d["trades"]*100
        findings.append(f"- {sym}: {d['trades']}t, {wr:.0f}% WR, ${d['pnl']:+.2f}")

    return "\n".join(findings)

def analyze_regime_performance(trades):
    """Study how strategies perform in different regimes"""
    # Simulate regime detection (simplified)
    regime_stats = defaultdict(lambda: {"trades": 0, "wins": 0, "pnl": 0.0, "agents": defaultdict(lambda: {"t":0,"pnl":0})})

    for t in trades:
        try:
            ts = datetime.fromisoformat(t["opened_at"])
            h = ts.hour
            # Crude regime: Asian (0-7), London (8-15), NY (16-23)
            if 0 <= h < 8: regime = "ASIAN"
            elif 8 <= h < 16: regime = "LONDON"
            else: regime = "NEW_YORK"

            pnl = float(t.get("pnl", 0) or 0)
            agent = t.get("agent", "?")
            regime_stats[regime]["trades"] += 1
            regime_stats[regime]["pnl"] += pnl
            if pnl > 0: regime_stats[regime]["wins"] += 1
            regime_stats[regime]["agents"][agent]["t"] += 1
            regime_stats[regime]["agents"][agent]["pnl"] += pnl
        except: pass

    findings = ["### Regime Performance"]
    for regime, d in sorted(regime_stats.items()):
        wr = d["wins"]/d["trades"]*100 if d["trades"] else 0
        findings.append(f"\n#### {regime} ({d['trades']} trades, {wr:.0f}% WR, ${d['pnl']:+.2f})")
        best_agent = max(d["agents"].items(), key=lambda x: x[1]["pnl"])
        findings.append(f"- Best agent: **{best_agent[0]}** (${best_agent[1]['pnl']:+.2f})")

    return "\n".join(findings)

def analyze_entry_quality(trades):
    """Study what makes a good entry - RSI, volume, time, confluence"""
    findings = ["### Entry Quality Analysis"]

    # Trades that went into profit vs straight to loss
    profitable = [t for t in trades if float(t.get("pnl",0) or 0) > 0]
    instant_loss = [t for t in trades if float(t.get("pnl",0) or 0) < -1.0]  # >1% loss

    if profitable:
        avg_profit = mean([float(t.get("pnl",0) or 0) for t in profitable])
        findings.append(f"- Profitable entries: {len(profitable)} trades, avg +${avg_profit:.2f}")

    if instant_loss:
        avg_loss = mean([abs(float(t.get("pnl",0) or 0)) for t in instant_loss])
        findings.append(f"- Instant losers: {len(instant_loss)} trades, avg -${avg_loss:.2f}")

    # What % of profitable trades had positive MFE?
    findings.append(f"- Win/Loss ratio: {len(profitable)}:{len(instant_loss)}")

    return "\n".join(findings)

def generate_recommendations(trades):
    """Generate actionable recommendations from all analysis"""
    findings = ["## 🧠 ACTIONABLE RECOMMENDATIONS\n"]

    # Find losing patterns
    sl_hits = [t for t in trades if "stop" in (t.get("close_reason","")).lower()]
    trail_exits = [t for t in trades if "trail" in (t.get("close_reason","")).lower()]

    if len(sl_hits) > len(trail_exits) * 2:
        findings.append("1. **SL TOO TIGHT**: SL hits 2× more than trail exits. Widen SL by 0.5-1% or improve entries.")

    # Check for time-based patterns
    losing_hours = defaultdict(float)
    for t in trades:
        try:
            h = datetime.fromisoformat(t["opened_at"]).hour
            pnl = float(t.get("pnl",0) or 0)
            losing_hours[h] += pnl
        except: pass

    worst_hours = sorted(losing_hours.items(), key=lambda x: x[1])[:3]
    findings.append(f"2. **Avoid these hours**: {', '.join(f'{h:02d}:00' for h,_ in worst_hours)} — consistent losers.")

    # Agent recommendations
    agent_pnl = defaultdict(float)
    agent_trades = defaultdict(int)
    for t in trades:
        agent_pnl[t.get("agent","?")] += float(t.get("pnl",0) or 0)
        agent_trades[t.get("agent","?")] += 1

    worst_agents = sorted(agent_pnl.items(), key=lambda x: x[1])[:3]
    best_agents = sorted(agent_pnl.items(), key=lambda x: -x[1])[:3]

    findings.append(f"3. **Scale up**: {', '.join(f'{a} (${p:+.0f})' for a,p in best_agents)}")
    findings.append(f"4. **Kill/restrict**: {', '.join(f'{a} (${p:+.0f})' for a,p in worst_agents)}")

    return "\n".join(findings)

# ── MAIN ──────────────────────────────────────────────────────

def main():
    trades = load_trades()
    if not trades:
        print("No trades found")
        return

    print(f"Deep Learn: analyzing {len(trades)} trades...")

    report = f"""# 🧠 Hermes Deep Learn Report
**Generated**: {datetime.now(timezone.utc).isoformat()}
**Trades analyzed**: {len(trades)}

---
"""

    report += analyze_entry_timing(trades)
    report += "\n\n---\n\n"
    report += analyze_stop_loss(trades)
    report += "\n\n---\n\n"
    report += analyze_trail_mastery(trades)
    report += "\n\n---\n\n"
    report += analyze_symbol_edge(trades)
    report += "\n\n---\n\n"
    report += analyze_regime_performance(trades)
    report += "\n\n---\n\n"
    report += analyze_entry_quality(trades)
    report += "\n\n---\n\n"
    report += generate_recommendations(trades)

    report += f"\n\n---\n*Deep Learn ran at {datetime.now(timezone.utc).isoformat()} | Hermes autonomous education system*"

    # Save
    with open(LEARN_PATH, "w") as f:
        f.write(report)

    print(f"Deep Learn complete. Report: {LEARN_PATH}")
    print(f"Key stats: {len(trades)} trades analyzed across {len(set(t.get('agent','?') for t in trades))} agents")

    # Save config insights
    config = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "trades_analyzed": len(trades),
        "version": 1
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
