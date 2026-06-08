# Trade #11 — BNB-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.3768 (-0.750% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.13 min

> Long gave back gains on trail on BNB-USDT (connors_rsi2, -0.75%) (was up 0.51% before reversing) trail gave back 1.26% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD80312`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T07:38:33.046562+00:00`
- closed: `2026-05-04T13:38:40.950164+00:00` · hour UTC 13 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=3.5, in uptrend

### Parsed signal features
- **rsi2**: 3.5
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 618.74745,
  "atr_tp": 640.7334
}
```

## 3 · Plan vs Execution
- entry_price: 628.17
- exit_price: 623.46
- tp_price: 640.7334
- sl_price: 618.74745
- qty: 8.0 · notional: 50.2536
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 75.3804
- **planned_reward_usd**: 100.5072
- **realized_r_multiple**: -0.005
- **exit_distance_from_tp_pct**: 2.7498
- **exit_distance_from_sl_pct**: 0.7502
- **notional**: 50.2536

### Market excursion (MFE / MAE proxy)
- high_water: 631.39 · low_water: 628.17
- current_stop_at_close: 618.74745
- **mfe_pct**: 0.5126
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.2624

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.005
- slippage vs planned TP: 2.7498%
- slippage vs planned SL: 0.7502%

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
  - high confidence (10) lost

## 7 · Tags
`confluence`, `gave_back_winner`, `trail_too_loose`, `long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558237Z · journaler v2*
