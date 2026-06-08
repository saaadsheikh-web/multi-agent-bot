# Trade #134 — NVDA-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0276 (-0.054% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.09 min

> Short gave back gains on trail on NVDA-USDT (connors_rsi2, -0.05%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONNVDAUS33543`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `NVDA-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-18T19:45:45.994532+00:00`
- closed: `2026-05-19T01:45:51.500944+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.9, ATR%=0.31, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.9
- **atr_pct**: 0.31
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 225.23864999999998,
  "atr_tp": 217.4718,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 221.91
- exit_price: 222.03
- tp_price: 217.47
- sl_price: 225.24
- qty: 23.0 · notional: 51.039300000000004
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0008
- **planned_sl_distance_pct**: 1.5006
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 76.59
- **planned_reward_usd**: 102.12
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0549
- **exit_distance_from_sl_pct**: 1.4465
- **notional**: 51.039300000000004

### Market excursion (MFE / MAE proxy)
- high_water: 221.91 · low_water: 221.22
- current_stop_at_close: 225.24
- **mfe_pct**: 0.3109
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.365

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0549%
- slippage vs planned SL: 1.4465%

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
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T03:00:53.640162Z · journaler v2*
