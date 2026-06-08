# Trade #182 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7785 (-1.489% if pct available) · **Decision grade:** A (100/100) · **Hold:** 39.02 min

> Long stopped out at full risk on HYPE-USDT (connors_rsi2, -1.49%) trail gave back 1.91% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS64612`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T15:43:33.895312+00:00`
- closed: `2026-05-22T16:22:35.080867+00:00` · hour UTC 16 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.1, ATR%=0.74, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.1
- **atr_pct**: 0.74
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 57.233425,
  "atr_tp": 59.2671,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 58.08
- exit_price: 57.215
- tp_price: 59.267
- sl_price: 57.233
- qty: 9.0 · notional: 52.272
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0437
- **planned_sl_distance_pct**: 1.4583
- **planned_r_multiple**: 1.401
- **planned_risk_usd**: 7.623
- **planned_reward_usd**: 10.683
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.5331
- **exit_distance_from_sl_pct**: -0.031
- **notional**: 52.272

### Market excursion (MFE / MAE proxy)
- high_water: 58.326 · low_water: 58.08
- current_stop_at_close: 57.233
- **mfe_pct**: 0.4236
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.9129

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.5331%
- slippage vs planned SL: -0.031%

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
  - high confidence (8) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570609Z · journaler v2*
