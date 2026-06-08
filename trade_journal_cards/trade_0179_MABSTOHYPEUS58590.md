# Trade #179 — HYPE-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.7254 (+1.313% if pct available) · **Decision grade:** A (90/100) · **Hold:** 14.93 min

> Clean short TP hit on HYPE-USDT (stoch_rsi, +1.31%) [grade A / 90].

## 1 · Identity
- custom_id: `MABSTOHYPEUS58590`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T14:03:12.033265+00:00`
- closed: `2026-05-22T14:18:07.545392+00:00` · hour UTC 14 (Fri)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [swing,bb_bounce,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=71

### Parsed signal features
- **rsi**: 71.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 62.18166,
  "atr_tp": 60.64251,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 61.366
- exit_price: 60.56
- tp_price: 60.643
- sl_price: 62.182
- qty: 9.0 · notional: 55.2294
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.1782
- **planned_sl_distance_pct**: 1.3297
- **planned_r_multiple**: 0.886
- **planned_risk_usd**: 7.344
- **planned_reward_usd**: 6.507
- **realized_r_multiple**: 0.099
- **exit_distance_from_tp_pct**: -0.1353
- **exit_distance_from_sl_pct**: 2.6432
- **notional**: 55.2294

### Market excursion (MFE / MAE proxy)
- high_water: 61.366 · low_water: 60.56
- current_stop_at_close: 60.86279999999999
- **mfe_pct**: 1.3134
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.099
- slippage vs planned TP: -0.1353%
- slippage vs planned SL: 2.6432%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - poor planned R:R=0.886
  - multi-agent confluence

## 7 · Tags
`confluence`, `short_win`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570561Z · journaler v2*
