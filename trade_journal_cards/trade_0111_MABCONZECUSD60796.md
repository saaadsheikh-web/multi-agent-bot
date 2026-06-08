# Trade #111 — ZEC-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0099 (-0.020% if pct available) · **Decision grade:** A (100/100) · **Hold:** 35.62 min

> Short gave back gains on trail on ZEC-USDT (connors_rsi2, -0.02%) during good-zone hour 05:00 UTC (was up 0.67% before reversing) trail gave back 0.69% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD60796`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-12T04:39:58.246649+00:00`
- closed: `2026-05-12T05:15:35.552493+00:00` · hour UTC 05 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.1, ATR%=0.35, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.1
- **atr_pct**: 0.35
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 566.3091000000001,
  "atr_tp": 546.7812,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 557.94
- exit_price: 558.05
- tp_price: 546.78
- sl_price: 566.31
- qty: 0.9 · notional: 50.21460000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0002
- **planned_sl_distance_pct**: 1.5002
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.533
- **planned_reward_usd**: 10.044
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.0199
- **exit_distance_from_sl_pct**: 1.4804
- **notional**: 50.21460000000001

### Market excursion (MFE / MAE proxy)
- high_water: 557.94 · low_water: 554.2
- current_stop_at_close: 557.94
- **mfe_pct**: 0.6703
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.69

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.0199%
- slippage vs planned SL: 1.4804%

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
*journaled_at 2026-05-17T03:54:39.562491Z · journaler v2*
