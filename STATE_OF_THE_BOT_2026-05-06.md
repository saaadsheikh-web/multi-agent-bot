# State of the Bot — 2026-05-06 04:50 UTC
*The "school → PhD" report Saad asked for: where we are, what's broken, what's missing, where we go next.*

---

## 🟢 What's working (today's snapshot)

| Metric | Value |
|---|---|
| Trades closed today | 6 |
| Today's bot P&L | **+$1.85** |
| Open positions | 0 |
| Lifetime closed P&L | **+$5.60** (across 50+ trades) |
| Signal volume | 45-57 raw → 18-23 aggregated per scan (healthy) |
| Top conf cap holding | yes (max 9 in logs) |
| KILL-SWITCH active | yes (hurst_regime auto-dropped) |

## 🟢 Agents pulling their weight (lifetime)

| Agent | Trades | Lifetime $ |
|---|---|---|
| connors_rsi2 | 20 | **+$4.05** ⭐ |
| hurst_regime | 14 | +$1.12 (auto-killed) |
| fibonacci | 4 | +$0.79 |
| tradingview | 1 | +$0.43 |
| funding_extremes | 4 | +$0.31 |
| daily_breakout_2h | 2 | +$0.22 |
| daily_breakout_4h | 2 | −$0.39 |
| daily_breakout_24h | 3 | −$0.93 |

---

## 🟡 Active bugs / warnings (not blocking but worth fixing)

### Bug 1: AI Arbiter broken (3 errors in last 4h)
```
ERROR: Fatal error in message reader: Command failed with exit code 1
WARNING: max-sdk arbiter: Command failed with exit code 1
```
**What this means:** the Claude Max SDK arbiter that's supposed to review high-conviction signals isn't running. The bot falls back to "approve" by default — meaning AI vetoes are silently disabled. **Not critical** (the WR-weighted kill-switch + trend filter cover the gap), but the AI quality check is offline.
**Fix:** investigate Claude SDK install / OpenRouter fallback path. Probably a token/path issue.

### Bug 2: BLOFIN_BROKER_ID warning (cosmetic)
Spammed every reload. Bot has fallback handling, doesn't actually break orders. Just noise.
**Fix:** suppress the warning OR set the env var. Low priority.

### Bug 3: Position reconciliation warnings (race conditions)
3 cases of "open in DB but gone from exchange" — DASH, TAO, XMR. Bot self-heals (syncs closed) but suggests timing issue between BloFin's actual fills and the bot's DB tracking.
**Fix:** tighter reconciliation polling. Medium priority.

---

## ❌ Data we DON'T have (but probably should)

The bot currently sees: 5m/15m/1h candles + funding rate + order book + a news_sentiment field that's underused + computed TrendState.

**What we DON'T see:**

| Missing data | What it would give us | Source |
|---|---|---|
| **4H + 1D candles** | True multi-timeframe Fib confluence (currently can only fake from 1H) | BloFin API |
| **BTC dominance %** | Filter: when BTC dom rising, alts bleed — short bias | TradingView, CoinGecko |
| **Liquidation data** | Fade liquidation cascades (~70% bounce within hours) | CoinGlass, Hyblock |
| **Real news headlines** | Pause trading around FOMC, CPI, hack news | RSS feeds, NewsAPI |
| **Twitter/X sentiment** | Crypto Twitter often front-runs moves | LunarCrush, Santiment |
| **On-chain flows** | Exchange inflows = sell pressure, outflows = accumulation | Glassnode, CryptoQuant |
| **Options flow** | Put/call ratio extremes precede reversals | Deribit, Greeks.live |
| **ETH/BTC ratio** | Alt season indicator | Computable from prices |
| **Realized volatility (per symbol)** | Filter: don't trade mean-rev when realized vol > 2× normal | Computable from candles |

---

## ❌ Indicators we DON'T compute (but should)

The bot already has: RSI, EMA, ATR, MACD, Bollinger Bands, Stochastic, Williams %R, Hurst exponent, Kalman filter, Supertrend, VWAP.

**What's still missing:**

