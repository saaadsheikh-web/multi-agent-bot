# Trade #71 — BTCDOM-USDT long (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.0790 (+0.144% if pct available) · **Decision grade:** A (100/100) · **Hold:** 7.83 min

> Long trailed into profit on BTCDOM-USDT (zscore_reversion, +0.14%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCBTCDOM72790`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-08T20:39:52.021619+00:00`
- closed: `2026-05-08T20:47:41.970266+00:00` · hour UTC 20 (Fri)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [bb_bounce,zscore_reversion,stoch_rsi,wide_scalp] — best: z-score long z=-3.28 mean=5543.7480

### Parsed signal features
- **z_score**: -3.28
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 5449.0999543855305,
  "atr_tp": 5543.748,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5471.2
- exit_price: 5479.1
- tp_price: 5543.7
- sl_price: 5449.1
- qty: 10.0 · notional: 54.711999999999996
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 1.3251
- **planned_sl_distance_pct**: 0.4039
- **planned_r_multiple**: 3.281
- **planned_risk_usd**: 221.0
- **planned_reward_usd**: 725.0
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.1807
- **exit_distance_from_sl_pct**: 0.5483
- **notional**: 54.711999999999996

### Market excursion (MFE / MAE proxy)
- high_water: 5479.1 · low_water: 5471.2
- current_stop_at_close: 5449.1
- **mfe_pct**: 0.1444
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.1807%
- slippage vs planned SL: 0.5483%

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
  - strong planned R:R=3.281
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560299Z · journaler v2*
