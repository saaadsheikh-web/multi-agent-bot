# Trade #246 — ZEC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0850 (+0.080% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.62 min

> Long timed out in profit on ZEC-USDT (stoch_rsi, +0.08%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD70643`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-26T04:44:04.697814+00:00`
- closed: `2026-05-26T04:47:41.812560+00:00` · hour UTC 04 (Tue)

## 2 · Hypothesis (why we entered)
> [trend-2] StochRSI long stoch=0.09 rsi=31

### Parsed signal features
- **rsi**: 31.0
- **trend_score**: -2
- **trend_dir**: DOWN

### Raw meta from agent
```json
{
  "atr_sl": 615.285,
  "atr_tp": 630.8225,
  "_trend_score": -2,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 621.5
- exit_price: 622.0
- tp_price: 630.82
- sl_price: 615.28
- qty: 1.7 · notional: 105.655
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4996
- **planned_sl_distance_pct**: 1.0008
- **planned_r_multiple**: 1.498
- **planned_risk_usd**: 10.574
- **planned_reward_usd**: 15.844
- **realized_r_multiple**: 0.008
- **exit_distance_from_tp_pct**: 1.4191
- **exit_distance_from_sl_pct**: 1.0813
- **notional**: 105.655

### Market excursion (MFE / MAE proxy)
- high_water: 622.11 · low_water: 621.5
- current_stop_at_close: 615.28
- **mfe_pct**: 0.0981
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0177

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.008
- slippage vs planned TP: 1.4191%
- slippage vs planned SL: 1.0813%

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
`very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-26T07:01:11.917161Z · journaler v2*
