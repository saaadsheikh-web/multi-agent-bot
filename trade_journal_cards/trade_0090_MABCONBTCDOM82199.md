# Trade #90 — BTCDOM-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0080 (-0.015% if pct available) · **Decision grade:** A (90/100) · **Hold:** 2.51 min

> Short closed in the red without clean exit on BTCDOM-USDT (connors_rsi2, -0.01%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBTCDOM82199`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTCDOM-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T06:50:01.056371+00:00`
- closed: `2026-05-11T06:52:31.404661+00:00` · hour UTC 06 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.5, ATR%=0.04, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.5
- **atr_pct**: 0.04
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 5523.020999999999,
  "atr_tp": 5332.571999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5440.6
- exit_price: 5441.4
- tp_price: 5332.6
- sl_price: 5523.0
- qty: 10.0 · notional: 54.406000000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9851
- **planned_sl_distance_pct**: 1.5145
- **planned_r_multiple**: 1.311
- **planned_risk_usd**: 824.0
- **planned_reward_usd**: 1080.0
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.9998
- **exit_distance_from_sl_pct**: 1.4998
- **notional**: 54.406000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 5440.6 · low_water: 5440.6
- current_stop_at_close: 5523.0
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.9998%
- slippage vs planned SL: 1.4998%

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
`very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.561826Z · journaler v2*
