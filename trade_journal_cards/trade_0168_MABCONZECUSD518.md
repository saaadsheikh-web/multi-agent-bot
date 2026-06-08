# Trade #168 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.9776 (-1.820% if pct available) · **Decision grade:** A (100/100) · **Hold:** 147.53 min

> Long stopped out at full risk on ZEC-USDT (connors_rsi2, -1.82%) during good-zone hour 00:00 UTC trail gave back 2.06% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD518`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T21:55:20.415713+00:00`
- closed: `2026-05-22T00:22:52.013675+00:00` · hour UTC 00 (Fri)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [connors_rsi2,hurst_regime] — best: Connors RSI2 long: RSI2=2.3, ATR%=0.42, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.3
- **atr_pct**: 0.42
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 661.3585499999999,
  "atr_tp": 684.8585999999999,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 671.43
- exit_price: 659.21
- tp_price: 684.86
- sl_price: 661.36
- qty: 0.8 · notional: 53.714400000000005
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0002
- **planned_sl_distance_pct**: 1.4998
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 8.056
- **planned_reward_usd**: 10.744
- **realized_r_multiple**: -0.121
- **exit_distance_from_tp_pct**: 3.8202
- **exit_distance_from_sl_pct**: -0.3202
- **notional**: 53.714400000000005

### Market excursion (MFE / MAE proxy)
- high_water: 673.07 · low_water: 671.43
- current_stop_at_close: 661.36
- **mfe_pct**: 0.2443
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 2.0643

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.121
- slippage vs planned TP: 3.8202%
- slippage vs planned SL: -0.3202%

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
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `confluence`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570377Z · journaler v2*
