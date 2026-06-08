# Trade #199 — VVV-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +1.5602 (+3.079% if pct available) · **Decision grade:** A (100/100) · **Hold:** 52.47 min

> Long trailed into profit on VVV-USDT (macd_cross, +3.08%) trail gave back 1.05% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACVVVUSD47052`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `VVV-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-23T14:37:33.786556+00:00`
- closed: `2026-05-23T15:30:02.122041+00:00` · hour UTC 15 (Sat)

## 2 · Hypothesis (why we entered)
> MACD bull cross hist 0.0062 vol 2.5x

### Parsed signal features
- **atr_val**: 0.4274655457953254
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 16.81880168130701,
  "atr_tp": 18.742396637385976,
  "atr_val": 0.4274655457953254,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 17.473
- exit_price: 18.011
- tp_price: 18.742
- sl_price: 16.819
- qty: 29.0 · notional: 50.6717
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 7.2626
- **planned_sl_distance_pct**: 3.7429
- **planned_r_multiple**: 1.94
- **planned_risk_usd**: 18.966
- **planned_reward_usd**: 36.801
- **realized_r_multiple**: 0.082
- **exit_distance_from_tp_pct**: 4.1836
- **exit_distance_from_sl_pct**: 6.822
- **notional**: 50.6717

### Market excursion (MFE / MAE proxy)
- high_water: 18.195 · low_water: 17.473
- current_stop_at_close: 18.01305
- **mfe_pct**: 4.1321
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0531

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.082
- slippage vs planned TP: 4.1836%
- slippage vs planned SL: 6.822%

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
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905298Z · journaler v2*
