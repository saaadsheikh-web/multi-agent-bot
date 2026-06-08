# Trade #219 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1458 (+0.262% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.2 min

> Long trailed into profit on HYPE-USDT (connors_rsi2, +0.26%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS58582`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-24T21:36:24.133432+00:00`
- closed: `2026-05-24T21:39:36.187868+00:00` · hour UTC 21 (Sun)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.8, ATR%=0.44, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.8
- **atr_pct**: 0.44
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 60.883835,
  "atr_tp": 63.04722,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 61.811
- exit_price: 61.973
- tp_price: 63.047
- sl_price: 60.884
- qty: 9.0 · notional: 55.6299
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9996
- **planned_sl_distance_pct**: 1.4997
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 8.343
- **planned_reward_usd**: 11.124
- **realized_r_multiple**: 0.017
- **exit_distance_from_tp_pct**: 1.7376
- **exit_distance_from_sl_pct**: 1.7618
- **notional**: 55.6299

### Market excursion (MFE / MAE proxy)
- high_water: 61.978 · low_water: 61.811
- current_stop_at_close: 60.884
- **mfe_pct**: 0.2702
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0081

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.017
- slippage vs planned TP: 1.7376%
- slippage vs planned SL: 1.7618%

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
  - (no notable factors)

## 7 · Tags
`very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905674Z · journaler v2*
