# Trade #197 — VVV-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.3857 (+0.763% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.69 min

> Long trailed into profit on VVV-USDT (macd_cross, +0.76%) trail gave back 0.50% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACVVVUSD46672`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `VVV-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-23T14:31:13.549834+00:00`
- closed: `2026-05-23T14:34:54.697765+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> MACD bull cross hist 0.0045 vol 2.1x

### Parsed signal features
- **atr_val**: 0.41103697436675396
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 16.81644453844987,
  "atr_tp": 18.666110923100263,
  "atr_val": 0.41103697436675396,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 17.436
- exit_price: 17.569
- tp_price: 18.666
- sl_price: 16.816
- qty: 29.0 · notional: 50.564400000000006
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 7.0544
- **planned_sl_distance_pct**: 3.5559
- **planned_r_multiple**: 1.984
- **planned_risk_usd**: 17.98
- **planned_reward_usd**: 35.67
- **realized_r_multiple**: 0.021
- **exit_distance_from_tp_pct**: 6.2916
- **exit_distance_from_sl_pct**: 4.3187
- **notional**: 50.564400000000006

### Market excursion (MFE / MAE proxy)
- high_water: 17.657 · low_water: 17.436
- current_stop_at_close: 17.505744
- **mfe_pct**: 1.2675
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5047

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.021
- slippage vs planned TP: 6.2916%
- slippage vs planned SL: 4.3187%

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
`trail_too_loose`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570851Z · journaler v2*
