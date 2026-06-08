# SESSION MEMORY — read this first next session
_Last updated: 2026-05-07 14:30 BST_

> **NEW SESSION INSTRUCTION FOR CLAUDE:**
> 1. Read this whole file first.
> 2. Read `WHY_LOSE_HOW_WIN_2026-05-07.md` for trade forensics.
> 3. Read `HOW_TO_SAVE_TOKENS.md` for token-saving setup.
> 4. Then ask Saad what he wants. Don't re-discover, don't re-grep, don't re-summarize bot.py.

## Saad's communication style — IMPORTANT
- Dyslexic. Short sentences. No walls of text.
- Wants paste-ready commands and code, NOT explanations.
- Wants content inline in chat (not via `cat`/`pbcopy`).
- One question at a time.
- He says "snd / dylacix / olama" — that's normal, not a typo to fix.

## Bot location
- Code: `/Users/saad/multi_agent_bot/bot.py`
- Log:  `/Users/saad/multi_agent_bot/bot.log`
- DB:   `/Users/saad/multi_agent_bot/bot.db`
- Pine: `/Users/saad/multi_agent_bot/MAB_Fib_786_Setup.pine`
- Env:  `/Users/saad/multi_agent_bot/.env`

## Current bot health (as of 14:30 BST 2026-05-07)
- Webhook: listening on `0.0.0.0:8787/tv` ✅
- Equity: **$3,530** (gained +$165.62 / +4.94% during fix session)
- Reload time: 14:21:55 UTC, no errors after
- All filters live: BAD_HOURS_UTC, DISABLED_AGENTS, AGENT_SYM_BLACKLIST
- DATA_DISABLED filter blocked 165 bad trades during session
- AI Arbiter chain: Ollama (OFF by default) → Claude SDK → OpenRouter

## TradingView webhook
- URL:    `https://brigida-tristichic-janet.ngrok-free.dev/tv`
- Secret: `178f9024586197ca101fac18fdb8796579165984f3e5058b`
- Secret is in **JSON body** (TV free tier = no custom headers).
- Bot accepts header OR body OR query.
- ngrok must point at `127.0.0.1:8787` (IPv4). `localhost` resolves to IPv6 → fails ERR_NGROK_8012.

## Bugs fixed across both sessions
1. Permanent revenge lockout → `recent_two_losses` with NOISE_THRESHOLD ($0.50) + WINDOW_HOURS (2h)
2. AI Arbiter silent auto-approve → returns None on error, falls through
3. Pine v6: `color.gold` undeclared → `#FFD700` hex
4. TV alerts: secret moved into JSON body (TV free tier)
5. Pine loosened: RSI 30/70 → 40/60, proximity 0.5%→1.0%, min swing 2.5%→1.5%
6. `tickers()` simplified — was passing bogus `instType=` kwarg, removed (12 sites)
7. Reconcile mass-fake-close protected — skip cycle if 0 exchange but 3+ DB open
8. IP-restricted symbols (102134) auto-added to `BloFin._bad_symbols_cache`
9. Claude SDK noisy logs silenced → loggers set to CRITICAL
10. Bot startup hang resolved via hard-kill + restart
11. **Ollama tier-1 arbiter added then DISABLED by default** (Saad: "Olama is very slow, will ruin trading")
    - Default `OLLAMA_URL=off` (opt-in only)
    - Hard timeout 3 seconds (was 8)
    - Default model `llama3.2:3b` (smaller/faster)

## Data-driven filters now live in `scan_once`
```python
BAD_HOURS_UTC      = {10, 11, 12, 13}        # net -$4.95 historic
DISABLED_AGENTS    = {"vwap_reversion"}      # net -$1.43
AGENT_SYM_BLACKLIST = {"connors_rsi2": {"TAO-USDT"}}
```

