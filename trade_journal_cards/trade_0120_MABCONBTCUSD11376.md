# Trade #120 — BTC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0243 (+0.044% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.87 min

> Short timed out in profit on BTC-USDT (connors_rsi2, +0.04%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBTCUSD11376`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T06:02:58.144220+00:00`
- closed: `2026-05-16T06:08:50.305886+00:00` · hour UTC 06 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.4, ATR%=0.06, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.4
- **atr_pct**: 0.06
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 80184.69549999999,
  "atr_tp": 77419.70599999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 78999.7
- exit_price: 78965.0
- tp_price: 77419.7
- sl_price: 80184.7
- qty: 0.7 · notional: 55.299789999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 829.5
- **planned_reward_usd**: 1106.0
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9561
- **exit_distance_from_sl_pct**: 1.5439
- **notional**: 55.299789999999994

### Market excursion (MFE / MAE proxy)
- high_water: 78999.7 · low_water: 78965.0
- current_stop_at_close: 80184.7
- **mfe_pct**: 0.0439
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9561%
- slippage vs planned SL: 1.5439%

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
`short_win`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562791Z · journaler v2*
