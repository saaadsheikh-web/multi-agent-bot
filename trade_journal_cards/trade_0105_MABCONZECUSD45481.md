# Trade #105 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.9000 (+1.603% if pct available) · **Decision grade:** A (100/100) · **Hold:** 51.38 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +1.60%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD45481`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-12T00:24:42.687411+00:00`
- closed: `2026-05-12T01:16:05.508669+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.7, ATR%=0.35, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.7
- **atr_pct**: 0.35
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 569.9224999999999,
  "atr_tp": 550.27,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 561.5
- exit_price: 552.5
- tp_price: 550.27
- sl_price: 569.92
- qty: 1.0 · notional: 56.150000000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.4996
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 8.42
- **planned_reward_usd**: 11.23
- **realized_r_multiple**: 0.107
- **exit_distance_from_tp_pct**: 0.3972
- **exit_distance_from_sl_pct**: 3.1024
- **notional**: 56.150000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 561.5 · low_water: 550.75
- current_stop_at_close: 554.0545
- **mfe_pct**: 1.9145
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3117

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.107
- slippage vs planned TP: 0.3972%
- slippage vs planned SL: 3.1024%

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
  - (no notable factors)

## 7 · Tags
`good_hour`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562337Z · journaler v2*
