# Trade #188 — XMR-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.6986 (+1.300% if pct available) · **Decision grade:** A (100/100) · **Hold:** 536.55 min

> Short trailed into profit on XMR-USDT (connors_rsi2, +1.30%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD82826`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T20:47:08.773676+00:00`
- closed: `2026-05-23T05:43:41.804836+00:00` · hour UTC 05 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.0, ATR%=0.26, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.0
- **atr_pct**: 0.26
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 389.50624999999997,
  "atr_tp": 376.075,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 383.75
- exit_price: 378.76
- tp_price: 376.08
- sl_price: 389.51
- qty: 1.4 · notional: 53.724999999999994
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9987
- **planned_sl_distance_pct**: 1.501
- **planned_r_multiple**: 1.332
- **planned_risk_usd**: 8.064
- **planned_reward_usd**: 10.738
- **realized_r_multiple**: 0.087
- **exit_distance_from_tp_pct**: 0.6984
- **exit_distance_from_sl_pct**: 2.8013
- **notional**: 53.724999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 383.75 · low_water: 378.76
- current_stop_at_close: 381.03256
- **mfe_pct**: 1.3003
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.087
- slippage vs planned TP: 0.6984%
- slippage vs planned SL: 2.8013%

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
`good_hour`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570777Z · journaler v2*
