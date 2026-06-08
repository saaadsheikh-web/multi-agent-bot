# Trade #261 — XMR-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +2.6012 (+2.558% if pct available) · **Decision grade:** B (85/100) · **Hold:** 74.55 min

> Clean long TP hit on XMR-USDT (funding_extremes, +2.56%) during dead-zone hour 10:00 UTC [grade B / 85].

## 1 · Identity
- custom_id: `MABFUNXMRUSD44540`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-29T08:49:02.374581+00:00`
- closed: `2026-05-29T10:03:35.335238+00:00` · hour UTC 10 (Fri)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0541%/8h (annual≈-59%), RSI=49, EMA50 slope=-0.36%

### Parsed signal features
- **rsi**: 48.927723540808586
- **ema_slope**: -0.36030629219240273
- **atr_pct**: 1.4428022963580012
- **funding_rate**: -0.0005406181734492476
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005406181734492476,
  "rsi": 48.927723540808586,
  "ema_slope": -0.36030629219240273,
  "atr_pct": 1.4428022963580012,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 363.17
- exit_price: 372.46
- tp_price: 372.25
- sl_price: 357.72
- qty: 2.8 · notional: 101.68759999999999
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.5002
- **planned_sl_distance_pct**: 1.5007
- **planned_r_multiple**: 1.666
- **planned_risk_usd**: 15.26
- **planned_reward_usd**: 25.424
- **realized_r_multiple**: 0.17
- **exit_distance_from_tp_pct**: -0.0578
- **exit_distance_from_sl_pct**: 4.0587
- **notional**: 101.68759999999999

### Market excursion (MFE / MAE proxy)
- high_water: 372.46 · low_water: 363.17
- current_stop_at_close: 368.73539999999997
- **mfe_pct**: 2.558
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.17
- slippage vs planned TP: -0.0578%
- slippage vs planned SL: 4.0587%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `tp_hit`, `grade_B`

---
*journaled_at 2026-06-05T21:57:18.617043+00:00Z · journaler v2*
