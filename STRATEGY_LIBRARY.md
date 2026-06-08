# Strategy Library

Reference for every strategy currently coded into the bot. For each: what it trades, when it works, when it breaks, and how confident I am in its edge.

This file is paired with `BACKTEST_FORENSICS.md` (which explains why the original backtest was misleading) and `BACKTEST_REPORT.md` (the actual numerical verdicts).

---

## How to read this doc

For every strategy I list:
- **Setup** — exact conditions that trigger an entry
- **Profile** — `tp/sl/trail/activate/max_hold` from `bot.py PROFILES`
- **Best regime** — when this strategy historically works
- **Failure mode** — the exact way this strategy bleeds money
- **Edge confidence** — my honest read: HIGH / MEDIUM / LOW / UNVALIDATED

Confidence is based on (a) the original backtest after correcting for the simulator bugs, (b) whether the setup is well-known in TA literature, and (c) my logical assessment.

---

## Original 11 strategies

### 1. Scalp (RSI extremes + volume + body confirm)
**Setup (5m):** RSI < 25 with volume > 1.8× avg + green body ⇒ long. Mirror for short.
**Profile:** TP 0.6%, SL 0.4%, trail 0.25%, activate 0.3%, max-hold 30 min
**Best regime:** RANGING, VOLATILE
**Failure mode:** Strong trends — every "oversold" reading just goes more oversold. Fees eat 0.12% per round-trip vs 0.6% target = thin margin.
**Edge confidence:** LOW. 35.5% WR but -0.41R avg in original BT. Even with corrected sim, the R:R is too tight for fee drag.

### 2. Momentum (EMA stack + MACD rising + RSI 50-72)
**Setup (15m):** EMA 9 > 21 > 50, MACD histogram rising, 50 < RSI < 72, price > EMA9 ⇒ long.
**Profile:** TP 3%, SL 1.2%, trail 1%, activate 0.8%, max-hold 6h
**Best regime:** TRENDING
**Failure mode:** Mean-reverting markets — every breakout fails back into the range.
**Edge confidence:** MEDIUM. 29.9% WR with 2.5:1 RR = breakeven before fees. With trailing stops + regime filter it should improve. Claude Code found break-even WR is 31.4% at 0.12% round-trip fees — momentum is 1.5% under that. Tightening entry to RSI 55-68 + volume gate likely closes the gap.

### 3. Swing (Bollinger tag + RSI extreme on 1h)
**Setup (1h):** Price ≤ lower BB × 1.005 with RSI < 38 ⇒ long. Mirror.
**Profile:** TP 4.5%, SL 2%, trail 2%, activate 1.5%, max-hold 24h
**Best regime:** RANGING
**Failure mode:** Strong trends — BB tags keep happening but never reverse.
**Edge confidence:** LOW originally (negative ExpR). Re-validating with trailing stops.

### 4. MeanReversion (RSI extreme + 3-bar move + BB tag)
**Setup (5m):** RSI < 22 + 3-bar move < -2% + price below lower BB ⇒ long.
**Profile:** TP 1.8%, SL 1%, trail 0.8%, activate 0.6%, max-hold 2h
**Best regime:** RANGING
**Failure mode:** Capitulation moves go further than 3 bars.
**Edge confidence:** LOW. 696 trades is too few to draw conclusions.

### 5. WhaleTracker (orderbook imbalance)
**Setup:** Order book bid/ask volume imbalance > 30% + recent volume spike + price impact.
**Profile:** TP 2%, SL 1%, trail 0.8%
**Best regime:** TRENDING, VOLATILE
**Failure mode:** Order books are easily spoofed by exchanges and bot farms — phantom liquidity vanishes the moment price approaches.
**Edge confidence:** LOW (UNVALIDATED in backtest because order book is live-only).

### 6. News (RSS sentiment scoring)
**Setup:** Pull CoinDesk/CoinTelegraph/Decrypt RSS every 15 min, score keywords (surge, hack, ETF, ban, partnership), trade the coins mentioned.
**Profile:** TP 2.5%, SL 1.2%, trail 1%
**Best regime:** any
**Failure mode:** RSS feeds are slow — by the time the bot reads "BTC ETF approved" the price has already moved 8%. Also: noisy keywords give false positives.
**Edge confidence:** LOW. Real news edge requires sub-second feeds (Bloomberg, news APIs with low latency).

### 7. AsymmetricBreakout (BB squeeze + 3+ confluences)
**Setup (15m):** BB width in bottom 15% of last 100 bars + breakout above 20-bar high + 3+ of (EMA stack, 2× volume, RSI 55-70, HTF 1h trend agrees).
**Profile:** TP 3× ATR, SL 1× ATR, trail 0.5× ATR, activate 2× ATR, max-hold 12h
**Best regime:** TRENDING
**Failure mode:** Per Claude Code's gate analysis: 22-23% actual WR vs ~28-30% break-even at 3:1 RR. The 3R target rarely hits on 15m bars before reversal. Stop at 1× ATR is too tight for normal 15m noise (0.8-1.2× ATR range).
**Edge confidence:** UNVALIDATED. Conceptually sound (squeeze breakouts are real). Claude Code recommends lowering TP to 2× ATR or doing partial close at 1.5× ATR + trail.

### 8. BollingerSqueeze (5m squeeze breakout)
**Setup (5m):** BB width in bottom 20% of last 100 bars + breakout + volume confirm + RSI confirm direction.
**Profile:** Momentum (TP 3%, SL 1.2%)
**Edge confidence:** LOW. Faster timeframe of asymmetric — same failure mode but more fee drag.

