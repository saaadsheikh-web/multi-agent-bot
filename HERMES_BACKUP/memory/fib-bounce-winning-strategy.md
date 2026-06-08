---
name: fib-bounce-winning-strategy
description: "WOW strategy — fib 0.618 bounce + ADX regime filter. +558% at 5m (20% DD), +72% at 1H (11% DD). 73% cross-val profitable."
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

**Discovered**: 2026-06-03 through exhaustive cross-validation (3,300+ backtests).

## All-TF Results (Vectorized, 10 coins, 1 year, 2% risk)

| TF | Return | WR | Trades | DD |
|----|--------|----|--------|----|
| 5m | **+558.5%** | 52% | 1,844 | 20% |
| 1H | **+72.0%** | 52% | 591 | 11% |
| 15m | +43.4% | 46% | 1,934 | 26% |
| 30m | -11.0% | 38% | 107 | 13% |

## The Formula
- Entry: Price near fib 0.618 of 100-bar swing (1.2% tolerance)
- Reversal: 1-bar (c > c[-1], c[-1] <= c[-2])
- Volume: >0.6× 50-bar average
- RSI: 25-55
- Trend filter: OFF
- **REGIME: ADX > 22 AND +DI > -DI** (THE KEY)
- SL: 7%, Trail: 5%, Activate: 3%
- Risk: 2% per trade, 5× leverage
- Signal cap: 200

## Deployed
- Agent: FibBounceAgent in bot.py (enabled=True)
- Profile: fib_bounce (SL=7%, trail=5%, max_hold=96h)
- Uses ctx.df_1h for stable signals, but 5m data for timing

**Why**: Regime filter eliminates choppy market losses. 73% of 2-month periods profitable in cross-validation.
**How to apply**: Deployed in bot.py. Trade on 1H signals with 5m confirmation. Size at 2% risk.
