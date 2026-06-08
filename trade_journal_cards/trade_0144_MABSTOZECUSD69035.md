# Trade #144 — ZEC-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.3609 (+0.702% if pct available) · **Decision grade:** A (100/100) · **Hold:** 57.86 min

> Short trailed into profit on ZEC-USDT (stoch_rsi, +0.70%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD69035`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-19T05:37:16.985023+00:00`
- closed: `2026-05-19T06:35:08.320902+00:00` · hour UTC 06 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=0.90 rsi=69

### Parsed signal features
- **rsi**: 69.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 576.5888,
  "atr_tp": 562.3168,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 571.12
- exit_price: 567.11
- tp_price: 562.32
- sl_price: 576.59
- qty: 0.9 · notional: 51.400800000000004
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5408
- **planned_sl_distance_pct**: 0.9578
- **planned_r_multiple**: 1.609
- **planned_risk_usd**: 4.923
- **planned_reward_usd**: 7.92
- **realized_r_multiple**: 0.073
- **exit_distance_from_tp_pct**: 0.8387
- **exit_distance_from_sl_pct**: 1.6599
- **notional**: 51.400800000000004

### Market excursion (MFE / MAE proxy)
- high_water: 571.12 · low_water: 564.28
- current_stop_at_close: 567.1013999999999
- **mfe_pct**: 1.1976
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4955

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.073
- slippage vs planned TP: 0.8387%
- slippage vs planned SL: 1.6599%

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
`short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T07:00:59.092699Z · journaler v2*
