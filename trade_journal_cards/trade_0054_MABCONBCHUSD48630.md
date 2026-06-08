# Trade #54 — BCH-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.3740 (-0.716% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.02 min

> Long gave back gains on trail on BCH-USDT (connors_rsi2, -0.72%) trail gave back 1.12% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD48630`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T06:23:51.498705+00:00`
- closed: `2026-05-06T12:23:52.462212+00:00` · hour UTC 12 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [ema_ribbon,connors_rsi2] — best: Connors RSI2 long: RSI2=4.3, in uptrend

### Parsed signal features
- **rsi2**: 4.3
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 467.1658,
  "atr_tp": 483.7656,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 474.6
- exit_price: 471.2
- tp_price: 483.77
- sl_price: 467.17
- qty: 1.1 · notional: 52.20600000000001
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9322
- **planned_sl_distance_pct**: 1.5655
- **planned_r_multiple**: 1.234
- **planned_risk_usd**: 8.173
- **planned_reward_usd**: 10.087
- **realized_r_multiple**: -0.046
- **exit_distance_from_tp_pct**: 2.6485
- **exit_distance_from_sl_pct**: 0.8491
- **notional**: 52.20600000000001

### Market excursion (MFE / MAE proxy)
- high_water: 476.5 · low_water: 474.6
- current_stop_at_close: 467.17
- **mfe_pct**: 0.4003
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.1167

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.046
- slippage vs planned TP: 2.6485%
- slippage vs planned SL: 0.8491%

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
`confluence`, `trail_too_loose`, `long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559739Z · journaler v2*
