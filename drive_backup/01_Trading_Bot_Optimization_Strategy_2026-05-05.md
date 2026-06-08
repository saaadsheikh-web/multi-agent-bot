# Trading Bot Optimization Strategy

**Source:** Google Drive (2026-05-05) — saaadsheikh@gmail.com
**Drive URL:** https://docs.google.com/document/d/1Zxg6jINLxyQgtZR6T-ZKRo6YQrU6piEKKRlOXH7BYHw/edit
**Saved locally:** 2026-05-18 by Claude (Cowork)

---

## The Fee Answer (and a Shocking Finding)

**Fees:** $2.51 estimated total (mixed taker/maker rate)

| Scenario | Fee Cost |
|---|---|
| Worst case (all taker, 0.06% × 2 sides) | $3.77 |
| Real-world mixed (0.04% × 2 sides) | $2.51 |
| Best case (all maker, 0.02% × 2 sides) | $1.26 |

**Pre-fee gross profit:** +$2.33
**After realistic fees:** −$0.18 to +$1.08

The bot is roughly break-even after fees. Fees ate ~100% of the edge. This is the single biggest leak.

---

## The Shocking Confidence Finding

| Confidence | n | WR | PnL | Avg/trade |
|---|---|---|---|---|
| ≤7 (low) | 3 | 100% | +$2.21 | +$0.74 |
| 8 | 9 | 11% | −$0.02 | −$0.00 |
| 9 | 1 | 100% | +$0.43 | +$0.43 |
| 10 (highest) | 23 | 39% | −$0.28 | −$0.01 |

**Confidence is inverted.** The "10/10 conviction" trades LOST money on average. Scaling up high-conf trades right now would lose more, not less.

---

## Should you size up to $200/trade? Use 10–30x leverage?

**Short answer: NO. Not yet.**

### Bigger trades scale fees linearly

| Avg/trade | Gross | Fees | Net |
|---|---|---|---|
| $87 (current) | +$2.33 | $2.51 | −$0.18 |
| $200 | +$5.36 | $5.77 | −$0.41 |
| $500 | +$13.30 | $14.40 | −$1.10 |

Doubling size doesn't double profit — it doubles fees too.

### Higher leverage doesn't make winners bigger — it makes losers fatal

- 5× leverage → liquidation at ~20% adverse move (huge buffer)
- 10× → liq at ~10% (safe)
- 20× → liq at ~5% (one wick wipes you)
- 30× → liq at ~3.3% (one bad candle = wiped)
- 50×+ → suicide

Worst single-trade move on the bot was −2.27%. At 30× a 3.5% wick liquidates before SL fires.

---

## What WILL make more money — ranked

1. **Make the bot use MAKER orders** ⭐ BIGGEST LEVER
   - Cuts fees ~70% ($2.51 → $0.83)
   - Same trades become +$1.50 net instead of −$0.18
2. **Fix the inverted confidence scoring** — weight by historical agent accuracy, not headcount
3. **Confidence-graded sizing** (AFTER fixing #2): conf 6-7 = $50, conf 8 = $80, conf 9 = $120, conf 10 = $180
4. **Wider TPs for shorts** — push 2% → 3.5–4%. Est +$1–1.50 lift / 35 trades
5. **Modest size-up only on connors_rsi2** on BTC, CL, XAG, GIGGLE, HYPE at $120–150
6. **Keep leverage 5–10× max**

## DO NOT

- ❌ Don't go 20×+ leverage
- ❌ Don't blanket-double trade size
- ❌ Don't trust conf-10 trades right now
- ❌ Don't size up untested agents

## The Real Path (in order)

1. Switch to maker orders → fees drop 70% → strategy actually profitable
2. Kill the bleeders (hurst_regime + 3 daily_breakouts + fibonacci)
3. Fix confidence scoring
4. THEN size up connors_rsi2 to $120/trade
5. THEN add the funding-rate agent

Expected after all 5: **+$15–20 net per 35 trades** vs current break-even.
