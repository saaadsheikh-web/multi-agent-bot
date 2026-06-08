# Trade #166 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8334 (-1.588% if pct available) · **Decision grade:** A (100/100) · **Hold:** 10.07 min

> Long stopped out at full risk on HYPE-USDT (connors_rsi2, -1.59%) during good-zone hour 19:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS90617`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T19:10:19.136939+00:00`
- closed: `2026-05-21T19:20:23.496713+00:00` · hour UTC 19 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.4, ATR%=0.74, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.4
- **atr_pct**: 0.74
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 57.402845,
  "atr_tp": 59.44254,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 58.318
- exit_price: 57.392
- tp_price: 59.443
- sl_price: 57.403
- qty: 9.0 · notional: 52.4862
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9291
- **planned_sl_distance_pct**: 1.569
- **planned_r_multiple**: 1.23
- **planned_risk_usd**: 8.235
- **planned_reward_usd**: 10.125
- **realized_r_multiple**: -0.101
- **exit_distance_from_tp_pct**: 3.5169
- **exit_distance_from_sl_pct**: -0.0189
- **notional**: 52.4862

### Market excursion (MFE / MAE proxy)
- high_water: 58.318 · low_water: 58.318
- current_stop_at_close: 57.403
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.101
- slippage vs planned TP: 3.5169%
- slippage vs planned SL: -0.0189%

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
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570293Z · journaler v2*
