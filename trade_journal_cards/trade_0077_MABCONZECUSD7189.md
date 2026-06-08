# Trade #77 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -1.1830 (-1.878% if pct available) · **Decision grade:** A (100/100) · **Hold:** 29.22 min

> Long stopped out at full risk on ZEC-USDT (connors_rsi2, -1.88%) trail gave back 2.09% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD7189`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T06:13:10.481442+00:00`
- closed: `2026-05-09T06:42:23.889117+00:00` · hour UTC 06 (Sat)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [ema_ribbon,connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=4.9, in uptrend

### Parsed signal features
- **rsi2**: 4.9
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 620.1560000000001,
  "atr_tp": 642.192,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 629.78
- exit_price: 617.95
- tp_price: 642.19
- sl_price: 620.16
- qty: 1.0 · notional: 62.978
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9705
- **planned_sl_distance_pct**: 1.5275
- **planned_r_multiple**: 1.29
- **planned_risk_usd**: 9.62
- **planned_reward_usd**: 12.41
- **realized_r_multiple**: -0.123
- **exit_distance_from_tp_pct**: 3.849
- **exit_distance_from_sl_pct**: -0.3509
- **notional**: 62.978

### Market excursion (MFE / MAE proxy)
- high_water: 631.12 · low_water: 629.78
- current_stop_at_close: 620.16
- **mfe_pct**: 0.2128
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 2.0912

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.123
- slippage vs planned TP: 3.849%
- slippage vs planned SL: -0.3509%

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
  - high confidence (9) lost

## 7 · Tags
`confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560492Z · journaler v2*
