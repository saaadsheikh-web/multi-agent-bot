# Trade #241 — BNB-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0048 (+0.005% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.15 min

> Long timed out in profit on BNB-USDT (connors_rsi2, +0.00%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD56309`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-26T00:45:10.954502+00:00`
- closed: `2026-05-26T00:50:19.895721+00:00` · hour UTC 00 (Tue)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=2.1, ATR%=0.11, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.1
- **atr_pct**: 0.11
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 650.72055,
  "atr_tp": 673.8426000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 660.64
- exit_price: 660.67
- tp_price: 673.84
- sl_price: 650.72
- qty: 16.0 · notional: 105.7024
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9981
- **planned_sl_distance_pct**: 1.5016
- **planned_r_multiple**: 1.331
- **planned_risk_usd**: 158.72
- **planned_reward_usd**: 211.2
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.9935
- **exit_distance_from_sl_pct**: 1.5061
- **notional**: 105.7024

### Market excursion (MFE / MAE proxy)
- high_water: 661.28 · low_water: 660.64
- current_stop_at_close: 650.72
- **mfe_pct**: 0.0969
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0923

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.9935%
- slippage vs planned SL: 1.5061%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`good_hour`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-26T03:01:12.558724Z · journaler v2*
