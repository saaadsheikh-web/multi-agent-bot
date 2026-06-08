# Trade #80 — ZEC-USDT short (hurst_regime)

**Outcome:** LOSS · **PnL:** -2.0660 (-3.483% if pct available) · **Decision grade:** B (85/100) · **Hold:** 10.08 min

> Short stopped out at full risk on ZEC-USDT (hurst_regime, -3.48%) [killed-agent] trail gave back 3.51% [grade B / 85].

## 1 · Identity
- custom_id: `MABHURZECUSD36160`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-09T14:16:02.551942+00:00`
- closed: `2026-05-09T14:26:07.638836+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> Hurst trend short H=0.950 EMA-dist=0.5ATR ATR%=2.35

### Parsed signal features
- **atr_pct**: 2.35
- **hurst**: 0.9503821684618174
- **atr_val**: 13.915671664402124
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 613.8835074966032,
  "atr_tp": 551.2629850067937,
  "hurst": 0.9503821684618174,
  "atr_val": 13.915671664402124,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 593.22
- exit_price: 613.88
- tp_price: 551.26
- sl_price: 613.88
- qty: 1.0 · notional: 59.322
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 7.0733
- **planned_sl_distance_pct**: 3.4827
- **planned_r_multiple**: 2.031
- **planned_risk_usd**: 20.66
- **planned_reward_usd**: 41.96
- **realized_r_multiple**: -0.1
- **exit_distance_from_tp_pct**: 10.5559
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 59.322

### Market excursion (MFE / MAE proxy)
- high_water: 593.22 · low_water: 593.06
- current_stop_at_close: 613.88
- **mfe_pct**: 0.027
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 3.5097

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.1
- slippage vs planned TP: 10.5559%
- slippage vs planned SL: 0.0%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=2.031
  - high confidence (8) lost

## 7 · Tags
`killed_agent`, `trail_too_loose`, `sl_hit`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.560621Z · journaler v2*
