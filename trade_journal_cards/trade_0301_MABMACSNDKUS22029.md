# Trade #301 — SNDK-USDT short (macd_cross)

**Outcome:** WIN · **PnL:** +2.1582 (+2.142% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.93 min

> Short trailed into profit on SNDK-USDT (macd_cross, +2.14%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACSNDKUS22029`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `SNDK-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T13:53:50.944862+00:00`
- closed: `2026-06-01T14:00:46.485125+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [daily_breakout_4h,daily_breakout_2h,macd_cross] — best: MACD bear cross hist -0.3427 vol 1.5x

### Parsed signal features
- **atr_val**: 16.91213957956665
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1761.75820936935,
  "atr_tp": 1685.6535812613001,
  "atr_val": 16.91213957956665,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1737.03
- exit_price: 1699.82
- tp_price: 1685.65
- sl_price: 1761.76
- qty: 5.8 · notional: 100.74774
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.9579
- **planned_sl_distance_pct**: 1.4237
- **planned_r_multiple**: 2.078
- **planned_risk_usd**: 143.434
- **planned_reward_usd**: 298.004
- **realized_r_multiple**: 0.015
- **exit_distance_from_tp_pct**: 0.8158
- **exit_distance_from_sl_pct**: 3.5659
- **notional**: 100.74774

### Market excursion (MFE / MAE proxy)
- high_water: 1737.03 · low_water: 1697.55
- current_stop_at_close: 1714.5255
- **mfe_pct**: 2.2728
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1307

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.015
- slippage vs planned TP: 0.8158%
- slippage vs planned SL: 3.5659%

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
  - strong planned R:R=2.078
  - multi-agent confluence

## 7 · Tags
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617871+00:00Z · journaler v2*
