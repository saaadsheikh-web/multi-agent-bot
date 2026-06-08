# Trade #259 — BCH-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +0.3960 (+0.394% if pct available) · **Decision grade:** A (100/100) · **Hold:** 99.4 min

> Long trailed into profit on BCH-USDT (funding_extremes, +0.39%) trail gave back 0.89% [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD34753`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-29T06:05:54.772624+00:00`
- closed: `2026-05-29T07:45:18.629558+00:00` · hour UTC 07 (Fri)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0593%/8h (annual≈-65%), RSI=43, EMA50 slope=-0.75%

### Parsed signal features
- **rsi**: 42.600698502140084
- **ema_slope**: -0.7506504709454354
- **atr_pct**: 1.2904616615534248
- **funding_rate**: -0.0005932135142363382
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005932135142363382,
  "rsi": 42.600698502140084,
  "ema_slope": -0.7506504709454354,
  "atr_pct": 1.2904616615534248,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 304.7
- exit_price: 305.9
- tp_price: 312.32
- sl_price: 300.13
- qty: 3.3 · notional: 100.551
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5008
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 15.081
- **planned_reward_usd**: 25.146
- **realized_r_multiple**: 0.026
- **exit_distance_from_tp_pct**: 2.107
- **exit_distance_from_sl_pct**: 1.8937
- **notional**: 100.551

### Market excursion (MFE / MAE proxy)
- high_water: 308.6 · low_water: 304.7
- current_stop_at_close: 305.9188
- **mfe_pct**: 1.2799
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8861

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.026
- slippage vs planned TP: 2.107%
- slippage vs planned SL: 1.8937%

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
  - (no notable factors)

## 7 · Tags
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.616983+00:00Z · journaler v2*
