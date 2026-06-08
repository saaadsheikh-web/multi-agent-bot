# Hermes Learning Directive — 2026-06-07

## 1. SHORTS ARE DANGEROUS
- 148 shorts lost -$26.42 vs 210 longs lost only -$2.64
- Only short when trend_score ≤ -1 (strong DOWN trend)
- XMR, ICP, CL shorts were the biggest losers
- Default to LONG unless market is clearly falling

## 2. CONFIDENCE MATTERS
- ALL 15 losing trades on June 6-7 were conf=3
- Never trade conf=1-2 signals
- Conf=4+ signals have better win rate
- hermes_signals 3/6 agreement at score≥55 is the minimum

## 3. ENTRY HOURS ARE EVERYTHING
- 04:00 UTC = $27 loss (WORST) | 06:00 UTC = $18 loss
- 20:00 UTC = $15 profit (BEST) | 09:00 UTC = $10 profit
- Block hours 4, 6 UTC — hard rule

## 4. TRAIL PROTECTION RULES
- Breakeven ladder at +0.3% (not 0.5%)
- Trail activates at +1.0% (not 3.0%)
- 40% of losers had profit but trail never kicked in

## 5. WHICH AGENTS ACTUALLY WORK
- macd_cross: 31t, 71% WR, +$32 ← ONLY PROVEN WINNER
- funding_extremes: 26t, 54% WR, +$2.62
- hermes_master: most active, needs quality filter

## 6. WHICH SYMBOLS BLEED MONEY
- ICP, SOL, BCH, ZEC, BTC → blacklisted or restricted
- XMR, HYPE, BTCDOM → best performers

## 7. BACKTEST PROVEN
- daily_breakout 1H+5m: +2,310% | macd_cross 15m+5m: +29%
- viki 30m+5m: +14.5% | asymmetric 1H+15m: +15%
- fib_bounce 0.618: 73% profitable cross-validated

## 8. NEVER REPEAT
- 4 duplicate bots = rate limit hell
- Trail too late = profits turn to losses
- conf=3 shorts = guaranteed losers
- Silent crashes (vol_score_short bug)

## 9. DOCTOR CHECKS EVERY 30 MIN
Bot alive, port 8787, rate limits, duplicates, API health

## 10. MACD_CROSS IS THE GOLDEN CHILD
Only agent with proven live edge. 15m+5m. 2x size. Trust it.
