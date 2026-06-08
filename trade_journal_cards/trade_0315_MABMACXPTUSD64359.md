# Trade #315 — XPT-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +1.5059 (+1.491% if pct available) · **Decision grade:** A (100/100) · **Hold:** 232.85 min

> Clean long TP hit on XPT-USDT (macd_cross, +1.49%) during good-zone hour 05:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABMACXPTUSD64359`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `XPT-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-02T01:39:20.393713+00:00`
- closed: `2026-06-02T05:32:11.134366+00:00` · hour UTC 05 (Tue)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [daily_breakout_4h,daily_breakout_2h,macd_cross,hurst_regime] — best: MACD bull cross hist 0.3360 vol 1.5x

### Parsed signal features
- **atr_val**: 9.446415264790401
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1928.3703771028145,
  "atr_tp": 1970.8792457943712,
  "atr_val": 9.446415264790401,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1942.54
- exit_price: 1971.5
- tp_price: 1970.88
- sl_price: 1928.37
- qty: 52.0 · notional: 101.01208000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.4589
- **planned_sl_distance_pct**: 0.7295
- **planned_r_multiple**: 2.0
- **planned_risk_usd**: 736.84
- **planned_reward_usd**: 1473.68
- **realized_r_multiple**: 0.002
- **exit_distance_from_tp_pct**: -0.0319
- **exit_distance_from_sl_pct**: 2.2203
- **notional**: 101.01208000000001

### Market excursion (MFE / MAE proxy)
- high_water: 1971.5 · low_water: 1942.54
- current_stop_at_close: 1950.31016
- **mfe_pct**: 1.4908
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.002
- slippage vs planned TP: -0.0319%
- slippage vs planned SL: 2.2203%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - strong planned R:R=2.0
  - multi-agent confluence

## 7 · Tags
`good_hour`, `confluence`, `tp_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618307+00:00Z · journaler v2*
