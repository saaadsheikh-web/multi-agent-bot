# Trade #181 — SPY-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0889 (+0.170% if pct available) · **Decision grade:** A (100/100) · **Hold:** 240.17 min

> Short trailed into profit on SPY-USDT (stoch_rsi, +0.17%) during good-zone hour 19:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOSPYUSD62438`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `SPY-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T15:07:20.641683+00:00`
- closed: `2026-05-22T19:07:31.136925+00:00` · hour UTC 19 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=0.97 rsi=67

### Parsed signal features
- **rsi**: 67.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 755.076,
  "atr_tp": 736.386,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 747.59
- exit_price: 746.32
- tp_price: 736.39
- sl_price: 755.08
- qty: 7.0 · notional: 52.331300000000006
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4981
- **planned_sl_distance_pct**: 1.0019
- **planned_r_multiple**: 1.495
- **planned_risk_usd**: 52.43
- **planned_reward_usd**: 78.4
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: 1.3283
- **exit_distance_from_sl_pct**: 1.1718
- **notional**: 52.331300000000006

### Market excursion (MFE / MAE proxy)
- high_water: 747.59 · low_water: 746.1
- current_stop_at_close: 755.08
- **mfe_pct**: 0.1993
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0294

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.002
- slippage vs planned TP: 1.3283%
- slippage vs planned SL: 1.1718%

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
`good_hour`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570668Z · journaler v2*
