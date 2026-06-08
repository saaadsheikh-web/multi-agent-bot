# Trade #45 — ETH-USDT long (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** C (70/100) · **Hold:** 12.62 min

> Long flat exit (scratch) on ETH-USDT (connors_rsi2, +0.00%) [flagged-losing-symbol] [grade C / 70].

## 1 · Identity
- custom_id: `MABCONETHUSD16931`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ETH-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-05T21:35:32.278935+00:00`
- closed: `2026-05-05T21:48:09.670324+00:00` · hour UTC 21 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.5, in uptrend

### Parsed signal features
- **rsi2**: 4.5
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 2333.9476499999996,
  "atr_tp": 2416.8797999999997
}
```

## 3 · Plan vs Execution
- entry_price: 2368.73
- exit_price: 2368.73
- tp_price: 2416.88
- sl_price: 2333.95
- qty: 2.2 · notional: 52.11206000000001
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0327
- **planned_sl_distance_pct**: 1.4683
- **planned_r_multiple**: 1.384
- **planned_risk_usd**: 76.516
- **planned_reward_usd**: 105.93
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.0327
- **exit_distance_from_sl_pct**: 1.4683
- **notional**: 52.11206000000001

### Market excursion (MFE / MAE proxy)
- high_water: 2372.42 · low_water: 2368.73
- current_stop_at_close: 2333.95
- **mfe_pct**: 0.1558
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1558

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.0327%
- slippage vs planned SL: 1.4683%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol

## 7 · Tags
`losing_symbol`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.559384Z · journaler v2*
