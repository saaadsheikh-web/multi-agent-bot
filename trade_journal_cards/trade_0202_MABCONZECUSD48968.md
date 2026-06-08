# Trade #202 — ZEC-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -1.0044 (-1.857% if pct available) · **Decision grade:** A (100/100) · **Hold:** 89.15 min

> Short stopped out at full risk on ZEC-USDT (connors_rsi2, -1.86%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD48968`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T15:09:30.148230+00:00`
- closed: `2026-05-23T16:38:39.439604+00:00` · hour UTC 16 (Sat)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 short: RSI2=95.8, ATR%=0.56, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.8
- **atr_pct**: 0.56
- **trend_score**: -3
- **trend_dir**: DOWN
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 610.5630999999998,
  "atr_tp": 589.5092,
  "_trend_score": -3,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 600.96
- exit_price: 612.12
- tp_price: 589.51
- sl_price: 610.56
- qty: 0.9 · notional: 54.08640000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9053
- **planned_sl_distance_pct**: 1.5974
- **planned_r_multiple**: 1.193
- **planned_risk_usd**: 8.64
- **planned_reward_usd**: 10.305
- **realized_r_multiple**: -0.116
- **exit_distance_from_tp_pct**: 3.7623
- **exit_distance_from_sl_pct**: -0.2596
- **notional**: 54.08640000000001

### Market excursion (MFE / MAE proxy)
- high_water: 600.96 · low_water: 600.96
- current_stop_at_close: 610.56
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.116
- slippage vs planned TP: 3.7623%
- slippage vs planned SL: -0.2596%

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
  - high confidence (9) lost

## 7 · Tags
`sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905326Z · journaler v2*
