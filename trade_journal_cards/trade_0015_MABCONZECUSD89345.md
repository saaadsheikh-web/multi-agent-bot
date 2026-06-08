# Trade #15 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -1.8700 (-2.274% if pct available) · **Decision grade:** A (95/100) · **Hold:** 14.15 min

> Long stopped out at full risk on ZEC-USDT (connors_rsi2, -2.27%) during dead-zone hour 10:00 UTC trail gave back 2.54% [grade A / 95].

## 1 · Identity
- custom_id: `MABCONZECUSD89345`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T10:09:06.711274+00:00`
- closed: `2026-05-04T10:23:15.550942+00:00` · hour UTC 10 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=3.2, in uptrend

### Parsed signal features
- **rsi2**: 3.2
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 405.0911,
  "atr_tp": 419.4852
}
```

## 3 · Plan vs Execution
- entry_price: 411.25
- exit_price: 401.9
- tp_price: 419.4852
- sl_price: 405.0911
- qty: 2.0 · notional: 82.25
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0025
- **planned_sl_distance_pct**: 1.4976
- **planned_r_multiple**: 1.337
- **planned_risk_usd**: 12.3178
- **planned_reward_usd**: 16.4704
- **realized_r_multiple**: -0.152
- **exit_distance_from_tp_pct**: 4.276
- **exit_distance_from_sl_pct**: -0.776
- **notional**: 82.25

### Market excursion (MFE / MAE proxy)
- high_water: 412.35 · low_water: 411.25
- current_stop_at_close: 405.0911
- **mfe_pct**: 0.2675
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 2.541

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.152
- slippage vs planned TP: 4.276%
- slippage vs planned SL: -0.776%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - dead-zone-hour
  - multi-agent confluence
  - high confidence (10) lost

## 7 · Tags
`dead_hour`, `confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558138Z · journaler v2*
