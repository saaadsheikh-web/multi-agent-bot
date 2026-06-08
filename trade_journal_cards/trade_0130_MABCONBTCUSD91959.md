# Trade #130 — BTC-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.2626 (-0.480% if pct available) · **Decision grade:** B (85/100) · **Hold:** 360.05 min

> Short gave back gains on trail on BTC-USDT (connors_rsi2, -0.48%) during dead-zone hour 10:00 UTC trail gave back 0.61% [grade B / 85].

## 1 · Identity
- custom_id: `MABCONBTCUSD91959`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-17T04:26:01.157322+00:00`
- closed: `2026-05-17T10:26:04.026929+00:00` · hour UTC 10 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.1, ATR%=0.07, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.1
- **atr_pct**: 0.07
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 79261.4515,
  "atr_tp": 76528.29800000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 78090.1
- exit_price: 78465.3
- tp_price: 76528.3
- sl_price: 79261.5
- qty: 0.7 · notional: 54.663070000000005
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5001
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 819.98
- **planned_reward_usd**: 1093.26
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.4805
- **exit_distance_from_sl_pct**: 1.0196
- **notional**: 54.663070000000005

### Market excursion (MFE / MAE proxy)
- high_water: 78090.1 · low_water: 77985.6
- current_stop_at_close: 79261.5
- **mfe_pct**: 0.1338
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6143

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.4805%
- slippage vs planned SL: 1.0196%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `trail_too_loose`, `long_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T20:17:10.680119Z · journaler v2*
