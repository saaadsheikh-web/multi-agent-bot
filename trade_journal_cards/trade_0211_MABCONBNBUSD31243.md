# Trade #211 — BNB-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.1152 (-0.219% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.12 min

> Long gave back gains on trail on BNB-USDT (connors_rsi2, -0.22%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD31243`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T14:00:44.778342+00:00`
- closed: `2026-05-24T20:00:52.101802+00:00` · hour UTC 20 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=4.2, ATR%=0.10, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.2
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 648.10045,
  "atr_tp": 671.1294,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 657.9
- exit_price: 656.46
- tp_price: 671.13
- sl_price: 648.1
- qty: 8.0 · notional: 52.632
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0109
- **planned_sl_distance_pct**: 1.4896
- **planned_r_multiple**: 1.35
- **planned_risk_usd**: 78.4
- **planned_reward_usd**: 105.84
- **realized_r_multiple**: -0.001
- **exit_distance_from_tp_pct**: 2.2298
- **exit_distance_from_sl_pct**: 1.2707
- **notional**: 52.632

### Market excursion (MFE / MAE proxy)
- high_water: 658.68 · low_water: 657.9
- current_stop_at_close: 648.1
- **mfe_pct**: 0.1186
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.3374

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.001
- slippage vs planned TP: 2.2298%
- slippage vs planned SL: 1.2707%

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
`long_hold`, `long_loss`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905598Z · journaler v2*
