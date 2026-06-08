# Trade #73 — ONDO-USDT long (hurst_regime)

**Outcome:** LOSS · **PnL:** -0.0879 (-0.176% if pct available) · **Decision grade:** D (55/100) · **Hold:** 24.33 min

> Long gave back gains on trail on ONDO-USDT (hurst_regime, -0.18%) [flagged-losing-symbol] [killed-agent] (was up 0.88% before reversing) trail gave back 1.05% [grade D / 55].

## 1 · Identity
- custom_id: `MABHURONDOUS95340`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T02:55:41.411395+00:00`
- closed: `2026-05-09T03:20:01.148643+00:00` · hour UTC 03 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Hurst trend-regime long H=0.971 above EMA21

### Parsed signal features
- **hurst**: 0.9705459748065106
- **atr_val**: 0.01644148994173483
- **trend_score**: 3
- **trend_dir**: UP

### Raw meta from agent
```json
{
  "atr_sl": 0.4308377650873978,
  "atr_tp": 0.5048244698252045,
  "hurst": 0.9705459748065106,
  "atr_val": 0.01644148994173483,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4553
- exit_price: 0.4545
- tp_price: 0.5048
- sl_price: 0.4308
- qty: 1099.0 · notional: 50.03747
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 10.872
- **planned_sl_distance_pct**: 5.3811
- **planned_r_multiple**: 2.02
- **planned_risk_usd**: 26.9255
- **planned_reward_usd**: 54.4005
- **realized_r_multiple**: -0.003
- **exit_distance_from_tp_pct**: 11.0477
- **exit_distance_from_sl_pct**: 5.2054
- **notional**: 50.03747

### Market excursion (MFE / MAE proxy)
- high_water: 0.4593 · low_water: 0.4553
- current_stop_at_close: 0.4553
- **mfe_pct**: 0.8785
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0542

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.003
- slippage vs planned TP: 11.0477%
- slippage vs planned SL: 5.2054%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** D (55/100)
- factors:
  - flagged-losing-symbol
  - agent-on-kill-list
  - strong planned R:R=2.02
  - high confidence (9) lost

## 7 · Tags
`losing_symbol`, `killed_agent`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.560388Z · journaler v2*
