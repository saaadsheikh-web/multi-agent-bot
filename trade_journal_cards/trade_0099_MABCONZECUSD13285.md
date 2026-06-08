# Trade #99 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.4470 (+0.801% if pct available) · **Decision grade:** A (100/100) · **Hold:** 35.37 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.80%) trail gave back 0.61% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD13285`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T15:28:07.197682+00:00`
- closed: `2026-05-11T16:03:29.445144+00:00` · hour UTC 16 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [ema_ribbon,connors_rsi2] — best: Connors RSI2 short: RSI2=99.1, ATR%=0.50, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.1
- **atr_pct**: 0.5
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 566.1365499999999,
  "atr_tp": 546.6146,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 557.94
- exit_price: 553.47
- tp_price: 546.61
- sl_price: 566.14
- qty: 1.0 · notional: 55.79400000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0307
- **planned_sl_distance_pct**: 1.4697
- **planned_r_multiple**: 1.382
- **planned_risk_usd**: 8.2
- **planned_reward_usd**: 11.33
- **realized_r_multiple**: 0.055
- **exit_distance_from_tp_pct**: 1.2295
- **exit_distance_from_sl_pct**: 2.2709
- **notional**: 55.79400000000001

### Market excursion (MFE / MAE proxy)
- high_water: 557.94 · low_water: 550.06
- current_stop_at_close: 553.3603599999999
- **mfe_pct**: 1.4123
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6112

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.055
- slippage vs planned TP: 1.2295%
- slippage vs planned SL: 2.2709%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562123Z · journaler v2*
