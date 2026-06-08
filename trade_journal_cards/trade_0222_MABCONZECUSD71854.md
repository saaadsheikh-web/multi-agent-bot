# Trade #222 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1968 (+0.376% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.42 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.38%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD71854`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T01:17:36.039738+00:00`
- closed: `2026-05-25T01:20:01.348943+00:00` · hour UTC 01 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.5, ATR%=0.50, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.5
- **atr_pct**: 0.5
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 644.978,
  "atr_tp": 667.896,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 654.8
- exit_price: 657.26
- tp_price: 667.9
- sl_price: 644.98
- qty: 0.8 · notional: 52.38400000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0006
- **planned_sl_distance_pct**: 1.4997
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.856
- **planned_reward_usd**: 10.48
- **realized_r_multiple**: 0.025
- **exit_distance_from_tp_pct**: 1.6249
- **exit_distance_from_sl_pct**: 1.8754
- **notional**: 52.38400000000001

### Market excursion (MFE / MAE proxy)
- high_water: 657.68 · low_water: 654.8
- current_stop_at_close: 644.98
- **mfe_pct**: 0.4398
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0641

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.025
- slippage vs planned TP: 1.6249%
- slippage vs planned SL: 1.8754%

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
`good_hour`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905688Z · journaler v2*
