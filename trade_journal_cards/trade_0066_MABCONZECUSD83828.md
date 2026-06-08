# Trade #66 — ZEC-USDT long (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 20.85 min

> Long flat exit (scratch) on ZEC-USDT (connors_rsi2, +0.00%) trail gave back 0.53% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD83828`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-07T19:57:10.118396+00:00`
- closed: `2026-05-07T20:18:01.015672+00:00` · hour UTC 20 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.1, in uptrend

### Parsed signal features
- **rsi2**: 4.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 551.3242,
  "atr_tp": 570.9144,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 559.8
- exit_price: 559.8
- tp_price: 570.91
- sl_price: 551.32
- qty: 1.0 · notional: 55.98
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9846
- **planned_sl_distance_pct**: 1.5148
- **planned_r_multiple**: 1.31
- **planned_risk_usd**: 8.48
- **planned_reward_usd**: 11.11
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9846
- **exit_distance_from_sl_pct**: 1.5148
- **notional**: 55.98

### Market excursion (MFE / MAE proxy)
- high_water: 562.77 · low_water: 559.8
- current_stop_at_close: 551.32
- **mfe_pct**: 0.5305
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5305

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9846%
- slippage vs planned SL: 1.5148%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560110Z · journaler v2*
