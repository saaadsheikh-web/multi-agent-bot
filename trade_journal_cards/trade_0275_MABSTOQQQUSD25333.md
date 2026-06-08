# Trade #275 — QQQ-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0042 (+0.004% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.63 min

> Short timed out in profit on QQQ-USDT (stoch_rsi, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOQQQUSD25333`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `QQQ-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-30T07:15:34.386914+00:00`
- closed: `2026-05-30T07:22:12.212889+00:00` · hour UTC 07 (Sat)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=0.91 rsi=65

### Parsed signal features
- **rsi**: 65.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 748.1777,
  "atr_tp": 729.65845,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 740.77
- exit_price: 740.74
- tp_price: 729.66
- sl_price: 748.18
- qty: 14.0 · notional: 103.7078
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4998
- **planned_sl_distance_pct**: 1.0003
- **planned_r_multiple**: 1.499
- **planned_risk_usd**: 103.74
- **planned_reward_usd**: 155.54
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4957
- **exit_distance_from_sl_pct**: 1.0044
- **notional**: 103.7078

### Market excursion (MFE / MAE proxy)
- high_water: 740.77 · low_water: 740.68
- current_stop_at_close: 748.18
- **mfe_pct**: 0.0121
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0081

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4957%
- slippage vs planned SL: 1.0044%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`short_win`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617353+00:00Z · journaler v2*
