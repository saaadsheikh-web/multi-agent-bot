# HERMES HISTORY LESSONS — Mistakes We Already Made

**Last updated:** 2026-05-18
**Purpose:** Every loss has a story. Hermes reads this on boot so we never repeat the same mistake twice.
**Sources:** SESSION_REPORT_2026-05-16, CRYPTO_BOT_FULL_SNAPSHOT, WHY_LOSE_HOW_WIN_2026-05-07, LEARNINGS, PROFIT_LOSS_FORENSICS, OVERNIGHT_LOG.

---

## THE 10 MISTAKES THAT COST US REAL MONEY

### Mistake #1 — Trusting stats without checking for phantom trades
**What happened (May 16):** `reconcile_sync` was marking trades CLOSED with $0 P&L when BloFin returned an empty position list. 17 phantom closes polluted per-agent stats. `hurst_regime` looked like a 25% WR loser when its real WR was 80%.
**Cost:** Almost killed a winning strategy on bad data.
**Rule:** Any stat that looks extreme — verify against bot.db row-by-row. Filter out `entry_price=exit_price AND pnl=0.0`.

### Mistake #2 — Fees ate ~100% of the gross edge
**What happened (May 5 doc):** Pre-fee +$2.33 across 35 trades. After taker fees (0.06% × 2): −$0.18 to +$1.08. Break-even, not profitable.
**Cost:** Months of "profitable" backtests delivering nothing live.
**Rule:** Maker orders only on entries (limit at top-of-book). Reject any strategy with stops < 1.5% on this venue.

### Mistake #3 — Confidence scoring is inverted
**What happened:** Conf-10 trades (highest conviction) LOST −$0.01/trade on 23 trades. Conf ≤7 trades (low conviction) WON +$0.74/trade on 3 trades.
**Cost:** Sizing up high-conf trades increased losses, not profits.
**Rule:** Never size by raw confidence. Weight by historical agent accuracy. Until fixed, treat conf-10 as a yellow flag, not green.

### Mistake #4 — Trading the London open chop (08:00–13:00 UTC)
**What happened:** Hours 08:00–11:00 UTC bled −$6.86 across 19 trades. Hours 10–13 UTC alone = −$4.95 (more than total profit).
**Cost:** Killer hours wiped out the rest of the day's gains.
**Rule:** Hard gate. No new trades in 08:00–13:00 UTC unless ≥2-agent confluence AND BTC vol within 1× ATR average.

### Mistake #5 — Cutting winners too fast (tight trail in first 30 min)
**What happened:** Trades held 5–30 min lost −$3.69 avg. Same patterns held 30 min–2 hr won +$4.83. We trail-stop in normal MFE retracement.
**Cost:** Killed our own best trades.
**Rule:** Trail stop 1.5% in first 30 min, tighten to 0.8% after. Let winners breathe through normal retrace.

### Mistake #6 — Counter-trend longs in downtrending symbols
**What happened:** TAO-USDT longs via `connors_rsi2` = 3 losses, −$1.76. TAO trends DOWN; mean-reversion long is the wrong setup. YFI same pattern −$0.78.
**Cost:** ~$2.50+ across just two symbols.
**Rule:** EMA200 / regime filter. Block longs when symbol is in confirmed downtrend on 4H. Block shorts when in confirmed uptrend.

### Mistake #7 — One bad agent quietly bleeding
**What happened:** `vwap_reversion` = 2 trades, −$1.43. Faded a real TON pump that kept pumping. `daily_breakout_24h` = 3 trades, 0% WR, −$0.93.
**Cost:** Two agents responsible for ~30% of all losses.
**Rule:** Auto-kill: 50+ trades AND negative expectancy → disabled. < 50 trades AND −0.5R avg over ≥10 trades → paper-only.

### Mistake #8 — Longs vs shorts edge ignored
**What happened:** Shorts = 48 trades, 45.8% WR, +$0.63. Longs = 71 trades, 46.5% WR, **−$3.29**. The bleed is on the long side.
**Cost:** Long bias = structural loss in current regime.
**Rule:** When BTC daily trend is down or sideways → short bias. Cut long position-size to 50% until regime confirms uptrend.

