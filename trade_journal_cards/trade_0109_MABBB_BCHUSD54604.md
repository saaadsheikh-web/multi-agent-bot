# Trade #109 — BCH-USDT long (bb_bounce)

**Outcome:** WIN · **PnL:** +0.1080 (+0.202% if pct available) · **Decision grade:** A (100/100) · **Hold:** 12.04 min

> Long trailed into profit on BCH-USDT (bb_bounce, +0.20%) [grade A / 100].

## 1 · Identity
- custom_id: `MABBB_BCHUSD54604`
- agent: `bb_bounce` · profile: `bb_bounce`
- symbol: `BCH-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-12T02:56:45.811880+00:00`
- closed: `2026-05-12T03:08:48.184515+00:00` · hour UTC 03 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [bb_bounce,wide_scalp] — best: BB lower tag long, RSI 28, width 0.0166

### Parsed signal features
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 440.055,
  "atr_tp": 449.27,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 444.5
- exit_price: 445.4
- tp_price: 449.27
- sl_price: 440.06
- qty: 1.2 · notional: 53.339999999999996
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.0731
- **planned_sl_distance_pct**: 0.9989
- **planned_r_multiple**: 1.074
- **planned_risk_usd**: 5.328
- **planned_reward_usd**: 5.724
- **realized_r_multiple**: 0.02
- **exit_distance_from_tp_pct**: 0.8706
- **exit_distance_from_sl_pct**: 1.2013
- **notional**: 53.339999999999996

### Market excursion (MFE / MAE proxy)
- high_water: 445.5 · low_water: 444.5
- current_stop_at_close: 440.06
- **mfe_pct**: 0.225
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0225

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.02
- slippage vs planned TP: 0.8706%
- slippage vs planned SL: 1.2013%

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
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562431Z · journaler v2*
