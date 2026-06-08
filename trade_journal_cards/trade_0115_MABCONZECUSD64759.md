# Trade #115 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1090 (+0.196% if pct available) · **Decision grade:** B (85/100) · **Hold:** 73.52 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.20%) during dead-zone hour 10:00 UTC trail gave back 0.62% [grade B / 85].

## 1 · Identity
- custom_id: `MABCONZECUSD64759`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-13T09:32:40.486815+00:00`
- closed: `2026-05-13T10:46:11.907950+00:00` · hour UTC 10 (Wed)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.2, ATR%=0.31, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.2
- **atr_pct**: 0.31
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 563.2641,
  "atr_tp": 543.8412000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 554.88
- exit_price: 553.79
- tp_price: 543.84
- sl_price: 563.26
- qty: 1.0 · notional: 55.488
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9896
- **planned_sl_distance_pct**: 1.5102
- **planned_r_multiple**: 1.317
- **planned_risk_usd**: 8.38
- **planned_reward_usd**: 11.04
- **realized_r_multiple**: 0.013
- **exit_distance_from_tp_pct**: 1.7932
- **exit_distance_from_sl_pct**: 1.7067
- **notional**: 55.488

### Market excursion (MFE / MAE proxy)
- high_water: 554.88 · low_water: 550.33
- current_stop_at_close: 553.63198
- **mfe_pct**: 0.82
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6236

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.013
- slippage vs planned TP: 1.7932%
- slippage vs planned SL: 1.7067%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.562647Z · journaler v2*
