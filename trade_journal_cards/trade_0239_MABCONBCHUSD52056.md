# Trade #239 — BCH-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.4640 (+0.457% if pct available) · **Decision grade:** A (100/100) · **Hold:** 81.44 min

> Short trailed into profit on BCH-USDT (connors_rsi2, +0.46%) during good-zone hour 00:00 UTC trail gave back 0.60% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD52056`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-25T23:34:18.370479+00:00`
- closed: `2026-05-26T00:55:44.920984+00:00` · hour UTC 00 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.3, ATR%=0.14, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.3
- **atr_pct**: 0.14
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 355.453,
  "atr_tp": 343.19599999999997,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 350.2
- exit_price: 348.6
- tp_price: 343.2
- sl_price: 355.45
- qty: 2.9 · notional: 101.55799999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9989
- **planned_sl_distance_pct**: 1.4991
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 15.225
- **planned_reward_usd**: 20.3
- **realized_r_multiple**: 0.03
- **exit_distance_from_tp_pct**: 1.542
- **exit_distance_from_sl_pct**: 1.956
- **notional**: 101.55799999999999

### Market excursion (MFE / MAE proxy)
- high_water: 350.2 · low_water: 346.5
- current_stop_at_close: 348.579
- **mfe_pct**: 1.0565
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5997

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.03
- slippage vs planned TP: 1.542%
- slippage vs planned SL: 1.956%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`good_hour`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-26T03:01:12.558758Z · journaler v2*
