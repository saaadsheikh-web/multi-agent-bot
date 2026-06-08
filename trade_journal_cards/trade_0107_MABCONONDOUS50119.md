# Trade #107 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.1144 (+2.228% if pct available) · **Decision grade:** C (70/100) · **Hold:** 8.67 min

> Clean long TP hit on ONDO-USDT (connors_rsi2, +2.23%) during good-zone hour 01:00 UTC [flagged-losing-symbol] [grade C / 70].

## 1 · Identity
- custom_id: `MABCONONDOUS50119`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-12T01:42:01.032069+00:00`
- closed: `2026-05-12T01:50:41.122571+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.0, ATR%=0.68, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.0
- **atr_pct**: 0.68
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 0.420398,
  "atr_tp": 0.435336,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4263
- exit_price: 0.4358
- tp_price: 0.4353
- sl_price: 0.4204
- qty: 1173.0 · notional: 50.00499000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.1112
- **planned_sl_distance_pct**: 1.384
- **planned_r_multiple**: 1.525
- **planned_risk_usd**: 6.9207
- **planned_reward_usd**: 10.557
- **realized_r_multiple**: 0.161
- **exit_distance_from_tp_pct**: -0.1173
- **exit_distance_from_sl_pct**: 3.6125
- **notional**: 50.00499000000001

### Market excursion (MFE / MAE proxy)
- high_water: 0.4358 · low_water: 0.4263
- current_stop_at_close: 0.4331852
- **mfe_pct**: 2.2285
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.161
- slippage vs planned TP: -0.1173%
- slippage vs planned SL: 3.6125%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol

## 7 · Tags
`good_hour`, `losing_symbol`, `tp_hit`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.562395Z · journaler v2*
