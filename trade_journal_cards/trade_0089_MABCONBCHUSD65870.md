# Trade #89 — BCH-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0110 (-0.022% if pct available) · **Decision grade:** A (90/100) · **Hold:** 3.76 min

> Long closed in the red without clean exit on BCH-USDT (connors_rsi2, -0.02%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBCHUSD65870`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T02:17:52.467407+00:00`
- closed: `2026-05-11T02:21:38.344836+00:00` · hour UTC 02 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.5, ATR%=0.21, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.5
- **atr_pct**: 0.21
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 451.6225,
  "atr_tp": 467.67,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 458.5
- exit_price: 458.4
- tp_price: 467.67
- sl_price: 451.62
- qty: 1.1 · notional: 50.43500000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5005
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.568
- **planned_reward_usd**: 10.087
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.0218
- **exit_distance_from_sl_pct**: 1.4787
- **notional**: 50.43500000000001

### Market excursion (MFE / MAE proxy)
- high_water: 458.8 · low_water: 458.5
- current_stop_at_close: 451.62
- **mfe_pct**: 0.0654
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0872

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.0218%
- slippage vs planned SL: 1.4787%

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
*journaled_at 2026-05-17T03:54:39.561790Z · journaler v2*
