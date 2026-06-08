# Trade #289 — MSFT-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.3740 (+0.366% if pct available) · **Decision grade:** A (95/100) · **Hold:** 225.8 min

> Short trailed into profit on MSFT-USDT (funding_extremes, +0.37%) during dead-zone hour 08:00 UTC trail gave back 0.83% [grade A / 95].

## 1 · Identity
- custom_id: `MABFUNMSFTUS88312`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `MSFT-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T04:31:54.017564+00:00`
- closed: `2026-06-01T08:17:42.280373+00:00` · hour UTC 08 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [funding,funding_extremes] — best: Funding extremes SHORT: fr=0.1147%/8h (annual≈126%), RSI=62, EMA50 slope=+0.17%

### Parsed signal features
- **rsi**: 61.577534778454044
- **atr_pct**: 0.5690505113357545
- **funding_rate**: 0.0011465404520439918
- **ema_slope**: 0.16506760087564576
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.0011465404520439918,
  "rsi": 61.577534778454044,
  "ema_slope": 0.16506760087564576,
  "atr_pct": 0.5690505113357545,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 464.43
- exit_price: 462.73
- tp_price: 452.82
- sl_price: 471.4
- qty: 22.0 · notional: 102.1746
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4998
- **planned_sl_distance_pct**: 1.5008
- **planned_r_multiple**: 1.666
- **planned_risk_usd**: 153.34
- **planned_reward_usd**: 255.42
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: 2.1338
- **exit_distance_from_sl_pct**: 1.8668
- **notional**: 102.1746

### Market excursion (MFE / MAE proxy)
- high_water: 464.43 · low_water: 458.88
- current_stop_at_close: 462.57228
- **mfe_pct**: 1.195
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.829

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.002
- slippage vs planned TP: 2.1338%
- slippage vs planned SL: 1.8668%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - dead-zone-hour
  - multi-agent confluence

## 7 · Tags
`dead_hour`, `confluence`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617688+00:00Z · journaler v2*
