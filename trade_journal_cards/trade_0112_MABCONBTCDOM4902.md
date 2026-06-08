# Trade #112 — BTCDOM-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0150 (-0.027% if pct available) · **Decision grade:** A (90/100) · **Hold:** 6.67 min

> Long closed in the red without clean exit on BTCDOM-USDT (connors_rsi2, -0.03%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBTCDOM4902`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTCDOM-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-12T16:55:04.366171+00:00`
- closed: `2026-05-12T17:01:44.585858+00:00` · hour UTC 17 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.9, ATR%=0.07, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.9
- **atr_pct**: 0.07
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 5433.9495,
  "atr_tp": 5627.034,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 5516.7
- exit_price: 5515.2
- tp_price: 5627.0
- sl_price: 5433.9
- qty: 10.0 · notional: 55.167
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9994
- **planned_sl_distance_pct**: 1.5009
- **planned_r_multiple**: 1.332
- **planned_risk_usd**: 828.0
- **planned_reward_usd**: 1103.0
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0266
- **exit_distance_from_sl_pct**: 1.4737
- **notional**: 55.167

### Market excursion (MFE / MAE proxy)
- high_water: 5517.5 · low_water: 5516.7
- current_stop_at_close: 5433.9
- **mfe_pct**: 0.0145
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0417

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0266%
- slippage vs planned SL: 1.4737%

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
`long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562549Z · journaler v2*
