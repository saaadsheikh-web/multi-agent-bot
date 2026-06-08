# Trade #254 — ZEC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0594 (-0.059% if pct available) · **Decision grade:** A (100/100) · **Hold:** 11.06 min

> Long gave back gains on trail on ZEC-USDT (stoch_rsi, -0.06%) (was up 0.52% before reversing) trail gave back 0.57% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD286`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-27T16:44:47.898808+00:00`
- closed: `2026-05-27T16:55:51.477228+00:00` · hour UTC 16 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [swing,stoch_rsi] — best: StochRSI long stoch=0.14 rsi=33

### Parsed signal features
- **rsi**: 33.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 551.628,
  "atr_tp": 565.558,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 557.12
- exit_price: 556.79
- tp_price: 565.56
- sl_price: 551.63
- qty: 1.8 · notional: 100.28160000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5149
- **planned_sl_distance_pct**: 0.9854
- **planned_r_multiple**: 1.537
- **planned_risk_usd**: 9.882
- **planned_reward_usd**: 15.192
- **realized_r_multiple**: -0.006
- **exit_distance_from_tp_pct**: 1.5742
- **exit_distance_from_sl_pct**: 0.9262
- **notional**: 100.28160000000001

### Market excursion (MFE / MAE proxy)
- high_water: 559.99 · low_water: 557.12
- current_stop_at_close: 557.19005
- **mfe_pct**: 0.5151
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5744

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.006
- slippage vs planned TP: 1.5742%
- slippage vs planned SL: 0.9262%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence
  - high confidence (8) lost

## 7 · Tags
`confluence`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-27T19:00:51.546095Z · journaler v2*
