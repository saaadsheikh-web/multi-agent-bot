# Trade #264 — BTC-USDT short (macd_cross)

**Outcome:** LOSS · **PnL:** -0.1411 (-0.138% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.04 min

> Short gave back gains on trail on BTC-USDT (macd_cross, -0.14%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACBTCUSD66404`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `BTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-29T14:53:25.990480+00:00`
- closed: `2026-05-29T14:59:28.485675+00:00` · hour UTC 14 (Fri)

## 2 · Hypothesis (why we entered)
> 3 agents agree (same-family) [ema_ribbon,macd_cross,hurst_regime] — best: MACD bear cross hist -21.9596 vol 4.7x

### Parsed signal features
- **atr_val**: 381.67248186314197
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 73531.7087227947,
  "atr_tp": 71814.18255441057,
  "atr_val": 381.67248186314197,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 72981.8
- exit_price: 73082.6
- tp_price: 71814.2
- sl_price: 73531.7
- qty: 1.4 · notional: 102.17452
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5999
- **planned_sl_distance_pct**: 0.7535
- **planned_r_multiple**: 2.123
- **planned_risk_usd**: 769.86
- **planned_reward_usd**: 1634.64
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.738
- **exit_distance_from_sl_pct**: 0.6154
- **notional**: 102.17452

### Market excursion (MFE / MAE proxy)
- high_water: 72981.8 · low_water: 72888.4
- current_stop_at_close: 73531.7
- **mfe_pct**: 0.128
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2661

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.738%
- slippage vs planned SL: 0.6154%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - strong planned R:R=2.123
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617100+00:00Z · journaler v2*
