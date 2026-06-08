# Trade #25 — GIGGLE-USDT long (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 28.19 min

> Long flat exit (scratch) on GIGGLE-USDT (hurst_regime, +0.00%) during good-zone hour 01:00 UTC [killed-agent] trail gave back 0.72% [grade A / 95].

## 1 · Identity
- custom_id: `MABHURGIGGLE42167`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `GIGGLE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-05T00:49:28.802130+00:00`
- closed: `2026-05-05T01:17:40.236537+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime long H=0.938 above EMA21

### Parsed signal features
- **hurst**: 0.9379577149027346
- **atr_val**: 1.6263971004368154
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 34.99040434934478,
  "atr_tp": 74.4857,
  "hurst": 0.9379577149027346,
  "atr_val": 1.6263971004368154
}
```

## 3 · Plan vs Execution
- entry_price: 37.43
- exit_price: 37.43
- tp_price: 74.49
- sl_price: 34.99
- qty: 134.0 · notional: 50.156200000000005
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0115
- **planned_sl_distance_pct**: 6.5188
- **planned_r_multiple**: 15.189
- **planned_risk_usd**: 326.96
- **planned_reward_usd**: 4966.04
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0115
- **exit_distance_from_sl_pct**: 6.5188
- **notional**: 50.156200000000005

### Market excursion (MFE / MAE proxy)
- high_water: 37.7 · low_water: 37.43
- current_stop_at_close: 34.99
- **mfe_pct**: 0.7213
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7213

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0115%
- slippage vs planned SL: 6.5188%

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
  - strong planned R:R=15.189
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558705Z · journaler v2*
