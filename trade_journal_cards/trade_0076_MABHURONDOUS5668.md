# Trade #76 — ONDO-USDT long (hurst_regime)

**Outcome:** LOSS · **PnL:** -2.5109 (-5.019% if pct available) · **Decision grade:** F (30/100) · **Hold:** 176.43 min

> Long gave back gains on trail on ONDO-USDT (hurst_regime, -5.02%) during dead-zone hour 08:00 UTC [flagged-losing-symbol] [killed-agent] trail gave back 5.22% [grade F / 30].

## 1 · Identity
- custom_id: `MABHURONDOUS5668`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T05:47:49.835687+00:00`
- closed: `2026-05-09T08:44:15.713434+00:00` · hour UTC 08 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Hurst trend-regime long H=0.963 above EMA21

### Parsed signal features
- **hurst**: 0.9629914770398992
- **atr_val**: 0.015753672584161646
- **trend_score**: 3
- **trend_dir**: UP

### Raw meta from agent
```json
{
  "atr_sl": 0.42646949112375754,
  "atr_tp": 0.4973610177524849,
  "hurst": 0.9629914770398992,
  "atr_val": 0.015753672584161646,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4503
- exit_price: 0.4277
- tp_price: 0.4974
- sl_price: 0.4265
- qty: 1111.0 · notional: 50.028330000000004
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 10.4597
- **planned_sl_distance_pct**: 5.2854
- **planned_r_multiple**: 1.979
- **planned_risk_usd**: 26.4418
- **planned_reward_usd**: 52.3281
- **realized_r_multiple**: -0.095
- **exit_distance_from_tp_pct**: 15.4786
- **exit_distance_from_sl_pct**: 0.2665
- **notional**: 50.028330000000004

### Market excursion (MFE / MAE proxy)
- high_water: 0.4512 · low_water: 0.4503
- current_stop_at_close: 0.4265
- **mfe_pct**: 0.1999
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 5.2187

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.095
- slippage vs planned TP: 15.4786%
- slippage vs planned SL: 0.2665%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** F (30/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour
  - agent-on-kill-list
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `losing_symbol`, `killed_agent`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_F`

---
*journaled_at 2026-05-17T03:54:39.560523Z · journaler v2*
