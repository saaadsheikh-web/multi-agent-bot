# Trade #52 — DASH-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.3850 (+0.726% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.08 min

> Long trailed into profit on DASH-USDT (connors_rsi2, +0.73%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONDASHUS33318`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `DASH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T02:08:40.031996+00:00`
- closed: `2026-05-06T02:11:44.667446+00:00` · hour UTC 02 (Wed)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=3.5, in uptrend

### Parsed signal features
- **rsi2**: 3.5
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 47.477000000000004,
  "atr_tp": 49.164,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 48.21
- exit_price: 48.56
- tp_price: 49.16
- sl_price: 47.48
- qty: 11.0 · notional: 53.031000000000006
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.9705
- **planned_sl_distance_pct**: 1.5142
- **planned_r_multiple**: 1.301
- **planned_risk_usd**: 8.03
- **planned_reward_usd**: 10.45
- **realized_r_multiple**: 0.048
- **exit_distance_from_tp_pct**: 1.2446
- **exit_distance_from_sl_pct**: 2.2402
- **notional**: 53.031000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 48.5 · low_water: 48.21
- current_stop_at_close: 47.48
- **mfe_pct**: 0.6015
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.1245

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.048
- slippage vs planned TP: 1.2446%
- slippage vs planned SL: 2.2402%

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
`very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559675Z · journaler v2*
