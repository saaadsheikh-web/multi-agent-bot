---
name: permanently-banned
description: "Agents and patterns permanently banned — never suggest, mention, or deploy these again"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

# 🚫 PERMANENTLY BANNED — DO NOT USE

## Agents (Killed by Live P&L)
- **stoch_rsi**: 70 trades, -$11.33 — biggest loser
- **daily_breakout_24h**: 6 trades, -$10.89 — backtest lied (+78% paper, -$11 live)
- **tv_fibonacci**: 2 trades, -$10.09
- **daily_breakout_4h**: 3 trades, -$0.75
- **daily_breakout_2h**: 2 trades, +$0.22 — waste of CPU
- **connors_rsi2**: 162 trades, -$3.75 — overtrades
- **hurst_regime**: 20 trades, -$3.47
- **bb_bounce**: 5 trades, -$0.27
- **vwap_reversion**: 2 trades, -$1.43
- **zscore_reversion**: 11 trades, -$0.86

## Patterns Banned
- Tight trails (trail < 50% of SL)
- No regime filter
- >500 trades/year
- Trusting backtest over live P&L

## Current Bot (6 Survivors)
asymmetric, daily_breakout, daily_breakout_8h, macd_cross, viki, fib_bounce

**Why**: Live P&L is the only truth. These agents lost real money.
**How to apply**: Blocked in DEAD_AGENT_PURGE + class-level enabled=False. Hermes must never suggest re-enabling.
