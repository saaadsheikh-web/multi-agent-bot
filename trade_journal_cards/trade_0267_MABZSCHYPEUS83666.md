# Trade #267 — HYPE-USDT short (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.1296 (+0.122% if pct available) · **Decision grade:** A (100/100) · **Hold:** 11.89 min

> Short trailed into profit on HYPE-USDT (zscore_reversion, +0.12%) during good-zone hour 19:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCHYPEUS83666`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-29T19:41:07.897395+00:00`
- closed: `2026-05-29T19:53:01.516786+00:00` · hour UTC 19 (Fri)

## 2 · Hypothesis (why we entered)
> z-score short z=2.52 mean=60.7600

### Parsed signal features
- **z_score**: 2.52
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 68.32928803772108,
  "atr_tp": 60.75996,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 66.18
- exit_price: 66.099
- tp_price: 60.76
- sl_price: 68.329
- qty: 16.0 · notional: 105.88800000000002
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 8.1898
- **planned_sl_distance_pct**: 3.2472
- **planned_r_multiple**: 2.522
- **planned_risk_usd**: 34.384
- **planned_reward_usd**: 86.72
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 8.0674
- **exit_distance_from_sl_pct**: 3.3696
- **notional**: 105.88800000000002

### Market excursion (MFE / MAE proxy)
- high_water: 66.18 · low_water: 65.827
- current_stop_at_close: 66.090308
- **mfe_pct**: 0.5334
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.411

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 8.0674%
- slippage vs planned SL: 3.3696%

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
  - strong planned R:R=2.522

## 7 · Tags
`good_hour`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617194+00:00Z · journaler v2*
