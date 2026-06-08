# Trade #238 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7048 (-1.336% if pct available) · **Decision grade:** A (100/100) · **Hold:** 181.36 min

> Long stopped out at full risk on ZEC-USDT (connors_rsi2, -1.34%) trail gave back 1.79% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD35768`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T19:02:50.533498+00:00`
- closed: `2026-05-25T22:04:12.327640+00:00` · hour UTC 22 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.4, ATR%=0.46, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.4
- **atr_pct**: 0.46
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 650.5038499999999,
  "atr_tp": 673.6182,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 659.3
- exit_price: 650.49
- tp_price: 673.62
- sl_price: 650.5
- qty: 0.8 · notional: 52.74400000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.172
- **planned_sl_distance_pct**: 1.3347
- **planned_r_multiple**: 1.627
- **planned_risk_usd**: 7.04
- **planned_reward_usd**: 11.456
- **realized_r_multiple**: -0.1
- **exit_distance_from_tp_pct**: 3.5083
- **exit_distance_from_sl_pct**: -0.0015
- **notional**: 52.74400000000001

### Market excursion (MFE / MAE proxy)
- high_water: 662.26 · low_water: 659.3
- current_stop_at_close: 650.5
- **mfe_pct**: 0.449
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.7852

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.1
- slippage vs planned TP: 3.5083%
- slippage vs planned SL: -0.0015%

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
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905951Z · journaler v2*
