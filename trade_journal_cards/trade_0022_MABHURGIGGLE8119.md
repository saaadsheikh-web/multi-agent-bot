# Trade #22 — GIGGLE-USDT long (hurst_regime)

**Outcome:** WIN · **PnL:** +0.1350 (+0.269% if pct available) · **Decision grade:** A (95/100) · **Hold:** 46.18 min

> Long trailed into profit on GIGGLE-USDT (hurst_regime, +0.27%) [killed-agent] trail gave back 1.02% [grade A / 95].

## 1 · Identity
- custom_id: `MABHURGIGGLE8119`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `GIGGLE-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T15:22:00.148242+00:00`
- closed: `2026-05-04T16:08:10.992797+00:00` · hour UTC 16 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime long H=0.982 above EMA21

### Parsed signal features
- **hurst**: 0.9818771899966288
- **atr_val**: 1.4783329594522507
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 35.01250056082162,
  "atr_tp": 74.0877,
  "hurst": 0.9818771899966288,
  "atr_val": 1.4783329594522507
}
```

## 3 · Plan vs Execution
- entry_price: 37.2
- exit_price: 37.3
- tp_price: 74.0877
- sl_price: 35.01250056082162
- qty: 135.0 · notional: 50.220000000000006
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.1605
- **planned_sl_distance_pct**: 5.8804
- **planned_r_multiple**: 16.863
- **planned_risk_usd**: 295.3124
- **planned_reward_usd**: 4979.8395
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 98.8917
- **exit_distance_from_sl_pct**: 6.1492
- **notional**: 50.220000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 37.68 · low_water: 37.2
- current_stop_at_close: 37.37856
- **mfe_pct**: 1.2903
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0215

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 98.8917%
- slippage vs planned SL: 6.1492%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=16.863
  - multi-agent confluence

## 7 · Tags
`killed_agent`, `confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558426Z · journaler v2*
