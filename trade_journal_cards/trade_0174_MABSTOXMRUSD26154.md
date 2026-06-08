# Trade #174 — XMR-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.8316 (+1.563% if pct available) · **Decision grade:** A (100/100) · **Hold:** 57.34 min

> Clean long TP hit on XMR-USDT (stoch_rsi, +1.56%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXMRUSD26154`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XMR-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-22T05:02:36.729694+00:00`
- closed: `2026-05-22T05:59:57.022443+00:00` · hour UTC 05 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.03 rsi=29

### Parsed signal features
- **rsi**: 29.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 376.3584,
  "atr_tp": 385.8624,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 379.97
- exit_price: 385.91
- tp_price: 385.86
- sl_price: 376.36
- qty: 1.4 · notional: 53.1958
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5501
- **planned_sl_distance_pct**: 0.9501
- **planned_r_multiple**: 1.632
- **planned_risk_usd**: 5.054
- **planned_reward_usd**: 8.246
- **realized_r_multiple**: 0.165
- **exit_distance_from_tp_pct**: -0.0132
- **exit_distance_from_sl_pct**: 2.5134
- **notional**: 53.1958

### Market excursion (MFE / MAE proxy)
- high_water: 385.91 · low_water: 379.97
- current_stop_at_close: 383.98045
- **mfe_pct**: 1.5633
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.165
- slippage vs planned TP: -0.0132%
- slippage vs planned SL: 2.5134%

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
`good_hour`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570474Z · journaler v2*
