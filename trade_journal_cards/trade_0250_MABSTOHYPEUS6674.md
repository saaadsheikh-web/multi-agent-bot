# Trade #250 — HYPE-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.1072 (-0.105% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.05 min

> Short gave back gains on trail on HYPE-USDT (stoch_rsi, -0.11%) (was up 0.53% before reversing) trail gave back 0.64% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS6674`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-26T14:44:35.905237+00:00`
- closed: `2026-05-26T14:48:38.748662+00:00` · hour UTC 14 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [vwap_reversion,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=66

### Parsed signal features
- **rsi**: 66.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 64.3976,
  "atr_tp": 62.803599999999996,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 63.757
- exit_price: 63.824
- tp_price: 62.804
- sl_price: 64.398
- qty: 16.0 · notional: 102.0112
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4947
- **planned_sl_distance_pct**: 1.0054
- **planned_r_multiple**: 1.487
- **planned_risk_usd**: 10.256
- **planned_reward_usd**: 15.248
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 1.5998
- **exit_distance_from_sl_pct**: 0.9003
- **notional**: 102.0112

### Market excursion (MFE / MAE proxy)
- high_water: 63.757 · low_water: 63.419
- current_stop_at_close: 63.73609499999999
- **mfe_pct**: 0.5301
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6352

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.01
- slippage vs planned TP: 1.5998%
- slippage vs planned SL: 0.9003%

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
  - high confidence (9) lost

## 7 · Tags
`confluence`, `gave_back_winner`, `trail_too_loose`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-26T15:01:27.129122Z · journaler v2*
