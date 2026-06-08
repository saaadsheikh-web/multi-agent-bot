# Trade #271 — BNB-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0768 (+0.074% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.56 min

> Short timed out in profit on BNB-USDT (stoch_rsi, +0.07%) during good-zone hour 01:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD4658`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-30T01:30:59.635381+00:00`
- closed: `2026-05-30T01:36:32.959831+00:00` · hour UTC 01 (Sat)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [vwap_reversion,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=66

### Parsed signal features
- **rsi**: 66.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 654.4295000000001,
  "atr_tp": 638.2307500000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 648.05
- exit_price: 647.57
- tp_price: 638.23
- sl_price: 654.43
- qty: 16.0 · notional: 103.68799999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5153
- **planned_sl_distance_pct**: 0.9845
- **planned_r_multiple**: 1.539
- **planned_risk_usd**: 102.08
- **planned_reward_usd**: 157.12
- **realized_r_multiple**: 0.001
- **exit_distance_from_tp_pct**: 1.4412
- **exit_distance_from_sl_pct**: 1.0586
- **notional**: 103.68799999999999

### Market excursion (MFE / MAE proxy)
- high_water: 648.05 · low_water: 647.52
- current_stop_at_close: 654.43
- **mfe_pct**: 0.0818
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0077

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.001
- slippage vs planned TP: 1.4412%
- slippage vs planned SL: 1.0586%

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
`good_hour`, `confluence`, `short_win`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617260+00:00Z · journaler v2*
