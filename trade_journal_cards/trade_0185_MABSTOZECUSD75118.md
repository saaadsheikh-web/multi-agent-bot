# Trade #185 — ZEC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.4653 (-0.838% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.02 min

> Long stopped out at full risk on ZEC-USDT (stoch_rsi, -0.84%) during good-zone hour 18:00 UTC trail gave back 1.10% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD75118`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-22T18:38:40.210087+00:00`
- closed: `2026-05-22T18:44:41.251981+00:00` · hour UTC 18 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=28

### Parsed signal features
- **rsi**: 28.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 612.0873,
  "atr_tp": 627.54405,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 616.75
- exit_price: 611.58
- tp_price: 627.54
- sl_price: 612.09
- qty: 0.9 · notional: 55.50750000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.7495
- **planned_sl_distance_pct**: 0.7556
- **planned_r_multiple**: 2.315
- **planned_risk_usd**: 4.194
- **planned_reward_usd**: 9.711
- **realized_r_multiple**: -0.111
- **exit_distance_from_tp_pct**: 2.5878
- **exit_distance_from_sl_pct**: -0.0827
- **notional**: 55.50750000000001

### Market excursion (MFE / MAE proxy)
- high_water: 618.35 · low_water: 616.75
- current_stop_at_close: 612.09
- **mfe_pct**: 0.2594
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0977

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.111
- slippage vs planned TP: 2.5878%
- slippage vs planned SL: -0.0827%

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
  - strong planned R:R=2.315
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570654Z · journaler v2*
