# Trade #221 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -1.0449 (-1.871% if pct available) · **Decision grade:** A (100/100) · **Hold:** 58.91 min

> Long stopped out at full risk on HYPE-USDT (connors_rsi2, -1.87%) during good-zone hour 01:00 UTC trail gave back 2.12% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS70841`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-25T01:00:43.504855+00:00`
- closed: `2026-05-25T01:59:38.266583+00:00` · hour UTC 01 (Mon)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.2, ATR%=0.43, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.2
- **atr_pct**: 0.43
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 61.00893,
  "atr_tp": 63.17676,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 62.044
- exit_price: 60.883
- tp_price: 63.177
- sl_price: 61.009
- qty: 9.0 · notional: 55.8396
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.8261
- **planned_sl_distance_pct**: 1.6682
- **planned_r_multiple**: 1.095
- **planned_risk_usd**: 9.315
- **planned_reward_usd**: 10.197
- **realized_r_multiple**: -0.112
- **exit_distance_from_tp_pct**: 3.6974
- **exit_distance_from_sl_pct**: -0.2031
- **notional**: 55.8396

### Market excursion (MFE / MAE proxy)
- high_water: 62.198 · low_water: 62.044
- current_stop_at_close: 61.009
- **mfe_pct**: 0.2482
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 2.1195

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.112
- slippage vs planned TP: 3.6974%
- slippage vs planned SL: -0.2031%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905704Z · journaler v2*
