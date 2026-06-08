# Trade #303 — XAU-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.5531 (+0.539% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.14 min

> Long trailed into profit on XAU-USDT (stoch_rsi, +0.54%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAUUSD22950`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAU-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T14:09:11.550745+00:00`
- closed: `2026-06-01T20:09:19.826342+00:00` · hour UTC 20 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.29 (was 0.00) rsi=20

### Parsed signal features
- **rsi**: 20.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4413.9348,
  "atr_tp": 4525.3978,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 4458.52
- exit_price: 4482.57
- tp_price: 4525.4
- sl_price: 4413.93
- qty: 23.0 · notional: 102.54596000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.5
- **planned_sl_distance_pct**: 1.0001
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1025.57
- **planned_reward_usd**: 1538.24
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 0.9606
- **exit_distance_from_sl_pct**: 1.5395
- **notional**: 102.54596000000001

### Market excursion (MFE / MAE proxy)
- high_water: 4494.88 · low_water: 4458.52
- current_stop_at_close: 4458.52
- **mfe_pct**: 0.8155
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2761

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.001
- slippage vs planned TP: 0.9606%
- slippage vs planned SL: 1.5395%

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
`confluence`, `long_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618065+00:00Z · journaler v2*
