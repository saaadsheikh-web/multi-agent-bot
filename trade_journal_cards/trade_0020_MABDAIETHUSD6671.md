# Trade #20 — ETH-USDT long (daily_breakout_4h)

**Outcome:** LOSS · **PnL:** -0.6536 (-1.252% if pct available) · **Decision grade:** A (90/100) · **Hold:** 22.42 min

> Long stopped out at full risk on ETH-USDT (daily_breakout_4h, -1.25%) [flagged-losing-symbol] trail gave back 1.30% [grade A / 90].

## 1 · Identity
- custom_id: `MABDAIETHUSD6671`
- agent: `daily_breakout_4h` · profile: `daily_breakout_4h`
- symbol: `ETH-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T14:57:52.831469+00:00`
- closed: `2026-05-04T15:20:17.837172+00:00` · hour UTC 15 (Mon)

## 2 · Hypothesis (why we entered)
> 3 agents agree [daily_breakout_4h,daily_breakout_2h,hurst_regime] — best: 4h-high break long (2368.8100) vol 1.6x

### Parsed signal features
- **atr_val**: 20.604078657205207
- **v_ratio**: 1.6013379094900946
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 2343.62492,
  "atr_tp": 4720.4591,
  "atr_val": 20.604078657205207,
  "v_ratio": 1.6013379094900946
}
```

## 3 · Plan vs Execution
- entry_price: 2372.09
- exit_price: 2342.38
- tp_price: 4720.4591
- sl_price: 2343.62492
- qty: 2.2 · notional: 52.18598000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 99.0
- **planned_sl_distance_pct**: 1.2
- **planned_r_multiple**: 82.5
- **planned_risk_usd**: 62.6232
- **planned_reward_usd**: 5166.412
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 100.2525
- **exit_distance_from_sl_pct**: -0.0525
- **notional**: 52.18598000000001

### Market excursion (MFE / MAE proxy)
- high_water: 2373.24 · low_water: 2372.09
- current_stop_at_close: 2343.62492
- **mfe_pct**: 0.0485
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.301

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.01
- slippage vs planned TP: 100.2525%
- slippage vs planned SL: -0.0525%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - flagged-losing-symbol
  - strong planned R:R=82.5
  - multi-agent confluence
  - high confidence (10) lost

## 7 · Tags
`losing_symbol`, `confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558386Z · journaler v2*
