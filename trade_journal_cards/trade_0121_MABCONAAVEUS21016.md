# Trade #121 — AAVE-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7504 (-1.498% if pct available) · **Decision grade:** A (95/100) · **Hold:** 5.53 min

> Short stopped out at full risk on AAVE-USDT (connors_rsi2, -1.50%) during dead-zone hour 08:00 UTC trail gave back 1.74% [grade A / 95].

## 1 · Identity
- custom_id: `MABCONAAVEUS21016`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `AAVE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T08:43:37.511244+00:00`
- closed: `2026-05-16T08:49:09.449357+00:00` · hour UTC 08 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [ema_ribbon,connors_rsi2] — best: Connors RSI2 short: RSI2=99.3, ATR%=0.25, downtrend slope-down

### Parsed signal features
- **rsi2**: 99.3
- **atr_pct**: 0.25
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 90.78159999999998,
  "atr_tp": 87.6512,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 89.44
- exit_price: 90.78
- tp_price: 87.65
- sl_price: 90.78
- qty: 5.6 · notional: 50.08639999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0013
- **planned_sl_distance_pct**: 1.4982
- **planned_r_multiple**: 1.336
- **planned_risk_usd**: 7.504
- **planned_reward_usd**: 10.024
- **realized_r_multiple**: -0.1
- **exit_distance_from_tp_pct**: 3.4996
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 50.08639999999999

### Market excursion (MFE / MAE proxy)
- high_water: 89.44 · low_water: 89.22
- current_stop_at_close: 90.78
- **mfe_pct**: 0.246
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.7442

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.1
- slippage vs planned TP: 3.4996%
- slippage vs planned SL: 0.0%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - dead-zone-hour
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `confluence`, `trail_too_loose`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562833Z · journaler v2*
