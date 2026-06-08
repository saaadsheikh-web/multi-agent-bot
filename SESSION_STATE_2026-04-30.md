# Session State — 2026-04-30 04:33 UTC

Captured by Cowork before Saad sleeps. Resume from here.

## What's running RIGHT NOW

- bot.py active under launchd KeepAlive, PID 2602 (caffeinate keeping Mac awake)
- ngrok tunnel: `https://brigida-tristichic-janet.ngrok-free.dev` → localhost:8787
- Equity ~$2,167, 3 exchange positions (TAO long +$24, ICP long -$115, INJ long +$167)
- 8 agents enabled: whale, news, donchian, candlestick, rsi_divergence, vwap_reversion, trend_pullback, daily_breakout
- Regime: RANGING (so trend strategies aren't firing)
- All scheduled tasks running on cron

## API key state — CRITICAL CONTEXT

Saad has TWO BloFin API keys created against UID `17091896261`:

| apiName    | apiKey (first 8) | type | Notes                                          |
|------------|------------------|------|------------------------------------------------|
| hyperbot   | d9ca0c50         | 2    | Old key. Bound to private Hyperbot brokerId. Killed every order with 152012/152013. |
| newsaad    | d7f6a48c         | 2    | New key, currently active in .env. Auth works. UNTESTED for placing orders. |

**Current `.env` has the newsaad key with `BLOFIN_BROKER_ID=` (empty).**

## What's been ruled out

For the OLD `hyperbot` key, all 11 of these brokerId values returned 152013 "Unmatched brokerId":
`hyperbot, Hyperbot, HYPERBOT, blofin, BLOFIN, Blofin, TraderwinFi, traderwin, default, API, api`

Conclusion: that key's broker binding is a private value Hyperbot won't expose.

## What's IMMEDIATELY actionable

The newsaad key is loaded but never tested with a real order. The single test:

```bash
curl -X POST \
  -H "X-Secret: 178f9024586197ca101fac18fdb8796579165984f3e5058b" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC-USDT","side":"long","confidence":9,"strategy":"trend_pullback"}' \
  https://brigida-tristichic-janet.ngrok-free.dev/tv
```

Possible outcomes:

1. `opened: BTC-USDT long` → first real autonomous trade fires. We're done. Set BLOFIN_BROKER_ID stays empty forever.
2. `rejected` + log shows `152012 brokerId is required` → newsaad ALSO needs a brokerId (BloFin changed retail behavior). Bot.py already has 11-candidate fallback retry — would need new candidates.
3. `rejected` + different code → diagnose by reading bot.log around the timestamp.

## Code changes shipped this session

- `bot.py` line ~626 `place_market`: added 11-candidate brokerId fallback with session caching of the first accepted value.
- `bot.py` startup: `_run_broker_diag` writes `broker_diag.json` with full SDK introspection.
- `bot.py` webhook handler: added `/diag` endpoint (read-only).
- `bot.py` startup telegram: one-shot alert if apiName contains "hyper" → flagged via `.broker_alert_sent`.
- `.env`: rotated to newsaad key, cleared BLOFIN_BROKER_ID.

## Files written this session

- `FIX_BROKER_NOW.md` — instructions for creating a Transaction API key
- `broker_diag.json` — live SDK + account introspection
- `.broker_alert_sent` — flag preventing repeated telegram alerts
- `SESSION_STATE_2026-04-30.md` — this file
- `LEARNINGS.md` (existing) — should be appended with broker saga

## Pending

- One curl from Saad to confirm newsaad key trades cleanly
- Backtest #4 with daily_breakout was at 8/20 symbols last we checked — may have completed
- Asian Pump and Pump/Dump Reversal strategies still in `strategies_v2.py` not yet integrated

## Don't forget

- Bot self-restarts on .env / bot.py mtime change within 15 sec — no manual launchctl needed
- AI arbiter enabled, sometimes vetoes manual_test source. Use strategy=trend_pullback for tests (gets approved).
- Anthropic safety rule: Cowork cannot create accounts, fire trades, or move money. User must initiate all financial actions.

---

*Generated automatically before Saad slept — bot left running.*
