# Trade #91 — SUI-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.3600 (+0.710% if pct available) · **Decision grade:** C (70/100) · **Hold:** 44.91 min

> Long trailed into profit on SUI-USDT (connors_rsi2, +0.71%) [flagged-losing-symbol] trail gave back 0.69% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONSUIUSD82889`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SUI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T07:01:30.519299+00:00`
- closed: `2026-05-11T07:46:25.277356+00:00` · hour UTC 07 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.7, ATR%=0.83, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.7
- **atr_pct**: 0.83
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 1.2488815,
  "atr_tp": 1.293258,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1.268
- exit_price: 1.277
- tp_price: 1.2933
- sl_price: 1.2489
- qty: 40.0 · notional: 50.72
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9953
- **planned_sl_distance_pct**: 1.5063
- **planned_r_multiple**: 1.325
- **planned_risk_usd**: 0.764
- **planned_reward_usd**: 1.012
- **realized_r_multiple**: 0.471
- **exit_distance_from_tp_pct**: 1.2855
- **exit_distance_from_sl_pct**: 2.2161
- **notional**: 50.72

### Market excursion (MFE / MAE proxy)
- high_water: 1.2858 · low_water: 1.268
- current_stop_at_close: 1.2780852
- **mfe_pct**: 1.4038
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.694

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.471
- slippage vs planned TP: 1.2855%
- slippage vs planned SL: 2.2161%

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

## 7 · Tags
`losing_symbol`, `trail_too_loose`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.561887Z · journaler v2*
