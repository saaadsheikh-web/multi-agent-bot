# Trade #172 — XMR-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.4004 (+0.744% if pct available) · **Decision grade:** A (100/100) · **Hold:** 50.24 min

> Short trailed into profit on XMR-USDT (connors_rsi2, +0.74%) trail gave back 0.65% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD19400`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T03:10:01.790502+00:00`
- closed: `2026-05-22T04:00:16.284296+00:00` · hour UTC 04 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [funding,connors_rsi2] — best: Connors RSI2 short: RSI2=99.0, ATR%=0.33, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.0
- **atr_pct**: 0.33
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 390.34869999999995,
  "atr_tp": 376.8884,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 384.58
- exit_price: 381.72
- tp_price: 376.89
- sl_price: 390.35
- qty: 1.4 · notional: 53.84119999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9996
- **planned_sl_distance_pct**: 1.5003
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 8.078
- **planned_reward_usd**: 10.766
- **realized_r_multiple**: 0.05
- **exit_distance_from_tp_pct**: 1.2559
- **exit_distance_from_sl_pct**: 2.244
- **notional**: 53.84119999999999

### Market excursion (MFE / MAE proxy)
- high_water: 384.58 · low_water: 379.23
- current_stop_at_close: 381.50538
- **mfe_pct**: 1.3911
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6475

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.05
- slippage vs planned TP: 1.2559%
- slippage vs planned SL: 2.244%

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
`confluence`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570438Z · journaler v2*
