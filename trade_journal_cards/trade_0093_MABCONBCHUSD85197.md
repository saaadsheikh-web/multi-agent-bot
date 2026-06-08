# Trade #93 — BCH-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0240 (-0.044% if pct available) · **Decision grade:** A (90/100) · **Hold:** 2.62 min

> Short closed in the red without clean exit on BCH-USDT (connors_rsi2, -0.04%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBCHUSD85197`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T07:39:58.827270+00:00`
- closed: `2026-05-11T07:42:36.305747+00:00` · hour UTC 07 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.5, ATR%=0.14, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.5
- **atr_pct**: 0.14
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 457.15599999999995,
  "atr_tp": 441.392,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 450.2
- exit_price: 450.4
- tp_price: 441.39
- sl_price: 457.16
- qty: 1.2 · notional: 54.023999999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9569
- **planned_sl_distance_pct**: 1.546
- **planned_r_multiple**: 1.266
- **planned_risk_usd**: 8.352
- **planned_reward_usd**: 10.572
- **realized_r_multiple**: -0.003
- **exit_distance_from_tp_pct**: 2.0013
- **exit_distance_from_sl_pct**: 1.5016
- **notional**: 54.023999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 450.2 · low_water: 450.1
- current_stop_at_close: 457.16
- **mfe_pct**: 0.0222
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0666

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.003
- slippage vs planned TP: 2.0013%
- slippage vs planned SL: 1.5016%

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
*journaled_at 2026-05-17T03:54:39.561857Z · journaler v2*
