# Trade #74 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1800 (+0.294% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.63 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.29%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD97852`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T03:37:34.220548+00:00`
- closed: `2026-05-09T03:41:11.835264+00:00` · hour UTC 03 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=4.9, in uptrend

### Parsed signal features
- **rsi2**: 4.9
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 603.91335,
  "atr_tp": 625.3722,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 612.72
- exit_price: 614.52
- tp_price: 625.37
- sl_price: 603.91
- qty: 1.0 · notional: 61.272000000000006
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 2.0646
- **planned_sl_distance_pct**: 1.4379
- **planned_r_multiple**: 1.436
- **planned_risk_usd**: 8.81
- **planned_reward_usd**: 12.65
- **realized_r_multiple**: 0.02
- **exit_distance_from_tp_pct**: 1.7708
- **exit_distance_from_sl_pct**: 1.7316
- **notional**: 61.272000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 614.52 · low_water: 612.72
- current_stop_at_close: 603.91
- **mfe_pct**: 0.2938
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.02
- slippage vs planned TP: 1.7708%
- slippage vs planned SL: 1.7316%

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
  - multi-agent confluence

## 7 · Tags
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560423Z · journaler v2*
