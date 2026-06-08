# Trade #175 — XMR-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0052 (-0.010% if pct available) · **Decision grade:** A (100/100) · **Hold:** 16.68 min

> Short gave back gains on trail on XMR-USDT (connors_rsi2, -0.01%) (was up 0.62% before reversing) trail gave back 0.63% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD29913`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-22T06:05:14.671013+00:00`
- closed: `2026-05-22T06:21:55.376931+00:00` · hour UTC 06 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=99.7, ATR%=0.26, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.7
- **atr_pct**: 0.26
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 391.77984999999995,
  "atr_tp": 378.2702,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 385.92
- exit_price: 385.96
- tp_price: 378.27
- sl_price: 391.78
- qty: 1.3 · notional: 50.1696
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9823
- **planned_sl_distance_pct**: 1.5184
- **planned_r_multiple**: 1.306
- **planned_risk_usd**: 7.618
- **planned_reward_usd**: 9.945
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 1.9926
- **exit_distance_from_sl_pct**: 1.5081
- **notional**: 50.1696

### Market excursion (MFE / MAE proxy)
- high_water: 385.92 · low_water: 383.54
- current_stop_at_close: 385.92
- **mfe_pct**: 0.6167
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6271

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 1.9926%
- slippage vs planned SL: 1.5081%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (8) lost

## 7 · Tags
`gave_back_winner`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570495Z · journaler v2*
