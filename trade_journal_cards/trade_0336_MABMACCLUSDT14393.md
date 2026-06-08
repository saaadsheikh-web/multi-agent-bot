# Trade #336 — CL-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.3161 (+0.315% if pct available) · **Decision grade:** A (100/100) · **Hold:** 7.53 min

> Long trailed into profit on CL-USDT (macd_cross, +0.31%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACCLUSDT14393`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `CL-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T15:33:14.190717+00:00`
- closed: `2026-06-02T15:40:46.023844+00:00` · hour UTC 15 (Tue)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [macd_cross,hurst_regime,us_open] — best: MACD bull cross hist 0.0022 vol 2.5x

### Parsed signal features
- **atr_val**: 0.8133646850690687
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 90.8499529723964,
  "atr_tp": 94.5100940552072,
  "atr_val": 0.8133646850690687,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 92.07
- exit_price: 92.36
- tp_price: 94.51
- sl_price: 90.85
- qty: 109.0 · notional: 100.3563
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.6502
- **planned_sl_distance_pct**: 1.3251
- **planned_r_multiple**: 2.0
- **planned_risk_usd**: 132.98
- **planned_reward_usd**: 265.96
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: 2.3352
- **exit_distance_from_sl_pct**: 1.6401
- **notional**: 100.3563

### Market excursion (MFE / MAE proxy)
- high_water: 92.34 · low_water: 92.07
- current_stop_at_close: 90.85
- **mfe_pct**: 0.2933
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.0217

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.002
- slippage vs planned TP: 2.3352%
- slippage vs planned SL: 1.6401%

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
  - strong planned R:R=2.0
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618652+00:00Z · journaler v2*
