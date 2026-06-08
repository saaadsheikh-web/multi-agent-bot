# Trade #177 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7520 (-1.453% if pct available) · **Decision grade:** B (85/100) · **Hold:** 27.28 min

> Long stopped out at full risk on ZEC-USDT (connors_rsi2, -1.45%) during dead-zone hour 10:00 UTC trail gave back 1.47% [grade B / 85].

## 1 · Identity
- custom_id: `MABCONZECUSD42401`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T09:33:23.401585+00:00`
- closed: `2026-05-22T10:00:40.213462+00:00` · hour UTC 10 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.1, ATR%=0.30, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.1
- **atr_pct**: 0.3
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 637.6496,
  "atr_tp": 660.3072000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 646.84
- exit_price: 637.44
- tp_price: 660.31
- sl_price: 637.65
- qty: 0.8 · notional: 51.747200000000014
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0824
- **planned_sl_distance_pct**: 1.4208
- **planned_r_multiple**: 1.466
- **planned_risk_usd**: 7.352
- **planned_reward_usd**: 10.776
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.5357
- **exit_distance_from_sl_pct**: -0.0325
- **notional**: 51.747200000000014

### Market excursion (MFE / MAE proxy)
- high_water: 646.95 · low_water: 646.84
- current_stop_at_close: 637.65
- **mfe_pct**: 0.017
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.4702

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.5357%
- slippage vs planned SL: -0.0325%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour
  - high confidence (8) lost

## 7 · Tags
`dead_hour`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_B`

---
*journaled_at 2026-05-23T15:00:56.570541Z · journaler v2*
