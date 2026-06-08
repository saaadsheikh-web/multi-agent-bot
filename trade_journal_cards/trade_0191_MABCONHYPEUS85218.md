# Trade #191 — HYPE-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0387 (-0.077% if pct available) · **Decision grade:** A (100/100) · **Hold:** 98.44 min

> Short gave back gains on trail on HYPE-USDT (connors_rsi2, -0.08%) (was up 0.70% before reversing) trail gave back 0.78% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS85218`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T21:27:00.085562+00:00`
- closed: `2026-05-22T23:05:26.284007+00:00` · hour UTC 23 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.2, ATR%=0.67, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.2
- **atr_pct**: 0.67
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 56.539559999999994,
  "atr_tp": 54.58992,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 55.704
- exit_price: 55.747
- tp_price: 54.59
- sl_price: 56.54
- qty: 9.0 · notional: 50.1336
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9999
- **planned_sl_distance_pct**: 1.5008
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.524
- **planned_reward_usd**: 10.026
- **realized_r_multiple**: -0.005
- **exit_distance_from_tp_pct**: 2.0771
- **exit_distance_from_sl_pct**: 1.4236
- **notional**: 50.1336

### Market excursion (MFE / MAE proxy)
- high_water: 55.704 · low_water: 55.315
- current_stop_at_close: 55.704
- **mfe_pct**: 0.6983
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7755

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.005
- slippage vs planned TP: 2.0771%
- slippage vs planned SL: 1.4236%

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
  - high confidence (9) lost

## 7 · Tags
`gave_back_winner`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570747Z · journaler v2*
