# Trade #31 — XPT-USDT short (fibonacci)

**Outcome:** WIN · **PnL:** +0.7082 (+1.372% if pct available) · **Decision grade:** A (100/100) · **Hold:** 720.19 min

> Short trailed into profit on XPT-USDT (fibonacci, +1.37%) during good-zone hour 19:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABFIBXPTUSD67815`
- agent: `fibonacci` · profile: `fibonacci`
- symbol: `XPT-USDT` · side: `short`
- confidence: 7
- opened: `2026-05-05T07:56:56.326847+00:00`
- closed: `2026-05-05T19:57:07.841923+00:00` · hour UTC 19 (Tue)

## 2 · Hypothesis (why we entered)
> FIB short @ 50.0% retrace, RSI 59, vol 1.3x — rejecting in downtrend

### Parsed signal features
- **fib_level**: 0.5
- **swing_high**: 2022.62
- **swing_low**: 1933.73
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 2013.6155276999998,
  "atr_tp": 1933.73,
  "fib_level": 0.5,
  "swing_high": 2022.62,
  "swing_low": 1933.73
}
```

## 3 · Plan vs Execution
- entry_price: 1985.15
- exit_price: 1957.91
- tp_price: 1933.73
- sl_price: 2013.62
- qty: 26.0 · notional: 51.61390000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.5902
- **planned_sl_distance_pct**: 1.4341
- **planned_r_multiple**: 1.806
- **planned_risk_usd**: 740.22
- **planned_reward_usd**: 1336.92
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 1.218
- **exit_distance_from_sl_pct**: 2.8063
- **notional**: 51.61390000000001

### Market excursion (MFE / MAE proxy)
- high_water: 1985.15 · low_water: 1957.91
- current_stop_at_close: 1969.6574600000001
- **mfe_pct**: 1.3722
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 1.218%
- slippage vs planned SL: 2.8063%

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
  - (no notable factors)

## 7 · Tags
`good_hour`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559178Z · journaler v2*
