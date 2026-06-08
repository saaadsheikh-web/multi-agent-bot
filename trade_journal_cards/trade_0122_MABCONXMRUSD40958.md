# Trade #122 — XMR-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0476 (+0.089% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.13 min

> Short timed out in profit on XMR-USDT (connors_rsi2, +0.09%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD40958`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T14:16:00.688431+00:00`
- closed: `2026-05-16T14:18:08.717171+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.0, ATR%=0.24, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.0
- **atr_pct**: 0.24
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 389.42505,
  "atr_tp": 375.9966,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 383.35
- exit_price: 383.01
- tp_price: 376.0
- sl_price: 389.43
- qty: 1.4 · notional: 53.669
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9173
- **planned_sl_distance_pct**: 1.586
- **planned_r_multiple**: 1.209
- **planned_risk_usd**: 8.512
- **planned_reward_usd**: 10.29
- **realized_r_multiple**: 0.006
- **exit_distance_from_tp_pct**: 1.8286
- **exit_distance_from_sl_pct**: 1.6747
- **notional**: 53.669

### Market excursion (MFE / MAE proxy)
- high_water: 383.35 · low_water: 383.08
- current_stop_at_close: 389.43
- **mfe_pct**: 0.0704
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.0183

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.006
- slippage vs planned TP: 1.8286%
- slippage vs planned SL: 1.6747%

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
`very_short_hold`, `short_win`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562861Z · journaler v2*
