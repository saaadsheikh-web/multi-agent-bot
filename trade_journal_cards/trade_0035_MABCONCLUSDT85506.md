# Trade #35 — CL-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.0878 (+2.148% if pct available) · **Decision grade:** A (100/100) · **Hold:** 76.86 min

> Clean short TP hit on CL-USDT (connors_rsi2, +2.15%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONCLUSDT85506`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `CL-USDT` · side: `short`
- confidence: 10
- opened: `2026-05-05T12:51:47.139927+00:00`
- closed: `2026-05-05T14:08:38.894078+00:00` · hour UTC 14 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 short: RSI2=95.9, in downtrend

### Parsed signal features
- **rsi2**: 95.9
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 104.90024999999999,
  "atr_tp": 101.28299999999999
}
```

## 3 · Plan vs Execution
- entry_price: 103.35
- exit_price: 101.13
- tp_price: 101.28
- sl_price: 104.9
- qty: 49.0 · notional: 50.64149999999999
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0029
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.335
- **planned_risk_usd**: 75.95
- **planned_reward_usd**: 101.43
- **realized_r_multiple**: 0.014
- **exit_distance_from_tp_pct**: -0.1451
- **exit_distance_from_sl_pct**: 3.6478
- **notional**: 50.64149999999999

### Market excursion (MFE / MAE proxy)
- high_water: 103.35 · low_water: 101.13
- current_stop_at_close: 101.93903999999999
- **mfe_pct**: 2.148
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.014
- slippage vs planned TP: -0.1451%
- slippage vs planned SL: 3.6478%

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
*journaled_at 2026-05-17T03:54:39.558982Z · journaler v2*
