---
name: never-do-again
description: Rules from live trading losses — never repeat these mistakes
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

# 🚫 RULES — NEVER DO AGAIN

## RULE 1: Backtest Winners ≠ Live Winners
**daily_breakout_24h was +78% in backtest, -$10.89 live.**
Backtests assume perfect fills, no slippage, no rate limits. The real world is different.
**Rule**: Any agent with >5 live trades and negative P&L gets killed immediately. Trust live data over paper.

## RULE 2: Win Rate Alone Means Nothing
**stoch_rsi had 55% WR but lost -$11.33. connors_rsi2 had 52% WR, lost -$3.75.**
High WR with bad risk/reward = death by a thousand cuts.
**Rule**: Kill any agent where avg loss > avg win (R:R < 1:1).

## RULE 3: Tight Trails Kill
**trend_pullback: 63% WR, -47% return. Trail 1.5% vs SL 2.5% = one loss eats 1.7 wins.**
**Rule**: Trail must be ≥50% of SL distance. SL=7% means trail≥3.5%.

## RULE 4: No Regime Filter = Gambling
**Agents without ADX/trend filters lose in choppy markets.**
**Rule**: Every agent must have a regime filter. No filter = no trades.

## RULE 5: Overtrading Destroys Accounts
**ema_ribbon: 28,473 trades, -100% return. connors_rsi2: 162 trades in a week.**
**Rule**: Cap signals at 200 max. Quality > quantity. If an agent fires >500 trades in a year, kill it.

## RULE 6: Live Data Over Backtests
**Lifetime P&L from bot.db is the ONLY truth.**
Paper backtests are directionally useful but live P&L is the final judge.
**Rule**: Check bot.db weekly. Kill any agent with negative lifetime P&L over >5 trades.

## RULE 7: Only Keep Proven Winners
After 344 live trades across all agents, ONLY macd_cross is truly profitable (+$17.41, 30t, 72% WR).
**Rule**: New agents start in paper mode. Only promote to live after 10+ paper trades with positive P&L.

---

**Current kills applied**: stoch_rsi, daily_breakout_24h, daily_breakout_4h, daily_breakout_2h, tv_fibonacci, + 30 more
**Only survivors**: macd_cross, asymmetric, viki, fib_bounce, daily_breakout, daily_breakout_8h
