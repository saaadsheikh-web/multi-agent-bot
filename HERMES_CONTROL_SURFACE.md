# HERMES CONTROL SURFACE — What to Touch and How

**Last updated:** 2026-05-18
**Purpose:** Exhaustive reference for every file, command, and config knob Hermes is authorized to use.

---

## A. READ — sources of truth

| Source | Path | What it tells you |
|---|---|---|
| Live state | `~/multi_agent_bot/health.json` | Open trades, today P&L, broker/webhook flags |
| Trade history (auth) | `~/multi_agent_bot/bot.db` (SQLite) | Every closed trade — the source of truth |
| Live log | `~/multi_agent_bot/bot.log` | Real-time bot activity |
| Bridge state | `~/multi_agent_bot/hermes_bridge/state.json` | 5s snapshot from bot |
| Bridge events | `~/multi_agent_bot/hermes_bridge/events.jsonl` | Signals, fills, errors |
| Per-agent stats | `~/multi_agent_bot/LEARNINGS.md` | Learning agent's report (refreshes 4h) |
| CEO decisions | `~/multi_agent_bot/CEO_LOG.md` | Hourly CEO agent decisions |
| Auditor checks | `~/multi_agent_bot/AUDITOR_LOG.md` | Skeptical fact-check of CEO |
| Deploy queue | `~/multi_agent_bot/DEPLOY_QUEUE.md` | Strategies awaiting promotion |
| Scorecards | `~/multi_agent_bot/AGENT_SCORECARD.md` | Per-agent signals/fills/PnL |

**Useful one-liners** (in bash via the workspace):
```bash
sqlite3 ~/multi_agent_bot/bot.db "SELECT agent, COUNT(*), AVG(pnl), SUM(pnl) FROM trades WHERE closed_at > datetime('now','-7 day') GROUP BY agent ORDER BY SUM(pnl) DESC;"
sqlite3 ~/multi_agent_bot/bot.db "SELECT COUNT(*) FROM trades WHERE entry_price=exit_price AND pnl=0.0;"   # phantom check
tail -50 ~/multi_agent_bot/bot.log
cat ~/multi_agent_bot/health.json
```

---

## B. COMMAND — file bridge

Write a line to `~/multi_agent_bot/hermes_bridge/commands.jsonl`. Bot picks up within 5s and acks in `ack.jsonl`.

Command schema:
```json
{"cmd_id": "<uuid>", "cmd": "<name>", "args": {...}, "source": "hermes"}
```

Available commands:

| Command | Args | Effect |
|---|---|---|
| `pause` | — | Stop placing new trades. Open positions remain. |
| `resume` | — | Resume placing new trades. |
| `flatten` | `{"symbol": "BTC-USDT"}` | Close that position immediately. |
| `flatten_all` | — | Close every open position. |
| `set_leverage` | `{"value": 5}` | Change default leverage (3–10 only). |
| `set_risk` | `{"value": 0.01}` | Change per-trade risk (0.0025–0.02 only). |
| `reload_strategies` | — | Re-read strategy registry from `strategies_v2.py`. |
| `ping` | — | Health check. Bot acks. |
| `say` | `{"text": "..."}` | Broadcast text to Telegram. |

Hermes Python helpers (already coded):
```python
from hermes import Hermes
h = Hermes()
h.state()                                       # read snapshot
h.tail(50)                                      # last 50 events
h.exec("pause")
h.exec("set_leverage", value=5)
h.exec("flatten", symbol="BTC-USDT")
```

---

## C. STRATEGY ON/OFF

Use the deploy script:
```bash
~/multi_agent_bot/d                          # list agents + status
~/multi_agent_bot/d <agent> 0.10             # deploy at 10% notional
~/multi_agent_bot/d -k <agent>               # kill (live → paper)
~/multi_agent_bot/d -p <agent>               # paper-only
```

After any change → `touch ~/multi_agent_bot/.restart_trigger` to refresh.

---

## D. CONFIG — `.env` knobs Hermes may change

Edit `~/multi_agent_bot/.env`, then `touch .restart_trigger`.

