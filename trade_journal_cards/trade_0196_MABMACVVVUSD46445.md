# Trade #196 — VVV-USDT long (macd_cross)

**Outcome:** WIN · **PnL:** +0.0493 (+0.098% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.4 min

> Long trailed into profit on VVV-USDT (macd_cross, +0.10%) [grade A / 100].

## 1 · Identity
- custom_id: `MABMACVVVUSD46445`
- agent: `macd_cross` · profile: `macd_cross`
- symbol: `VVV-USDT` · side: `long`
- confidence: 7
- opened: `2026-05-23T14:27:26.588381+00:00`
- closed: `2026-05-23T14:29:50.877095+00:00` · hour UTC 14 (Sat)

## 2 · Hypothesis (why we entered)
> MACD bull cross hist 0.0005 vol 2.1x

### Parsed signal features
- **atr_val**: 0.41103697436675396
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 16.754444538449867,
  "atr_tp": 18.60411092310026,
  "atr_val": 0.41103697436675396,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 17.369
- exit_price: 17.386
- tp_price: 18.604
- sl_price: 16.754
- qty: 29.0 · notional: 50.37010000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 7.1104
- **planned_sl_distance_pct**: 3.5408
- **planned_r_multiple**: 2.008
- **planned_risk_usd**: 17.835
- **planned_reward_usd**: 35.815
- **realized_r_multiple**: 0.003
- **exit_distance_from_tp_pct**: 7.0125
- **exit_distance_from_sl_pct**: 3.6387
- **notional**: 50.37010000000001

### Market excursion (MFE / MAE proxy)
- high_water: 17.402 · low_water: 17.369
- current_stop_at_close: 16.754
- **mfe_pct**: 0.19
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0921

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.003
- slippage vs planned TP: 7.0125%
- slippage vs planned SL: 3.6387%

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
  - strong planned R:R=2.008

## 7 · Tags
`very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570838Z · journaler v2*
