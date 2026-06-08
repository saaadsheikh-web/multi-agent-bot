# Trade #23 — TAO-USDT short (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** C (65/100) · **Hold:** 181.42 min

> Short flat exit (scratch) on TAO-USDT (hurst_regime, +0.00%) during good-zone hour 19:00 UTC [flagged-losing-symbol] [killed-agent] [grade C / 65].

## 1 · Identity
- custom_id: `MABHURTAOUSD11464`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `TAO-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-04T16:17:45.418487+00:00`
- closed: `2026-05-04T19:19:10.458516+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [momentum,hurst_regime] — best: Hurst trend-regime short H=0.893 below EMA21

### Parsed signal features
- **hurst**: 0.8925096179887103
- **atr_val**: 4.19859376871583
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 284.50789065307373,
  "atr_tp": 2.7821,
  "hurst": 0.8925096179887103,
  "atr_val": 4.19859376871583
}
```

## 3 · Plan vs Execution
- entry_price: 278.21
- exit_price: 278.21
- tp_price: 2.7821
- sl_price: 284.50789065307373
- qty: 18.0 · notional: 50.077799999999996
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0
- **planned_sl_distance_pct**: 2.2637
- **planned_r_multiple**: 43.734
- **planned_risk_usd**: 113.362
- **planned_reward_usd**: 4957.7022
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0
- **exit_distance_from_sl_pct**: 2.2637
- **notional**: 50.077799999999996

### Market excursion (MFE / MAE proxy)
- high_water: 278.21 · low_water: 277.83
- current_stop_at_close: 284.50789065307373
- **mfe_pct**: 0.1366
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1366

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0%
- slippage vs planned SL: 2.2637%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** C (65/100)
- factors:
  - flagged-losing-symbol
  - agent-on-kill-list
  - strong planned R:R=43.734
  - multi-agent confluence

## 7 · Tags
`good_hour`, `losing_symbol`, `killed_agent`, `confluence`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.558634Z · journaler v2*
