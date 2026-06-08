# Trade #280 — SOXL-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0344 (-0.034% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.83 min

> Short gave back gains on trail on SOXL-USDT (stoch_rsi, -0.03%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOSOXLUS62487`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `SOXL-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-31T21:21:30.329461+00:00`
- closed: `2026-05-31T21:26:20.390564+00:00` · hour UTC 21 (Sun)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [swing,stoch_rsi,funding_extremes] — best: StochRSI short stoch=0.94 rsi=71

### Parsed signal features
- **rsi**: 71.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 236.845,
  "atr_tp": 230.9825,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 234.67
- exit_price: 234.75
- tp_price: 230.98
- sl_price: 236.84
- qty: 43.0 · notional: 100.90809999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5724
- **planned_sl_distance_pct**: 0.9247
- **planned_r_multiple**: 1.7
- **planned_risk_usd**: 93.31
- **planned_reward_usd**: 158.67
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.6065
- **exit_distance_from_sl_pct**: 0.8906
- **notional**: 100.90809999999999

### Market excursion (MFE / MAE proxy)
- high_water: 234.67 · low_water: 234.29
- current_stop_at_close: 236.84
- **mfe_pct**: 0.1619
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.196

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.6065%
- slippage vs planned SL: 0.8906%

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
  - high confidence (9) lost

## 7 · Tags
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617437+00:00Z · journaler v2*
