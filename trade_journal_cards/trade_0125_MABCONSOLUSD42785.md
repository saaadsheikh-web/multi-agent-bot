# Trade #125 — SOL-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.1044 (-0.208% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.05 min

> Short gave back gains on trail on SOL-USDT (connors_rsi2, -0.21%) trail gave back 0.53% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONSOLUSD42785`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T14:46:27.524518+00:00`
- closed: `2026-05-16T20:46:30.502069+00:00` · hour UTC 20 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 short: RSI2=95.4, ATR%=0.14, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.4
- **atr_pct**: 0.14
- **trend_score**: -3
- **trend_dir**: DOWN
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 87.78734999999999,
  "atr_tp": 84.7602,
  "_trend_score": -3,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 86.5
- exit_price: 86.68
- tp_price: 84.76
- sl_price: 87.79
- qty: 0.58 · notional: 50.169999999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0116
- **planned_sl_distance_pct**: 1.4913
- **planned_r_multiple**: 1.349
- **planned_risk_usd**: 0.7482
- **planned_reward_usd**: 1.0092
- **realized_r_multiple**: -0.14
- **exit_distance_from_tp_pct**: 2.2197
- **exit_distance_from_sl_pct**: 1.2832
- **notional**: 50.169999999999995

### Market excursion (MFE / MAE proxy)
- high_water: 86.5 · low_water: 86.22
- current_stop_at_close: 87.79
- **mfe_pct**: 0.3237
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5318

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.14
- slippage vs planned TP: 2.2197%
- slippage vs planned SL: 1.2832%

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
*journaled_at 2026-05-17T03:54:39.562980Z · journaler v2*
