# Trade #113 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2844 (+0.569% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.04 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.57%) during good-zone hour 19:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD15468`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-12T19:51:09.777859+00:00`
- closed: `2026-05-12T19:56:12.430432+00:00` · hour UTC 19 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.5, ATR%=0.33, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.5
- **atr_pct**: 0.33
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 564.0355,
  "atr_tp": 544.586,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 555.69
- exit_price: 552.53
- tp_price: 544.59
- sl_price: 564.04
- qty: 0.9 · notional: 50.01210000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9975
- **planned_sl_distance_pct**: 1.5026
- **planned_r_multiple**: 1.329
- **planned_risk_usd**: 7.515
- **planned_reward_usd**: 9.99
- **realized_r_multiple**: 0.038
- **exit_distance_from_tp_pct**: 1.4289
- **exit_distance_from_sl_pct**: 2.0713
- **notional**: 50.01210000000001

### Market excursion (MFE / MAE proxy)
- high_water: 555.69 · low_water: 552.56
- current_stop_at_close: 555.69
- **mfe_pct**: 0.5633
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.0054

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.038
- slippage vs planned TP: 1.4289%
- slippage vs planned SL: 2.0713%

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
  - (no notable factors)

## 7 · Tags
`good_hour`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562577Z · journaler v2*
