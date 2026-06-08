# Trade #245 — HYPE-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +1.6932 (+1.678% if pct available) · **Decision grade:** A (100/100) · **Hold:** 105.15 min

> Clean long TP hit on HYPE-USDT (stoch_rsi, +1.68%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS66563`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-26T03:36:05.661435+00:00`
- closed: `2026-05-26T05:21:14.703295+00:00` · hour UTC 05 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.13 rsi=33

### Parsed signal features
- **rsi**: 33.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 58.74858,
  "atr_tp": 60.23212999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 59.342
- exit_price: 60.338
- tp_price: 60.232
- sl_price: 58.749
- qty: 17.0 · notional: 100.88140000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4998
- **planned_sl_distance_pct**: 0.9993
- **planned_r_multiple**: 1.501
- **planned_risk_usd**: 10.081
- **planned_reward_usd**: 15.13
- **realized_r_multiple**: 0.168
- **exit_distance_from_tp_pct**: -0.1786
- **exit_distance_from_sl_pct**: 2.6777
- **notional**: 100.88140000000001

### Market excursion (MFE / MAE proxy)
- high_water: 60.338 · low_water: 59.342
- current_stop_at_close: 60.03631
- **mfe_pct**: 1.6784
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.168
- slippage vs planned TP: -0.1786%
- slippage vs planned SL: 2.6777%

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
`good_hour`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-26T07:01:11.917177Z · journaler v2*
