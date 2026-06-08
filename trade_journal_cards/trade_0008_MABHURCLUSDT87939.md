# Trade #8 — CL-USDT short (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** C (70/100) · **Hold:** 480.1 min

> Short flat exit (scratch) on CL-USDT (hurst_regime, +0.00%) during dead-zone hour 10:00 UTC [killed-agent] [grade C / 70].

## 1 · Identity
- custom_id: `MABHURCLUSDT87939`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `CL-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-02T02:12:19.851960+00:00`
- closed: `2026-05-02T10:12:25.906481+00:00` · hour UTC 10 (Sat)

## 2 · Hypothesis (why we entered)
> Hurst trend-regime short H=0.939 below EMA21

### Parsed signal features
- **hurst**: 0.9390103887328868
- **atr_val**: 0.9094848930706438

### Raw meta from agent
```json
{
  "atr_sl": 103.90422733960597,
  "atr_tp": 1.0254,
  "hurst": 0.9390103887328868,
  "atr_val": 0.9094848930706438,
  "_paper_only": true
}
```

## 3 · Plan vs Execution
- entry_price: 102.54
- exit_price: 102.54
- tp_price: 1.0254
- sl_price: 103.90422733960597
- qty: 222.0 · notional: 227.63880000000003
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0
- **planned_sl_distance_pct**: 1.3304
- **planned_r_multiple**: 74.414
- **planned_risk_usd**: 302.8585
- **planned_reward_usd**: 22536.2412
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0
- **exit_distance_from_sl_pct**: 1.3304
- **notional**: 227.63880000000003

### Market excursion (MFE / MAE proxy)
- high_water: 102.54 · low_water: 102.44
- current_stop_at_close: 103.90422733960597
- **mfe_pct**: 0.0975
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0975

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0%
- slippage vs planned SL: 1.3304%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: True
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - dead-zone-hour
  - agent-on-kill-list
  - strong planned R:R=74.414

## 7 · Tags
`dead_hour`, `killed_agent`, `long_hold`, `time_or_manual`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.558027Z · journaler v2*
