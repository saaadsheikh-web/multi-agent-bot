# Trade #141 — BTC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0024 (+0.005% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.04 min

> Short timed out in profit on BTC-USDT (connors_rsi2, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBTCUSD66560`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-19T04:56:01.931204+00:00`
- closed: `2026-05-19T04:58:04.374551+00:00` · hour UTC 04 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.7, ATR%=0.10, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.7
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 78046.39499999999,
  "atr_tp": 75355.14,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 76881.0
- exit_price: 76877.5
- tp_price: 75355.1
- sl_price: 78046.4
- qty: 0.7 · notional: 53.8167
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9848
- **planned_sl_distance_pct**: 1.5158
- **planned_r_multiple**: 1.309
- **planned_risk_usd**: 815.78
- **planned_reward_usd**: 1068.13
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9802
- **exit_distance_from_sl_pct**: 1.5204
- **notional**: 53.8167

### Market excursion (MFE / MAE proxy)
- high_water: 76881.0 · low_water: 76877.5
- current_stop_at_close: 78046.4
- **mfe_pct**: 0.0046
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9802%
- slippage vs planned SL: 1.5204%

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
*journaled_at 2026-05-19T07:00:59.092634Z · journaler v2*