### 9. DonchianBreakout (1h channel break + volume)
**Setup (1h):** Price > 20-bar high with volume > 1.8× avg ⇒ long.
**Profile:** Swing (TP 4.5%, SL = 1× ATR)
**Best regime:** TRENDING
**Failure mode:** False breakouts in choppy markets. Whipsaws.
**Edge confidence:** MEDIUM. **The only original agent with positive ExpR (+0.026R)**. Claude Code's parameter sweep shows best at period=30, ATR_mult=2.0 → +0.052R ExpR. With trailing stops, likely improves further.

### 10. FundingHunter (funding-rate extremes)
**Setup:** When BloFin funding > 0.08% (longs paying shorts heavily, market crowded long), take SHORT. Inverse for negative.
**Profile:** MeanRev
**Edge confidence:** UNVALIDATED — backtest had no funding rate data feed (0 trades simulated).

### 11. EMARibbon (3-timeframe EMA align)
**Setup:** EMA 9>21>50 on 5m AND 15m AND 1h, plus RSI 50-75 ⇒ long.
**Profile:** Momentum
**Edge confidence:** LOW originally. Conceptually correct but fires too rarely to compound.

---

## NEW strategies added tonight (paper-only until validated)

### 12. CandlestickAgent (Japanese reversals at exhaustion)
**Setup (15m):**
- **Bullish:** Price < EMA50 × 0.985 (extended below), RSI < 38 (oversold), volume ≥ 1.3× avg, AND ONE OF:
  - Hammer pattern (small body, long lower wick ≥ 2× body, small upper wick)
  - Bullish engulfing (current green body fully engulfs prior red body)
  - Morning star (3-bar: long red → small body → long green closing > midpoint of bar 1)
- **Bearish:** mirror — price > EMA50 × 1.015, RSI > 62, with shooting star / bearish engulfing / evening star

**Why this should have edge:**
Japanese candlestick patterns are battle-tested over centuries of rice trading and modern markets. The key is they MUST appear at exhaustion zones — random hammers in the middle of a trend are noise. By gating on EMA50 distance + RSI extreme, we only count patterns that fire when sellers (or buyers) are demonstrably exhausted.

**Why standard backtest might still kill it:**
The patterns are inherently small-sample (only fire when both conditions align). Need walk-forward across many regimes to see if edge holds. Watch for: pattern fires correctly but reversal fails because the larger trend resumes. This is why we use SWING profile (4.5% TP, 2% SL) — gives the trade room to develop.

**Profile:** swing (TP 4.5%, SL 2%, trail 2%, activate 1.5%, max-hold 24h)
**Best regime:** RANGING and TRENDING (patterns work in both)
**Edge confidence:** UNVALIDATED. Will be backtested in next run.

### 13. RSIDivergenceAgent (price-RSI divergence at swing points)
**Setup (1h):**
- **Bullish divergence:** find two most recent swing lows in price (using 3-bar pivot detection on 30-bar window). If second swing has *lower price* but *higher RSI* (and second RSI < 45, first RSI < 40, and price has turned up at least 0.3% since swing low) ⇒ long.
- **Bearish:** mirror — second swing has higher price but lower RSI, both > 55/60 region.

**Why this should have edge:**
Divergence is one of the highest-conviction reversal signals in TA. The logic: price made a new low but momentum (RSI) didn't — meaning sellers are exhausted even though they pushed to a new low. This is mechanically distinct from "RSI is just oversold" which doesn't account for structure.

**Why standard backtest might still kill it:**
- Swing point detection is noisy with small N. Need parameter tuning (currently N=3 pivot lookback; could try N=5).
- Fires rarely — divergences only set up at meaningful turning points. Could be too few trades to be statistically meaningful.
- Trend continuations CAN have divergence and still continue trending (especially in strong markets).

**Profile:** swing (same as candlestick)
**Best regime:** RANGING and TRENDING
**Edge confidence:** UNVALIDATED. Backtest pending.

---

## My honest assessment of edge

After both my analysis and Claude Code's rigorous experiments:

**Currently has SOME edge:**
- Donchian breakout (only positive original ExpR; needs parameter optimization + trailing stops)

**Conceptually sound but parameter-sensitive:**
- Asymmetric breakout (lower TP needed)
- Momentum (tighten entry, add volume gate)

**Likely no edge regardless of tuning:**
- Scalp (R:R too thin for fees)
- Swing (negative across all configurations)
- MeanReversion (too few signals to validate)

**Untestable in backtest, theory-based:**
- Whale (orderbook gameable)
- News (RSS too slow)
- Funding (no data feed in backtest)

**New, awaiting validation:**
- Candlestick — well-established TA, conditions are strict
- RSI divergence — high-conviction reversal signal in TA literature

---

## Path forward

1. **Bootstrap restart** — load my new code (auto-restart watcher, /backtest endpoint, 2 new agents)
2. **Re-run backtest** with corrected simulator (trailing stops + regime filter + per-agent max-hold + global cap). New agents (candlestick, rsi_divergence) get their first verdict.
3. **Apply Claude Code's recommended fixes** to momentum and asymmetric (entry tightening, TP adjustment).
4. **Compare verdicts** between my v2 simulator and the original. Which agents move from KILL to KEEP?
5. **Find the highest-edge survivor**. Flip ONE agent from paper → live with reduced position size ($100 notional).
6. **Watch first 10 real trades**. If real performance matches backtest, scale up. If not, pull back and investigate.

**Conservative target:** one validated agent live within 7 days, generating 1-3 trades per day, $100 position size. After 30 trades of real data, scale to $200 if expectancy holds. Add second agent if first one proves stable.

**Aggressive but disciplined:** within 30 days, 2-3 validated agents live, $200-$500 position size, 5-10 trades per day across all agents. Compounding monthly at 5-15% per the realistic target shape.

Anything faster than this is gambling.
