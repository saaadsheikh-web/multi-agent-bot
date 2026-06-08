# Trade #210 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0160 (-0.032% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.51 min

> Long gave back gains on trail on HYPE-USDT (connors_rsi2, -0.03%) (was up 0.51% before reversing) trail gave back 0.55% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS31231`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-24T14:00:33.037881+00:00`
- closed: `2026-05-24T14:04:03.762389+00:00` · hour UTC 14 (Sun)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=2.9, ATR%=0.55, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.9
- **atr_pct**: 0.55
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 62.208659999999995,
  "atr_tp": 64.41912,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 63.221
- exit_price: 63.201
- tp_price: 64.419
- sl_price: 62.209
- qty: 8.0 · notional: 50.5768
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.8949
- **planned_sl_distance_pct**: 1.6007
- **planned_r_multiple**: 1.184
- **planned_risk_usd**: 8.096
- **planned_reward_usd**: 9.584
- **realized_r_multiple**: -0.002
- **exit_distance_from_tp_pct**: 1.9266
- **exit_distance_from_sl_pct**: 1.5691
- **notional**: 50.5768

### Market excursion (MFE / MAE proxy)
- high_water: 63.546 · low_water: 63.221
- current_stop_at_close: 63.221
- **mfe_pct**: 0.5141
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5457

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.002
- slippage vs planned TP: 1.9266%
- slippage vs planned SL: 1.5691%

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
  - high confidence (9) lost

## 7 · Tags
`gave_back_winner`, `trail_too_loose`, `very_short_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905540Z · journaler v2*
