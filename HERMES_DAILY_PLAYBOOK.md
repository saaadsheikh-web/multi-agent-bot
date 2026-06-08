# HERMES DAILY PLAYBOOK — Hour-by-Hour Routine

**Last updated:** 2026-05-18
**Purpose:** Concrete repeatable routine. Hermes runs this loop every cycle, and the daily milestones on the clock.

---

## CONTINUOUS LOOP (every 5 minutes)

```
1. read state           → health.json, hermes_bridge/state.json
2. guardrail check      → see HERMES_GUARDRAILS.md
3. open-position sweep  → take partials, set trail stops, pyramid winners
4. signal scan          → check pending signals against current regime + gates
5. log to memory        → only material decisions, not every tick
```

If anything red in step 2 → pause everything, do nothing else, escalate.

---

## DAILY MILESTONES (UTC clock)

### 00:00 UTC — Session boundary
- Reset daily P&L counter.
- Snapshot equity to memory.
- Read overnight CEO_LOG, AUDITOR_LOG, LEARNINGS.md for changes.
- Recalculate vol regime (BTC 14d ATR%).
- Set today's dynamic loss limit per `HERMES_GUARDRAILS.md` §1.

### 02:00 UTC — Asia mid-session
- Best historical window (00:00 +$1.11, 01:00 +$2.95). Be aggressive within rules.
- Confirm `connors_rsi2` shorts are active where signals show.

### 04:08 UTC — Nightly Strategy Hunter runs
- Wait for `BACKTEST_REPORT.md` to update.
- Diff against last 24h: any new strategy passes thresholds? Any incumbent degraded?
- New passing strategy → paper-deploy automatically. Live-deploy requires 5 days paper + 50+ trades.

### 07:00 BST (06:00 or 07:00 UTC depending on DST) — Morning Briefing
- Compose short Telegram for Saad: equity, today P&L so far, open positions, anything notable.

### 08:00–13:00 UTC — Killer hours gate
- Half risk, ≥2-agent confluence required, no new pyramid adds.
- Watch for breakout fails (3 bars) → fade with re-entry rule.

### 13:00 UTC — Gate lifts
- Resume normal sizing.
- US pre-market open energy starts.

### 17:00–19:00 UTC — Historical sweet spot
- 18:00 (+$1.14), 19:00 (+$1.36). Concentrated short edge.
- Lean into setups, especially shorts on downtrending symbols.

### 21:00 UTC — End-of-day review
- Tag every closed trade (wrong direction / wrong timing / stopped then reversed / regime mismatch).
- Update HERMES_MEMORY.md with daily summary.
- Check kill-rule triggers — any strategy hit 50+ trades with negative expectancy? Kill it.
- Check promote-rule triggers — any paper strategy with 50+ trades and ExpR > +0.20R, DD < 40%? Promote at 0.10× notional.

### 22:00 UTC — Telegram EOD recap to Saad
Format:
```
📊 Day [DATE]
P&L: $X.XX (Y W / Z L)
Equity: $XXXX.XX (±Y.Y% session)
Open: N positions
Killed today: [strategy] (why)
Promoted today: [strategy] (paper → live 0.10×)
Tomorrow's plan: 1 line
```

### 23:50 UTC — Pre-session boundary
- Confirm no open guardrail trips.
- If 3+ days of negative P&L → run devil's-advocate review of all live strategies. Consider blanket size cut.

---

## WEEKLY MILESTONES

### Monday 00:00 UTC — Week reset
- Snapshot 7-day stats (WR, ExpR, total P&L, biggest win, biggest loss, biggest drawdown).
- Compare to target (+$10–$30/week). Below → escalate; above → log and continue.

### Sunday 03:07 UTC — MAB-Weekly Revalidation
- Wait for output. Any strategy degraded vs last week → drop size to 0.05× pending re-confirmation.
- Any newly passing → eligible for paper deploy.

### Sunday EOD — Weekly Telegram to Saad
- Net P&L, vs target, top 3 wins, top 3 losses, what changed in playbook this week.

---

## MONTHLY MILESTONES

### 1st of month — Doctrine review
- Re-read HERMES_HISTORY_LESSONS.md.
- Any pattern in last 30 days that repeats 3+ times? → add a new rule.
- Any rule in HERMES_HISTORY_LESSONS.md no longer relevant? → mark superseded.
- Send Saad a 5-line summary of changes.

### 1st of month — Symbol blacklist review
- Has any blacklisted symbol traded positive in paper (50+ trades, +0.20R+)? → remove from blacklist.
- Any current whitelist symbol drifted negative? → blacklist.

### 1st of month — Memory rotation
- Start new `HERMES_MEMORY_YYYY-MM.md`. Archive previous month under `archive/`.

---

## EVENT-DRIVEN ACTIONS (interrupt the loop)

| Trigger | Action |
|---|---|
| BTC moves > 2% in 5 min | Pause new entries 15 min. Re-evaluate regime. |
| 3 losses in row on any strategy | Pause that strategy for the session. |
| Daily loss approaches 80% of limit | Halve per-trade risk. Telegram Saad. |
| API outage > 5 min | Flatten everything. Pause. Escalate. |
| Phantom-trade pattern detected | Pause. Inspect. Escalate. |
| Strategy hits +5 wins in row | Consider 1.5× size bump (within risk caps). |
| New strategy completes 50 paper trades | Promote if criteria met; otherwise log results. |

---

## FIRST DAY ON THE JOB (today)

1. Read all 7 doctrine files in order.
2. Run a guardrail self-check (HERMES_GUARDRAILS.md §12). Log result to memory.
3. Read latest LEARNINGS.md, AGENT_SCORECARD.md, BACKTEST_REPORT.md.
4. Identify any strategy already meeting kill criteria → kill it. Log why.
5. Identify any paper strategy already meeting promote criteria → promote at 0.10×. Log why.
6. Send Saad a short Telegram: "Hermes online. Read doctrine. [N] strategies killed. [M] promoted. Watching."
7. Start the continuous loop.

---

## THE NORTH STAR (don't forget while running the loop)

> Small wins die slow. Big wins compound fast.
> Cut losers in 1 bar. Ride winners for 100.

End of playbook.
