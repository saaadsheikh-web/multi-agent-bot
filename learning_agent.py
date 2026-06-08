#!/usr/bin/env python3
"""
learning_agent.py — runs daily. Reviews closed trades, extracts lessons.

Goal: continuously improve the bot's edge. Every day:
  1. Pull all closed trades from bot.db
  2. Group by agent, regime, time-of-day, symbol class
  3. Compute per-segment WR, ExpR, avg_win, avg_loss
  4. Identify patterns:
     - Which agents work in TRENDING vs RANGING vs VOLATILE
     - Which symbols are profitable, which aren't
     - Time-of-day effects
     - Holding-time vs PnL correlation
  5. Write findings to LEARNINGS.md (cumulative) and TODAYS_LEARNINGS.md (overwrite)
  6. Surface top 3 actionable insights to CEO_LOG.md
"""
import os, sys, json, sqlite3, datetime as dt
from pathlib import Path
from collections import defaultdict
from statistics import mean, median, stdev

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
DB = WORK / "bot.db"
LEARN_LOG = WORK / "learning_agent.log"
LEARN_FILE = WORK / "LEARNINGS.md"
TODAY_FILE = WORK / "TODAYS_LEARNINGS.md"
CEO_LOG = WORK / "CEO_LOG.md"


def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(LEARN_LOG, "a") as f:
        f.write(line + "\n")


