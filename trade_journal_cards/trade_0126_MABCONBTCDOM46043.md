# Trade #126 — BTCDOM-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0010 (-0.002% if pct available) · **Decision grade:** A (90/100) · **Hold:** 3.1 min

> Long closed in the red without clean exit on BTCDOM-USDT (connors_rsi2, -0.00%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBTCDOM46043`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-16T15:40:44.983491+00:00`
- closed: `2026-05-16T15:43:50.843712+00:00` · hour UTC 15 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.8, ATR%=0.06, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.8
- **atr_pct**: 0.06
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 5457.786499999999,
  "atr_tp": 5651.718,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5540.2
- exit_price: 5540.1
- tp_price: 5651.7
- sl_price: 5457.8
- qty: 10.0 · notional: 55.402
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0126
- **planned_sl_distance_pct**: 1.4873
- **planned_r_multiple**: 1.353
- **planned_risk_usd**: 824.0
- **planned_reward_usd**: 1115.0
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0144
- **exit_distance_from_sl_pct**: 1.4855
- **notional**: 55.402

### Market excursion (MFE / MAE proxy)
- high_water: 5541.6 · low_water: 5540.2
- current_stop_at_close: 5457.8
- **mfe_pct**: 0.0253
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0271

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0144%
- slippage vs planned SL: 1.4855%

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
  - high confidence (8) lost

## 7 · Tags
`very_short_hold`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562890Z · journaler v2*
