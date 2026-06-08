# Trade #29 — XAG-USDT short (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 11.81 min

> Short flat exit (scratch) on XAG-USDT (hurst_regime, +0.00%) during good-zone hour 01:00 UTC [killed-agent] [grade A / 95].

## 1 · Identity
- custom_id: `MABHURXAGUSD43150`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `XAG-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-05T01:05:51.472261+00:00`
- closed: `2026-05-05T01:17:40.303097+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime short H=0.950 below EMA21

### Parsed signal features
- **hurst**: 0.9498605144538865
- **atr_val**: 0.47601468524907337
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 73.7340220278736,
  "atr_tp": 0.7302,
  "hurst": 0.9498605144538865,
  "atr_val": 0.47601468524907337
}
```

## 3 · Plan vs Execution
- entry_price: 73.02
- exit_price: 73.02
- tp_price: 0.73
- sl_price: 73.73
- qty: 69.0 · notional: 50.3838
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0003
- **planned_sl_distance_pct**: 0.9723
- **planned_r_multiple**: 101.821
- **planned_risk_usd**: 48.99
- **planned_reward_usd**: 4988.01
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0003
- **exit_distance_from_sl_pct**: 0.9723
- **notional**: 50.3838

### Market excursion (MFE / MAE proxy)
- high_water: 73.02 · low_water: 72.96
- current_stop_at_close: 73.73
- **mfe_pct**: 0.0822
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0822

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0003%
- slippage vs planned SL: 0.9723%

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
  - strong planned R:R=101.821
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558849Z · journaler v2*
