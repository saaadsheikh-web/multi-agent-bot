# Trade #192 — BCH-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0700 (+0.138% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.74 min

> Short trailed into profit on BCH-USDT (connors_rsi2, +0.14%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD18582`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T06:43:04.496676+00:00`
- closed: `2026-05-23T06:48:48.661111+00:00` · hour UTC 06 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.8, ATR%=0.12, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.8
- **atr_pct**: 0.12
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 367.227,
  "atr_tp": 354.564,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 361.8
- exit_price: 361.3
- tp_price: 354.56
- sl_price: 367.23
- qty: 1.4 · notional: 50.651999999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0011
- **planned_sl_distance_pct**: 1.5008
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.602
- **planned_reward_usd**: 10.136
- **realized_r_multiple**: 0.009
- **exit_distance_from_tp_pct**: 1.8629
- **exit_distance_from_sl_pct**: 1.639
- **notional**: 50.651999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 361.8 · low_water: 361.1
- current_stop_at_close: 367.23
- **mfe_pct**: 0.1935
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0553

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.009
- slippage vs planned TP: 1.8629%
- slippage vs planned SL: 1.639%

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
*journaled_at 2026-05-23T15:00:56.570792Z · journaler v2*
