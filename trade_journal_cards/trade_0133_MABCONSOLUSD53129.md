# Trade #133 — SOL-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.3630 (+2.706% if pct available) · **Decision grade:** A (100/100) · **Hold:** 138.72 min

> Clean short TP hit on SOL-USDT (connors_rsi2, +2.71%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONSOLUSD53129`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-17T21:25:32.927493+00:00`
- closed: `2026-05-17T23:44:16.142710+00:00` · hour UTC 23 (Sun)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.6, ATR%=0.10, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.6
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 88.1426,
  "atr_tp": 85.1032,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 86.84
- exit_price: 84.49
- tp_price: 85.1
- sl_price: 88.14
- qty: 0.58 · notional: 50.3672
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0037
- **planned_sl_distance_pct**: 1.497
- **planned_r_multiple**: 1.338
- **planned_risk_usd**: 0.754
- **planned_reward_usd**: 1.0092
- **realized_r_multiple**: 1.808
- **exit_distance_from_tp_pct**: -0.7024
- **exit_distance_from_sl_pct**: 4.2031
- **notional**: 50.3672

### Market excursion (MFE / MAE proxy)
- high_water: 86.84 · low_water: 84.41
- current_stop_at_close: 84.91646
- **mfe_pct**: 2.7982
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0921

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 1.808
- slippage vs planned TP: -0.7024%
- slippage vs planned SL: 4.2031%

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
`short_win`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-18T03:01:31.523904Z · journaler v2*
