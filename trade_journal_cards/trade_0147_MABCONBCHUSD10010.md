# Trade #147 — BCH-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0140 (-0.027% if pct available) · **Decision grade:** A (100/100) · **Hold:** 197.55 min

> Short gave back gains on trail on BCH-USDT (connors_rsi2, -0.03%) during good-zone hour 00:00 UTC (was up 0.71% before reversing) trail gave back 0.73% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD10010`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-20T20:46:53.296688+00:00`
- closed: `2026-05-21T00:04:26.262850+00:00` · hour UTC 00 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.7, ATR%=0.16, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.7
- **atr_pct**: 0.16
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 379.5084999999999,
  "atr_tp": 366.42199999999997,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 373.9
- exit_price: 374.0
- tp_price: 366.42
- sl_price: 379.51
- qty: 1.4 · notional: 52.34599999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0005
- **planned_sl_distance_pct**: 1.5004
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.854
- **planned_reward_usd**: 10.472
- **realized_r_multiple**: -0.002
- **exit_distance_from_tp_pct**: 2.0273
- **exit_distance_from_sl_pct**: 1.4737
- **notional**: 52.34599999999999

### Market excursion (MFE / MAE proxy)
- high_water: 373.9 · low_water: 371.26
- current_stop_at_close: 373.9
- **mfe_pct**: 0.7061
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7328

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.002
- slippage vs planned TP: 2.0273%
- slippage vs planned SL: 1.4737%

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
*journaled_at 2026-05-21T03:00:48.024462Z · journaler v2*
