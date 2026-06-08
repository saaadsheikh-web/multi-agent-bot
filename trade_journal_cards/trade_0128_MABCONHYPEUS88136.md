# Trade #128 — HYPE-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7752 (-1.540% if pct available) · **Decision grade:** A (100/100) · **Hold:** 28.55 min

> Short stopped out at full risk on HYPE-USDT (connors_rsi2, -1.54%) trail gave back 1.61% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS88136`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-17T03:22:18.333414+00:00`
- closed: `2026-05-17T03:50:51.151825+00:00` · hour UTC 03 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.9, ATR%=0.31, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.9
- **atr_pct**: 0.31
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 42.574175,
  "atr_tp": 41.1061,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 41.945
- exit_price: 42.591
- tp_price: 41.106
- sl_price: 42.574
- qty: 12.0 · notional: 50.33400000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0002
- **planned_sl_distance_pct**: 1.4996
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.548
- **planned_reward_usd**: 10.068
- **realized_r_multiple**: -0.103
- **exit_distance_from_tp_pct**: 3.5404
- **exit_distance_from_sl_pct**: -0.0405
- **notional**: 50.33400000000001

### Market excursion (MFE / MAE proxy)
- high_water: 41.945 · low_water: 41.916
- current_stop_at_close: 42.574
- **mfe_pct**: 0.0691
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.6093

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.103
- slippage vs planned TP: 3.5404%
- slippage vs planned SL: -0.0405%

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
`trail_too_loose`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.563044Z · journaler v2*
