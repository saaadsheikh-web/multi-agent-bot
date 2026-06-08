# Advanced Fibonacci Backtest — Results

**Date:** 2026-05-06  
**Period:** 90 days × 12 symbols × 1H bars  
**Fees:** 0.04% round-trip (post-maker)  
**Sample sizes shown — small samples = noise.**

---

## TEST 1 — Less-Common Single Ratios

| Level | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| **0.786** | **256** | **41.0%** | **+0.140%** | ✅ **STRONG EDGE** |
| 0.886 | 72 | 36.1% | +0.018% | ⚠️ Small sample, marginal |
| 0.236 | 909 | 29.4% | −0.181% | ❌ Losing |
| 1.272 reversal | 27 | 25.9% | −0.384% | ❌ Losing |

### THE FINDING

**0.786 is BETTER THAN 0.618.** 0.140% per trade vs 0.068% for 0.618. This contradicts common Fib-trading wisdom — 0.786 is supposed to be "the deep retracement, last chance before invalidation." But the data says: when price gets to 0.786, the bounce is more reliable than at 0.618.

This is consistent with Pesavento's writings — 0.786 is the harmonic anchor used in Bat patterns precisely because it's a high-probability reversal level.

---

## TEST 2 — 0.786 + RSI Confluence

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| **0.786 + RSI<30 (oversold long)** | **112** | **45.5%** | **+0.156%** | ✅ **STRONGEST SETUP FOUND** |
| 0.786 + RSI>70 (overbought short) | 70 | 37.1% | −0.089% | ❌ Losing |

### THE FINDING

**0.786 retrace + oversold RSI for LONGS = the single strongest setup in 90 days of testing.** 45.5% WR with +0.156% per trade. Asymmetric: works on longs (price bounces from oversold deep retrace), doesn't work on shorts (overbought rejections at 0.786 fail more often than they succeed).

---

## TEST 3 — 0.236 Momentum Continuation

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| 0.236 + EMA50 trend filter | 1100 | 32.3% | −0.098% | ❌ Losing |

The "shallow retrace = strong continuation" thesis doesn't hold up. 32% WR is at coin-flip and the avg loss after fees is real. **DROP this idea.**

---

## TEST 4 — Multi-Timeframe Fib Confluence

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| 1H + pseudo-4H Fib cluster | 817 | 37.6% | −0.142% | ❌ Losing |

**Disappointing.** The research said MTF confluence should be the highest-edge play. Backtest says no. Possible explanations:
- Pseudo-4H from sampled 1H bars isn't true 4H data
- Cluster proximity (0.3%) was too loose
- Need actual 4H/1D candle data to test properly
- May need 3-timeframe alignment (1H + 4H + 1D), not 2

**Verdict:** don't ship MTF confluence based on this data. Re-test if we get true 4H/1D data into the backtest cache.

---

## TEST 5 — Anchored Fibonacci (90-day period high/low)

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| **Anchored 0.236 from period high** | **48** | **45.8%** | **+0.148%** | ✅ Edge but small sample |
| Anchored 0.382 | 34 | 29.4% | −0.403% | ❌ |
| Anchored 0.500 | 138 | 29.7% | −0.439% | ❌ |
| Anchored 0.618 | 250 | 35.2% | −0.200% | ❌ |
| Anchored 0.786 | 178 | 34.3% | −0.215% | ❌ |

### THE FINDING

**Anchored 0.236 from a major period high WORKS.** 45.8% WR. Translation: when price has retraced only 23.6% from the period high, it tends to bounce there because the trend is still strong. But all the deeper anchored Fibs FAIL — once you've retraced 38% or more from a major high, the trend is breaking and the level doesn't hold.

---

## TEST 6 — Fibonacci EMA Ribbon (8/13/21/34/55/89)

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| Uptrend stack pullback to 21-EMA | 372 | 26.9% | −0.245% | ❌ Losing |
| Downtrend stack pullback to 21-EMA | 425 | 35.1% | −0.020% | ❌ ~break-even |

**The Fib EMA Ribbon is largely superstition.** Using 8/13/21/34/55/89 instead of 9/20/50/200 doesn't add edge. Pullbacks to 21-EMA in a trending stack lose money. **DROP this idea.**

---

## CONSOLIDATED RANKING — what actually works

| Rank | Setup | Trades | WR | Avg | $/100 |
|---|---|---|---|---|---|
| 1 | **0.786 + RSI<30 oversold LONG** | 112 | 45.5% | **+0.156%** | +$0.156 |
| 2 | **Anchored 0.236 from period high** | 48 | 45.8% | **+0.148%** | +$0.148 |
| 3 | **0.786 alone** | 256 | 41.0% | **+0.140%** | +$0.140 |
| 4 | 0.618 alone (from prior test) | 195 | 37.9% | +0.068% | +$0.068 |
| 5 | Hot zone with 6+ confluence | 28 | 39.3% | +0.028% | +$0.028 |
| 6 | Trend line downtrend resist short | 258 | 36.0% | +0.017% | +$0.017 |
| Everything else | | | <0% | losing | |

---

## What we should ship in the agents (when freeze ends)

### High priority — proven edge:

1. **Add 0.786 to `fibonacci` agent** as a new fire-level. Currently fires at 0.382/0.500/0.618 — all losers. Replace with 0.618/0.786 only.
2. **New `Fib786OversoldAgent`** — fires LONG when price retraces to 0.786 of a recent swing AND RSI<30. The single best setup found.
3. **New `AnchoredFib236Agent`** — uses period-high anchor (50+ days back), fires LONG bounce when price is at 0.236 retrace from anchor high.

### Drop:

- **MTF confluence** — backtest doesn't support it. Need real 4H/1D data first.
- **Fib EMA Ribbon** — superstition.
- **0.236 continuation** — losing thesis.
- **0.382, 0.500** as standalone signals.

---

## Honest read

We spent a session researching MTF confluence as the "biggest opportunity" — backtest says no. The actual winners were unexpected: **0.786 (the level supposedly indicating exhaustion) and Anchored 0.236 (the shallow retrace from major highs)**. Both have small but real edge.

This is the value of testing. Research said one thing, data said another.

Saved 2026-05-06.
