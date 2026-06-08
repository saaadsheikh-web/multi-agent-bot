# Trade #178 — BNB-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2192 (+0.417% if pct available) · **Decision grade:** A (100/100) · **Hold:** 279.22 min

> Long trailed into profit on BNB-USDT (connors_rsi2, +0.42%) trail gave back 0.66% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD42849`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T09:40:51.116720+00:00`
- closed: `2026-05-22T14:20:04.347349+00:00` · hour UTC 14 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.3, ATR%=0.11, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.3
- **atr_pct**: 0.11
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 647.27305,
  "atr_tp": 670.2726,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 657.2
- exit_price: 659.94
- tp_price: 670.27
- sl_price: 647.27
- qty: 8.0 · notional: 52.57600000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9887
- **planned_sl_distance_pct**: 1.511
- **planned_r_multiple**: 1.316
- **planned_risk_usd**: 79.44
- **planned_reward_usd**: 104.56
- **realized_r_multiple**: 0.003
- **exit_distance_from_tp_pct**: 1.5718
- **exit_distance_from_sl_pct**: 1.9279
- **notional**: 52.57600000000001

### Market excursion (MFE / MAE proxy)
- high_water: 664.29 · low_water: 657.2
- current_stop_at_close: 660.30426
- **mfe_pct**: 1.0788
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6619

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.003
- slippage vs planned TP: 1.5718%
- slippage vs planned SL: 1.9279%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`trail_too_loose`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570576Z · journaler v2*
