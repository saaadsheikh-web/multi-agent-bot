# Trade #38 — BNB-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2912 (+0.578% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.21 min

> Long trailed into profit on BNB-USDT (connors_rsi2, +0.58%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD90742`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-05T14:19:03.204425+00:00`
- closed: `2026-05-05T20:19:15.534768+00:00` · hour UTC 20 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=3.0, in uptrend

### Parsed signal features
- **rsi2**: 3.0
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 620.02795,
  "atr_tp": 642.0594
}
```

## 3 · Plan vs Execution
- entry_price: 629.55
- exit_price: 633.19
- tp_price: 642.06
- sl_price: 620.03
- qty: 8.0 · notional: 50.364
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.9871
- **planned_sl_distance_pct**: 1.5122
- **planned_r_multiple**: 1.314
- **planned_risk_usd**: 76.16
- **planned_reward_usd**: 100.08
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.4089
- **exit_distance_from_sl_pct**: 2.0904
- **notional**: 50.364

### Market excursion (MFE / MAE proxy)
- high_water: 633.55 · low_water: 629.55
- current_stop_at_close: 620.03
- **mfe_pct**: 0.6354
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0572

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.4089%
- slippage vs planned SL: 2.0904%

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
`confluence`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559265Z · journaler v2*
