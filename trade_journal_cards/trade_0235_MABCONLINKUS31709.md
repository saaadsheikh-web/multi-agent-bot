# Trade #235 — LINK-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7632 (-1.501% if pct available) · **Decision grade:** A (100/100) · **Hold:** 278.95 min

> Long stopped out at full risk on LINK-USDT (connors_rsi2, -1.50%) trail gave back 1.78% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONLINKUS31709`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `LINK-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T17:55:11.297588+00:00`
- closed: `2026-05-25T22:34:08.295622+00:00` · hour UTC 22 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.6, ATR%=0.15, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.6
- **atr_pct**: 0.15
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 9.45206,
  "atr_tp": 9.78792,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 9.596
- exit_price: 9.452
- tp_price: 9.788
- sl_price: 9.452
- qty: 5.3 · notional: 50.8588
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0008
- **planned_sl_distance_pct**: 1.5006
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 0.7632
- **planned_reward_usd**: 1.0176
- **realized_r_multiple**: -1.0
- **exit_distance_from_tp_pct**: 3.5015
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 50.8588

### Market excursion (MFE / MAE proxy)
- high_water: 9.623 · low_water: 9.596
- current_stop_at_close: 9.452
- **mfe_pct**: 0.2814
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.782

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.0
- slippage vs planned TP: 3.5015%
- slippage vs planned SL: 0.0%

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
`trail_too_loose`, `long_hold`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905965Z · journaler v2*
