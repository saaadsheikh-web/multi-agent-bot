# Trade #164 — BNB-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0592 (+0.112% if pct available) · **Decision grade:** A (100/100) · **Hold:** 147.28 min

> Short trailed into profit on BNB-USDT (stoch_rsi, +0.11%) during good-zone hour 19:00 UTC trail gave back 0.51% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD84363`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-21T17:26:04.947290+00:00`
- closed: `2026-05-21T19:53:22.029702+00:00` · hour UTC 19 (Thu)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [swing,stoch_rsi] — best: StochRSI short stoch=0.90 rsi=66

### Parsed signal features
- **rsi**: 66.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 665.5597,
  "atr_tp": 649.08545,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 659.09
- exit_price: 658.35
- tp_price: 649.09
- sl_price: 665.56
- qty: 8.0 · notional: 52.7272
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5172
- **planned_sl_distance_pct**: 0.9817
- **planned_r_multiple**: 1.545
- **planned_risk_usd**: 51.76
- **planned_reward_usd**: 80.0
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 1.405
- **exit_distance_from_sl_pct**: 1.0939
- **notional**: 52.7272

### Market excursion (MFE / MAE proxy)
- high_water: 659.09 · low_water: 654.98
- current_stop_at_close: 658.2548999999999
- **mfe_pct**: 0.6236
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5113

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 1.405%
- slippage vs planned SL: 1.0939%

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
`good_hour`, `confluence`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570333Z · journaler v2*
