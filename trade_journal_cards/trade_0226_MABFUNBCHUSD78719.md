# Trade #226 — BCH-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +0.9300 (+1.798% if pct available) · **Decision grade:** A (100/100) · **Hold:** 240.17 min

> Long trailed into profit on BCH-USDT (funding_extremes, +1.80%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD78719`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T03:12:00.600295+00:00`
- closed: `2026-05-25T07:12:10.810053+00:00` · hour UTC 07 (Mon)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0501%/8h (annual≈-55%), RSI=39, EMA50 slope=-0.41%

### Parsed signal features
- **rsi**: 39.271647492252924
- **ema_slope**: -0.4118111696448934
- **atr_pct**: 0.8918889989253442
- **funding_rate**: -0.0005010771313710529
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005010771313710529,
  "rsi": 39.271647492252924,
  "ema_slope": -0.4118111696448934,
  "atr_pct": 0.8918889989253442,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 344.8
- exit_price: 351.0
- tp_price: 353.42
- sl_price: 339.63
- qty: 1.5 · notional: 51.720000000000006
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5
- **planned_sl_distance_pct**: 1.4994
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 7.755
- **planned_reward_usd**: 12.93
- **realized_r_multiple**: 0.12
- **exit_distance_from_tp_pct**: 0.7019
- **exit_distance_from_sl_pct**: 3.2976
- **notional**: 51.720000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 351.3 · low_water: 344.8
- current_stop_at_close: 347.78700000000003
- **mfe_pct**: 1.8852
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.087

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.12
- slippage vs planned TP: 0.7019%
- slippage vs planned SL: 3.2976%

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
`long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905833Z · journaler v2*
