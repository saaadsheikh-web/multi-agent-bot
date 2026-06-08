# Trade #116 — SOL-USDT short (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.0605 (-0.119% if pct available) · **Decision grade:** A (90/100) · **Hold:** 6.3 min

> Short closed in the red without clean exit on SOL-USDT (connors_rsi2, -0.12%) [grade A / 90].

## 1 · Identity
- custom_id: `MABCONSOLUSD70400`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SOL-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-14T14:53:22.541968+00:00`
- closed: `2026-05-14T14:59:40.826382+00:00` · hour UTC 14 (Thu)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.3, ATR%=0.28, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.3
- **atr_pct**: 0.28
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 93.49164999999999,
  "atr_tp": 90.2678,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 92.09
- exit_price: 92.2
- tp_price: 90.27
- sl_price: 93.49
- qty: 0.55 · notional: 50.6495
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9763
- **planned_sl_distance_pct**: 1.5203
- **planned_r_multiple**: 1.3
- **planned_risk_usd**: 0.77
- **planned_reward_usd**: 1.001
- **realized_r_multiple**: -0.079
- **exit_distance_from_tp_pct**: 2.0958
- **exit_distance_from_sl_pct**: 1.4008
- **notional**: 50.6495

### Market excursion (MFE / MAE proxy)
- high_water: 92.09 · low_water: 92.09
- current_stop_at_close: 93.49
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.079
- slippage vs planned TP: 2.0958%
- slippage vs planned SL: 1.4008%

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
`time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562676Z · journaler v2*
