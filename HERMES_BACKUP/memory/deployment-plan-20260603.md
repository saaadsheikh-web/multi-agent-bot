---
name: deployment-plan-20260603
description: "Final deployment plan from comprehensive backtest — what to enable, disable, modify, and how to scout new coins"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

Deployment plan based on comprehensive 44-agent backtest (2026-06-03).

**Changes applied to bot.py**:
- ✅ ENABLED: asymmetric (was disabled, +13% at 1H)
- ❌ DISABLED: trend_pullback, golden_cross, kalman_trend, rsi_divergence (all losing)

**Winner formula** (extracted from backtest):
- 500-3,000 trades/year
- 55-80% win rate
- 1H timeframe (best) or 15m (second best)
- Trailing stop with SL:trail ratio ≥ 2:1
- Volume confirmation on entry
- WIDER trails — don't choke winners

**Coin scout approach**:
- Score every coin by: daily range, ADX trend, fib levels, ATR, volume trend, RSI, spread
- Match high-scoring coins to best strategy
- Priority adds: SUI, DOGE, BNB, XRP, ADA, TAO, TIA, APT
- Drop: SOL from most strategies

**Files**: 
- [[comprehensive-backtest-20260603]] — full backtest results
- [[backtest-statistical-findings]] — statistical patterns
- [[backtest-agent-recommendations]] — per-agent actions
- [[trail-stop-strategy]] — why tight trails kill
- bot.py — changes applied
- COIN_SCOUT_PLAN.md — scout logic

**Why**: To deploy the empirically best configuration and continuously find new profitable coins
**How to apply**: Bot is already updated. Run the coin scout every 4 hours. Monitor asymmetric performance.
