# Trade #132 — BCH-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0780 (-0.145% if pct available) · **Decision grade:** A (90/100) · **Hold:** 4.7 min

> Short closed in the red without clean exit on BCH-USDT (connors_rsi2, -0.15%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBCHUSD52965`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-17T21:22:46.801854+00:00`
- closed: `2026-05-17T21:27:28.538316+00:00` · hour UTC 21 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.8, ATR%=0.10, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.8
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 419.39799999999997,
  "atr_tp": 404.936,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 413.2
- exit_price: 413.8
- tp_price: 404.94
- sl_price: 419.4
- qty: 1.3 · notional: 53.716
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.999
- **planned_sl_distance_pct**: 1.5005
- **planned_r_multiple**: 1.332
- **planned_risk_usd**: 8.06
- **planned_reward_usd**: 10.738
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 2.1442
- **exit_distance_from_sl_pct**: 1.3553
- **notional**: 53.716

### Market excursion (MFE / MAE proxy)
- high_water: 413.2 · low_water: 413.0
- current_stop_at_close: 419.4
- **mfe_pct**: 0.0484
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1936

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.01
- slippage vs planned TP: 2.1442%
- slippage vs planned SL: 1.3553%

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
*journaled_at 2026-05-17T23:01:19.388221Z · journaler v2*
