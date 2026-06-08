# Trade #285 — SOXL-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.0704 (-0.070% if pct available) · **Decision grade:** A (100/100) · **Hold:** 21.02 min

> Long gave back gains on trail on SOXL-USDT (funding_extremes, -0.07%) during good-zone hour 00:00 UTC (was up 0.91% before reversing) trail gave back 0.98% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNSOXLUS70741`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `SOXL-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-31T23:39:03.395040+00:00`
- closed: `2026-06-01T00:00:04.776139+00:00` · hour UTC 00 (Mon)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0537%/8h (annual≈-59%), RSI=44, EMA50 slope=+0.21%

### Parsed signal features
- **rsi**: 44.36628562119468
- **atr_pct**: 1.0847242797683379
- **funding_rate**: -0.0005365753402004625
- **ema_slope**: 0.20894840293186334
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005365753402004625,
  "rsi": 44.36628562119468,
  "ema_slope": 0.20894840293186334,
  "atr_pct": 1.0847242797683379,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 227.94
- exit_price: 227.78
- tp_price: 233.64
- sl_price: 224.52
- qty: 44.0 · notional: 100.2936
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5007
- **planned_sl_distance_pct**: 1.5004
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 150.48
- **planned_reward_usd**: 250.8
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.5709
- **exit_distance_from_sl_pct**: 1.4302
- **notional**: 100.2936

### Market excursion (MFE / MAE proxy)
- high_water: 230.01 · low_water: 227.94
- current_stop_at_close: 227.94
- **mfe_pct**: 0.9081
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.9783

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.5709%
- slippage vs planned SL: 1.4302%

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
*journaled_at 2026-06-05T21:57:18.617545+00:00Z · journaler v2*
