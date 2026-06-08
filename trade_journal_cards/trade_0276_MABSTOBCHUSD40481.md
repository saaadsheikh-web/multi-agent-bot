# Trade #276 — BCH-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.1360 (+0.134% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.71 min

> Long trailed into profit on BCH-USDT (stoch_rsi, +0.13%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBCHUSD40481`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-31T15:14:43.164052+00:00`
- closed: `2026-05-31T15:19:25.719782+00:00` · hour UTC 15 (Sun)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.05 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 296.307,
  "atr_tp": 303.7895,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 299.3
- exit_price: 299.7
- tp_price: 303.79
- sl_price: 296.31
- qty: 3.4 · notional: 101.76200000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5002
- **planned_sl_distance_pct**: 0.999
- **planned_r_multiple**: 1.502
- **planned_risk_usd**: 10.166
- **planned_reward_usd**: 15.266
- **realized_r_multiple**: 0.013
- **exit_distance_from_tp_pct**: 1.3665
- **exit_distance_from_sl_pct**: 1.1326
- **notional**: 101.76200000000001

### Market excursion (MFE / MAE proxy)
- high_water: 299.7 · low_water: 299.3
- current_stop_at_close: 296.31
- **mfe_pct**: 0.1336
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.013
- slippage vs planned TP: 1.3665%
- slippage vs planned SL: 1.1326%

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
*journaled_at 2026-06-05T21:57:18.617369+00:00Z · journaler v2*
