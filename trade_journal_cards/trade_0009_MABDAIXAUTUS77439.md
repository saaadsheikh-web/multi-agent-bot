# Trade #9 — XAUT-USDT short (daily_breakout_24h)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 748.5 min

> Short flat exit (scratch) on XAUT-USDT (daily_breakout_24h, +0.00%) during good-zone hour 19:00 UTC [killed-agent] trail gave back 1.74% [grade A / 95].

## 1 · Identity
- custom_id: `MABDAIXAUTUS77439`
- agent: `daily_breakout_24h` · profile: `daily_breakout_24h`
- symbol: `XAUT-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-04T06:50:40.285760+00:00`
- closed: `2026-05-04T19:19:10.415595+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> 7 agents agree [daily_breakout_24h,daily_breakout_4h,daily_breakout_12h,daily_breakout_48h,daily_breakout_2h,daily_breakout_8h,hurst_regime] — best: 24h-low break short (4584.0000) vol 2.6x

### Parsed signal features
- **atr_val**: 9.876115513190841
- **v_ratio**: 2.5829547019138097
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4697.472499999999,
  "atr_tp": 45.829,
  "atr_val": 9.876115513190841,
  "v_ratio": 2.5829547019138097
}
```

## 3 · Plan vs Execution
- entry_price: 4582.5
- exit_price: 4582.5
- tp_price: 45.829
- sl_price: 4697.472499999999
- qty: 6.0 · notional: 27.495
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 98.9999
- **planned_sl_distance_pct**: 2.5089
- **planned_r_multiple**: 39.459
- **planned_risk_usd**: 689.835
- **planned_reward_usd**: 27220.026
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 98.9999
- **exit_distance_from_sl_pct**: 2.5089
- **notional**: 27.495

### Market excursion (MFE / MAE proxy)
- high_water: 4582.5 · low_water: 4502.8
- current_stop_at_close: 4556.8336
- **mfe_pct**: 1.7392
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.7392

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 98.9999%
- slippage vs planned SL: 2.5089%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=39.459
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `trail_too_loose`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558513Z · journaler v2*
