# Trade #262 — HYPE-USDT short (macd_cross)

**Outcome:** WIN · **PnL:** +0.3536 (+0.354% if pct available) · **Decision grade:** A (100/100) · **Hold:** 15.76 min

> Short trailed into profit on HYPE-USDT (macd_cross, +0.35%) trail gave back 0.70% [grade A / 100].

## 1 · Identity
- custom_id: `MABMACHYPEUS65099`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-29T14:31:41.200407+00:00`
- closed: `2026-05-29T14:47:27.077961+00:00` · hour UTC 14 (Fri)

## 2 · Hypothesis (why we entered)
> MACD bear cross hist -0.0164 vol 1.6x

### Parsed signal features
- **atr_val**: 1.144028795343988
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 64.18604319301598,
  "atr_tp": 59.03791361396804,
  "atr_val": 1.144028795343988,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 62.513
- exit_price: 62.292
- tp_price: 59.038
- sl_price: 64.186
- qty: 16.0 · notional: 100.02080000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 5.5588
- **planned_sl_distance_pct**: 2.6762
- **planned_r_multiple**: 2.077
- **planned_risk_usd**: 26.768
- **planned_reward_usd**: 55.6
- **realized_r_multiple**: 0.013
- **exit_distance_from_tp_pct**: 5.2053
- **exit_distance_from_sl_pct**: 3.0298
- **notional**: 100.02080000000001

### Market excursion (MFE / MAE proxy)
- high_water: 62.513 · low_water: 61.857
- current_stop_at_close: 62.262947999999994
- **mfe_pct**: 1.0494
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6959

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.013
- slippage vs planned TP: 5.2053%
- slippage vs planned SL: 3.0298%

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
  - strong planned R:R=2.077

## 7 · Tags
`trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617069+00:00Z · journaler v2*
