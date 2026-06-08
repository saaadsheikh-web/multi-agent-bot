# Trade #297 — CL-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +2.2880 (+2.277% if pct available) · **Decision grade:** A (100/100) · **Hold:** 33.29 min

> Clean long TP hit on CL-USDT (macd_cross, +2.28%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACCLUSDT19841`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `CL-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T13:17:22.853384+00:00`
- closed: `2026-06-01T13:50:40.439897+00:00` · hour UTC 13 (Mon)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [daily_breakout_24h,daily_breakout_4h,daily_breakout_2h,macd_cross] — best: MACD bull cross hist 0.0441 vol 2.5x

### Parsed signal features
- **atr_val**: 0.6780337346769465
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 90.31294939798458,
  "atr_tp": 93.36410120403083,
  "atr_val": 0.6780337346769465,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 91.34
- exit_price: 93.42
- tp_price: 93.36
- sl_price: 90.31
- qty: 110.0 · notional: 100.47400000000002
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.2115
- **planned_sl_distance_pct**: 1.1277
- **planned_r_multiple**: 1.961
- **planned_risk_usd**: 113.3
- **planned_reward_usd**: 222.2
- **realized_r_multiple**: 0.02
- **exit_distance_from_tp_pct**: -0.0657
- **exit_distance_from_sl_pct**: 3.4049
- **notional**: 100.47400000000002

### Market excursion (MFE / MAE proxy)
- high_water: 93.42 · low_water: 91.34
- current_stop_at_close: 92.4858
- **mfe_pct**: 2.2772
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.02
- slippage vs planned TP: -0.0657%
- slippage vs planned SL: 3.4049%

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

## 7 · Tags
`confluence`, `tp_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617823+00:00Z · journaler v2*
