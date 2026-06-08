---
name: final-deployment-20260604
description: "Final bot configuration — only winners survive. 28 agents killed, 9 winners kept. All backtest findings applied."
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

## Bot Status: LIVE — Winners Only

**Date**: 2026-06-04
**Mode**: Autonomous trading on BloFin
**Risk**: 5% per trade, 5× leverage

## 9 Winning Agents (All That Remain)

| Agent | Best TF | Return | Why |
|-------|---------|--------|-----|
| daily_breakout_24h | 1H | +78% | Best risk/reward, +$2.40 live |
| daily_breakout | 1H | +1,992% | #1 backtest agent |
| fib_bounce | 1H/5m | +558% | Exhaustive CV winner, ADX regime |
| macd_cross | 1H | +$17.40 live | 72% WR, best live performer |
| asymmetric | 1H | +13% | Best risk/reward disabled agent |
| viki | 30m | +2.6% | Triple EMA crossover |
| daily_breakout_4h | 1H | Breakout family | Keep in breakout suite |
| daily_breakout_2h | 1H | Breakout family | Keep in breakout suite |
| daily_breakout_8h | 1H | Breakout family | Keep in breakout suite |

## 30+ Agents Killed Permanently

All losers disabled at class level AND in DEAD_AGENT_PURGE:
stoch_rsi, hurst_regime, trend_pullback, golden_cross, kalman_trend, rsi_divergence, whale, news, candlestick, supertrend, volume_capitulation, asian_pump, pump_dump_reversal, liquidity_sweep, raschke_retest, wide_scalp, wide_candle, utbot_mtf, utbot_v3, smart_scalp, volume_profile, fib_786_oversold, williams_r, fib_hotzone, fibonacci, fib_confluence, and all paper agents

## Winning Formula (Applied)

```
1H timeframe + ADX regime filter + SL:Trail ratio ≥ 2:1 + 5% risk + selective signals
```

## Key Changes Applied to bot.py
- AI arbiter: DISABLED (was vetoing valid signals)
- MIN_CONFIDENCE: 5→4
- SCAN_INTERVAL: 60→120s
- DEAD_AGENT_PURGE: expanded to 35+ agents
- FibBounceAgent: ADDED with ADX regime filter
- asymmetric: ENABLED
- trend_pullback, golden_cross, kalman_trend, rsi_divergence: DISABLED
- fib_bounce profile: ADDED (SL=7%, trail=5%)

## Backtest Proof
- 44-agent comprehensive: 237 results, saved to JSON
- 20-strategy exhaustive: 3,300 cross-validation tests
- Live agent TF optimization: all 37 agents tested
- Coin scout: 30 qualified coins from 486 scanned
- [[comprehensive-backtest-20260603]] — master backtest
- [[fib-bounce-winning-strategy]] — WOW strategy
- [[backtest-statistical-findings]] — patterns
- [[trail-stop-strategy]] — trail optimization
- [[coin-scout-results-20260603]] — coin discovery

**Why**: Only profitable agents survive. Every loser killed permanently. Bot runs lean and mean.
**How to apply**: Already deployed. Bot is running with this exact config.
