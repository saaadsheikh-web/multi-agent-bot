# Trade #331 — SOL-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.0033 (-0.999% if pct available) · **Decision grade:** A (100/100) · **Hold:** 51.76 min

> Long stopped out at full risk on SOL-USDT (stoch_rsi, -1.00%) trail gave back 1.14% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOSOLUSD6331`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `SOL-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T13:18:52.160832+00:00`
- closed: `2026-06-02T14:10:37.880957+00:00` · hour UTC 14 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.24 (was 0.08) rsi=38

### Parsed signal features
- **rsi**: 38.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 78.2991,
  "atr_tp": 80.27635,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 79.07
- exit_price: 78.28
- tp_price: 80.28
- sl_price: 78.3
- qty: 1.27 · notional: 100.4189
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5303
- **planned_sl_distance_pct**: 0.9738
- **planned_r_multiple**: 1.571
- **planned_risk_usd**: 0.9779
- **planned_reward_usd**: 1.5367
- **realized_r_multiple**: -1.026
- **exit_distance_from_tp_pct**: 2.5294
- **exit_distance_from_sl_pct**: -0.0253
- **notional**: 100.4189

### Market excursion (MFE / MAE proxy)
- high_water: 79.18 · low_water: 79.07
- current_stop_at_close: 78.3
- **mfe_pct**: 0.1391
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.1382

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.026
- slippage vs planned TP: 2.5294%
- slippage vs planned SL: -0.0253%

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
*journaled_at 2026-06-05T21:57:18.618621+00:00Z · journaler v2*
