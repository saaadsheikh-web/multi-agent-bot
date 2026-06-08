# Trade #314 — BCH-USDT long (funding_extremes)

**Outcome:** LOSS · **PnL:** -0.3185 (-0.313% if pct available) · **Decision grade:** A (90/100) · **Hold:** 15.29 min

> Long closed in the red without clean exit on BCH-USDT (funding_extremes, -0.31%) during good-zone hour 01:00 UTC [grade A / 90].

## 1 · Identity
- custom_id: `MABFUNBCHUSD63281`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T01:21:23.036308+00:00`
- closed: `2026-06-02T01:36:40.204459+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0517%/8h (annual≈-57%), RSI=47, EMA50 slope=-0.24%

### Parsed signal features
- **rsi**: 47.33602749934203
- **ema_slope**: -0.24482263708841545
- **atr_pct**: 1.0752203082892153
- **funding_rate**: -0.0005174545676632071
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.0005174545676632071,
  "rsi": 47.33602749934203,
  "ema_slope": -0.24482263708841545,
  "atr_pct": 1.0752203082892153,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 290.7
- exit_price: 289.79
- tp_price: 302.33
- sl_price: 281.98
- qty: 3.5 · notional: 101.745
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 4.0007
- **planned_sl_distance_pct**: 2.9997
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 30.52
- **planned_reward_usd**: 40.705
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 4.3137
- **exit_distance_from_sl_pct**: 2.6866
- **notional**: 101.745

### Market excursion (MFE / MAE proxy)
- high_water: 290.88 · low_water: 290.7
- current_stop_at_close: 281.98
- **mfe_pct**: 0.0619
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.375

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: -0.01
- slippage vs planned TP: 4.3137%
- slippage vs planned SL: 2.6866%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
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
`good_hour`, `long_loss`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618178+00:00Z · journaler v2*
