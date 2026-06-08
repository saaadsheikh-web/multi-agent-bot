# Trade #287 — BNB-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0195 (+0.019% if pct available) · **Decision grade:** A (100/100) · **Hold:** 10.3 min

> Long trailed into profit on BNB-USDT (stoch_rsi, +0.02%) during good-zone hour 01:00 UTC trail gave back 0.59% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD78395`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T01:46:36.491117+00:00`
- closed: `2026-06-01T01:56:54.427445+00:00` · hour UTC 01 (Mon)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 688.4558999999999,
  "atr_tp": 705.8411499999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 695.39
- exit_price: 695.52
- tp_price: 705.84
- sl_price: 688.46
- qty: 15.0 · notional: 104.3085
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5028
- **planned_sl_distance_pct**: 0.9966
- **planned_r_multiple**: 1.508
- **planned_risk_usd**: 103.95
- **planned_reward_usd**: 156.75
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4841
- **exit_distance_from_sl_pct**: 1.0153
- **notional**: 104.3085

### Market excursion (MFE / MAE proxy)
- high_water: 699.62 · low_water: 695.39
- current_stop_at_close: 696.1219
- **mfe_pct**: 0.6083
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5896

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4841%
- slippage vs planned SL: 1.0153%

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
`good_hour`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617584+00:00Z · journaler v2*
