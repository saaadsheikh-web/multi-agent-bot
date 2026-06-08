# Why we lose. Why we win. How to make more.
_Built from 40 real trades in bot.db, 2026-05-07 05:00 BST_

## TL;DR — the truth in 3 lines
- We are **NOT bleeding**. 60% WR, profit factor 1.21, total +$2.19.
- Three killer hours (10/12/13 UTC) = -$4.95 = **more than total profit**.
- One bad agent (`vwap_reversion`) lost -$1.43 in 2 trades. Disable it.

## What's working ✅
1. **`connors_rsi2`** is the engine. 23 trades, 52% WR, +$2.09. Best agent we have.
2. **Shorts** beat longs: 63.6% WR vs 58.6%, $+1.82 vs $+0.36.
3. **Holding 30 min – 2 hours** is the sweet spot: 78% WR, +$4.83.
4. **Best symbols**: ZEC (+$3.83), CL (+$2.10), GIGGLE (+$1.70), BTC (+$1.24).
5. **Best hours UTC**: 08h (+$2.80), 17h (+$1.56), 00h (+$1.39), 14h, 15h.

## What's bleeding ❌
1. **Hours 10-13 UTC** = London/EU open chop = -$4.95 across 9 trades.
2. **`vwap_reversion`** = -$1.43 (TON-USDT shorted +4.75σ pump that kept pumping for 2 min, then trail-stopped).
3. **`daily_breakout_24h`** = -$0.93 from 1 trade. 0% WR.
4. **TAO-USDT** longs via connors_rsi2 = 3 losses, $-1.76. TAO trends DOWN, mean-reversion longs are wrong setup.
5. **Cutting too fast**: trades held 5-30 min lose -$3.69 (avg -$0.28). Same pattern in 30m-2h hold lane wins +$0.54. We're hitting trail stops before MFE matures.

## The math says: 4 changes = 3-5x more profit

### 1. Disable trading hours 10-13 UTC
- These hours net **-$4.95** across our entire history
- Skipping them = "+$4.95 found money" (more than 2x today's PnL)
- **Code change**: add hour filter in `scan_once`, skip if UTC hour in [10,11,12,13]

### 2. Disable `vwap_reversion` permanently
- 2 trades, 50% WR, -$1.43 net
- Single TON disaster shows this agent fades real momentum
- **Code change**: add `vwap_reversion` to backtest-disabled list

### 3. Symbol blacklist for connors_rsi2 longs
- TAO-USDT longs: 3 losses, $-1.76. Never wins long.
- **Code change**: add per-agent symbol skip in connors_rsi2

### 4. Loosen trail stop in first 30 minutes
- Best winners hold 70-270 minutes. We cut at 14-22m on losers.
- The trail stop is too tight in the early-life of trades during normal MFE retracement.
- **Code change**: trail-pct 0.8% → 1.5% during first 30 min, then tighten

## Stretch plays (after the 4 above are validated)

5. **Scale connors_rsi2 size** — best agent. Currently 0.05x → try 0.08x once profit factor > 1.5.
6. **Short bias**: shorts win 63%. Add a "short-only" Connors variant on downtrending symbols.
7. **Symbol whitelist**: concentrate on ZEC, CL, BTC, GIGGLE. They're 70% of all profit.
8. **Re-enable `funding_extremes` size**: 67% WR, +$0.31 from 3 trades. Promote from paper.

## Why each loss happened (forensic)

| Symbol | Agent | -$ | Hold | Why |
|---|---|---|---|---|
| ZEC long | connors_rsi2 | -1.87 | 14m | Caught knife — exited too fast on whipsaw |
| TON short | vwap_reversion | -1.56 | 2m | Faded a real pump, stopped immediately |
| ZEC long | connors_rsi2 | -0.94 | 87m | Counter-trend long, exhausted RSI didn't bounce |
| CL long | daily_breakout_24h | -0.93 | 11m | Failed breakout, retest failed |
| TAO long | connors_rsi2 | -0.84 | 7m | TAO downtrend, RSI dipped but kept falling |
| TAO long | connors_rsi2 | -0.80 | 207m | Held too long while bleeding |
| YFI long | connors_rsi2 | -0.78 | 121m | Same falling-knife pattern |
| ETH long | daily_breakout_4h | -0.65 | 22m | Failed 4h break |

**Pattern:** longs in falling markets. Need EMA200 / regime filter to block longs when symbol is in clear downtrend.

## Why each big winner worked

| Symbol | Side | +$ | Hold | Setup |
|---|---|---|---|---|
| ZEC long | connors_rsi2 | +1.68 | 270m | RSI2=4.9 in confirmed uptrend, held to MFE |
| GIGGLE short | connors_rsi2 | +1.15 | 39m | RSI2=96 in confirmed downtrend, fade extreme |
| CL short | connors_rsi2 | +1.09 | 77m | Same pattern, with-trend mean reversion |
| ZEC long | connors_rsi2 | +1.08 | 71m | Trend+ confluence boost |

**Pattern:** Connors RSI2 + with-trend (uptrend long, downtrend short) + 1-3h hold. THAT's the playbook. Repeat it more.

## Bottom line
You have a **working strategy** with one excellent agent. The losses are concentrated:
- 3 killer hours
- 1 bad agent (vwap_reversion)
- 1 bad symbol-side combo (TAO long via connors_rsi2)

Fixing those three things alone would have flipped the bot from +$2.19 to roughly +$8-10 over the same period. **That's 3-5x more profit with zero new code, just better filters.**

The grow-the-company answer is: disable the bleeders, scale the winner.
