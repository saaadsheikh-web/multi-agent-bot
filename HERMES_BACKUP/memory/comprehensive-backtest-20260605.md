---
name: comprehensive-backtest-20260605
description: "Complete backtest — all 35 agents × all timeframes × 10 symbols, June 5 2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: 21124681-62b2-45f5-903c-fd0266b8fe16
---

## COMPREHENSIVE BACKTEST — 2026-06-05
46 agents tested, 226 results, 35 with trade data, 94.5 min runtime
Saved: comprehensive_backtest_20260605_233144.json (430KB)

## ALL AGENTS — BEST TIMEFRAME

| Agent | Best TF | Return | Trades | WR | DD |
|---|---|---|---|---|---|
| daily_breakout | 1H +5m | +2,310% | 902 | 75% | 50% |
| daily_breakout_24h | 1H +5m | +1,022% | 2,724 | 59% | 78% |
| zscore_reversion | 1H | +794% | 9,315 | 54% | 58% |
| fib_confluence | 1H +5m | +239% | 1,806 | 53% | 44% |
| fibonacci | 1H | +172% | 2,839 | 52% | 77% |
| liquidity_sweep | 1H | +125% | 2,161 | 51% | 34% |
| wide_scalp | 1H | +113% | 3,658 | 63% | 12% |
| fib_hotzone | 15m | +93% | 366 | 56% | 7% |
| utbot_v3 | 15m +5m | +79% | 933 | 64% | 29% |
| utbot_mtf | 1H | +62% | 1,829 | 80% | 40% |
| macd_cross | 15m +5m | +29% | 675 | 50% | 23% |
| asymmetric | 1H +5m | +15% | 321 | 41% | 10% |
| viki | 30m +5m | +15% | 34 | 79% | 7% |
| williams_r | 1H +5m | +13% | 78 | 62% | 4% |
| stoch_rsi | 15m | +13% | 1,404 | 49% | 36% |
| connors_rsi2 | 1H | +12% | 187 | 62% | 7% |
| donchian | 15m +5m | +11% | 2,530 | 47% | 52% |
| candlestick | 5m | +8% | 44 | 50% | 6% |
| bb_bounce | 30m +5m | +6% | 58 | 71% | 1% |
| vwap_reversion | 15m | +5% | 1,236 | 50% | 38% |

## LOSERS (negative at ALL timeframes)
ema_ribbon (-93%), momentum (-53%), hurst_regime (-39%), golden_cross (-17%), trend_pullback (-12%), rsi_divergence (-11%)

## 6 SURVIVORS CONFIGURED
1. daily_breakout — 1H primary (correct)
2. macd_cross — 15m + 5m confirm (+29% vs -50% at 1H)
3. asymmetric — 1H + 15m confirm (+15% vs -17% at 15m)
4. viki — 30m + 5m confirm (+15% vs -31% at 15m)
5. daily_breakout_8h — 1H, paper_only removed
6. fib_bounce — 1H (not in this dataset, separate backtest)

## KEY FINDINGS
- Lower-TF confirmation improves 68 tests, worsens 18, avg +7.6%
- 1H is the dominant winning TF for most agents
- 15m is terrible for viki and asymmetric, great for macd_cross
- Entry speed matters: 5m confirm on 15m/30m primary beats 1H-only

**Data files:**
- JSON: /Users/saad/multi_agent_bot/backtest_results/comprehensive_backtest_20260605_233144.json
- CSV: /Users/saad/multi_agent_bot/backtest_results/comprehensive_backtest_20260605_233144.csv
