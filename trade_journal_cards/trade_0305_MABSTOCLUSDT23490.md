# Trade #305 — CL-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.3424 (-0.342% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.07 min

> Short closed in the red without clean exit on CL-USDT (stoch_rsi, -0.34%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOCLUSDT23490`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `CL-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T14:18:11.174396+00:00`
- closed: `2026-06-01T14:23:15.351865+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [bb_bounce,zscore_reversion,stoch_rsi,golden_hour] — best: StochRSI short stoch=0.76 (was 1.00) rsi=73

### Parsed signal features
- **rsi**: 73.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 94.45519999999999,
  "atr_tp": 92.1172,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 93.56
- exit_price: 93.88
- tp_price: 92.12
- sl_price: 94.46
- qty: 107.0 · notional: 100.1092
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5391
- **planned_sl_distance_pct**: 0.9619
- **planned_r_multiple**: 1.6
- **planned_risk_usd**: 96.3
- **planned_reward_usd**: 154.08
- **realized_r_multiple**: -0.004
- **exit_distance_from_tp_pct**: 1.8811
- **exit_distance_from_sl_pct**: 0.6199
- **notional**: 100.1092

### Market excursion (MFE / MAE proxy)
- high_water: 93.56 · low_water: 93.56
- current_stop_at_close: 94.46
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.004
- slippage vs planned TP: 1.8811%
- slippage vs planned SL: 0.6199%

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
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617936+00:00Z · journaler v2*
