# Trade #223 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.3626 (+0.725% if pct available) · **Decision grade:** C (70/100) · **Hold:** 26.38 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +0.72%) [flagged-losing-symbol] trail gave back 0.86% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS74284`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T01:58:05.802016+00:00`
- closed: `2026-05-25T02:24:28.612002+00:00` · hour UTC 02 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.7, ATR%=0.61, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.7
- **atr_pct**: 0.61
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.434385,
  "atr_tp": 0.44982,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4415
- exit_price: 0.4447
- tp_price: 0.4498
- sl_price: 0.4344
- qty: 1133.0 · notional: 50.021950000000004
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.88
- **planned_sl_distance_pct**: 1.6082
- **planned_r_multiple**: 1.169
- **planned_risk_usd**: 8.0443
- **planned_reward_usd**: 9.4039
- **realized_r_multiple**: 0.045
- **exit_distance_from_tp_pct**: 1.1552
- **exit_distance_from_sl_pct**: 2.333
- **notional**: 50.021950000000004

### Market excursion (MFE / MAE proxy)
- high_water: 0.4485 · low_water: 0.4415
- current_stop_at_close: 0.445809
- **mfe_pct**: 1.5855
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8607

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.045
- slippage vs planned TP: 1.1552%
- slippage vs planned SL: 2.333%

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
`losing_symbol`, `trail_too_loose`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-25T23:01:34.905749Z · journaler v2*
