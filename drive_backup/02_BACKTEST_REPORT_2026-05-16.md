# BACKTEST REPORT — From Google Drive

**Source:** Google Drive (2026-05-16) — saaadsheikh@gmail.com
**Drive URL:** https://docs.google.com/document/d/1CQsG9oPeZaCHWVSjKuMGkI1hfo11eWA_C2BMKXL5YlM/edit
**Generated:** 2026-05-16T03:15:49Z
**Saved locally:** 2026-05-18 by Claude (Cowork)

---

## Verdict Table — Agents to KEEP & SCALE 🟢

| Agent | Trades | WR | Exp_R | DD(eq) | PF | Sharpe |
|---|---|---|---|---|---|---|
| daily_breakout_4h | 5,696 | 77.2% | +0.726 | −20.7% | 4.98 | 6.00 |
| daily_breakout | 576 | 82.1% | +0.670 | −9.8% | 5.83 | 2.88 |
| daily_breakout_2h | 6,900 | 74.0% | +0.604 | −17.5% | 3.99 | **15.84** |
| daily_breakout_24h | 2,014 | 82.6% | +0.573 | −11.9% | 5.22 | 3.95 |
| daily_breakout_12h | 3,437 | 79.9% | +0.548 | −17.5% | 4.81 | 6.22 |
| daily_breakout_48h | 805 | 78.3% | +0.507 | −15.3% | 3.71 | 3.46 |
| daily_breakout_8h | 1,736 | 77.8% | +0.488 | −6.2% | 4.02 | 10.75 |
| asian_pump | 36 | 83.3% | +0.399 | −0.3% | 37.49 | 23.20 |

## KEEP 🟡 (working but smaller edge)

| Agent | Trades | WR | Exp_R | PF | Sharpe |
|---|---|---|---|---|---|
| trend_pullback | 1,241 | 73.0% | +0.213 | 1.95 | 5.09 |
| macd_cross | 1,396 | 75.2% | +0.203 | 2.16 | 7.57 |

## TUNE 🟠 (marginal)

| Agent | Trades | WR | Exp_R | PF |
|---|---|---|---|---|
| donchian | 988 | 51.6% | +0.043 | 1.13 |
| rsi_divergence | 1,013 | 46.7% | +0.018 | 1.04 |

## KILL 🔴 (losers — backtest confirmed)

- meanrev (45.1% WR, -0.060 Exp_R)
- candlestick (42.0% WR, -0.061)
- momentum (43.1% WR, -0.091, 15K trades, −95% DD)
- ema_ribbon (43.4% WR, -0.097, 10K trades, −95% DD)
- bb_squeeze (41.3% WR, -0.136, 2K trades, −95% DD)
- scalp (46.2% WR, -0.179)
- asymmetric (40.0% WR, -0.188)
- swing (34.8% WR, -0.330)
- volume_capitulation (0% WR, -0.979, 10 trades)
- funding, daily_breakout_4h_trend, daily_breakout_7d, pump_dump_reversal, supertrend — 0 trades, dead code

---

## Combined 20-symbol leaderboard — appended 2026-05-16 03:17 UTC

| Agent | Trades | WR | Exp_R | DD(eq) | PF | Sharpe | PASS |
|---|---|---|---|---|---|---|---|
| daily_breakout_2h | 26,292 | 73.7% | +0.560 | −23.5% | 3.90 | 15.80 | ✅ |
| daily_breakout_8h | 6,258 | 76.4% | +0.449 | −9.0% | 3.71 | 10.63 | ✅ |
| macd_cross | 5,652 | 74.1% | +0.221 | −17.3% | 2.19 | 8.63 | ✅ |
| daily_breakout_4h | 22,192 | 76.4% | +0.673 | −22.4% | 4.75 | 6.16 | ✅ |
| daily_breakout_12h | 13,110 | 78.5% | +0.497 | −24.1% | 4.26 | 5.70 | ✅ |
| trend_pullback | 5,016 | 70.4% | +0.193 | −22.2% | 1.76 | 4.63 | ✅ |
| daily_breakout_24h | 8,096 | 81.2% | +0.520 | −18.7% | 4.76 | 3.86 | ✅ |
| daily_breakout | 2,338 | 82.6% | +0.595 | −13.3% | 5.30 | 2.55 | ✅ |

**Note:** Live data is overriding the backtest for `daily_breakout_24h` (live: 0% WR / 3 trades / −$0.93). The backtest says PASS, live says KILL. Trust live.

---

## Per-Agent Detail (top winners)

### daily_breakout_4h 🟢 KEEP & SCALE
- Top coins: OP-USDT (+0.83R, n=550), ARB-USDT (+0.82R, n=546), TIA-USDT (+0.78R, n=570), SUI-USDT (+0.75R, n=675), NEAR-USDT (+0.73R, n=567)
- Worst coins (still positive): INJ-USDT (+0.70R), ATOM-USDT (+0.66R), LTC-USDT (+0.54R)
- Avg hold: 65 min

### daily_breakout_2h 🟢 KEEP & SCALE
- Top coins: INJ-USDT (+0.71R, n=695), TAO-USDT (+0.69R, n=882), OP-USDT (+0.66R, n=709), ARB-USDT (+0.65R, n=551), NEAR-USDT (+0.63R, n=680)
- Avg hold: 29 min
- **Sharpe 15.84 — best in cohort**

### asian_pump 🟢 KEEP & SCALE
- Top coins: ARB-USDT (+0.68R, n=6), TAO-USDT (+0.66R, n=5)
- **PF 37.49, Sharpe 23.20** — strongest single signal, but n=36 small
