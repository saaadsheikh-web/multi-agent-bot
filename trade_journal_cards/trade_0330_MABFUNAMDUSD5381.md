# Trade #330 — AMD-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.0800 (+0.079% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.04 min

> Short trailed into profit on AMD-USDT (funding_extremes, +0.08%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNAMDUSD5381`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `AMD-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-02T13:03:02.915104+00:00`
- closed: `2026-06-02T13:05:05.531355+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> Funding extremes SHORT: fr=0.0640%/8h (annual≈70%), RSI=50, EMA50 slope=-0.14%

### Parsed signal features
- **rsi**: 50.29418205852495
- **ema_slope**: -0.13941356473891053
- **atr_pct**: 0.9271173045996024
- **funding_rate**: 0.0006395709202743192
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": 0.0006395709202743192,
  "rsi": 50.29418205852495,
  "ema_slope": -0.13941356473891053,
  "atr_pct": 0.9271173045996024,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 506.34
- exit_price: 505.94
- tp_price: 486.09
- sl_price: 521.53
- qty: 20.0 · notional: 101.268
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 3.9993
- **planned_sl_distance_pct**: 3.0
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 303.8
- **planned_reward_usd**: 405.0
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 3.9203
- **exit_distance_from_sl_pct**: 3.079
- **notional**: 101.268

### Market excursion (MFE / MAE proxy)
- high_water: 506.34 · low_water: 505.75
- current_stop_at_close: 521.53
- **mfe_pct**: 0.1165
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0375

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 3.9203%
- slippage vs planned SL: 3.079%

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
`very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618487+00:00Z · journaler v2*
