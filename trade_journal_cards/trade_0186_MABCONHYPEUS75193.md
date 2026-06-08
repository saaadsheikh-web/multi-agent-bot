# Trade #186 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8316 (-1.616% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.08 min

> Long stopped out at full risk on HYPE-USDT (connors_rsi2, -1.62%) during good-zone hour 18:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS75193`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T18:39:55.014177+00:00`
- closed: `2026-05-22T18:42:59.661780+00:00` · hour UTC 18 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.4, ATR%=0.63, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.4
- **atr_pct**: 0.63
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 56.30851,
  "atr_tp": 58.30932,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 57.181
- exit_price: 56.257
- tp_price: 58.309
- sl_price: 56.309
- qty: 9.0 · notional: 51.4629
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9727
- **planned_sl_distance_pct**: 1.525
- **planned_r_multiple**: 1.294
- **planned_risk_usd**: 7.848
- **planned_reward_usd**: 10.152
- **realized_r_multiple**: -0.106
- **exit_distance_from_tp_pct**: 3.5886
- **exit_distance_from_sl_pct**: -0.0909
- **notional**: 51.4629

### Market excursion (MFE / MAE proxy)
- high_water: 57.181 · low_water: 57.181
- current_stop_at_close: 56.309
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.106
- slippage vs planned TP: 3.5886%
- slippage vs planned SL: -0.0909%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (8) lost

## 7 · Tags
`good_hour`, `very_short_hold`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570640Z · journaler v2*
