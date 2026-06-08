# Trade #311 — XMR-USDT long (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.0556 (-1.028% if pct available) · **Decision grade:** A (100/100) · **Hold:** 22.62 min

> Long stopped out at full risk on XMR-USDT (stoch_rsi, -1.03%) trail gave back 1.04% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXMRUSD46828`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XMR-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T20:47:09.566608+00:00`
- closed: `2026-06-01T21:09:47.020209+00:00` · hour UTC 21 (Mon)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.23 (was 0.00) rsi=40

### Parsed signal features
- **rsi**: 40.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 350.6481,
  "atr_tp": 359.50284999999997,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 354.19
- exit_price: 350.55
- tp_price: 359.5
- sl_price: 350.65
- qty: 2.9 · notional: 102.71509999999999
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.4992
- **planned_sl_distance_pct**: 0.9995
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 10.266
- **planned_reward_usd**: 15.399
- **realized_r_multiple**: -0.103
- **exit_distance_from_tp_pct**: 2.5269
- **exit_distance_from_sl_pct**: -0.0282
- **notional**: 102.71509999999999

### Market excursion (MFE / MAE proxy)
- high_water: 354.25 · low_water: 354.19
- current_stop_at_close: 350.65
- **mfe_pct**: 0.0169
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.0446

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.103
- slippage vs planned TP: 2.5269%
- slippage vs planned SL: -0.0282%

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
  - high confidence (9) lost

## 7 · Tags
`trail_too_loose`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618106+00:00Z · journaler v2*
