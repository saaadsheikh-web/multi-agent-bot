# Trade #322 — ONDO-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +1.7372 (+1.737% if pct available) · **Decision grade:** A (90/100) · **Hold:** 24.75 min

> Long trailed into profit on ONDO-USDT (macd_cross, +1.74%) [flagged-losing-symbol] trail gave back 1.09% [grade A / 90].

## 1 · Identity
- custom_id: `MABMACONDOUS71224`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T03:33:46.025278+00:00`
- closed: `2026-06-02T03:58:31.276295+00:00` · hour UTC 03 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [macd_cross,hurst_regime] — best: MACD bull cross hist 0.0003 vol 1.6x

### Parsed signal features
- **atr_val**: 0.007158097366451538
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 0.3462628539503227,
  "atr_tp": 0.37847429209935457,
  "atr_val": 0.007158097366451538,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.357
- exit_price: 0.3632
- tp_price: 0.3785
- sl_price: 0.3463
- qty: 2802.0 · notional: 100.03139999999999
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 6.0224
- **planned_sl_distance_pct**: 2.9972
- **planned_r_multiple**: 2.009
- **planned_risk_usd**: 29.9814
- **planned_reward_usd**: 60.243
- **realized_r_multiple**: 0.058
- **exit_distance_from_tp_pct**: 4.2857
- **exit_distance_from_sl_pct**: 4.7339
- **notional**: 100.03139999999999

### Market excursion (MFE / MAE proxy)
- high_water: 0.3671 · low_water: 0.357
- current_stop_at_close: 0.363429
- **mfe_pct**: 2.8291
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0924

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.058
- slippage vs planned TP: 4.2857%
- slippage vs planned SL: 4.7339%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - flagged-losing-symbol
  - strong planned R:R=2.009
  - multi-agent confluence

## 7 · Tags
`losing_symbol`, `confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618275+00:00Z · journaler v2*
