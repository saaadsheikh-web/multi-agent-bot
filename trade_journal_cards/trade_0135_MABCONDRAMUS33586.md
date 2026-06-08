# Trade #135 — DRAM-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2958 (+0.588% if pct available) · **Decision grade:** A (100/100) · **Hold:** 353.18 min

> Short trailed into profit on DRAM-USDT (connors_rsi2, +0.59%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONDRAMUS33586`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `DRAM-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-18T19:46:27.585581+00:00`
- closed: `2026-05-19T01:39:38.371837+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [funding,connors_rsi2] — best: Connors RSI2 short: RSI2=95.6, ATR%=0.44, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.6
- **atr_pct**: 0.44
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 50.04965,
  "atr_tp": 48.3238,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 49.31
- exit_price: 49.02
- tp_price: 48.32
- sl_price: 50.05
- qty: 102.0 · notional: 50.296200000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0077
- **planned_sl_distance_pct**: 1.5007
- **planned_r_multiple**: 1.338
- **planned_risk_usd**: 75.48
- **planned_reward_usd**: 100.98
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.4196
- **exit_distance_from_sl_pct**: 2.0888
- **notional**: 50.296200000000006

### Market excursion (MFE / MAE proxy)
- high_water: 49.31 · low_water: 48.85
- current_stop_at_close: 49.143100000000004
- **mfe_pct**: 0.9329
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3448

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.4196%
- slippage vs planned SL: 2.0888%

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
`good_hour`, `confluence`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T03:00:53.640111Z · journaler v2*
