# Trade #96 — BCH-USDT short (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** B (85/100) · **Hold:** 3.91 min

> Short flat exit (scratch) on BCH-USDT (connors_rsi2, +0.00%) during dead-zone hour 09:00 UTC [grade B / 85].

## 1 · Identity
- custom_id: `MABCONBCHUSD93334`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T09:55:36.012214+00:00`
- closed: `2026-05-11T09:59:30.686704+00:00` · hour UTC 09 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.3, ATR%=0.10, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.3
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 457.359,
  "atr_tp": 441.588,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 450.4
- exit_price: 450.4
- tp_price: 441.59
- sl_price: 457.36
- qty: 1.2 · notional: 54.047999999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.956
- **planned_sl_distance_pct**: 1.5453
- **planned_r_multiple**: 1.266
- **planned_risk_usd**: 8.352
- **planned_reward_usd**: 10.572
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.956
- **exit_distance_from_sl_pct**: 1.5453
- **notional**: 54.047999999999995

### Market excursion (MFE / MAE proxy)
- high_water: 450.4 · low_water: 450.4
- current_stop_at_close: 457.36
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.956%
- slippage vs planned SL: 1.5453%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `very_short_hold`, `time_or_manual`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.562023Z · journaler v2*
