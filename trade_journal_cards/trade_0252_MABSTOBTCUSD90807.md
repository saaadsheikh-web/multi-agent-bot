# Trade #252 — BTC-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.3531 (-0.336% if pct available) · **Decision grade:** A (100/100) · **Hold:** 240.07 min

> Long gave back gains on trail on BTC-USDT (stoch_rsi, -0.34%) during good-zone hour 18:00 UTC trail gave back 0.82% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBTCUSD90807`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-27T14:06:49.878752+00:00`
- closed: `2026-05-27T18:06:54.177836+00:00` · hour UTC 18 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.11 rsi=30

### Parsed signal features
- **rsi**: 30.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 74353.95,
  "atr_tp": 76231.575,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 75106.6
- exit_price: 74854.4
- tp_price: 76231.6
- sl_price: 74353.9
- qty: 1.4 · notional: 105.14924
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4979
- **planned_sl_distance_pct**: 1.0022
- **planned_r_multiple**: 1.495
- **planned_risk_usd**: 1053.78
- **planned_reward_usd**: 1575.0
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.8337
- **exit_distance_from_sl_pct**: 0.6664
- **notional**: 105.14924

### Market excursion (MFE / MAE proxy)
- high_water: 75471.5 · low_water: 75106.6
- current_stop_at_close: 74353.9
- **mfe_pct**: 0.4858
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.8216

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.8337%
- slippage vs planned SL: 0.6664%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence
  - high confidence (8) lost

## 7 · Tags
`good_hour`, `confluence`, `trail_too_loose`, `long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-27T19:00:51.546124Z · journaler v2*
