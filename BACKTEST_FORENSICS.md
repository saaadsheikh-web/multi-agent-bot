# BACKTEST FORENSICS REPORT
Generated: 2026-04-29 05:01 UTC

---

## Summary of Findings

The -554% MAX_DD is real but mismeasured. Four distinct bugs/issues found:
1. **Equity model** — fixed-notional, no bankruptcy stop → DD > 100% is meaningless
2. **Fee-to-risk ratio** — asymmetric uses ATR-based stops so tight that 0.12% fees cost 0.5–1.6R per trade
3. **Stop model** — wick-triggered stops on 15m bars add ~0.07R drag vs bar-close stops
4. **Momentum win rate** — 29.9% < 31.4% breakeven → structurally negative at market-order fees

The infrastructure (math, entry logic, fee calculation) is **correct**. The strategies are the problem.

---

## 1. Root Cause: Why -554% MAX_DD on Momentum?

### What the number actually means

The equity model uses **fixed dollar risk** per trade: `r_multiple × $200 × 0.01 = r_multiple × $2`.
There is no position-sizing adjustment as equity falls, and no bankruptcy stop.

Over 17,889 trades at -0.066R avg, the cumulative dollar loss peaks at ~$1,108 from a $200 start,
driving equity to approximately **-$908**. The DD formula `(equity - peak) / peak × 100` gives:
`(-908 - 200) / 200 × 100 = -554%`.

This means the strategy goes bankrupt (equity < 0) and keeps ghost-trading with borrowed capital.
The -554% is not inflated — the strategy genuinely loses more than 5× its starting capital before its worst trough.

### Comparison: % equity model (correct)

With 1% risk per trade (`risk = current_equity × 0.01`) and position size scaling down as equity drops,
momentum reaches **$0 (full ruin)** before the 365-day window ends on BTC alone (MaxDD = -37.4% on BTC,
but -100% on all 20 symbols combined). Both models agree: momentum is unprofitable.

### Math verification (momentum)

```
Long trade: TP = entry × 1.030, SL = entry × 0.988
Risk           = 1.200% of entry
R on TP hit    = (3.00% − 0.12% fee) / 1.20% = +2.40R
R on SL hit    = (−1.20% − 0.12% fee) / 1.20% = −1.10R
Break-even WR  = 1.10 / (2.40 + 1.10) = 31.4%
Actual WR      = 29.9%  →  negative edge by 1.5 percentage points
Expected value = 0.299 × 2.40 + 0.701 × (−1.10) = −0.054R
Reported avg_r = −0.066R  (extra drag from timeout exits at unfavorable prices)
```

---

## 2. Trade Math Verification — PASS

10 random momentum trades manually verified against candle data. All delta = 0.000000.
No fee double-charging. R-multiple formula confirmed correct.

**Same-bar SL+TP conflicts** (pessimistic SL-wins): **0 / 400 = 0%** on BTC-USDT.
The 1.2% SL and 3.0% TP are wide enough that simultaneous touches in a single 15m bar never occurred.

Sample of verified trades:
```
2025-05-07 08:15  long   TP  entry=96804.10  exit=99708.22  r_stored=+2.4000  delta=0.000000
2025-06-21 23:30  short  SL  entry=101363.80 exit=102580.17 r_stored=-1.1000  delta=0.000000
2025-06-26 02:00  long   TO  entry=107569.60 exit=107004.70 r_stored=-0.5376  delta=0.000000
2026-02-28 18:00  long   TP  entry=65401.40  exit=67363.44  r_stored=+2.4000  delta=0.000000
2026-04-07 20:30  long   TP  entry=69335.50  exit=71415.57  r_stored=+2.4000  delta=0.000000
```

---

## 3. Fee/Slippage Sensitivity (All 20 Symbols, Momentum)

| Configuration | N | WR% | ExpR | MaxDD(pct_eq) | Final Eq ($200 start) |
|---|---|---|---|---|---|
| **Original** (0.06% taker, wick-stop) | 17,896 | 29.9% | −0.0661 | −100% (ruined) | $0 |
| Realistic (0.06% + 0.05% slip, wick-stop) | 17,896 | 29.8% | −0.1034 | −100% (ruined) | $0 |
| Limit-entry (0.02% maker, no slip, wick-stop) | 17,896 | 29.9% | **+0.0006** | −99.9% | $24 |
| Bar-close stops (0.06% taker, no slip) | 14,770 | 31.9% | **−0.0006** | −99.9% | $27 |
| **Best-case** (0.02% maker + bar-close stops) | 14,770 | 31.9% | **+0.066** | −97% | path-dep† |

† The best-case compounding model reaches high final equity because it survives the drawdown and then
compounds. A real account would be stopped out at −97% drawdown. Not reliable.

### Key findings

- **Fee reduction from 0.06% to 0.02%** (market→limit orders) saves 0.067R per trade —
  enough to flip momentum from −0.066R to approximately breakeven (+0.0006R).
