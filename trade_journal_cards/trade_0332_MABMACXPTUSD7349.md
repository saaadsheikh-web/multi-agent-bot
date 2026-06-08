# Trade #332 — XPT-USDT short (macd_cross)

**Outcome:** LOSS · **PnL:** -0.1196 (-0.118% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.39 min

> Short closed in the red without clean exit on XPT-USDT (macd_cross, -0.12%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACXPTUSD7349`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `XPT-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T13:35:51.261436+00:00`
- closed: `2026-06-02T13:40:14.393842+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [daily_breakout_4h,daily_breakout_2h,macd_cross,hurst_regime] — best: MACD bear cross hist -0.2509 vol 1.6x

### Parsed signal features
- **atr_val**: 10.874208425503921
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1964.991312638256,
  "atr_tp": 1916.0573747234882,
  "atr_val": 10.874208425503921,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1948.68
- exit_price: 1950.98
- tp_price: 1916.06
- sl_price: 1964.99
- qty: 52.0 · notional: 101.33136000000002
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.674
- **planned_sl_distance_pct**: 0.837
- **planned_r_multiple**: 2.0
- **planned_risk_usd**: 848.12
- **planned_reward_usd**: 1696.24
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.792
- **exit_distance_from_sl_pct**: 0.7189
- **notional**: 101.33136000000002

### Market excursion (MFE / MAE proxy)
- high_water: 1948.68 · low_water: 1948.68
- current_stop_at_close: 1964.99
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.792%
- slippage vs planned SL: 0.7189%

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
  - strong planned R:R=2.0
  - multi-agent confluence
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`confluence`, `very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618541+00:00Z · journaler v2*
