# Trade #333 — MU-USDT short (macd_cross)

**Outcome:** LOSS · **PnL:** -2.1530 (-2.085% if pct available) · **Decision grade:** A (100/100) · **Hold:** 15.11 min

> Short stopped out at full risk on MU-USDT (macd_cross, -2.08%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACMUUSDT7804`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `MU-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T13:43:25.655386+00:00`
- closed: `2026-06-02T13:58:32.390928+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> MACD bear cross hist -0.0424 vol 1.4x

### Parsed signal features
- **atr_val**: 13.033897138160107
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 1052.7708457072401,
  "atr_tp": 994.1183085855197,
  "atr_val": 13.033897138160107,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1032.8
- exit_price: 1054.33
- tp_price: 994.12
- sl_price: 1052.77
- qty: 10.0 · notional: 103.28
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 3.7452
- **planned_sl_distance_pct**: 1.9336
- **planned_r_multiple**: 1.937
- **planned_risk_usd**: 199.7
- **planned_reward_usd**: 386.8
- **realized_r_multiple**: -0.011
- **exit_distance_from_tp_pct**: 5.8298
- **exit_distance_from_sl_pct**: -0.151
- **notional**: 103.28

### Market excursion (MFE / MAE proxy)
- high_water: 1032.8 · low_water: 1032.8
- current_stop_at_close: 1052.77
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.011
- slippage vs planned TP: 5.8298%
- slippage vs planned SL: -0.151%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618562+00:00Z · journaler v2*
