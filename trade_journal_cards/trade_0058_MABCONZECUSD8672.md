# Trade #58 — ZEC-USDT long (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 45.16 min

> Long flat exit (scratch) on ZEC-USDT (connors_rsi2, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD8672`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-06T23:04:34.091719+00:00`
- closed: `2026-05-06T23:49:43.913564+00:00` · hour UTC 23 (Wed)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.8, in uptrend

### Parsed signal features
- **rsi2**: 3.8
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 543.2669,
  "atr_tp": 562.5708,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 551.73
- exit_price: 551.73
- tp_price: 562.57
- sl_price: 543.27
- qty: 1.0 · notional: 55.173
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9647
- **planned_sl_distance_pct**: 1.5334
- **planned_r_multiple**: 1.281
- **planned_risk_usd**: 8.46
- **planned_reward_usd**: 10.84
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9647
- **exit_distance_from_sl_pct**: 1.5334
- **notional**: 55.173

### Market excursion (MFE / MAE proxy)
- high_water: 554.22 · low_water: 551.73
- current_stop_at_close: 543.27
- **mfe_pct**: 0.4513
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4513

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9647%
- slippage vs planned SL: 1.5334%

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
`trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559873Z · journaler v2*
