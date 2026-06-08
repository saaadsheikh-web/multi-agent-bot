# Trade #78 — ZEC-USDT long (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** C (70/100) · **Hold:** 37.65 min

> Long flat exit (scratch) on ZEC-USDT (hurst_regime, +0.00%) during dead-zone hour 09:00 UTC [killed-agent] trail gave back 0.88% [grade C / 70].

## 1 · Identity
- custom_id: `MABHURZECUSD16156`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-09T08:42:37.403405+00:00`
- closed: `2026-05-09T09:20:16.668768+00:00` · hour UTC 09 (Sat)

## 2 · Hypothesis (why we entered)
> Hurst trend-regime long H=0.959 above EMA21

### Parsed signal features
- **hurst**: 0.9585385339379004
- **atr_val**: 15.003199094250695
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 593.1652013586239,
  "atr_tp": 660.6795972827521,
  "hurst": 0.9585385339379004,
  "atr_val": 15.003199094250695,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 614.99
- exit_price: 614.99
- tp_price: 660.68
- sl_price: 593.17
- qty: 1.0 · notional: 61.499
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 7.4294
- **planned_sl_distance_pct**: 3.548
- **planned_r_multiple**: 2.094
- **planned_risk_usd**: 21.82
- **planned_reward_usd**: 45.69
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 7.4294
- **exit_distance_from_sl_pct**: 3.548
- **notional**: 61.499

### Market excursion (MFE / MAE proxy)
- high_water: 620.38 · low_water: 614.99
- current_stop_at_close: 614.99
- **mfe_pct**: 0.8764
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8764

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 7.4294%
- slippage vs planned SL: 3.548%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - dead-zone-hour
  - agent-on-kill-list
  - strong planned R:R=2.094

## 7 · Tags
`dead_hour`, `killed_agent`, `trail_too_loose`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.560555Z · journaler v2*
