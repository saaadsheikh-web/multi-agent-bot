# Trade #296 — XAG-USDT short (macd_cross)

**Outcome:** WIN · **PnL:** +0.7906 (+0.786% if pct available) · **Decision grade:** A (100/100) · **Hold:** 78.37 min

> Short trailed into profit on XAG-USDT (macd_cross, +0.79%) trail gave back 0.81% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACXAGUSD19671`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `XAG-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T13:14:32.190830+00:00`
- closed: `2026-06-01T14:32:54.172646+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [daily_breakout_4h,daily_breakout_2h,macd_cross,hurst_regime] — best: MACD bear cross hist -0.0273 vol 1.6x

### Parsed signal features
- **atr_val**: 0.41383522067135825
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 75.65075283100704,
  "atr_tp": 73.78849433798592,
  "atr_val": 0.41383522067135825,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75.11
- exit_price: 74.52
- tp_price: 73.79
- sl_price: 75.65
- qty: 134.0 · notional: 100.6474
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.7574
- **planned_sl_distance_pct**: 0.7189
- **planned_r_multiple**: 2.445
- **planned_risk_usd**: 72.36
- **planned_reward_usd**: 176.88
- **realized_r_multiple**: 0.011
- **exit_distance_from_tp_pct**: 0.9719
- **exit_distance_from_sl_pct**: 1.5045
- **notional**: 100.6474

### Market excursion (MFE / MAE proxy)
- high_water: 75.11 · low_water: 73.91
- current_stop_at_close: 74.50912
- **mfe_pct**: 1.5977
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8121

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.011
- slippage vs planned TP: 0.9719%
- slippage vs planned SL: 1.5045%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - strong planned R:R=2.445
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617981+00:00Z · journaler v2*
