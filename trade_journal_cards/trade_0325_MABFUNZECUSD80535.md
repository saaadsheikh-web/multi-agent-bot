# Trade #325 — ZEC-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.1634 (-0.156% if pct available) · **Decision grade:** A (100/100) · **Hold:** 73.22 min

> Long gave back gains on trail on ZEC-USDT (funding_extremes, -0.16%) (was up 0.70% before reversing) trail gave back 0.85% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNZECUSD80535`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T06:08:56.698634+00:00`
- closed: `2026-06-02T07:22:09.823596+00:00` · hour UTC 07 (Tue)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0591%/8h (annual≈-65%), RSI=49, EMA50 slope=+0.32%

### Parsed signal features
- **rsi**: 49.44114860820569
- **atr_pct**: 2.3649231587228448
- **funding_rate**: -0.0005914056759546602
- **ema_slope**: 0.31938090548115916
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005914056759546602,
  "rsi": 49.44114860820569,
  "ema_slope": 0.31938090548115916,
  "atr_pct": 2.3649231587228448,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 550.79
- exit_price: 549.93
- tp_price: 572.82
- sl_price: 534.27
- qty: 1.9 · notional: 104.6501
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 3.9997
- **planned_sl_distance_pct**: 2.9993
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 31.388
- **planned_reward_usd**: 41.857
- **realized_r_multiple**: -0.005
- **exit_distance_from_tp_pct**: 4.1558
- **exit_distance_from_sl_pct**: 2.8432
- **notional**: 104.6501

### Market excursion (MFE / MAE proxy)
- high_water: 554.62 · low_water: 550.79
- current_stop_at_close: 550.79
- **mfe_pct**: 0.6954
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8515

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.005
- slippage vs planned TP: 4.1558%
- slippage vs planned SL: 2.8432%

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
  - high confidence (9) lost

## 7 · Tags
`gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618369+00:00Z · journaler v2*
