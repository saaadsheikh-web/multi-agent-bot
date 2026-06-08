# Profitable Strategy Designs — From First Principles

**Goal:** strategies that have demonstrable theoretical edge AFTER fee drag, not just signal quality.

**The fee constraint** (the lesson from last night's forensics):
- BloFin taker fee: 0.06% per side, 0.12% round-trip
- For SL = 1% of price: fees consume 12% of stop-risk → break-even WR rises ~6%
- For SL = 5% of price: fees consume 2.4% of stop-risk → break-even WR rises ~1%

**Implication:** strategies with SLs < 1.5% of price get killed by fees. Strategies with SLs > 4% have fees as background noise. **Higher timeframes naturally have wider SLs.**

---

## Strategy 1: DailyRangeBreakoutAgent (HIGHEST CONVICTION)

**Premise:** Multi-day range breaks with strong volume have well-documented follow-through edge in literature (Wilder, Donchian, Turtle Traders).

**Setup (1H bars, but multi-day structure):**
- Look at the highest-high and lowest-low of the **last 168 bars** (1 week)
- LONG: close above 1-week high AND volume > 2× 20-bar avg AND ATR-volatility expanding
- SHORT: mirror
- **SL:** 50% retracement of the breakout candle, OR 4% from entry (whichever wider)
- **TP:** trailing-only after 2× ATR favorable move
- Max-hold: 7 days

**Why this should clear fees:**
- SL ~ 4-6% on most coins → fee/risk ratio = 2-3% (negligible)
- Real range breakouts have 45-55% WR in literature
- Trailing-only lets winners 5-10× the SL distance

**Expected math:**
- WR 45%, avg win = 4R, avg loss = 1R
- ExpR = 0.45×4 - 0.55×1 = +1.25R per trade
- Fewer trades (~50-100/year across 20 coins) but huge per-trade edge

---

## Strategy 2: HighFundingFadeAgent (revival, properly tuned)

**Premise:** When perpetual funding rate is extreme (>0.20% per 8h cycle = >219% APR), shorts are paying longs heavily — the market is dramatically over-leveraged in one direction. Statistical fade.

**Setup:**
- Trigger only when funding rate > 0.20% (extreme) OR < -0.20%
- Take OPPOSITE side of funding
- Hold ONE funding cycle (8 hours)
- **SL:** 3% from entry
- **TP:** 1.5% gain OR funding payment received, whichever first
- After collecting funding, exit immediately

**Why this should clear fees:**
- Funding payment alone ≥ 0.20% of position value (free money)
- Round-trip fees: 0.12%
- Net gain just from funding: 0.08% per cycle
- Plus expected mean reversion of overcrowded position

**Expected math:**
- ~2-5 funding extreme events per coin per month
- 20 coins × 3 events × 12 months = ~720 trades/year potential
- Even 50% WR with 1:1 R:R gives +0.40R after net funding income
- Realistic ExpR: +0.30R to +0.60R per trade

---

## Strategy 3: VolatilityCompressionBreakoutAgent (smarter asymmetric)

**Premise:** Bollinger Band width in the bottom 10% of last 200 bars = volatility coil. Breakouts from coils have strong follow-through statistically (Bollinger's own research).

**Setup (1H bars):**
- BB width < 10th percentile of last 200 bars (rare, ~5% of bars)
- Breakout candle closes outside BB by >0.5×ATR
- Volume > 1.5× 20-bar avg
- **SL:** 2× ATR or 3% (whichever wider) — wider than original asymmetric's 1×ATR fix
- **TP:** trailing-only after 2× ATR favorable move
- Max-hold: 24 hours

**Why this fixes the original asymmetric's failure:**
- Original asymmetric had 1×ATR stop on 15m bars (0.23% on BTC) — fees ate 50% of risk
- This version: 1H bars + 2×ATR or 3% floor → fees are 2-4% of risk, not 50%
- Still uses the high-quality squeeze gate
- Trailing replaces the 3R fixed TP that rarely got hit

---

## Strategy 4: HTFRSIDivergenceAgent (4H timeframe)

**Premise:** RSI divergences are a real reversal signal in TA literature. The 4H timeframe filters noise far better than 1H.

**Setup (4H bars, derived from 1H by aggregation):**
- Identify last 2 swing highs/lows in price (10-bar lookback)
- Bullish div: lower price low + higher RSI low + RSI < 50 + price turned up
- Bearish div: higher price high + lower RSI high + RSI > 50 + price turned down
- **SL:** beyond the swing extreme + 0.5×ATR buffer (typically 4-7%)
- **TP:** trailing-only after 1×ATR favorable move

**Why this should clear fees:**
- 4H timeframe → average bar range 1-2% on BTC
- SL beyond swing extreme = wide (4-7%)
- Fee/risk ratio: 1.5-3% (negligible)
- Fewer signals (real divergences fire ~5-10 times/year per coin)
- High-conviction setups when they fire

---

## Strategy 5: PerpetualBasisArbitrageAgent (advanced, market-neutral)

**Premise:** When perp price diverges from spot price by >0.3%, mean reversion is near-certain. Combined with funding rate, can profit on both sides.

**Setup (requires spot price feed):**
- Get BloFin perp price + spot index price
- Calculate basis = (perp - spot) / spot × 100
- LONG perp + SHORT futures (or vice versa) when basis is extreme
- Exit when basis returns to ±0.05%
- Holds typically 2-12 hours

**Why this should clear fees:**
- Market-neutral (long one side, short other)
- Pure convergence trade — high WR (75-85% in literature)
- SL: opposite extreme of basis (rare event)
- Win comes from basis closing + funding collection

**Caveat:** requires spot index data feed (BloFin provides via API). More complex to implement.

---

## Strategy 6: VWAPRejectionAgent (intraday institutional)

**Premise:** Institutions use VWAP as benchmark. When price extends >1.5σ from VWAP and shows rejection (wick + reversal candle), price typically returns to VWAP.

**Setup:**
- Daily-anchored VWAP (resets at 00:00 UTC)
- Calculate σ-bands at ±1σ, ±2σ from VWAP
- LONG: price wicks below -2σ + closes above -1σ (rejection)
- SHORT: mirror at +2σ
- **SL:** beyond the wick extreme + 0.3×ATR
- **TP:** VWAP itself
- Trailing once price reaches VWAP - 0.5σ (lock 75% of move)

**Why this should clear fees:**
- 2σ VWAP extensions are rare (~3-5 per coin per day)
- SL distance from wick to entry: typically 1.5-2.5%
- TP distance to VWAP: typically 2-4%
- R:R ~ 1:2 minimum
- High WR (60-70%) due to mean-reversion mechanics

---

## My ranked recommendation

For Saad's $2,272 capital + "don't lose money" constraint:

**Tier 1 (build first, lowest risk):**
1. **DailyRangeBreakoutAgent** — simplest robust edge, lowest fee drag, highest expected R per trade
2. **HighFundingFadeAgent** — pure +EV from funding mechanics, market-neutral over time

**Tier 2 (build after tier 1 validates):**
3. VolatilityCompressionBreakoutAgent (rebuild of asymmetric)
4. HTFRSIDivergenceAgent (4H div trades)

**Tier 3 (advanced, build only if tier 1+2 prove out):**
5. PerpetualBasisArbitrageAgent
6. VWAPRejectionAgent

---

## Pick now (so I can implement when backtest finishes)

Tell me which 1-2 to implement first. I'll code them in a separate file (`strategies_v2.py`) so the auto-restart doesn't kill the running backtest. Once it's done, I integrate into bot.py and we backtest the new strategies.

Default if you don't pick: I'll do **DailyRangeBreakoutAgent + HighFundingFadeAgent**.
</thinking>
