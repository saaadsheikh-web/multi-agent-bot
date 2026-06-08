# Trade #251 — BTC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.5369 (+0.508% if pct available) · **Decision grade:** B (85/100) · **Hold:** 240.11 min

> Long trailed into profit on BTC-USDT (stoch_rsi, +0.51%) during dead-zone hour 08:00 UTC [grade B / 85].

## 1 · Identity
- custom_id: `MABSTOBTCUSD55682`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-27T04:21:24.286002+00:00`
- closed: `2026-05-27T08:21:30.722948+00:00` · hour UTC 08 (Wed)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.15 rsi=33

### Parsed signal features
- **rsi**: 33.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 74750.841,
  "atr_tp": 76638.48849999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75502.1
- exit_price: 75885.6
- tp_price: 76638.5
- sl_price: 74750.8
- qty: 1.4 · notional: 105.70294000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5051
- **planned_sl_distance_pct**: 0.9951
- **planned_r_multiple**: 1.513
- **planned_risk_usd**: 1051.82
- **planned_reward_usd**: 1590.96
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 0.9972
- **exit_distance_from_sl_pct**: 1.503
- **notional**: 105.70294000000001

### Market excursion (MFE / MAE proxy)
- high_water: 75972.0 · low_water: 75502.1
- current_stop_at_close: 75592.14
- **mfe_pct**: 0.6224
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1144

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 0.9972%
- slippage vs planned SL: 1.503%

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
`dead_hour`, `long_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-27T11:01:24.788017Z · journaler v2*
