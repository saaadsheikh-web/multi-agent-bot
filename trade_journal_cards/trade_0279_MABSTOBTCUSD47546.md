# Trade #279 — BTC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0626 (+0.061% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.87 min

> Long timed out in profit on BTC-USDT (stoch_rsi, +0.06%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBTCUSD47546`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-31T17:12:28.070158+00:00`
- closed: `2026-05-31T17:15:20.317775+00:00` · hour UTC 17 (Sun)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=35

### Parsed signal features
- **rsi**: 35.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 72709.857,
  "atr_tp": 74545.9645,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 73444.3
- exit_price: 73489.0
- tp_price: 74546.0
- sl_price: 72709.9
- qty: 1.4 · notional: 102.82202000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5
- **planned_sl_distance_pct**: 0.9999
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1028.16
- **planned_reward_usd**: 1542.38
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4392
- **exit_distance_from_sl_pct**: 1.0608
- **notional**: 102.82202000000001

### Market excursion (MFE / MAE proxy)
- high_water: 73490.0 · low_water: 73444.3
- current_stop_at_close: 72709.9
- **mfe_pct**: 0.0622
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0014

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4392%
- slippage vs planned SL: 1.0608%

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
*journaled_at 2026-06-05T21:57:18.617415+00:00Z · journaler v2*
