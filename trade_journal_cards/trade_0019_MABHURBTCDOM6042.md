# Trade #19 — BTCDOM-USDT long (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 271.79 min

> Long flat exit (scratch) on BTCDOM-USDT (hurst_regime, +0.00%) during good-zone hour 19:00 UTC [killed-agent] trail gave back 1.05% [grade A / 95].

## 1 · Identity
- custom_id: `MABHURBTCDOM6042`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T14:47:23.039236+00:00`
- closed: `2026-05-04T19:19:10.446623+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [daily_breakout_4h,hurst_regime] — best: Hurst trend-regime long H=0.892 above EMA21

### Parsed signal features
- **hurst**: 0.8922980054063866
- **atr_val**: 14.187321131291498
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 5486.419018303062,
  "atr_tp": 10960.323,
  "hurst": 0.8922980054063866,
  "atr_val": 14.187321131291498
}
```

## 3 · Plan vs Execution
- entry_price: 5507.6
- exit_price: 5507.6
- tp_price: 10960.323
- sl_price: 5486.419018303062
- qty: 10.0 · notional: 55.07600000000001
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0036
- **planned_sl_distance_pct**: 0.3846
- **planned_r_multiple**: 257.42
- **planned_risk_usd**: 211.8098
- **planned_reward_usd**: 54527.23
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0036
- **exit_distance_from_sl_pct**: 0.3846
- **notional**: 55.07600000000001

### Market excursion (MFE / MAE proxy)
- high_water: 5565.3 · low_water: 5507.6
- current_stop_at_close: 5520.7776
- **mfe_pct**: 1.0476
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0476

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0036%
- slippage vs planned SL: 0.3846%

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
  - strong planned R:R=257.42
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `trail_too_loose`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558598Z · journaler v2*
