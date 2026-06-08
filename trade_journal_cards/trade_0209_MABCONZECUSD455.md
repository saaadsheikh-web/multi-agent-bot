# Trade #209 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1816 (+0.360% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.49 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.36%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD455`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T05:27:37.220474+00:00`
- closed: `2026-05-24T05:32:06.724795+00:00` · hour UTC 05 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.1, ATR%=0.38, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.1
- **atr_pct**: 0.38
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 621.52515,
  "atr_tp": 643.6098000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 630.86
- exit_price: 633.13
- tp_price: 643.61
- sl_price: 621.53
- qty: 0.8 · notional: 50.46880000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0211
- **planned_sl_distance_pct**: 1.4789
- **planned_r_multiple**: 1.367
- **planned_risk_usd**: 7.464
- **planned_reward_usd**: 10.2
- **realized_r_multiple**: 0.024
- **exit_distance_from_tp_pct**: 1.6612
- **exit_distance_from_sl_pct**: 1.8388
- **notional**: 50.46880000000001

### Market excursion (MFE / MAE proxy)
- high_water: 633.69 · low_water: 630.86
- current_stop_at_close: 621.53
- **mfe_pct**: 0.4486
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0888

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.024
- slippage vs planned TP: 1.6612%
- slippage vs planned SL: 1.8388%

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
`good_hour`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905485Z · journaler v2*
