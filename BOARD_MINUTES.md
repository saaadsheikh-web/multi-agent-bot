# Board Minutes — MAB Trading Co.

Bridgewater-style partner reviews. Tactical and quant. Appended each scheduled run.

---

## Board Meeting — 2026-05-04 23:58 UTC

### Performance (last 5h, bot-only)

- **Bot PnL (real closes only): +$0.44** — single trailing-stop close on `hurst_regime` BTC-USDT long at 19:52:27 UTC.
- **Trades: 1 real (1W / 0L)**, plus 5 `reconcile_sync` zero-PnL bookkeeping closes at 20:19:10 (XAUT, XAU, BTCDOM, TAO, BTC) — bot reconciled stale state with the exchange after a connectivity gap; not signal-driven, excluded from win/loss math.
- **Trades opened in window: 0.** 25-symbol scans produced 26-43 raw signals each tick, but every candidate hit a `REGIME_SKIP` (TRENDING regime filtering vwap_reversion + swing) or a `DISABLED_SKIP` (ema_ribbon, momentum agents disabled by backtest). The bot is alive and scanning, just gated.
- **Realized R:R:** single +0.79% trailing exit on a >0% setup — call it ~+1R. Insufficient sample for meaningful R:R math this window.
- **Equity drift:** $2284.54 → $2227.53 over the window (−$57). This is **manual position attribution** (7 manual exch_positions held, 0 bot_open most of the window). Bot-only `today_pnl` per `health.json` = **−$1.74** for the calendar day.

#### Per-agent (5h, real closes only)
| Agent | Trades | Wins | PnL |
|---|---|---|---|
| hurst_regime | 1 | 1 | +$0.44 |
| (all others) | 0 | 0 | $0.00 |

#### Lifetime running tally (sorted)
| Agent | n | PnL | Win% |
|---|---|---|---|
| hurst_regime | 9 | +$1.12 | 44% |
| tradingview | 1 | +$0.43 | 100% |
| daily_breakout_2h | 1 | +$0.14 | 100% |
| daily_breakout_4h | 1 | −$0.65 | 0% |
| daily_breakout_24h | 3 | −$0.93 | 0% |
| connors_rsi2 | 7 | −$1.44 | 43% |

**Best trade:** hurst_regime BTC-USDT long +$0.44, trailing_stop, 79bp move on Hurst H=0.94 trend-regime confirmation.
**Worst trade:** None this window. Lifetime worst remains connors_rsi2 ZEC-USDT long −$1.87 on 2026-05-04 10:23 (out of window).
**Kill flag (>$5 cumulative):** None. connors_rsi2 closest at −$1.44 lifetime.

### Market Context

- **BTC regime:** TRENDING (per bot scan, 25 symbols, every tick this window).
- **Spot:** BTC ~$78,975 → high $80,393 — first $80k print since Jan 31, reclaimed bull-market support band.
- **Macro driver:** Trump responded to Iran's 14-pt peace proposal + US to escort vessels through Strait of Hormuz. Crude −5%, risk-on. Geopolitical de-escalation removed a Q1 macro headwind.
- **Forward catalysts:** Powell's last day as Fed Chair May 15; Warsh confirmation vote week of May 11. Both rate-policy events, both vol-positive.
- **Funding / RSI extremes:** Not exposed in current scan output. **Research action item — wire funding > 0.04% and RSI >75/<25 alerts into the scan summary line.**
- **Big-shot candidates:** None visible in current bot scan output. Cannot screen 24h movers >15% from this log alone — needs a market-wide pull. Research note for next meeting.

### Operational Health — RED FLAG

52 ERR lines in the 5h window. Two distinct failure modes:
1. **BloFin API DNS unreachable** — `NameResolutionError` on `openapi.blofin.com:443` for `positions`, `balance`, `close-position`. Caused the 5 stale closes that needed `reconcile_sync` cleanup. Network-layer issue (VPN/DNS/routing) — Saad to investigate.
2. **`PublicAPI.get_tickers()` signature break** — `unexpected keyword argument 'instType'`. This is a wrapper/SDK version mismatch in `bybit_wrapper.py` or equivalent. Every tickers call is failing. **This may explain the 0-opens window** if scan price-data reads are broken.

Neither qualifies for autonomous action under this charter (code edit forbidden), but **both block trading.**

### Big-Shot Candidates

None this window. Need 24h winner/loser screen wired in to surface these — current scan only shows 25 fixed-symbol roster. Promoting to research backlog.

### Decisions

- **EXECUTED:** None. No agent crossed the −$10 undeploy threshold (worst is connors_rsi2 at −$1.44). Status quo on the roster.
- **PROPOSED TO SAAD:** None. No new candidate in `strategy_pool.json` has a backtest meeting Sharpe ≥3 / ExpR ≥0.20R / Trades ≥50 — every entry shows `trades: 0, sharpe: 0` (pool generated but never re-run against data after seeding on 2026-05-01). Cannot propose a deploy on empty backtests.
- **NO TELEGRAM SENT.** Bot-only PnL drawdown (−$1.74 today) is not anywhere near the $50 emergency threshold. Total equity drift is manual-position attribution and out of scope.

### Research Notes (for next meeting)

