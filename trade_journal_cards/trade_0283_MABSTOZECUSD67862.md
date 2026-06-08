# Trade #283 — ZEC-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.4050 (+0.394% if pct available) · **Decision grade:** A (100/100) · **Hold:** 26.65 min

> Short trailed into profit on ZEC-USDT (stoch_rsi, +0.39%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD67862`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-31T22:51:04.461967+00:00`
- closed: `2026-05-31T23:17:43.741239+00:00` · hour UTC 23 (Sun)

## 2 · Hypothesis (why we entered)
> 3 agents agree (same-family) [bb_bounce,zscore_reversion,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=68

### Parsed signal features
- **rsi**: 68.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 576.5484,
  "atr_tp": 562.2774000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 570.51
- exit_price: 568.26
- tp_price: 562.28
- sl_price: 576.55
- qty: 1.8 · notional: 102.69180000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4426
- **planned_sl_distance_pct**: 1.0587
- **planned_r_multiple**: 1.363
- **planned_risk_usd**: 10.872
- **planned_reward_usd**: 14.814
- **realized_r_multiple**: 0.037
- **exit_distance_from_tp_pct**: 1.0482
- **exit_distance_from_sl_pct**: 1.4531
- **notional**: 102.69180000000001

### Market excursion (MFE / MAE proxy)
- high_water: 570.51 · low_water: 565.43
- current_stop_at_close: 568.2571499999999
- **mfe_pct**: 0.8904
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.496

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.037
- slippage vs planned TP: 1.0482%
- slippage vs planned SL: 1.4531%

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
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617499+00:00Z · journaler v2*
