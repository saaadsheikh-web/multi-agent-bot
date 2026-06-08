# Trade #104 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2730 (+0.487% if pct available) · **Decision grade:** A (100/100) · **Hold:** 69.44 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.49%) trail gave back 0.62% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD32858`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T20:54:20.227507+00:00`
- closed: `2026-05-11T22:03:46.532068+00:00` · hour UTC 22 (Mon)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 short: RSI2=97.0, ATR%=0.38, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.0
- **atr_pct**: 0.38
- **trend_score**: -3
- **trend_dir**: DOWN
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 568.55225,
  "atr_tp": 548.947,
  "_trend_score": -3,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 560.09
- exit_price: 557.36
- tp_price: 548.95
- sl_price: 568.55
- qty: 1.0 · notional: 56.00900000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.989
- **planned_sl_distance_pct**: 1.5105
- **planned_r_multiple**: 1.317
- **planned_risk_usd**: 8.46
- **planned_reward_usd**: 11.14
- **realized_r_multiple**: 0.032
- **exit_distance_from_tp_pct**: 1.5015
- **exit_distance_from_sl_pct**: 1.9979
- **notional**: 56.00900000000001

### Market excursion (MFE / MAE proxy)
- high_water: 560.09 · low_water: 553.88
- current_stop_at_close: 557.20328
- **mfe_pct**: 1.1088
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6213

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.032
- slippage vs planned TP: 1.5015%
- slippage vs planned SL: 1.9979%

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
  - (no notable factors)

## 7 · Tags
`trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562306Z · journaler v2*
