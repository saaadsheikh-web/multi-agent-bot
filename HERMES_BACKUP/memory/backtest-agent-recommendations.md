---
name: backtest-agent-recommendations
description: "Which agents to keep, enable, disable, or modify based on comprehensive backtest"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

Agent deployment recommendations from comprehensive backtest 2026-06-03:

**KEEP ENABLED (profitable at best TF)**:
- daily_breakout @ 1H: +1,992% (909t, 73.9% WR, 50.2% DD)
- daily_breakout_24h @ 1H: +618% (2,787t, 58.8% WR, 78.6% DD)
- fib_confluence @ 15m: +191% (9,335t, 48% WR, 88.7% DD)
- fibonacci @ 1H: +172% (2,839t, 51.5% WR, 77.1% DD)
- liquidity_sweep @ 1H: +125% (2,161t, 51.2% WR, 33.5% DD)
- wide_scalp @ 1H: +113% (3,658t, 63.2% WR, 12.2% DD)
- fib_hotzone @ 15m: +93% (366t, 55.7% WR, 7.4% DD) — best risk/reward
- volume_capitulation @ 1H: +86% (296t, 79.1% WR, 14.3% DD)
- utbot_mtf @ 1H: +62% (1,829t, 79.7% WR, 40.2% DD)
- utbot_v3 @ 15m: +58% (1,038t, 62.9% WR, 34.4% DD)
- williams_r @ 5m: +9% (668t, 51.2% WR, 11.9% DD)
- candlestick @ 5m: +8% (44t, 50% WR, 6.0% DD)
- pump_dump_reversal @ 1H: +14% (20t, 75% WR, 5.9% DD) — too few trades
- supertrend @ 1H: +4% (1t, 100% WR) — only 1 trade, unreliable

**ENABLE (currently disabled but profitable)**:
- zscore_reversion @ 1H: +794% — needs signal cap (9,315 trades is too many)
- asymmetric @ 1H: +13%, 333t, 10.7% DD — BEST risk-adjusted disabled agent
- connors_rsi2 @ 1H: +12%, 187t, 6.7% DD — very safe, low DD

**MODIFY**:
- Viki: move from 15m → 30m + 5m confirmation (+14.5% vs -31.4%)
- macd_cross: add 5m confirmation at 15m (-15.8% → +22.4%)
- donchian: add 5m confirmation at 15m (-17.2% → +11.4%)

**DISABLE (losing at ALL timeframes)**:
- ema_ribbon: -97.7% to -100%
- momentum: -60% to -94%
- hurst_regime: -72% to -100%
- golden_cross: -27% to -100%
- kalman_trend: -7% to -68% (all negative)
- bb_bounce: -13% to -66% (all negative)

**DATA-DEPENDENT (need external data, can't backtest with OHLCV)**:
- whale: order book data needed
- news: news headlines needed
- funding: funding rate data needed

**Why**: To optimize the bot's agent roster based on empirical backtest data
**How to apply**: Enable/disable agents in bot.py, change Viki to 30m, add confirmation filters
