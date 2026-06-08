# Trade #117 — BCH-USDT short (connors_rsi2)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.33 min

> Short flat exit (scratch) on BCH-USDT (connors_rsi2, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD84112`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-15T22:28:34.708025+00:00`
- closed: `2026-05-15T22:32:54.391207+00:00` · hour UTC 22 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.1, ATR%=0.10, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.1
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 431.984,
  "atr_tp": 417.088,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 425.6
- exit_price: 425.6
- tp_price: 417.09
- sl_price: 431.98
- qty: 1.2 · notional: 51.072
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9995
- **planned_sl_distance_pct**: 1.4991
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.656
- **planned_reward_usd**: 10.212
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9995
- **exit_distance_from_sl_pct**: 1.4991
- **notional**: 51.072

### Market excursion (MFE / MAE proxy)
- high_water: 425.6 · low_water: 425.5
- current_stop_at_close: 431.98
- **mfe_pct**: 0.0235
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0235

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9995%
- slippage vs planned SL: 1.4991%

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
`very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562703Z · journaler v2*
