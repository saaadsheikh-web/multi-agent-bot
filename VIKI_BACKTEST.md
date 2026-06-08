# VIKI Backtest Report — 2026-06-03

**Strategy:** Triple EMA 9/21/50 crossover on 15-minute candles
**Period:** 28 Feb – 1 May 2026 (63 days)
**Symbols:** SOL-USDT, TAO-USDT, TIA-USDT

## Optimal Settings

| Parameter | Value |
|---|---|
| Timeframe | 15 minutes |
| Entry | 9 EMA crosses 21 EMA, both on same side of 50 EMA |
| Stop Loss | 7% (hard) |
| Trail Activate | +3% profit |
| Trail Distance | 1.5% behind peak |
| Max Hold | 4 days |
| Leverage | 10× |
| Risk per trade | 10% of balance |

## Results

| Metric | Value |
|---|---|
| Starting balance | $100.00 |
| Final balance | $167.92 |
| Return | +67.9% |
| Peak balance | $206.26 |
| Max drawdown | 18.6% |
| Total trades | 65 |
| Win rate | 81.5% (53W / 12L) |
| Avg win | +$3.63 (+2.45%) |
| Avg loss | -$10.39 (-6.13%) |
| Max loss streak | 3 |
| Avg hold time | 27 hours |

## By Symbol

| Symbol | Trades | Win Rate | P&L |
|---|---|---|---|
| TAO-USDT | 25 | 84% | +$35.42 |
| SOL-USDT | 22 | 77% | +$20.91 |
| TIA-USDT | 18 | 83% | +$11.60 |

## By Exit

| Exit | Trades | Win Rate | P&L |
|---|---|---|---|
| TRAIL_STOP | 49 | 100% | +$186.35 |
| TIMEOUT | 5 | 80% | -$1.04 |
| SL_HIT | 9 | 0% | -$104.59 |
| EOD_FORCED | 2 | 0% | -$12.79 |

## Weekly P&L

| Week | P&L | Trades |
|---|---|---|
| 1 | +$1.11 | 9 |
| 2 | +$7.15 | 7 |
| 3 | +$38.68 | 12 |
| 4 | +$34.91 | 8 |
| 5 | +$10.35 | 6 |
| 6 | -$5.27 | 7 |
| 7 | -$7.00 | 9 |
| 8 | +$2.75 | 5 |
| 9 | -$14.75 | 2 |

---

## 1-Year Backtest (Updated 2026-06-03)

| Metric | Value |
|---|---|
| Period | 365 days (Jun 2025 – Jun 2026) |
| Starting | $100.00 |
| Final | $22.69 |
| Return | −77.3% |
| Trades | 432 |
| Win rate | 69.4% (300W / 132L) |
| SL hits | 117 (27% of trades) |
| Trail winners | 292/292 (100% WR on trailed) |

**Verdict:** Strategy profitable in trending periods, loses in choppy/ranging.
Needs regime filter (TRENDING only) or wider SL.
