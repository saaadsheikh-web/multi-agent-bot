# Trade #206 — BNB-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0240 (-0.046% if pct available) · **Decision grade:** A (90/100) · **Hold:** 5.7 min

> Long closed in the red without clean exit on BNB-USDT (connors_rsi2, -0.05%) during good-zone hour 05:00 UTC [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBNBUSD99772`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T05:16:13.722784+00:00`
- closed: `2026-05-24T05:21:55.618217+00:00` · hour UTC 05 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.5, ATR%=0.09, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.5
- **atr_pct**: 0.09
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 645.93345,
  "atr_tp": 668.8854,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 655.74
- exit_price: 655.44
- tp_price: 668.89
- sl_price: 645.93
- qty: 8.0 · notional: 52.4592
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0054
- **planned_sl_distance_pct**: 1.496
- **planned_r_multiple**: 1.341
- **planned_risk_usd**: 78.48
- **planned_reward_usd**: 105.2
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0511
- **exit_distance_from_sl_pct**: 1.4503
- **notional**: 52.4592

### Market excursion (MFE / MAE proxy)
- high_water: 655.84 · low_water: 655.74
- current_stop_at_close: 645.93
- **mfe_pct**: 0.0152
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.061

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0511%
- slippage vs planned SL: 1.4503%

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
*journaled_at 2026-05-25T23:01:34.905452Z · journaler v2*
