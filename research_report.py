#!/usr/bin/env python3
"""
research_report.py — roll trade_journal.jsonl up into RESEARCH_REPORT.md

Statistics produced:
  - Headline P&L, win rate, expectancy, profit factor
  - Per-agent, per-symbol, per-hour breakdowns
  - Exit-reason economics (TP / SL / trail / time)
  - Decision-grade distribution and PnL by grade
  - MFE/MAE summary: how often were we "up" before losing
  - Slippage analysis: how far did exits land from planned TP / SL
  - Top ranked hypotheses about what's hurting us
"""
from __future__ import annotations

import os
import json
import statistics as stats
from collections import defaultdict, Counter
from pathlib import Path
import datetime as dt

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
JOURNAL = WORK / "trade_journal.jsonl"
REPORT = WORK / "RESEARCH_REPORT.md"


def load() -> list[dict]:
    if not JOURNAL.exists():
        return []
    rows = []
    with open(JOURNAL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def fmt_pnl(x):
    return f"{x:+.4f}"


def group_stats(rows: list[dict], key_fn) -> list[tuple]:
    by = defaultdict(list)
    for r in rows:
        k = key_fn(r)
        if k is None:
            continue
        by[k].append(r)
    out = []
    for k, group in by.items():
        n = len(group)
        wins = sum(1 for r in group if r["outcome"] == "WIN")
        losses = sum(1 for r in group if r["outcome"] == "LOSS")
        total_pnl = sum(r["pnl"] for r in group)
        wr = wins / n * 100 if n else 0
        avg = total_pnl / n if n else 0
        out.append((k, n, wr, total_pnl, avg, wins, losses))
    out.sort(key=lambda x: x[3], reverse=True)
    return out


def main():
    rows = load()
    if not rows:
        print("no journal data; run trade_journal.py first")
        return

    n = len(rows)
    wins = [r for r in rows if r["outcome"] == "WIN"]
    losses = [r for r in rows if r["outcome"] == "LOSS"]
    flats = [r for r in rows if r["outcome"] == "FLAT"]
    total_pnl = sum(r["pnl"] for r in rows)
    win_pnls = [r["pnl"] for r in wins]
    loss_pnls = [r["pnl"] for r in losses]
    avg_win = stats.mean(win_pnls) if win_pnls else 0
    avg_loss = stats.mean(loss_pnls) if loss_pnls else 0
    profit_factor = (sum(win_pnls) / abs(sum(loss_pnls))) if loss_pnls and sum(loss_pnls) != 0 else float("inf")
    expectancy = total_pnl / n if n else 0
    wr = len(wins) / n * 100 if n else 0

    lines: list[str] = []
    lines.append(f"# Research Report — {dt.date.today().isoformat()}\n")
    lines.append(f"_Generated from {n} journaled closed trades._\n")

    # ── Headline
    lines.append("## 1 · Headline\n")
    lines.append(f"- Closed trades: **{n}**")
    lines.append(f"- Win rate: **{wr:.1f}%** ({len(wins)}W / {len(losses)}L / {len(flats)}F)")
    lines.append(f"- Total PnL: **{fmt_pnl(total_pnl)}**")
    lines.append(f"- Avg win: {fmt_pnl(avg_win)} · Avg loss: {fmt_pnl(avg_loss)}")
    lines.append(f"- Expectancy / trade: {fmt_pnl(expectancy)}")
    lines.append(f"- Profit factor: {profit_factor:.2f}")
    lines.append("")

    # ── Exit-reason economics
    lines.append("## 2 · Exit-reason economics\n")
    lines.append("| exit_reason | n | win_rate | total_pnl | avg/trade |")
    lines.append("|---|---|---|---|---|")
    for k, count, wrk, tp, avg, w, l in group_stats(rows, lambda r: r["exit_reason"]):
        lines.append(f"| {k} | {count} | {wrk:.0f}% | {fmt_pnl(tp)} | {fmt_pnl(avg)} |")
    lines.append("")

    # ── Per-agent
    lines.append("## 3 · Per-agent performance\n")
    lines.append("| agent | n | win_rate | total_pnl | avg/trade |")
    lines.append("|---|---|---|---|---|")
    for k, count, wrk, tp, avg, w, l in group_stats(rows, lambda r: r["agent"]):
        lines.append(f"| {k} | {count} | {wrk:.0f}% | {fmt_pnl(tp)} | {fmt_pnl(avg)} |")
    lines.append("")

    # ── Per-symbol (top 15)
    lines.append("## 4 · Per-symbol performance (top 15 by PnL)\n")
    lines.append("| symbol | n | win_rate | total_pnl | avg/trade |")
    lines.append("|---|---|---|---|---|")
    sym = group_stats(rows, lambda r: r["symbol"])
    for k, count, wrk, tp, avg, w, l in sym[:15]:
        lines.append(f"| {k} | {count} | {wrk:.0f}% | {fmt_pnl(tp)} | {fmt_pnl(avg)} |")
    lines.append("")
    lines.append("### Worst 10 symbols\n")
    lines.append("| symbol | n | win_rate | total_pnl | avg/trade |")
    lines.append("|---|---|---|---|---|")
    for k, count, wrk, tp, avg, w, l in sym[-10:][::-1]:
        lines.append(f"| {k} | {count} | {wrk:.0f}% | {fmt_pnl(tp)} | {fmt_pnl(avg)} |")
    lines.append("")

    # ── Per-hour
    lines.append("## 5 · Per-hour (UTC)\n")
    lines.append("| hour | n | win_rate | total_pnl | avg/trade |")
    lines.append("|---|---|---|---|---|")
    for k, count, wrk, tp, avg, w, l in sorted(group_stats(rows, lambda r: r["hour_utc"]), key=lambda x: x[0]):
        lines.append(f"| {k:02d} | {count} | {wrk:.0f}% | {fmt_pnl(tp)} | {fmt_pnl(avg)} |")
    lines.append("")

    # ── Decision grade
    lines.append("## 6 · Decision-grade distribution\n")
    lines.append("Grade is independent of outcome — it rates the *quality of the entry decision*.\n")
    lines.append("| grade | n | win_rate | total_pnl | avg/trade |")
    lines.append("|---|---|---|---|---|")
    for k, count, wrk, tp, avg, w, l in sorted(group_stats(rows, lambda r: r["decision"]["decision_grade"]), key=lambda x: x[0]):
        lines.append(f"| {k} | {count} | {wrk:.0f}% | {fmt_pnl(tp)} | {fmt_pnl(avg)} |")
    lines.append("")

    # ── MFE / MAE
    mfe = [r["mfe_mae"]["mfe_pct"] for r in rows if r["mfe_mae"].get("mfe_pct") is not None]
    mae = [r["mfe_mae"]["mae_pct"] for r in rows if r["mfe_mae"].get("mae_pct") is not None]
    gave_back = [r["mfe_mae"]["trail_gave_back_pct"] for r in rows if r["mfe_mae"].get("trail_gave_back_pct") is not None]
    lines.append("## 7 · Excursion analysis (MFE / MAE)\n")
    if mfe:
        lines.append(f"- MFE: median {stats.median(mfe):.2f}% · p90 {sorted(mfe)[int(len(mfe)*0.9)-1]:.2f}%")
    if mae:
        lines.append(f"- MAE: median {stats.median(mae):.2f}% · p90 {sorted(mae)[int(len(mae)*0.9)-1]:.2f}%")
    if gave_back:
        lines.append(f"- Trail gave back: median {stats.median(gave_back):.2f}% · p90 {sorted(gave_back)[int(len(gave_back)*0.9)-1]:.2f}%")

    # Losers who were winners
    reverters = [r for r in losses if r["mfe_mae"].get("mfe_pct") and r["mfe_mae"]["mfe_pct"] > 0.5]
    lines.append(f"- **Reversal losses** (lost trades that were up >0.5% at peak): {len(reverters)} of {len(losses)} losses")
    if reverters:
        avg_peak = stats.mean([r["mfe_mae"]["mfe_pct"] for r in reverters])
        lines.append(f"  - Average peak gain before reversal: {avg_peak:.2f}%")
        lines.append(f"  - **Hypothesis:** trail-stop trigger is too far. Tightening trail_pct on these symbols would convert losses to scratches or wins.")
    lines.append("")

    # ── Tags
    tag_counter = Counter()
    for r in rows:
        for t in r.get("tags", []):
            tag_counter[t] += 1
    lines.append("## 8 · Tag frequency\n")
    lines.append("| tag | count |")
    lines.append("|---|---|")
    for tag, c in tag_counter.most_common(20):
        lines.append(f"| {tag} | {c} |")
    lines.append("")

    # ── Ranked hypotheses
    lines.append("## 9 · Ranked hypotheses — what's hurting us\n")
    hyps = []
    # 1. Killed agents
    killed_loss = sum(r["pnl"] for r in rows if r["flags"]["agent_killed"])
    n_killed = sum(1 for r in rows if r["flags"]["agent_killed"])
    if n_killed:
        hyps.append((abs(killed_loss), f"**Killed-list agents still bled $-{abs(killed_loss):.2f} over {n_killed} trades.** Confirm they're disabled in bot.py."))
    # 2. Blacklisted symbols
    bl_loss = sum(r["pnl"] for r in rows if r["flags"]["symbol_blacklisted"])
    n_bl = sum(1 for r in rows if r["flags"]["symbol_blacklisted"])
    if n_bl:
        hyps.append((abs(bl_loss), f"**Blacklisted symbols still bled $-{abs(bl_loss):.2f} over {n_bl} trades.** Enforce the blacklist gate at order time."))
    # 3. Trail gave back too much
    big_giveback = [r for r in rows if (r["mfe_mae"].get("trail_gave_back_pct") or 0) > 1.0]
    if big_giveback:
        gb_loss = sum(r["pnl"] for r in big_giveback)
        hyps.append((abs(gb_loss), f"**Trail-stop gave back >1% on {len(big_giveback)} trades (net $${fmt_pnl(gb_loss)}).** Trail_pct of 0.6% appears too loose; test 0.3-0.4%."))
    # 4. TP almost never hits
    n_tp = sum(1 for r in rows if r["exit_reason"] == "TP_HIT")
    n_sl = sum(1 for r in rows if r["exit_reason"] == "SL_HIT")
    if n_tp and n_sl:
        ratio = n_sl / n_tp
        hyps.append((ratio * 10, f"**TPs hit {n_tp}× vs SLs {n_sl}× ({ratio:.1f}:1 SL:TP ratio).** TPs may be too far. Consider tighter TPs or partial profit-taking at 0.5R."))
    # 5. Long-side bias
    long_pnl = sum(r["pnl"] for r in rows if r["side"] == "long")
    short_pnl = sum(r["pnl"] for r in rows if r["side"] == "short")
    if long_pnl < 0 and short_pnl > 0:
        hyps.append((abs(long_pnl - short_pnl), f"**Longs net $${fmt_pnl(long_pnl)}, shorts net $${fmt_pnl(short_pnl)}.** Strong asymmetry — either market is in downtrend or long-entry logic is too eager."))
    # 6. Dead-hour bleed
    dh_pnl = sum(r["pnl"] for r in rows if r["flags"]["in_dead_zone"])
    n_dh = sum(1 for r in rows if r["flags"]["in_dead_zone"])
    if dh_pnl < 0:
        hyps.append((abs(dh_pnl), f"**Dead-zone hours (08-11 UTC) lost $${fmt_pnl(dh_pnl)} over {n_dh} trades.** Pause or require 2-agent confluence in this window."))

    hyps.sort(reverse=True)
    for _, msg in hyps:
        lines.append(f"- {msg}")
    lines.append("")

    # ── Recommended next steps
    lines.append("## 10 · Recommended next experiments\n")
    lines.append("1. **Tighten trail_pct** from 0.6% to 0.3% on `connors_rsi2` for 50 trades; measure trail_gave_back_pct delta.")
    lines.append("2. **Add 0.5R partial profit-take** so TP_HIT rate rises and trail_too_loose losses convert to scratches.")
    lines.append("3. **Hard-gate blacklisted symbols and killed agents at order time** (not just config). Audit any new trades from them as bugs.")
    lines.append("4. **Long-bias check:** investigate whether long entries chase pumps. Compare RSI at long-entry vs short-entry.")
    lines.append("5. **Dead-zone pause:** require ≥2 agent confluence between 08-11 UTC, or skip entirely.")
    lines.append("")

    REPORT.write_text("\n".join(lines))
    print(f"wrote {REPORT} ({len(lines)} lines, {n} trades analyzed)")


if __name__ == "__main__":
    main()
