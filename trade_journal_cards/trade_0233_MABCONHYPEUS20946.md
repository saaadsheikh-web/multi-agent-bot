# Trade #233 — HYPE-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0368 (-0.073% if pct available) · **Decision grade:** A (100/100) · **Hold:** 27.46 min

> Long gave back gains on trail on HYPE-USDT (connors_rsi2, -0.07%) (was up 0.67% before reversing) trail gave back 0.74% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS20946`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T14:55:48.241147+00:00`
- closed: `2026-05-25T15:23:16.064534+00:00` · hour UTC 15 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=0.9, ATR%=0.35, uptrend slope-up

### Parsed signal features
- **rsi2**: 0.9
- **atr_pct**: 0.35
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 61.739799999999995,
  "atr_tp": 63.9336,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 62.703
- exit_price: 62.657
- tp_price: 63.934
- sl_price: 61.74
- qty: 8.0 · notional: 50.162400000000005
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9632
- **planned_sl_distance_pct**: 1.5358
- **planned_r_multiple**: 1.278
- **planned_risk_usd**: 7.704
- **planned_reward_usd**: 9.848
- **realized_r_multiple**: -0.005
- **exit_distance_from_tp_pct**: 2.0366
- **exit_distance_from_sl_pct**: 1.4624
- **notional**: 50.162400000000005

### Market excursion (MFE / MAE proxy)
- high_water: 63.124 · low_water: 62.703
- current_stop_at_close: 62.703
- **mfe_pct**: 0.6714
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7448

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.005
- slippage vs planned TP: 2.0366%
- slippage vs planned SL: 1.4624%

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
  - high confidence (8) lost

## 7 · Tags
`gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905887Z · journaler v2*
