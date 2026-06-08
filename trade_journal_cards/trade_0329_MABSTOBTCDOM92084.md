# Trade #329 — BTCDOM-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.0184 (-1.004% if pct available) · **Decision grade:** A (100/100) · **Hold:** 245.56 min

> Long stopped out at full risk on BTCDOM-USDT (stoch_rsi, -1.00%) trail gave back 1.05% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBTCDOM92084`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T09:21:26.215348+00:00`
- closed: `2026-06-02T13:26:59.570698+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.29 (was 0.05) rsi=28

### Parsed signal features
- **rsi**: 28.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 5286.402,
  "atr_tp": 5419.897,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5339.8
- exit_price: 5286.2
- tp_price: 5419.9
- sl_price: 5286.4
- qty: 19.0 · notional: 101.4562
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5001
- **planned_sl_distance_pct**: 1.0
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1014.6
- **planned_reward_usd**: 1521.9
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.5038
- **exit_distance_from_sl_pct**: -0.0037
- **notional**: 101.4562

### Market excursion (MFE / MAE proxy)
- high_water: 5342.1 · low_water: 5339.8
- current_stop_at_close: 5286.4
- **mfe_pct**: 0.0431
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0469

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.5038%
- slippage vs planned SL: -0.0037%

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
`trail_too_loose`, `long_hold`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618509+00:00Z · journaler v2*
