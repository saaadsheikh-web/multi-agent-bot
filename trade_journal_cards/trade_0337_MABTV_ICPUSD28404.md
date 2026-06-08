# Trade #337 — ICP-USDT long (tv_fibonacci)

**Outcome:** LOSS · **PnL:** -5.8060 (-0.829% if pct available) · **Decision grade:** A (100/100) · **Hold:** 8.92 min

> Long gave back gains on trail on ICP-USDT (tv_fibonacci, -0.83%) during good-zone hour 19:00 UTC trail gave back 0.96% [grade A / 100].

## 1 · Identity
- custom_id: `MABTV_ICPUSD28404`
- agent: `tv_fibonacci` · profile: `fibonacci`
- symbol: `ICP-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T19:26:45.853312+00:00`
- closed: `2026-06-02T19:35:40.899324+00:00` · hour UTC 19 (Tue)

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
- entry_price: 3.014
- exit_price: 2.989
- tp_price: 5.998
- sl_price: 2.924
- qty: 23224.0 · notional: 699.97136
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 99.0046
- **planned_sl_distance_pct**: 2.9861
- **planned_r_multiple**: 33.155
- **planned_risk_usd**: 2090.16
- **planned_reward_usd**: 69300.416
- **realized_r_multiple**: -0.003
- **exit_distance_from_tp_pct**: 99.8341
- **exit_distance_from_sl_pct**: 2.1566
- **notional**: 699.97136

### Market excursion (MFE / MAE proxy)
- high_water: 3.018 · low_water: 3.014
- current_stop_at_close: 2.924
- **mfe_pct**: 0.1327
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.9622

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.003
- slippage vs planned TP: 99.8341%
- slippage vs planned SL: 2.1566%

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
  - strong planned R:R=33.155
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618703+00:00Z · journaler v2*
