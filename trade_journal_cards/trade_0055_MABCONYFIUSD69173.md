# Trade #55 — YFI-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7783 (-1.554% if pct available) · **Decision grade:** C (70/100) · **Hold:** 120.48 min

> Long stopped out at full risk on YFI-USDT (connors_rsi2, -1.55%) [flagged-losing-symbol] trail gave back 1.66% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONYFIUSD69173`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `YFI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T12:06:14.384942+00:00`
- closed: `2026-05-06T14:06:43.319785+00:00` · hour UTC 14 (Wed)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.9, in uptrend

### Parsed signal features
- **rsi2**: 2.9
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 2725.495,
  "atr_tp": 2822.34,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 2767.0
- exit_price: 2724.0
- tp_price: 2822.0
- sl_price: 2725.0
- qty: 181.0 · notional: 50.0827
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.9877
- **planned_sl_distance_pct**: 1.5179
- **planned_r_multiple**: 1.31
- **planned_risk_usd**: 7602.0
- **planned_reward_usd**: 9955.0
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 3.5417
- **exit_distance_from_sl_pct**: -0.0361
- **notional**: 50.0827

### Market excursion (MFE / MAE proxy)
- high_water: 2770.0 · low_water: 2767.0
- current_stop_at_close: 2725.0
- **mfe_pct**: 0.1084
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.6625

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.0
- slippage vs planned TP: 3.5417%
- slippage vs planned SL: -0.0361%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol
  - high confidence (9) lost

## 7 · Tags
`losing_symbol`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.559821Z · journaler v2*
