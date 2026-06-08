# Trade #5 — SOL-USDT long (hurst_regime)

**Outcome:** WIN · **PnL:** +0.2380 (+0.083% if pct available) · **Decision grade:** B (80/100) · **Hold:** 480.13 min

> Long trailed into profit on SOL-USDT (hurst_regime, +0.08%) during dead-zone hour 09:00 UTC [killed-agent] [grade B / 80].

## 1 · Identity
- custom_id: `MABHURSOLUSD86931`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `SOL-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-02T01:55:32.161803+00:00`
- closed: `2026-05-02T09:55:40.089357+00:00` · hour UTC 09 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree [asymmetric,hurst_regime] — best: Hurst trend-regime long H=0.953 above EMA21

### Parsed signal features
- **hurst**: 0.9529472186789534
- **atr_val**: 0.43612998931234226
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 83.3258050160315,
  "atr_tp": 167.1202,
  "hurst": 0.9529472186789534,
  "atr_val": 0.43612998931234226,
  "_paper_only": true
}
```

## 3 · Plan vs Execution
- entry_price: 83.98
- exit_price: 84.05
- tp_price: 167.1202
- sl_price: 83.3258050160315
- qty: 3.4 · notional: 285.532
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0
- **planned_sl_distance_pct**: 0.779
- **planned_r_multiple**: 127.086
- **planned_risk_usd**: 2.2243
- **planned_reward_usd**: 282.6767
- **realized_r_multiple**: 0.107
- **exit_distance_from_tp_pct**: 98.9166
- **exit_distance_from_sl_pct**: 0.8623
- **notional**: 285.532

### Market excursion (MFE / MAE proxy)
- high_water: 84.14 · low_water: 83.98
- current_stop_at_close: 83.3258050160315
- **mfe_pct**: 0.1905
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1072

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.107
- slippage vs planned TP: 98.9166%
- slippage vs planned SL: 0.8623%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: True
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - dead-zone-hour
  - agent-on-kill-list
  - strong planned R:R=127.086
  - multi-agent confluence

## 7 · Tags
`dead_hour`, `killed_agent`, `confluence`, `long_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.557941Z · journaler v2*
