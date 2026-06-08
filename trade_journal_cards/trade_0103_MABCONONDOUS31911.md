# Trade #103 — ONDO-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.0579 (+0.116% if pct available) · **Decision grade:** B (80/100) · **Hold:** 2.05 min

> Long trailed into profit on ONDO-USDT (connors_rsi2, +0.12%) [flagged-losing-symbol] [grade B / 80].

## 1 · Identity
- custom_id: `MABCONONDOUS31911`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `ONDO-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-11T20:38:32.654068+00:00`
- closed: `2026-05-11T20:40:35.583925+00:00` · hour UTC 20 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (cross-family) [ema_ribbon,connors_rsi2] — best: Connors RSI2 long: RSI2=3.6, ATR%=0.45, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.6
- **atr_pct**: 0.45
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 0.4254215,
  "atr_tp": 0.44053800000000004,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 0.4319
- exit_price: 0.4324
- tp_price: 0.4405
- sl_price: 0.4254
- qty: 1158.0 · notional: 50.01402
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9912
- **planned_sl_distance_pct**: 1.505
- **planned_r_multiple**: 1.323
- **planned_risk_usd**: 7.527
- **planned_reward_usd**: 9.9588
- **realized_r_multiple**: 0.008
- **exit_distance_from_tp_pct**: 1.8754
- **exit_distance_from_sl_pct**: 1.6207
- **notional**: 50.01402

### Market excursion (MFE / MAE proxy)
- high_water: 0.4324 · low_water: 0.4319
- current_stop_at_close: 0.4254
- **mfe_pct**: 0.1158
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.008
- slippage vs planned TP: 1.8754%
- slippage vs planned SL: 1.6207%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** B (80/100)
- factors:
  - flagged-losing-symbol
  - multi-agent confluence

## 7 · Tags
`losing_symbol`, `confluence`, `very_short_hold`, `trail_stop`, `grade_B`

---
*journaled_at 2026-05-17T03:54:39.562196Z · journaler v2*
