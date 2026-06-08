# Trade #10 — YFI-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.1128 (-0.225% if pct available) · **Decision grade:** C (65/100) · **Hold:** 177.56 min

> Long gave back gains on trail on YFI-USDT (connors_rsi2, -0.23%) during dead-zone hour 10:00 UTC [flagged-losing-symbol] (was up 0.86% before reversing) trail gave back 1.09% [grade C / 65].

## 1 · Identity
- custom_id: `MABCONYFIUSD78496`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `YFI-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T07:08:17.623554+00:00`
- closed: `2026-05-04T10:05:51.285705+00:00` · hour UTC 10 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=3.2, in uptrend

### Parsed signal features
- **rsi2**: 3.2
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 2625.025,
  "atr_tp": 2718.3
}
```

## 3 · Plan vs Execution
- entry_price: 2665.0
- exit_price: 2659.0
- tp_price: 2718.3
- sl_price: 2625.025
- qty: 188.0 · notional: 50.102000000000004
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7515.3
- **planned_reward_usd**: 10020.4
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.2251
- **exit_distance_from_sl_pct**: 1.2749
- **notional**: 50.102000000000004

### Market excursion (MFE / MAE proxy)
- high_water: 2688.0 · low_water: 2665.0
- current_stop_at_close: 2666.496
- **mfe_pct**: 0.863
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0882

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.2251%
- slippage vs planned SL: 1.2749%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** C (65/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour
  - multi-agent confluence
  - high confidence (10) lost

## 7 · Tags
`dead_hour`, `losing_symbol`, `confluence`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.558067Z · journaler v2*
