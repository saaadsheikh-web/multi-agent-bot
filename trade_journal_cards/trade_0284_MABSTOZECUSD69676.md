# Trade #284 — ZEC-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.9972 (+0.970% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.5 min

> Short trailed into profit on ZEC-USDT (stoch_rsi, +0.97%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD69676`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-31T23:21:18.132148+00:00`
- closed: `2026-05-31T23:26:47.981937+00:00` · hour UTC 23 (Sun)

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
  "atr_sl": 576.5585,
  "atr_tp": 562.28725,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 571.41
- exit_price: 565.87
- tp_price: 562.29
- sl_price: 576.56
- qty: 1.8 · notional: 102.8538
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5961
- **planned_sl_distance_pct**: 0.9013
- **planned_r_multiple**: 1.771
- **planned_risk_usd**: 9.27
- **planned_reward_usd**: 16.416
- **realized_r_multiple**: 0.108
- **exit_distance_from_tp_pct**: 0.6265
- **exit_distance_from_sl_pct**: 1.8708
- **notional**: 102.8538

### Market excursion (MFE / MAE proxy)
- high_water: 571.41 · low_water: 565.77
- current_stop_at_close: 568.59885
- **mfe_pct**: 0.987
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0175

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.108
- slippage vs planned TP: 0.6265%
- slippage vs planned SL: 1.8708%

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
*journaled_at 2026-06-05T21:57:18.617520+00:00Z · journaler v2*
