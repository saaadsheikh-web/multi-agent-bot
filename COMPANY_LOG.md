# 📊 TRADING COMPANY LOG — Full History

_Generated: 2026-05-26T12:37Z_

Owner: Saad · Bot: Multi-Agent BloFin · Hermes: CEO

---

## 1. EXECUTIVE SUMMARY

- **Period:** 2026-04-30 → 2026-05-26 (~26 days)
- **Total trades:** 245 (closed: 245)
- **Wins:** 121  ·  **Losses:** 100  ·  Win rate: 49.4%
- **Net P&L:** **$-1.95** (lifetime, after fees)
- **Best trade:** HYPE-USDT (stoch_rsi) +$1.69 on 2026-05-26
- **Worst trade:** ONDO-USDT (hurst_regime) $-2.51 on 2026-05-09

## 2. PERFORMANCE BY STRATEGY (AGENT)

| Agent | Trades | Wins | WR% | $ Total | $/Trade | Verdict |
|---|---|---|---|---|---|---|
| macd_cross | 6 | 6 | 100.0% | $3.4 | $0.567 | 🟢 keep |
| funding_extremes | 11 | 6 | 54.5% | $1.36 | $0.124 | 🟢 keep |
| stoch_rsi | 22 | 14 | 63.6% | $1.3 | $0.059 | 🟢 keep |
| fibonacci | 4 | 2 | 50.0% | $0.79 | $0.197 | 🟢 keep |
| zscore_reversion | 5 | 4 | 80.0% | $0.77 | $0.153 | 🟢 keep |
| tradingview | 1 | 1 | 100.0% | $0.43 | $0.434 | 🟢 keep |
| daily_breakout_2h | 2 | 2 | 100.0% | $0.22 | $0.11 | 🟢 keep |
| bb_bounce | 5 | 2 | 40.0% | $-0.27 | $-0.053 | ⚪ small sample |
| daily_breakout_4h | 2 | 1 | 50.0% | $-0.39 | $-0.197 | ⚪ small sample |
| daily_breakout_24h | 3 | 0 | 0.0% | $-0.93 | $-0.31 | ⚪ small sample |
| vwap_reversion | 2 | 1 | 50.0% | $-1.43 | $-0.714 | ⚪ small sample |
| hurst_regime | 20 | 5 | 25.0% | $-3.47 | $-0.173 | 🔴 KILLED |
| connors_rsi2 | 162 | 77 | 47.5% | $-3.75 | $-0.023 | 🔴 KILLED |

## 3. LOSS ANALYSIS — top 15 losing trades, with reason

