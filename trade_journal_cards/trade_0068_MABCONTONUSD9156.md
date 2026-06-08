# Trade #68 — TON-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0760 (-0.149% if pct available) · **Decision grade:** C (70/100) · **Hold:** 53.5 min

> Long gave back gains on trail on TON-USDT (connors_rsi2, -0.15%) [flagged-losing-symbol] (was up 1.01% before reversing) trail gave back 1.16% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONTONUSD9156`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `TON-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-08T02:59:18.471683+00:00`
- closed: `2026-05-08T03:52:48.544791+00:00` · hour UTC 03 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.9, in uptrend

### Parsed signal features
- **rsi2**: 3.9
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 2.636845,
  "atr_tp": 2.73054,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 2.68
- exit_price: 2.676
- tp_price: 2.7305
- sl_price: 2.6368
- qty: 19.0 · notional: 50.92
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 1.8843
- **planned_sl_distance_pct**: 1.6119
- **planned_r_multiple**: 1.169
- **planned_risk_usd**: 0.8208
- **planned_reward_usd**: 0.9595
- **realized_r_multiple**: -0.093
- **exit_distance_from_tp_pct**: 2.0336
- **exit_distance_from_sl_pct**: 1.4627
- **notional**: 50.92

### Market excursion (MFE / MAE proxy)
- high_water: 2.707 · low_water: 2.68
- current_stop_at_close: 2.68
- **mfe_pct**: 1.0075
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.1567

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.093
- slippage vs planned TP: 2.0336%
- slippage vs planned SL: 1.4627%

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
  - high confidence (8) lost

## 7 · Tags
`losing_symbol`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.560175Z · journaler v2*
