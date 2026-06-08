# Trade #84 — SUI-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.1845 (+0.362% if pct available) · **Decision grade:** B (75/100) · **Hold:** 97.99 min

> Long trailed into profit on SUI-USDT (macd_cross, +0.36%) during dead-zone hour 10:00 UTC [flagged-losing-symbol] trail gave back 0.77% [grade B / 75].

## 1 · Identity
- custom_id: `MABMACSUIUSD3299`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `SUI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-10T08:55:00.403890+00:00`
- closed: `2026-05-10T10:32:59.677245+00:00` · hour UTC 10 (Sun)

## 2 · Hypothesis (why we entered)
> 7 agents agree (cross-family) [daily_breakout_24h,daily_breakout_4h,daily_breakout_12h,daily_breakout_48h,daily_breakout_2h,daily_breakout_8h,macd_cross] — best: [trend+] MACD bull cross hist 0.0028 vol 2.2x

### Parsed signal features
- **atr_val**: 0.016507828489024018
- **trend_score**: 3
- **trend_dir**: UP
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1.109838257266464,
  "atr_tp": 1.1841234854670721,
  "atr_val": 0.016507828489024018,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 1.1341
- exit_price: 1.1382
- tp_price: 1.1841
- sl_price: 1.1098
- qty: 45.0 · notional: 51.03450000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 4.4088
- **planned_sl_distance_pct**: 2.1427
- **planned_r_multiple**: 2.058
- **planned_risk_usd**: 1.0935
- **planned_reward_usd**: 2.25
- **realized_r_multiple**: 0.169
- **exit_distance_from_tp_pct**: 4.0473
- **exit_distance_from_sl_pct**: 2.5042
- **notional**: 51.03450000000001

### Market excursion (MFE / MAE proxy)
- high_water: 1.1469 · low_water: 1.1341
- current_stop_at_close: 1.1386364000000002
- **mfe_pct**: 1.1286
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7671

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.169
- slippage vs planned TP: 4.0473%
- slippage vs planned SL: 2.5042%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** B (75/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour
  - strong planned R:R=2.058
  - multi-agent confluence

## 7 · Tags
`dead_hour`, `losing_symbol`, `confluence`, `trail_too_loose`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.561666Z · journaler v2*
