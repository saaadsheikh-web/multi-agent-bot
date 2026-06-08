# Trade #180 — ZEC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0216 (+0.043% if pct available) · **Decision grade:** A (100/100) · **Hold:** 56.19 min

> Long trailed into profit on ZEC-USDT (stoch_rsi, +0.04%) trail gave back 0.51% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD61063`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-22T14:44:25.059153+00:00`
- closed: `2026-05-22T15:40:36.268473+00:00` · hour UTC 15 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 625.1949,
  "atr_tp": 640.9826499999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 631.77
- exit_price: 632.04
- tp_price: 640.98
- sl_price: 625.19
- qty: 0.8 · notional: 50.54160000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4578
- **planned_sl_distance_pct**: 1.0415
- **planned_r_multiple**: 1.4
- **planned_risk_usd**: 5.264
- **planned_reward_usd**: 7.368
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.4151
- **exit_distance_from_sl_pct**: 1.0843
- **notional**: 50.54160000000001

### Market excursion (MFE / MAE proxy)
- high_water: 635.26 · low_water: 631.77
- current_stop_at_close: 632.0837
- **mfe_pct**: 0.5524
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5097

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.4151%
- slippage vs planned SL: 1.0843%

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
  - (no notable factors)

## 7 · Tags
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570589Z · journaler v2*
