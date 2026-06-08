# Trade #151 — XMR-USDT short (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.4160 (+0.784% if pct available) · **Decision grade:** A (100/100) · **Hold:** 51.46 min

> Short trailed into profit on XMR-USDT (zscore_reversion, +0.78%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCXMRUSD35477`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-21T03:51:20.145260+00:00`
- closed: `2026-05-21T04:42:47.682052+00:00` · hour UTC 04 (Thu)

## 2 · Hypothesis (why we entered)
> z-score short z=2.65 mean=391.7114

### Parsed signal features
- **z_score**: 2.65
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 414.4817043159442,
  "atr_tp": 391.71139999999986,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 408.35
- exit_price: 405.15
- tp_price: 391.71
- sl_price: 414.48
- qty: 1.3 · notional: 53.0855
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 4.0749
- **planned_sl_distance_pct**: 1.5012
- **planned_r_multiple**: 2.714
- **planned_risk_usd**: 7.969
- **planned_reward_usd**: 21.632
- **realized_r_multiple**: 0.052
- **exit_distance_from_tp_pct**: 3.2913
- **exit_distance_from_sl_pct**: 2.2848
- **notional**: 53.0855

### Market excursion (MFE / MAE proxy)
- high_water: 408.35 · low_water: 403.53
- current_stop_at_close: 405.14412
- **mfe_pct**: 1.1804
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3967

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.052
- slippage vs planned TP: 3.2913%
- slippage vs planned SL: 2.2848%

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
  - strong planned R:R=2.714

## 7 · Tags
`short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-21T07:01:00.212462Z · journaler v2*
