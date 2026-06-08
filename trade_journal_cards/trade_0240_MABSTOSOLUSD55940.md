# Trade #240 — SOL-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0476 (-0.047% if pct available) · **Decision grade:** A (90/100) · **Hold:** 240.19 min

> Long closed in the red without clean exit on SOL-USDT (stoch_rsi, -0.05%) [grade A / 90].

## 1 · Identity
- custom_id: `MABSTOSOLUSD55940`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `SOL-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-26T00:39:01.538942+00:00`
- closed: `2026-05-26T04:39:13.152607+00:00` · hour UTC 04 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=34

### Parsed signal features
- **rsi**: 34.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 83.55600000000001,
  "atr_tp": 85.666,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 84.43
- exit_price: 84.39
- tp_price: 85.67
- sl_price: 83.56
- qty: 1.19 · notional: 100.4717
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4687
- **planned_sl_distance_pct**: 1.0304
- **planned_r_multiple**: 1.425
- **planned_risk_usd**: 1.0353
- **planned_reward_usd**: 1.4756
- **realized_r_multiple**: -0.046
- **exit_distance_from_tp_pct**: 1.516
- **exit_distance_from_sl_pct**: 0.9831
- **notional**: 100.4717

### Market excursion (MFE / MAE proxy)
- high_water: 84.49 · low_water: 84.43
- current_stop_at_close: 83.56
- **mfe_pct**: 0.0711
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1184

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.046
- slippage vs planned TP: 1.516%
- slippage vs planned SL: 0.9831%

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
`long_hold`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-26T07:01:11.917143Z · journaler v2*
