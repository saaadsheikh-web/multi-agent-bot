# Trade #163 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0288 (-0.054% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.21 min

> Long gave back gains on trail on HYPE-USDT (connors_rsi2, -0.05%) (was up 0.52% before reversing) trail gave back 0.57% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS81662`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T16:41:04.037977+00:00`
- closed: `2026-05-21T16:44:16.905942+00:00` · hour UTC 16 (Thu)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.5, ATR%=0.99, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.5
- **atr_pct**: 0.99
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 58.28048,
  "atr_tp": 60.35136,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 59.114
- exit_price: 59.082
- tp_price: 60.351
- sl_price: 58.28
- qty: 9.0 · notional: 53.2026
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0926
- **planned_sl_distance_pct**: 1.4108
- **planned_r_multiple**: 1.483
- **planned_risk_usd**: 7.506
- **planned_reward_usd**: 11.133
- **realized_r_multiple**: -0.004
- **exit_distance_from_tp_pct**: 2.1467
- **exit_distance_from_sl_pct**: 1.3567
- **notional**: 53.2026

### Market excursion (MFE / MAE proxy)
- high_water: 59.42 · low_water: 59.114
- current_stop_at_close: 59.114
- **mfe_pct**: 0.5176
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5718

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.004
- slippage vs planned TP: 2.1467%
- slippage vs planned SL: 1.3567%

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
*journaled_at 2026-05-23T15:00:56.570277Z · journaler v2*
