# Trade #228 — SOL-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.4012 (-0.798% if pct available) · **Decision grade:** A (90/100) · **Hold:** 513.85 min

> Short closed in the red without clean exit on SOL-USDT (connors_rsi2, -0.80%) trail gave back 0.87% [grade A / 90].

## 1 · Identity
- custom_id: `MABCONSOLUSD83634`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-25T04:33:55.950426+00:00`
- closed: `2026-05-25T13:07:47.184459+00:00` · hour UTC 13 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=99.5, ATR%=0.15, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.5
- **atr_pct**: 0.15
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 86.51859999999999,
  "atr_tp": 83.53519999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 85.24
- exit_price: 85.92
- tp_price: 83.54
- sl_price: 86.52
- qty: 0.59 · notional: 50.291599999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9944
- **planned_sl_distance_pct**: 1.5016
- **planned_r_multiple**: 1.328
- **planned_risk_usd**: 0.7552
- **planned_reward_usd**: 1.003
- **realized_r_multiple**: -0.531
- **exit_distance_from_tp_pct**: 2.7921
- **exit_distance_from_sl_pct**: 0.7039
- **notional**: 50.291599999999995

### Market excursion (MFE / MAE proxy)
- high_water: 85.24 · low_water: 85.18
- current_stop_at_close: 86.52
- **mfe_pct**: 0.0704
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8681

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.531
- slippage vs planned TP: 2.7921%
- slippage vs planned SL: 0.7039%

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
  - high confidence (8) lost

## 7 · Tags
`trail_too_loose`, `long_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905850Z · journaler v2*