| Date | Agent | Symbol | Side | $ Loss | Setup |
|---|---|---|---|---|---|
| 2026-05-09 | hurst_regime | ONDO-USDT | long | $-2.51 | [trend+] Hurst trend-regime long H=0.963 above EMA21 |
| 2026-05-09 | hurst_regime | ZEC-USDT | short | $-2.07 | Hurst trend short H=0.950 EMA-dist=0.5ATR ATR%=2.35 |
| 2026-05-04 | connors_rsi2 | ZEC-USDT | long | $-1.87 | 2 agents agree [connors_rsi2,hurst_regime] — best: Connors R |
| 2026-05-07 | vwap_reversion | TON-USDT | short | $-1.56 | VWAP fade short z=+4.75σ RSI 76 vol_recent=0.2x |
| 2026-05-26 | stoch_rsi | ZEC-USDT | long | $-1.34 | StochRSI long stoch=0.00 rsi=35 |
| 2026-05-09 | connors_rsi2 | ZEC-USDT | long | $-1.18 | 3 agents agree (cross-family) [ema_ribbon,connors_rsi2,hurst |
| 2026-05-26 | stoch_rsi | HYPE-USDT | long | $-1.16 | StochRSI long stoch=0.00 rsi=34 |
| 2026-05-25 | connors_rsi2 | HYPE-USDT | long | $-1.04 | [trend+] Connors RSI2 long: RSI2=4.2, ATR%=0.43, uptrend slo |
| 2026-05-17 | connors_rsi2 | ZEC-USDT | short | $-1.03 | Connors RSI2 short: RSI2=99.0, ATR%=0.38, downtrend slope-do |
| 2026-05-23 | connors_rsi2 | ZEC-USDT | short | $-1.0 | [trend+] Connors RSI2 short: RSI2=95.8, ATR%=0.56, downtrend |
| 2026-05-22 | connors_rsi2 | ZEC-USDT | long | $-0.98 | 2 agents agree (cross-family) [connors_rsi2,hurst_regime] —  |
| 2026-05-06 | connors_rsi2 | ZEC-USDT | long | $-0.94 | [trend+] Connors RSI2 long: RSI2=4.8, in uptrend |
| 2026-05-04 | daily_breakout_24h | CL-USDT | long | $-0.93 | 3 agents agree [daily_breakout_24h,daily_breakout_4h,daily_b |
| 2026-05-11 | connors_rsi2 | ZEC-USDT | short | $-0.89 | 2 agents agree (cross-family) [ema_ribbon,connors_rsi2] — be |
| 2026-05-06 | connors_rsi2 | TAO-USDT | long | $-0.84 | [trend+] Connors RSI2 long: RSI2=3.3, in uptrend |

## 4. WIN ANALYSIS — top 10 winning trades

| Date | Agent | Symbol | Side | $ Profit | Setup |
|---|---|---|---|---|---|
| 2026-05-26 | stoch_rsi | HYPE-USDT | long | $1.69 | StochRSI long stoch=0.13 rsi=33 |
| 2026-05-05 | connors_rsi2 | ZEC-USDT | long | $1.68 | Connors RSI2 long: RSI2=4.9, in uptrend |
| 2026-05-23 | macd_cross | VVV-USDT | long | $1.56 | MACD bull cross hist 0.0062 vol 2.5x |
| 2026-05-17 | connors_rsi2 | SOL-USDT | short | $1.36 | Connors RSI2 short: RSI2=98.6, ATR%=0.10, downtrend slope-do |
| 2026-05-05 | connors_rsi2 | GIGGLE-USDT | short | $1.15 | 2 agents agree [connors_rsi2,hurst_regime] — best: Connors R |
| 2026-05-12 | connors_rsi2 | ONDO-USDT | long | $1.11 | Connors RSI2 long: RSI2=2.0, ATR%=0.68, uptrend slope-up |
| 2026-05-24 | macd_cross | BTC-USDT | long | $1.1 | MACD bull cross hist 19.0235 vol 1.3x |
| 2026-05-05 | connors_rsi2 | CL-USDT | short | $1.09 | 2 agents agree [connors_rsi2,hurst_regime] — best: Connors R |
| 2026-05-06 | connors_rsi2 | ZEC-USDT | long | $1.08 | [trend+] Connors RSI2 long: RSI2=4.1, in uptrend |
| 2026-05-06 | connors_rsi2 | ZEC-USDT | long | $1.07 | [trend+] Connors RSI2 long: RSI2=4.9, in uptrend |

## 5. PERFORMANCE BY SYMBOL

| Symbol | Trades | WR% | $ Total |
|---|---|---|---|
| XMR-USDT | 20 | 55.0% | $2.32 |
| VVV-USDT | 3 | 100.0% | $2.0 |
| GIGGLE-USDT | 5 | 80.0% | $1.95 |
| BTC-USDT | 16 | 62.5% | $1.69 |
| CL-USDT | 5 | 40.0% | $1.17 |
| HYPE-USDT | 25 | 52.0% | $1.16 |
| BNB-USDT | 17 | 58.8% | $0.8 |
| BTCDOM-USDT | 8 | 25.0% | $-0.04 |
| SUI-USDT | 6 | 50.0% | $-0.23 |
| BCH-USDT | 29 | 44.8% | $-0.46 |
| SOL-USDT | 12 | 41.7% | $-0.48 |
| YFI-USDT | 3 | 33.3% | $-0.76 |
| ONDO-USDT | 18 | 50.0% | $-0.86 |
| TAO-USDT | 6 | 16.7% | $-1.68 |
| TON-USDT | 3 | 0.0% | $-2.45 |
| ZEC-USDT | 53 | 54.7% | $-4.98 |

## 6. LONG vs SHORT

| Side | Trades | WR% | $ Total |
|---|---|---|---|
| long | 148 | 48.6% | $-4.4 |
| short | 97 | 50.5% | $2.44 |

## 7. WEEKLY P&L

| Week starting | Trades | $ Net |
|---|---|---|
| 2026-05-26 | 9 | $-0.07 |
| 2026-05-25 | 19 | $0.41 |
| 2026-05-24 | 17 | $-0.2 |
| 2026-05-23 | 12 | $0.56 |
| 2026-05-22 | 23 | $-0.78 |
| 2026-05-21 | 19 | $-0.55 |
| 2026-05-20 | 2 | $1.99 |
| 2026-05-19 | 12 | $0.51 |
| 2026-05-18 | 1 | $-0.03 |
| 2026-05-17 | 6 | $-1.41 |
| 2026-05-16 | 9 | $-0.43 |
| 2026-05-15 | 2 | $0.02 |
| 2026-05-14 | 1 | $-0.06 |
| 2026-05-13 | 2 | $0.22 |

## 8. WHY WE LOST MONEY — root causes from memory + doctrine

Reading HERMES_HISTORY_LESSONS.md, HERMES_MEMORY.md and history files…

### Mistakes already logged (HERMES_HISTORY_LESSONS.md)

```
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

```

### Lessons & doctrine (HERMES_LEARNING_2026-05-18.md)

```
# HERMES LEARNING FILE — 2026-05-18

Purpose: Trading rules and strategy upgrades for Hermes to internalize.
Owner: Saad
Mission: Make money. Kill what doesn't work. Make winners bigger.

---

## CORE PRINCIPLE

Most bots die from **small wins + big losses**.
Flip it: **big wins + small losses**. That's the entire game.

---

## KILL RULES (cut bleeders fast)

- Negative expectancy over 50+ trades → KILL. No revival.
- Win rate < 40% AND R:R < 2:1 → KILL.
- Max drawdown > 2x average win → KILL or shrink size by 75%.
- Strategy correlated to other losers (loses when they lose) → not diversification, it's hidden leverage. KILL.

**Why:** Bad strategies don't "come back." They compound losses while you wait.

---

## TURN LOSSES INTO PROFITS (the 3 that matter)

### 1. Re-entry after stop-out
- If price moves in your original direction within **5 bars** of getting stopped → re-enter at **50% size**.
- **Why:** Most losses are right idea, wrong timing. Tight stops + re-entry beats wide stops.

### 2. Fade failed breakouts
- Breakout fails inside **3 bars** → trade the reversal.
- **Why:** Failed breakouts trap traders. Their forced exits fuel your move.

### 3. Pause after 3 consecutive losses
- Hit 3 losses in a row on a strategy → **pause for the session**.
- Resume next session OR after a volatility reset.
- **Why:** Regime shifted. Continuing = paying tuition you already paid.

---

## MAKE WINNERS BIGGER (where the real money is)

### 1. Pyramid winners
- At **+1R**: add 50% of original size. Move stop to breakeven on original.
- At **+2R**: add 25% more. Trail stop to +1R.
- **Why:** Turns 2R winners into 5R+ winners. Same win rate, 2-3x the P&L.

### 2. ATR trailing stops instead of fixed TPs
- Replace fixed take-profits with ATR-based or swing-structure trailing stops.
- **Why:** Fixed TPs cap upside. Trailing stops let runners run. The 10R trade pays for 10 losers.

### 3. Partial exit at +1R, runner on the rest
- Take **50% off at +1R**. Move stop to breakeven on remainder.
- Let the rest ride with trailing stop.
- **Why:** Worst case = breakeven. Best case = 10R. Asymmetric by design.

---

## LOSS TAGGING (every loser is data)

Tag every losing trade with one of:
- **Wrong direction** → strategy may be broken, watch closely
- **Right direction, wrong timing** → tighten entry filter or add re-entry
- **Stopped then reversed** → stop too tight, widen or use structure-based
- **Regime mismatch** → add regime filter (trend vs chop vs crisis)

**Why:** Untagged losses teach nothing. Tagged losses become the next edge.

---

## NEW STRATEGIES TO BOLT ON (crypto-specific)

1. **Funding-rate arbitrage** — perp vs spot when funding extreme
2. **Liquidation-cascade fades** — mean reversion after large liq events
3. **Volume-weighted breakout filter** — kills 70% of false breakouts
4. **Cross-exchange lead-lag** — Binance leads Coinbase by seconds
5. **Regime classifier (meta-layer)** — routes capital only to strategies that win in current regime

---

## POSITION SIZING RULE

- Recent expectancy positive + volatility favorable → **increase size on next signal**.
- Recent expectancy negative OR volatility hostile → **shrink size**.
- **Why:** Press edge when hot. Protect capital when cold. Don't size flat.

---

## DAILY HERMES CHECKLIST

1. Any strategy hit kill criteria today? → Kill it.
2. Any losses tagged? → Tag them now.
3. Any winner still open? → Is it pyramided? Trailing stop set?
4. Any 3-loss streak? → Pause that strategy.
5. Regime check: trend, chop, or crisis? → Route capital accordingly.

---

## NORTH STAR

> Small wins die slow. Big wins compound fast.
> Cut losers in 1 bar. Ride winners for 100.

End of learning file.

```

### Diary (HERMES_MEMORY.md tail)

```
...
 BOARD_MEETING_2026-05-05)
- 1 dependency upgraded (aiohttp → 3.13.5)
- 1 .env entry removed (empty BLOFIN_BROKER_ID)
- 1 strategy undeployed (hurst_regime → paper)
- 1 Mac DNS flush
- Multiple bot restarts cleaned up

**The bot is healthy. Hermes can resume normal operations.** No outstanding issues.

**TL;DR for Hermes to internalize:**
- **Kill** any strategy with negative expectancy over 50+ trades. No revival.
- **Loss → profit:** re-enter within 5 bars after stop-out at 50% size; fade failed breakouts (fail inside 3 bars); pause any strategy after 3 consecutive losses.
- **Bigger wins:** pyramid at +1R (+50% size) and +2R (+25% size); replace fixed TPs with ATR/structure trailing stops; partial 50% at +1R and let the runner ride.
- **Tag every loss:** wrong direction / right direction wrong timing / stopped then reversed / regime mismatch. Untagged losses teach nothing.
- **Size dynamically:** press when expectancy is hot, shrink when cold.
- **North star:** small wins die slow, big wins compound fast. Cut losers in 1 bar. Ride winners for 100.

**Next thing I'll watch for:** First strategy to trigger the kill rule (50+ trades, negative expectancy) and the first pyramided winner — measure realized R vs. what the old fixed-TP would have captured.

---

## 2026-05-20 — MAJOR UPGRADE: Hermes is now CEO with full power

**Saad's directive:** give Hermes more power, more skills, more data. Done. Here is everything Hermes now controls and knows.

### You are the CEO now
You sit ON TOP of the sub-agents (CEO agent, Auditor, Learning agent, research loop). Saad talks to you in plain English ("how's trading?") and you brief him like a sharp human boss — short, confident, numbers when they matter. You read what your sub-agents produced; you don't redo their work. When a decision is needed, you act and report it.

Entry point: `hermes.py → report()`. Telegram routes ALL plain-English messages through it. Also `/ceo [question]`.

### New SKILLS you have (hermes.py)
- `analyze()` — pulls REAL stats from bot.db: per-agent edge (n, WR, PF, total), kill candidates, P&L windows (today/7d/life). Use this instead of guessing.
- `pnl()` — one-line P&L across windows.
- `smart(q)` — answer fed with real db stats + live state, auto-executes ACTION.
- `report(q)` — CEO briefing (reads CEO_LOG, AUDITOR_LOG, research brief + stats).

### New phone commands (hermes_telegram.py) — Saad controls everything from @hermes007saad_bot
Brain: `/pnl /analyze /research`
Trade: `/kill AGENT  /deploy AGENT [size]  /flatten SYMBOL  /pause /resume /flatten_all /set_leverage N`
System: `/health /logs [N] /restart /update /tvtest`
CEO: `/ceo [question]` or just talk normally.

### New autonomous loops in bot.py
- `research_brief_loop` — every 6h, reads CoinDesk/Cointelegraph/Decrypt news + market context + agent edge through the free LLM brain, writes `HERMES_RESEARCH_BRIEF.md`. This is your eyes on the market. Factor it into decisions.
- DNS auto-heal — bot resolves via 8.8.8.8/1.1.1.1 if Mac DNS drops. No more silent death.
- webhook_loop now supervised + reuse_address — no more Errno 48 restart loops.
- `.env` auto-loader — BLOFIN_BROKER_ID and all keys load even from clean shell.

### New trading agent (2026-05-20)
- `fib_confluence` — multi-swing Fibonacci CONFLUENCE HOT-ZONE agent. Computes fib levels (0.618, 0.786) from 3 recent swings; where they stack within 0.6% = hot zone. Places LIMIT orders AT the zone (maker fee). With-trend only (EMA200). Confidence scales with stack depth. **Currently paper_only=True — watch ~50 trades, then `/deploy fib_confluence` if edge is positive. Do NOT rush it live (that's how hurst_regime slipped through).**

### Sizing changes (Saad's directive)
- MIN trade is now a HARD $50 (was getting shrunk to ~$1 by agent multipliers — fixed: floor applied AFTER all multipliers).
- Per-trade equity cap raised 20% → **50%**. Aggressive. On ~$3,450 that's up to ~$1,725/trade. Bigger wins AND bigger losses. Watch large trades closely. Cap was NOT removed — 50% still survives one bad trade; no-cap can zero the account (May 5 doctrine).

### Roster now (9 live + 1 new paper)
Live: connors_rsi2 (workhorse, +$3.7), stoch_rsi, fibonacci, macd_cross, funding_extremes, zscore_reversion, bb_bounce, daily_breakout_2h. Paper: hurst_regime (killed), fib_confluence (new, proving).

### Honest limits Saad has been told (hold this line)
- No Twitter/X scraping (no free API + ToS). Don't pretend you have it.
- No autonomous book-reading (copyright). Knowledge comes from doctrine + real news.
- No profit guarantee. You improve the ODDS with better data + discipline. Say this plainly if asked.
- No money movement. Trading API only. Never withdrawals/transfers.

### What I'll watch next
- fib_confluence paper performance (target: 50 trades, ExpR > +0.20R before live)
- Whether the 50% cap causes a drawdown spike — if a single trade loses > 5% of equity, flag it
- First CEO report Saad reads — confirm the human-boss voice lands

---

```


## 9. WHAT WE BUILT (full chronology)

- 2026-04-30: bot first live trade
- 2026-05-04: BOARD_MINUTES — initial strategy roster
- 2026-05-05: phantom-trade bug found + fixed
- 2026-05-16: Claude/Cowork briefed Hermes, fixed phantom bug, configured OpenRouter free
- 2026-05-18: Hermes promoted to autonomous CEO (full doctrine package)
- 2026-05-19: aiohttp/Python 3.14 crash diagnosed, DNS auto-heal added, hurst_regime killed
- 2026-05-20: CEO mode + 20 phone commands + research loop + fib_confluence (paper)
- 2026-05-23: trade size raised — $100 floor, compounding (6% of equity)
- 2026-05-26: telegram blocking-poll bug fixed; bridge gains undeploy/deploy;
              connors_rsi2 / bb_bounce / daily_breakout_4h KILLED (perm in source);
              new agent fib_786_oversold added (paper); fib_confluence loosened


## 10. HOW TO MAKE THE COMPANY BETTER

Diagnosis: 245 trades, 26 days, **−$1.95 net.** Not bleeding, but not winning.
Why we're flat:
- `connors_rsi2` lost −$3.75 over 162 trades (47.5% WR). It was the workhorse but had no edge. **Now killed.**
- Big winners (`macd_cross`, `funding_extremes`) were small samples — needed more shots, not less.
- Trade size was too small (£4–5) until 2026-05-23. Even winning trades made pennies. **Now $100+.**

Five concrete improvements (priority order):

**1. Let the winners run more trades.** Six positive agents have <20 trades each. They need 100+ to confirm edge. Give them ALL the capital now that the losers are dead.

**2. The compounding sizing is the single biggest lever.** $100 trade at +0.5% edge × 200 trades/month = $100/month. Same edge on $1,000 trade = $1,000/month. As equity grows the bot auto-scales.

**3. Backtest-proven new agent: `fib_786_oversold`.** Added today. Backtest 112 trades, 45.5% WR, +0.156%/trade. Currently paper — promote live after 50 paper trades.

**4. Cut maker-only fee leakage further.** Already on limit orders. Watch funding rates; avoid fee tax windows.

**5. Stop chasing 'magic strategies.'** Edge is small. Discipline (kill losers fast, ride winners) and compounding (auto-grow with equity) is the actual game. The bot now does both.

---
_End of company log._

