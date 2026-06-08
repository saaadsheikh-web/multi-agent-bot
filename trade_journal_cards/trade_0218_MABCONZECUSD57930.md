# Trade #218 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.5928 (-1.110% if pct available) · **Decision grade:** A (90/100) · **Hold:** 13.98 min

> Long closed in the red without clean exit on ZEC-USDT (connors_rsi2, -1.11%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONZECUSD57930`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-24T21:25:32.202115+00:00`
- closed: `2026-05-24T21:39:31.108804+00:00` · hour UTC 21 (Sun)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=2.2, ATR%=0.53, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.2
- **atr_pct**: 0.53
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 657.7829999999999,
  "atr_tp": 681.156,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 667.27
- exit_price: 659.86
- tp_price: 681.16
- sl_price: 657.78
- qty: 0.8 · notional: 53.381600000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0816
- **planned_sl_distance_pct**: 1.4222
- **planned_r_multiple**: 1.464
- **planned_risk_usd**: 7.592
- **planned_reward_usd**: 11.112
- **realized_r_multiple**: -0.078
- **exit_distance_from_tp_pct**: 3.1921
- **exit_distance_from_sl_pct**: 0.3117
- **notional**: 53.381600000000006

### Market excursion (MFE / MAE proxy)
- high_water: 667.27 · low_water: 667.27
- current_stop_at_close: 657.78
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.078
- slippage vs planned TP: 3.1921%
- slippage vs planned SL: 0.3117%

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
*journaled_at 2026-05-25T23:01:34.905659Z · journaler v2*
