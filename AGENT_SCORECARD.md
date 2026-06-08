# Agent Scorecard — 2026-05-01 05:09 UTC

Run window: last 7 days of `bot.log` (effective span: 2026-04-28 23:50 → 2026-05-01 06:07 UTC, ~2.3 days).
Live roster: 10 agents (every class in `bot.py` with `paper_only = False` explicitly set).

| Agent | Signals | Fills | PnL ($) | Avg/trade | Status |
|---|---|---|---|---|---|
| trend_pullback | 0 | 0 | $0.00 | — | 🟡 |
| daily_breakout | 0 | 0 | $0.00 | — | 🟡 |
| daily_breakout_24h | 0 | 0 | $0.00 | — | 🟡 |
| daily_breakout_4h | 0 | 0 | $0.00 | — | 🟡 |
| daily_breakout_7d | 0 | 0 | $0.00 | — | 🟡 |
| supertrend | 0 | 0 | $0.00 | — | 🟡 |
| volume_capitulation | 0 | 0 | $0.00 | — | 🟡 |
| asian_pump | 0 | 0 | $0.00 | — | 🟡 |
| pump_dump_reversal | 0 | 0 | $0.00 | — | 🟡 |
| macd_cross | 0 | 0 | $0.00 | — | 🟡 |

## Live duration (since DEPLOY warning in log)

| Agent | Deployed (UTC) | Time live | 48h freeloader threshold |
|---|---|---|---|
| trend_pullback | 2026-04-29 21:11:11 | 32h 58m | not yet (15h to go) |
| daily_breakout_4h | 2026-04-30 23:16:39 | 6h 53m | no |
| daily_breakout_24h | 2026-04-30 23:17:44 | 6h 51m | no |
| daily_breakout | 2026-04-30 23:18:25 | 6h 51m | no |
| daily_breakout_7d | 2026-04-30 23:18:46 | 6h 50m | no |
| supertrend | 2026-05-01 04:33:18 | 1h 36m | no |
| asian_pump | 2026-05-01 04:33:41 | 1h 35m | no |
| macd_cross | 2026-05-01 04:34:08 | 1h 35m | no |
| volume_capitulation | 2026-05-01 04:35:16 | 1h 34m | no |
| pump_dump_reversal | 2026-05-01 04:35:27 | 1h 34m | no |

## Notes & methodology choices (autonomous run)

- **Live roster** was identified by grepping `paper_only = False` in `bot.py`. The base `Agent` class also has `paper_only = False` but it is not a tradable subclass; ten concrete agent classes explicitly opt in to live trading.
- **Signal counting**: scanned `bot.log` for `OPEN {agent}/{profile}` (the format produced at `bot.py:2733`) and for the agent's `name` string in any signal-context line. None of the ten live agent names appear in any OPEN line.
- **What did fire**: the only OPEN lines in the window are 7 × `tradingview/momentum` and 3 × `tradingview/meanrev` — these are inbound TradingView webhook signals, not native agent firings, and are out of scope for this scorecard.
- **Fills**: no live agent had an OPEN, so fill_rate is undefined. No `order rejected` lines were found anywhere in the log.
- **CLOSE / PnL**: only one CLOSE in the window — `BTC-USDT long pnl=$+0.43 reason=reconcile_sync` on 2026-04-30 23:28:02. It was a reconcile-sync close on a TradingView-originated position, not attributable to any of the ten agents being scored, so it is excluded from per-agent PnL.
- **Status calls**: by the literal rubric, 🔴 requires either 0 signals over 48h+ OR consistently negative PnL. No agent has been live ≥48h yet (trend_pullback is the only one close at ~33h), and no agent has any PnL — so no 🔴 flags this run. None meet the ≥1 signal/72h bar for 🟡 either, but with 0 PnL (not negative) and live time still inside the grace window, 🟡 ("quiet but earning, ±$0") is the most defensible classification. Re-run in ~16h and trend_pullback will cross the 48h freeloader line if it stays silent.

## Watchlist for next run

1. **trend_pullback** — crosses the 48h zero-signal line at ~2026-05-01 21:11 UTC. Top candidate to flip 🔴 next run.
2. **daily_breakout family** (4 agents) — all hit 48h around 2026-05-02 23:17 UTC. If still silent, expect a quad-flag.
3. The five 0.05x-notional agents deployed 04:33–04:35 today have plenty of runway; revisit on 2026-05-03.

## Freeloader candidates (live > 48h, 0 signals)

None this run.
