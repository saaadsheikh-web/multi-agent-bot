# Trade #57 — TAO-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8432 (-1.611% if pct available) · **Decision grade:** C (70/100) · **Hold:** 6.48 min

> Long stopped out at full risk on TAO-USDT (connors_rsi2, -1.61%) [flagged-losing-symbol] trail gave back 1.65% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONTAOUSD72496`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `TAO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-06T13:01:37.606313+00:00`
- closed: `2026-05-06T13:08:06.572061+00:00` · hour UTC 13 (Wed)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=3.3, in uptrend

### Parsed signal features
- **rsi2**: 3.3
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 303.35045,
  "atr_tp": 314.12940000000003,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 307.97
- exit_price: 303.01
- tp_price: 314.13
- sl_price: 303.35
- qty: 17.0 · notional: 52.35490000000001
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 2.0002
- **planned_sl_distance_pct**: 1.5001
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 78.54
- **planned_reward_usd**: 104.72
- **realized_r_multiple**: -0.011
- **exit_distance_from_tp_pct**: 3.6107
- **exit_distance_from_sl_pct**: -0.1104
- **notional**: 52.35490000000001

### Market excursion (MFE / MAE proxy)
- high_water: 308.1 · low_water: 307.97
- current_stop_at_close: 303.35
- **mfe_pct**: 0.0422
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.6528

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.011
- slippage vs planned TP: 3.6107%
- slippage vs planned SL: -0.1104%

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
*journaled_at 2026-05-17T03:54:39.559767Z · journaler v2*
