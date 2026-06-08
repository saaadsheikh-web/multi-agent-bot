# Trade #215 — ONDO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7232 (-1.446% if pct available) · **Decision grade:** C (70/100) · **Hold:** 78.4 min

> Long stopped out at full risk on ONDO-USDT (connors_rsi2, -1.45%) [flagged-losing-symbol] trail gave back 1.67% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS48339`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T18:45:41.152998+00:00`
- closed: `2026-05-24T20:04:05.294118+00:00` · hour UTC 20 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.7, ATR%=0.69, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.7
- **atr_pct**: 0.69
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.4364535,
  "atr_tp": 0.451962,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4425
- exit_price: 0.4361
- tp_price: 0.452
- sl_price: 0.4365
- qty: 1130.0 · notional: 50.0025
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.1469
- **planned_sl_distance_pct**: 1.3559
- **planned_r_multiple**: 1.583
- **planned_risk_usd**: 6.78
- **planned_reward_usd**: 10.735
- **realized_r_multiple**: -0.107
- **exit_distance_from_tp_pct**: 3.5932
- **exit_distance_from_sl_pct**: -0.0904
- **notional**: 50.0025

### Market excursion (MFE / MAE proxy)
- high_water: 0.4435 · low_water: 0.4425
- current_stop_at_close: 0.4365
- **mfe_pct**: 0.226
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.6723

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.107
- slippage vs planned TP: 3.5932%
- slippage vs planned SL: -0.0904%

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
  - high confidence (8) lost

## 7 · Tags
`losing_symbol`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_C`

---
*journaled_at 2026-05-25T23:01:34.905613Z · journaler v2*
