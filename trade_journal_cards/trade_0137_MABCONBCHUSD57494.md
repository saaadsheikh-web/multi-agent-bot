# Trade #137 — BCH-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7420 (-1.402% if pct available) · **Decision grade:** A (100/100) · **Hold:** 271.26 min

> Short gave back gains on trail on BCH-USDT (connors_rsi2, -1.40%) trail gave back 1.67% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD57494`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-19T02:24:55.671881+00:00`
- closed: `2026-05-19T06:56:11.426105+00:00` · hour UTC 06 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.2, ATR%=0.25, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.2
- **atr_pct**: 0.25
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 383.5684999999999,
  "atr_tp": 370.342,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 377.9
- exit_price: 383.2
- tp_price: 370.34
- sl_price: 383.57
- qty: 1.4 · notional: 52.90599999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0005
- **planned_sl_distance_pct**: 1.5004
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.938
- **planned_reward_usd**: 10.584
- **realized_r_multiple**: -0.093
- **exit_distance_from_tp_pct**: 3.403
- **exit_distance_from_sl_pct**: 0.0979
- **notional**: 52.90599999999999

### Market excursion (MFE / MAE proxy)
- high_water: 377.9 · low_water: 376.9
- current_stop_at_close: 383.57
- **mfe_pct**: 0.2646
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.6671

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.093
- slippage vs planned TP: 3.403%
- slippage vs planned SL: 0.0979%

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
  - high confidence (9) lost

## 7 · Tags
`trail_too_loose`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T07:00:59.092716Z · journaler v2*
