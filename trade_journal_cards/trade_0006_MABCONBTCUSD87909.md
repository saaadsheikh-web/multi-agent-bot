# Trade #6 — BTC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0050 (+0.002% if pct available) · **Decision grade:** A (100/100) · **Hold:** 120.03 min

> Long trailed into profit on BTC-USDT (connors_rsi2, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBTCUSD87909`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-02T02:11:50.521611+00:00`
- closed: `2026-05-02T04:11:52.171652+00:00` · hour UTC 04 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=3.7, in uptrend

### Parsed signal features
- **rsi2**: 3.7
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 77073.295,
  "atr_tp": 79811.94,
  "_paper_only": true
}
```

## 3 · Plan vs Execution
- entry_price: 78247.0
- exit_price: 78248.4
- tp_price: 79811.94
- sl_price: 77073.295
- qty: 3.6 · notional: 281.6892
- trail_pct: 0.7

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 4225.338
- **planned_reward_usd**: 5633.784
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9982
- **exit_distance_from_sl_pct**: 1.5018
- **notional**: 281.6892

### Market excursion (MFE / MAE proxy)
- high_water: 78499.3 · low_water: 78247.0
- current_stop_at_close: 77073.295
- **mfe_pct**: 0.3224
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3207

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9982%
- slippage vs planned SL: 1.5018%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: True
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.557891Z · journaler v2*
