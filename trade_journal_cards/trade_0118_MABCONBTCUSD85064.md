# Trade #118 — BTC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0188 (+0.034% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.66 min

> Short timed out in profit on BTC-USDT (connors_rsi2, +0.03%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBTCUSD85064`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-15T22:44:25.649023+00:00`
- closed: `2026-05-15T22:48:05.341337+00:00` · hour UTC 22 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.8, ATR%=0.08, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.8
- **atr_pct**: 0.08
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 80300.10099999998,
  "atr_tp": 77531.132,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 79113.4
- exit_price: 79086.6
- tp_price: 77531.1
- sl_price: 80300.1
- qty: 0.7 · notional: 55.37938
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 830.69
- **planned_reward_usd**: 1107.61
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9662
- **exit_distance_from_sl_pct**: 1.5339
- **notional**: 55.37938

### Market excursion (MFE / MAE proxy)
- high_water: 79113.4 · low_water: 79086.6
- current_stop_at_close: 80300.1
- **mfe_pct**: 0.0339
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9662%
- slippage vs planned SL: 1.5339%

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
`very_short_hold`, `short_win`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562734Z · journaler v2*
