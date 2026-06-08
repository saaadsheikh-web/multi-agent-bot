# Trade #309 — BCH-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +0.7000 (+0.697% if pct available) · **Decision grade:** A (100/100) · **Hold:** 112.36 min

> Long trailed into profit on BCH-USDT (funding_extremes, +0.70%) during good-zone hour 18:00 UTC trail gave back 1.07% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD30829`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T16:20:30.796975+00:00`
- closed: `2026-06-01T18:12:52.471139+00:00` · hour UTC 18 (Mon)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0508%/8h (annual≈-56%), RSI=39, EMA50 slope=-0.68%

### Parsed signal features
- **rsi**: 39.37212400576881
- **ema_slope**: -0.6789111370032685
- **atr_pct**: 1.2471188820000094
- **funding_rate**: -0.0005079014957080154
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005079014957080154,
  "rsi": 39.37212400576881,
  "ema_slope": -0.6789111370032685,
  "atr_pct": 1.2471188820000094,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 286.9
- exit_price: 288.9
- tp_price: 298.38
- sl_price: 278.29
- qty: 3.5 · notional: 100.415
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 4.0014
- **planned_sl_distance_pct**: 3.001
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 30.135
- **planned_reward_usd**: 40.18
- **realized_r_multiple**: 0.023
- **exit_distance_from_tp_pct**: 3.3043
- **exit_distance_from_sl_pct**: 3.6982
- **notional**: 100.415

### Market excursion (MFE / MAE proxy)
- high_water: 291.96 · low_water: 286.9
- current_stop_at_close: 289.1952
- **mfe_pct**: 1.7637
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0666

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.023
- slippage vs planned TP: 3.3043%
- slippage vs planned SL: 3.6982%

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
`good_hour`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618020+00:00Z · journaler v2*
