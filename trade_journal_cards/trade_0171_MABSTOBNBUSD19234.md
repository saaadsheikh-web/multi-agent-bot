# Trade #171 — BNB-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.4056 (+0.766% if pct available) · **Decision grade:** A (100/100) · **Hold:** 240.06 min

> Short trailed into profit on BNB-USDT (stoch_rsi, +0.77%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD19234`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T03:07:16.101621+00:00`
- closed: `2026-05-22T07:07:19.593137+00:00` · hour UTC 07 (Fri)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=1.00 rsi=67

### Parsed signal features
- **rsi**: 67.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 668.1351999999999,
  "atr_tp": 651.5971999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 661.52
- exit_price: 656.45
- tp_price: 651.6
- sl_price: 668.14
- qty: 8.0 · notional: 52.9216
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4996
- **planned_sl_distance_pct**: 1.0007
- **planned_r_multiple**: 1.499
- **planned_risk_usd**: 52.96
- **planned_reward_usd**: 79.36
- **realized_r_multiple**: 0.008
- **exit_distance_from_tp_pct**: 0.7332
- **exit_distance_from_sl_pct**: 1.7671
- **notional**: 52.9216

### Market excursion (MFE / MAE proxy)
- high_water: 661.52 · low_water: 655.99
- current_stop_at_close: 659.26995
- **mfe_pct**: 0.836
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0695

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.008
- slippage vs planned TP: 0.7332%
- slippage vs planned SL: 1.7671%

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
`long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570510Z · journaler v2*
