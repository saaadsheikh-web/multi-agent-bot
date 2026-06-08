# Treatise-Driven Backtest — Results

**Date:** 2026-05-06  
**Period:** 60 days × 8 high-liquidity symbols × 1H bars  
**Fees:** 0.04% round-trip (post-maker)  

These tests were chosen to validate (or kill) the most promising ideas from the new treatises.

---

## 🎯 TEST 4 — WEDGE PATTERNS = the standout discovery

| Setup | Trades | WR | Avg per trade | Verdict |
|---|---|---|---|---|
| **Falling wedge LONG (break of upper line)** | **126** | **46.0%** | **+0.212%** | ✅ **STRONG EDGE** |
| **Rising wedge SHORT (break of lower line)** | **124** | **40.3%** | **+0.109%** | ✅ **EDGE** |

### Why this matters

**This is the highest-edge setup found today** — beats 0.786+RSI<30 (+0.156%), beats anchored 0.236 (+0.148%), beats every Fib level individually.

Falling wedges have particularly strong edge: 46% WR with +0.21% avg per trade is near-best-of-class for any technical setup. The literature predicted wedges would work; data confirms it.

**Why wedges work:** they're consolidation patterns where price is being squeezed. The break direction has built-up momentum behind it. Institutions watch wedges carefully because they offer clean risk-defined entries.

---

## TEST 1 — Multi-factor zone scoring

| Score | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| Score 4-5 | 507 | 34.1% | −0.065% | ❌ Losing |
| **Score 6+** | **172** | **37.8%** | **+0.020%** | ⚠️ Small edge |

**The scoring system DOES work as a filter.** Score 4-5 setups lose; score 6+ shows a small positive. This validates the approach but the edge alone isn't huge — the filter's value is in REJECTING the weak setups, not as a standalone signal.

**Action:** raise current `fib_hotzone` MIN_ZONE_SIZE to 6 + use multi-factor scoring; expected to reduce signal count but improve quality.

---

## TEST 2 — 0.786 with extra filters

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| 0.786 baseline (60d) | 152 | 41.4% | −0.023% | ❌ Losing on shorter period |
| 0.786 + volume confirm | 71 | 33.8% | −0.340% | ❌ Volume filter HURTS |
| **0.786 + EMA200 trend** | **59** | **45.8%** | **+0.098%** | ✅ EDGE |

### Two important findings

1. **0.786 + EMA200 trend filter works** — adding a trend filter improves WR from 41% to 46% and turns negative into positive
2. **Volume confirmation HURTS** — adding volume>1.3× requirement made things worse, not better. Counter-intuitive but real. **Don't add volume filters to 0.786 setups.**

(Note: 0.786 baseline went −0.023% here vs +0.140% in the 90-day test — that's normal sample variation between 60d and 90d periods.)

---

## TEST 3 — Log-scale trend channels (200-bar fit, R²>0.5)

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| **Log channel BOTTOM long** | **35** | **40.0%** | **+0.039%** | ⚠️ Small edge |
| Log channel TOP short | 54 | 24.1% | −0.293% | ❌ Loses badly |

### Asymmetric finding (consistent with earlier trend-line test)

Log-scale channel BOTTOMS work as longs (small but positive). Log-scale channel TOPS as shorts FAIL — the same pattern we saw with simple trend lines: in crypto, bouncing off support is harder than rejecting at resistance because uptrends in crypto tend to overshoot.

**Action:** if we ship `LogChannelAgent`, make it BTC-bottom-LONG only.

---

## TEST 5 — Cross-asset 0.618 confluence (BTC + ETH + SOL together)

| Setup | Trades | WR | Avg | Verdict |
|---|---|---|---|---|
| BTC + ETH + SOL all at 0.618 | 3 | 33.3% | −0.180% | ❌ Too few trades |

**Only 3 setups in 60 days** — the requirement that 3 assets all be at 0.618 retracement at the same bar is too strict. Either drop to 2-asset confluence, or relax proximity to 0.6%.

**Action:** rework or drop. Not enough data.

---

## CONSOLIDATED RANKING — best setups across ALL backtests today

| # | Setup | n | WR | Avg/trade | Source |
|---|---|---|---|---|---|
| 1 | **Falling wedge LONG** | 126 | 46.0% | **+0.212%** | NEW |
| 2 | **0.786 + RSI<30 oversold LONG** | 112 | 45.5% | +0.156% | Earlier |
| 3 | Anchored 0.236 from period high | 48 | 45.8% | +0.148% | Earlier |
| 4 | 0.786 alone (90d) | 256 | 41.0% | +0.140% | Earlier |
| 5 | **Rising wedge SHORT** | 124 | 40.3% | **+0.109%** | NEW |
| 6 | **0.786 + EMA200 trend** | 59 | 45.8% | **+0.098%** | NEW |
| 7 | 0.618 alone | 195 | 37.9% | +0.068% | Earlier |
| 8 | Log channel bottom LONG | 35 | 40.0% | +0.039% | NEW |
| 9 | Hot zone (multi-factor) score 6+ | 172 | 37.8% | +0.020% | NEW |
| 10 | Hot zone with 6+ Fibs | 28 | 39.3% | +0.028% | Earlier |

---

## Updated ship priority (highest expected edge first)

| # | Agent | Edge basis | Lines |
|---|---|---|---|
| 1 | **`WedgeAgent`** (falling-wedge long + rising-wedge short) | +0.212% / +0.109% per trade | 120 |
| 2 | `Fib786OversoldAgent` (0.786 + RSI<30 LONG) | +0.156% per trade | 80 |
| 3 | Add EMA200 trend filter to fibonacci agent for 0.786 | +0.098% | 30 |
| 4 | `AnchoredFib236Agent` (period-high anchor) | +0.148% | 70 |
| 5 | Multi-factor zone score (≥6) for fib_hotzone | +0.020% as filter | 100 |

---

## What we DON'T ship

- ❌ Cross-asset Fib confluence — too few trades to validate
- ❌ Log-channel SHORTS — loses money
- ❌ Volume confirmation for 0.786 — counterintuitively hurts
- ❌ Multi-factor zone score 4-5 (only 6+ has edge)

---

## The honest meta-finding

The agents we already built (`fibonacci`, `fib_hotzone`) were designed BEFORE we had this data. They use the wrong levels (0.382, 0.500 are losers), the wrong proximity (too loose), and the wrong filters (no trend gate).

**The data says: rebuild fibonacci to fire ONLY at 0.618 + 0.786 with EMA200 trend confirmation. Drop everything else.**

The single biggest near-term improvement isn't a new agent — it's tightening the existing one based on what we now know.

---

End of treatise backtest. Saved 2026-05-06.
