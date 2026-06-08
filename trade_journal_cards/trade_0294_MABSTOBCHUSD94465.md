# Trade #294 — BCH-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.1200 (-1.089% if pct available) · **Decision grade:** A (100/100) · **Hold:** 95.23 min

> Long stopped out at full risk on BCH-USDT (stoch_rsi, -1.09%) trail gave back 1.43% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBCHUSD94465`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T06:14:26.775928+00:00`
- closed: `2026-06-01T07:49:40.402553+00:00` · hour UTC 07 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [swing,stoch_rsi] — best: StochRSI long stoch=0.00 rsi=33

### Parsed signal features
- **rsi**: 33.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 290.6838,
  "atr_tp": 298.0243,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 293.8
- exit_price: 290.6
- tp_price: 298.02
- sl_price: 290.68
- qty: 3.5 · notional: 102.83000000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4364
- **planned_sl_distance_pct**: 1.0619
- **planned_r_multiple**: 1.353
- **planned_risk_usd**: 10.92
- **planned_reward_usd**: 14.77
- **realized_r_multiple**: -0.103
- **exit_distance_from_tp_pct**: 2.5255
- **exit_distance_from_sl_pct**: -0.0272
- **notional**: 102.83000000000001

### Market excursion (MFE / MAE proxy)
- high_water: 294.8 · low_water: 293.8
- current_stop_at_close: 290.68
- **mfe_pct**: 0.3404
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.4295

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.103
- slippage vs planned TP: 2.5255%
- slippage vs planned SL: -0.0272%

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
  - high confidence (9) lost

## 7 · Tags
`confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617658+00:00Z · journaler v2*
