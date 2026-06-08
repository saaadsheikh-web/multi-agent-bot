# Trade #282 — HYPE-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0420 (+0.041% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.9 min

> Short trailed into profit on HYPE-USDT (stoch_rsi, +0.04%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS66641`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-31T22:30:43.299866+00:00`
- closed: `2026-05-31T22:36:37.451443+00:00` · hour UTC 22 (Sun)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=75

### Parsed signal features
- **rsi**: 75.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 73.17652,
  "atr_tp": 71.36522,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 72.432
- exit_price: 72.402
- tp_price: 71.365
- sl_price: 73.177
- qty: 14.0 · notional: 101.40480000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4731
- **planned_sl_distance_pct**: 1.0286
- **planned_r_multiple**: 1.432
- **planned_risk_usd**: 10.43
- **planned_reward_usd**: 14.938
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.4317
- **exit_distance_from_sl_pct**: 1.07
- **notional**: 101.40480000000001

### Market excursion (MFE / MAE proxy)
- high_water: 72.432 · low_water: 72.215
- current_stop_at_close: 73.177
- **mfe_pct**: 0.2996
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2582

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.4317%
- slippage vs planned SL: 1.07%

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
  - multi-agent confluence

## 7 · Tags
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617477+00:00Z · journaler v2*
