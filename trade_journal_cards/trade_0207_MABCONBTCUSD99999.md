# Trade #207 — BTC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0019 (-0.004% if pct available) · **Decision grade:** A (90/100) · **Hold:** 7.01 min

> Long closed in the red without clean exit on BTC-USDT (connors_rsi2, -0.00%) during good-zone hour 05:00 UTC [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBTCUSD99999`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T05:20:00.781819+00:00`
- closed: `2026-05-24T05:27:01.290603+00:00` · hour UTC 05 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.1, ATR%=0.06, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.1
- **atr_pct**: 0.06
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 75524.284,
  "atr_tp": 78207.88799999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 76674.4
- exit_price: 76671.7
- tp_price: 78207.9
- sl_price: 75524.3
- qty: 0.7 · notional: 53.672079999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 805.07
- **planned_reward_usd**: 1073.45
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0035
- **exit_distance_from_sl_pct**: 1.4965
- **notional**: 53.672079999999994

### Market excursion (MFE / MAE proxy)
- high_water: 76683.4 · low_water: 76674.4
- current_stop_at_close: 75524.3
- **mfe_pct**: 0.0117
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0153

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0035%
- slippage vs planned SL: 1.4965%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
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
`good_hour`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905469Z · journaler v2*
