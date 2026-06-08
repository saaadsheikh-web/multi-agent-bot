# Trade #324 — NVDA-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.0450 (+0.044% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.04 min

> Short trailed into profit on NVDA-USDT (funding_extremes, +0.04%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNNVDAUS80442`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `NVDA-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T06:07:23.692643+00:00`
- closed: `2026-06-02T06:13:25.833781+00:00` · hour UTC 06 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [zscore_reversion,funding_extremes] — best: Funding extremes SHORT: fr=0.0508%/8h (annual≈56%), RSI=68, EMA50 slope=+0.39%

### Parsed signal features
- **rsi**: 68.09556186770676
- **atr_pct**: 0.668647224244764
- **funding_rate**: 0.0005078514054619001
- **ema_slope**: 0.3937437281653411
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.0005078514054619001,
  "rsi": 68.09556186770676,
  "ema_slope": 0.3937437281653411,
  "atr_pct": 0.668647224244764,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 225.31
- exit_price: 225.21
- tp_price: 216.3
- sl_price: 232.07
- qty: 45.0 · notional: 101.3895
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 3.9989
- **planned_sl_distance_pct**: 3.0003
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 304.2
- **planned_reward_usd**: 405.45
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 3.9546
- **exit_distance_from_sl_pct**: 3.0447
- **notional**: 101.3895

### Market excursion (MFE / MAE proxy)
- high_water: 225.31 · low_water: 225.01
- current_stop_at_close: 232.07
- **mfe_pct**: 0.1331
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0888

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 3.9546%
- slippage vs planned SL: 3.0447%

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
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618342+00:00Z · journaler v2*
