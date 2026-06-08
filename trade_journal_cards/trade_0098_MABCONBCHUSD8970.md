# Trade #98 — BCH-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0288 (+0.053% if pct available) · **Decision grade:** A (100/100) · **Hold:** 3.77 min

> Short timed out in profit on BCH-USDT (connors_rsi2, +0.05%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBCHUSD8970`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BCH-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-11T14:16:11.876928+00:00`
- closed: `2026-05-11T14:19:57.803988+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=96.7, ATR%=0.13, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.7
- **atr_pct**: 0.13
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 457.76499999999993,
  "atr_tp": 441.98,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 450.74
- exit_price: 450.5
- tp_price: 441.98
- sl_price: 457.76
- qty: 1.2 · notional: 54.0888
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9435
- **planned_sl_distance_pct**: 1.5574
- **planned_r_multiple**: 1.248
- **planned_risk_usd**: 8.424
- **planned_reward_usd**: 10.512
- **realized_r_multiple**: 0.003
- **exit_distance_from_tp_pct**: 1.8902
- **exit_distance_from_sl_pct**: 1.6107
- **notional**: 54.0888

### Market excursion (MFE / MAE proxy)
- high_water: 450.74 · low_water: 450.4
- current_stop_at_close: 457.76
- **mfe_pct**: 0.0754
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0222

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.003
- slippage vs planned TP: 1.8902%
- slippage vs planned SL: 1.6107%

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
*journaled_at 2026-05-17T03:54:39.562083Z · journaler v2*
