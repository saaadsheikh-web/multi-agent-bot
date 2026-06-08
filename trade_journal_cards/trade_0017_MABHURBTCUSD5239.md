# Trade #17 — BTC-USDT long (hurst_regime)

**Outcome:** WIN · **PnL:** +0.3668 (+0.661% if pct available) · **Decision grade:** B (85/100) · **Hold:** 45.87 min

> Long trailed into profit on BTC-USDT (hurst_regime, +0.66%) [killed-agent] trail gave back 0.82% [grade B / 85].

## 1 · Identity
- custom_id: `MABHURBTCUSD5239`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `BTC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-04T14:34:00.134888+00:00`
- closed: `2026-05-04T15:19:52.414033+00:00` · hour UTC 15 (Mon)

## 2 · Hypothesis (why we entered)
> Hurst trend-regime long H=0.927 above EMA21

### Parsed signal features
- **hurst**: 0.9273061368217903
- **atr_val**: 515.5704658278363

### Raw meta from agent
```json
{
  "atr_sl": 78518.74430125825,
  "atr_tp": 157791.279,
  "hurst": 0.9273061368217903,
  "atr_val": 515.5704658278363
}
```

## 3 · Plan vs Execution
- entry_price: 79292.1
- exit_price: 79816.1
- tp_price: 157791.279
- sl_price: 78518.74430125825
- qty: 0.7 · notional: 55.504470000000005
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0
- **planned_sl_distance_pct**: 0.9753
- **planned_r_multiple**: 101.507
- **planned_risk_usd**: 541.349
- **planned_reward_usd**: 54949.4253
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 98.3392
- **exit_distance_from_sl_pct**: 1.6362
- **notional**: 55.504470000000005

### Market excursion (MFE / MAE proxy)
- high_water: 80467.2 · low_water: 79292.1
- current_stop_at_close: 79823.46239999999
- **mfe_pct**: 1.482
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8211

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 98.3392%
- slippage vs planned SL: 1.6362%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=101.507

## 7 · Tags
`killed_agent`, `trail_too_loose`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.558343Z · journaler v2*
