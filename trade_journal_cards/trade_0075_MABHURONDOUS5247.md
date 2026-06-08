# Trade #75 — ONDO-USDT long (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** D (55/100) · **Hold:** 6.01 min

> Long flat exit (scratch) on ONDO-USDT (hurst_regime, +0.00%) during good-zone hour 05:00 UTC [flagged-losing-symbol] [killed-agent] trail gave back 0.84% [grade D / 55].

## 1 · Identity
- custom_id: `MABHURONDOUS5247`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T05:40:48.759179+00:00`
- closed: `2026-05-09T05:46:49.359138+00:00` · hour UTC 05 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Hurst trend-regime long H=0.963 above EMA21

### Parsed signal features
- **hurst**: 0.9629120651015235
- **atr_val**: 0.015560815441304504
- **trend_score**: 3
- **trend_dir**: UP

### Raw meta from agent
```json
{
  "atr_sl": 0.4275587768380433,
  "atr_tp": 0.4975824463239135,
  "hurst": 0.9629120651015235,
  "atr_val": 0.015560815441304504,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4508
- exit_price: 0.4508
- tp_price: 0.4976
- sl_price: 0.4276
- qty: 1110.0 · notional: 50.038799999999995
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 10.3815
- **planned_sl_distance_pct**: 5.1464
- **planned_r_multiple**: 2.017
- **planned_risk_usd**: 25.752
- **planned_reward_usd**: 51.948
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 10.3815
- **exit_distance_from_sl_pct**: 5.1464
- **notional**: 50.038799999999995

### Market excursion (MFE / MAE proxy)
- high_water: 0.4546 · low_water: 0.4508
- current_stop_at_close: 0.4508
- **mfe_pct**: 0.8429
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8429

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 10.3815%
- slippage vs planned SL: 5.1464%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** D (55/100)
- factors:
  - flagged-losing-symbol
  - agent-on-kill-list
  - strong planned R:R=2.017

## 7 · Tags
`good_hour`, `losing_symbol`, `killed_agent`, `trail_too_loose`, `trail_stop`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.560456Z · journaler v2*
