# Trade #129 — ZEC-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -1.0270 (-2.010% if pct available) · **Decision grade:** A (100/100) · **Hold:** 61.0 min

> Short stopped out at full risk on ZEC-USDT (connors_rsi2, -2.01%) during good-zone hour 05:00 UTC trail gave back 2.05% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD90864`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-17T04:07:45.885524+00:00`
- closed: `2026-05-17T05:08:45.636365+00:00` · hour UTC 05 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=99.0, ATR%=0.38, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.0
- **atr_pct**: 0.38
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 518.5838,
  "atr_tp": 500.7016,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 510.92
- exit_price: 521.19
- tp_price: 500.7
- sl_price: 518.58
- qty: 1.0 · notional: 51.092000000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0003
- **planned_sl_distance_pct**: 1.4993
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.66
- **planned_reward_usd**: 10.22
- **realized_r_multiple**: -0.134
- **exit_distance_from_tp_pct**: 4.0104
- **exit_distance_from_sl_pct**: -0.5108
- **notional**: 51.092000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 510.92 · low_water: 510.73
- current_stop_at_close: 518.58
- **mfe_pct**: 0.0372
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 2.0473

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.134
- slippage vs planned TP: 4.0104%
- slippage vs planned SL: -0.5108%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `trail_too_loose`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T07:01:23.053442Z · journaler v2*
