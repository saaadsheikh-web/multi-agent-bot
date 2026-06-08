# Trade #194 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2475 (+0.467% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.86 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.47%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD45746`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T14:15:47.506711+00:00`
- closed: `2026-05-23T14:19:38.823127+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 short: RSI2=97.7, ATR%=0.45, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.7
- **atr_pct**: 0.45
- **trend_score**: -3
- **trend_dir**: DOWN
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 597.1244999999999,
  "atr_tp": 576.534,
  "_trend_score": -3,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 588.3
- exit_price: 585.55
- tp_price: 576.53
- sl_price: 597.12
- qty: 0.9 · notional: 52.947
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0007
- **planned_sl_distance_pct**: 1.4992
- **planned_r_multiple**: 1.335
- **planned_risk_usd**: 7.938
- **planned_reward_usd**: 10.593
- **realized_r_multiple**: 0.031
- **exit_distance_from_tp_pct**: 1.5332
- **exit_distance_from_sl_pct**: 1.9667
- **notional**: 52.947

### Market excursion (MFE / MAE proxy)
- high_water: 588.3 · low_water: 585.61
- current_stop_at_close: 597.12
- **mfe_pct**: 0.4572
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.0102

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.031
- slippage vs planned TP: 1.5332%
- slippage vs planned SL: 1.9667%

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
`very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570808Z · journaler v2*