### Mistake #9 — Sizing up at break-even
**What happened (May 5 analysis):** Doubling trade size ($87 → $200) just scales fees linearly. Break-even stays break-even, fees grow.
**Cost:** Would've burned capital faster.
**Rule:** Never increase size before edge is proven positive (50+ trades, ExpR > +0.20R, post-fee). Then scale 1.5× max per step.

### Mistake #10 — High leverage with tight liquidation
**What happened (May 5 doc):** 30× leverage = liquidation at ~3.3% adverse move. Worst single trade was −2.27%. A 3.5% wick wipes the account.
**Cost:** Catastrophic risk for zero P&L benefit (leverage doesn't change % returns).
**Rule:** Max leverage 10×. Default 5×. Liquidation distance must be ≥ 2× max single-trade loss in last 30 days.

---

## OPERATIONAL MISTAKES (NON-TRADING)

### #11 — The brokerId saga (April 30)
Three BloFin keys with different broker bindings. `hyperbot` key needed a private brokerId we couldn't guess. Burned hours.
**Rule:** If `apiName` looks like a 3rd-party product, it's a Broker key. Tell Saad to create a fresh Transaction key.

### #12 — Mac sleep killed the bot
**Rule:** `caffeinate -dimsu` spawned as bot subprocess in `main()`. Never trust the OS toggle.

### #13 — ngrok interstitial + Telegram link preview = accidental deploy
Telegram fetched a deploy URL for link preview, fired the deploy.
**Rule:** Any control URL must require POST + secret. No GET-only triggers.

### #14 — Multiple agents Telegram-spamming Saad
**Rule:** One alert per event. Coalesce within 60s window. Saad is dyslexic and tired.

### #15 — n<5 false kills/promotes
**Rule:** Minimum sample size before any kill, deploy, or size change: 50 trades for live, 200+ for backtest. Below that, log only.

---

## STRATEGIES THAT STRUCTURALLY DON'T WORK (don't keep tuning them)

- 15m bar momentum with tight stops — fee drag kills it
- 5m mean-reversion in trending markets — gets steamrolled
- 3:1 RR with ATR-tight stops — TP rarely hit on lower TF
- Multi-confluence breakouts on 15m — over-fitted
- Order book whale tracking — too easily spoofed
- Counter-trend longs in falling markets
- vwap_reversion on momentum pumps

If a strategy is on this list, it's not "broken pending fix." It's structurally wrong for this venue and size. Don't revive it.

---

## STRATEGIES THAT ACTUALLY WORK (do more of these)

- **connors_rsi2** + with-trend bias + 30 min – 2 hr hold = our engine. 23 trades on the May 7 sample, 52% WR, +$2.09. Strongest base.
- **Higher timeframes (1H+) + wide stops + trailing exit + regime filter** — `trend_pullback` and `daily_breakout` family.
- **Shorts in down/sideways regimes** — 63% WR on the May 7 sample.
- **bb_bounce, macd_cross** — small samples but 100% WR so far, watch closely.

---

## TOP SYMBOLS BY HISTORICAL P&L (concentrate here)

Winners: GIGGLE-USDT (+$1.95), BTC-USDT (+$1.29), CL-USDT (+$1.17), XPT-USDT (+$0.71), DASH-USDT (+$0.39), BCH-USDT (+$0.27).

Blacklist: **ZEC, ONDO, SUI, TON, YFI, TAO, ETH** — loss-per-trade between −58% and −205% on the May 16 learning report. Do not trade these without per-strategy override.

---

## REGIME-BY-REGIME PLAYBOOK

| Regime | Long bias | Short bias | Strategies to favor | Strategies to pause |
|---|---|---|---|---|
| BTC uptrend (above 50d MA, ADX>20) | Full | Half | connors_rsi2, daily_breakout family, trend_pullback | hurst_regime, mean-revert shorts |
| BTC chop (ADX<20, BB squeeze) | Half | Half | bb_bounce, zscore_reversion, funding_extremes | All breakouts, all daily_breakout_* |
| BTC downtrend / crisis | Off | Full | connors_rsi2 shorts, macd_cross shorts | All longs, daily_breakout_24h |

---

## THE NORTH STAR (from Saad, May 18)

> Small wins die slow. Big wins compound fast.
> Cut losers in 1 bar. Ride winners for 100.

End of history file. Hermes — internalize this. Every loss above is a tuition payment we already made. Don't pay again.
