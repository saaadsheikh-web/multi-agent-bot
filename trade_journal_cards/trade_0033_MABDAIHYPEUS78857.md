# Trade #33 — HYPE-USDT long (daily_breakout_4h)

**Outcome:** WIN · **PnL:** +0.2604 (+0.496% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.21 min

> Long trailed into profit on HYPE-USDT (daily_breakout_4h, +0.50%) trail gave back 0.57% [grade A / 100].

## 1 · Identity
- custom_id: `MABDAIHYPEUS78857`
- agent: `daily_breakout_4h` · profile: `daily_breakout_4h`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-05T11:00:58.753312+00:00`
- closed: `2026-05-05T17:01:11.286752+00:00` · hour UTC 17 (Tue)

## 2 · Hypothesis (why we entered)
> 4h-high break long (43.2820) vol 1.1x

### Parsed signal features
- **atr_val**: 0.43473267748598254
- **v_ratio**: 1.1437624246042786

### Raw meta from agent
```json
{
  "atr_sl": 43.218084000000005,
  "atr_tp": 87.04857,
  "atr_val": 0.43473267748598254,
  "v_ratio": 1.1437624246042786
}
```

## 3 · Plan vs Execution
- entry_price: 43.723
- exit_price: 43.94
- tp_price: 87.049
- sl_price: 43.218
- qty: 12.0 · notional: 52.467600000000004
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 99.092
- **planned_sl_distance_pct**: 1.155
- **planned_r_multiple**: 85.794
- **planned_risk_usd**: 6.06
- **planned_reward_usd**: 519.912
- **realized_r_multiple**: 0.043
- **exit_distance_from_tp_pct**: 98.5957
- **exit_distance_from_sl_pct**: 1.6513
- **notional**: 52.467600000000004

### Market excursion (MFE / MAE proxy)
- high_water: 44.19 · low_water: 43.723
- current_stop_at_close: 43.218
- **mfe_pct**: 1.0681
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5718

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.043
- slippage vs planned TP: 98.5957%
- slippage vs planned SL: 1.6513%

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
  - strong planned R:R=85.794

## 7 · Tags
`trail_too_loose`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559010Z · journaler v2*
