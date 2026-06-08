# Trade #44 — TAO-USDT short (fibonacci)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** B (80/100) · **Hold:** 13.86 min

> Short flat exit (scratch) on TAO-USDT (fibonacci, +0.00%) [flagged-losing-symbol] [grade B / 80].

## 1 · Identity
- custom_id: `MABFIBTAOUSD16857`
- agent: `fibonacci` · profile: `fibonacci`
- symbol: `TAO-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-05T21:34:18.145432+00:00`
- closed: `2026-05-05T21:48:09.662515+00:00` · hour UTC 21 (Tue)

## 2 · Hypothesis (why we entered)
> FIB short @ 61.8% retrace, RSI 56, vol 1.5x — rejecting in downtrend

### Parsed signal features
- **fib_level**: 0.618
- **swing_high**: 295.84
- **swing_low**: 276.29
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 293.11458149999993,
  "atr_tp": 276.29,
  "fib_level": 0.618,
  "swing_high": 295.84,
  "swing_low": 276.29
}
```

## 3 · Plan vs Execution
- entry_price: 289.02
- exit_price: 289.02
- tp_price: 276.29
- sl_price: 293.11
- qty: 18.0 · notional: 52.023599999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 4.4045
- **planned_sl_distance_pct**: 1.4151
- **planned_r_multiple**: 3.113
- **planned_risk_usd**: 73.62
- **planned_reward_usd**: 229.14
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 4.4045
- **exit_distance_from_sl_pct**: 1.4151
- **notional**: 52.023599999999995

### Market excursion (MFE / MAE proxy)
- high_water: 289.02 · low_water: 287.89
- current_stop_at_close: 293.11
- **mfe_pct**: 0.391
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.391

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 4.4045%
- slippage vs planned SL: 1.4151%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - flagged-losing-symbol
  - strong planned R:R=3.113

## 7 · Tags
`losing_symbol`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.559358Z · journaler v2*
