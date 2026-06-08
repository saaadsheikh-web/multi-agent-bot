# Trade #304 — XAUT-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0575 (+0.056% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.8 min

> Long timed out in profit on XAUT-USDT (stoch_rsi, +0.06%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAUTUS23082`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAUT-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T14:11:23.582426+00:00`
- closed: `2026-06-01T14:18:11.630044+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.28 (was 0.00) rsi=22

### Parsed signal features
- **rsi**: 22.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4401.837,
  "atr_tp": 4512.9945,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 4445.8
- exit_price: 4448.3
- tp_price: 4513.0
- sl_price: 4401.8
- qty: 23.0 · notional: 102.2534
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5115
- **planned_sl_distance_pct**: 0.9897
- **planned_r_multiple**: 1.527
- **planned_risk_usd**: 1012.0
- **planned_reward_usd**: 1545.6
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4553
- **exit_distance_from_sl_pct**: 1.0459
- **notional**: 102.2534

### Market excursion (MFE / MAE proxy)
- high_water: 4448.3 · low_water: 4445.8
- current_stop_at_close: 4401.8
- **mfe_pct**: 0.0562
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4553%
- slippage vs planned SL: 1.0459%

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
`confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617912+00:00Z · journaler v2*
