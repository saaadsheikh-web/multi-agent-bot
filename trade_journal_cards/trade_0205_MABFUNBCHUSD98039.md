# Trade #205 — BCH-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.1545 (-0.290% if pct available) · **Decision grade:** B (75/100) · **Hold:** 399.24 min

> Long closed in the red without clean exit on BCH-USDT (funding_extremes, -0.29%) during dead-zone hour 11:00 UTC [grade B / 75].

## 1 · Identity
- custom_id: `MABFUNBCHUSD98039`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 6
- opened: `2026-05-24T04:47:22.431212+00:00`
- closed: `2026-05-24T11:26:36.603208+00:00` · hour UTC 11 (Sun)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0563%/8h (annual≈-62%), RSI=46, EMA50 slope=-0.31%

### Parsed signal features
- **rsi**: 46.43019725130262
- **ema_slope**: -0.30836941215810487
- **atr_pct**: 0.8438068435237426
- **funding_rate**: -0.0005633693192340197
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005633693192340197,
  "rsi": 46.43019725130262,
  "ema_slope": -0.30836941215810487,
  "atr_pct": 0.8438068435237426,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 354.8
- exit_price: 353.77
- tp_price: 363.67
- sl_price: 349.48
- qty: 1.5 · notional: 53.22000000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5
- **planned_sl_distance_pct**: 1.4994
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 7.98
- **planned_reward_usd**: 13.305
- **realized_r_multiple**: -0.019
- **exit_distance_from_tp_pct**: 2.7903
- **exit_distance_from_sl_pct**: 1.2091
- **notional**: 53.22000000000001

### Market excursion (MFE / MAE proxy)
- high_water: 354.8 · low_water: 354.8
- current_stop_at_close: 349.48
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.019
- slippage vs planned TP: 2.7903%
- slippage vs planned SL: 1.2091%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (75/100)
- factors:
  - dead-zone-hour
  - timed-out loser (no clean exit signal)

## 7 · Tags
`dead_hour`, `long_hold`, `long_loss`, `time_or_manual`, `grade_B`

---
*journaled_at 2026-05-25T23:01:34.905522Z · journaler v2*
