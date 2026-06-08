# Trade #334 — BTCDOM-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0133 (-0.013% if pct available) · **Decision grade:** A (100/100) · **Hold:** 76.18 min

> Long gave back gains on trail on BTCDOM-USDT (stoch_rsi, -0.01%) (was up 0.56% before reversing) trail gave back 0.57% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBTCDOM12381`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T14:59:43.216960+00:00`
- closed: `2026-06-02T16:15:53.868944+00:00` · hour UTC 16 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [stoch_rsi,golden_hour] — best: StochRSI long stoch=0.62 (was 0.00) rsi=29

### Parsed signal features
- **rsi**: 29.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 5252.247,
  "atr_tp": 5384.8795,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5305.3
- exit_price: 5304.6
- tp_price: 5384.9
- sl_price: 5252.2
- qty: 19.0 · notional: 100.8007
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5004
- **planned_sl_distance_pct**: 1.0009
- **planned_r_multiple**: 1.499
- **planned_risk_usd**: 1008.9
- **planned_reward_usd**: 1512.4
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.5136
- **exit_distance_from_sl_pct**: 0.9877
- **notional**: 100.8007

### Market excursion (MFE / MAE proxy)
- high_water: 5334.8 · low_water: 5305.3
- current_stop_at_close: 5305.3
- **mfe_pct**: 0.556
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5692

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.5136%
- slippage vs planned SL: 0.9877%

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
`confluence`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618681+00:00Z · journaler v2*
