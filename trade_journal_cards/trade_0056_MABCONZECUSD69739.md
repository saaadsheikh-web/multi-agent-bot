# Trade #56 — ZEC-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.9390 (-1.653% if pct available) · **Decision grade:** A (100/100) · **Hold:** 87.11 min

> Long stopped out at full risk on ZEC-USDT (connors_rsi2, -1.65%) (was up 1.84% before reversing) trail gave back 3.50% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD69739`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T12:15:41.281458+00:00`
- closed: `2026-05-06T13:42:47.789446+00:00` · hour UTC 13 (Wed)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.8, in uptrend

### Parsed signal features
- **rsi2**: 4.8
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 559.48,
  "atr_tp": 579.36,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 568.08
- exit_price: 558.69
- tp_price: 579.36
- sl_price: 559.48
- qty: 1.0 · notional: 56.80800000000001
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9856
- **planned_sl_distance_pct**: 1.5139
- **planned_r_multiple**: 1.312
- **planned_risk_usd**: 8.6
- **planned_reward_usd**: 11.28
- **realized_r_multiple**: -0.109
- **exit_distance_from_tp_pct**: 3.6386
- **exit_distance_from_sl_pct**: -0.1391
- **notional**: 56.80800000000001

### Market excursion (MFE / MAE proxy)
- high_water: 578.56 · low_water: 568.08
- current_stop_at_close: 559.48
- **mfe_pct**: 1.8448
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 3.4977

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.109
- slippage vs planned TP: 3.6386%
- slippage vs planned SL: -0.1391%

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
`gave_back_winner`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559795Z · journaler v2*
