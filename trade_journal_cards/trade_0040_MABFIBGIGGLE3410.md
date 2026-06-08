# Trade #40 — GIGGLE-USDT long (fibonacci)

**Outcome:** WIN · **PnL:** +0.4117 (+0.661% if pct available) · **Decision grade:** A (100/100) · **Hold:** 136.78 min

> Long trailed into profit on GIGGLE-USDT (fibonacci, +0.66%) trail gave back 0.72% [grade A / 100].

## 1 · Identity
- custom_id: `MABFIBGIGGLE3410`
- agent: `fibonacci` · profile: `fibonacci`
- symbol: `GIGGLE-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-05T17:50:11.620786+00:00`
- closed: `2026-05-05T20:06:58.224844+00:00` · hour UTC 20 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [vwap_reversion,fibonacci] — best: FIB long @ 61.8% retrace, RSI 39, vol 2.8x — bouncing in uptrend

### Parsed signal features
- **fib_level**: 0.618
- **swing_high**: 41.04
- **swing_low**: 31.09
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 33.053203499999995,
  "atr_tp": 41.04,
  "fib_level": 0.618,
  "swing_high": 41.04,
  "swing_low": 31.09
}
```

## 3 · Plan vs Execution
- entry_price: 34.8
- exit_price: 35.03
- tp_price: 41.04
- sl_price: 33.05
- qty: 179.0 · notional: 62.291999999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 17.931
- **planned_sl_distance_pct**: 5.0287
- **planned_r_multiple**: 3.566
- **planned_risk_usd**: 313.25
- **planned_reward_usd**: 1116.96
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 17.2701
- **exit_distance_from_sl_pct**: 5.6897
- **notional**: 62.291999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 35.28 · low_water: 34.8
- current_stop_at_close: 35.06832
- **mfe_pct**: 1.3793
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7184

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 17.2701%
- slippage vs planned SL: 5.6897%

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
  - strong planned R:R=3.566
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559230Z · journaler v2*
