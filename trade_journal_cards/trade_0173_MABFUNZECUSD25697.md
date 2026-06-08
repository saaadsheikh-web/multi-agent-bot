# Trade #173 — ZEC-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.0056 (-0.011% if pct available) · **Decision grade:** A (100/100) · **Hold:** 63.61 min

> Long gave back gains on trail on ZEC-USDT (funding_extremes, -0.01%) during good-zone hour 05:00 UTC (was up 0.68% before reversing) trail gave back 0.69% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNZECUSD25697`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-22T04:54:59.189419+00:00`
- closed: `2026-05-22T05:58:35.725660+00:00` · hour UTC 05 (Fri)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0503%/8h (annual≈-55%), RSI=47, EMA50 slope=+0.38%

### Parsed signal features
- **rsi**: 47.03173998708758
- **atr_pct**: 1.650243718361767
- **funding_rate**: -0.0005025582662246732
- **ema_slope**: 0.3802998592612905
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005025582662246732,
  "rsi": 47.03173998708758,
  "ema_slope": 0.3802998592612905,
  "atr_pct": 1.650243718361767,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 653.96
- exit_price: 653.89
- tp_price: 670.31
- sl_price: 644.15
- qty: 0.8 · notional: 52.316800000000015
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5002
- **planned_sl_distance_pct**: 1.5001
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 7.848
- **planned_reward_usd**: 13.08
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.5109
- **exit_distance_from_sl_pct**: 1.4894
- **notional**: 52.316800000000015

### Market excursion (MFE / MAE proxy)
- high_water: 658.38 · low_water: 653.96
- current_stop_at_close: 653.96
- **mfe_pct**: 0.6759
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6866

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.5109%
- slippage vs planned SL: 1.4894%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570460Z · journaler v2*
