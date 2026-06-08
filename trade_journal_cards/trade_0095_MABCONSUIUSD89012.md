# Trade #95 — SUI-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0920 (-0.183% if pct available) · **Decision grade:** D (55/100) · **Hold:** 35.87 min

> Long gave back gains on trail on SUI-USDT (connors_rsi2, -0.18%) during dead-zone hour 09:00 UTC [flagged-losing-symbol] trail gave back 0.56% [grade D / 55].

## 1 · Identity
- custom_id: `MABCONSUIUSD89012`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SUI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T08:43:33.887853+00:00`
- closed: `2026-05-11T09:19:26.024182+00:00` · hour UTC 09 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.2, ATR%=0.69, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.2
- **atr_pct**: 0.69
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 1.236766,
  "atr_tp": 1.280712,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1.2558
- exit_price: 1.2535
- tp_price: 1.2807
- sl_price: 1.2368
- qty: 40.0 · notional: 50.232
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9828
- **planned_sl_distance_pct**: 1.513
- **planned_r_multiple**: 1.311
- **planned_risk_usd**: 0.76
- **planned_reward_usd**: 0.996
- **realized_r_multiple**: -0.121
- **exit_distance_from_tp_pct**: 2.1659
- **exit_distance_from_sl_pct**: 1.3298
- **notional**: 50.232

### Market excursion (MFE / MAE proxy)
- high_water: 1.2605 · low_water: 1.2558
- current_stop_at_close: 1.2368
- **mfe_pct**: 0.3743
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5574

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.121
- slippage vs planned TP: 2.1659%
- slippage vs planned SL: 1.3298%

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
`dead_hour`, `losing_symbol`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.561993Z · journaler v2*
