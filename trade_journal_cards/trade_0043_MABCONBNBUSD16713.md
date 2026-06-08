# Trade #43 — BNB-USDT long (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 16.26 min

> Long flat exit (scratch) on BNB-USDT (connors_rsi2, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD16713`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-05T21:31:54.074400+00:00`
- closed: `2026-05-05T21:48:09.655666+00:00` · hour UTC 21 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.3, in uptrend

### Parsed signal features
- **rsi2**: 4.3
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 623.3178499999999,
  "atr_tp": 645.4662
}
```

## 3 · Plan vs Execution
- entry_price: 632.81
- exit_price: 632.81
- tp_price: 645.47
- sl_price: 623.32
- qty: 8.0 · notional: 50.62479999999999
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0006
- **planned_sl_distance_pct**: 1.4997
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 75.92
- **planned_reward_usd**: 101.28
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.0006
- **exit_distance_from_sl_pct**: 1.4997
- **notional**: 50.62479999999999

### Market excursion (MFE / MAE proxy)
- high_water: 633.24 · low_water: 632.81
- current_stop_at_close: 623.32
- **mfe_pct**: 0.068
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.068

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.0006%
- slippage vs planned SL: 1.4997%

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
`time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559326Z · journaler v2*
