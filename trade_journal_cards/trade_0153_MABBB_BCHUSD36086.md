# Trade #153 — BCH-USDT short (bb_bounce)

**Outcome:** LOSS · **PnL:** -0.0840 (-0.158% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.45 min

> Short closed in the red without clean exit on BCH-USDT (bb_bounce, -0.16%) [grade A / 100].

## 1 · Identity
- custom_id: `MABBB_BCHUSD36086`
- agent: `bb_bounce` · profile: `bb_bounce`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-21T04:01:28.959101+00:00`
- closed: `2026-05-21T04:04:56.143749+00:00` · hour UTC 04 (Thu)

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
- entry_price: 380.1
- exit_price: 380.7
- tp_price: 371.61
- sl_price: 383.8
- qty: 1.4 · notional: 53.214
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 2.2336
- **planned_sl_distance_pct**: 0.9734
- **planned_r_multiple**: 2.295
- **planned_risk_usd**: 5.18
- **planned_reward_usd**: 11.886
- **realized_r_multiple**: -0.016
- **exit_distance_from_tp_pct**: 2.3915
- **exit_distance_from_sl_pct**: 0.8156
- **notional**: 53.214

### Market excursion (MFE / MAE proxy)
- high_water: 380.1 · low_water: 380.1
- current_stop_at_close: 383.8
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.016
- slippage vs planned TP: 2.3915%
- slippage vs planned SL: 0.8156%

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
  - strong planned R:R=2.295
  - multi-agent confluence
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`confluence`, `very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-21T07:01:00.212437Z · journaler v2*
