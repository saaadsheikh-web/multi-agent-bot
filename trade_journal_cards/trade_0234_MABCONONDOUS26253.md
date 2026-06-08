# Trade #234 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.9843 (+1.968% if pct available) · **Decision grade:** C (70/100) · **Hold:** 62.82 min

> Clean long TP hit on ONDO-USDT (connors_rsi2, +1.97%) [flagged-losing-symbol] [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS26253`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T16:24:15.835859+00:00`
- closed: `2026-05-25T17:27:05.198178+00:00` · hour UTC 17 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.8, ATR%=0.47, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.8
- **atr_pct**: 0.47
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.42522449999999995,
  "atr_tp": 0.440334,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4319
- exit_price: 0.4404
- tp_price: 0.4403
- sl_price: 0.4252
- qty: 1158.0 · notional: 50.01402
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9449
- **planned_sl_distance_pct**: 1.5513
- **planned_r_multiple**: 1.254
- **planned_risk_usd**: 7.7586
- **planned_reward_usd**: 9.7272
- **realized_r_multiple**: 0.127
- **exit_distance_from_tp_pct**: -0.0232
- **exit_distance_from_sl_pct**: 3.5193
- **notional**: 50.01402

### Market excursion (MFE / MAE proxy)
- high_water: 0.4404 · low_water: 0.4319
- current_stop_at_close: 0.4377576
- **mfe_pct**: 1.968
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.127
- slippage vs planned TP: -0.0232%
- slippage vs planned SL: 3.5193%

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
`losing_symbol`, `tp_hit`, `grade_C`

---
*journaled_at 2026-05-25T23:01:34.905901Z · journaler v2*
