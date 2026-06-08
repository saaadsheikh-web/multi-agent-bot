# Trade #183 — ZEC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.5232 (-1.036% if pct available) · **Decision grade:** A (100/100) · **Hold:** 49.58 min

> Long stopped out at full risk on ZEC-USDT (stoch_rsi, -1.04%) trail gave back 1.25% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD64804`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-22T15:46:45.994692+00:00`
- closed: `2026-05-22T16:36:20.835217+00:00` · hour UTC 16 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 624.7791,
  "atr_tp": 640.55635,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 630.97
- exit_price: 624.43
- tp_price: 640.56
- sl_price: 624.78
- qty: 0.8 · notional: 50.47760000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5199
- **planned_sl_distance_pct**: 0.981
- **planned_r_multiple**: 1.549
- **planned_risk_usd**: 4.952
- **planned_reward_usd**: 7.672
- **realized_r_multiple**: -0.106
- **exit_distance_from_tp_pct**: 2.5564
- **exit_distance_from_sl_pct**: -0.0555
- **notional**: 50.47760000000001

### Market excursion (MFE / MAE proxy)
- high_water: 632.3 · low_water: 630.97
- current_stop_at_close: 624.78
- **mfe_pct**: 0.2108
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.2473

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.106
- slippage vs planned TP: 2.5564%
- slippage vs planned SL: -0.0555%

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
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570625Z · journaler v2*
