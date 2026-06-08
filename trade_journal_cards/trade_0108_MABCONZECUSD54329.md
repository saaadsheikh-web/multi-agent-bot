# Trade #108 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1540 (+0.276% if pct available) · **Decision grade:** A (100/100) · **Hold:** 59.28 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.28%) trail gave back 0.60% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD54329`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-12T02:52:11.323380+00:00`
- closed: `2026-05-12T03:51:28.333002+00:00` · hour UTC 03 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.6, ATR%=0.47, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.6
- **atr_pct**: 0.47
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 565.8726499999999,
  "atr_tp": 546.3598,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 557.35
- exit_price: 555.81
- tp_price: 546.36
- sl_price: 565.87
- qty: 1.0 · notional: 55.73500000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9718
- **planned_sl_distance_pct**: 1.5287
- **planned_r_multiple**: 1.29
- **planned_risk_usd**: 8.52
- **planned_reward_usd**: 10.99
- **realized_r_multiple**: 0.018
- **exit_distance_from_tp_pct**: 1.6955
- **exit_distance_from_sl_pct**: 1.805
- **notional**: 55.73500000000001

### Market excursion (MFE / MAE proxy)
- high_water: 557.35 · low_water: 552.46
- current_stop_at_close: 555.77476
- **mfe_pct**: 0.8774
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6011

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.018
- slippage vs planned TP: 1.6955%
- slippage vs planned SL: 1.805%

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
`trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562461Z · journaler v2*
