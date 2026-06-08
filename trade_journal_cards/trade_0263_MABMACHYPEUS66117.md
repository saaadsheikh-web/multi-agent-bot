# Trade #263 — HYPE-USDT short (macd_cross)

**Outcome:** LOSS · **PnL:** -3.3269 (-3.142% if pct available) · **Decision grade:** A (100/100) · **Hold:** 18.33 min

> Short stopped out at full risk on HYPE-USDT (macd_cross, -3.14%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACHYPEUS66117`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-29T14:48:39.054808+00:00`
- closed: `2026-05-29T15:06:58.680271+00:00` · hour UTC 15 (Fri)

## 2 · Hypothesis (why we entered)
> MACD bear cross hist -0.0255 vol 2.0x

### Parsed signal features
- **atr_val**: 1.144028795343988
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 64.04304319301598,
  "atr_tp": 58.894913613968036,
  "atr_val": 1.144028795343988,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 62.284
- exit_price: 64.241
- tp_price: 58.895
- sl_price: 64.043
- qty: 17.0 · notional: 105.8828
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 5.4412
- **planned_sl_distance_pct**: 2.8242
- **planned_r_multiple**: 1.927
- **planned_risk_usd**: 29.903
- **planned_reward_usd**: 57.613
- **realized_r_multiple**: -0.111
- **exit_distance_from_tp_pct**: 8.5833
- **exit_distance_from_sl_pct**: -0.3179
- **notional**: 105.8828

### Market excursion (MFE / MAE proxy)
- high_water: 62.284 · low_water: 62.284
- current_stop_at_close: 64.043
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.111
- slippage vs planned TP: 8.5833%
- slippage vs planned SL: -0.3179%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617119+00:00Z · journaler v2*
