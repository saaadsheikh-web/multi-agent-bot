# Trade #42 — TAO-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.1134 (-0.222% if pct available) · **Decision grade:** B (80/100) · **Hold:** 19.1 min

> Short gave back gains on trail on TAO-USDT (connors_rsi2, -0.22%) during good-zone hour 19:00 UTC [flagged-losing-symbol] [grade B / 80].

## 1 · Identity
- custom_id: `MABCONTAOUSD8286`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `TAO-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-05T19:11:27.852697+00:00`
- closed: `2026-05-05T19:30:33.991715+00:00` · hour UTC 19 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 short: RSI2=95.5, in downtrend

### Parsed signal features
- **rsi2**: 95.5
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 288.3006,
  "atr_tp": 278.3592
}
```

## 3 · Plan vs Execution
- entry_price: 284.04
- exit_price: 284.67
- tp_price: 278.36
- sl_price: 288.3
- qty: 18.0 · notional: 51.1272
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.9997
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 76.68
- **planned_reward_usd**: 102.24
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.2215
- **exit_distance_from_sl_pct**: 1.278
- **notional**: 51.1272

### Market excursion (MFE / MAE proxy)
- high_water: 284.04 · low_water: 283.38
- current_stop_at_close: 288.3
- **mfe_pct**: 0.2324
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4542

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.2215%
- slippage vs planned SL: 1.278%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - flagged-losing-symbol
  - multi-agent confluence
  - high confidence (10) lost

## 7 · Tags
`good_hour`, `losing_symbol`, `confluence`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.559146Z · journaler v2*
