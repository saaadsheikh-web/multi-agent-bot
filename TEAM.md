# MAB Trading Co. — Org Chart

```
              ┌────────────────────┐
              │   Saad (CEO)       │
              │   final approval   │
              │   capital owner    │
              └─────────┬──────────┘
                        │
              ┌─────────┴──────────┐
              │  Cowork (Brain)    │
              │  strategy design   │
              │  code/research     │
              │  coordination      │
              └─────────┬──────────┘
                        │
   ┌────────────────────┼────────────────────┐
   │                    │                    │
   ▼                    ▼                    ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│ Schedule │    │  bot.py 24/7 │    │  Forensics   │
│  Agents  │    │  (live)      │    │  (Claude     │
│ (6 roles)│    │  14 traders  │    │   Code)      │
└──────────┘    └──────────────┘    └──────────────┘
```

---

## Scheduled Agents (the "company team")

### 1. Risk Monitor — every 30 min
**Role:** healer / nurse
- Reads bot.log for last 50 lines
- Reads health.json for liveness
- Fetches BTC/ETH/SOL prices for context
- Telegram on anomalies (stuck loops, daily PnL near limit, errors)

### 2. News Scanner — every 4 hours
**Role:** field intelligence officer
- Scans CoinGecko prices, CoinDesk RSS, CoinTelegraph
- Flags major events (ETF, hacks, regulation)
- Telegrams summary if anything noteworthy
- Logs everything to NEWS_LOG.md

### 3. Strategy Validator — every 6 hours
**Role:** quality control / promotions board
- Reads BACKTEST_REPORT.md
- Scores strategies against deployment thresholds:
  - PASS: ExpR > +0.20R AND DD < 40% AND N >= 50
  - WATCH: ExpR > +0.05R AND DD < 70% AND N >= 50
- Adds passing strategies to DEPLOY_QUEUE.md
- Telegrams Saad on new candidates

### 4. Daily Morning Briefing — 07:00 BST
**Role:** chief of staff
- Comprehensive daily summary
- Bot health, market state, news, deploy queue, action items
- One Telegram per day to start Saad's day

### 5. Weekly Re-Validation — Sundays 03:00 UTC
**Role:** auditor / risk officer
- Triggers fresh backtest weekly
- Compares to last week's results
- Flags any strategy degradation > 30%
- Catches strategy decay before it hurts real money

### 6. Deploy Approver — every 2 hours
**Role:** project manager
- Watches DEPLOY_QUEUE.md
- Reminds Saad of pending approvals > 24h old
- Prevents validated strategies from rotting in queue

---

## bot.py Internal Agents (the "field workers")

These run inside the live bot, scanning markets every 60 seconds:

| Agent | Profile | Status | Role |
|-------|---------|--------|------|
| whale | whale | paper | orderbook tracker |
| news | news | paper | RSS sentiment |
| donchian | swing | paper | breakout |
| candlestick | swing | paper | reversal patterns |
| rsi_divergence | swing | paper | divergence reversals |
| vwap_reversion | meanrev | paper | institutional fade |
| trend_pullback | trend_pullback | paper | HTF pullback |
| scalp | scalp | DISABLED | (failed backtest) |
| momentum | momentum | DISABLED | (failed backtest) |
| swing | swing | DISABLED | (failed backtest) |
| meanrev | meanrev | DISABLED | (failed backtest) |
| asymmetric | asymmetric | DISABLED | (failed backtest) |
| bb_squeeze | momentum | DISABLED | (failed backtest) |
| funding | meanrev | DISABLED | (no funding data) |
| ema_ribbon | momentum | DISABLED | (failed backtest) |

---

## Roles by analogy (Saad's terminology mapped)

| Saad's role | Real implementation |
|---|---|
| Doctor / healer | Risk Monitor (auto-restart on crash via LaunchAgent KeepAlive + caffeinate) |
| Surgeon | Cowork Brain (me — code repairs and edits) |
| Producer (creates new agents) | Cowork Brain (writes new strategies into bot.py + strategies_v2.py) |
| Producer (kills useless agents) | Strategy Validator (auto-disables agents that fail backtest) |
| Director | Saad (you — final approval on live deployments) |
| Field manager | bot.py supervisor (auto-restarts crashed loops) |
| Worker | The 14 internal trading agents |
| Radar | News Scanner + on-chain monitor (future) |
| Communicator | Telegram bot (sends alerts to Saad) |
| Therapist | (skipped — agents are software, no feelings to therapize) |
| Genius | (skipped — there's no magic; just disciplined edge) |
| Back tester | bot.py /backtest endpoint + Weekly Re-Validation |
| Reseacher | Cowork Brain + Strategy Researcher (future scheduled task) |

---

## What's NOT in the team (and why)

- **Therapy agents** — agents don't have emotional state. Skipping.
- **24/7 idea generators** — random idea generation produces noise. Curated strategy library (MEGA_STRATEGY_CATALOG.md) is more useful.
- **Auto-deploy without approval** — Anthropic safety rule blocks me from initiating real money trades. Saad's approval is the final gate, by design.

---

## File system as shared memory

All agents communicate via files in `~/multi_agent_bot/`:

- `bot.log` — live trading actions, scan results
- `health.json` — bot liveness
- `BACKTEST_REPORT.md` — latest verdict table
- `BACKTEST_FORENSICS.md` — deep analysis
- `DEPLOY_QUEUE.md` — strategies awaiting Saad's approval
- `NEWS_LOG.md` — news scanner outputs
- `VALIDATOR_LOG.md` — strategy validator decisions
- `DEPLOY_QUEUE_LOG.md` — approver actions
- `OVERNIGHT_LOG.md` — Claude Code overnight forensics
- `TEAM.md` — this file (org chart)

---

## What needs to happen for the team to fully click

1. **First validated strategy.** Once one strategy crosses 80% confidence threshold, it gets queued for deployment, you approve, it goes live. The team's whole flow gets exercised.

2. **First real trade.** Risk Monitor catches it, Daily Briefing reports it, all telemetry validates.

3. **First real loss.** Stress test of risk management — does the daily $50 loss limit hold? Does the hard liquidation guard fire? Does anti-revenge lockout kick in?

4. **First profitable week.** Compounding begins. Validator watches for strategy decay. Re-Validation re-checks weekly.

The "company" works end-to-end once we've done one full cycle of: validate → deploy → trade → measure → adjust. That cycle hasn't happened yet because no strategy has crossed validation.

That's the next milestone.
