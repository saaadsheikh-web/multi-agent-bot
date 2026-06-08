# Trade #14 — XAU-USDT short (daily_breakout_24h)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 552.37 min

> Short flat exit (scratch) on XAU-USDT (daily_breakout_24h, +0.00%) during good-zone hour 19:00 UTC [killed-agent] trail gave back 0.94% [grade A / 95].

## 1 · Identity
- custom_id: `MABDAIXAUUSD89207`
- agent: `daily_breakout_24h` · profile: `daily_breakout_24h`
- symbol: `XAU-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-04T10:06:48.487370+00:00`
- closed: `2026-05-04T19:19:10.433267+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> 6 agents agree [daily_breakout_24h,daily_breakout_4h,daily_breakout_12h,daily_breakout_48h,daily_breakout_2h,daily_breakout_8h] — best: 24h-low break short (4571.7200) vol 3.6x

### Parsed signal features
- **atr_val**: 11.99703517793502
- **v_ratio**: 3.5957903924267343
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4661.3412499999995,
  "atr_tp": 45.476499999999994,
  "atr_val": 11.99703517793502,
  "v_ratio": 3.5957903924267343
}
```

## 3 · Plan vs Execution
- entry_price: 4548.04
- exit_price: 4548.04
- tp_price: 45.476499999999994
- sl_price: 4661.3412499999995
- qty: 11.0 · notional: 50.028439999999996
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 99.0001
- **planned_sl_distance_pct**: 2.4912
- **planned_r_multiple**: 39.74
- **planned_risk_usd**: 1246.3137
- **planned_reward_usd**: 49528.1985
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0001
- **exit_distance_from_sl_pct**: 2.4912
- **notional**: 50.028439999999996

### Market excursion (MFE / MAE proxy)
- high_water: 4548.04 · low_water: 4505.09
- current_stop_at_close: 4661.3412499999995
- **mfe_pct**: 0.9444
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.9444

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0001%
- slippage vs planned SL: 2.4912%

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
  - strong planned R:R=39.74
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `trail_too_loose`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558561Z · journaler v2*
