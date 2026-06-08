# Trade #318 — XAG-USDT long (macd_cross)

**Outcome:** LOSS · **PnL:** -0.0532 (-0.053% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.98 min

> Long closed in the red without clean exit on XAG-USDT (macd_cross, -0.05%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACXAGUSD68080`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `XAG-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T02:41:21.659704+00:00`
- closed: `2026-06-02T02:47:20.413546+00:00` · hour UTC 02 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [macd_cross,hurst_regime] — best: MACD bull cross hist 0.0056 vol 1.3x

### Parsed signal features
- **atr_val**: 0.5048818875823725
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 74.44267716862645,
  "atr_tp": 76.71464566274712,
  "atr_val": 0.5048818875823725,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75.2
- exit_price: 75.16
- tp_price: 76.71
- sl_price: 74.44
- qty: 133.0 · notional: 100.016
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.008
- **planned_sl_distance_pct**: 1.0106
- **planned_r_multiple**: 1.987
- **planned_risk_usd**: 101.08
- **planned_reward_usd**: 200.83
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.0612
- **exit_distance_from_sl_pct**: 0.9574
- **notional**: 100.016

### Market excursion (MFE / MAE proxy)
- high_water: 75.2 · low_water: 75.2
- current_stop_at_close: 74.44
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.0612%
- slippage vs planned SL: 0.9574%

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
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`confluence`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618202+00:00Z · journaler v2*
