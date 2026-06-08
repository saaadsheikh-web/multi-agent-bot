# Trade #16 — CL-USDT long (daily_breakout_24h)

**Outcome:** LOSS · **PnL:** -0.9306 (-1.849% if pct available) · **Decision grade:** C (70/100) · **Hold:** 10.93 min

> Long closed in the red without clean exit on CL-USDT (daily_breakout_24h, -1.85%) during dead-zone hour 10:00 UTC [killed-agent] [grade C / 70].

## 1 · Identity
- custom_id: `MABDAICLUSDT90238`
- agent: `daily_breakout_24h` · profile: `daily_breakout_24h`
- symbol: `CL-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T10:23:59.600783+00:00`
- closed: `2026-05-04T10:34:55.167453+00:00` · hour UTC 10 (Mon)

## 2 · Hypothesis (why we entered)
> 3 agents agree [daily_breakout_24h,daily_breakout_4h,daily_breakout_2h] — best: 24h-high break long (104.4600) vol 1.3x

### Parsed signal features
- **atr_val**: 1.218986660371697
- **v_ratio**: 1.3086335119222237
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 104.40299999999999,
  "atr_tp": 213.0892,
  "atr_val": 1.218986660371697,
  "v_ratio": 1.3086335119222237
}
```

## 3 · Plan vs Execution
- entry_price: 107.1
- exit_price: 105.12
- tp_price: 213.0892
- sl_price: 104.40299999999999
- qty: 47.0 · notional: 50.337
- trail_pct: 1.2

### Risk plan
- **planned_tp_distance_pct**: 98.9628
- **planned_sl_distance_pct**: 2.5182
- **planned_r_multiple**: 39.299
- **planned_risk_usd**: 126.759
- **planned_reward_usd**: 4981.4924
- **realized_r_multiple**: -0.007
- **exit_distance_from_tp_pct**: 100.8116
- **exit_distance_from_sl_pct**: 0.6695
- **notional**: 50.337

### Market excursion (MFE / MAE proxy)
- high_water: 107.1 · low_water: 107.1
- current_stop_at_close: 104.40299999999999
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.007
- slippage vs planned TP: 100.8116%
- slippage vs planned SL: 0.6695%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - dead-zone-hour
  - agent-on-kill-list
  - strong planned R:R=39.299
  - multi-agent confluence
  - timed-out loser (no clean exit signal)
  - high confidence (10) lost

## 7 · Tags
`dead_hour`, `killed_agent`, `confluence`, `long_loss`, `time_or_manual`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.558181Z · journaler v2*
