# Trade #170 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.0323 (+2.019% if pct available) · **Decision grade:** A (100/100) · **Hold:** 46.48 min

> Clean long TP hit on HYPE-USDT (connors_rsi2, +2.02%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS14109`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T01:41:51.045093+00:00`
- closed: `2026-05-22T02:28:19.943175+00:00` · hour UTC 02 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.4, ATR%=0.55, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.4
- **atr_pct**: 0.55
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 55.970655,
  "atr_tp": 57.95946,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 56.823
- exit_price: 57.97
- tp_price: 57.959
- sl_price: 55.971
- qty: 9.0 · notional: 51.1407
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9992
- **planned_sl_distance_pct**: 1.4994
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.668
- **planned_reward_usd**: 10.224
- **realized_r_multiple**: 0.135
- **exit_distance_from_tp_pct**: -0.0194
- **exit_distance_from_sl_pct**: 3.5179
- **notional**: 51.1407

### Market excursion (MFE / MAE proxy)
- high_water: 57.97 · low_water: 56.823
- current_stop_at_close: 57.62218
- **mfe_pct**: 2.0185
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.135
- slippage vs planned TP: -0.0194%
- slippage vs planned SL: 3.5179%

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
`tp_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570417Z · journaler v2*
