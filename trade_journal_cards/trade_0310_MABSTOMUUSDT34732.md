# Trade #310 — MU-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -0.0070 (-0.007% if pct available) · **Decision grade:** A (100/100) · **Hold:** 68.92 min

> Short gave back gains on trail on MU-USDT (stoch_rsi, -0.01%) during good-zone hour 18:00 UTC (was up 0.66% before reversing) trail gave back 0.67% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOMUUSDT34732`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `MU-USDT` · side: `short`
- confidence: 9
- opened: `2026-06-01T17:25:33.181608+00:00`
- closed: `2026-06-01T18:34:28.344013+00:00` · hour UTC 18 (Mon)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [swing,stoch_rsi,golden_hour] — best: StochRSI short stoch=0.77 (was 1.00) rsi=72

### Parsed signal features
- **rsi**: 72.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 1050.7939000000001,
  "atr_tp": 1024.7841500000002,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 1041.54
- exit_price: 1041.61
- tp_price: 1024.78
- sl_price: 1050.79
- qty: 10.0 · notional: 104.154
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.6092
- **planned_sl_distance_pct**: 0.8881
- **planned_r_multiple**: 1.812
- **planned_risk_usd**: 92.5
- **planned_reward_usd**: 167.6
- **realized_r_multiple**: -0.0
- **exit_distance_from_tp_pct**: 1.6159
- **exit_distance_from_sl_pct**: 0.8814
- **notional**: 104.154

### Market excursion (MFE / MAE proxy)
- high_water: 1041.54 · low_water: 1034.64
- current_stop_at_close: 1041.54
- **mfe_pct**: 0.6625
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.6692

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: -0.0
- slippage vs planned TP: 1.6159%
- slippage vs planned SL: 0.8814%

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
  - multi-agent confluence
  - high confidence (9) lost

## 7 · Tags
`good_hour`, `confluence`, `gave_back_winner`, `trail_too_loose`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.618044+00:00Z · journaler v2*
