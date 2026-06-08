# Trade #217 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0552 (+0.110% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.48 min

> Long trailed into profit on HYPE-USDT (connors_rsi2, +0.11%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS53326`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-24T20:08:48.084493+00:00`
- closed: `2026-05-24T20:14:17.074209+00:00` · hour UTC 20 (Sun)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=0.8, ATR%=0.52, uptrend slope-up

### Parsed signal features
- **rsi2**: 0.8
- **atr_pct**: 0.52
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 61.89346,
  "atr_tp": 64.09272,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 62.836
- exit_price: 62.905
- tp_price: 64.093
- sl_price: 61.893
- qty: 8.0 · notional: 50.2688
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0004
- **planned_sl_distance_pct**: 1.5007
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.544
- **planned_reward_usd**: 10.056
- **realized_r_multiple**: 0.007
- **exit_distance_from_tp_pct**: 1.8906
- **exit_distance_from_sl_pct**: 1.6105
- **notional**: 50.2688

### Market excursion (MFE / MAE proxy)
- high_water: 63.014 · low_water: 62.836
- current_stop_at_close: 61.893
- **mfe_pct**: 0.2833
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1735

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.007
- slippage vs planned TP: 1.8906%
- slippage vs planned SL: 1.6105%

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
`trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905628Z · journaler v2*