## Saad's pending todos (HIS action, not mine)
- **#46** Paste new Pine Script v2 into TradingView (Cmd+A, Delete, Cmd+V, Save)
- **#47** Set per-chart Symbol input: BTC-USDT, ETH-USDT, SOL-USDT, BNB-USDT
- Set `BLOFIN_BROKER_ID` in `.env` — get from blofin.com/account/apiManagement (orders rejected without it)
- **OPTIONAL:** install Ollama + add `OLLAMA_URL=http://127.0.0.1:11434` to `.env` if Mac is fast enough. Currently OFF.

## Performance snapshot (40-trade sample)
- Win rate: 60% • Profit factor: 1.21 • Total: +$2.19
- Best agent: `connors_rsi2` (23 trades, 52% WR, +$2.09) — KEEP, scale up
- Best symbols: ZEC +$3.83, CL +$2.10, GIGGLE +$1.70, BTC +$1.24 = 70% of profit
- Worst hours: 10/12/13 UTC = -$4.95 (filter now blocks these)
- Worst combo: TAO-USDT longs via connors_rsi2 = -$1.76 (now blacklisted)
- Math: filters alone push +$2.19 → ~+$10 over same trades = 5x

## Useful one-liners
```bash
# Restart bot (hot reload)
touch /Users/saad/multi_agent_bot/.restart_trigger

# Hard-kill + restart
pkill -9 -f "python.*bot.py" && cd /Users/saad/multi_agent_bot && nohup /opt/homebrew/Caskroom/miniconda/base/bin/python bot.py > bot.stdout.log 2>&1 &

# Test webhook
curl -X POST "https://brigida-tristichic-janet.ngrok-free.dev/tv" \
  -H "Content-Type: application/json" \
  -d '{"secret":"178f9024586197ca101fac18fdb8796579165984f3e5058b","symbol":"BTC-USDT","side":"long","confidence":9,"strategy":"fib_786_long","price":99999}'

# Check listener
lsof -nP -iTCP:8787 -sTCP:LISTEN

# Tail bot log
tail -50 /Users/saad/multi_agent_bot/bot.log

# Equity
sqlite3 /Users/saad/multi_agent_bot/bot.db "SELECT equity FROM equity_history ORDER BY ts DESC LIMIT 1"

# Last 20 trades
sqlite3 /Users/saad/multi_agent_bot/bot.db "SELECT symbol,side,agent,pnl,closed_at FROM trades WHERE status='closed' ORDER BY closed_at DESC LIMIT 20"

# Filter activity
grep -c "BAD_HOUR_SKIP\|DATA_DISABLED\|AGENT_SYM_SKIP" /Users/saad/multi_agent_bot/bot.log

# Restart ngrok if down
pkill -9 ngrok; nohup ngrok http 127.0.0.1:8787 > /tmp/ngrok.log 2>&1 &
```

## Files in `/Users/saad/multi_agent_bot/` worth knowing
- `bot.py` — primary bot (long, use Read with offset)
- `MAB_Fib_786_Setup.pine` — Pine v2 to paste in TradingView
- `WHY_LOSE_HOW_WIN_2026-05-07.md` — trade forensics
- `HOW_TO_SAVE_TOKENS.md` — token-saving + Ollama setup
- `SESSION_MEMORY.md` — this file
- `.env` — secrets (BloFin keys, broker ID, optional Ollama URL)
- `.restart_trigger` — touch to hot-reload bot

## DON'T re-do these things next session
- Don't re-grep bot.py to find `recent_two_losses` — it's already fixed.
- Don't re-explain BAD_HOURS_UTC filter — it's live, search log for `BAD_HOUR_SKIP`.
- Don't re-read full bot.py top-to-bottom — it's 8000+ lines. Use Grep/Read with offset.
- Don't re-discover the webhook URL — it's at top of this file.
- Don't suggest enabling Ollama — Saad explicitly asked it OFF. He'll re-enable if he wants.

## If bot stops working — first 4 things to check
1. `lsof -nP -iTCP:8787 -sTCP:LISTEN` — webhook listening?
2. `tail -100 /Users/saad/multi_agent_bot/bot.log` — recent errors?
3. `ps aux | grep bot.py | grep -v grep` — process alive?
4. `curl -s http://127.0.0.1:4040/api/tunnels | python -m json.tool` — ngrok up?
