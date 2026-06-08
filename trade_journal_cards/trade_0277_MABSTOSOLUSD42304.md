# Trade #277 — SOL-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0366 (-0.037% if pct available) · **Decision grade:** A (90/100) · **Hold:** 4.92 min

> Long closed in the red without clean exit on SOL-USDT (stoch_rsi, -0.04%) [grade A / 90].

## 1 · Identity
- custom_id: `MABSTOSOLUSD42304`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `SOL-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-31T15:45:06.243950+00:00`
- closed: `2026-05-31T15:50:01.701492+00:00` · hour UTC 15 (Sun)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.07 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 81.1602,
  "atr_tp": 83.2097,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 81.98
- exit_price: 81.95
- tp_price: 83.21
- sl_price: 81.16
- qty: 1.22 · notional: 100.0156
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5004
- **planned_sl_distance_pct**: 1.0002
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1.0004
- **planned_reward_usd**: 1.5006
- **realized_r_multiple**: -0.037
- **exit_distance_from_tp_pct**: 1.537
- **exit_distance_from_sl_pct**: 0.9636
- **notional**: 100.0156

### Market excursion (MFE / MAE proxy)
- high_water: 82.03 · low_water: 81.98
- current_stop_at_close: 81.16
- **mfe_pct**: 0.061
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0976

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.037
- slippage vs planned TP: 1.537%
- slippage vs planned SL: 0.9636%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`very_short_hold`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617385+00:00Z · journaler v2*
