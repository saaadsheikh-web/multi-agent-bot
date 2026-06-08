# Trade #232 — BNB-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.7400 (+1.378% if pct available) · **Decision grade:** A (100/100) · **Hold:** 240.04 min

> Short trailed into profit on BNB-USDT (stoch_rsi, +1.38%) during good-zone hour 18:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD18387`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-25T14:13:09.656317+00:00`
- closed: `2026-05-25T18:13:12.279886+00:00` · hour UTC 18 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI short stoch=0.87 rsi=73

### Parsed signal features
- **rsi**: 73.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 678.0534,
  "atr_tp": 661.2699,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 671.34
- exit_price: 662.09
- tp_price: 661.27
- sl_price: 678.05
- qty: 8.0 · notional: 53.7072
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5
- **planned_sl_distance_pct**: 0.9995
- **planned_r_multiple**: 1.501
- **planned_risk_usd**: 53.68
- **planned_reward_usd**: 80.56
- **realized_r_multiple**: 0.014
- **exit_distance_from_tp_pct**: 0.1221
- **exit_distance_from_sl_pct**: 2.3773
- **notional**: 53.7072

### Market excursion (MFE / MAE proxy)
- high_water: 671.34 · low_water: 661.34
- current_stop_at_close: 664.6467
- **mfe_pct**: 1.4896
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1117

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.014
- slippage vs planned TP: 0.1221%
- slippage vs planned SL: 2.3773%

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

## 7 · Tags
`good_hour`, `confluence`, `long_hold`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905921Z · journaler v2*
