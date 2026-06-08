# Trade #131 — ZEC-USDT short (bb_bounce)

**Outcome:** LOSS · **PnL:** -0.6270 (-1.174% if pct available) · **Decision grade:** A (100/100) · **Hold:** 9.94 min

> Short stopped out at full risk on ZEC-USDT (bb_bounce, -1.17%) trail gave back 1.41% [grade A / 100].

## 1 · Identity
- custom_id: `MABBB_ZECUSD51123`
- agent: `bb_bounce` · profile: `bb_bounce`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-17T20:52:05.354787+00:00`
- closed: `2026-05-17T21:02:01.547888+00:00` · hour UTC 21 (Sun)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: BB upper tag short, RSI 70, width 0.0658

### Parsed signal features
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 539.5521,
  "atr_tp": 515.417,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 534.19
- exit_price: 540.46
- tp_price: 515.42
- sl_price: 539.55
- qty: 1.0 · notional: 53.41900000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 3.5137
- **planned_sl_distance_pct**: 1.0034
- **planned_r_multiple**: 3.502
- **planned_risk_usd**: 5.36
- **planned_reward_usd**: 18.77
- **realized_r_multiple**: -0.117
- **exit_distance_from_tp_pct**: 4.6875
- **exit_distance_from_sl_pct**: -0.1704
- **notional**: 53.41900000000001

### Market excursion (MFE / MAE proxy)
- high_water: 534.19 · low_water: 532.93
- current_stop_at_close: 539.55
- **mfe_pct**: 0.2359
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.4096

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.117
- slippage vs planned TP: 4.6875%
- slippage vs planned SL: -0.1704%

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
  - strong planned R:R=3.502
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T23:01:19.388159Z · journaler v2*
