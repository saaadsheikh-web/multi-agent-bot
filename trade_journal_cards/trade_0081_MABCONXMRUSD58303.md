# Trade #81 — XMR-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8008 (-1.500% if pct available) · **Decision grade:** A (100/100) · **Hold:** 16.93 min

> Long stopped out at full risk on XMR-USDT (connors_rsi2, -1.50%) trail gave back 1.60% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD58303`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-09T20:25:04.704678+00:00`
- closed: `2026-05-09T20:42:00.393994+00:00` · hour UTC 20 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.9, ATR%=0.24, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.9
- **atr_pct**: 0.24
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 404.4804,
  "atr_tp": 418.8528,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 410.64
- exit_price: 404.48
- tp_price: 418.85
- sl_price: 404.48
- qty: 1.3 · notional: 53.3832
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9993
- **planned_sl_distance_pct**: 1.5001
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 8.008
- **planned_reward_usd**: 10.673
- **realized_r_multiple**: -0.1
- **exit_distance_from_tp_pct**: 3.4994
- **exit_distance_from_sl_pct**: 0.0
- **notional**: 53.3832

### Market excursion (MFE / MAE proxy)
- high_water: 411.03 · low_water: 410.64
- current_stop_at_close: 404.48
- **mfe_pct**: 0.095
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.5951

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.1
- slippage vs planned TP: 3.4994%
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
  - high confidence (9) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.560650Z · journaler v2*
