# Trade #190 — ZEC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.3834 (+0.712% if pct available) · **Decision grade:** A (100/100) · **Hold:** 21.54 min

> Long trailed into profit on ZEC-USDT (stoch_rsi, +0.71%) trail gave back 0.52% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD83317`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 6
- opened: `2026-05-22T20:55:19.125251+00:00`
- closed: `2026-05-22T21:16:51.707013+00:00` · hour UTC 21 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: [trend-2] StochRSI long stoch=0.00 rsi=21

### Parsed signal features
- **rsi**: 21.0
- **trend_score**: -2
- **trend_dir**: DOWN
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 593.901,
  "atr_tp": 608.8984999999999,
  "_trend_score": -2,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 598.69
- exit_price: 602.95
- tp_price: 608.9
- sl_price: 593.9
- qty: 0.9 · notional: 53.88210000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.7054
- **planned_sl_distance_pct**: 0.8001
- **planned_r_multiple**: 2.131
- **planned_risk_usd**: 4.311
- **planned_reward_usd**: 9.189
- **realized_r_multiple**: 0.089
- **exit_distance_from_tp_pct**: 0.9938
- **exit_distance_from_sl_pct**: 1.5116
- **notional**: 53.88210000000001

### Market excursion (MFE / MAE proxy)
- high_water: 606.09 · low_water: 598.69
- current_stop_at_close: 603.0595500000001
- **mfe_pct**: 1.236
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5245

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.089
- slippage vs planned TP: 0.9938%
- slippage vs planned SL: 1.5116%

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
  - strong planned R:R=2.131
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570710Z · journaler v2*
