# Trade #37 — TAO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8046 (-1.563% if pct available) · **Decision grade:** B (80/100) · **Hold:** 206.55 min

> Long stopped out at full risk on TAO-USDT (connors_rsi2, -1.56%) [flagged-losing-symbol] trail gave back 1.72% [grade B / 80].

## 1 · Identity
- custom_id: `MABCONTAOUSD88528`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `TAO-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-05T13:42:08.808345+00:00`
- closed: `2026-05-05T17:08:41.682252+00:00` · hour UTC 17 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=3.5, in uptrend

### Parsed signal features
- **rsi2**: 3.5
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 281.71,
  "atr_tp": 291.72
}
```

## 3 · Plan vs Execution
- entry_price: 286.0
- exit_price: 281.53
- tp_price: 291.72
- sl_price: 281.71
- qty: 18.0 · notional: 51.48
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 77.22
- **planned_reward_usd**: 102.96
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 3.5629
- **exit_distance_from_sl_pct**: -0.0629
- **notional**: 51.48

### Market excursion (MFE / MAE proxy)
- high_water: 286.46 · low_water: 286.0
- current_stop_at_close: 281.71
- **mfe_pct**: 0.1608
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.7238

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.01
- slippage vs planned TP: 3.5629%
- slippage vs planned SL: -0.0629%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - flagged-losing-symbol
  - multi-agent confluence
  - high confidence (10) lost

## 7 · Tags
`losing_symbol`, `confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.559047Z · journaler v2*
