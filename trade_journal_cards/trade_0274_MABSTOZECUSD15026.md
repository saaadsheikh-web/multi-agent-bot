# Trade #274 — ZEC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0720 (-0.071% if pct available) · **Decision grade:** A (100/100) · **Hold:** 40.15 min

> Long gave back gains on trail on ZEC-USDT (stoch_rsi, -0.07%) during good-zone hour 05:00 UTC (was up 0.57% before reversing) trail gave back 0.64% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD15026`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-30T04:23:47.931502+00:00`
- closed: `2026-05-30T05:03:56.904818+00:00` · hour UTC 05 (Sat)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 501.4251,
  "atr_tp": 514.08735,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 506.33
- exit_price: 505.97
- tp_price: 514.09
- sl_price: 501.43
- qty: 2.0 · notional: 101.266
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5326
- **planned_sl_distance_pct**: 0.9677
- **planned_r_multiple**: 1.584
- **planned_risk_usd**: 9.8
- **planned_reward_usd**: 15.52
- **realized_r_multiple**: -0.007
- **exit_distance_from_tp_pct**: 1.6037
- **exit_distance_from_sl_pct**: 0.8966
- **notional**: 101.266

### Market excursion (MFE / MAE proxy)
- high_water: 509.21 · low_water: 506.33
- current_stop_at_close: 506.66395
- **mfe_pct**: 0.5688
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6399

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.007
- slippage vs planned TP: 1.6037%
- slippage vs planned SL: 0.8966%

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
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617314+00:00Z · journaler v2*
