# Trade #295 — CL-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.8436 (-0.841% if pct available) · **Decision grade:** B (85/100) · **Hold:** 104.71 min

> Short closed in the red without clean exit on CL-USDT (stoch_rsi, -0.84%) during dead-zone hour 08:00 UTC trail gave back 0.91% [grade B / 85].

## 1 · Identity
- custom_id: `MABSTOCLUSDT97474`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `CL-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T07:04:35.613144+00:00`
- closed: `2026-06-01T08:49:18.157106+00:00` · hour UTC 08 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [swing,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=71

### Parsed signal features
- **rsi**: 71.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 91.24340000000001,
  "atr_tp": 88.9849,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 90.34
- exit_price: 91.1
- tp_price: 88.98
- sl_price: 91.24
- qty: 111.0 · notional: 100.27740000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5054
- **planned_sl_distance_pct**: 0.9962
- **planned_r_multiple**: 1.511
- **planned_risk_usd**: 99.9
- **planned_reward_usd**: 150.96
- **realized_r_multiple**: -0.008
- **exit_distance_from_tp_pct**: 2.3467
- **exit_distance_from_sl_pct**: 0.155
- **notional**: 100.27740000000001

### Market excursion (MFE / MAE proxy)
- high_water: 90.34 · low_water: 90.28
- current_stop_at_close: 91.24
- **mfe_pct**: 0.0664
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.9077

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.008
- slippage vs planned TP: 2.3467%
- slippage vs planned SL: 0.155%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour
  - multi-agent confluence
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `confluence`, `trail_too_loose`, `time_or_manual`, `grade_B`

---
*journaled_at 2026-06-05T21:57:18.617754+00:00Z · journaler v2*
