# Trade #61 — XMR-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0156 (-0.029% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.47 min

> Short gave back gains on trail on XMR-USDT (connors_rsi2, -0.03%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD22843`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-07T03:00:46.102454+00:00`
- closed: `2026-05-07T03:05:14.316247+00:00` · hour UTC 03 (Thu)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [funding,connors_rsi2] — best: Connors RSI2 short: RSI2=95.2, in downtrend

### Parsed signal features
- **rsi2**: 95.2
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 413.95759999999996,
  "atr_tp": 399.68319999999994,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 407.98
- exit_price: 408.1
- tp_price: 399.68
- sl_price: 413.96
- qty: 1.3 · notional: 53.037400000000005
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 2.0344
- **planned_sl_distance_pct**: 1.4658
- **planned_r_multiple**: 1.388
- **planned_risk_usd**: 7.774
- **planned_reward_usd**: 10.79
- **realized_r_multiple**: -0.002
- **exit_distance_from_tp_pct**: 2.0638
- **exit_distance_from_sl_pct**: 1.4363
- **notional**: 53.037400000000005

### Market excursion (MFE / MAE proxy)
- high_water: 407.98 · low_water: 407.57
- current_stop_at_close: 413.96
- **mfe_pct**: 0.1005
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1299

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.002
- slippage vs planned TP: 2.0638%
- slippage vs planned SL: 1.4363%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559945Z · journaler v2*
