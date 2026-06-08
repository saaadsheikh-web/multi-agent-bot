# Trade #290 — XAU-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0375 (+0.036% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.78 min

> Long timed out in profit on XAU-USDT (stoch_rsi, +0.04%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAUUSD88627`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAU-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T04:37:08.783893+00:00`
- closed: `2026-06-01T04:42:55.517097+00:00` · hour UTC 04 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.00 rsi=24

### Parsed signal features
- **rsi**: 24.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4471.5626999999995,
  "atr_tp": 4584.480949999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 4516.73
- exit_price: 4518.36
- tp_price: 4584.48
- sl_price: 4471.56
- qty: 23.0 · notional: 103.88479
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5
- **planned_sl_distance_pct**: 1.0001
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1038.91
- **planned_reward_usd**: 1558.25
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4639
- **exit_distance_from_sl_pct**: 1.0361
- **notional**: 103.88479

### Market excursion (MFE / MAE proxy)
- high_water: 4519.1 · low_water: 4516.73
- current_stop_at_close: 4471.56
- **mfe_pct**: 0.0525
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0164

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4639%
- slippage vs planned SL: 1.0361%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617622+00:00Z · journaler v2*
