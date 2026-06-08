# Trade #204 — BCH-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +0.0150 (+0.028% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.41 min

> Long timed out in profit on BCH-USDT (funding_extremes, +0.03%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD97802`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 6
- opened: `2026-05-24T04:43:24.311919+00:00`
- closed: `2026-05-24T04:46:48.783841+00:00` · hour UTC 04 (Sun)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0589%/8h (annual≈-64%), RSI=47, EMA50 slope=-0.31%

### Parsed signal features
- **rsi**: 46.66877130950322
- **ema_slope**: -0.3072860681216705
- **atr_pct**: 0.8435690844807662
- **funding_rate**: -0.0005889942694418056
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005889942694418056,
  "rsi": 46.66877130950322,
  "ema_slope": -0.3072860681216705,
  "atr_pct": 0.8435690844807662,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 354.7
- exit_price: 354.8
- tp_price: 363.57
- sl_price: 349.38
- qty: 1.5 · notional: 53.205000000000005
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5007
- **planned_sl_distance_pct**: 1.4999
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 7.98
- **planned_reward_usd**: 13.305
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: 2.4725
- **exit_distance_from_sl_pct**: 1.5281
- **notional**: 53.205000000000005

### Market excursion (MFE / MAE proxy)
- high_water: 355.0 · low_water: 354.7
- current_stop_at_close: 349.38
- **mfe_pct**: 0.0846
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0564

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.002
- slippage vs planned TP: 2.4725%
- slippage vs planned SL: 1.5281%

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
`very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905434Z · journaler v2*
