# Trade #269 — HYPE-USDT short (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.2912 (+0.275% if pct available) · **Decision grade:** A (100/100) · **Hold:** 25.61 min

> Short trailed into profit on HYPE-USDT (zscore_reversion, +0.28%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCHYPEUS84453`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-29T19:54:15.665006+00:00`
- closed: `2026-05-29T20:19:52.188627+00:00` · hour UTC 20 (Fri)

## 2 · Hypothesis (why we entered)
> z-score short z=2.52 mean=60.7599

### Parsed signal features
- **z_score**: 2.52
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 68.3221098363713,
  "atr_tp": 60.75989,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 66.173
- exit_price: 65.991
- tp_price: 60.76
- sl_price: 68.322
- qty: 16.0 · notional: 105.8768
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 8.1801
- **planned_sl_distance_pct**: 3.2475
- **planned_r_multiple**: 2.519
- **planned_risk_usd**: 34.384
- **planned_reward_usd**: 86.608
- **realized_r_multiple**: 0.008
- **exit_distance_from_tp_pct**: 7.905
- **exit_distance_from_sl_pct**: 3.5226
- **notional**: 105.8768

### Market excursion (MFE / MAE proxy)
- high_water: 66.173 · low_water: 65.697
- current_stop_at_close: 65.959788
- **mfe_pct**: 0.7193
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4443

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.008
- slippage vs planned TP: 7.905%
- slippage vs planned SL: 3.5226%

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
  - strong planned R:R=2.519

## 7 · Tags
`short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617237+00:00Z · journaler v2*
