# Trade #291 — XAUT-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.4232 (-0.409% if pct available) · **Decision grade:** A (95/100) · **Hold:** 240.08 min

> Long gave back gains on trail on XAUT-USDT (stoch_rsi, -0.41%) during dead-zone hour 08:00 UTC trail gave back 0.61% [grade A / 95].

## 1 · Identity
- custom_id: `MABSTOXAUTUS88644`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAUT-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T04:37:26.219666+00:00`
- closed: `2026-06-01T08:37:31.048340+00:00` · hour UTC 08 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.00 rsi=27

### Parsed signal features
- **rsi**: 27.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4452.4259999999995,
  "atr_tp": 4564.860999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 4497.4
- exit_price: 4479.0
- tp_price: 4564.9
- sl_price: 4452.4
- qty: 23.0 · notional: 103.44019999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5009
- **planned_sl_distance_pct**: 1.0006
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1035.0
- **planned_reward_usd**: 1552.5
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.91
- **exit_distance_from_sl_pct**: 0.5915
- **notional**: 103.44019999999999

### Market excursion (MFE / MAE proxy)
- high_water: 4506.3 · low_water: 4497.4
- current_stop_at_close: 4452.4
- **mfe_pct**: 0.1979
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.607

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.91%
- slippage vs planned SL: 0.5915%

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
`dead_hour`, `confluence`, `trail_too_loose`, `long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617712+00:00Z · journaler v2*
