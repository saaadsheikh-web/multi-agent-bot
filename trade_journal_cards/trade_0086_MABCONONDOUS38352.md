# Trade #86 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.4835 (+0.966% if pct available) · **Decision grade:** C (70/100) · **Hold:** 66.7 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +0.97%) during good-zone hour 19:00 UTC [flagged-losing-symbol] trail gave back 0.61% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS38352`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-10T18:39:13.800449+00:00`
- closed: `2026-05-10T19:45:55.983308+00:00` · hour UTC 19 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.4, ATR%=0.46, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.4
- **atr_pct**: 0.46
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.40631249999999997,
  "atr_tp": 0.42074999999999996,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4125
- exit_price: 0.41648599999999997
- tp_price: 0.4207
- sl_price: 0.4063
- qty: 1213.0 · notional: 50.03625
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9879
- **planned_sl_distance_pct**: 1.503
- **planned_r_multiple**: 1.323
- **planned_risk_usd**: 7.5206
- **planned_reward_usd**: 9.9466
- **realized_r_multiple**: 0.064
- **exit_distance_from_tp_pct**: 1.0216
- **exit_distance_from_sl_pct**: 2.4693
- **notional**: 50.03625

### Market excursion (MFE / MAE proxy)
- high_water: 0.419 · low_water: 0.4125
- current_stop_at_close: 0.41648599999999997
- **mfe_pct**: 1.5758
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6095

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.064
- slippage vs planned TP: 1.0216%
- slippage vs planned SL: 2.4693%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol

## 7 · Tags
`good_hour`, `losing_symbol`, `trail_too_loose`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.561700Z · journaler v2*
