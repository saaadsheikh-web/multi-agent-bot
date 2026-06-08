# Trade #244 — ONDO-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0729 (-0.073% if pct available) · **Decision grade:** C (70/100) · **Hold:** 23.38 min

> Long gave back gains on trail on ONDO-USDT (stoch_rsi, -0.07%) [flagged-losing-symbol] (was up 0.51% before reversing) trail gave back 0.58% [grade C / 70].

## 1 · Identity
- custom_id: `MABSTOONDOUS64676`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-26T03:04:38.369610+00:00`
- closed: `2026-05-26T03:28:01.130279+00:00` · hour UTC 03 (Tue)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.13 rsi=34

### Parsed signal features
- **rsi**: 34.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 0.407682,
  "atr_tp": 0.41797699999999993,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4118
- exit_price: 0.4115
- tp_price: 0.418
- sl_price: 0.4077
- qty: 2429.0 · notional: 100.02622000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5056
- **planned_sl_distance_pct**: 0.9956
- **planned_r_multiple**: 1.512
- **planned_risk_usd**: 9.9589
- **planned_reward_usd**: 15.0598
- **realized_r_multiple**: -0.007
- **exit_distance_from_tp_pct**: 1.5784
- **exit_distance_from_sl_pct**: 0.9228
- **notional**: 100.02622000000001

### Market excursion (MFE / MAE proxy)
- high_water: 0.4139 · low_water: 0.4118
- current_stop_at_close: 0.4118305
- **mfe_pct**: 0.51
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5828

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.007
- slippage vs planned TP: 1.5784%
- slippage vs planned SL: 0.9228%

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
`losing_symbol`, `gave_back_winner`, `trail_too_loose`, `long_loss`, `trail_stop`, `grade_C`

---
*journaled_at 2026-05-26T07:01:11.917120Z · journaler v2*
