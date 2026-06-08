# Trade #320 — ONDO-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.1129 (+0.113% if pct available) · **Decision grade:** B (80/100) · **Hold:** 2.98 min

> Long trailed into profit on ONDO-USDT (macd_cross, +0.11%) [flagged-losing-symbol] [grade B / 80].

## 1 · Identity
- custom_id: `MABMACONDOUS70667`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T03:24:29.039916+00:00`
- closed: `2026-06-02T03:27:28.055015+00:00` · hour UTC 03 (Tue)

## 2 · Hypothesis (why we entered)
> MACD bull cross hist 0.0002 vol 1.6x

### Parsed signal features
- **atr_val**: 0.007015240223594395
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 0.34407713966460846,
  "atr_tp": 0.3756457206707832,
  "atr_val": 0.007015240223594395,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.3543
- exit_price: 0.3547
- tp_price: 0.3756
- sl_price: 0.3441
- qty: 2823.0 · notional: 100.01889
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 6.0119
- **planned_sl_distance_pct**: 2.8789
- **planned_r_multiple**: 2.088
- **planned_risk_usd**: 28.7946
- **planned_reward_usd**: 60.1299
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 5.899
- **exit_distance_from_sl_pct**: 2.9918
- **notional**: 100.01889

### Market excursion (MFE / MAE proxy)
- high_water: 0.3553 · low_water: 0.3543
- current_stop_at_close: 0.3441
- **mfe_pct**: 0.2822
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1693

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 5.899%
- slippage vs planned SL: 2.9918%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - flagged-losing-symbol
  - strong planned R:R=2.088

## 7 · Tags
`losing_symbol`, `very_short_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-06-05T21:57:18.618225+00:00Z · journaler v2*
