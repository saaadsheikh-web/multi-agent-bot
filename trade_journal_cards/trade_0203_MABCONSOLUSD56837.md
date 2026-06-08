# Trade #203 — SOL-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0900 (+0.178% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.2 min

> Short trailed into profit on SOL-USDT (connors_rsi2, +0.18%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONSOLUSD56837`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T17:20:39.330094+00:00`
- closed: `2026-05-23T17:23:51.033522+00:00` · hour UTC 17 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.0, ATR%=0.19, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.0
- **atr_pct**: 0.19
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 85.51374999999999,
  "atr_tp": 82.565,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 84.25
- exit_price: 84.1
- tp_price: 82.56
- sl_price: 85.51
- qty: 0.6 · notional: 50.55
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0059
- **planned_sl_distance_pct**: 1.4955
- **planned_r_multiple**: 1.341
- **planned_risk_usd**: 0.756
- **planned_reward_usd**: 1.014
- **realized_r_multiple**: 0.119
- **exit_distance_from_tp_pct**: 1.8279
- **exit_distance_from_sl_pct**: 1.6736
- **notional**: 50.55

### Market excursion (MFE / MAE proxy)
- high_water: 84.25 · low_water: 84.1
- current_stop_at_close: 85.51
- **mfe_pct**: 0.178
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.119
- slippage vs planned TP: 1.8279%
- slippage vs planned SL: 1.6736%

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
`very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905346Z · journaler v2*
