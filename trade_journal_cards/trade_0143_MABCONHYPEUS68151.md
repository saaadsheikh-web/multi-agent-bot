# Trade #143 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0451 (+0.087% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.48 min

> Long trailed into profit on HYPE-USDT (connors_rsi2, +0.09%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS68151`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-19T05:22:32.387158+00:00`
- closed: `2026-05-19T05:25:01.003526+00:00` · hour UTC 05 (Tue)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.2, ATR%=0.34, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.2
- **atr_pct**: 0.34
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 46.561935,
  "atr_tp": 48.21642,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 47.24
- exit_price: 47.281
- tp_price: 48.216
- sl_price: 46.562
- qty: 11.0 · notional: 51.964000000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.066
- **planned_sl_distance_pct**: 1.4352
- **planned_r_multiple**: 1.44
- **planned_risk_usd**: 7.458
- **planned_reward_usd**: 10.736
- **realized_r_multiple**: 0.006
- **exit_distance_from_tp_pct**: 1.9793
- **exit_distance_from_sl_pct**: 1.522
- **notional**: 51.964000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 47.347 · low_water: 47.24
- current_stop_at_close: 46.562
- **mfe_pct**: 0.2265
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1397

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.006
- slippage vs planned TP: 1.9793%
- slippage vs planned SL: 1.522%

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
  - (no notable factors)

## 7 · Tags
`good_hour`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-19T07:00:59.092670Z · journaler v2*
