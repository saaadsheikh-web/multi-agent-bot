# Trade #87 — GIGGLE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2540 (+0.508% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.17 min

> Long trailed into profit on GIGGLE-USDT (connors_rsi2, +0.51%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONGIGGLE57967`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `GIGGLE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T00:06:09.525550+00:00`
- closed: `2026-05-11T00:11:19.655367+00:00` · hour UTC 00 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.9, ATR%=0.68, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.9
- **atr_pct**: 0.68
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 38.759750000000004,
  "atr_tp": 40.137,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 39.4
- exit_price: 39.6
- tp_price: 40.14
- sl_price: 38.76
- qty: 127.0 · notional: 50.038
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.8782
- **planned_sl_distance_pct**: 1.6244
- **planned_r_multiple**: 1.156
- **planned_risk_usd**: 81.28
- **planned_reward_usd**: 93.98
- **realized_r_multiple**: 0.003
- **exit_distance_from_tp_pct**: 1.3706
- **exit_distance_from_sl_pct**: 2.132
- **notional**: 50.038

### Market excursion (MFE / MAE proxy)
- high_water: 39.6 · low_water: 39.4
- current_stop_at_close: 39.4
- **mfe_pct**: 0.5076
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.003
- slippage vs planned TP: 1.3706%
- slippage vs planned SL: 2.132%

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
*journaled_at 2026-05-17T03:54:39.561731Z · journaler v2*
