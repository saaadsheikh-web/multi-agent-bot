# Trade #12 — BTCDOM-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1090 (+0.198% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.14 min

> Short trailed into profit on BTCDOM-USDT (connors_rsi2, +0.20%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBTCDOM82738`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTCDOM-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-04T08:18:59.664674+00:00`
- closed: `2026-05-04T14:19:08.315882+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 short: RSI2=96.4, in downtrend

### Parsed signal features
- **rsi2**: 96.4
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 5584.326999999999,
  "atr_tp": 5391.764
}
```

## 3 · Plan vs Execution
- entry_price: 5501.8
- exit_price: 5490.9
- tp_price: 5391.764
- sl_price: 5584.326999999999
- qty: 10.0 · notional: 55.018
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 825.27
- **planned_reward_usd**: 1100.36
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.8019
- **exit_distance_from_sl_pct**: 1.6981
- **notional**: 55.018

### Market excursion (MFE / MAE proxy)
- high_water: 5501.8 · low_water: 5481.6
- current_stop_at_close: 5584.326999999999
- **mfe_pct**: 0.3672
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.169

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.8019%
- slippage vs planned SL: 1.6981%

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

## 7 · Tags
`confluence`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558275Z · journaler v2*
