# Trade #323 — BTC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.0853 (-1.029% if pct available) · **Decision grade:** A (95/100) · **Hold:** 180.28 min

> Long stopped out at full risk on BTC-USDT (stoch_rsi, -1.03%) during dead-zone hour 09:00 UTC trail gave back 1.13% [grade A / 95].

## 1 · Identity
- custom_id: `MABSTOBTCUSD80138`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T06:02:19.296532+00:00`
- closed: `2026-06-02T09:02:36.060346+00:00` · hour UTC 09 (Tue)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [swing,zscore_reversion,stoch_rsi] — best: StochRSI long stoch=0.36 (was 0.13) rsi=29

### Parsed signal features
- **rsi**: 29.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 69626.799,
  "atr_tp": 71385.0515,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 70330.1
- exit_price: 69606.6
- tp_price: 71385.1
- sl_price: 69626.8
- qty: 1.5 · notional: 105.49515000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5001
- **planned_sl_distance_pct**: 1.0
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1054.95
- **planned_reward_usd**: 1582.5
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.5288
- **exit_distance_from_sl_pct**: -0.0287
- **notional**: 105.49515000000001

### Market excursion (MFE / MAE proxy)
- high_water: 70404.0 · low_water: 70330.1
- current_stop_at_close: 69626.8
- **mfe_pct**: 0.1051
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.1338

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.5288%
- slippage vs planned SL: -0.0287%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - dead-zone-hour
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618398+00:00Z · journaler v2*
