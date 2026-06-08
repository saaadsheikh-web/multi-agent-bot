# Trade #157 — BTC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0148 (-0.027% if pct available) · **Decision grade:** A (90/100) · **Hold:** 6.68 min

> Long closed in the red without clean exit on BTC-USDT (connors_rsi2, -0.03%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBTCUSD46118`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T06:48:40.057949+00:00`
- closed: `2026-05-21T06:55:20.984336+00:00` · hour UTC 06 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.8, ATR%=0.09, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.8
- **atr_pct**: 0.09
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 76406.35149999999,
  "atr_tp": 79121.298,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 77591.2
- exit_price: 77570.0
- tp_price: 79121.3
- sl_price: 76406.4
- qty: 0.7 · notional: 54.31384
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.972
- **planned_sl_distance_pct**: 1.527
- **planned_r_multiple**: 1.291
- **planned_risk_usd**: 829.36
- **planned_reward_usd**: 1071.07
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.9993
- **exit_distance_from_sl_pct**: 1.4997
- **notional**: 54.31384

### Market excursion (MFE / MAE proxy)
- high_water: 77607.0 · low_water: 77591.2
- current_stop_at_close: 76406.4
- **mfe_pct**: 0.0204
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0477

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.9993%
- slippage vs planned SL: 1.4997%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-21T07:01:00.212505Z · journaler v2*
