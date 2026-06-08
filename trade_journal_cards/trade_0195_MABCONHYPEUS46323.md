# Trade #195 — HYPE-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0549 (+0.109% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.33 min

> Short trailed into profit on HYPE-USDT (connors_rsi2, +0.11%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS46323`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T14:25:25.242397+00:00`
- closed: `2026-05-23T14:29:44.813419+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.9, ATR%=0.46, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.9
- **atr_pct**: 0.46
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 56.646134999999994,
  "atr_tp": 54.69282,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 55.841
- exit_price: 55.78
- tp_price: 54.693
- sl_price: 56.646
- qty: 9.0 · notional: 50.2569
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0558
- **planned_sl_distance_pct**: 1.4416
- **planned_r_multiple**: 1.426
- **planned_risk_usd**: 7.245
- **planned_reward_usd**: 10.332
- **realized_r_multiple**: 0.008
- **exit_distance_from_tp_pct**: 1.9466
- **exit_distance_from_sl_pct**: 1.5508
- **notional**: 50.2569

### Market excursion (MFE / MAE proxy)
- high_water: 55.841 · low_water: 55.7
- current_stop_at_close: 56.646
- **mfe_pct**: 0.2525
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1433

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.008
- slippage vs planned TP: 1.9466%
- slippage vs planned SL: 1.5508%

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
*journaled_at 2026-05-23T15:00:56.570823Z · journaler v2*
