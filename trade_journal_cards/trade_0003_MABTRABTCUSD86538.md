# Trade #3 — BTC-USDT long (tradingview)

**Outcome:** WIN · **PnL:** +0.4340 (+0.172% if pct available) · **Decision grade:** A (100/100) · **Hold:** 25.72 min

> Long trailed into profit on BTC-USDT (tradingview, +0.17%) [grade A / 100].

## 1 · Identity
- custom_id: `MABTRABTCUSD86538`
- agent: `tradingview` · profile: `momentum`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-04-30T22:02:19.756515+00:00`
- closed: `2026-04-30T22:28:02.764887+00:00` · hour UTC 22 (Thu)

## 2 · Hypothesis (why we entered)
> TradingView/trend_pullback conf=9

### Parsed signal features
- **strategy**: trend_pullback

### Raw meta from agent
```json
{
  "strategy": "trend_pullback",
  "price_hint": null
}
```

## 3 · Plan vs Execution
- entry_price: 76248.7
- exit_price: 76380.2
- tp_price: 78536.161
- sl_price: 75333.7156
- qty: 3.3 · notional: 251.62071
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 3.0
- **planned_sl_distance_pct**: 1.2
- **planned_r_multiple**: 2.5
- **planned_risk_usd**: 3019.4485
- **planned_reward_usd**: 7548.6213
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.8275
- **exit_distance_from_sl_pct**: 1.3725
- **notional**: 251.62071

### Market excursion (MFE / MAE proxy)
- high_water: 76381.0 · low_water: 76248.7
- current_stop_at_close: 75333.7156
- **mfe_pct**: 0.1735
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.001

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.8275%
- slippage vs planned SL: 1.3725%

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
  - strong planned R:R=2.5

## 7 · Tags
`trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.557753Z · journaler v2*
