# Trade #214 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0680 (+0.132% if pct available) · **Decision grade:** A (100/100) · **Hold:** 7.03 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.13%) trail gave back 0.74% [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD32350`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-24T14:19:11.881384+00:00`
- closed: `2026-05-24T14:26:13.472725+00:00` · hour UTC 14 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=1.1, ATR%=0.80, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.1
- **atr_pct**: 0.8
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 633.1579999999999,
  "atr_tp": 655.656,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 642.8
- exit_price: 643.65
- tp_price: 655.66
- sl_price: 633.16
- qty: 0.8 · notional: 51.42400000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0006
- **planned_sl_distance_pct**: 1.4997
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 7.712
- **planned_reward_usd**: 10.288
- **realized_r_multiple**: 0.009
- **exit_distance_from_tp_pct**: 1.8684
- **exit_distance_from_sl_pct**: 1.6319
- **notional**: 51.42400000000001

### Market excursion (MFE / MAE proxy)
- high_water: 648.43 · low_water: 642.8
- current_stop_at_close: 644.53942
- **mfe_pct**: 0.8759
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.7436

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.009
- slippage vs planned TP: 1.8684%
- slippage vs planned SL: 1.6319%

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
*journaled_at 2026-05-25T23:01:34.905584Z · journaler v2*
