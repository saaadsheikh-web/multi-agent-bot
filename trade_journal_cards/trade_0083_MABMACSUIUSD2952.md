# Trade #83 — SUI-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.1215 (+0.239% if pct available) · **Decision grade:** C (65/100) · **Hold:** 4.81 min

> Long trailed into profit on SUI-USDT (macd_cross, +0.24%) during dead-zone hour 08:00 UTC [flagged-losing-symbol] [grade C / 65].

## 1 · Identity
- custom_id: `MABMACSUIUSD2952`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `SUI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-10T08:49:14.009810+00:00`
- closed: `2026-05-10T08:54:02.860320+00:00` · hour UTC 08 (Sun)

## 2 · Hypothesis (why we entered)
> 7 agents agree (cross-family) [daily_breakout_24h,daily_breakout_4h,daily_breakout_12h,daily_breakout_48h,daily_breakout_2h,daily_breakout_8h,macd_cross] — best: [trend+] MACD bull cross hist 0.0026 vol 2.0x

### Parsed signal features
- **atr_val**: 0.01630068563188115
- **trend_score**: 3
- **trend_dir**: UP
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1.1069489715521783,
  "atr_tp": 1.1803020568956435,
  "atr_val": 0.01630068563188115,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 1.1319
- exit_price: 1.1346
- tp_price: 1.1803
- sl_price: 1.1069
- qty: 45.0 · notional: 50.9355
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 4.276
- **planned_sl_distance_pct**: 2.2087
- **planned_r_multiple**: 1.936
- **planned_risk_usd**: 1.125
- **planned_reward_usd**: 2.178
- **realized_r_multiple**: 0.108
- **exit_distance_from_tp_pct**: 4.0375
- **exit_distance_from_sl_pct**: 2.4472
- **notional**: 50.9355

### Market excursion (MFE / MAE proxy)
- high_water: 1.1361 · low_water: 1.1319
- current_stop_at_close: 1.1069
- **mfe_pct**: 0.3711
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1325

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.108
- slippage vs planned TP: 4.0375%
- slippage vs planned SL: 2.4472%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** C (65/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour
  - multi-agent confluence

## 7 · Tags
`dead_hour`, `losing_symbol`, `confluence`, `very_short_hold`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.560742Z · journaler v2*
