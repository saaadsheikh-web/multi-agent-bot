# Trade #156 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0032 (-0.006% if pct available) · **Decision grade:** A (100/100) · **Hold:** 32.25 min

> Long gave back gains on trail on ZEC-USDT (connors_rsi2, -0.01%) during good-zone hour 05:00 UTC (was up 0.59% before reversing) trail gave back 0.59% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD39837`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T05:03:59.079080+00:00`
- closed: `2026-05-21T05:36:13.996634+00:00` · hour UTC 05 (Thu)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=2.1, ATR%=0.40, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.1
- **atr_pct**: 0.4
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 660.6789,
  "atr_tp": 684.1548,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 670.74
- exit_price: 670.7
- tp_price: 684.15
- sl_price: 660.68
- qty: 0.8 · notional: 53.65920000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9993
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 8.048
- **planned_reward_usd**: 10.728
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0052
- **exit_distance_from_sl_pct**: 1.4939
- **notional**: 53.65920000000001

### Market excursion (MFE / MAE proxy)
- high_water: 674.67 · low_water: 670.74
- current_stop_at_close: 670.74
- **mfe_pct**: 0.5859
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5919

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0052%
- slippage vs planned SL: 1.4939%

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
*journaled_at 2026-05-21T07:01:00.212486Z · journaler v2*
