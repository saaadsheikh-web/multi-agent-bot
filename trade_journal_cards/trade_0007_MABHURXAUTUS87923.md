# Trade #7 — XAUT-USDT short (hurst_regime)

**Outcome:** LOSS · **PnL:** -0.0588 (-0.026% if pct available) · **Decision grade:** C (60/100) · **Hold:** 480.14 min

> Short closed in the red without clean exit on XAUT-USDT (hurst_regime, -0.03%) during dead-zone hour 10:00 UTC [killed-agent] [grade C / 60].

## 1 · Identity
- custom_id: `MABHURXAUTUS87923`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `XAUT-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-02T02:12:04.754155+00:00`
- closed: `2026-05-02T10:12:13.147576+00:00` · hour UTC 10 (Sat)

## 2 · Hypothesis (why we entered)
> Hurst trend-regime short H=0.962 below EMA21

### Parsed signal features
- **hurst**: 0.9624199172957641
- **atr_val**: 10.91633781970189

### Raw meta from agent
```json
{
  "atr_sl": 4615.374506729553,
  "atr_tp": 45.99,
  "hurst": 0.9624199172957641,
  "atr_val": 10.91633781970189,
  "_paper_only": true
}
```

## 3 · Plan vs Execution
- entry_price: 4599.0
- exit_price: 4600.2
- tp_price: 45.99
- sl_price: 4615.374506729553
- qty: 49.0 · notional: 225.351
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0
- **planned_sl_distance_pct**: 0.356
- **planned_r_multiple**: 278.09
- **planned_risk_usd**: 802.3508
- **planned_reward_usd**: 223097.49
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 99.0261
- **exit_distance_from_sl_pct**: 0.33
- **notional**: 225.351

### Market excursion (MFE / MAE proxy)
- high_water: 4599.0 · low_water: 4597.8
- current_stop_at_close: 4615.374506729553
- **mfe_pct**: 0.0261
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0522

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 99.0261%
- slippage vs planned SL: 0.33%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: True
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (60/100)
- factors:
  - dead-zone-hour
  - agent-on-kill-list
  - strong planned R:R=278.09
  - timed-out loser (no clean exit signal)
  - high confidence (8) lost

## 7 · Tags
`dead_hour`, `killed_agent`, `long_hold`, `time_or_manual`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.557979Z · journaler v2*
