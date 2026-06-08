# Trade #213 — XMR-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0806 (+0.160% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.1 min

> Long trailed into profit on XMR-USDT (connors_rsi2, +0.16%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD32260`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T14:17:42.235609+00:00`
- closed: `2026-05-24T14:21:47.997889+00:00` · hour UTC 14 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.4, ATR%=0.24, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.4
- **atr_pct**: 0.24
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 381.12605,
  "atr_tp": 394.6686,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 387.11
- exit_price: 387.73
- tp_price: 394.67
- sl_price: 381.13
- qty: 1.3 · notional: 50.3243
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9529
- **planned_sl_distance_pct**: 1.5448
- **planned_r_multiple**: 1.264
- **planned_risk_usd**: 7.774
- **planned_reward_usd**: 9.828
- **realized_r_multiple**: 0.01
- **exit_distance_from_tp_pct**: 1.7928
- **exit_distance_from_sl_pct**: 1.7049
- **notional**: 50.3243

### Market excursion (MFE / MAE proxy)
- high_water: 387.87 · low_water: 387.11
- current_stop_at_close: 381.13
- **mfe_pct**: 0.1963
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0362

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.01
- slippage vs planned TP: 1.7928%
- slippage vs planned SL: 1.7049%

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
  - (no notable factors)

## 7 · Tags
`very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905570Z · journaler v2*
