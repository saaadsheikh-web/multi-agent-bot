# Trade #26 — XPT-USDT short (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 28.14 min

> Short flat exit (scratch) on XPT-USDT (hurst_regime, +0.00%) during good-zone hour 01:00 UTC [killed-agent] [grade A / 95].

## 1 · Identity
- custom_id: `MABHURXPTUSD42171`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `XPT-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-05T00:49:31.937226+00:00`
- closed: `2026-05-05T01:17:40.252150+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime short H=0.924 below EMA21

### Parsed signal features
- **hurst**: 0.9243364367033924
- **atr_val**: 10.054453949510936
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1970.1616809242664,
  "atr_tp": 19.5508,
  "hurst": 0.9243364367033924,
  "atr_val": 10.054453949510936
}
```

## 3 · Plan vs Execution
- entry_price: 1955.19
- exit_price: 1955.19
- tp_price: 19.55
- sl_price: 1970.16
- qty: 26.0 · notional: 50.83494
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0001
- **planned_sl_distance_pct**: 0.7657
- **planned_r_multiple**: 129.294
- **planned_risk_usd**: 389.22
- **planned_reward_usd**: 50326.64
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0001
- **exit_distance_from_sl_pct**: 0.7657
- **notional**: 50.83494

### Market excursion (MFE / MAE proxy)
- high_water: 1955.19 · low_water: 1954.99
- current_stop_at_close: 1970.16
- **mfe_pct**: 0.0102
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0102

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0001%
- slippage vs planned SL: 0.7657%

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
  - strong planned R:R=129.294
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558742Z · journaler v2*
