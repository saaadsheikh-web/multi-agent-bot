# Trade #299 — TSLA-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.9960 (-0.968% if pct available) · **Decision grade:** A (100/100) · **Hold:** 14.32 min

> Long stopped out at full risk on TSLA-USDT (stoch_rsi, -0.97%) trail gave back 1.06% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOTSLAUS19889`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `TSLA-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T13:18:11.090594+00:00`
- closed: `2026-06-01T13:32:30.581693+00:00` · hour UTC 13 (Mon)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.29 (was 0.19) rsi=28

### Parsed signal features
- **rsi**: 28.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 424.7001,
  "atr_tp": 435.42485,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 428.8
- exit_price: 424.65
- tp_price: 435.42
- sl_price: 424.7
- qty: 24.0 · notional: 102.91199999999999
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5438
- **planned_sl_distance_pct**: 0.9562
- **planned_r_multiple**: 1.615
- **planned_risk_usd**: 98.4
- **planned_reward_usd**: 158.88
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 2.5117
- **exit_distance_from_sl_pct**: -0.0117
- **notional**: 102.91199999999999

### Market excursion (MFE / MAE proxy)
- high_water: 429.21 · low_water: 428.8
- current_stop_at_close: 424.7
- **mfe_pct**: 0.0956
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0634

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.01
- slippage vs planned TP: 2.5117%
- slippage vs planned SL: -0.0117%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (9) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617798+00:00Z · journaler v2*
