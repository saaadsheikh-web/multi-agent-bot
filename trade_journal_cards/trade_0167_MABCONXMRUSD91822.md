# Trade #167 — XMR-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7956 (-1.524% if pct available) · **Decision grade:** A (100/100) · **Hold:** 112.59 min

> Long stopped out at full risk on XMR-USDT (connors_rsi2, -1.52%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD91822`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T19:30:24.083402+00:00`
- closed: `2026-05-21T21:22:59.733472+00:00` · hour UTC 21 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.7, ATR%=0.25, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.7
- **atr_pct**: 0.25
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 395.576,
  "atr_tp": 409.632,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 401.6
- exit_price: 395.48
- tp_price: 409.63
- sl_price: 395.58
- qty: 1.3 · notional: 52.208000000000006
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9995
- **planned_sl_distance_pct**: 1.499
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.826
- **planned_reward_usd**: 10.439
- **realized_r_multiple**: -0.102
- **exit_distance_from_tp_pct**: 3.5234
- **exit_distance_from_sl_pct**: -0.0249
- **notional**: 52.208000000000006

### Market excursion (MFE / MAE proxy)
- high_water: 401.6 · low_water: 401.6
- current_stop_at_close: 395.58
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.102
- slippage vs planned TP: 3.5234%
- slippage vs planned SL: -0.0249%

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
  - high confidence (9) lost

## 7 · Tags
`long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570354Z · journaler v2*
