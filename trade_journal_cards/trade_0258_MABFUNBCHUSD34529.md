# Trade #258 — BCH-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +0.2310 (+0.230% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.72 min

> Long trailed into profit on BCH-USDT (funding_extremes, +0.23%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD34529`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-29T06:02:10.924678+00:00`
- closed: `2026-05-29T06:04:54.315860+00:00` · hour UTC 06 (Fri)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0626%/8h (annual≈-69%), RSI=42, EMA50 slope=-0.75%

### Parsed signal features
- **rsi**: 42.21415619228113
- **ema_slope**: -0.753098123960172
- **atr_pct**: 1.2772390024811866
- **funding_rate**: -0.0006261849731951868
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0006261849731951868,
  "rsi": 42.21415619228113,
  "ema_slope": -0.753098123960172,
  "atr_pct": 1.2772390024811866,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 304.6
- exit_price: 305.3
- tp_price: 312.21
- sl_price: 300.03
- qty: 3.3 · notional: 100.51800000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4984
- **planned_sl_distance_pct**: 1.5003
- **planned_r_multiple**: 1.665
- **planned_risk_usd**: 15.081
- **planned_reward_usd**: 25.113
- **realized_r_multiple**: 0.015
- **exit_distance_from_tp_pct**: 2.2685
- **exit_distance_from_sl_pct**: 1.7301
- **notional**: 100.51800000000001

### Market excursion (MFE / MAE proxy)
- high_water: 305.3 · low_water: 304.6
- current_stop_at_close: 300.03
- **mfe_pct**: 0.2298
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.015
- slippage vs planned TP: 2.2685%
- slippage vs planned SL: 1.7301%

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
`very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.616817+00:00Z · journaler v2*
