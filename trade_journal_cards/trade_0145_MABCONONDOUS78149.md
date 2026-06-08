# Trade #145 — ONDO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0653 (-0.131% if pct available) · **Decision grade:** D (55/100) · **Hold:** 14.37 min

> Long gave back gains on trail on ONDO-USDT (connors_rsi2, -0.13%) during dead-zone hour 08:00 UTC [flagged-losing-symbol] (was up 0.63% before reversing) trail gave back 0.76% [grade D / 55].

## 1 · Identity
- custom_id: `MABCONONDOUS78149`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-19T08:09:10.472264+00:00`
- closed: `2026-05-19T08:23:32.765720+00:00` · hour UTC 08 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.6, ATR%=0.68, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.6
- **atr_pct**: 0.68
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.3771565,
  "atr_tp": 0.390558,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.3829
- exit_price: 0.3824
- tp_price: 0.3906
- sl_price: 0.3772
- qty: 1306.0 · notional: 50.00674
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.011
- **planned_sl_distance_pct**: 1.4886
- **planned_r_multiple**: 1.351
- **planned_risk_usd**: 7.4442
- **planned_reward_usd**: 10.0562
- **realized_r_multiple**: -0.009
- **exit_distance_from_tp_pct**: 2.1416
- **exit_distance_from_sl_pct**: 1.3581
- **notional**: 50.00674

### Market excursion (MFE / MAE proxy)
- high_water: 0.3853 · low_water: 0.3829
- current_stop_at_close: 0.3829
- **mfe_pct**: 0.6268
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7574

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.009
- slippage vs planned TP: 2.1416%
- slippage vs planned SL: 1.3581%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** D (55/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `losing_symbol`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_D`

---
*journaled_at 2026-05-19T11:00:53.857620Z · journaler v2*
