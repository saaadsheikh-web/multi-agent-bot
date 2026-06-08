# Trade #326 — NVDA-USDT short (funding_extremes)

**Outcome:** LOSS · **PnL:** -3.0555 (-3.015% if pct available) · **Decision grade:** A (100/100) · **Hold:** 463.5 min

> Short stopped out at full risk on NVDA-USDT (funding_extremes, -3.01%) trail gave back 3.05% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNNVDAUS80916`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `NVDA-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T06:15:17.840713+00:00`
- closed: `2026-06-02T13:58:48.136255+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [zscore_reversion,funding_extremes] — best: Funding extremes SHORT: fr=0.0502%/8h (annual≈55%), RSI=67, EMA50 slope=+0.39%

### Parsed signal features
- **rsi**: 67.48909718242771
- **atr_pct**: 0.6762389025240666
- **funding_rate**: 0.0005018609724999848
- **ema_slope**: 0.3919518155485191
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.0005018609724999848,
  "rsi": 67.48909718242771,
  "ema_slope": 0.3919518155485191,
  "atr_pct": 0.6762389025240666,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 225.21
- exit_price: 232.0
- tp_price: 216.2
- sl_price: 231.97
- qty: 45.0 · notional: 101.34450000000001
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 4.0007
- **planned_sl_distance_pct**: 3.0016
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 304.2
- **planned_reward_usd**: 405.45
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 7.0157
- **exit_distance_from_sl_pct**: -0.0133
- **notional**: 101.34450000000001

### Market excursion (MFE / MAE proxy)
- high_water: 225.21 · low_water: 225.14
- current_stop_at_close: 231.97
- **mfe_pct**: 0.0311
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 3.046

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.01
- slippage vs planned TP: 7.0157%
- slippage vs planned SL: -0.0133%

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
`confluence`, `trail_too_loose`, `long_hold`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618598+00:00Z · journaler v2*
