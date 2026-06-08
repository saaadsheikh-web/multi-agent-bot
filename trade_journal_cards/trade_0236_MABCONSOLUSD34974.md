# Trade #236 — SOL-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7611 (-1.501% if pct available) · **Decision grade:** A (100/100) · **Hold:** 226.89 min

> Long stopped out at full risk on SOL-USDT (connors_rsi2, -1.50%) trail gave back 1.57% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONSOLUSD34974`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T18:49:36.828486+00:00`
- closed: `2026-05-25T22:36:30.410130+00:00` · hour UTC 22 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.3, ATR%=0.11, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.3
- **atr_pct**: 0.11
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 84.6706,
  "atr_tp": 87.6792,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 85.96
- exit_price: 84.67
- tp_price: 87.68
- sl_price: 84.67
- qty: 0.59 · notional: 50.71639999999999
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0009
- **planned_sl_distance_pct**: 1.5007
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 0.7611
- **planned_reward_usd**: 1.0148
- **realized_r_multiple**: -1.0
- **exit_distance_from_tp_pct**: 3.5016
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 50.71639999999999

### Market excursion (MFE / MAE proxy)
- high_water: 86.02 · low_water: 85.96
- current_stop_at_close: 84.67
- **mfe_pct**: 0.0698
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.5705

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.0
- slippage vs planned TP: 3.5016%
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
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905979Z · journaler v2*
