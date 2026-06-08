# MAB Trading + Infinity Lux + OpenClaw — Full System Status

Last updated: end of this Cowork session.

---

## 🟢 TRADING BOT (multi_agent_bot)

**Status:** Running. ~26 LIVE agents trading real money on BloFin.

**Equity:** ~$2,225 (varies hourly)

**Position cap:** Max 5 concurrent. Min $50 notional per trade.

### What you'll see on Telegram (only these):
- 🚀 OPEN — real fill on BloFin
- 📉 CLOSE — exit with PnL
- ❌ REJECTED — rare now (precision bugs fixed)
- 🛡 Anti-revenge lockout — paused after 2 losses
- 🎯 *I have found a new trade!* — CEO deploy proposal (reply YES)
- 🚨 EMERGENCY — account drop > $50
- 🔍 Error scan (every 30 min)
- 🦞 OpenClaw 2-hour learning report (one-time)

### How to manage it
```
~/multi_agent_bot/d              # list all agents + status
~/multi_agent_bot/d AGENT 0.05   # deploy at 5% notional
~/multi_agent_bot/d -k AGENT     # kill (undeploy)
```

### Logs (when something feels wrong)
```
tail -f ~/multi_agent_bot/bot.log              # live bot activity
cat ~/multi_agent_bot/CEO_LOG.md               # CEO decisions
cat ~/multi_agent_bot/AGENT_SCORECARD.md       # per-agent stats
cat ~/multi_agent_bot/LEARNINGS.md             # daily insights
cat ~/multi_agent_bot/self_healer.log          # auto-restart history
cat ~/multi_agent_bot/error_detective.log      # error patterns
```

---

## 🤖 SCHEDULED TASKS (running 24/7)

### Trading bot:
- `ceo-accountability` — every hour at :12, makes decisions
- `nightly-strategy-hunter` — daily 04:08, full backtest
- `weekly-revalidation` — Sunday 03:00
- `hourly-strategy-lab` — every 30 min, generates variants
- `learning-agent` — daily 03:00, extracts patterns
- `agent-scorecard` — every 6h, ranks agents (currently disabled)
- `self-healer` — every 5 min, auto-restart bot
- `error-detective` — every 30 min, surfaces new errors
- `telegram-deploy-responder` — every 1 min, fires deploy on YES
- `deep-learning-session-2hr` — one-time research (already completed/scheduled)

### Infinity Lux:
- `infinity-lux-daily-outreach` — Mon-Fri 09:00, 8 cold emails
- `infinity-lux-inbox-responder` — every hour
- `infinity-lux-followup-agent` — Monday 10:00
- `infinity-lux-leads-hunter` — Sunday 08:00
- `infinity-lux-25day-plan` — every 3 hours
- `infinity-lux-social-content` — daily, 3 social drafts
- `infinity-lux-inbox-responder` — weekday 18:00 reply log

---

## 🦞 OPENCLAW

**Status:** Updated to 2026.5.3-1, doctor cleaned, model = `moonshotai/kimi-k2`

**Action item:** Top up OpenRouter credit at https://openrouter.ai/credits — it's currently out of balance which causes the billing error you saw.

**Dashboard:** http://127.0.0.1:18789/ (NOT just 127.0.0.1)

### To extend OpenClaw to your website
See: `~/multi_agent_bot/infinity_lux_concierge_setup.md`

That file has:
- OpenClaw agent setup commands
- A drop-in chat widget HTML for your website
- ngrok exposure instructions
- Where to paste the widget per platform

---

## 🛟 IF SOMETHING BREAKS

### Bot stops trading
1. Check: `tail ~/multi_agent_bot/bot.log` — see latest errors
2. Self-healer should restart it within 5 min
3. Manual restart: `touch ~/multi_agent_bot/.restart_trigger`

### Telegram stops sending alerts
1. Check trading bot still running (above)
2. Check `~/multi_agent_bot/.env` has `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`
3. Test: `python3 ~/multi_agent_bot/test_telegram.py`

### OpenClaw web UI blank
1. Open http://127.0.0.1:18789/ (NOT 127.0.0.1)
2. If still blank: `openclaw doctor`
3. If billing errors: top up OpenRouter

### Account losing money
- CEO auto-kills any agent down >$10
- If account down >$50, you'll get 🚨 emergency telegram
- Manual emergency stop: close all positions on BloFin web → bot will reconcile

---

## 📁 KEY FILES

```
~/multi_agent_bot/
├── bot.py                    # Main trading bot (don't edit unless needed)
├── d                         # Deploy script
├── .env                      # Secrets (DON'T share)
├── bot.log                   # Trade activity
├── bot.db                    # Trade history (SQLite)
├── CEO_LOG.md                # CEO decisions
├── LEARNINGS.md              # Daily insights
├── BACKTEST_REPORT.md        # Backtest results
├── AGENT_SCORECARD.md        # Per-agent ranking
├── strategy_pool.json        # Generated strategy candidates
├── infinity_lux_concierge_setup.md   # Website chat setup
└── backups/                  # Code backups by date
```

---

## 💰 WHAT TO DO NEXT (priority order)

1. **Top up OpenRouter** — OpenClaw is broken without credit
2. **Verify outreach emails are good** — read today's `infinity-lux-daily-outreach` output
3. **Watch for Telegram fills** — bot should fire trades; if silent for 12h+ tell me
4. **Add chat widget to your website** — use `infinity_lux_concierge_setup.md`
5. **Don't add more automation right now** — let what's running prove itself first

---

End of status doc. Everything's running. Walk away.
