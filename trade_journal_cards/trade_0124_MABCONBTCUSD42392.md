# Trade #124 — BTC-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0748 (-0.137% if pct available) · **Decision grade:** A (90/100) · **Hold:** 360.03 min

> Short closed in the red without clean exit on BTC-USDT (connors_rsi2, -0.14%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONBTCUSD42392`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BTC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T14:39:54.275240+00:00`
- closed: `2026-05-16T20:39:55.977581+00:00` · hour UTC 20 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=95.1, ATR%=0.10, downtrend slope-down

### Parsed signal features
- **rsi2**: 95.1
- **atr_pct**: 0.1
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 79268.252,
  "atr_tp": 76534.864,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 78096.8
- exit_price: 78203.6
- tp_price: 76534.9
- sl_price: 79268.3
- qty: 0.7 · notional: 54.66776
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0
- **planned_sl_distance_pct**: 1.5001
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 820.05
- **planned_reward_usd**: 1093.33
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 2.1367
- **exit_distance_from_sl_pct**: 1.3633
- **notional**: 54.66776

### Market excursion (MFE / MAE proxy)
- high_water: 78096.8 · low_water: 78037.0
- current_stop_at_close: 79268.3
- **mfe_pct**: 0.0766
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2133

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.0
- slippage vs planned TP: 2.1367%
- slippage vs planned SL: 1.3633%

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
`long_hold`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562949Z · journaler v2*
