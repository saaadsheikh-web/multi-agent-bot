# Trade #138 — ZEC-USDT short (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.2565 (+0.497% if pct available) · **Decision grade:** A (100/100) · **Hold:** 27.82 min

> Short trailed into profit on ZEC-USDT (zscore_reversion, +0.50%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCZECUSD63452`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-19T04:04:13.420204+00:00`
- closed: `2026-05-19T04:32:02.635928+00:00` · hour UTC 04 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [zscore_reversion,stoch_rsi] — best: z-score short z=2.59 mean=524.4656

### Parsed signal features
- **z_score**: 2.59
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 592.82715389116,
  "atr_tp": 524.4656,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 573.93
- exit_price: 571.08
- tp_price: 524.47
- sl_price: 592.83
- qty: 0.9 · notional: 51.6537
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 8.6178
- **planned_sl_distance_pct**: 3.2931
- **planned_r_multiple**: 2.617
- **planned_risk_usd**: 17.01
- **planned_reward_usd**: 44.514
- **realized_r_multiple**: 0.015
- **exit_distance_from_tp_pct**: 8.1212
- **exit_distance_from_sl_pct**: 3.7897
- **notional**: 51.6537

### Market excursion (MFE / MAE proxy)
- high_water: 573.93 · low_water: 568.79
- current_stop_at_close: 571.06516
- **mfe_pct**: 0.8956
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.399

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.015
- slippage vs planned TP: 8.1212%
- slippage vs planned SL: 3.7897%

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
  - strong planned R:R=2.617
  - multi-agent confluence

## 7 · Tags
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T07:00:59.092585Z · journaler v2*
