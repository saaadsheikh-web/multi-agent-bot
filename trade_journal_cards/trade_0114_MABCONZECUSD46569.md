# Trade #114 — ZEC-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.1080 (+0.207% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.12 min

> Long trailed into profit on ZEC-USDT (connors_rsi2, +0.21%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONZECUSD46569`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ZEC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-13T04:29:30.841018+00:00`
- closed: `2026-05-13T04:31:38.331674+00:00` · hour UTC 04 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [rsi_divergence,connors_rsi2] — best: Connors RSI2 long: RSI2=1.5, ATR%=0.39, uptrend slope-up

### Parsed signal features
- **rsi2**: 1.5
- **atr_pct**: 0.39
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 569.95055,
  "atr_tp": 590.2026,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 578.63
- exit_price: 579.83
- tp_price: 590.2
- sl_price: 569.95
- qty: 0.9 · notional: 52.0767
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9996
- **planned_sl_distance_pct**: 1.5001
- **planned_r_multiple**: 1.333
- **planned_risk_usd**: 7.812
- **planned_reward_usd**: 10.413
- **realized_r_multiple**: 0.014
- **exit_distance_from_tp_pct**: 1.7922
- **exit_distance_from_sl_pct**: 1.7075
- **notional**: 52.0767

### Market excursion (MFE / MAE proxy)
- high_water: 579.84 · low_water: 578.63
- current_stop_at_close: 569.95
- **mfe_pct**: 0.2091
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0017

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.014
- slippage vs planned TP: 1.7922%
- slippage vs planned SL: 1.7075%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - multi-agent confluence

## 7 · Tags
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.562617Z · journaler v2*
