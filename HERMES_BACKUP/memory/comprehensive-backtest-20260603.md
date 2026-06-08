---
name: comprehensive-backtest-20260603
description: "Full backtest of all 44 agents across 4 timeframes — top performers, statistical findings, agent recommendations, Viki results, confirmation impact"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

Comprehensive backtest 2026-06-03: 44 agents × 4 timeframes (5m, 15m, 30m, 1H) × 20 symbols, 1 year, 5× leverage, compounding. 237 results, 103.7 min runtime.

**Top agent**: daily_breakout @ 1H = +1,992% (909 trades, 73.9% WR, 50.2% DD)
**Best TF**: 1H — only TF with positive avg return (+81.3%), 41% profitable
**Confirmation**: helps 76% of strategies, avg +6.9% improvement. Best pairs: 1H→15m, 15m→5m

**Key stats**: See [[backtest-statistical-findings]] for WR correlation, trade count sweet spot, native vs non-native analysis
**Agent recommendations**: See [[backtest-agent-recommendations]] for which to keep/enable/disable/modify
**Viki update**: See [[viki-strategy]] — best at 30m+5m confirm (+14.5%), not 15m native (-31.4%)

**Files**: COMPREHENSIVE_BACKTEST_20260603.md (summary), COMPREHENSIVE_BACKTEST_ANALYSIS_20260603.md (deep analysis), JSON+CSV in backtest_results/ and hermes-agent/

**Why**: To empirically determine which strategies work at which timeframes, optimize the bot's agent roster
**How to apply**: 
- Deploy daily_breakout @ 1H as primary strategy
- Move Viki to 30m + 5m confirmation
- Enable asymmetric @ 1H
- Disable ema_ribbon, momentum, hurst_regime
- Default all new strategies to 1H timeframe
- Target 65%+ WR and 500-2000 trades/year for new strategies
