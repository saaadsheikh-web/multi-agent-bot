# Trade #79 — ZEC-USDT short (hurst_regime)

**Outcome:** WIN · **PnL:** +0.0760 (+0.128% if pct available) · **Decision grade:** B (75/100) · **Hold:** 13.45 min

> Short trailed into profit on ZEC-USDT (hurst_regime, +0.13%) [killed-agent] trail gave back 0.70% [grade B / 75].

## 1 · Identity
- custom_id: `MABHURZECUSD35280`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-09T14:01:22.750929+00:00`
- closed: `2026-05-09T14:14:49.735532+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> Hurst trend short H=0.947 EMA-dist=0.5ATR ATR%=2.45

### Parsed signal features
- **atr_pct**: 2.45
- **hurst**: 0.9468077759044126
- **atr_val**: 14.529890366995058
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 615.1748355504926,
  "atr_tp": 549.7903288990149,
  "hurst": 0.9468077759044126,
  "atr_val": 14.529890366995058,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 593.24
- exit_price: 592.48
- tp_price: 549.79
- sl_price: 615.17
- qty: 1.0 · notional: 59.324000000000005
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 7.3242
- **planned_sl_distance_pct**: 3.6966
- **planned_r_multiple**: 1.981
- **planned_risk_usd**: 21.93
- **planned_reward_usd**: 43.45
- **realized_r_multiple**: 0.003
- **exit_distance_from_tp_pct**: 7.1961
- **exit_distance_from_sl_pct**: 3.8248
- **notional**: 59.324000000000005

### Market excursion (MFE / MAE proxy)
- high_water: 593.24 · low_water: 588.33
- current_stop_at_close: 591.8599800000001
- **mfe_pct**: 0.8277
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6995

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.003
- slippage vs planned TP: 7.1961%
- slippage vs planned SL: 3.8248%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (75/100)
- factors:
  - agent-on-kill-list

## 7 · Tags
`killed_agent`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.560587Z · journaler v2*
