# Trade #208 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.6275 (+1.254% if pct available) · **Decision grade:** C (70/100) · **Hold:** 52.28 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +1.25%) [flagged-losing-symbol] trail gave back 0.62% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS299`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T05:25:00.957575+00:00`
- closed: `2026-05-24T06:17:17.967087+00:00` · hour UTC 06 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.0, ATR%=0.58, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.0
- **atr_pct**: 0.58
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.4165565,
  "atr_tp": 0.431358,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4226
- exit_price: 0.4279
- tp_price: 0.4314
- sl_price: 0.4166
- qty: 1184.0 · notional: 50.03584
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0823
- **planned_sl_distance_pct**: 1.4198
- **planned_r_multiple**: 1.467
- **planned_risk_usd**: 7.104
- **planned_reward_usd**: 10.4192
- **realized_r_multiple**: 0.088
- **exit_distance_from_tp_pct**: 0.8282
- **exit_distance_from_sl_pct**: 2.6739
- **notional**: 50.03584

### Market excursion (MFE / MAE proxy)
- high_water: 0.4305 · low_water: 0.4226
- current_stop_at_close: 0.427917
- **mfe_pct**: 1.8694
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6152

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.088
- slippage vs planned TP: 0.8282%
- slippage vs planned SL: 2.6739%

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
*journaled_at 2026-05-25T23:01:34.905500Z · journaler v2*
