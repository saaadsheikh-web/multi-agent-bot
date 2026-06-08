# Trade #265 — INTC-USDT short (macd_cross)

**Outcome:** LOSS · **PnL:** -0.0170 (-0.017% if pct available) · **Decision grade:** A (100/100) · **Hold:** 47.78 min

> Short gave back gains on trail on INTC-USDT (macd_cross, -0.02%) (was up 0.77% before reversing) trail gave back 0.79% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACINTCUS68056`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `INTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-29T15:20:58.002762+00:00`
- closed: `2026-05-29T16:08:44.711806+00:00` · hour UTC 16 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [macd_cross,hurst_regime] — best: MACD bear cross hist -0.1780 vol 1.5x

### Parsed signal features
- **atr_val**: 1.659490559842622
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 121.28923583976393,
  "atr_tp": 113.82152832047213,
  "atr_val": 1.659490559842622,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 118.8
- exit_price: 118.82
- tp_price: 113.82
- sl_price: 121.29
- qty: 85.0 · notional: 100.97999999999999
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 4.1919
- **planned_sl_distance_pct**: 2.096
- **planned_r_multiple**: 2.0
- **planned_risk_usd**: 211.65
- **planned_reward_usd**: 423.3
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 4.2088
- **exit_distance_from_sl_pct**: 2.0791
- **notional**: 100.97999999999999

### Market excursion (MFE / MAE proxy)
- high_water: 118.8 · low_water: 117.88
- current_stop_at_close: 118.8
- **mfe_pct**: 0.7744
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7912

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 4.2088%
- slippage vs planned SL: 2.0791%

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
  - strong planned R:R=2.0
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`confluence`, `gave_back_winner`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617145+00:00Z · journaler v2*
