# Trade #288 — ZEC-USDT short (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.2736 (+0.261% if pct available) · **Decision grade:** A (100/100) · **Hold:** 11.61 min

> Short trailed into profit on ZEC-USDT (zscore_reversion, +0.26%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCZECUSD82154`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 5
- opened: `2026-06-01T02:49:15.896408+00:00`
- closed: `2026-06-01T03:00:52.688301+00:00` · hour UTC 03 (Mon)

## 2 · Hypothesis (why we entered)
> z-score short z=3.12 mean=539.1692

### Parsed signal features
- **z_score**: 3.12
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 595.2812239543456,
  "atr_tp": 539.1691999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 581.66
- exit_price: 580.14
- tp_price: 539.17
- sl_price: 595.28
- qty: 1.8 · notional: 104.6988
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 7.305
- **planned_sl_distance_pct**: 2.3416
- **planned_r_multiple**: 3.12
- **planned_risk_usd**: 24.516
- **planned_reward_usd**: 76.482
- **realized_r_multiple**: 0.011
- **exit_distance_from_tp_pct**: 7.0436
- **exit_distance_from_sl_pct**: 2.6029
- **notional**: 104.6988

### Market excursion (MFE / MAE proxy)
- high_water: 581.66 · low_water: 577.8
- current_stop_at_close: 580.1111999999999
- **mfe_pct**: 0.6636
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4023

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.011
- slippage vs planned TP: 7.0436%
- slippage vs planned SL: 2.6029%

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
  - strong planned R:R=3.12

## 7 · Tags
`short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617600+00:00Z · journaler v2*
