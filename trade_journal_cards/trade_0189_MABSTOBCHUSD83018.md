# Trade #189 — BCH-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.6860 (-1.314% if pct available) · **Decision grade:** A (100/100) · **Hold:** 157.55 min

> Long stopped out at full risk on BCH-USDT (stoch_rsi, -1.31%) trail gave back 1.80% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBCHUSD83018`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BCH-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T20:50:20.243293+00:00`
- closed: `2026-05-22T23:27:52.993044+00:00` · hour UTC 23 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.06 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 369.27,
  "atr_tp": 378.59499999999997,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 373.0
- exit_price: 368.1
- tp_price: 378.59
- sl_price: 369.27
- qty: 1.4 · notional: 52.21999999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4987
- **planned_sl_distance_pct**: 1.0
- **planned_r_multiple**: 1.499
- **planned_risk_usd**: 5.222
- **planned_reward_usd**: 7.826
- **realized_r_multiple**: -0.131
- **exit_distance_from_tp_pct**: 2.8123
- **exit_distance_from_sl_pct**: -0.3137
- **notional**: 52.21999999999999

### Market excursion (MFE / MAE proxy)
- high_water: 374.8 · low_water: 373.0
- current_stop_at_close: 369.27
- **mfe_pct**: 0.4826
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.7962

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.131
- slippage vs planned TP: 2.8123%
- slippage vs planned SL: -0.3137%

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
  - high confidence (8) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570761Z · journaler v2*
