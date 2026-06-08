# Mega Strategy Catalog — 50 Strategies for Crypto Perp Trading

**Goal:** comprehensive catalog of strategies used by professional traders across crypto, equities, FX, and futures markets. Each entry assessed for fee-survivability on BloFin (0.06% taker × 2 = 0.12% round-trip) and feasibility on $2,272 capital.

**Scoring:**
- **Fee-survival** (1-5): how much fees eat the per-trade edge. 5 = trivial. 1 = killer.
- **Edge confidence** (1-5): is there real documented edge in literature?
- **Code complexity** (1-5): 1 = simple, 5 = advanced (requires advanced market data / multi-symbol cointegration / etc.)
- **Priority** (P0-P3): P0 = build first, P3 = exploratory

Currently implemented agents are marked ✅. New designs from this catalog get a build queue rank.

---

## A. MOMENTUM / TREND-FOLLOWING (10 strategies)

### 1. ✅ Donchian Channel Breakout (period 30, ATR×2)
- 1H bar 30-period high/low break + volume confirm + ATR-based stop
- Fee-survival: **3** | Edge: **4** | Complexity: **2** | Priority: **P0** (already live, paper)
- Backtest result: WR 48.7%, ExpR +0.044R, DD 69.3% (% equity model)

### 2. Daily Range Breakout (1-week structure)
- 1H bars, 1-week high/low range break, 4% min stop, trailing only
- Fee-survival: **5** | Edge: **5** | Complexity: **2** | Priority: **P0** (drafted, awaiting integration)

### 3. ✅ Higher-TF Trend Pullback (50 EMA pullback)
- 1H, EMA 50/200 trend filter, pullback to 50 EMA, 2.5% stop, trailing exit
- Fee-survival: **5** | Edge: **4** | Complexity: **3** | Priority: **P0** (live, awaiting backtest verdict)

### 4. ADX Trend Following
- Enter when ADX > 25 with directional movement, exit when ADX < 20
- Position only in clear trends (ADX filter), pyramid on continuation
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 5. Golden Cross / Death Cross (50/200 EMA)
- Enter long on 50 EMA crossing above 200 EMA, exit on cross back
- Daily timeframe ideal; 1H acceptable for crypto
- Fee-survival: **5** | Edge: **4** | Complexity: **1** | Priority: **P1**

### 6. ✅ EMA Ribbon Alignment (3-timeframe)
- 5m + 15m + 1h all aligned 9>21>50 → long; reverse for short
- Fee-survival: **2** | Edge: **2** | Complexity: **2** | Priority: ❌ KILLED in backtest

### 7. Triple MA System (Hull/EMA/SMA blend)
- Hull MA fast + EMA medium + SMA slow; enter when all aligned + price above (below) all
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P3**

### 8. Parabolic SAR
- Trail stop based on Parabolic SAR; enter at SAR flip + volume confirm
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P3**

### 9. Supertrend Indicator
- ATR-based dynamic trend line; enter at flip + 1H bar close + volume
- Common in crypto algorithmic trading
- Fee-survival: **4** | Edge: **3** | Complexity: **2** | Priority: **P1**

### 10. Heikin Ashi Trend Persistence
- Use Heikin Ashi candles to filter noise; enter on 3+ consecutive same-color HA bars
- Fee-survival: **3** | Edge: **2** | Complexity: **2** | Priority: **P3**

---

## B. MEAN REVERSION (10 strategies)

### 11. Larry Connors RSI(2) Overnight
- 5m RSI < 5 in uptrend (price > 200 SMA) → long, exit when RSI > 70
- Famous Connors method; works on equities, less proven on crypto 24/7
- Fee-survival: **2** | Edge: **3** | Complexity: **1** | Priority: **P2**

### 12. ✅ Bollinger Band Squeeze Breakout
- BB width < 15th percentile of last 100 bars + breakout candle
- Fee-survival: **2** | Edge: **3** | Complexity: **3** | Priority: ❌ tight stops killed it

### 13. ✅ VWAP Mean Reversion
- Price >2σ from rolling 24h VWAP + declining volume + RSI extreme
- Fee-survival: **3** | Edge: **3** | Complexity: **3** | Priority: **P0** (paper-only, awaiting backtest)

### 14. Z-Score Mean Reversion on Price
- z = (price - rolling_mean) / rolling_std; enter when |z| > 2.5; exit at z=0
- 1H bars, 100-bar rolling window
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 15. Support/Resistance Bounce (price action)
- Identify horizontal S/R from prior swings, trade rejection candles at level
- Fee-survival: **4** | Edge: **4** | Complexity: **4** | Priority: **P1**

### 16. Bollinger Band Bounce (range-bound)
- Price tags lower BB + RSI < 30 + ranging market (ADX < 20) → long mean revert
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 17. Keltner Channel Mean Reversion
- Similar to BB but ATR-based bands; slower-reacting than BB
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P3**

### 18. ✅ RSI Divergence (1h)
- 2 most recent swing lows: lower price + higher RSI = bullish div
- Fee-survival: **5** | Edge: **4** | Complexity: **3** | Priority: **P0** (live, awaiting backtest)

