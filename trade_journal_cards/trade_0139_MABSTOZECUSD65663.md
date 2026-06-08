# Trade #139 — ZEC-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.2349 (+0.458% if pct available) · **Decision grade:** A (100/100) · **Hold:** 47.04 min

> Short trailed into profit on ZEC-USDT (stoch_rsi, +0.46%) during good-zone hour 05:00 UTC trail gave back 0.51% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD65663`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-19T04:41:05.115156+00:00`
- closed: `2026-05-19T05:28:07.226945+00:00` · hour UTC 05 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=0.92 rsi=70

### Parsed signal features
- **rsi**: 70.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 576.1545000000001,
  "atr_tp": 561.8932500000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 570.45
- exit_price: 567.84
- tp_price: 561.89
- sl_price: 576.15
- qty: 0.9 · notional: 51.34050000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5006
- **planned_sl_distance_pct**: 0.9992
- **planned_r_multiple**: 1.502
- **planned_risk_usd**: 5.13
- **planned_reward_usd**: 7.704
- **realized_r_multiple**: 0.046
- **exit_distance_from_tp_pct**: 1.043
- **exit_distance_from_sl_pct**: 1.4567
- **notional**: 51.34050000000001

### Market excursion (MFE / MAE proxy)
- high_water: 570.45 · low_water: 564.95
- current_stop_at_close: 567.77475
- **mfe_pct**: 0.9642
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5066

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.046
- slippage vs planned TP: 1.043%
- slippage vs planned SL: 1.4567%

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
  - (no notable factors)

## 7 · Tags
`good_hour`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T07:00:59.092686Z · journaler v2*
