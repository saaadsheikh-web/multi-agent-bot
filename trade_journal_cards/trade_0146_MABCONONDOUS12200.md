# Trade #146 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0939 (+0.188% if pct available) · **Decision grade:** C (70/100) · **Hold:** 2.54 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +0.19%) [flagged-losing-symbol] [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS12200`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-19T17:36:42.446019+00:00`
- closed: `2026-05-19T17:39:14.816257+00:00` · hour UTC 17 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.6, ATR%=0.57, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.6
- **atr_pct**: 0.57
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.367011,
  "atr_tp": 0.380052,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.3726
- exit_price: 0.3733
- tp_price: 0.3801
- sl_price: 0.367
- qty: 1342.0 · notional: 50.00292
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0129
- **planned_sl_distance_pct**: 1.503
- **planned_r_multiple**: 1.339
- **planned_risk_usd**: 7.5152
- **planned_reward_usd**: 10.065
- **realized_r_multiple**: 0.013
- **exit_distance_from_tp_pct**: 1.825
- **exit_distance_from_sl_pct**: 1.6908
- **notional**: 50.00292

### Market excursion (MFE / MAE proxy)
- high_water: 0.3735 · low_water: 0.3726
- current_stop_at_close: 0.367
- **mfe_pct**: 0.2415
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0537

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.013
- slippage vs planned TP: 1.825%
- slippage vs planned SL: 1.6908%

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
*journaled_at 2026-05-19T19:01:11.341042Z · journaler v2*