### 19. Stochastic RSI Mean Reversion
- StochRSI < 0.2 + price near lower BB → long
- Fee-survival: **3** | Edge: **2** | Complexity: **2** | Priority: **P3**

### 20. CCI Reversion (Commodity Channel Index)
- CCI < -100 + bullish reversal candle → long
- Fee-survival: **3** | Edge: **2** | Complexity: **1** | Priority: **P3**

---

## C. CHART PATTERNS (10 strategies)

### 21. ✅ Japanese Candlestick Patterns
- Hammer/engulfing/morning star at exhaustion zones (EMA50 + RSI extreme)
- Fee-survival: **5** | Edge: **3** | Complexity: **3** | Priority: **P0** (live, awaiting backtest)

### 22. Pin Bar Reversal at Key Level
- Single-bar rejection (long wick > 2× body, small upper wick) at S/R level
- Different from hammer because location matters
- Fee-survival: **5** | Edge: **4** | Complexity: **3** | Priority: **P1**

### 23. Bullish/Bearish Engulfing at HTF Trend
- Engulfing candle ON 1h timeframe + matching 4h trend direction
- Fee-survival: **5** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 24. Inside Bar Breakout
- Inside bar (range fully within prior bar) → break of either side = entry
- Volatility expansion play
- Fee-survival: **4** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 25. Three Drives / Three Pushes Reversal
- Price makes 3 successive highs/lows with declining momentum (RSI lower each push)
- Fee-survival: **5** | Edge: **3** | Complexity: **4** | Priority: **P3**

### 26. Head and Shoulders / Inverse H&S
- 3-peak pattern with neckline break
- Fee-survival: **5** | Edge: **3** | Complexity: **5** | Priority: **P3** (hard to code reliably)

### 27. Double Top / Double Bottom
- Two equal-ish peaks/troughs with neckline break
- Fee-survival: **5** | Edge: **3** | Complexity: **4** | Priority: **P3**

### 28. Triangle Breakout (Symmetric/Ascending/Descending)
- Converging trend lines compress price; breakout direction signals trade
- Fee-survival: **4** | Edge: **3** | Complexity: **5** | Priority: **P3**

### 29. Flag/Pennant Continuation
- Strong trend → consolidation flag → continuation breakout
- Fee-survival: **4** | Edge: **3** | Complexity: **4** | Priority: **P3**

### 30. Cup and Handle
- 6-week cup formation + handle pullback + breakout
- Fee-survival: **5** | Edge: **3** | Complexity: **5** | Priority: **P3** (very rare on crypto timeframes)

---

## D. VOLUME / ORDER FLOW (10 strategies)

### 31. OBV (On-Balance Volume) Trend
- OBV slope matching price slope = continuation; OBV diverging from price = reversal
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 32. ✅ Whale Tracker (orderbook imbalance)
- Top-of-book bid/ask volume imbalance > 30%
- Fee-survival: **3** | Edge: **2** | Complexity: **3** | Priority: ⚠️ orderbook gameable

### 33. Liquidation Sweep + Reversal
- Identify recent swing high/low (liquidity pool); enter on sweep + reversal candle
- Real institutional pattern
- Fee-survival: **5** | Edge: **5** | Complexity: **4** | Priority: **P1**

### 34. Smart Money Concepts (SMC) — Order Blocks + FVG
- Identify order blocks (last opposite candle before strong move) + Fair Value Gaps; enter on retest
- Used by prop traders extensively in 2024-2026
- Fee-survival: **5** | Edge: **5** | Complexity: **5** | Priority: **P1** (high effort, high reward)

### 35. Wyckoff Accumulation / Distribution
- Multi-stage pattern: PS (preliminary support), SC (selling climax), AR, ST, Spring, JOC, SOS, LPS
- Fee-survival: **5** | Edge: **5** | Complexity: **5** | Priority: **P3** (very hard to code)

### 36. POC (Point of Control) Bounce
- Volume profile peak (POC) acts as magnet; trade rejections from POC
- Requires session-based volume profile
- Fee-survival: **4** | Edge: **3** | Complexity: **4** | Priority: **P2**

### 37. Fair Value Gap (FVG) Fill
- Price imbalance gap between candles often gets filled; trade direction back into gap
- Subset of SMC
- Fee-survival: **5** | Edge: **4** | Complexity: **3** | Priority: **P1**

### 38. Volume Spike Capitulation
- Single bar with > 5× avg volume + RSI < 25 → long bottom-fishing
- Fee-survival: **3** | Edge: **3** | Complexity: **2** | Priority: **P2**

### 39. Delta Divergence (futures CVD)
- Cumulative Volume Delta diverging from price = absorption/exhaustion
- Requires tick-level data BloFin doesn't expose easily
- Fee-survival: **5** | Edge: **5** | Complexity: **5** | Priority: **P3** (data limitation)

