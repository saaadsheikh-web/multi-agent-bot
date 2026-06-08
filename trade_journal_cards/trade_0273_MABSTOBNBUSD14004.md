# Trade #273 — BNB-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.0624 (-1.006% if pct available) · **Decision grade:** A (100/100) · **Hold:** 108.25 min

> Short stopped out at full risk on BNB-USDT (stoch_rsi, -1.01%) during good-zone hour 05:00 UTC trail gave back 1.47% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD14004`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-30T04:06:46.128468+00:00`
- closed: `2026-05-30T05:55:01.352576+00:00` · hour UTC 05 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=78

### Parsed signal features
- **rsi**: 78.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 666.6202,
  "atr_tp": 650.1197,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 660.02
- exit_price: 666.66
- tp_price: 650.12
- sl_price: 666.62
- qty: 16.0 · notional: 105.6032
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5
- **planned_sl_distance_pct**: 1.0
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 105.6
- **planned_reward_usd**: 158.4
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 2.506
- **exit_distance_from_sl_pct**: -0.0061
- **notional**: 105.6032

### Market excursion (MFE / MAE proxy)
- high_water: 660.02 · low_water: 656.94
- current_stop_at_close: 666.62
- **mfe_pct**: 0.4667
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.4727

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.01
- slippage vs planned TP: 2.506%
- slippage vs planned SL: -0.0061%

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
`good_hour`, `confluence`, `trail_too_loose`, `sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617335+00:00Z · journaler v2*
