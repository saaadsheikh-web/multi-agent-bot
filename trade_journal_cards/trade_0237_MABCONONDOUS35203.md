# Trade #237 — ONDO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0689 (-0.138% if pct available) · **Decision grade:** C (60/100) · **Hold:** 6.83 min

> Long closed in the red without clean exit on ONDO-USDT (connors_rsi2, -0.14%) during good-zone hour 19:00 UTC [flagged-losing-symbol] [grade C / 60].

## 1 · Identity
- custom_id: `MABCONONDOUS35203`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T18:53:25.036179+00:00`
- closed: `2026-05-25T19:00:14.884092+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.7, ATR%=0.45, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.7
- **atr_pct**: 0.45
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.4287705,
  "atr_tp": 0.444006,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4354
- exit_price: 0.4348
- tp_price: 0.444
- sl_price: 0.4288
- qty: 1149.0 · notional: 50.027460000000005
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9752
- **planned_sl_distance_pct**: 1.5158
- **planned_r_multiple**: 1.303
- **planned_risk_usd**: 7.5834
- **planned_reward_usd**: 9.8814
- **realized_r_multiple**: -0.009
- **exit_distance_from_tp_pct**: 2.113
- **exit_distance_from_sl_pct**: 1.378
- **notional**: 50.027460000000005

### Market excursion (MFE / MAE proxy)
- high_water: 0.4354 · low_water: 0.4354
- current_stop_at_close: 0.4288
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.009
- slippage vs planned TP: 2.113%
- slippage vs planned SL: 1.378%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (60/100)
- factors:
  - flagged-losing-symbol
  - timed-out loser (no clean exit signal)
  - high confidence (8) lost

## 7 · Tags
`good_hour`, `losing_symbol`, `long_loss`, `time_or_manual`, `grade_C`

---
*journaled_at 2026-05-25T23:01:34.905936Z · journaler v2*
