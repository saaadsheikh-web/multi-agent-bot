# Trade #41 — HYPE-USDT long (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 170.92 min

> Long flat exit (scratch) on HYPE-USDT (connors_rsi2, +0.00%) trail gave back 0.69% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS7433`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-05T18:57:14.248605+00:00`
- closed: `2026-05-05T21:48:09.645755+00:00` · hour UTC 21 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [ema_ribbon,connors_rsi2] — best: Connors RSI2 long: RSI2=3.6, in uptrend

### Parsed signal features
- **rsi2**: 3.6
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 43.636485,
  "atr_tp": 45.187020000000004
}
```

## 3 · Plan vs Execution
- entry_price: 44.301
- exit_price: 44.301
- tp_price: 45.187
- sl_price: 43.636
- qty: 12.0 · notional: 53.16120000000001
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5011
- **planned_r_multiple**: 1.332
- **planned_risk_usd**: 7.98
- **planned_reward_usd**: 10.632
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.0
- **exit_distance_from_sl_pct**: 1.5011
- **notional**: 53.16120000000001

### Market excursion (MFE / MAE proxy)
- high_water: 44.608 · low_water: 44.301
- current_stop_at_close: 43.636
- **mfe_pct**: 0.693
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.693

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.0%
- slippage vs planned SL: 1.5011%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559299Z · journaler v2*
