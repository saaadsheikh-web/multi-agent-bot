# Trade #65 — SOL-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2337 (+0.465% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.58 min

> Long trailed into profit on SOL-USDT (connors_rsi2, +0.46%) during good-zone hour 18:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONSOLUSD79925`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `long`
- confidence: 5
- opened: `2026-05-07T18:52:07.170199+00:00`
- closed: `2026-05-07T18:57:41.964041+00:00` · hour UTC 18 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.6, in uptrend

### Parsed signal features
- **rsi2**: 2.6
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 86.93610000000001,
  "atr_tp": 90.02520000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 88.26
- exit_price: 88.67
- tp_price: 90.03
- sl_price: 86.94
- qty: 0.57 · notional: 50.3082
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 2.0054
- **planned_sl_distance_pct**: 1.4956
- **planned_r_multiple**: 1.341
- **planned_risk_usd**: 0.7524
- **planned_reward_usd**: 1.0089
- **realized_r_multiple**: 0.311
- **exit_distance_from_tp_pct**: 1.5409
- **exit_distance_from_sl_pct**: 1.9601
- **notional**: 50.3082

### Market excursion (MFE / MAE proxy)
- high_water: 88.67 · low_water: 88.26
- current_stop_at_close: 86.94
- **mfe_pct**: 0.4645
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.311
- slippage vs planned TP: 1.5409%
- slippage vs planned SL: 1.9601%

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
`good_hour`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560083Z · journaler v2*
