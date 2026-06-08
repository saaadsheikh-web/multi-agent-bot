# Trade #247 — ZEC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.2941 (+0.278% if pct available) · **Decision grade:** A (100/100) · **Hold:** 55.14 min

> Long trailed into profit on ZEC-USDT (stoch_rsi, +0.28%) during good-zone hour 05:00 UTC trail gave back 0.51% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD71030`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-26T04:50:31.587739+00:00`
- closed: `2026-05-26T05:45:39.847193+00:00` · hour UTC 05 (Tue)

## 2 · Hypothesis (why we entered)
> [trend-2] StochRSI long stoch=0.10 rsi=32

### Parsed signal features
- **rsi**: 32.0
- **trend_score**: -2
- **trend_dir**: DOWN

### Raw meta from agent
```json
{
  "atr_sl": 615.6315000000001,
  "atr_tp": 631.17775,
  "_trend_score": -2,
  "_trend_dir": "DOWN"
}
```

## 3 · Plan vs Execution
- entry_price: 622.04
- exit_price: 623.77
- tp_price: 631.18
- sl_price: 615.63
- qty: 1.7 · notional: 105.74680000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4694
- **planned_sl_distance_pct**: 1.0305
- **planned_r_multiple**: 1.426
- **planned_risk_usd**: 10.897
- **planned_reward_usd**: 15.538
- **realized_r_multiple**: 0.027
- **exit_distance_from_tp_pct**: 1.1912
- **exit_distance_from_sl_pct**: 1.3086
- **notional**: 105.74680000000001

### Market excursion (MFE / MAE proxy)
- high_water: 626.92 · low_water: 622.04
- current_stop_at_close: 623.7854
- **mfe_pct**: 0.7845
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5064

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.027
- slippage vs planned TP: 1.1912%
- slippage vs planned SL: 1.3086%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`good_hour`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-26T07:01:11.917194Z · journaler v2*