- **Bar-close stops** cut trade count by 17% (fewer wick-triggered exits), improving WR from 29.9% to 31.9%,
  crossing the 31.4% breakeven threshold for 0.06% fee regime.
- **Even best-case has −97% max drawdown.** The strategy is not robust enough for real capital.
  Edge is thin and fragile; a short stretch of losing correlation kills it.

---

## 4. Donchian Parameter Sweep (All 20 Symbols)

| Period | ATR Mult | N | WR% | ExpR | MaxDD(pct_eq) |
|---|---|---|---|---|---|
| 10 | 1.5 | 7,176 | 33.8% | +0.0295 | −92.9% |
| 10 | 2.0 | 6,514 | 40.9% | +0.0467 | −87.8% |
| 10 | 2.5 | 6,063 | 45.1% | +0.0253 | −82.4% |
| 10 | 3.0 | 5,635 | 49.0% | +0.0335 | −76.0% |
| 20 | 1.5 | 6,104 | 33.4% | +0.0107 | −96.1% |
| 20 | 2.0 | 5,639 | 40.5% | +0.0312 | −89.9% |
| 20 | 2.5 | 5,339 | 45.0% | +0.0195 | −83.6% |
| 20 | 3.0 | 5,063 | 49.1% | +0.0314 | −74.5% |
| **30** | **2.0** | **4,895** | **41.1%** | **+0.0523** | −84.1% ← Best ExpR |
| 30 | 1.5 | 5,221 | 34.6% | +0.0448 | −91.1% |
| 30 | 2.5 | 4,721 | 45.2% | +0.0325 | −77.4% |
| 30 | 3.0 | 4,531 | 49.1% | +0.0377 | −69.5% |
| 40 | 1.5 | 4,667 | 34.9% | +0.0517 | −86.8% |
| 40 | 2.0 | 4,405 | 41.1% | +0.0477 | −81.8% |
| 40 | 2.5 | 4,272 | 45.2% | +0.0277 | −75.0% |
| 40 | 3.0 | 4,149 | 48.4% | +0.0190 | −73.2% |
| 60 | 1.5 | 3,846 | 35.0% | +0.0254 | −86.8% |
| 60 | 2.0 | 3,642 | 40.6% | +0.0107 | −84.3% |
| 60 | 2.5 | 3,531 | 44.9% | +0.0033 | −79.1% |
| 60 | 3.0 | 3,442 | 48.2% | −0.0016 | −75.7% |

**Best by ExpR:** period=30, ATR_mult=2.0 → ExpR=+0.0523, n=4,895, MaxDD(pct_eq)=−84.1%

**Critical finding:** No cell passes n≥50 AND DD<30%. Every parameter combination has >69% max
drawdown in the % equity model. The −127% DD in the original backtest was actually a modest
understatement of the real drawdown severity.

However — **the positive ExpR is consistent across all 20 cells** (except 60/3.0 which is flat).
Donchian has genuine positive expectancy. The problem is drawdown, not edge. This can be managed
by using very small position sizing (e.g., 0.25% risk/trade instead of 1%), which would make
the maximum drawdown approximately 25% of the trough seen here.

**Recommended params for production:** period=30, ATR_mult=2.0
This is a direct upgrade from the current production settings (period=20, ATR_mult=2.0) with
+0.026R improvement in expectancy.

---

## 5. Asymmetric Agent — Root Cause of Failure

### Signal gate analysis on BTC-USDT 15m (35,500 bars)

```
Bars failing BB squeeze gate (bbw > q15):   28,771  (81.1%)
Bars passing squeeze, failing breakout:       6,328  (17.8%)
Bars with breakout, low confluence (cc<3):      153   (0.4%)
Valid signals generated:                        137   (0.4%)
Converted to trades (agent not in position):    126
```

The squeeze gate is intentionally selective. 81% of bars are range-trading noise filtered out.
Only 0.4% of bars produce signals. This is correct design. The failure is in the trade math.

### Win rate disaster: 13.5%

```
TP hits:    17 / 126 = 13.5%   Avg R: +2.19R
SL hits:   109 / 126 = 86.5%   Avg R: −1.62R
Timeouts:    0 / 126 =  0.0%
```

**The 3:1 RR is working — but the fee-to-risk ratio destroys it.**

### The ATR stop problem

ATR on BTC 15m ≈ **221 points** at ~$94,000 price = **0.23% of price**.

```
SL distance    = 1 × ATR = 0.23%
TP distance    = 3 × ATR = 0.70%
Round-trip fee = 0.12%

Effective R on TP:  (0.70% − 0.12%) / 0.23% = +2.52R   (target; rarely hit)
Effective R on SL:  (−0.23% − 0.12%) / 0.23% = −1.52R  (penalty; often hit)

Fee cost as % of risk: 0.12% / 0.23% = 52%

Break-even WR: 1.52 / (2.52 + 1.52) = 37.6%
Actual WR:     13.5%
Gap:           24 percentage points — catastrophic
```

