# Trade #293 — XAG-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0792 (+0.079% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.1 min

> Short trailed into profit on XAG-USDT (stoch_rsi, +0.08%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAGUSD93598`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAG-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T05:59:59.395003+00:00`
- closed: `2026-06-01T06:03:05.482877+00:00` · hour UTC 06 (Mon)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=1.00 rsi=65

### Parsed signal features
- **rsi**: 65.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 76.62870000000001,
  "atr_tp": 74.73195,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75.87
- exit_price: 75.81
- tp_price: 74.73
- sl_price: 76.63
- qty: 132.0 · notional: 100.14840000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5026
- **planned_sl_distance_pct**: 1.0017
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 100.32
- **planned_reward_usd**: 150.48
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 1.4235
- **exit_distance_from_sl_pct**: 1.0808
- **notional**: 100.14840000000001

### Market excursion (MFE / MAE proxy)
- high_water: 75.87 · low_water: 75.72
- current_stop_at_close: 76.63
- **mfe_pct**: 0.1977
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1186

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 1.4235%
- slippage vs planned SL: 1.0808%

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
`very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617638+00:00Z · journaler v2*
