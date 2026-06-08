# Trade #21 — BTC-USDT long (hurst_regime)

**Outcome:** WIN · **PnL:** +0.4418 (+0.795% if pct available) · **Decision grade:** A (95/100) · **Hold:** 210.51 min

> Long trailed into profit on BTC-USDT (hurst_regime, +0.79%) during good-zone hour 18:00 UTC [killed-agent] trail gave back 0.85% [grade A / 95].

## 1 · Identity
- custom_id: `MABHURBTCUSD8116`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `BTC-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T15:21:57.141362+00:00`
- closed: `2026-05-04T18:52:27.593229+00:00` · hour UTC 18 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime long H=0.948 above EMA21

### Parsed signal features
- **hurst**: 0.9479023343099667
- **atr_val**: 631.9896896142042
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 78466.41546557868,
  "atr_tp": 158034.656,
  "hurst": 0.9479023343099667,
  "atr_val": 631.9896896142042
}
```

## 3 · Plan vs Execution
- entry_price: 79420.2
- exit_price: 80051.4
- tp_price: 158034.656
- sl_price: 78466.41546557868
- qty: 0.7 · notional: 55.594139999999996
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 98.9855
- **planned_sl_distance_pct**: 1.2009
- **planned_r_multiple**: 82.426
- **planned_risk_usd**: 667.6492
- **planned_reward_usd**: 55030.1192
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 98.1907
- **exit_distance_from_sl_pct**: 1.9957
- **notional**: 55.594139999999996

### Market excursion (MFE / MAE proxy)
- high_water: 80727.2 · low_water: 79420.2
- current_stop_at_close: 80081.3824
- **mfe_pct**: 1.6457
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8509

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 98.1907%
- slippage vs planned SL: 1.9957%

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
  - strong planned R:R=82.426
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558462Z · journaler v2*