1. **Bot is gated, not broken (signal-side).** TRENDING regime is filtering vwap_reversion + swing every tick; `ema_ribbon` and `momentum` are universally `DISABLED_SKIP`'d by backtest. With BTC trending up and 5 days of clean BTC long bias from `hurst_regime`, **evaluate biasing the live roster toward trend-followers** (hurst_regime, daily_breakout_2h, tradingview) and pulling capital from connors_rsi2 (mean-reversion in a trending tape — wrong-regime, lifetime −$1.44 / 7 trades).
2. **Re-run the strategy_pool backtests.** All 14+ candidates in `strategy_pool.json` show `trades: 0` from a 2026-05-01 seeding pass — they are not promotion-ready. The deploy pipeline is starved until backtests are repopulated against real recent OHLCV.
3. **BloFin reachability + tickers SDK mismatch** is a P1 ops issue. The bot is scanning but cannot reliably close positions or read tickers. Saad: confirm `pip install bybit/blofin` versions match the wrapper, and check egress/DNS to `openapi.blofin.com`.
4. **Wire 24h-mover screen into scan output** — current `scan:` log line shows agent learning summaries but no symbol-universe context (top movers, RSI extremes, funding outliers). Big-shot opportunities are invisible to this meeting otherwise.
5. **Bias check for next meeting:** if BTC holds $80k and Iran headlines stay constructive, lean LONG bias and tighten short-side filters. If Warsh-vote uncertainty re-introduces macro chop, expect TRENDING → VOLATILE flip and vwap_reversion comes back online.

### Tone Check

Status quo. No actions warranted. The single +$0.44 win and the ops flags are the entire signal from this window.

---

## Board Meeting — 2026-05-05 00:01 UTC

**Cadence note:** This run fired ~3 minutes after the prior meeting (23:58 UTC). Same 5h window, materially same data. Treating this as a delta-only entry against prior minutes.

### Performance (last 5h, bot-only)

- **Bot PnL: +$0.44** (unchanged). Same single trailing-stop close on `hurst_regime` BTC-USDT long at 19:52:27 UTC.
- **Trades closed since prior meeting: 0.** No new opens or closes between 23:58 and 00:01.
- **Lifetime tally unchanged:** hurst_regime +$1.12 (9, 44%w), connors_rsi2 −$1.44 (7, 43%w). No agent crosses watch ($5) or kill ($10) threshold.
- **Equity drift:** $2231 → $2220 over the prior-meeting window (−$11), all manual-position attribution. Bot-only `today_pnl` = −$1.74, holding flat.

### Delta — what's new since prior meeting

1. **`fibonacci` (FibonacciRetracementAgent) flipped LIVE at 23:46:06 UTC** — `paper_only=False, notional=0.05`. This is a Saad-button deploy that happened **before** prior meeting was logged but was not captured in those minutes. Roster now has a new live agent. Notional 0.05 = ~$5/trade, low blast radius. **Watch first 10 trades.**
2. **`daily_breakout_4h` ZEC-USDT LONG at 23:17:11 was REJECTED by exchange** — `code 102016: Precision does not match: 0.01`. Bot logged `OPEN ... size=2.0 notional=$87.0` but the BloFin order rejected on lot-size precision. **No actual position opened**, no orphan risk, but the bot's "OPEN" log line is misleading — it should log only after exchange confirmation. Bug, not exposure.
3. **Multiple bot restarts (23:43–23:48 UTC)** triggered by agent registration changes (fibonacci added, then `paper_only` flip). Each restart re-loads `agents enabled` list. Last restart settled the live roster.
4. **UTC rollover:** we crossed into 2026-05-05 mid-meeting. `today_pnl` will reset on next bot tick. Anchor for tomorrow's 5h windows.

### Market Context

Unchanged from prior meeting. Regime TRENDING (ADX 27.3, ATR 553). BTC ~$80k, risk-on tilt on Iran de-escalation. No new macro print in last 3 min.

### Big-Shot Candidates

None this window. Same as prior — 24h-mover screen still not wired in.

### Decisions

- **EXECUTED:** None.
- **PROPOSED TO SAAD:** None. Strategy pool still has 0 candidates with `trades > 0` in their backtest stub. Cannot promote on empty math.
- **NO TELEGRAM SENT.** No emergency, no qualifying deploy candidate, no big-shot opportunity.

### Research Notes (for next meeting)

1. **`OPEN` log timing bug** — `bot.py` logs `OPEN ... size=...` before the exchange confirms the order. ZEC-USDT was a precision-rejection, not a real fill. Fix: log only after the order-create response returns success, or add a `REJECTED` follow-up line that's easy to grep. **Affects every "OPEN" line as ground truth for trade audit.**
2. **ZEC-USDT lot-size precision** — `daily_breakout_4h` computed `size=2.0` but BloFin requires `0.01` precision step. Either the symbol's `lotSize` metadata is stale in the bot's universe config, or the position-sizer is rounding wrong. One-line fix once Saad pulls fresh BloFin instrument metadata.
3. **Watch fibonacci** — first live trade hasn't fired yet. Track WR / R:R for first 10 trades; trim if it goes underwater past −$5 like the connors_rsi2 watch.
4. **Connors_rsi2 still drifting in trending tape** — same as prior meeting's research note. If next 5h window adds another connors_rsi2 loss, propose tightening it to RANGING/VOLATILE only (mirror of `vwap_reversion` and `swing` regime filters) at the meeting after that.
5. **Carry-over from prior meeting:** BloFin DNS/SDK ops issues unresolved (P1, Saad-action), strategy_pool needs backtest re-population, 24h-mover screen needs wiring.

### Tone Check

Status quo, no actions warranted. Three new datapoints (fibonacci live, ZEC precision rejection, restart cluster) — all logged for next meeting's trend check, none actionable under this charter.

---