Fees eat **52% of the 1-ATR risk** on every trade. The 3×ATR target is almost never reached
because at compression points (low BBW), the first ATR of expansion is followed by a retest
or mean-reversion, not a 3× continuation. The mean outcome is a stopped-out trade before the
expected expansion materialises.

### First 20 signals on BTC (for reference)

```
[  1] 2025-04-25 11:15  long  entry=93981  tp=94644(+0.7%)  sl=93760(−0.2%)  ATR=221  cc=3
[  2] 2025-04-25 11:30  long  entry=94127  tp=94797(+0.7%)  sl=93903(−0.2%)  ATR=223  cc=3
[  4] 2025-04-28 23:30  long  entry=95015  tp=95732(+0.8%)  sl=94776(−0.3%)  ATR=239  cc=4
[ 14] 2025-05-07 13:45  long  entry=97170  tp=97708(+0.6%)  sl=96990(−0.2%)  ATR=180  cc=4  vr=6.1
[ 19] 2025-05-17 14:00  short entry=102663 tp=102139(−0.5%) sl=102838(+0.2%) ATR=175  cc=4  vr=5.9
```

Visible pattern: TP and SL are within 1% of entry. A single normal candle wick can stop these
trades out without any directional failure. The 0.2% SL is noise-level for BTC on 15m bars.

---

## 6. Proposed Fixes

**NOTE: No flags changed. These are recommendations for Saad's review.**

### Fix 1: Equity model (affects all future backtests)
Replace fixed-notional with `risk = equity × risk_pct`. Add halt at 10% of initial equity.
Report DD as %-of-equity. This makes all metrics interpretable and comparable.

### Fix 2: Asymmetric — minimum SL floor
Change SL: `sl_dist = max(2×ATR, entry × 0.008)` (0.8% minimum).
At 0.8% stop with 0.12% fees: fee/risk = 15% (vs 52% currently).
New break-even WR: 1.15 / (2.85 + 1.15) = 28.8% — achievable.
Also consider reducing TP to 2.5×ATR to increase hit rate.

### Fix 3: Asymmetric — partial TP
Book 50% at 1.5×ATR, trail remainder with 1×ATR trailing stop.
This converts many near-misses (price reaches 1.5×ATR then reverses) into partial wins.

### Fix 4: Momentum — filter stack (choose one or combine)
- Use limit orders for entry: saves 0.067R/trade, brings near breakeven
- Add volume filter: bar volume > 1.5× 20-bar average (not currently required)
- Tighten RSI: require 55–68 for long (vs current 50–72) to avoid weak setups

### Fix 5: Donchian — parameter update
Change from period=20 to period=30, ATR_mult stays at 2.0.
Expected improvement: +0.026R per trade (from +0.031 to +0.052).
At 4,895 trades/year this is meaningful.

---

## 7. Recommended Live-Trading Roster

**Current state: ALL three active agents (whale, news, donchian) on paper_only. ✅**

| Agent | Status | Recommendation | Confidence |
|---|---|---|---|
| donchian | paper_only | Monitor paper 30d; if live WR≥40% consider tiny live (0.25% risk) | MED |
| whale | paper_only | Keep paper — not backtestable | LOW |
| news | paper_only | Keep paper — useful as sentiment monitor | LOW |
| momentum | disabled | Re-test with limit entries + volume filter | LOW |
| asymmetric | disabled | Re-test with 2×ATR SL floor; conceptually valid setup | LOW |
| bb_squeeze | disabled | Re-test alongside asymmetric (same concept) | LOW |
| scalp | disabled | Remove — fees structurally destroy edge | NONE |
| swing | disabled | Remove — negative across all regimes | NONE |
| meanrev | disabled | Remove — too few signals, negative EV | NONE |
| ema_ribbon | disabled | Remove — noisier momentum clone | NONE |
| funding | disabled | Redesign — needs 8h funding rate history not live rate | NONE |

**Bottom line:** No agent is ready for live capital. Suggested 30-day paper trading milestone
before any live transition, with donchian at period=30/ATR=2.0 as the most promising candidate.

---

## 8. Infrastructure Quality Assessment

| Component | Finding | Confidence |
|---|---|---|
| BloFin candle data | 35,500 bars BTC 15m, timestamped correctly | HIGH |
| Entry model | Signal on bar close → entry at next open | HIGH |
| Fee model | 0.06% per side matches BloFin taker rate | HIGH |
| R-multiple math | 10-trade manual verification, 0 errors | HIGH |
| DD metric (fixed-notional) | Breaks > 100%; relative ranking still valid | LOW absolute, HIGH relative |
| DD metric (% equity) | Correct model; all agents reach ~0 equity | HIGH |
| Stop triggers (wick-based) | Appropriate for stop-market; slight pessimism for limit stops | MED |
| Same-bar conflicts | 0/400 = 0% on BTC — not a material issue | HIGH |
| Funding rate backtest | Cannot be done fairly without historical 8h rates | N/A |

---

*Report generated by overnight forensics — 2026-04-29 05:01 UTC*
*No agent flags (enabled/paper_only) were modified. All changes require Saad's review.*
