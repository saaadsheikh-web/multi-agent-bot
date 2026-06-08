# Trade #106 — SUI-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0120 (-0.023% if pct available) · **Decision grade:** C (70/100) · **Hold:** 19.3 min

> Long gave back gains on trail on SUI-USDT (connors_rsi2, -0.02%) during good-zone hour 01:00 UTC [flagged-losing-symbol] (was up 0.56% before reversing) trail gave back 0.59% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONSUIUSD48616`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SUI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-12T01:16:57.860167+00:00`
- closed: `2026-05-12T01:36:16.016822+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.7, ATR%=0.54, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.7
- **atr_pct**: 0.54
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 1.2632625,
  "atr_tp": 1.30815,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 1.2807
- exit_price: 1.2804
- tp_price: 1.3081
- sl_price: 1.2633
- qty: 40.0 · notional: 51.227999999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.1395
- **planned_sl_distance_pct**: 1.3586
- **planned_r_multiple**: 1.575
- **planned_risk_usd**: 0.696
- **planned_reward_usd**: 1.096
- **realized_r_multiple**: -0.017
- **exit_distance_from_tp_pct**: 2.1629
- **exit_distance_from_sl_pct**: 1.3352
- **notional**: 51.227999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 1.2879 · low_water: 1.2807
- current_stop_at_close: 1.2807
- **mfe_pct**: 0.5622
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5856

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.017
- slippage vs planned TP: 2.1629%
- slippage vs planned SL: 1.3352%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `losing_symbol`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.562367Z · journaler v2*
