# Trade #243 — HYPE-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.1577 (-1.136% if pct available) · **Decision grade:** A (100/100) · **Hold:** 12.16 min

> Long stopped out at full risk on HYPE-USDT (stoch_rsi, -1.14%) during good-zone hour 01:00 UTC trail gave back 1.20% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS58573`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-26T01:22:54.526199+00:00`
- closed: `2026-05-26T01:35:04.190673+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=34

### Parsed signal features
- **rsi**: 34.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 59.368320000000004,
  "atr_tp": 60.86752,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 59.968
- exit_price: 59.287
- tp_price: 60.868
- sl_price: 59.368
- qty: 17.0 · notional: 101.94560000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5008
- **planned_sl_distance_pct**: 1.0005
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 10.2
- **planned_reward_usd**: 15.3
- **realized_r_multiple**: -0.114
- **exit_distance_from_tp_pct**: 2.6364
- **exit_distance_from_sl_pct**: -0.1351
- **notional**: 101.94560000000001

### Market excursion (MFE / MAE proxy)
- high_water: 60.008 · low_water: 59.968
- current_stop_at_close: 59.368
- **mfe_pct**: 0.0667
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.2023

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.114
- slippage vs planned TP: 2.6364%
- slippage vs planned SL: -0.1351%

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
`good_hour`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-26T03:01:12.558778Z · journaler v2*
