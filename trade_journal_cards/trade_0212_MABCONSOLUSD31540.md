# Trade #212 — SOL-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8378 (-1.655% if pct available) · **Decision grade:** A (100/100) · **Hold:** 11.64 min

> Long stopped out at full risk on SOL-USDT (connors_rsi2, -1.65%) trail gave back 1.72% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONSOLUSD31540`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T14:05:42.416696+00:00`
- closed: `2026-05-24T14:17:20.653915+00:00` · hour UTC 14 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.4, ATR%=0.17, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.4
- **atr_pct**: 0.17
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 84.48344999999999,
  "atr_tp": 87.4854,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 85.82
- exit_price: 84.4
- tp_price: 87.49
- sl_price: 84.48
- qty: 0.59 · notional: 50.633799999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9459
- **planned_sl_distance_pct**: 1.5614
- **planned_r_multiple**: 1.246
- **planned_risk_usd**: 0.7906
- **planned_reward_usd**: 0.9853
- **realized_r_multiple**: -1.06
- **exit_distance_from_tp_pct**: 3.6006
- **exit_distance_from_sl_pct**: -0.0932
- **notional**: 50.633799999999994

### Market excursion (MFE / MAE proxy)
- high_water: 85.88 · low_water: 85.82
- current_stop_at_close: 84.48
- **mfe_pct**: 0.0699
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.7245

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.06
- slippage vs planned TP: 3.6006%
- slippage vs planned SL: -0.0932%

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
  - high confidence (8) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905556Z · journaler v2*
