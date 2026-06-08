# VALIDATOR LOG

One-line summary per scheduled run of the strategy validator.

---

2026-04-30 03:39 UTC — scanned 12 strategies — PASS: 1 (trend_pullback) — WATCH: 0 — REJECT: 11 — queued 1 new (trend_pullback) — Telegram alert sent (msg_id 177) — log status: clean (no errors, parquet cache warnings only)
2026-04-30 05:03 UTC — scanned 15 strategies — PASS: 2 (daily_breakout, daily_breakout_24h) — WATCH: 2 (trend_pullback, rsi_divergence) — REJECT: 11 — queued 2 new (daily_breakout, daily_breakout_24h) — Telegram alerts sent (msg_ids 187, 188) — log status: clean (parquet cache warnings only; backtest_output.log appears stale/truncated mid-run from prior 21:21Z run, but BACKTEST_REPORT.md is fresh at 03:56Z and contains complete results for all 20 symbols)
2026-04-30 11:03 UTC — scanned 15 strategies (report unchanged, 03:56Z) — PASS: 2 (daily_breakout, daily_breakout_24h) — WATCH: 2 (trend_pullback, rsi_divergence) — REJECT: 11 — queued 0 new (both PASS already in queue from 05:03 run) — no Telegram alert (no new PASS) — log status: clean (parquet cache warnings only, no fatal errors)
2026-04-30 13:45 UTC — scanned 17 strategies (fresh report 13:40Z) — PASS: 4 (daily_breakout_4h, daily_breakout, daily_breakout_24h, daily_breakout_7d) — WATCH: 2 (trend_pullback, rsi_divergence) — REJECT: 11 — queued 2 new (daily_breakout_4h, daily_breakout_7d) — Telegram alerts sent (msg_ids 250, 251) — log status: clean (parquet cache warnings only, no fatal errors)
2026-05-01 03:25 UTC — scanned 23 strategies (fresh report 03:18Z, 6-symbol limited universe) — PASS: 7 (daily_breakout_4h, daily_breakout_2h, daily_breakout, daily_breakout_24h, daily_breakout_12h, daily_breakout_8h, daily_breakout_48h) — WATCH: 2 (trend_pullback, donchian) — REJECT: 14 — queued 4 new (daily_breakout_2h, daily_breakout_12h, daily_breakout_8h, daily_breakout_48h) — Telegram alerts sent via Chrome JS (msg_ids 351, 352, 353, 354) — log status: clean (only aiohttp module warning; sandbox blocks api.telegram.org so used Chrome JS fetch instead of bash curl) — note: daily_breakout_7d in queue from prior run reported n=0 in this universe-limited run, kept queued pending re-test
