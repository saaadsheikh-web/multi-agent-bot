# Trade #155 — BNB-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0368 (+0.070% if pct available) · **Decision grade:** B (85/100) · **Hold:** 185.85 min

> Short trailed into profit on BNB-USDT (stoch_rsi, +0.07%) during dead-zone hour 08:00 UTC trail gave back 0.51% [grade B / 85].

## 1 · Identity
- custom_id: `MABSTOBNBUSD39381`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-21T04:56:22.984565+00:00`
- closed: `2026-05-21T08:02:13.689119+00:00` · hour UTC 08 (Thu)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=0.85 rsi=68

### Parsed signal features
- **rsi**: 68.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 661.2571,
  "atr_tp": 644.88935,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 654.71
- exit_price: 654.25
- tp_price: 644.89
- sl_price: 661.26
- qty: 8.0 · notional: 52.3768
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4999
- **planned_sl_distance_pct**: 1.0004
- **planned_r_multiple**: 1.499
- **planned_risk_usd**: 52.4
- **planned_reward_usd**: 78.56
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 1.4296
- **exit_distance_from_sl_pct**: 1.0707
- **notional**: 52.3768

### Market excursion (MFE / MAE proxy)
- high_water: 654.71 · low_water: 650.92
- current_stop_at_close: 654.1745999999999
- **mfe_pct**: 0.5789
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5086

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 1.4296%
- slippage vs planned SL: 1.0707%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-23T15:00:56.569893Z · journaler v2*
