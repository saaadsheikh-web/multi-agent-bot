# Trade #85 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2460 (+0.404% if pct available) · **Decision grade:** B (85/100) · **Hold:** 4.37 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.40%) during dead-zone hour 09:00 UTC [grade B / 85].

## 1 · Identity
- custom_id: `MABCONZECUSD3581`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-10T08:59:42.994770+00:00`
- closed: `2026-05-10T09:04:04.897627+00:00` · hour UTC 09 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.7, ATR%=0.35, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.7
- **atr_pct**: 0.35
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 599.83545,
  "atr_tp": 621.1494,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 608.97
- exit_price: 611.43
- tp_price: 621.15
- sl_price: 599.84
- qty: 1.0 · notional: 60.897000000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0001
- **planned_sl_distance_pct**: 1.4993
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 9.13
- **planned_reward_usd**: 12.18
- **realized_r_multiple**: 0.027
- **exit_distance_from_tp_pct**: 1.5961
- **exit_distance_from_sl_pct**: 1.9032
- **notional**: 60.897000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 611.34 · low_water: 608.97
- current_stop_at_close: 599.84
- **mfe_pct**: 0.3892
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.0148

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.027
- slippage vs planned TP: 1.5961%
- slippage vs planned SL: 1.9032%

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

## 7 · Tags
`dead_hour`, `very_short_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.561605Z · journaler v2*
