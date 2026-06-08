# Trade #62 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.1990 (-0.368% if pct available) · **Decision grade:** A (90/100) · **Hold:** 19.38 min

> Long closed in the red without clean exit on ZEC-USDT (connors_rsi2, -0.37%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONZECUSD23089`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-07T03:04:52.062665+00:00`
- closed: `2026-05-07T03:24:15.124440+00:00` · hour UTC 03 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.0, in uptrend

### Parsed signal features
- **rsi2**: 2.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 532.8357500000001,
  "atr_tp": 551.769,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 541.0
- exit_price: 539.01
- tp_price: 551.77
- sl_price: 532.84
- qty: 1.0 · notional: 54.1
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9908
- **planned_sl_distance_pct**: 1.5083
- **planned_r_multiple**: 1.32
- **planned_risk_usd**: 8.16
- **planned_reward_usd**: 10.77
- **realized_r_multiple**: -0.024
- **exit_distance_from_tp_pct**: 2.3586
- **exit_distance_from_sl_pct**: 1.1405
- **notional**: 54.1

### Market excursion (MFE / MAE proxy)
- high_water: 541.0 · low_water: 541.0
- current_stop_at_close: 532.84
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.024
- slippage vs planned TP: 2.3586%
- slippage vs planned SL: 1.1405%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - timed-out loser (no clean exit signal)
  - high confidence (8) lost

## 7 · Tags
`long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560009Z · journaler v2*
