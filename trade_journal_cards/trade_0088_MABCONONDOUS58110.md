# Trade #88 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.3805 (+0.760% if pct available) · **Decision grade:** C (70/100) · **Hold:** 2.81 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +0.76%) during good-zone hour 00:00 UTC [flagged-losing-symbol] [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS58110`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T00:08:32.265028+00:00`
- closed: `2026-05-11T00:11:20.837018+00:00` · hour UTC 00 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.6, ATR%=0.62, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.6
- **atr_pct**: 0.62
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.414488,
  "atr_tp": 0.42921600000000004,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4208
- exit_price: 0.424
- tp_price: 0.4292
- sl_price: 0.4145
- qty: 1189.0 · notional: 50.033120000000004
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9962
- **planned_sl_distance_pct**: 1.4971
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.4907
- **planned_reward_usd**: 9.9876
- **realized_r_multiple**: 0.051
- **exit_distance_from_tp_pct**: 1.2357
- **exit_distance_from_sl_pct**: 2.2576
- **notional**: 50.033120000000004

### Market excursion (MFE / MAE proxy)
- high_water: 0.4241 · low_water: 0.4208
- current_stop_at_close: 0.4208
- **mfe_pct**: 0.7842
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0238

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.051
- slippage vs planned TP: 1.2357%
- slippage vs planned SL: 2.2576%

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
`good_hour`, `losing_symbol`, `very_short_hold`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.561761Z · journaler v2*
