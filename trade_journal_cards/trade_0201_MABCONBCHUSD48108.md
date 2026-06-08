# Trade #201 — BCH-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7950 (-1.523% if pct available) · **Decision grade:** A (100/100) · **Hold:** 206.32 min

> Short stopped out at full risk on BCH-USDT (connors_rsi2, -1.52%) during good-zone hour 18:00 UTC trail gave back 1.58% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD48108`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T14:55:10.274596+00:00`
- closed: `2026-05-23T18:21:29.569878+00:00` · hour UTC 18 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.6, ATR%=0.19, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.6
- **atr_pct**: 0.19
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 353.1184999999999,
  "atr_tp": 340.94199999999995,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 347.9
- exit_price: 353.2
- tp_price: 340.94
- sl_price: 353.12
- qty: 1.5 · notional: 52.185
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0006
- **planned_sl_distance_pct**: 1.5004
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.83
- **planned_reward_usd**: 10.44
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.524
- **exit_distance_from_sl_pct**: -0.023
- **notional**: 52.185

### Market excursion (MFE / MAE proxy)
- high_water: 347.9 · low_water: 347.7
- current_stop_at_close: 353.12
- **mfe_pct**: 0.0575
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.5809

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.524%
- slippage vs planned SL: -0.023%

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
*journaled_at 2026-05-25T23:01:34.905384Z · journaler v2*
