# Trade #136 — BNB-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0256 (-0.050% if pct available) · **Decision grade:** A (90/100) · **Hold:** 5.98 min

> Short closed in the red without clean exit on BNB-USDT (connors_rsi2, -0.05%) during good-zone hour 19:00 UTC [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBNBUSD33761`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-18T19:49:23.018864+00:00`
- closed: `2026-05-18T19:55:21.630730+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=99.5, ATR%=0.17, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.5
- **atr_pct**: 0.17
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 654.2081,
  "atr_tp": 631.6492,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 644.34
- exit_price: 644.66
- tp_price: 631.65
- sl_price: 654.21
- qty: 8.0 · notional: 51.547200000000004
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9695
- **planned_sl_distance_pct**: 1.5318
- **planned_r_multiple**: 1.286
- **planned_risk_usd**: 78.96
- **planned_reward_usd**: 101.52
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0191
- **exit_distance_from_sl_pct**: 1.4821
- **notional**: 51.547200000000004

### Market excursion (MFE / MAE proxy)
- high_water: 644.34 · low_water: 644.26
- current_stop_at_close: 654.21
- **mfe_pct**: 0.0124
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0621

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0191%
- slippage vs planned SL: 1.4821%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
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
`good_hour`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-18T23:01:50.789786Z · journaler v2*
