# Trade #160 — BCH-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0420 (+0.080% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.53 min

> Long timed out in profit on BCH-USDT (connors_rsi2, +0.08%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD73360`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T14:22:42.170166+00:00`
- closed: `2026-05-21T14:26:14.151950+00:00` · hour UTC 14 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.2, ATR%=0.25, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.2
- **atr_pct**: 0.25
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 370.4585,
  "atr_tp": 383.622,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 376.1
- exit_price: 376.4
- tp_price: 383.62
- sl_price: 370.46
- qty: 1.4 · notional: 52.653999999999996
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9995
- **planned_sl_distance_pct**: 1.4996
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.896
- **planned_reward_usd**: 10.528
- **realized_r_multiple**: 0.005
- **exit_distance_from_tp_pct**: 1.9197
- **exit_distance_from_sl_pct**: 1.5794
- **notional**: 52.653999999999996

### Market excursion (MFE / MAE proxy)
- high_water: 376.4 · low_water: 376.1
- current_stop_at_close: 370.46
- **mfe_pct**: 0.0798
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.005
- slippage vs planned TP: 1.9197%
- slippage vs planned SL: 1.5794%

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
`very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570227Z · journaler v2*
