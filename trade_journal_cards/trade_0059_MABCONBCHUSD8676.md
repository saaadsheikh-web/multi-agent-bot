# Trade #59 — BCH-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1100 (+0.216% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.03 min

> Long trailed into profit on BCH-USDT (connors_rsi2, +0.22%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD8676`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-06T23:04:38.314211+00:00`
- closed: `2026-05-06T23:09:40.215466+00:00` · hour UTC 23 (Wed)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.2, in uptrend

### Parsed signal features
- **rsi2**: 4.2
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 456.3505,
  "atr_tp": 472.56600000000003,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 463.1
- exit_price: 464.1
- tp_price: 472.57
- sl_price: 456.35
- qty: 1.1 · notional: 50.94100000000001
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 2.0449
- **planned_sl_distance_pct**: 1.4576
- **planned_r_multiple**: 1.403
- **planned_risk_usd**: 7.425
- **planned_reward_usd**: 10.417
- **realized_r_multiple**: 0.015
- **exit_distance_from_tp_pct**: 1.829
- **exit_distance_from_sl_pct**: 1.6735
- **notional**: 50.94100000000001

### Market excursion (MFE / MAE proxy)
- high_water: 464.1 · low_water: 463.1
- current_stop_at_close: 456.35
- **mfe_pct**: 0.2159
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.015
- slippage vs planned TP: 1.829%
- slippage vs planned SL: 1.6735%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559846Z · journaler v2*
