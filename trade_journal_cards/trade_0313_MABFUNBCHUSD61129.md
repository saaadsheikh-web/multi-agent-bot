# Trade #313 — BCH-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.0350 (-0.034% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.77 min

> Long gave back gains on trail on BCH-USDT (funding_extremes, -0.03%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD61129`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T00:45:31.105188+00:00`
- closed: `2026-06-02T00:50:17.195251+00:00` · hour UTC 00 (Tue)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0503%/8h (annual≈-55%), RSI=47, EMA50 slope=-0.26%

### Parsed signal features
- **rsi**: 47.26845081441028
- **ema_slope**: -0.26443149194093074
- **atr_pct**: 1.1331208812735611
- **funding_rate**: -0.0005025089775172528
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005025089775172528,
  "rsi": 47.26845081441028,
  "ema_slope": -0.26443149194093074,
  "atr_pct": 1.1331208812735611,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 290.6
- exit_price: 290.5
- tp_price: 302.22
- sl_price: 281.88
- qty: 3.5 · notional: 101.71000000000002
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 3.9986
- **planned_sl_distance_pct**: 3.0007
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 30.52
- **planned_reward_usd**: 40.67
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 4.033
- **exit_distance_from_sl_pct**: 2.9663
- **notional**: 101.71000000000002

### Market excursion (MFE / MAE proxy)
- high_water: 290.9 · low_water: 290.6
- current_stop_at_close: 281.88
- **mfe_pct**: 0.1032
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1376

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 4.033%
- slippage vs planned SL: 2.9663%

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
`good_hour`, `very_short_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618153+00:00Z · journaler v2*
