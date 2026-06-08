# Trade #32 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.6780 (+2.009% if pct available) · **Decision grade:** A (100/100) · **Hold:** 270.4 min

> Clean long TP hit on ZEC-USDT (connors_rsi2, +2.01%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD69790`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 5
- opened: `2026-05-05T08:29:51.541017+00:00`
- closed: `2026-05-05T13:00:15.746587+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.9, in uptrend

### Parsed signal features
- **rsi2**: 4.9
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 411.30645,
  "atr_tp": 425.9214
}
```

## 3 · Plan vs Execution
- entry_price: 417.57
- exit_price: 425.96
- tp_price: 425.92
- sl_price: 411.31
- qty: 2.0 · notional: 83.51400000000001
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.9997
- **planned_sl_distance_pct**: 1.4991
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 12.52
- **planned_reward_usd**: 16.7
- **realized_r_multiple**: 0.134
- **exit_distance_from_tp_pct**: -0.0096
- **exit_distance_from_sl_pct**: 3.5084
- **notional**: 83.51400000000001

### Market excursion (MFE / MAE proxy)
- high_water: 425.96 · low_water: 417.57
- current_stop_at_close: 422.55231999999995
- **mfe_pct**: 2.0092
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.134
- slippage vs planned TP: -0.0096%
- slippage vs planned SL: 3.5084%

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
  - (no notable factors)

## 7 · Tags
`long_hold`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558912Z · journaler v2*
