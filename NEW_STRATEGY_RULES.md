# NEW STRATEGY RULES — MANDATORY BEFORE ANY AGENT GOES LIVE
# Set by CEO: 2026-06-08

## RULE 1: MINIMUM 1 YEAR BACKTEST
Every new strategy MUST be backtested on 365 days of data minimum.
No exceptions. No "looks good on paper."

## RULE 2: EVERY TIMEFRAME
Test on ALL available timeframes:
- 5m
- 15m  
- 30m
- 1H
(Add 4H and 1D if data available)

## RULE 3: EVERY COIN WITH DATA
Test on ALL 46+ coins in backtest_data/.
A strategy that only works on 1 coin is not a strategy, it's luck.

## RULE 4: TEST 3 TIMES
Run the backtest 3 times to confirm consistency.
If results vary significantly (>10%), investigate why.
One pass could be luck. Three passes = proof.

## RULE 5: MULTIPLE TRAIL SETTINGS
Test each strategy with:
- No trail
- 0.5%, 1%, 2%, 3%, 5%, 10%, 20% fixed trail
- ATR-based trail (x1, x2, x3, x5)
- Step trail (breakeven at 1%, trail 50% of peak)

## RULE 6: MINIMUM PROFITABILITY
Strategy must show:
- Positive total R on at least 10+ coins
- Positive total PnL
- At least 30 trades (enough for statistical significance)
- Profit factor > 1.2

## RULE 7: DOCUMENT EVERYTHING
Save results to a report file with:
- Parameters tested
- Best/worst coin
- Optimal trail setting
- Expected R per trade
- Any failure cases

## RULE 8: COMPARE TO EXISTING WINNERS
New strategy must beat OR complement existing winners:
- breakout_12h 1H: +653R, 60% WR
- breakout_48h 30m: +233R, 67% WR
- fib_ext 15m: +111R, 73% WR
- trend_pullback 1H: +55R, 59% WR

If it doesn't beat these, it's redundant. Don't add it.

## RULE 9: NO "LOOKS GOOD" SHORTCUTS
Visual inspection of charts is NOT validation.
Paper trading is NOT validation.
Only backtest data over 1 year minimum counts.

## RULE 10: CEO APPROVAL
Every new strategy needs CEO_CONFIG.json update.
Nothing goes live without passing all 10 rules.
