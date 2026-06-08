# Trade #102 — SUI-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7878 (-1.542% if pct available) · **Decision grade:** C (70/100) · **Hold:** 84.04 min

> Long stopped out at full risk on SUI-USDT (connors_rsi2, -1.54%) [flagged-losing-symbol] trail gave back 1.87% [grade C / 70].

## 1 · Identity
- custom_id: `MABCONSUIUSD29205`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `SUI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T19:53:26.848893+00:00`
- closed: `2026-05-11T21:17:29.498571+00:00` · hour UTC 21 (Mon)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=2.6, ATR%=0.58, uptrend slope-up

### Parsed signal features
- **rsi2**: 2.6
- **atr_pct**: 0.58
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 1.291138,
  "atr_tp": 1.337016,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 1.31
- exit_price: 1.2898
- tp_price: 1.337
- sl_price: 1.2911
- qty: 39.0 · notional: 51.09
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0611
- **planned_sl_distance_pct**: 1.4427
- **planned_r_multiple**: 1.429
- **planned_risk_usd**: 0.7371
- **planned_reward_usd**: 1.053
- **realized_r_multiple**: -1.069
- **exit_distance_from_tp_pct**: 3.6031
- **exit_distance_from_sl_pct**: -0.0992
- **notional**: 51.09

### Market excursion (MFE / MAE proxy)
- high_water: 1.3143 · low_water: 1.31
- current_stop_at_close: 1.2911
- **mfe_pct**: 0.3282
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.8702

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.069
- slippage vs planned TP: 3.6031%
- slippage vs planned SL: -0.0992%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** C (70/100)
- factors:
  - flagged-losing-symbol
  - high confidence (9) lost

## 7 · Tags
`losing_symbol`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_C`

---
*journaled_at 2026-05-17T03:54:39.562273Z · journaler v2*
