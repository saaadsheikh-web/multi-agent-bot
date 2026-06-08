# Trade #82 — XMR-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0689 (-0.130% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.1 min

> Short closed in the red without clean exit on XMR-USDT (connors_rsi2, -0.13%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD95423`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-10T06:43:44.603405+00:00`
- closed: `2026-05-10T06:48:50.568867+00:00` · hour UTC 06 (Sun)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [funding,connors_rsi2] — best: Connors RSI2 short: RSI2=95.2, ATR%=0.16, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.2
- **atr_pct**: 0.16
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 413.17605,
  "atr_tp": 398.92859999999996,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 407.07
- exit_price: 407.6
- tp_price: 398.93
- sl_price: 413.18
- qty: 1.3 · notional: 52.9191
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9997
- **planned_sl_distance_pct**: 1.501
- **planned_r_multiple**: 1.332
- **planned_risk_usd**: 7.943
- **planned_reward_usd**: 10.582
- **realized_r_multiple**: -0.009
- **exit_distance_from_tp_pct**: 2.1299
- **exit_distance_from_sl_pct**: 1.3708
- **notional**: 52.9191

### Market excursion (MFE / MAE proxy)
- high_water: 407.07 · low_water: 406.91
- current_stop_at_close: 413.18
- **mfe_pct**: 0.0393
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1695

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.009
- slippage vs planned TP: 2.1299%
- slippage vs planned SL: 1.3708%

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
*journaled_at 2026-05-17T03:54:39.560691Z · journaler v2*
