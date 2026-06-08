# Trade #30 — BNB-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2672 (+0.533% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.03 min

> Long trailed into profit on BNB-USDT (connors_rsi2, +0.53%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD62512`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-05T06:28:33.651238+00:00`
- closed: `2026-05-05T12:28:35.571015+00:00` · hour UTC 12 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=4.5, in uptrend

### Parsed signal features
- **rsi2**: 4.5
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 617.34875,
  "atr_tp": 639.285
}
```

## 3 · Plan vs Execution
- entry_price: 626.75
- exit_price: 630.09
- tp_price: 639.28
- sl_price: 617.35
- qty: 8.0 · notional: 50.14
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.9992
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 75.2
- **planned_reward_usd**: 100.24
- **realized_r_multiple**: 0.004
- **exit_distance_from_tp_pct**: 1.4663
- **exit_distance_from_sl_pct**: 2.0327
- **notional**: 50.14

### Market excursion (MFE / MAE proxy)
- high_water: 630.11 · low_water: 626.75
- current_stop_at_close: 617.35
- **mfe_pct**: 0.5361
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0032

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.004
- slippage vs planned TP: 1.4663%
- slippage vs planned SL: 2.0327%

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
*journaled_at 2026-05-17T03:54:39.558884Z · journaler v2*
