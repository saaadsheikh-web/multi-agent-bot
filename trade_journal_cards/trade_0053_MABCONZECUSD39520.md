# Trade #53 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.0690 (+2.047% if pct available) · **Decision grade:** A (100/100) · **Hold:** 85.97 min

> Clean long TP hit on ZEC-USDT (connors_rsi2, +2.05%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD39520`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T03:52:01.255012+00:00`
- closed: `2026-05-06T05:17:59.399146+00:00` · hour UTC 05 (Wed)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.9, in uptrend

### Parsed signal features
- **rsi2**: 4.9
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 514.33745,
  "atr_tp": 532.6134,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 522.17
- exit_price: 532.86
- tp_price: 532.61
- sl_price: 514.34
- qty: 1.0 · notional: 52.217
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9993
- **planned_sl_distance_pct**: 1.4995
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.83
- **planned_reward_usd**: 10.44
- **realized_r_multiple**: 0.137
- **exit_distance_from_tp_pct**: -0.0479
- **exit_distance_from_sl_pct**: 3.5467
- **notional**: 52.217

### Market excursion (MFE / MAE proxy)
- high_water: 532.86 · low_water: 522.17
- current_stop_at_close: 514.34
- **mfe_pct**: 2.0472
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.137
- slippage vs planned TP: -0.0479%
- slippage vs planned SL: 3.5467%

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
*journaled_at 2026-05-17T03:54:39.559701Z · journaler v2*
