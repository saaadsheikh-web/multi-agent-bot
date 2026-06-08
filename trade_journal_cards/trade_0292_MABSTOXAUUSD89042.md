# Trade #292 — XAU-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.4453 (-0.428% if pct available) · **Decision grade:** A (95/100) · **Hold:** 240.23 min

> Long gave back gains on trail on XAU-USDT (stoch_rsi, -0.43%) during dead-zone hour 08:00 UTC trail gave back 0.54% [grade A / 95].

## 1 · Identity
- custom_id: `MABSTOXAUUSD89042`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAU-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T04:44:03.567045+00:00`
- closed: `2026-06-01T08:44:17.409425+00:00` · hour UTC 08 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.00 rsi=25

### Parsed signal features
- **rsi**: 25.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4472.8695,
  "atr_tp": 4585.82075,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 4518.52
- exit_price: 4499.16
- tp_price: 4585.82
- sl_price: 4472.87
- qty: 23.0 · notional: 103.92596
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4894
- **planned_sl_distance_pct**: 1.0103
- **planned_r_multiple**: 1.474
- **planned_risk_usd**: 1049.95
- **planned_reward_usd**: 1547.9
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.9179
- **exit_distance_from_sl_pct**: 0.5818
- **notional**: 103.92596

### Market excursion (MFE / MAE proxy)
- high_water: 4523.7 · low_water: 4518.52
- current_stop_at_close: 4472.87
- **mfe_pct**: 0.1146
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5431

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.9179%
- slippage vs planned SL: 0.5818%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - dead-zone-hour
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `confluence`, `trail_too_loose`, `long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617732+00:00Z · journaler v2*
