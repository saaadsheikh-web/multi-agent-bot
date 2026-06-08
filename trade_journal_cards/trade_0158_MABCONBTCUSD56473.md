# Trade #158 — BTC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0004 (+0.001% if pct available) · **Decision grade:** B (85/100) · **Hold:** 4.45 min

> Long timed out in profit on BTC-USDT (connors_rsi2, +0.00%) during dead-zone hour 09:00 UTC [grade B / 85].

## 1 · Identity
- custom_id: `MABCONBTCUSD56473`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T09:41:15.415032+00:00`
- closed: `2026-05-21T09:45:42.210879+00:00` · hour UTC 09 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.6, ATR%=0.10, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.6
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 76487.9095,
  "atr_tp": 79205.754,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 77664.0
- exit_price: 77664.6
- tp_price: 79205.8
- sl_price: 76487.9
- qty: 0.7 · notional: 54.3648
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9852
- **planned_sl_distance_pct**: 1.5143
- **planned_r_multiple**: 1.311
- **planned_risk_usd**: 823.27
- **planned_reward_usd**: 1079.26
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9844
- **exit_distance_from_sl_pct**: 1.5151
- **notional**: 54.3648

### Market excursion (MFE / MAE proxy)
- high_water: 77690.9 · low_water: 77664.0
- current_stop_at_close: 76487.9
- **mfe_pct**: 0.0346
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0339

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9844%
- slippage vs planned SL: 1.5151%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** B (85/100)
- factors:
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `very_short_hold`, `time_or_manual`, `grade_B`

---
*journaled_at 2026-05-23T15:00:56.570190Z · journaler v2*
