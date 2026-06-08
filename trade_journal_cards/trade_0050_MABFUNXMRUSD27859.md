# Trade #50 — XMR-USDT short (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.1339 (-0.252% if pct available) · **Decision grade:** A (100/100) · **Hold:** 41.93 min

> Short gave back gains on trail on XMR-USDT (funding_extremes, -0.25%) during good-zone hour 01:00 UTC (was up 0.63% before reversing) trail gave back 0.88% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNXMRUSD27859`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-06T00:37:41.166023+00:00`
- closed: `2026-05-06T01:19:36.727709+00:00` · hour UTC 01 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [funding,funding_extremes] — best: Funding extremes SHORT: fr=0.1139%/8h (annual≈125%), RSI=50, EMA50 slope=+0.40%

### Parsed signal features
- **rsi**: 50.49312809375501
- **atr_pct**: 1.4429149588277257
- **funding_rate**: 0.001139289786845988
- **ema_slope**: 0.3979454484206446
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.001139289786845988,
  "rsi": 50.49312809375501,
  "ema_slope": 0.3979454484206446,
  "atr_pct": 1.4429149588277257,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 408.32
- exit_price: 409.35
- tp_price: 400.97
- sl_price: 412.4
- qty: 1.3 · notional: 53.0816
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.8001
- **planned_sl_distance_pct**: 0.9992
- **planned_r_multiple**: 1.802
- **planned_risk_usd**: 5.304
- **planned_reward_usd**: 9.555
- **realized_r_multiple**: -0.025
- **exit_distance_from_tp_pct**: 2.0523
- **exit_distance_from_sl_pct**: 0.747
- **notional**: 53.0816

### Market excursion (MFE / MAE proxy)
- high_water: 408.32 · low_water: 405.76
- current_stop_at_close: 409.00608
- **mfe_pct**: 0.627
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8792

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.025
- slippage vs planned TP: 2.0523%
- slippage vs planned SL: 0.747%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence
  - high confidence (8) lost

## 7 · Tags
`good_hour`, `confluence`, `gave_back_winner`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559573Z · journaler v2*
