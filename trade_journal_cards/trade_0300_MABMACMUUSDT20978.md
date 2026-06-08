# Trade #300 — MU-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.2350 (+0.229% if pct available) · **Decision grade:** A (100/100) · **Hold:** 17.16 min

> Long trailed into profit on MU-USDT (macd_cross, +0.23%) trail gave back 0.85% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACMUUSDT20978`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `MU-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T13:36:19.903899+00:00`
- closed: `2026-06-01T13:53:29.484135+00:00` · hour UTC 13 (Mon)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [daily_breakout_24h,daily_breakout_4h,daily_breakout_2h,macd_cross] — best: MACD bull cross hist 0.7877 vol 1.3x

### Parsed signal features
- **atr_val**: 11.4077508627774
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1011.1983737058339,
  "atr_tp": 1062.533252588332,
  "atr_val": 11.4077508627774,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1027.16
- exit_price: 1029.51
- tp_price: 1062.53
- sl_price: 1011.2
- qty: 10.0 · notional: 102.71600000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 3.4435
- **planned_sl_distance_pct**: 1.5538
- **planned_r_multiple**: 2.216
- **planned_risk_usd**: 159.6
- **planned_reward_usd**: 353.7
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 3.2147
- **exit_distance_from_sl_pct**: 1.7826
- **notional**: 102.71600000000001

### Market excursion (MFE / MAE proxy)
- high_water: 1038.24 · low_water: 1027.16
- current_stop_at_close: 1031.26864
- **mfe_pct**: 1.0787
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8499

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 3.2147%
- slippage vs planned SL: 1.7826%

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
  - strong planned R:R=2.216
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617848+00:00Z · journaler v2*
