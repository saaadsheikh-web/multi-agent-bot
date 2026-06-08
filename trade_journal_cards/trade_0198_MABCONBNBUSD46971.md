# Trade #198 — BNB-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0216 (-0.042% if pct available) · **Decision grade:** A (90/100) · **Hold:** 3.8 min

> Short closed in the red without clean exit on BNB-USDT (connors_rsi2, -0.04%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBNBUSD46971`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-23T14:36:12.977280+00:00`
- closed: `2026-05-23T14:40:00.787491+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=98.8, ATR%=0.09, downtrend slope-down

### Parsed signal features
- **rsi2**: 98.8
- **atr_pct**: 0.09
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 654.7968,
  "atr_tp": 632.2176,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 645.3
- exit_price: 645.57
- tp_price: 632.22
- sl_price: 654.8
- qty: 8.0 · notional: 51.623999999999995
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.027
- **planned_sl_distance_pct**: 1.4722
- **planned_r_multiple**: 1.377
- **planned_risk_usd**: 76.0
- **planned_reward_usd**: 104.64
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.0688
- **exit_distance_from_sl_pct**: 1.4303
- **notional**: 51.623999999999995

### Market excursion (MFE / MAE proxy)
- high_water: 645.3 · low_water: 645.17
- current_stop_at_close: 654.8
- **mfe_pct**: 0.0201
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.062

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.0688%
- slippage vs planned SL: 1.4303%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (90/100)
- factors:
  - timed-out loser (no clean exit signal)
  - high confidence (9) lost

## 7 · Tags
`very_short_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570868Z · journaler v2*
