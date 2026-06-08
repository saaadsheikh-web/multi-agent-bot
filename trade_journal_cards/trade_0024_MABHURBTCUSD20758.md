# Trade #24 — BTC-USDT long (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 26.52 min

> Long flat exit (scratch) on BTC-USDT (hurst_regime, +0.00%) during good-zone hour 19:00 UTC [killed-agent] [grade A / 95].

## 1 · Identity
- custom_id: `MABHURBTCUSD20758`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `BTC-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T18:52:39.008686+00:00`
- closed: `2026-05-04T19:19:10.471777+00:00` · hour UTC 19 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime long H=0.944 above EMA21

### Parsed signal features
- **hurst**: 0.943740036740148
- **atr_val**: 630.3838623015273
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 79120.82420654771,
  "atr_tp": 159332.136,
  "hurst": 0.943740036740148,
  "atr_val": 630.3838623015273
}
```

## 3 · Plan vs Execution
- entry_price: 80051.3
- exit_price: 80051.3
- tp_price: 159332.136
- sl_price: 79120.82420654771
- qty: 0.7 · notional: 56.03591
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0375
- **planned_sl_distance_pct**: 1.1623
- **planned_r_multiple**: 85.208
- **planned_risk_usd**: 651.3331
- **planned_reward_usd**: 55496.5852
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0375
- **exit_distance_from_sl_pct**: 1.1623
- **notional**: 56.03591

### Market excursion (MFE / MAE proxy)
- high_water: 80118.3 · low_water: 80051.3
- current_stop_at_close: 79120.82420654771
- **mfe_pct**: 0.0837
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0837

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0375%
- slippage vs planned SL: 1.1623%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=85.208
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558669Z · journaler v2*
