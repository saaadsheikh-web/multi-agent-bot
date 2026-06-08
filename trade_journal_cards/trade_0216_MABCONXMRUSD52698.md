# Trade #216 — XMR-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0156 (-0.031% if pct available) · **Decision grade:** A (100/100) · **Hold:** 28.66 min

> Long gave back gains on trail on XMR-USDT (connors_rsi2, -0.03%) (was up 0.66% before reversing) trail gave back 0.69% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD52698`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T19:58:19.538935+00:00`
- closed: `2026-05-24T20:26:59.093775+00:00` · hour UTC 20 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.9, ATR%=0.35, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.9
- **atr_pct**: 0.35
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 386.76025,
  "atr_tp": 400.503,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 393.12
- exit_price: 393.0
- tp_price: 400.5
- sl_price: 386.76
- qty: 1.3 · notional: 51.1056
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.8773
- **planned_sl_distance_pct**: 1.6178
- **planned_r_multiple**: 1.16
- **planned_risk_usd**: 8.268
- **planned_reward_usd**: 9.594
- **realized_r_multiple**: -0.002
- **exit_distance_from_tp_pct**: 1.9078
- **exit_distance_from_sl_pct**: 1.5873
- **notional**: 51.1056

### Market excursion (MFE / MAE proxy)
- high_water: 395.72 · low_water: 393.12
- current_stop_at_close: 393.12
- **mfe_pct**: 0.6614
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6919

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.002
- slippage vs planned TP: 1.9078%
- slippage vs planned SL: 1.5873%

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
*journaled_at 2026-05-25T23:01:34.905643Z · journaler v2*
