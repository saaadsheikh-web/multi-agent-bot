# Trade #286 — ZEC-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.9630 (-0.939% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.24 min

> Short stopped out at full risk on ZEC-USDT (stoch_rsi, -0.94%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD72167`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T00:02:49.143979+00:00`
- closed: `2026-06-01T00:05:03.249523+00:00` · hour UTC 00 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [zscore_reversion,stoch_rsi] — best: StochRSI short stoch=0.87 rsi=66

### Parsed signal features
- **rsi**: 66.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 574.2052,
  "atr_tp": 559.9922,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 570.05
- exit_price: 575.4
- tp_price: 559.99
- sl_price: 574.21
- qty: 1.8 · notional: 102.60900000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.7648
- **planned_sl_distance_pct**: 0.7298
- **planned_r_multiple**: 2.418
- **planned_risk_usd**: 7.488
- **planned_reward_usd**: 18.108
- **realized_r_multiple**: -0.129
- **exit_distance_from_tp_pct**: 2.7033
- **exit_distance_from_sl_pct**: -0.2088
- **notional**: 102.60900000000001

### Market excursion (MFE / MAE proxy)
- high_water: 570.05 · low_water: 570.05
- current_stop_at_close: 574.21
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.129
- slippage vs planned TP: 2.7033%
- slippage vs planned SL: -0.2088%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - strong planned R:R=2.418
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `confluence`, `very_short_hold`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617566+00:00Z · journaler v2*
