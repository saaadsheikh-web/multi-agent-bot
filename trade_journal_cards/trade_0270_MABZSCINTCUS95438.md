# Trade #270 — INTC-USDT long (zscore_reversion)

**Outcome:** LOSS · **PnL:** -0.2697 (-0.268% if pct available) · **Decision grade:** A (100/100) · **Hold:** 180.05 min

> Long gave back gains on trail on INTC-USDT (zscore_reversion, -0.27%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCINTCUS95438`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `INTC-USDT` · side: `long`
- confidence: 5
- opened: `2026-05-29T22:57:19.578549+00:00`
- closed: `2026-05-30T01:57:22.527788+00:00` · hour UTC 01 (Sat)

## 2 · Hypothesis (why we entered)
> z-score long z=-2.51 mean=120.9477

### Parsed signal features
- **z_score**: -2.51
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 113.5701761233067,
  "atr_tp": 120.9477,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 115.69
- exit_price: 115.38
- tp_price: 120.95
- sl_price: 113.57
- qty: 87.0 · notional: 100.6503
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 4.5466
- **planned_sl_distance_pct**: 1.8325
- **planned_r_multiple**: 2.481
- **planned_risk_usd**: 184.44
- **planned_reward_usd**: 457.62
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 4.8146
- **exit_distance_from_sl_pct**: 1.5645
- **notional**: 100.6503

### Market excursion (MFE / MAE proxy)
- high_water: 115.91 · low_water: 115.69
- current_stop_at_close: 113.57
- **mfe_pct**: 0.1902
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4581

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 4.8146%
- slippage vs planned SL: 1.5645%

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
  - strong planned R:R=2.481

## 7 · Tags
`good_hour`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617278+00:00Z · journaler v2*
