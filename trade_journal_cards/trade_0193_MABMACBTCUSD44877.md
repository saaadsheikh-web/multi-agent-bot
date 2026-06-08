# Trade #193 — BTC-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +1.1033 (+2.097% if pct available) · **Decision grade:** A (100/100) · **Hold:** 880.82 min

> Clean long TP hit on BTC-USDT (macd_cross, +2.10%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACBTCUSD44877`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `BTC-USDT` · side: `long`
- confidence: 6
- opened: `2026-05-23T14:01:18.627096+00:00`
- closed: `2026-05-24T04:42:07.706916+00:00` · hour UTC 04 (Sun)

## 2 · Hypothesis (why we entered)
> MACD bull cross hist 19.0235 vol 1.3x

### Parsed signal features
- **atr_val**: 316.6614383750536
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 74695.00784243742,
  "atr_tp": 76119.98431512516,
  "atr_val": 316.6614383750536,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75150.1
- exit_price: 76726.3
- tp_price: 76120.0
- sl_price: 74695.0
- qty: 0.7 · notional: 52.605070000000005
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.2906
- **planned_sl_distance_pct**: 0.6056
- **planned_r_multiple**: 2.131
- **planned_risk_usd**: 318.57
- **planned_reward_usd**: 678.93
- **realized_r_multiple**: 0.003
- **exit_distance_from_tp_pct**: -0.8068
- **exit_distance_from_sl_pct**: 2.703
- **notional**: 52.605070000000005

### Market excursion (MFE / MAE proxy)
- high_water: 76726.3 · low_water: 75150.1
- current_stop_at_close: 75959.037
- **mfe_pct**: 2.0974
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.003
- slippage vs planned TP: -0.8068%
- slippage vs planned SL: 2.703%

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
  - strong planned R:R=2.131

## 7 · Tags
`long_hold`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905402Z · journaler v2*
