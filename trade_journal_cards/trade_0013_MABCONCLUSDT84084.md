# Trade #13 — CL-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.0143 (+2.005% if pct available) · **Decision grade:** A (95/100) · **Hold:** 85.67 min

> Clean long TP hit on CL-USDT (connors_rsi2, +2.00%) during dead-zone hour 10:00 UTC [grade A / 95].

## 1 · Identity
- custom_id: `MABCONCLUSDT84084`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `CL-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T08:41:25.750792+00:00`
- closed: `2026-05-04T10:07:06.105101+00:00` · hour UTC 10 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=4.2, in uptrend

### Parsed signal features
- **rsi2**: 4.2
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 101.7111,
  "atr_tp": 105.32520000000001
}
```

## 3 · Plan vs Execution
- entry_price: 103.26
- exit_price: 105.33
- tp_price: 105.32520000000001
- sl_price: 101.7111
- qty: 49.0 · notional: 50.5974
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 75.8961
- **planned_reward_usd**: 101.1948
- **realized_r_multiple**: 0.013
- **exit_distance_from_tp_pct**: -0.0046
- **exit_distance_from_sl_pct**: 3.5046
- **notional**: 50.5974

### Market excursion (MFE / MAE proxy)
- high_water: 105.33 · low_water: 103.26
- current_stop_at_close: 104.48736
- **mfe_pct**: 2.0046
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.013
- slippage vs planned TP: -0.0046%
- slippage vs planned SL: 3.5046%

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
`dead_hour`, `confluence`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558103Z · journaler v2*