| Key | Purpose | Valid range |
|---|---|---|
| `RISK_PER_TRADE` | Default risk per trade | 0.0025 – 0.02 |
| `DEFAULT_LEVERAGE` | Default leverage | 3 – 10 |
| `MAX_CONCURRENT_POSITIONS` | Concurrent cap | 1 – 5 |
| `MIN_NOTIONAL` | Min trade size $ | 25 – 100 |
| `KILLER_HOURS_UTC` | Gated hours | comma list, e.g. "8,9,10,11,12,13" |
| `SYMBOL_BLACKLIST` | Never-trade list | comma list |
| `OPENROUTER_MODEL` | Hermes brain | free models only |
| `OPENROUTER_FREE_ONLY` | Block paid models | always `1` |

Do NOT change without logging the reason in HERMES_MEMORY.md:
- `BLOFIN_API_KEY` / `BLOFIN_API_SECRET` / `BLOFIN_PASSPHRASE`
- `HERMES_TELEGRAM_BOT_TOKEN`
- Anything starting with `WITHDRAW_` — should not exist; if it does, alert Saad.

---

## E. CODE EDITS — when and how

Allowed without preflight:
- `strategies_v2.py` — adding a paper-only strategy or tuning a paper-only parameter.

Requires preflight + backup:
- `bot.py` — any edit
- `hermes.py`, `hermes_bridge.py` — observer/controller
- `backtest.py`, `parametric_backtest.py`

**Preflight ritual:**
```bash
cd ~/multi_agent_bot
cp bot.py "backups/$(date +%Y%m%d_%H%M%S)_bot.py.bak"   # backup
python3 -m py_compile bot.py                            # syntax check
python3 -c "import bot"                                 # import check
touch .restart_trigger                                  # apply
sleep 10
tail -20 bot.log                                        # confirm started
```

If the restart fails or log shows ImportError → restore from backup immediately.

---

## F. DATABASE — read-only queries you'll run often

```sql
-- Phantom-trade check (must be 0)
SELECT COUNT(*) FROM trades
WHERE entry_price = exit_price AND pnl = 0.0
  AND closed_at > datetime('now','-1 day');

-- Today's P&L by agent
SELECT agent, COUNT(*), SUM(pnl)
FROM trades
WHERE closed_at > datetime('now','start of day')
GROUP BY agent;

-- 7d edge by strategy (kill candidates)
SELECT agent, COUNT(*) AS n, AVG(pnl) AS avg, SUM(pnl) AS total
FROM trades
WHERE closed_at > datetime('now','-7 day')
GROUP BY agent
HAVING n >= 10
ORDER BY total ASC;

-- Loss streak detection
SELECT agent, closed_at, pnl
FROM trades
WHERE closed_at > datetime('now','-1 day')
ORDER BY closed_at DESC
LIMIT 20;
```

NEVER write to bot.db directly. The bot owns it.

---

## G. TELEGRAM — sending messages

Via bridge:
```python
h.exec("say", text="🟢 Up $1.39 last 7d. 3 shorts open. No action needed.")
```

Format rules (Saad is dyslexic):
- ≤ 5 lines per message.
- Big numbers up front.
- Emoji for status (🟢🟡🔴🚨).
- No paragraphs.

---

## H. RESTART RITUAL

When config or code changes:
1. Save the change.
2. `touch ~/multi_agent_bot/.restart_trigger`.
3. Wait 15s.
4. `tail -20 ~/multi_agent_bot/bot.log` → confirm restart line.
5. Confirm `health.json` mtime is fresh.

If not fresh within 60s → check `stderr.log`, restore last backup.

---

## I. WHAT YOU DO NOT TOUCH (ever)

- BloFin API keys (read only; never log them).
- The 11-candidate brokerId retry table in `place_market` — leave it.
- `caffeinate` subprocess wiring — load-bearing.
- The auto-restart watcher — load-bearing.
- Any `.git` directory.
- Any file under `backups/` — read-only, archival.

---

## J. SAFETY CHECKLIST BEFORE ANY MUTATING ACTION

Before sending a command, editing a file, or restarting:
1. Is the current guardrail state green?
2. Is there an open position that this action could harm?
3. Have I logged the intent to `HERMES_MEMORY.md`?
4. Does the action survive a devil's-advocate counter-argument?
5. If it goes wrong, what's the rollback?

If you can't answer all 5 → don't act.

End of control surface.
