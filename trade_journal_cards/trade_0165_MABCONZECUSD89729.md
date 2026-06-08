# Trade #165 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0016 (-0.003% if pct available) · **Decision grade:** A (100/100) · **Hold:** 27.11 min

> Long gave back gains on trail on ZEC-USDT (connors_rsi2, -0.00%) during good-zone hour 19:00 UTC (was up 0.73% before reversing) trail gave back 0.74% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD89729`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T18:55:32.664680+00:00`
- closed: `2026-05-21T19:22:39.408541+00:00` · hour UTC 19 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.4, ATR%=0.64, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.4
- **atr_pct**: 0.64
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 657.4875,
  "atr_tp": 680.85,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 667.51
- exit_price: 667.49
- tp_price: 680.85
- sl_price: 657.49
- qty: 0.8 · notional: 53.40080000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9985
- **planned_sl_distance_pct**: 1.5011
- **planned_r_multiple**: 1.331
- **planned_risk_usd**: 8.016
- **planned_reward_usd**: 10.672
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0015
- **exit_distance_from_sl_pct**: 1.4981
- **notional**: 53.40080000000001

### Market excursion (MFE / MAE proxy)
- high_water: 672.4 · low_water: 667.51
- current_stop_at_close: 667.51
- **mfe_pct**: 0.7326
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7356

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0015%
- slippage vs planned SL: 1.4981%

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
`good_hour`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570312Z · journaler v2*
