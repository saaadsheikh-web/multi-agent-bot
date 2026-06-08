# Trade #64 — XMR-USDT short (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.0403 (-0.075% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.23 min

> Short closed in the red without clean exit on XMR-USDT (funding_extremes, -0.07%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNXMRUSD35709`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-07T06:35:10.259521+00:00`
- closed: `2026-05-07T06:41:23.969505+00:00` · hour UTC 06 (Thu)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [funding,funding_extremes] — best: Funding extremes SHORT: fr=0.1004%/8h (annual≈110%), RSI=52, EMA50 slope=-0.01%

### Parsed signal features
- **rsi**: 51.694491776283066
- **ema_slope**: -0.013177433751365708
- **atr_pct**: 1.586794472450069
- **funding_rate**: 0.0010040280403348393
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.0010040280403348393,
  "rsi": 51.694491776283066,
  "ema_slope": -0.013177433751365708,
  "atr_pct": 1.586794472450069,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 414.99
- exit_price: 415.3
- tp_price: 404.62
- sl_price: 421.21
- qty: 1.3 · notional: 53.9487
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4989
- **planned_sl_distance_pct**: 1.4988
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 8.086
- **planned_reward_usd**: 13.481
- **realized_r_multiple**: -0.005
- **exit_distance_from_tp_pct**: 2.5736
- **exit_distance_from_sl_pct**: 1.4241
- **notional**: 53.9487

### Market excursion (MFE / MAE proxy)
- high_water: 414.99 · low_water: 414.88
- current_stop_at_close: 421.21
- **mfe_pct**: 0.0265
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1012

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.005
- slippage vs planned TP: 2.5736%
- slippage vs planned SL: 1.4241%

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
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560055Z · journaler v2*
