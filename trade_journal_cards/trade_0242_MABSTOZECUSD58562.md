# Trade #242 — ZEC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.3376 (-1.318% if pct available) · **Decision grade:** A (100/100) · **Hold:** 42.29 min

> Long stopped out at full risk on ZEC-USDT (stoch_rsi, -1.32%) trail gave back 1.51% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD58562`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-26T01:22:43.442134+00:00`
- closed: `2026-05-26T02:05:00.983042+00:00` · hour UTC 02 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 626.9571,
  "atr_tp": 642.7893499999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 634.1
- exit_price: 625.74
- tp_price: 642.79
- sl_price: 626.96
- qty: 1.6 · notional: 101.45600000000002
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.3704
- **planned_sl_distance_pct**: 1.126
- **planned_r_multiple**: 1.217
- **planned_risk_usd**: 11.424
- **planned_reward_usd**: 13.904
- **realized_r_multiple**: -0.117
- **exit_distance_from_tp_pct**: 2.6889
- **exit_distance_from_sl_pct**: -0.1924
- **notional**: 101.45600000000002

### Market excursion (MFE / MAE proxy)
- high_water: 635.3 · low_water: 634.1
- current_stop_at_close: 626.96
- **mfe_pct**: 0.1892
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.5076

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.117
- slippage vs planned TP: 2.6889%
- slippage vs planned SL: -0.1924%

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
  - high confidence (9) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-26T03:01:12.558794Z · journaler v2*
