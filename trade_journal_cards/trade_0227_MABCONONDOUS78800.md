# Trade #227 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0572 (+0.114% if pct available) · **Decision grade:** C (70/100) · **Hold:** 18.29 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +0.11%) [flagged-losing-symbol] trail gave back 0.73% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS78800`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T03:13:22.087722+00:00`
- closed: `2026-05-25T03:31:39.513277+00:00` · hour UTC 03 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.4, ATR%=0.63, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.4
- **atr_pct**: 0.63
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.431036,
  "atr_tp": 0.44635199999999997,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4377
- exit_price: 0.4382
- tp_price: 0.4464
- sl_price: 0.431
- qty: 1143.0 · notional: 50.02911
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9877
- **planned_sl_distance_pct**: 1.5307
- **planned_r_multiple**: 1.299
- **planned_risk_usd**: 7.6581
- **planned_reward_usd**: 9.9441
- **realized_r_multiple**: 0.007
- **exit_distance_from_tp_pct**: 1.8734
- **exit_distance_from_sl_pct**: 1.645
- **notional**: 50.02911

### Market excursion (MFE / MAE proxy)
- high_water: 0.4414 · low_water: 0.4377
- current_stop_at_close: 0.4387516
- **mfe_pct**: 0.8453
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7311

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.007
- slippage vs planned TP: 1.8734%
- slippage vs planned SL: 1.645%

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
*journaled_at 2026-05-25T23:01:34.905784Z · journaler v2*