def fetch_trades():
    if not DB.exists():
        return []
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    cur = conn.execute("""
        SELECT * FROM trades
        WHERE status='closed' AND closed_at IS NOT NULL
        ORDER BY closed_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def stats(trades, key=None):
    """Compute stats. If key given, group by that field."""
    if not trades:
        return None
    if key is None:
        pnls = [float(t.get("pnl") or 0) for t in trades]
        if not pnls:
            return None
        wins = [p for p in pnls if p > 0]
        return {
            "n": len(pnls),
            "wr": round(len(wins) / len(pnls) * 100, 1),
            "total_pnl": round(sum(pnls), 2),
            "avg_pnl": round(mean(pnls), 2),
            "avg_win": round(mean(wins), 2) if wins else 0,
            "avg_loss": round(mean([p for p in pnls if p <= 0]), 2) if any(p <= 0 for p in pnls) else 0,
        }
    grouped = defaultdict(list)
    for t in trades:
        grouped[t.get(key) or "unknown"].append(t)
    out = {}
    for k, ts in grouped.items():
        out[k] = stats(ts)
    return out


def time_of_day_breakdown(trades):
    """Bin closed trades by UTC hour."""
    bins = defaultdict(list)
    for t in trades:
        ts = t.get("closed_at") or t.get("opened_at")
        if not ts:
            continue
        try:
            d = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            bins[d.hour].append(float(t.get("pnl") or 0))
        except Exception:
            continue
    out = {}
    for h, pnls in sorted(bins.items()):
        if pnls:
            out[h] = {
                "n": len(pnls),
                "total": round(sum(pnls), 2),
                "avg": round(mean(pnls), 2),
            }
    return out


def write_learnings(trades):
    """Generate the LEARNINGS markdown."""
    today = dt.datetime.now().strftime("%Y-%m-%d")
    lines = [f"# Learning Agent Report — {today}\n"]

    overall = stats(trades)
    if not overall:
        lines.append("No closed trades to analyze.\n")
        return "\n".join(lines)

    lines.append("## Overall Performance\n")
    lines.append(f"- Closed trades: {overall['n']}")
    lines.append(f"- Win rate: {overall['wr']}%")
    lines.append(f"- Total PnL: ${overall['total_pnl']}")
    lines.append(f"- Avg PnL/trade: ${overall['avg_pnl']}")
    lines.append(f"- Avg win: ${overall['avg_win']}")
    lines.append(f"- Avg loss: ${overall['avg_loss']}\n")

    # Per-agent
    by_agent = stats(trades, key="agent")
    if by_agent:
        lines.append("## Per-Agent Performance\n")
        ranked = sorted(by_agent.items(), key=lambda x: -(x[1]["total_pnl"]))
        lines.append("| Agent | Trades | WR | Total PnL | Avg/trade |")
        lines.append("|---|---|---|---|---|")
        for name, s in ranked:
            lines.append(f"| {name} | {s['n']} | {s['wr']}% | ${s['total_pnl']} | ${s['avg_pnl']} |")
        lines.append("")

    # Per-symbol
    by_sym = stats(trades, key="symbol")
    if by_sym:
        lines.append("## Per-Symbol Performance\n")
        ranked = sorted(by_sym.items(), key=lambda x: -(x[1]["total_pnl"]))[:10]
        lines.append("| Symbol | Trades | WR | Total PnL |")
        lines.append("|---|---|---|---|")
        for name, s in ranked:
            lines.append(f"| {name} | {s['n']} | {s['wr']}% | ${s['total_pnl']} |")
        lines.append("")

    # Per-side
    by_side = stats(trades, key="side")
    if by_side:
        lines.append("## Long vs Short\n")
        for side, s in by_side.items():
            lines.append(f"- **{side}**: {s['n']} trades, {s['wr']}% WR, total ${s['total_pnl']}")
        lines.append("")

    # Time-of-day
    tod = time_of_day_breakdown(trades)
    if tod:
        lines.append("## Time-of-Day (UTC)\n")
        ranked = sorted(tod.items(), key=lambda x: -(x[1]["total"]))[:5]
        lines.append("Top profitable hours:")
        for h, s in ranked:
            lines.append(f"- {h:02d}:00 UTC — {s['n']} trades, ${s['total']} total")
        lines.append("")
        ranked_loss = sorted(tod.items(), key=lambda x: x[1]["total"])[:3]
        lines.append("Worst hours:")
        for h, s in ranked_loss:
            lines.append(f"- {h:02d}:00 UTC — {s['n']} trades, ${s['total']} total")
        lines.append("")

    # Actionable insights — calibrated for paper / 0.10x sizing where $ moves
    # are small. Use net-PnL relative to per-trade avg, not absolute thresholds.
    lines.append("## Actionable Insights\n")
    insights: list[str] = []

    # Agent kill candidates: net negative AND (WR<40 with n>=3 OR worst single
    # loss < -100% of position, which means leverage was eating us alive).
    if by_agent:
        for name, s in by_agent.items():
            if s["n"] < 3 or s["total_pnl"] >= 0:
                continue
            agent_trades = [t for t in trades if (t.get("agent") or "") == name]
            wins_only = [t for t in agent_trades if (t.get("pnl") or 0) > 0]
            wr = len(wins_only) / len(agent_trades) * 100 if agent_trades else 0
            worst_pct = min(
                (float(t.get("pnl_pct") or 0) for t in agent_trades),
                default=0,
            )
            if wr < 40 or worst_pct < -1.0:
                insights.append(
                    f"- **KILL/RESTRICT**: `{name}` — {s['n']} trades, "
                    f"WR {wr:.0f}%, net ${s['total_pnl']:.2f}, worst -{abs(worst_pct)*100:.0f}%. "
                    f"Disable or paper-only until backtest re-validates."
                )

    # Agent scale candidates: net positive AND WR >= 45% AND n >= 5.
    if by_agent:
        for name, s in by_agent.items():
            if s["n"] < 5 or s["total_pnl"] <= 0:
                continue
            agent_trades = [t for t in trades if (t.get("agent") or "") == name]
            wins_only = [t for t in agent_trades if (t.get("pnl") or 0) > 0]
            wr = len(wins_only) / len(agent_trades) * 100 if agent_trades else 0
            if wr >= 45:
                insights.append(
                    f"- **SCALE UP**: `{name}` — {s['n']} trades, "
                    f"WR {wr:.0f}%, net ${s['total_pnl']:.2f}. "
                    f"Increase notional_multiplier 1.5x next deploy review."
                )

    # Symbol blacklist candidates: any symbol with >=2 trades and net negative
    # AND avg loss% < -50% of position (real damage, not slippage).
    if by_sym:
        for name, s in by_sym.items():
            if s["n"] < 2 or s["total_pnl"] >= 0:
                continue
            sym_losses = [
                float(t.get("pnl_pct") or 0)
                for t in trades
                if (t.get("symbol") or "") == name and (t.get("pnl") or 0) < 0
            ]
            if not sym_losses:
                continue
            avg_loss_pct = sum(sym_losses) / len(sym_losses)
            if avg_loss_pct < -0.5:
                insights.append(
                    f"- **SYMBOL BLACKLIST**: `{name}` — {s['n']} trades, "
                    f"net ${s['total_pnl']:.2f}, avg loss {avg_loss_pct*100:.0f}%. "
                    f"Add to LOSING_SYMBOL_BLACKLIST in bot.py."
                )

    # Hour-window warnings: any 3-hour rolling window with cumulative < -$1
    # AND combined WR < 30%.
    tod = time_of_day_breakdown(trades) if trades else {}
    if tod:
        bad_windows = []
        for h_start in range(0, 22):
            window = [tod.get(h, {"n": 0, "total": 0}) for h in range(h_start, h_start + 3)]
            n_total = sum(w["n"] for w in window)
            pnl_total = sum(w["total"] for w in window)
            if n_total >= 4 and pnl_total < -1.0:
                bad_windows.append((h_start, n_total, pnl_total))
        if bad_windows:
            bad_windows.sort(key=lambda x: x[2])
            h_start, n, p = bad_windows[0]
            insights.append(
                f"- **HOUR GATE**: {h_start:02d}:00–{h_start+3:02d}:00 UTC bled "
                f"${p:.2f} across {n} trades. Require ≥2-agent confluence in this window."
            )

    # Long vs short bias
    if by_side:
        long_pnl = by_side.get("long", {}).get("total_pnl", 0)
        short_pnl = by_side.get("short", {}).get("total_pnl", 0)
        long_n = by_side.get("long", {}).get("n", 0)
        short_n = by_side.get("short", {}).get("n", 0)
        if long_n >= 5 and short_n >= 5:
            ratio = (short_pnl / max(short_n, 1)) - (long_pnl / max(long_n, 1))
            if ratio > 0.10:
                insights.append(
                    f"- **EDGE: SHORTS**: avg short ${short_pnl/short_n:.2f}/trade vs "
                    f"long ${long_pnl/long_n:.2f}/trade. Loosen short conf floor by 1."
                )
            elif ratio < -0.10:
                insights.append(
                    f"- **EDGE: LONGS**: avg long ${long_pnl/long_n:.2f}/trade vs "
                    f"short ${short_pnl/short_n:.2f}/trade. Loosen long conf floor by 1."
                )

    if insights:
        lines.extend(insights)
    else:
        lines.append("- No high-confidence patterns yet — keep collecting data.")
    lines.append("")

    return "\n".join(lines)


def append_to_ceo_log(insights_summary):
    """Add a section to CEO_LOG.md so the CEO sees today's learnings."""
    section = (
        f"\n\n## LEARNING AGENT — {dt.datetime.now().isoformat()}\n\n"
        f"{insights_summary}\n"
    )
    with open(CEO_LOG, "a") as f:
        f.write(section)


def main():
    log("=== learning agent run start ===")

    # Step 0a: journal every newly closed trade with full forensic detail.
    try:
        import trade_journal
        jr = trade_journal.run()
        log(f"trade journal v2: +{jr.get('new', 0)} new entries, {jr.get('total', 0)} total")
    except Exception as e:
        log(f"trade journal failed: {e!r}")

    # Step 0b: regenerate the rolled-up research report.
    try:
        import research_report
        research_report.main()
        log("research report regenerated")
    except Exception as e:
        log(f"research report failed: {e!r}")

    trades = fetch_trades()
    log(f"loaded {len(trades)} closed trades")

    report = write_learnings(trades)

    # Write today's report (overwrite)
    TODAY_FILE.write_text(report)
    log(f"wrote {TODAY_FILE.name}")

    # Append to cumulative LEARNINGS.md
    sep = "\n\n" + "─" * 60 + "\n\n"
    if LEARN_FILE.exists():
        with open(LEARN_FILE, "a") as f:
            f.write(sep + report)
    else:
        LEARN_FILE.write_text(report)
    log(f"appended to {LEARN_FILE.name}")

    # Surface to CEO
    short_summary = report.split("## Actionable Insights")[1] if "## Actionable Insights" in report else "(no insights yet — sample size too small)"
    append_to_ceo_log(f"### Today's actionable insights:{short_summary}")
    log("CEO_LOG.md updated with today's actionable insights")

    log("=== done ===")


if __name__ == "__main__":
    main()
