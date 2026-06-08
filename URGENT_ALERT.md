# URGENT ALERT — Bot Health Check (read-only monitoring)

**Generated:** 2026-05-01T00:06Z (scheduled 4h health check)
**Action taken:** none — read-only monitoring task. No code, env, or trade changes.

## Why this is flagged

Per the health-check criteria, the following red flag is met:

> any [FATAL] or recurring [ERROR] in last 50 lines

The last 50 lines of `bot.log` contain three recurring error patterns that have been
repeating for **>24 hours** (first seen 2026-04-28 23:50, still occurring at the
latest log line 2026-05-01 01:04):

1. `[ERROR] tickers: PublicAPI.get_tickers() got an unexpected keyword argument 'instType'`
   — every minute. (Earlier in the log it was `'inst_type'`, now `'instType'`, suggesting
   a partial fix attempt that introduced a new kwarg-name mismatch.)
2. `[WARNING] candles BTC-USDT 1H: PublicAPI.get_candlesticks() got an unexpected keyword argument 'instId'. Did you mean 'inst_id'?`
   — every minute.
3. `[ERROR] positions: BloFinRequestException ... NameResolutionError ... 'openapi.blofin.com'`
   — every ~5 minutes. Looks like a DNS resolution failure rather than an API problem.

No `[FATAL]` entries in the file (`grep -c "[FATAL]" bot.log` = 0).

## What is OK

- **Bot is alive.** Most recent successful scan: `2026-05-01 01:04:50 [INFO] scan: 25 symbols regime: RANGING`.
  Equity tick: `equity=$2147.37 exch_positions=2 our_open=0 today_pnl=$+0.00`.
- **No daily-loss-limit risk.** today_pnl = $0.00 (just rolled from +$0.43). Far from -$30 warning / -$50 cap.
- **Open trades within cap.** our_open = 0 (cap is 5).

## Anomalies worth a closer look (no immediate action needed)

- **Scan cadence is intermittent.** Successful scans ran every ~60s from 00:00–00:13,
  then a 24-min gap, then every ~60s 00:37–00:49, then a 15-min gap, then 01:04.
  The bot recovers but is not running cleanly.
- **Position-tracking mismatch.** Logs show `exch_positions=2 our_open=0` consistently —
  the exchange shows 2 open positions that the bot is not tracking. Worth investigating
  whether those are stale, manual, or from a previous bot run that wasn't cleaned up.
- **`health.json` is stale.** Last update timestamp `2026-05-01T00:05:01.776093+00:00`
  (~1h before this check). `last_scan_at` and `last_monitor_at` are both `0`, and
  `scan_lag_s` / `monitor_lag_s` are also 0/-0 — suggests the health-writer task may
  not be updating these fields, or it's stuck.
- **News feeds failing.** `news fetch ... Cannot connect to host` for coindesk,
  cointelegraph, decrypt — same DNS pattern as the BloFin failure. Could indicate a
  network/DNS issue on the host, not the bot itself.

## Likely root cause

The recurring `instType` / `instId` kwarg errors look like a **BloFin SDK version
mismatch**: the installed SDK's `PublicAPI.get_tickers` / `get_candlesticks` now expect
`inst_type` / `inst_id` (snake_case) while the calling code is passing camelCase.
The DNS NameResolutionError for `openapi.blofin.com` and several news domains in the
same time window suggests an intermittent host networking issue, not a code issue.

## Telegram

Two messages sent to chat 950763287:
- regular 4h health update (msg id 305)
- URGENT red-flag notification (msg id 306)

## Reminder

Read-only run. No code changes. No `.env` changes. No agent flags flipped. No trades placed.
Saad should review the SDK kwarg naming and the host's DNS resolution when awake.
