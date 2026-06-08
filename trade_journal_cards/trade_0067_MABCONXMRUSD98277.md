# Trade #67 — XMR-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0351 (+0.067% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.62 min

> Short trailed into profit on XMR-USDT (connors_rsi2, +0.07%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD98277`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-07T23:57:59.041513+00:00`
- closed: `2026-05-08T00:04:36.327218+00:00` · hour UTC 00 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [funding,connors_rsi2] — best: Connors RSI2 short: RSI2=96.2, in downtrend

### Parsed signal features
- **rsi2**: 96.2
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 406.55825,
  "atr_tp": 392.539,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 400.55
- exit_price: 400.28
- tp_price: 392.54
- sl_price: 406.56
- qty: 1.3 · notional: 52.0715
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9998
- **planned_sl_distance_pct**: 1.5004
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.813
- **planned_reward_usd**: 10.413
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.9323
- **exit_distance_from_sl_pct**: 1.5678
- **notional**: 52.0715

### Market excursion (MFE / MAE proxy)
- high_water: 400.55 · low_water: 399.74
- current_stop_at_close: 406.56
- **mfe_pct**: 0.2022
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1348

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.9323%
- slippage vs planned SL: 1.5678%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`good_hour`, `confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560146Z · journaler v2*
