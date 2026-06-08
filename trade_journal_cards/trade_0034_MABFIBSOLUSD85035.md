# Trade #34 — SOL-USDT short (fibonacci)

**Outcome:** LOSS · **PnL:** -0.3304 (-0.657% if pct available) · **Decision grade:** A (100/100) · **Hold:** 21.5 min

> Short stopped out at full risk on SOL-USDT (fibonacci, -0.66%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFIBSOLUSD85035`
- agent: `fibonacci` · profile: `fibonacci`
- symbol: `SOL-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-05T12:43:56.779064+00:00`
- closed: `2026-05-05T13:05:26.653716+00:00` · hour UTC 13 (Tue)

## 2 · Hypothesis (why we entered)
> FIB short @ 61.8% retrace, RSI 60, vol 1.7x — rejecting in downtrend

### Parsed signal features
- **fib_level**: 0.618
- **swing_high**: 85.88
- **swing_low**: 83.21
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 85.73516309999998,
  "atr_tp": 83.21,
  "fib_level": 0.618,
  "swing_high": 85.88,
  "swing_low": 83.21
}
```

## 3 · Plan vs Execution
- entry_price: 85.18
- exit_price: 85.74
- tp_price: 83.21
- sl_price: 85.74
- qty: 0.59 · notional: 50.2562
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.3127
- **planned_sl_distance_pct**: 0.6574
- **planned_r_multiple**: 3.518
- **planned_risk_usd**: 0.3304
- **planned_reward_usd**: 1.1623
- **realized_r_multiple**: -1.0
- **exit_distance_from_tp_pct**: 2.9702
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 50.2562

### Market excursion (MFE / MAE proxy)
- high_water: 85.18 · low_water: 85.18
- current_stop_at_close: 85.74
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.0
- slippage vs planned TP: 2.9702%
- slippage vs planned SL: 0.0%

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
  - strong planned R:R=3.518
  - high confidence (8) lost

## 7 · Tags
`sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558946Z · journaler v2*
