# Trade #220 — BCH-USDT short (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 179.94 min

> Short flat exit (scratch) on BCH-USDT (connors_rsi2, +0.00%) trail gave back 0.75% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD64502`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-24T23:15:03.679611+00:00`
- closed: `2026-05-25T02:15:00.188300+00:00` · hour UTC 02 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=99.8, ATR%=0.29, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.8
- **atr_pct**: 0.29
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 351.59599999999995,
  "atr_tp": 339.472,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 346.4
- exit_price: 346.4
- tp_price: 339.47
- sl_price: 351.6
- qty: 1.5 · notional: 51.96
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0006
- **planned_sl_distance_pct**: 1.5012
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.8
- **planned_reward_usd**: 10.395
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.0006
- **exit_distance_from_sl_pct**: 1.5012
- **notional**: 51.96

### Market excursion (MFE / MAE proxy)
- high_water: 346.4 · low_water: 343.8
- current_stop_at_close: 346.4
- **mfe_pct**: 0.7506
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7506

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.0006%
- slippage vs planned SL: 1.5012%

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
*journaled_at 2026-05-25T23:01:34.905734Z · journaler v2*
