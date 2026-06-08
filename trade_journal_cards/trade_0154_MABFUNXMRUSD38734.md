# Trade #154 — XMR-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.2015 (+0.383% if pct available) · **Decision grade:** B (85/100) · **Hold:** 203.97 min

> Short trailed into profit on XMR-USDT (funding_extremes, +0.38%) during dead-zone hour 08:00 UTC trail gave back 1.02% [grade B / 85].

## 1 · Identity
- custom_id: `MABFUNXMRUSD38734`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-21T04:45:36.384827+00:00`
- closed: `2026-05-21T08:09:34.812071+00:00` · hour UTC 08 (Thu)

## 2 · Hypothesis (why we entered)
> Funding extremes SHORT: fr=0.0511%/8h (annual≈56%), RSI=56, EMA50 slope=+0.38%

### Parsed signal features
- **rsi**: 55.998523918613685
- **atr_pct**: 1.2377740077661228
- **funding_rate**: 0.0005112151248723752
- **ema_slope**: 0.3806690940129531
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": 0.0005112151248723752,
  "rsi": 55.998523918613685,
  "ema_slope": 0.3806690940129531,
  "atr_pct": 1.2377740077661228,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 404.35
- exit_price: 402.8
- tp_price: 394.24
- sl_price: 410.42
- qty: 1.3 · notional: 52.56550000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5003
- **planned_sl_distance_pct**: 1.5012
- **planned_r_multiple**: 1.666
- **planned_risk_usd**: 7.891
- **planned_reward_usd**: 13.143
- **realized_r_multiple**: 0.026
- **exit_distance_from_tp_pct**: 2.117
- **exit_distance_from_sl_pct**: 1.8845
- **notional**: 52.56550000000001

### Market excursion (MFE / MAE proxy)
- high_water: 404.35 · low_water: 398.69
- current_stop_at_close: 402.73260000000005
- **mfe_pct**: 1.3998
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0164

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.026
- slippage vs planned TP: 2.117%
- slippage vs planned SL: 1.8845%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-23T15:00:56.570167Z · journaler v2*
