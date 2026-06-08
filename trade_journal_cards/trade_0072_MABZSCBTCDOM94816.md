# Trade #72 — BTCDOM-USDT long (zscore_reversion)

**Outcome:** LOSS · **PnL:** -0.0010 (-0.002% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.79 min

> Long closed in the red without clean exit on BTCDOM-USDT (zscore_reversion, -0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCBTCDOM94816`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T02:46:58.009059+00:00`
- closed: `2026-05-09T02:51:45.260465+00:00` · hour UTC 02 (Sat)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [zscore_reversion,stoch_rsi,wide_scalp] — best: z-score long z=-3.04 mean=5538.9940

### Parsed signal features
- **z_score**: -3.04
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 5419.970804642431,
  "atr_tp": 5538.993999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5449.4
- exit_price: 5449.3
- tp_price: 5539.0
- sl_price: 5420.0
- qty: 10.0 · notional: 54.494
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 1.6442
- **planned_sl_distance_pct**: 0.5395
- **planned_r_multiple**: 3.048
- **planned_risk_usd**: 294.0
- **planned_reward_usd**: 896.0
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.6461
- **exit_distance_from_sl_pct**: 0.5377
- **notional**: 54.494

### Market excursion (MFE / MAE proxy)
- high_water: 5449.4 · low_water: 5449.4
- current_stop_at_close: 5420.0
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.6461%
- slippage vs planned SL: 0.5377%

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
  - strong planned R:R=3.048
  - multi-agent confluence
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`confluence`, `very_short_hold`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560352Z · journaler v2*
