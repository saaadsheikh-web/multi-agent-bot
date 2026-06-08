# Trade #260 — BCH-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.1980 (-0.196% if pct available) · **Decision grade:** B (85/100) · **Hold:** 50.12 min

> Long gave back gains on trail on BCH-USDT (funding_extremes, -0.20%) during dead-zone hour 08:00 UTC (was up 0.95% before reversing) trail gave back 1.14% [grade B / 85].

## 1 · Identity
- custom_id: `MABFUNBCHUSD40770`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-29T07:46:11.583550+00:00`
- closed: `2026-05-29T08:36:19.017583+00:00` · hour UTC 08 (Fri)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0586%/8h (annual≈-64%), RSI=45, EMA50 slope=-0.65%

### Parsed signal features
- **rsi**: 45.11868592913378
- **ema_slope**: -0.6470798612118633
- **atr_pct**: 1.3198028501360293
- **funding_rate**: -0.0005858587517339724
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005858587517339724,
  "rsi": 45.11868592913378,
  "ema_slope": -0.6470798612118633,
  "atr_pct": 1.3198028501360293,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 306.2
- exit_price: 305.6
- tp_price: 313.85
- sl_price: 301.61
- qty: 3.3 · notional: 101.046
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4984
- **planned_sl_distance_pct**: 1.499
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 15.147
- **planned_reward_usd**: 25.245
- **realized_r_multiple**: -0.013
- **exit_distance_from_tp_pct**: 2.6943
- **exit_distance_from_sl_pct**: 1.3031
- **notional**: 101.046

### Market excursion (MFE / MAE proxy)
- high_water: 309.1 · low_water: 306.2
- current_stop_at_close: 306.2
- **mfe_pct**: 0.9471
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.143

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.013
- slippage vs planned TP: 2.6943%
- slippage vs planned SL: 1.3031%

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
  - high confidence (9) lost

## 7 · Tags
`dead_hour`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_B`

---
*journaled_at 2026-06-05T21:57:18.617017+00:00Z · journaler v2*
