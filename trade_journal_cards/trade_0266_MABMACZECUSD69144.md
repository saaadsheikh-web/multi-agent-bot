# Trade #266 — ZEC-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +1.3946 (+1.346% if pct available) · **Decision grade:** A (100/100) · **Hold:** 97.09 min

> Long trailed into profit on ZEC-USDT (macd_cross, +1.35%) trail gave back 1.04% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACZECUSD69144`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-29T15:39:05.689785+00:00`
- closed: `2026-05-29T17:16:10.859156+00:00` · hour UTC 17 (Fri)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [daily_breakout_4h,daily_breakout_2h,macd_cross,hurst_regime] — best: MACD bull cross hist 0.1120 vol 1.3x

### Parsed signal features
- **atr_val**: 11.623296764327494
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 529.1450548535088,
  "atr_tp": 581.4498902929826,
  "atr_val": 11.623296764327494,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 545.36
- exit_price: 552.7
- tp_price: 581.45
- sl_price: 529.15
- qty: 1.9 · notional: 103.61840000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 6.6176
- **planned_sl_distance_pct**: 2.9723
- **planned_r_multiple**: 2.226
- **planned_risk_usd**: 30.799
- **planned_reward_usd**: 68.571
- **realized_r_multiple**: 0.045
- **exit_distance_from_tp_pct**: 5.2717
- **exit_distance_from_sl_pct**: 4.3182
- **notional**: 103.61840000000001

### Market excursion (MFE / MAE proxy)
- high_water: 558.38 · low_water: 545.36
- current_stop_at_close: 552.7962
- **mfe_pct**: 2.3874
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0415

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.045
- slippage vs planned TP: 5.2717%
- slippage vs planned SL: 4.3182%

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
  - strong planned R:R=2.226
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617172+00:00Z · journaler v2*
