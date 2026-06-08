# Trade #230 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1256 (+0.239% if pct available) · **Decision grade:** A (100/100) · **Hold:** 26.24 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.24%) trail gave back 0.66% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD90318`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T06:25:20.071055+00:00`
- closed: `2026-05-25T06:51:34.626527+00:00` · hour UTC 06 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.7, ATR%=0.35, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.7
- **atr_pct**: 0.35
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 646.05165,
  "atr_tp": 669.0078,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 655.89
- exit_price: 657.46
- tp_price: 669.01
- sl_price: 646.05
- qty: 0.8 · notional: 52.47120000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0003
- **planned_sl_distance_pct**: 1.5003
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.872
- **planned_reward_usd**: 10.496
- **realized_r_multiple**: 0.016
- **exit_distance_from_tp_pct**: 1.761
- **exit_distance_from_sl_pct**: 1.7396
- **notional**: 52.47120000000001

### Market excursion (MFE / MAE proxy)
- high_water: 661.78 · low_water: 655.89
- current_stop_at_close: 657.80932
- **mfe_pct**: 0.898
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6586

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.016
- slippage vs planned TP: 1.761%
- slippage vs planned SL: 1.7396%

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
`trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905814Z · journaler v2*
