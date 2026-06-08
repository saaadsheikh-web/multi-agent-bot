# Trade #328 — XAG-USDT short (stoch_rsi)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 224.47 min

> Short flat exit (scratch) on XAG-USDT (stoch_rsi, +0.00%) trail gave back 0.55% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAGUSD89924`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAG-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T08:45:25.969609+00:00`
- closed: `2026-06-02T12:29:54.052626+00:00` · hour UTC 12 (Tue)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [zscore_reversion,stoch_rsi,metals_scalp] — best: StochRSI short stoch=0.78 (was 1.00) rsi=66

### Parsed signal features
- **rsi**: 66.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 77.4569,
  "atr_tp": 75.53965,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 76.69
- exit_price: 76.69
- tp_price: 75.54
- sl_price: 77.46
- qty: 131.0 · notional: 100.4639
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.4995
- **planned_sl_distance_pct**: 1.004
- **planned_r_multiple**: 1.494
- **planned_risk_usd**: 100.87
- **planned_reward_usd**: 150.65
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4995
- **exit_distance_from_sl_pct**: 1.004
- **notional**: 100.4639

### Market excursion (MFE / MAE proxy)
- high_water: 76.69 · low_water: 76.27
- current_stop_at_close: 76.69
- **mfe_pct**: 0.5477
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5477

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4995%
- slippage vs planned SL: 1.004%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618460+00:00Z · journaler v2*
