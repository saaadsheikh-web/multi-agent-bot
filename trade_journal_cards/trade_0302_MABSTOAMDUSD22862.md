# Trade #302 — AMD-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.6573 (+0.636% if pct available) · **Decision grade:** A (100/100) · **Hold:** 10.4 min

> Long trailed into profit on AMD-USDT (stoch_rsi, +0.64%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOAMDUSD22862`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `AMD-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T14:07:43.970129+00:00`
- closed: `2026-06-01T14:18:08.117531+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [zscore_reversion,stoch_rsi] — best: StochRSI long stoch=0.41 (was 0.07) rsi=28

### Parsed signal features
- **rsi**: 28.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 487.2285,
  "atr_tp": 499.5322499999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 491.84
- exit_price: 494.97
- tp_price: 499.53
- sl_price: 487.23
- qty: 21.0 · notional: 103.28639999999999
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5635
- **planned_sl_distance_pct**: 0.9373
- **planned_r_multiple**: 1.668
- **planned_risk_usd**: 96.81
- **planned_reward_usd**: 161.49
- **realized_r_multiple**: 0.007
- **exit_distance_from_tp_pct**: 0.9271
- **exit_distance_from_sl_pct**: 1.5737
- **notional**: 103.28639999999999

### Market excursion (MFE / MAE proxy)
- high_water: 494.97 · low_water: 491.84
- current_stop_at_close: 491.84
- **mfe_pct**: 0.6364
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.007
- slippage vs planned TP: 0.9271%
- slippage vs planned SL: 1.5737%

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
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617892+00:00Z · journaler v2*