| Indicator | Why it would help |
|---|---|
| **Order book imbalance** (top 5 levels bid/ask ratio) | Predicts 30-60s direction 58-64% per academic literature |
| **CVD (cumulative volume delta)** | Real buy/sell aggression — divergences = reversal |
| **Volume Profile / VPOC** | Already partially used; needs better integration as filter |
| **ADX** (currently only proxy) | True trend-strength gauge |
| **Donchian extremes** | Already partial; needs as confluence layer |
| **Money Flow Index (MFI)** | Volume-weighted RSI |
| **Heikin-Ashi smoothing** | Reduces noise on signal candles |

---

## 🎯 The honest assessment of where we are

We're **at the end of "school" / start of "high school"** in your analogy. Here's the proof:

**What we MASTERED (school graduation):**
- Limit-only execution
- Maker-fee optimization
- Multi-agent system with WR-weighted kill-switch
- Confidence-graded sizing
- Trend filter
- Pre-position at zone
- Strict SL/TP/trail logic

**What we HAVEN'T mastered (high school):**
- True multi-timeframe analysis (4H/1D missing)
- Real news event awareness
- Cross-asset correlation (BTC dom)
- Order flow micro-structure

**What's "university" stuff (months away):**
- Walk-forward strategy validation
- ML feature engineering with current indicators
- Portfolio optimization (which symbols to allocate to)
- Risk parity sizing

**What's "PhD" (1+ year):**
- Custom alpha factors from on-chain data
- HFT-style order book reading
- Multi-asset stat arb
- Reinforcement learning policy

---

## 🔥 The top 5 "next school year" priorities

Ranked by IMPACT × EASE:

### 1. Fix the AI arbiter (effort: 30 min)
The arbiter is silently failing on every high-conviction trade. Even if it wasn't perfect, it was a sanity check. **Either fix the Claude SDK path or wire OpenRouter as primary.**

### 2. Add 4H + 1D candles to MarketContext (effort: 1 hr)
Currently we only have 5m/15m/1h. The MTF Fib confluence backtest FAILED because we faked 4H from 1H. Real 4H/1D would unlock the highest-edge confluence per the research. **Add `df_4h` and `df_1d` fields to MarketContext.**

### 3. Add BTC dominance filter (effort: 45 min)
When BTC dominance is rising, alt-coin longs bleed. Add a `btc_dom_trend` to TrendState. **Mean-rev LONGs on alts get blocked when BTC dom rising.**

### 4. Real news event blackout (effort: 1.5 hr)
Currently `news_sentiment` is a field but not actively used. Wire a feed (CryptoCompare News API, NewsAPI) to detect FOMC/CPI/exchange-hack events and **pause trading 30 min before / 60 min after**.

### 5. Order book imbalance as confluence (effort: 2 hr)
We already pull the orderbook. Use it. **Compute (bid_qty − ask_qty) / (bid_qty + ask_qty) at top 5 levels.** Use as +1 confidence boost when imbalance agrees with signal direction.

---

## What this means for your money

Today's P&L is +$1.85. Lifetime is +$5.60. Account equity has grown from $2,225 → $3,000+ (most from manual TAO/INJ).

**The bot is profitable today, but small.** That's by design — we're in proof-of-concept phase. The path to meaningful profit isn't "trade bigger" — it's:

1. **Fix the leaks** (trail stops widened ✅ done tonight)
2. **Add the missing data** (4H/1D, news, BTC dom)
3. **THEN scale up** (when realized R:R hits 1.5+ over 100 trades)

Premature scaling = premature blowup. The "school → PhD" path Saad described is exactly right. We're not yet at the level where doubling notional is safe.

---

## Recommendation for tonight

The trail-stop widening shipped 8 minutes ago needs trades to validate. **Don't ship more code in the same window** — we won't be able to attribute results.

Tomorrow morning, look at the next 10-20 closes. If avg winner climbs from +0.876% toward +1.4%+ as predicted, the fix worked. If not, we go back to the data.

Then we ship priority #1 (AI arbiter fix) followed by #2 (4H/1D data).

Saved 2026-05-06.
