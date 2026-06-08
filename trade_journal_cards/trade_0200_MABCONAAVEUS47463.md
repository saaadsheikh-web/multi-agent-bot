# Trade #200 — AAVE-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7740 (-1.526% if pct available) · **Decision grade:** A (100/100) · **Hold:** 205.46 min

> Short stopped out at full risk on AAVE-USDT (connors_rsi2, -1.53%) during good-zone hour 18:00 UTC trail gave back 1.56% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONAAVEUS47463`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `AAVE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T14:44:25.096402+00:00`
- closed: `2026-05-23T18:09:52.639595+00:00` · hour UTC 18 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.9, ATR%=0.18, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.9
- **atr_pct**: 0.18
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 85.82839999999999,
  "atr_tp": 82.86880000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 84.56
- exit_price: 85.85
- tp_price: 82.87
- sl_price: 85.83
- qty: 6.0 · notional: 50.73600000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9986
- **planned_sl_distance_pct**: 1.5019
- **planned_r_multiple**: 1.331
- **planned_risk_usd**: 7.62
- **planned_reward_usd**: 10.14
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.5241
- **exit_distance_from_sl_pct**: -0.0237
- **notional**: 50.73600000000001

### Market excursion (MFE / MAE proxy)
- high_water: 84.56 · low_water: 84.53
- current_stop_at_close: 85.83
- **mfe_pct**: 0.0355
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.561

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.5241%
- slippage vs planned SL: -0.0237%

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
`good_hour`, `trail_too_loose`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905366Z · journaler v2*
