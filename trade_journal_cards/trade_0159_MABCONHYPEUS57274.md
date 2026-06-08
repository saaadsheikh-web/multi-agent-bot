# Trade #159 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.2097 (-0.403% if pct available) · **Decision grade:** B (85/100) · **Hold:** 32.25 min

> Long gave back gains on trail on HYPE-USDT (connors_rsi2, -0.40%) during dead-zone hour 10:00 UTC (was up 0.70% before reversing) trail gave back 1.10% [grade B / 85].

## 1 · Identity
- custom_id: `MABCONHYPEUS57274`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T09:54:36.129683+00:00`
- closed: `2026-05-21T10:26:51.333952+00:00` · hour UTC 10 (Thu)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=1.8, ATR%=0.59, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.8
- **atr_pct**: 0.59
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 56.99998,
  "atr_tp": 59.025360000000006,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 57.868
- exit_price: 57.635
- tp_price: 59.025
- sl_price: 57.0
- qty: 9.0 · notional: 52.0812
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9994
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.812
- **planned_reward_usd**: 10.413
- **realized_r_multiple**: -0.027
- **exit_distance_from_tp_pct**: 2.402
- **exit_distance_from_sl_pct**: 1.0973
- **notional**: 52.0812

### Market excursion (MFE / MAE proxy)
- high_water: 58.271 · low_water: 57.868
- current_stop_at_close: 57.868
- **mfe_pct**: 0.6964
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0991

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.027
- slippage vs planned TP: 2.402%
- slippage vs planned SL: 1.0973%

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
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-23T15:00:56.570210Z · journaler v2*
