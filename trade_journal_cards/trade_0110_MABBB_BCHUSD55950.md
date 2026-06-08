# Trade #110 — BCH-USDT long (bb_bounce)

**Outcome:** WIN · **PnL:** +0.3360 (+0.629% if pct available) · **Decision grade:** B (80/100) · **Hold:** 240.08 min

> Long trailed into profit on BCH-USDT (bb_bounce, +0.63%) [grade B / 80].

## 1 · Identity
- custom_id: `MABBB_BCHUSD55950`
- agent: `bb_bounce` · profile: `bb_bounce`
- symbol: `BCH-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-12T03:19:11.736121+00:00`
- closed: `2026-05-12T07:19:16.596110+00:00` · hour UTC 07 (Tue)

## 2 · Hypothesis (why we entered)
> BB lower tag long, RSI 31, width 0.0183

### Parsed signal features
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 440.55,
  "atr_tp": 449.0450000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 445.1
- exit_price: 447.9
- tp_price: 449.05
- sl_price: 440.55
- qty: 1.2 · notional: 53.412
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 0.8874
- **planned_sl_distance_pct**: 1.0222
- **planned_r_multiple**: 0.868
- **planned_risk_usd**: 5.46
- **planned_reward_usd**: 4.74
- **realized_r_multiple**: 0.062
- **exit_distance_from_tp_pct**: 0.2584
- **exit_distance_from_sl_pct**: 1.6513
- **notional**: 53.412

### Market excursion (MFE / MAE proxy)
- high_water: 448.1 · low_water: 445.1
- current_stop_at_close: 445.8595
- **mfe_pct**: 0.674
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0449

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.062
- slippage vs planned TP: 0.2584%
- slippage vs planned SL: 1.6513%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - poor planned R:R=0.868

## 7 · Tags
`long_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.562518Z · journaler v2*
