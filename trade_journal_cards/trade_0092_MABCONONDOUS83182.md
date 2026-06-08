# Trade #92 — ONDO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7514 (-1.503% if pct available) · **Decision grade:** D (55/100) · **Hold:** 62.15 min

> Long stopped out at full risk on ONDO-USDT (connors_rsi2, -1.50%) during dead-zone hour 08:00 UTC [flagged-losing-symbol] trail gave back 1.85% [grade D / 55].

## 1 · Identity
- custom_id: `MABCONONDOUS83182`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T07:06:24.448231+00:00`
- closed: `2026-05-11T08:08:33.669758+00:00` · hour UTC 08 (Mon)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.5, ATR%=0.77, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.5
- **atr_pct**: 0.77
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.42620949999999996,
  "atr_tp": 0.44135399999999997,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4326
- exit_price: 0.4261
- tp_price: 0.4414
- sl_price: 0.4262
- qty: 1156.0 · notional: 50.00856
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0342
- **planned_sl_distance_pct**: 1.4794
- **planned_r_multiple**: 1.375
- **planned_risk_usd**: 7.3984
- **planned_reward_usd**: 10.1728
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.5368
- **exit_distance_from_sl_pct**: -0.0231
- **notional**: 50.00856

### Market excursion (MFE / MAE proxy)
- high_water: 0.4341 · low_water: 0.4326
- current_stop_at_close: 0.4262
- **mfe_pct**: 0.3467
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.8493

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.5368%
- slippage vs planned SL: -0.0231%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** D (55/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `losing_symbol`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.561920Z · journaler v2*
