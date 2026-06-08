# Trade #224 — BNB-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1120 (+0.213% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.38 min

> Long trailed into profit on BNB-USDT (connors_rsi2, +0.21%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD74386`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-25T01:59:48.459780+00:00`
- closed: `2026-05-25T02:05:11.378923+00:00` · hour UTC 02 (Mon)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=0.4, ATR%=0.11, uptrend slope-up

### Parsed signal features
- **rsi2**: 0.4
- **atr_pct**: 0.11
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 646.3570000000001,
  "atr_tp": 669.3240000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 656.15
- exit_price: 657.55
- tp_price: 669.32
- sl_price: 646.36
- qty: 8.0 · notional: 52.492
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0072
- **planned_sl_distance_pct**: 1.492
- **planned_r_multiple**: 1.345
- **planned_risk_usd**: 78.32
- **planned_reward_usd**: 105.36
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 1.7938
- **exit_distance_from_sl_pct**: 1.7054
- **notional**: 52.492

### Market excursion (MFE / MAE proxy)
- high_water: 657.6 · low_water: 656.15
- current_stop_at_close: 646.36
- **mfe_pct**: 0.221
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0076

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 1.7938%
- slippage vs planned SL: 1.7054%

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
`trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905718Z · journaler v2*
