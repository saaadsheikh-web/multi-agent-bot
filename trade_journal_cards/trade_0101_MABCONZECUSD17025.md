# Trade #101 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2730 (+0.488% if pct available) · **Decision grade:** A (100/100) · **Hold:** 254.0 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.49%) trail gave back 0.61% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD17025`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T16:30:27.026745+00:00`
- closed: `2026-05-11T20:44:27.046920+00:00` · hour UTC 20 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.3, ATR%=0.48, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.3
- **atr_pct**: 0.48
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 567.4662,
  "atr_tp": 547.8984,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 559.4
- exit_price: 556.67
- tp_price: 547.9
- sl_price: 567.47
- qty: 1.0 · notional: 55.94
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0558
- **planned_sl_distance_pct**: 1.4426
- **planned_r_multiple**: 1.425
- **planned_risk_usd**: 8.07
- **planned_reward_usd**: 11.5
- **realized_r_multiple**: 0.034
- **exit_distance_from_tp_pct**: 1.5678
- **exit_distance_from_sl_pct**: 1.9306
- **notional**: 55.94

### Market excursion (MFE / MAE proxy)
- high_water: 559.4 · low_water: 553.26
- current_stop_at_close: 556.57956
- **mfe_pct**: 1.0976
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6096

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.034
- slippage vs planned TP: 1.5678%
- slippage vs planned SL: 1.9306%

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
`trail_too_loose`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562242Z · journaler v2*
