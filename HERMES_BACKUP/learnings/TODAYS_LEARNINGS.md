# Learning Agent Report — 2026-06-08

## Overall Performance

- Closed trades: 379
- Win rate: 50.7%
- Total PnL: $-17.09
- Avg PnL/trade: $-0.05
- Avg win: $0.84
- Avg loss: $-0.95

## Per-Agent Performance

| Agent | Trades | WR | Total PnL | Avg/trade |
|---|---|---|---|---|
| macd_cross | 31 | 71.0% | $32.37 | $1.04 |
| funding_extremes | 26 | 53.8% | $2.62 | $0.1 |
| fibonacci | 4 | 50.0% | $0.79 | $0.2 |
| tradingview | 1 | 100.0% | $0.43 | $0.43 |
| daily_breakout_2h | 2 | 100.0% | $0.22 | $0.11 |
| bb_bounce | 5 | 40.0% | $-0.27 | $-0.05 |
| daily_breakout_4h | 3 | 33.3% | $-0.75 | $-0.25 |
| zscore_reversion | 11 | 63.6% | $-0.86 | $-0.08 |
| vwap_reversion | 2 | 50.0% | $-1.43 | $-0.71 |
| hurst_regime | 20 | 25.0% | $-3.47 | $-0.17 |
| connors_rsi2 | 162 | 47.5% | $-3.75 | $-0.02 |
| tv_fibonacci | 2 | 0.0% | $-10.09 | $-5.04 |
| hermes_master | 34 | 55.9% | $-10.71 | $-0.31 |
| daily_breakout_24h | 6 | 16.7% | $-10.89 | $-1.81 |
| stoch_rsi | 70 | 54.3% | $-11.33 | $-0.16 |

## Per-Symbol Performance

| Symbol | Trades | WR | Total PnL |
|---|---|---|---|
| HYPE-USDT | 40 | 55.0% | $18.13 |
| ATOM-USDT | 1 | 100.0% | $14.52 |
| XAG-USDT | 9 | 66.7% | $7.24 |
| SNDK-USDT | 4 | 50.0% | $5.78 |
| XMR-USDT | 24 | 54.2% | $5.54 |
| AMD-USDT | 6 | 66.7% | $5.36 |
| XPT-USDT | 4 | 50.0% | $2.09 |
| VVV-USDT | 3 | 100.0% | $2.0 |
| GIGGLE-USDT | 5 | 80.0% | $1.95 |
| BTCDOM-USDT | 17 | 41.2% | $1.66 |

## Long vs Short

- **long**: 229 trades, 50.7% WR, total $15.19
- **short**: 150 trades, 50.7% WR, total $-32.28

## Time-of-Day (UTC)

Top profitable hours:
- 04:00 UTC — 16 trades, $19.35 total
- 21:00 UTC — 19 trades, $13.24 total
- 14:00 UTC — 37 trades, $7.58 total
- 07:00 UTC — 15 trades, $4.45 total
- 10:00 UTC — 13 trades, $3.58 total

Worst hours:
- 05:00 UTC — 24 trades, $-20.21 total
- 08:00 UTC — 16 trades, $-16.47 total
- 18:00 UTC — 12 trades, $-13.22 total

## Actionable Insights

- **KILL/RESTRICT**: `hermes_master` — 34 trades, WR 56%, net $-10.71, worst -264%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `daily_breakout_24h` — 6 trades, WR 17%, net $-10.89, worst -266%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `stoch_rsi` — 70 trades, WR 54%, net $-11.33, worst -203%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `daily_breakout_4h` — 3 trades, WR 33%, net $-0.75, worst -125%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `zscore_reversion` — 11 trades, WR 64%, net $-0.86, worst -191%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `connors_rsi2` — 162 trades, WR 48%, net $-3.75, worst -227%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `bb_bounce` — 5 trades, WR 40%, net $-0.27, worst -117%. Disable or paper-only until backtest re-validates.
- **KILL/RESTRICT**: `hurst_regime` — 20 trades, WR 25%, net $-3.47, worst -502%. Disable or paper-only until backtest re-validates.
- **SCALE UP**: `macd_cross` — 31 trades, WR 71%, net $32.37. Increase notional_multiplier 1.5x next deploy review.
- **SCALE UP**: `funding_extremes` — 26 trades, WR 54%, net $2.62. Increase notional_multiplier 1.5x next deploy review.
- **SYMBOL BLACKLIST**: `ONDO-USDT` — 23 trades, net $-3.59, avg loss -139%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `ICP-USDT` — 9 trades, net $-18.07, avg loss -197%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `CL-USDT` — 11 trades, net $-2.56, avg loss -104%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `BTC-USDT` — 26 trades, net $-9.52, avg loss -55%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `SOL-USDT` — 15 trades, net $-14.82, avg loss -87%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `TSLA-USDT` — 2 trades, net $-1.35, avg loss -52%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `MU-USDT` — 4 trades, net $-2.09, avg loss -71%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `BCH-USDT` — 38 trades, net $-10.85, avg loss -58%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `NVDA-USDT` — 3 trades, net $-3.04, avg loss -153%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `ZEC-USDT` — 64 trades, net $-3.11, avg loss -106%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `BNB-USDT` — 21 trades, net $-1.27, avg loss -58%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `INTC-USDT` — 3 trades, net $-2.22, avg loss -73%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `AAVE-USDT` — 2 trades, net $-1.52, avg loss -151%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `SUI-USDT` — 6 trades, net $-0.23, avg loss -58%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `TON-USDT` — 3 trades, net $-2.45, avg loss -160%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `YFI-USDT` — 3 trades, net $-0.76, avg loss -89%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `TAO-USDT` — 6 trades, net $-1.68, avg loss -113%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **SYMBOL BLACKLIST**: `ETH-USDT` — 2 trades, net $-0.65, avg loss -125%. Add to LOSING_SYMBOL_BLACKLIST in bot.py.
- **HOUR GATE**: 18:00–21:00 UTC bled $-20.77 across 51 trades. Require ≥2-agent confluence in this window.
- **EDGE: LONGS**: avg long $0.07/trade vs short $-0.22/trade. Loosen long conf floor by 1.
