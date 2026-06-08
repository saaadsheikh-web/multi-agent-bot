# Trade #94 — ZEC-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8870 (-1.556% if pct available) · **Decision grade:** A (95/100) · **Hold:** 62.82 min

> Short stopped out at full risk on ZEC-USDT (connors_rsi2, -1.56%) during dead-zone hour 09:00 UTC trail gave back 1.87% [grade A / 95].

## 1 · Identity
- custom_id: `MABCONZECUSD87383`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T08:16:24.917044+00:00`
- closed: `2026-05-11T09:19:13.981479+00:00` · hour UTC 09 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [ema_ribbon,connors_rsi2] — best: Connors RSI2 short: RSI2=95.0, ATR%=0.33, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.0
- **atr_pct**: 0.33
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 578.8748,
  "atr_tp": 558.9136000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 570.0
- exit_price: 578.87
- tp_price: 558.91
- sl_price: 578.87
- qty: 1.0 · notional: 57.0
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9456
- **planned_sl_distance_pct**: 1.5561
- **planned_r_multiple**: 1.25
- **planned_risk_usd**: 8.87
- **planned_reward_usd**: 11.09
- **realized_r_multiple**: -0.1
- **exit_distance_from_tp_pct**: 3.5018
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 57.0

### Market excursion (MFE / MAE proxy)
- high_water: 570.0 · low_water: 568.23
- current_stop_at_close: 578.87
- **mfe_pct**: 0.3105
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.8667

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.1
- slippage vs planned TP: 3.5018%
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
*journaled_at 2026-05-17T03:54:39.561962Z · journaler v2*
