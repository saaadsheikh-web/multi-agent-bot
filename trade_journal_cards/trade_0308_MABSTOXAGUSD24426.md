# Trade #308 — XAG-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.3915 (+0.390% if pct available) · **Decision grade:** A (100/100) · **Hold:** 103.85 min

> Long trailed into profit on XAG-USDT (stoch_rsi, +0.39%) trail gave back 0.73% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAGUSD24426`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAG-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T14:33:48.262437+00:00`
- closed: `2026-06-01T16:17:39.424927+00:00` · hour UTC 16 (Mon)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.25 (was 0.00) rsi=36

### Parsed signal features
- **rsi**: 36.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 73.68570000000001,
  "atr_tp": 75.54645,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 74.43
- exit_price: 74.72
- tp_price: 75.55
- sl_price: 73.69
- qty: 135.0 · notional: 100.48050000000002
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5048
- **planned_sl_distance_pct**: 0.9942
- **planned_r_multiple**: 1.514
- **planned_risk_usd**: 99.9
- **planned_reward_usd**: 151.2
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.1151
- **exit_distance_from_sl_pct**: 1.3839
- **notional**: 100.48050000000002

### Market excursion (MFE / MAE proxy)
- high_water: 75.26 · low_water: 74.43
- current_stop_at_close: 74.72772
- **mfe_pct**: 1.1151
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7255

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.1151%
- slippage vs planned SL: 1.3839%

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
*journaled_at 2026-06-05T21:57:18.617998+00:00Z · journaler v2*
