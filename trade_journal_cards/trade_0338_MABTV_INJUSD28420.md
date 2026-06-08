# Trade #338 — INJ-USDT long (tv_fibonacci)

**Outcome:** LOSS · **PnL:** -4.2800 (-0.612% if pct available) · **Decision grade:** A (100/100) · **Hold:** 8.72 min

> Long closed in the red without clean exit on INJ-USDT (tv_fibonacci, -0.61%) during good-zone hour 19:00 UTC trail gave back 0.66% [grade A / 100].

## 1 · Identity
- custom_id: `MABTV_INJUSD28420`
- agent: `tv_fibonacci` · profile: `fibonacci`
- symbol: `INJ-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T19:27:01.758684+00:00`
- closed: `2026-06-02T19:35:45.038720+00:00` · hour UTC 19 (Tue)

## 2 · Hypothesis (why we entered)
> TV/fibonacci_long conf=9

### Parsed signal features
- **strategy**: fibonacci_long

### Raw meta from agent
```json
{
  "strategy": "fibonacci_long",
  "price_hint": null,
  "source": "tradingview"
}
```

## 3 · Plan vs Execution
- entry_price: 6.535
- exit_price: 6.495
- tp_price: 13.005
- sl_price: 6.339
- qty: 107.0 · notional: 699.245
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 99.0054
- **planned_sl_distance_pct**: 2.9992
- **planned_r_multiple**: 33.011
- **planned_risk_usd**: 20.972
- **planned_reward_usd**: 692.29
- **realized_r_multiple**: -0.204
- **exit_distance_from_tp_pct**: 99.6174
- **exit_distance_from_sl_pct**: 2.3871
- **notional**: 699.245

### Market excursion (MFE / MAE proxy)
- high_water: 6.538 · low_water: 6.535
- current_stop_at_close: 6.339
- **mfe_pct**: 0.0459
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.658

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.204
- slippage vs planned TP: 99.6174%
- slippage vs planned SL: 2.3871%

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
  - strong planned R:R=33.011
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `trail_too_loose`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618722+00:00Z · journaler v2*
