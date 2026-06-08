# Trade #48 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.0790 (+2.110% if pct available) · **Decision grade:** A (100/100) · **Hold:** 70.72 min

> Clean long TP hit on ZEC-USDT (connors_rsi2, +2.11%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD26997`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T00:23:18.628123+00:00`
- closed: `2026-05-06T01:34:01.641224+00:00` · hour UTC 01 (Wed)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.1, in uptrend

### Parsed signal features
- **rsi2**: 4.1
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 503.77824999999996,
  "atr_tp": 521.679,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 511.45
- exit_price: 522.24
- tp_price: 521.68
- sl_price: 503.78
- qty: 1.0 · notional: 51.145
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0002
- **planned_sl_distance_pct**: 1.4997
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.67
- **planned_reward_usd**: 10.23
- **realized_r_multiple**: 0.141
- **exit_distance_from_tp_pct**: -0.1095
- **exit_distance_from_sl_pct**: 3.6093
- **notional**: 51.145

### Market excursion (MFE / MAE proxy)
- high_water: 522.24 · low_water: 511.45
- current_stop_at_close: 518.06208
- **mfe_pct**: 2.1097
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.141
- slippage vs planned TP: -0.1095%
- slippage vs planned SL: 3.6093%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`good_hour`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559605Z · journaler v2*
