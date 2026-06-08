# Trade #249 — HYPE-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.3584 (+0.350% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.15 min

> Short trailed into profit on HYPE-USDT (stoch_rsi, +0.35%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS6517`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-26T14:41:59.725215+00:00`
- closed: `2026-05-26T14:44:08.626006+00:00` · hour UTC 14 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [vwap_reversion,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=67

### Parsed signal features
- **rsi**: 67.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 64.59657,
  "atr_tp": 62.997645,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 64.003
- exit_price: 63.779
- tp_price: 62.998
- sl_price: 64.597
- qty: 16.0 · notional: 102.40480000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5702
- **planned_sl_distance_pct**: 0.9281
- **planned_r_multiple**: 1.692
- **planned_risk_usd**: 9.504
- **planned_reward_usd**: 16.08
- **realized_r_multiple**: 0.038
- **exit_distance_from_tp_pct**: 1.2203
- **exit_distance_from_sl_pct**: 1.2781
- **notional**: 102.40480000000001

### Market excursion (MFE / MAE proxy)
- high_water: 64.003 · low_water: 63.548
- current_stop_at_close: 63.865739999999995
- **mfe_pct**: 0.7109
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3609

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.038
- slippage vs planned TP: 1.2203%
- slippage vs planned SL: 1.2781%

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
`confluence`, `very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-26T15:01:27.129099Z · journaler v2*
