# Trade #187 — BTC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.3664 (-0.687% if pct available) · **Decision grade:** A (100/100) · **Hold:** 248.73 min

> Long gave back gains on trail on BTC-USDT (stoch_rsi, -0.69%) trail gave back 1.10% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBTCUSD75745`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-22T18:49:06.996620+00:00`
- closed: `2026-05-22T22:57:50.655384+00:00` · hour UTC 22 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.00 rsi=29

### Parsed signal features
- **rsi**: 29.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 75481.164,
  "atr_tp": 77387.254,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 76235.5
- exit_price: 75712.1
- tp_price: 77387.3
- sl_price: 75481.2
- qty: 0.7 · notional: 53.36485
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5108
- **planned_sl_distance_pct**: 0.9894
- **planned_r_multiple**: 1.527
- **planned_risk_usd**: 528.01
- **planned_reward_usd**: 806.26
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.1974
- **exit_distance_from_sl_pct**: 0.3029
- **notional**: 53.36485

### Market excursion (MFE / MAE proxy)
- high_water: 76551.5 · low_water: 76235.5
- current_stop_at_close: 75481.2
- **mfe_pct**: 0.4145
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.1011

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.1974%
- slippage vs planned SL: 0.3029%

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
  - high confidence (9) lost

## 7 · Tags
`confluence`, `trail_too_loose`, `long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570730Z · journaler v2*
