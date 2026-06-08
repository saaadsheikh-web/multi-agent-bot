# Trade #69 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0130 (-0.023% if pct available) · **Decision grade:** A (100/100) · **Hold:** 85.22 min

> Long gave back gains on trail on ZEC-USDT (connors_rsi2, -0.02%) (was up 0.75% before reversing) trail gave back 0.77% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD14930`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-08T04:35:31.672472+00:00`
- closed: `2026-05-08T06:00:44.589981+00:00` · hour UTC 06 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.9, in uptrend

### Parsed signal features
- **rsi2**: 4.9
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 558.3965,
  "atr_tp": 578.2379999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 567.46
- exit_price: 567.33
- tp_price: 578.24
- sl_price: 558.4
- qty: 1.0 · notional: 56.74600000000001
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.8997
- **planned_sl_distance_pct**: 1.5966
- **planned_r_multiple**: 1.19
- **planned_risk_usd**: 9.06
- **planned_reward_usd**: 10.78
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 1.9226
- **exit_distance_from_sl_pct**: 1.5737
- **notional**: 56.74600000000001

### Market excursion (MFE / MAE proxy)
- high_water: 571.7 · low_water: 567.46
- current_stop_at_close: 567.46
- **mfe_pct**: 0.7472
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7701

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 1.9226%
- slippage vs planned SL: 1.5737%

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
  - high confidence (8) lost

## 7 · Tags
`gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560226Z · journaler v2*
