# Trade #321 — ONDO-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.5074 (+0.507% if pct available) · **Decision grade:** C (70/100) · **Hold:** 4.12 min

> Long trailed into profit on ONDO-USDT (macd_cross, +0.51%) [flagged-losing-symbol] [grade C / 70].

## 1 · Identity
- custom_id: `MABMACONDOUS70903`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T03:28:25.174705+00:00`
- closed: `2026-06-02T03:32:32.145018+00:00` · hour UTC 03 (Tue)

## 2 · Hypothesis (why we entered)
> MACD bull cross hist 0.0002 vol 1.6x

### Parsed signal features
- **atr_val**: 0.007036668795022968
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 0.34424499680746556,
  "atr_tp": 0.3759100063850689,
  "atr_val": 0.007036668795022968,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.3548
- exit_price: 0.3566
- tp_price: 0.3759
- sl_price: 0.3442
- qty: 2819.0 · notional: 100.01812000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 5.947
- **planned_sl_distance_pct**: 2.9876
- **planned_r_multiple**: 1.991
- **planned_risk_usd**: 29.8814
- **planned_reward_usd**: 59.4809
- **realized_r_multiple**: 0.017
- **exit_distance_from_tp_pct**: 5.4397
- **exit_distance_from_sl_pct**: 3.4949
- **notional**: 100.01812000000001

### Market excursion (MFE / MAE proxy)
- high_water: 0.3566 · low_water: 0.3548
- current_stop_at_close: 0.3548
- **mfe_pct**: 0.5073
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.017
- slippage vs planned TP: 5.4397%
- slippage vs planned SL: 3.4949%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol

## 7 · Tags
`losing_symbol`, `very_short_hold`, `trail_stop`, `grade_C`

---
*journaled_at 2026-06-05T21:57:18.618246+00:00Z · journaler v2*
