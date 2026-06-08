# Trade #312 — HYPE-USDT long (macd_cross)

**Outcome:** LOSS · **PnL:** -0.2100 (-0.203% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.33 min

> Long gave back gains on trail on HYPE-USDT (macd_cross, -0.20%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACHYPEUS57180`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T23:39:41.910404+00:00`
- closed: `2026-06-01T23:44:01.802751+00:00` · hour UTC 23 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [ema_ribbon,macd_cross] — best: MACD bull cross hist 0.0006 vol 1.4x

### Parsed signal features
- **atr_val**: 1.5321260812050896
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 71.56881087819237,
  "atr_tp": 78.46337824361527,
  "atr_val": 1.5321260812050896,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 73.867
- exit_price: 73.717
- tp_price: 78.463
- sl_price: 71.569
- qty: 14.0 · notional: 103.41380000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 6.222
- **planned_sl_distance_pct**: 3.111
- **planned_r_multiple**: 2.0
- **planned_risk_usd**: 32.172
- **planned_reward_usd**: 64.344
- **realized_r_multiple**: -0.007
- **exit_distance_from_tp_pct**: 6.4251
- **exit_distance_from_sl_pct**: 2.9079
- **notional**: 103.41380000000001

### Market excursion (MFE / MAE proxy)
- high_water: 73.956 · low_water: 73.867
- current_stop_at_close: 71.569
- **mfe_pct**: 0.1205
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3236

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.007
- slippage vs planned TP: 6.4251%
- slippage vs planned SL: 2.9079%

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
  - strong planned R:R=2.0
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`confluence`, `very_short_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618130+00:00Z · journaler v2*
