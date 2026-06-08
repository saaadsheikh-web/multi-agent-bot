# Trade #253 — ZEC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.9196 (+0.875% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.79 min

> Long trailed into profit on ZEC-USDT (stoch_rsi, +0.88%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOZECUSD99773`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-27T16:36:15.253122+00:00`
- closed: `2026-05-27T16:40:02.928356+00:00` · hour UTC 16 (Wed)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [swing,bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.07 rsi=32

### Parsed signal features
- **rsi**: 32.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 549.8361,
  "atr_tp": 563.7208499999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 552.93
- exit_price: 557.77
- tp_price: 563.72
- sl_price: 549.84
- qty: 1.9 · notional: 105.05669999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.9514
- **planned_sl_distance_pct**: 0.5588
- **planned_r_multiple**: 3.492
- **planned_risk_usd**: 5.871
- **planned_reward_usd**: 20.501
- **realized_r_multiple**: 0.157
- **exit_distance_from_tp_pct**: 1.0761
- **exit_distance_from_sl_pct**: 1.4342
- **notional**: 105.05669999999999

### Market excursion (MFE / MAE proxy)
- high_water: 558.87 · low_water: 552.93
- current_stop_at_close: 556.07565
- **mfe_pct**: 1.0743
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1989

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.157
- slippage vs planned TP: 1.0761%
- slippage vs planned SL: 1.4342%

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
  - strong planned R:R=3.492
  - multi-agent confluence

## 7 · Tags
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-27T19:00:51.546065Z · journaler v2*
