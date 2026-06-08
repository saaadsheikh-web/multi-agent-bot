# Trade #327 — AMD-USDT short (funding_extremes)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** B (85/100) · **Hold:** 177.59 min

> Short flat exit (scratch) on AMD-USDT (funding_extremes, +0.00%) during dead-zone hour 11:00 UTC trail gave back 0.89% [grade B / 85].

## 1 · Identity
- custom_id: `MABFUNAMDUSD89408`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `AMD-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T08:36:49.723865+00:00`
- closed: `2026-06-02T11:34:25.135217+00:00` · hour UTC 11 (Tue)

## 2 · Hypothesis (why we entered)
> Funding extremes SHORT: fr=0.0742%/8h (annual≈81%), RSI=50, EMA50 slope=-0.16%

### Parsed signal features
- **rsi**: 50.15944937019553
- **ema_slope**: -0.15627145779808504
- **atr_pct**: 1.0075336895242268
- **funding_rate**: 0.0007417134217375905
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": 0.0007417134217375905,
  "rsi": 50.15944937019553,
  "ema_slope": -0.15627145779808504,
  "atr_pct": 1.0075336895242268,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 506.42
- exit_price: 506.42
- tp_price: 486.16
- sl_price: 521.61
- qty: 20.0 · notional: 101.284
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 4.0006
- **planned_sl_distance_pct**: 2.9995
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 303.8
- **planned_reward_usd**: 405.2
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 4.0006
- **exit_distance_from_sl_pct**: 2.9995
- **notional**: 101.284

### Market excursion (MFE / MAE proxy)
- high_water: 506.42 · low_water: 501.89
- current_stop_at_close: 506.42
- **mfe_pct**: 0.8945
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8945

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 4.0006%
- slippage vs planned SL: 2.9995%

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

## 7 · Tags
`dead_hour`, `trail_too_loose`, `trail_stop`, `grade_B`

---
*journaled_at 2026-06-05T21:57:18.618429+00:00Z · journaler v2*
