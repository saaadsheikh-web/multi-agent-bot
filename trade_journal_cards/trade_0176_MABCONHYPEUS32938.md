# Trade #176 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2952 (+0.572% if pct available) · **Decision grade:** B (85/100) · **Hold:** 74.11 min

> Long trailed into profit on HYPE-USDT (connors_rsi2, +0.57%) during dead-zone hour 08:00 UTC trail gave back 0.61% [grade B / 85].

## 1 · Identity
- custom_id: `MABCONHYPEUS32938`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T06:55:40.004827+00:00`
- closed: `2026-05-22T08:09:46.881626+00:00` · hour UTC 08 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.7, ATR%=0.40, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.7
- **atr_pct**: 0.4
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 56.512404999999994,
  "atr_tp": 58.52046,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 57.338
- exit_price: 57.666
- tp_price: 58.52
- sl_price: 56.512
- qty: 9.0 · notional: 51.6042
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0615
- **planned_sl_distance_pct**: 1.4406
- **planned_r_multiple**: 1.431
- **planned_risk_usd**: 7.434
- **planned_reward_usd**: 10.638
- **realized_r_multiple**: 0.04
- **exit_distance_from_tp_pct**: 1.4894
- **exit_distance_from_sl_pct**: 2.0126
- **notional**: 51.6042

### Market excursion (MFE / MAE proxy)
- high_water: 58.017 · low_water: 57.338
- current_stop_at_close: 57.668898000000006
- **mfe_pct**: 1.1842
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6122

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.04
- slippage vs planned TP: 1.4894%
- slippage vs planned SL: 2.0126%

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
`dead_hour`, `trail_too_loose`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-23T15:00:56.570526Z · journaler v2*
