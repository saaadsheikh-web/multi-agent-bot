# Trade #148 — BCH-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0280 (-0.054% if pct available) · **Decision grade:** A (100/100) · **Hold:** 196.23 min

> Short gave back gains on trail on BCH-USDT (connors_rsi2, -0.05%) during good-zone hour 00:00 UTC (was up 0.68% before reversing) trail gave back 0.73% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD10098`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-20T20:48:20.643152+00:00`
- closed: `2026-05-21T00:04:34.420673+00:00` · hour UTC 00 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.2, ATR%=0.16, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.2
- **atr_pct**: 0.16
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 379.407,
  "atr_tp": 366.324,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 373.8
- exit_price: 374.0
- tp_price: 366.32
- sl_price: 379.41
- qty: 1.4 · notional: 52.331999999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0011
- **planned_sl_distance_pct**: 1.5008
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.854
- **planned_reward_usd**: 10.472
- **realized_r_multiple**: -0.004
- **exit_distance_from_tp_pct**: 2.0546
- **exit_distance_from_sl_pct**: 1.4473
- **notional**: 52.331999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 373.8 · low_water: 371.26
- current_stop_at_close: 373.8
- **mfe_pct**: 0.6795
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.733

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.004
- slippage vs planned TP: 2.0546%
- slippage vs planned SL: 1.4473%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `gave_back_winner`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-21T03:00:48.024489Z · journaler v2*