### 40. Spoofing/Layering Detection
- Detect fake bid/ask walls that get pulled before fill; trade against them
- Requires real-time orderbook delta
- Fee-survival: **5** | Edge: **5** | Complexity: **5** | Priority: **P3** (advanced; gameable)

---

## E. STATISTICAL / QUANT (10 strategies)

### 41. Pairs Trading (BTC/ETH cointegration)
- BTC and ETH cointegrate ~95% of time; trade z-score of price ratio
- Long ETH/Short BTC when ratio extends below mean, mirror for above
- Fee-survival: **5** | Edge: **5** | Complexity: **5** | Priority: **P1** (high effort, market-neutral)

### 42. Cross-Symbol Statistical Arbitrage
- Find correlation breaks across coin clusters (DeFi, L1s, memes)
- Long laggards, short leaders during temporary divergence
- Fee-survival: **4** | Edge: **4** | Complexity: **5** | Priority: **P2**

### 43. ⚠️ Funding Rate Extreme Fade (proper implementation)
- Funding > 0.20% per 8h cycle = take opposite side, hold one cycle
- Pure +EV from funding capture
- Fee-survival: **5** | Edge: **5** | Complexity: **3** | Priority: **P0** (drafted)

### 44. Funding + Basis Combined
- Combine funding extremes with perp/spot basis extremes
- Double mean-reversion signal
- Fee-survival: **5** | Edge: **5** | Complexity: **4** | Priority: **P2**

### 45. Returns Mean Reversion (z-score on log returns)
- Trade z-score of log returns over rolling window
- Different from price MR — focuses on momentum exhaustion
- Fee-survival: **3** | Edge: **3** | Complexity: **3** | Priority: **P2**

### 46. Volatility Targeting (position-size by vol)
- Adjust position size inversely to ATR — keep risk constant
- Not a strategy itself but a position-sizing overlay
- Fee-survival: N/A | Edge: **5** | Complexity: **2** | Priority: **P0** (overlay all strategies)

### 47. Momentum Factor (cross-sectional)
- Rank all 20 coins by past 30-day return; long top 3, short bottom 3
- Classic Asness/Moskowitz momentum factor
- Fee-survival: **5** | Edge: **4** | Complexity: **3** | Priority: **P2**

### 48. Carry Trade (funding-based)
- Always long the coin with lowest (most negative) funding, short coin with highest funding
- Collect funding payments daily
- Fee-survival: **5** | Edge: **4** | Complexity: **3** | Priority: **P1**

### 49. Risk Parity Allocation
- Equal-risk weighting across all enabled strategies (vs equal-dollar)
- Better expected risk-adjusted returns
- Fee-survival: N/A | Edge: **4** | Complexity: **3** | Priority: **P2** (overlay)

### 50. Mean Reversion + Trend Hybrid (regime-switched)
- Use trend strategy in trending regime, mean-reversion in ranging
- Already partially implemented via regime filter
- Fee-survival: **4** | Edge: **5** | Complexity: **3** | Priority: **P0** (implicit in current architecture)

---

## TOP 10 BUILD QUEUE (after current backtest finishes)

Ranked by combined fee-survival × edge × ease of implementation:

| Rank | Strategy | Why First |
|------|----------|-----------|
| 1 | **Daily Range Breakout (#2)** | Highest theoretical ExpR, simplest code, drafted |
| 2 | **Funding Rate Extreme Fade (#43)** | Pure +EV from funding, drafted |
| 3 | **Carry Trade (#48)** | Cross-symbol funding capture, robust |
| 4 | **Pin Bar at Key Level (#22)** | High WR price action setup |
| 5 | **Liquidation Sweep + Reversal (#33)** | Real institutional pattern |
| 6 | **FVG Fill (#37)** | High-conviction SMC subset |
| 7 | **Pairs Trading BTC/ETH (#41)** | Market-neutral, robust math |
| 8 | **Supertrend (#9)** | Clean trend-following baseline |
| 9 | **S/R Bounce (#15)** | Classic price action |
| 10 | **Volatility Targeting Overlay (#46)** | Improves all strategies' risk-adjusted returns |

---

## What I'm NOT going to do (and why)

- **Implement all 50.** Code complexity 4-5 strategies (H&S, Wyckoff, SMC) take 2-3 days each. Not "tomorrow."
- **"Random DEMA strategies".** I assume DEMA = Dual Exponential Moving Average. I'd just be generating noise for noise's sake. Variant strategies with different MA periods rarely outperform a single well-tuned MA strategy.
- **Promise the "most powerful bot in the universe".** That phrase doesn't survive contact with markets. What survives: a 2-3 strategy portfolio with validated edge, traded with discipline, compounded for 1+ years.

## What I AM committing to

1. Code top 10 from queue above (1-2 per day = ~5-7 days work)
2. Backtest each before flipping live
3. Walk-forward validate the survivors
4. Live-deploy only those with ExpR > +0.20R AND DD < 40% AND >50 trades in backtest
5. Honest reporting on what passes and what fails

The bot becomes "powerful" when it has 3-5 uncorrelated validated strategies running in parallel. Not when it has 50 mediocre ones.
