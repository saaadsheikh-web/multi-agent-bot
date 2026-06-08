# Trade #161 — BCH-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2240 (+0.425% if pct available) · **Decision grade:** A (100/100) · **Hold:** 111.92 min

> Long trailed into profit on BCH-USDT (connors_rsi2, +0.43%) trail gave back 0.66% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD73656`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T14:27:38.095344+00:00`
- closed: `2026-05-21T16:19:33.342582+00:00` · hour UTC 16 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.2, ATR%=0.24, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.2
- **atr_pct**: 0.24
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 370.55699999999996,
  "atr_tp": 383.724,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 376.3
- exit_price: 377.9
- tp_price: 383.72
- sl_price: 370.56
- qty: 1.4 · notional: 52.681999999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9718
- **planned_sl_distance_pct**: 1.5254
- **planned_r_multiple**: 1.293
- **planned_risk_usd**: 8.036
- **planned_reward_usd**: 10.388
- **realized_r_multiple**: 0.028
- **exit_distance_from_tp_pct**: 1.5466
- **exit_distance_from_sl_pct**: 1.9506
- **notional**: 52.681999999999995

### Market excursion (MFE / MAE proxy)
- high_water: 380.4 · low_water: 376.3
- current_stop_at_close: 378.1176
- **mfe_pct**: 1.0896
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6644

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.028
- slippage vs planned TP: 1.5466%
- slippage vs planned SL: 1.9506%

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
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570260Z · journaler v2*
