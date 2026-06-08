# Trade #255 — ZEC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.2166 (+0.206% if pct available) · **Decision grade:** A (100/100) · **Hold:** 23.04 min

> Long trailed into profit on ZEC-USDT (stoch_rsi, +0.21%) during good-zone hour 19:00 UTC trail gave back 0.52% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD8191`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-27T18:56:33.221658+00:00`
- closed: `2026-05-27T19:19:35.734832+00:00` · hour UTC 19 (Wed)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [swing,bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.08 rsi=31

### Parsed signal features
- **rsi**: 31.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 546.5790000000001,
  "atr_tp": 560.3815,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 552.06
- exit_price: 553.2
- tp_price: 560.38
- sl_price: 546.58
- qty: 1.9 · notional: 104.89139999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5071
- **planned_sl_distance_pct**: 0.9926
- **planned_r_multiple**: 1.518
- **planned_risk_usd**: 10.412
- **planned_reward_usd**: 15.808
- **realized_r_multiple**: 0.021
- **exit_distance_from_tp_pct**: 1.3006
- **exit_distance_from_sl_pct**: 1.1991
- **notional**: 104.89139999999999

### Market excursion (MFE / MAE proxy)
- high_water: 556.05 · low_water: 552.06
- current_stop_at_close: 553.2697499999999
- **mfe_pct**: 0.7227
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5162

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.021
- slippage vs planned TP: 1.3006%
- slippage vs planned SL: 1.1991%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`good_hour`, `confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-27T23:00:45.862769Z · journaler v2*
