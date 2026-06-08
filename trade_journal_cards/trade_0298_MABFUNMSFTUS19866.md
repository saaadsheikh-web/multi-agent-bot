# Trade #298 — MSFT-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.6754 (+0.662% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.99 min

> Short trailed into profit on MSFT-USDT (funding_extremes, +0.66%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNMSFTUS19866`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `MSFT-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T13:17:48.153194+00:00`
- closed: `2026-06-01T13:24:47.788460+00:00` · hour UTC 13 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [funding,funding_extremes] — best: Funding extremes SHORT: fr=0.0888%/8h (annual≈97%), RSI=52, EMA50 slope=+0.26%

### Parsed signal features
- **rsi**: 52.45952965904668
- **atr_pct**: 0.7312741560841685
- **funding_rate**: 0.0008877201175224036
- **ema_slope**: 0.2568266377049211
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.0008877201175224036,
  "rsi": 52.45952965904668,
  "ema_slope": 0.2568266377049211,
  "atr_pct": 0.7312741560841685,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 464.04
- exit_price: 460.97
- tp_price: 445.48
- sl_price: 477.96
- qty: 22.0 · notional: 102.0888
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 3.9997
- **planned_sl_distance_pct**: 2.9997
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 306.24
- **planned_reward_usd**: 408.32
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: 3.3381
- **exit_distance_from_sl_pct**: 3.6613
- **notional**: 102.0888

### Market excursion (MFE / MAE proxy)
- high_water: 464.04 · low_water: 460.97
- current_stop_at_close: 464.04
- **mfe_pct**: 0.6616
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.002
- slippage vs planned TP: 3.3381%
- slippage vs planned SL: 3.6613%

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

## 7 · Tags
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617780+00:00Z · journaler v2*
