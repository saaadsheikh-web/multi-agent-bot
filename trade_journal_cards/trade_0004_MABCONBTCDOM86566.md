# Trade #4 — BTCDOM-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.2040 (-0.072% if pct available) · **Decision grade:** A (100/100) · **Hold:** 120.07 min

> Long closed in the red without clean exit on BTCDOM-USDT (connors_rsi2, -0.07%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBTCDOM86566`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-02T01:49:27.731231+00:00`
- closed: `2026-05-02T03:49:32.101406+00:00` · hour UTC 03 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=1.8, in uptrend

### Parsed signal features
- **rsi2**: 1.8
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 5481.4944,
  "atr_tp": 5580.956999999999,
  "_paper_only": true
}
```

## 3 · Plan vs Execution
- entry_price: 5526.3
- exit_price: 5522.3
- tp_price: 5580.956999999999
- sl_price: 5481.4944
- qty: 51.0 · notional: 281.84130000000005
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 0.989
- **planned_sl_distance_pct**: 0.8108
- **planned_r_multiple**: 1.22
- **planned_risk_usd**: 2285.0856
- **planned_reward_usd**: 2787.507
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.0614
- **exit_distance_from_sl_pct**: 0.7384
- **notional**: 281.84130000000005

### Market excursion (MFE / MAE proxy)
- high_water: 5527.1 · low_water: 5526.3
- current_stop_at_close: 5481.4944
- **mfe_pct**: 0.0145
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0869

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.0614%
- slippage vs planned SL: 0.7384%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: True
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence
  - timed-out loser (no clean exit signal)
  - high confidence (10) lost

## 7 · Tags
`confluence`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.557847Z · journaler v2*
