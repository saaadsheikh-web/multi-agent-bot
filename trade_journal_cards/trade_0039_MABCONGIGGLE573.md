# Trade #39 — GIGGLE-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.1502 (+2.290% if pct available) · **Decision grade:** A (100/100) · **Hold:** 39.12 min

> Clean short TP hit on GIGGLE-USDT (connors_rsi2, +2.29%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONGIGGLE573`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `GIGGLE-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-05T17:02:54.128294+00:00`
- closed: `2026-05-05T17:42:01.310795+00:00` · hour UTC 17 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 short: RSI2=96.1, in downtrend

### Parsed signal features
- **rsi2**: 96.1
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 35.900549999999996,
  "atr_tp": 34.6626
}
```

## 3 · Plan vs Execution
- entry_price: 35.37
- exit_price: 34.56
- tp_price: 34.66
- sl_price: 35.9
- qty: 142.0 · notional: 50.22539999999999
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0074
- **planned_sl_distance_pct**: 1.4984
- **planned_r_multiple**: 1.34
- **planned_risk_usd**: 75.26
- **planned_reward_usd**: 100.82
- **realized_r_multiple**: 0.015
- **exit_distance_from_tp_pct**: -0.2827
- **exit_distance_from_sl_pct**: 3.7885
- **notional**: 50.22539999999999

### Market excursion (MFE / MAE proxy)
- high_water: 35.37 · low_water: 34.56
- current_stop_at_close: 34.83648
- **mfe_pct**: 2.2901
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.015
- slippage vs planned TP: -0.2827%
- slippage vs planned SL: 3.7885%

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
`confluence`, `short_win`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559082Z · journaler v2*
