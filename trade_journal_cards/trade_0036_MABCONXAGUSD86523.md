# Trade #36 — XAG-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.4624 (+0.920% if pct available) · **Decision grade:** A (100/100) · **Hold:** 335.94 min

> Short trailed into profit on XAG-USDT (connors_rsi2, +0.92%) during good-zone hour 18:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXAGUSD86523`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XAG-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-05T13:08:43.964121+00:00`
- closed: `2026-05-05T18:44:40.173869+00:00` · hour UTC 18 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.7, in downtrend

### Parsed signal features
- **rsi2**: 95.7
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 75.0085,
  "atr_tp": 72.42200000000001
}
```

## 3 · Plan vs Execution
- entry_price: 73.9
- exit_price: 73.22
- tp_price: 72.42
- sl_price: 75.01
- qty: 68.0 · notional: 50.25200000000001
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0027
- **planned_sl_distance_pct**: 1.502
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 75.48
- **planned_reward_usd**: 100.64
- **realized_r_multiple**: 0.006
- **exit_distance_from_tp_pct**: 1.0825
- **exit_distance_from_sl_pct**: 2.4222
- **notional**: 50.25200000000001

### Market excursion (MFE / MAE proxy)
- high_water: 73.9 · low_water: 72.97
- current_stop_at_close: 75.01
- **mfe_pct**: 1.2585
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3383

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.006
- slippage vs planned TP: 1.0825%
- slippage vs planned SL: 2.4222%

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
`good_hour`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559112Z · journaler v2*
