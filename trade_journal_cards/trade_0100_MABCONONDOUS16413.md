# Trade #100 — ONDO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7456 (-1.490% if pct available) · **Decision grade:** C (70/100) · **Hold:** 42.38 min

> Long stopped out at full risk on ONDO-USDT (connors_rsi2, -1.49%) [flagged-losing-symbol] trail gave back 1.91% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS16413`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T16:20:14.696590+00:00`
- closed: `2026-05-11T17:02:37.320884+00:00` · hour UTC 17 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.7, ATR%=0.75, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.7
- **atr_pct**: 0.75
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.4230575,
  "atr_tp": 0.43809,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4294
- exit_price: 0.423
- tp_price: 0.4381
- sl_price: 0.4231
- qty: 1165.0 · notional: 50.0251
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0261
- **planned_sl_distance_pct**: 1.4672
- **planned_r_multiple**: 1.381
- **planned_risk_usd**: 7.3395
- **planned_reward_usd**: 10.1355
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.5165
- **exit_distance_from_sl_pct**: -0.0233
- **notional**: 50.0251

### Market excursion (MFE / MAE proxy)
- high_water: 0.4312 · low_water: 0.4294
- current_stop_at_close: 0.4231
- **mfe_pct**: 0.4192
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.9096

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.5165%
- slippage vs planned SL: -0.0233%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol
  - high confidence (9) lost

## 7 · Tags
`losing_symbol`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.562152Z · journaler v2*
