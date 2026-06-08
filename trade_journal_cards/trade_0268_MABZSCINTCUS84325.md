# Trade #268 — INTC-USDT long (zscore_reversion)

**Outcome:** LOSS · **PnL:** -1.9314 (-1.910% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.09 min

> Long stopped out at full risk on INTC-USDT (zscore_reversion, -1.91%) during good-zone hour 19:00 UTC trail gave back 2.07% [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCINTCUS84325`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `INTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-29T19:52:06.845403+00:00`
- closed: `2026-05-29T19:54:12.193704+00:00` · hour UTC 19 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [zscore_reversion,stoch_rsi] — best: z-score long z=-2.69 mean=121.1909

### Parsed signal features
- **z_score**: -2.69
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 114.14036674153957,
  "atr_tp": 121.19089999999998,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 116.22
- exit_price: 114.0
- tp_price: 121.19
- sl_price: 114.14
- qty: 87.0 · notional: 101.1114
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 4.2764
- **planned_sl_distance_pct**: 1.7897
- **planned_r_multiple**: 2.389
- **planned_risk_usd**: 180.96
- **planned_reward_usd**: 432.39
- **realized_r_multiple**: -0.011
- **exit_distance_from_tp_pct**: 6.1865
- **exit_distance_from_sl_pct**: -0.1205
- **notional**: 101.1114

### Market excursion (MFE / MAE proxy)
- high_water: 116.41 · low_water: 116.22
- current_stop_at_close: 114.14
- **mfe_pct**: 0.1635
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 2.0737

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.011
- slippage vs planned TP: 6.1865%
- slippage vs planned SL: -0.1205%

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
  - strong planned R:R=2.389
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `confluence`, `trail_too_loose`, `very_short_hold`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617220+00:00Z · journaler v2*
