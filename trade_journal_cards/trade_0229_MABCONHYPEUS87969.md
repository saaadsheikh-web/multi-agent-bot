# Trade #229 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.5625 (+1.010% if pct available) · **Decision grade:** A (100/100) · **Hold:** 24.45 min

> Long trailed into profit on HYPE-USDT (connors_rsi2, +1.01%) trail gave back 0.72% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS87969`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T05:46:10.634759+00:00`
- closed: `2026-05-25T06:10:37.630184+00:00` · hour UTC 06 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.7, ATR%=0.48, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.7
- **atr_pct**: 0.48
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 61.03651,
  "atr_tp": 63.20532,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 61.867
- exit_price: 62.492
- tp_price: 63.205
- sl_price: 61.037
- qty: 9.0 · notional: 55.680299999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.1627
- **planned_sl_distance_pct**: 1.3416
- **planned_r_multiple**: 1.612
- **planned_risk_usd**: 7.47
- **planned_reward_usd**: 12.042
- **realized_r_multiple**: 0.075
- **exit_distance_from_tp_pct**: 1.1525
- **exit_distance_from_sl_pct**: 2.3518
- **notional**: 55.680299999999995

### Market excursion (MFE / MAE proxy)
- high_water: 62.935 · low_water: 61.867
- current_stop_at_close: 62.557390000000005
- **mfe_pct**: 1.7263
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7161

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.075
- slippage vs planned TP: 1.1525%
- slippage vs planned SL: 2.3518%

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
  - (no notable factors)

## 7 · Tags
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905799Z · journaler v2*
