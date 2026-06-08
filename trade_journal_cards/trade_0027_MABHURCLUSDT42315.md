# Trade #27 — CL-USDT long (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 25.73 min

> Long flat exit (scratch) on CL-USDT (hurst_regime, +0.00%) during good-zone hour 01:00 UTC [killed-agent] [grade A / 95].

## 1 · Identity
- custom_id: `MABHURCLUSDT42315`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `CL-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-05T00:51:56.441234+00:00`
- closed: `2026-05-05T01:17:40.273628+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime long H=0.911 above EMA21

### Parsed signal features
- **hurst**: 0.9108850036946629
- **atr_val**: 1.206515838120173
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 102.90022624281974,
  "atr_tp": 208.3729,
  "hurst": 0.9108850036946629,
  "atr_val": 1.206515838120173
}
```

## 3 · Plan vs Execution
- entry_price: 104.71
- exit_price: 104.71
- tp_price: 208.37
- sl_price: 102.9
- qty: 48.0 · notional: 50.260799999999996
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 98.9972
- **planned_sl_distance_pct**: 1.7286
- **planned_r_multiple**: 57.27
- **planned_risk_usd**: 86.88
- **planned_reward_usd**: 4975.68
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 98.9972
- **exit_distance_from_sl_pct**: 1.7286
- **notional**: 50.260799999999996

### Market excursion (MFE / MAE proxy)
- high_water: 104.95 · low_water: 104.71
- current_stop_at_close: 102.9
- **mfe_pct**: 0.2292
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2292

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 98.9972%
- slippage vs planned SL: 1.7286%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=57.27
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558777Z · journaler v2*
