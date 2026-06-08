# Trade #123 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1640 (+0.326% if pct available) · **Decision grade:** A (100/100) · **Hold:** 107.08 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.33%) trail gave back 0.61% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD41354`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T14:22:36.559964+00:00`
- closed: `2026-05-16T16:09:41.332168+00:00` · hour UTC 16 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 short: RSI2=97.1, ATR%=0.36, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.1
- **atr_pct**: 0.36
- **trend_score**: -3
- **trend_dir**: DOWN
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 511.06264999999996,
  "atr_tp": 493.4398,
  "_trend_score": -3,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 503.16
- exit_price: 501.52
- tp_price: 493.44
- sl_price: 511.06
- qty: 1.0 · notional: 50.316
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9318
- **planned_sl_distance_pct**: 1.5701
- **planned_r_multiple**: 1.23
- **planned_risk_usd**: 7.9
- **planned_reward_usd**: 9.72
- **realized_r_multiple**: 0.021
- **exit_distance_from_tp_pct**: 1.6059
- **exit_distance_from_sl_pct**: 1.896
- **notional**: 50.316

### Market excursion (MFE / MAE proxy)
- high_water: 503.16 · low_water: 498.43
- current_stop_at_close: 501.42058000000003
- **mfe_pct**: 0.9401
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6141

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.021
- slippage vs planned TP: 1.6059%
- slippage vs planned SL: 1.896%

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
*journaled_at 2026-05-17T03:54:39.562920Z · journaler v2*
