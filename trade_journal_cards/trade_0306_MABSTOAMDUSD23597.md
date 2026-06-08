# Trade #306 — AMD-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.9219 (+0.887% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.34 min

> Long trailed into profit on AMD-USDT (stoch_rsi, +0.89%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOAMDUSD23597`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `AMD-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T14:19:58.895348+00:00`
- closed: `2026-06-01T14:23:19.089565+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [zscore_reversion,stoch_rsi] — best: StochRSI long stoch=0.67 (was 0.07) rsi=33

### Parsed signal features
- **rsi**: 33.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 490.1688,
  "atr_tp": 502.54679999999996,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 495.12
- exit_price: 499.51
- tp_price: 502.55
- sl_price: 490.17
- qty: 21.0 · notional: 103.9752
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5006
- **planned_sl_distance_pct**: 0.9998
- **planned_r_multiple**: 1.501
- **planned_risk_usd**: 103.95
- **planned_reward_usd**: 156.03
- **realized_r_multiple**: 0.009
- **exit_distance_from_tp_pct**: 0.614
- **exit_distance_from_sl_pct**: 1.8864
- **notional**: 103.9752

### Market excursion (MFE / MAE proxy)
- high_water: 500.21 · low_water: 495.12
- current_stop_at_close: 497.10048
- **mfe_pct**: 1.028
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1414

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.009
- slippage vs planned TP: 0.614%
- slippage vs planned SL: 1.8864%

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
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617957+00:00Z · journaler v2*
