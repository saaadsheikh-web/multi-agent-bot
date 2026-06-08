# Trade #152 — BCH-USDT short (bb_bounce)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 7.44 min

> Short flat exit (scratch) on BCH-USDT (bb_bounce, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABBB_BCHUSD35543`
- agent: `bb_bounce` · profile: `bb_bounce`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-21T03:52:25.350128+00:00`
- closed: `2026-05-21T03:59:52.020499+00:00` · hour UTC 03 (Thu)

## 2 · Hypothesis (why we entered)
> 3 agents agree (same-family) [vwap_reversion,bb_bounce,stoch_rsi] — best: BB upper tag short, RSI 69, width 0.0446

### Parsed signal features
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 383.8,
  "atr_tp": 371.6105,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 380.0
- exit_price: 380.0
- tp_price: 371.61
- sl_price: 383.8
- qty: 1.4 · notional: 53.199999999999996
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 2.2079
- **planned_sl_distance_pct**: 1.0
- **planned_r_multiple**: 2.208
- **planned_risk_usd**: 5.32
- **planned_reward_usd**: 11.746
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.2079
- **exit_distance_from_sl_pct**: 1.0
- **notional**: 53.199999999999996

### Market excursion (MFE / MAE proxy)
- high_water: 380.0 · low_water: 379.9
- current_stop_at_close: 383.8
- **mfe_pct**: 0.0263
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0263

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.2079%
- slippage vs planned SL: 1.0%

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
  - strong planned R:R=2.208
  - multi-agent confluence

## 7 · Tags
`confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-21T07:01:00.212384Z · journaler v2*
