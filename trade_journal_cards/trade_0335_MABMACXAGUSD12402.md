# Trade #335 — XAG-USDT short (macd_cross)

**Outcome:** WIN · **PnL:** +0.7980 (+0.792% if pct available) · **Decision grade:** A (100/100) · **Hold:** 578.25 min

> Short trailed into profit on XAG-USDT (macd_cross, +0.79%) during good-zone hour 00:00 UTC trail gave back 0.96% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACXAGUSD12402`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `XAG-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T15:00:03.922050+00:00`
- closed: `2026-06-03T00:38:18.963156+00:00` · hour UTC 00 (Wed)

## 2 · Hypothesis (why we entered)
> 5 agents agree (cross-family) [daily_breakout_4h,daily_breakout_2h,macd_cross,hurst_regime,us_open] — best: MACD bear cross hist -0.0155 vol 1.8x

### Parsed signal features
- **atr_val**: 0.518811100067182
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 76.55821665010077,
  "atr_tp": 74.22356669979845,
  "atr_val": 0.518811100067182,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75.75
- exit_price: 75.15
- tp_price: 74.22
- sl_price: 76.56
- qty: 133.0 · notional: 100.7475
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.0198
- **planned_sl_distance_pct**: 1.0693
- **planned_r_multiple**: 1.889
- **planned_risk_usd**: 107.73
- **planned_reward_usd**: 203.49
- **realized_r_multiple**: 0.007
- **exit_distance_from_tp_pct**: 1.2277
- **exit_distance_from_sl_pct**: 1.8614
- **notional**: 100.7475

### Market excursion (MFE / MAE proxy)
- high_water: 75.75 · low_water: 74.42
- current_stop_at_close: 75.144
- **mfe_pct**: 1.7558
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.9637

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.007
- slippage vs planned TP: 1.2277%
- slippage vs planned SL: 1.8614%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`good_hour`, `confluence`, `trail_too_loose`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618748+00:00Z · journaler v2*
