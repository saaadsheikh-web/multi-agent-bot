# Trade #162 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.4840 (+0.931% if pct available) · **Decision grade:** A (100/100) · **Hold:** 40.26 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.93%) trail gave back 0.74% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD75150`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-21T14:52:31.542115+00:00`
- closed: `2026-05-21T15:32:47.195426+00:00` · hour UTC 15 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.7, ATR%=0.58, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.7
- **atr_pct**: 0.58
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 640.4667000000001,
  "atr_tp": 663.2244000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 650.18
- exit_price: 656.23
- tp_price: 663.22
- sl_price: 640.47
- qty: 0.8 · notional: 52.01440000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0056
- **planned_sl_distance_pct**: 1.4934
- **planned_r_multiple**: 1.343
- **planned_risk_usd**: 7.768
- **planned_reward_usd**: 10.432
- **realized_r_multiple**: 0.062
- **exit_distance_from_tp_pct**: 1.0751
- **exit_distance_from_sl_pct**: 2.4239
- **notional**: 52.01440000000001

### Market excursion (MFE / MAE proxy)
- high_water: 661.07 · low_water: 650.18
- current_stop_at_close: 657.1035800000001
- **mfe_pct**: 1.6749
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7444

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.062
- slippage vs planned TP: 1.0751%
- slippage vs planned SL: 2.4239%

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
*journaled_at 2026-05-23T15:00:56.570244Z · journaler v2*
