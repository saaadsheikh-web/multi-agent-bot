# Trade #127 — ZEC-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.2300 (+0.447% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.58 min

> Short trailed into profit on ZEC-USDT (connors_rsi2, +0.45%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD72229`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-16T22:57:11.041413+00:00`
- closed: `2026-05-16T22:59:46.104177+00:00` · hour UTC 22 (Sat)

## 2 · Hypothesis (why we entered)
> Connors RSI2 short: RSI2=97.4, ATR%=0.28, downtrend slope-down

### Parsed signal features
- **rsi2**: 97.4
- **atr_pct**: 0.28
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend

### Raw meta from agent
```json
{
  "atr_sl": 522.0144999999999,
  "atr_tp": 504.01399999999995,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 514.3
- exit_price: 512.0
- tp_price: 504.01
- sl_price: 522.01
- qty: 1.0 · notional: 51.43
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0008
- **planned_sl_distance_pct**: 1.4991
- **planned_r_multiple**: 1.335
- **planned_risk_usd**: 7.71
- **planned_reward_usd**: 10.29
- **realized_r_multiple**: 0.03
- **exit_distance_from_tp_pct**: 1.5536
- **exit_distance_from_sl_pct**: 1.9463
- **notional**: 51.43

### Market excursion (MFE / MAE proxy)
- high_water: 514.3 · low_water: 512.0
- current_stop_at_close: 522.01
- **mfe_pct**: 0.4472
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.03
- slippage vs planned TP: 1.5536%
- slippage vs planned SL: 1.9463%

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
`very_short_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.563009Z · journaler v2*
