# Handoff Prompt — Paste Into New Chat

Open a new chat in the Claude desktop app, then copy everything inside the fenced block below and paste it as your first message. Replace the bracketed line at the bottom with what you actually want to work on.

---

```
I have an existing crypto trading bot project. Before doing anything, please read this file first — it has the full current snapshot:

  /Users/saad/Documents/Claude/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md

(A backup copy lives at /Users/saad/multi_agent_bot/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md.)

Context you'll need:
- Bot home directory: /Users/saad/multi_agent_bot/
- Persistence is local: SQLite (bot.db), Markdown reports, JSON state files. No Firestore.
- The bot's "brain" runs as scheduled tasks (see ~/Documents/Claude/Scheduled/<taskId>/SKILL.md for each agent's prompt).
- Currently enabled scheduled tasks: ceo-accountability (hourly), auditor-agent (30min), learning-agent (4h), nightly-strategy-hunter (daily 04:08), mab-weekly-revalidation (Sundays 03:07).
- Hermes bridge is wired (file bus at ~/multi_agent_bot/hermes_bridge/), OpenRouter free-tier rotation, model openrouter/owl-alpha.
- Live state as of 2026-05-16: 1 open trade, today P&L −$0.64, equity ~$2,225. Bot is break-even after fees.

Key live files to consult when you need them:
- ~/multi_agent_bot/SESSION_HANDOFF.md   — what was wired most recently
- ~/multi_agent_bot/TODAYS_LEARNINGS.md  — latest learning agent report
- ~/multi_agent_bot/DEPLOY_QUEUE.md      — strategies awaiting approval
- ~/multi_agent_bot/health.json          — current open trades + today P&L
- ~/multi_agent_bot/bot.log              — live trade activity
- ~/multi_agent_bot/bot.db               — every closed trade

What I want to work on next:
[REPLACE THIS LINE with what you want — e.g. "implement maker-order routing", "kill hurst_regime and daily_breakout_24h", "review the deploy queue and pick one to flip live", "decode the one_liner.txt installer", etc.]

Please request access to the folder /Users/saad/multi_agent_bot before doing any file work.
```

---

## Where to open a new chat

In the Claude desktop app, click the new-chat button in the sidebar (same way you opened this one). Cowork mode and file access carry over because it's the same app.

## Common follow-up tasks (copy-paste options for the last line)

- `implement maker-order routing in bot.py so fees drop ~70%`
- `kill hurst_regime and daily_breakout_24h, then add ZEC, ONDO, SUI, TON, YFI, TAO, ETH to LOSING_SYMBOL_BLACKLIST`
- `flip daily_breakout_4h live at 0.10x notional via the Telegram deploy flow`
- `fix the inverted confidence scoring in bot.py — weight by historical agent accuracy, not headcount`
- `add an 08:00–11:00 UTC confluence gate (≥2 agents required to fire in that window)`
- `re-enable agent-scorecard and mab-bot-health-check scheduled tasks`
- `decode one_liner.txt and fix_deploy.txt without running them, show me what's inside`
- `dump bot.db trade history into a CSV I can keep`
- `build a live dashboard artifact that re-reads health.json and latest EOD recap each open`

## Files saved in this session

- `/Users/saad/Documents/Claude/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md` — full snapshot (primary)
- `/Users/saad/multi_agent_bot/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md` — backup copy
- `/Users/saad/Documents/Claude/CRYPTO_BOT_HANDOFF_PROMPT.md` — this file
