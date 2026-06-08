# Trade #51 — TAO-USDT short (daily_breakout_2h)

**Outcome:** WIN · **PnL:** +0.0810 (+0.155% if pct available) · **Decision grade:** A (90/100) · **Hold:** 6.96 min

> Short trailed into profit on TAO-USDT (daily_breakout_2h, +0.16%) [flagged-losing-symbol] [grade A / 90].

## 1 · Identity
- custom_id: `MABDAITAOUSD32483`
- agent: `daily_breakout_2h` · profile: `daily_breakout_2h`
- symbol: `TAO-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-06T01:54:44.895056+00:00`
- closed: `2026-05-06T02:01:42.642273+00:00` · hour UTC 02 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [daily_breakout_2h,fib_hotzone] — best: 2h-low break short (290.0100) vol 1.3x

### Parsed signal features
- **atr_val**: 4.768185775366478
- **v_ratio**: 1.3120598391189442
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 292.05792,
  "atr_tp": 2.8974,
  "atr_val": 4.768185775366478,
  "v_ratio": 1.3120598391189442,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 289.79
- exit_price: 289.34
- tp_price: 2.9
- sl_price: 292.06
- qty: 18.0 · notional: 52.1622
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 98.9993
- **planned_sl_distance_pct**: 0.7833
- **planned_r_multiple**: 126.387
- **planned_risk_usd**: 40.86
- **planned_reward_usd**: 5164.02
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: 98.844
- **exit_distance_from_sl_pct**: 0.9386
- **notional**: 52.1622

### Market excursion (MFE / MAE proxy)
- high_water: 289.79 · low_water: 288.92
- current_stop_at_close: 292.06
- **mfe_pct**: 0.3002
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1449

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.002
- slippage vs planned TP: 98.844%
- slippage vs planned SL: 0.9386%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - flagged-losing-symbol
  - strong planned R:R=126.387
  - multi-agent confluence

## 7 · Tags
`losing_symbol`, `confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559646Z · journaler v2*
