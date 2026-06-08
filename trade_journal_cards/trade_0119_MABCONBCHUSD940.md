# Trade #119 — BCH-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0360 (+0.070% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.45 min

> Short trailed into profit on BCH-USDT (connors_rsi2, +0.07%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD940`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T03:09:01.729913+00:00`
- closed: `2026-05-16T03:13:28.583755+00:00` · hour UTC 03 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.6, ATR%=0.09, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.6
- **atr_pct**: 0.09
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 433.202,
  "atr_tp": 418.264,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 426.8
- exit_price: 426.5
- tp_price: 418.26
- sl_price: 433.2
- qty: 1.2 · notional: 51.216
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0009
- **planned_sl_distance_pct**: 1.4995
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.68
- **planned_reward_usd**: 10.248
- **realized_r_multiple**: 0.005
- **exit_distance_from_tp_pct**: 1.9306
- **exit_distance_from_sl_pct**: 1.5698
- **notional**: 51.216

### Market excursion (MFE / MAE proxy)
- high_water: 426.8 · low_water: 426.2
- current_stop_at_close: 433.2
- **mfe_pct**: 0.1406
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0703

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.005
- slippage vs planned TP: 1.9306%
- slippage vs planned SL: 1.5698%

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
`very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562762Z · journaler v2*
