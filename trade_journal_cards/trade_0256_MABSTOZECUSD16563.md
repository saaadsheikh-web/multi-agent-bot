# Trade #256 — ZEC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.0773 (-1.028% if pct available) · **Decision grade:** A (100/100) · **Hold:** 24.75 min

> Long stopped out at full risk on ZEC-USDT (stoch_rsi, -1.03%) trail gave back 1.22% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD16563`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-27T21:16:05.948093+00:00`
- closed: `2026-05-27T21:40:50.770839+00:00` · hour UTC 21 (Wed)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.15 rsi=32

### Parsed signal features
- **rsi**: 32.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 546.3909,
  "atr_tp": 560.1886499999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 551.71
- exit_price: 546.04
- tp_price: 560.19
- sl_price: 546.39
- qty: 1.9 · notional: 104.82490000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.537
- **planned_sl_distance_pct**: 0.9643
- **planned_r_multiple**: 1.594
- **planned_risk_usd**: 10.108
- **planned_reward_usd**: 16.112
- **realized_r_multiple**: -0.107
- **exit_distance_from_tp_pct**: 2.5648
- **exit_distance_from_sl_pct**: -0.0634
- **notional**: 104.82490000000001

### Market excursion (MFE / MAE proxy)
- high_water: 552.76 · low_water: 551.71
- current_stop_at_close: 546.39
- **mfe_pct**: 0.1903
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.218

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.107
- slippage vs planned TP: 2.5648%
- slippage vs planned SL: -0.0634%

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
*journaled_at 2026-05-27T23:00:45.862793Z · journaler v2*
