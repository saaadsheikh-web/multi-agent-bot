# Trade #257 — BTC-USDT long (zscore_reversion)

**Outcome:** LOSS · **PnL:** -0.1239 (-0.119% if pct available) · **Decision grade:** A (100/100) · **Hold:** 180.02 min

> Long gave back gains on trail on BTC-USDT (zscore_reversion, -0.12%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCBTCUSD18076`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-27T21:41:17.875505+00:00`
- closed: `2026-05-28T00:41:18.800379+00:00` · hour UTC 00 (Thu)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,zscore_reversion] — best: z-score long z=-2.65 mean=76557.8890

### Parsed signal features
- **z_score**: -2.65
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 73853.06519747972,
  "atr_tp": 76557.889,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 74594.9
- exit_price: 74506.4
- tp_price: 76557.9
- sl_price: 73853.1
- qty: 1.4 · notional: 104.43285999999999
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 2.6315
- **planned_sl_distance_pct**: 0.9944
- **planned_r_multiple**: 2.646
- **planned_risk_usd**: 1038.52
- **planned_reward_usd**: 2748.2
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.7502
- **exit_distance_from_sl_pct**: 0.8758
- **notional**: 104.43285999999999

### Market excursion (MFE / MAE proxy)
- high_water: 74757.9 · low_water: 74594.9
- current_stop_at_close: 73853.1
- **mfe_pct**: 0.2185
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3372

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.7502%
- slippage vs planned SL: 0.8758%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - strong planned R:R=2.646
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `confluence`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-28T03:00:42.632393Z · journaler v2*
