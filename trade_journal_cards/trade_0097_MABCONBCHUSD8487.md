# Trade #97 — BCH-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0600 (+0.111% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.79 min

> Short trailed into profit on BCH-USDT (connors_rsi2, +0.11%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD8487`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T14:08:08.893949+00:00`
- closed: `2026-05-11T14:14:56.057691+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.4, ATR%=0.14, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.4
- **atr_pct**: 0.14
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 458.17099999999994,
  "atr_tp": 442.37199999999996,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 451.4
- exit_price: 450.9
- tp_price: 442.37
- sl_price: 458.17
- qty: 1.2 · notional: 54.16799999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0004
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 8.124
- **planned_reward_usd**: 10.836
- **realized_r_multiple**: 0.007
- **exit_distance_from_tp_pct**: 1.8897
- **exit_distance_from_sl_pct**: 1.6105
- **notional**: 54.16799999999999

### Market excursion (MFE / MAE proxy)
- high_water: 451.4 · low_water: 450.8
- current_stop_at_close: 458.17
- **mfe_pct**: 0.1329
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0222

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.007
- slippage vs planned TP: 1.8897%
- slippage vs planned SL: 1.6105%

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
`short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562053Z · journaler v2*
