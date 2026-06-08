# Trade #231 — BNB-USDT short (zscore_reversion)

**Outcome:** WIN · **PnL:** +0.0168 (+0.031% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.12 min

> Short timed out in profit on BNB-USDT (zscore_reversion, +0.03%) [grade A / 100].

## 1 · Identity
- custom_id: `MABZSCBNBUSD18065`
- agent: `zscore_reversion` · profile: `zscore_reversion`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-25T14:07:47.780196+00:00`
- closed: `2026-05-25T14:11:55.006256+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 3 agents agree (same-family) [bb_bounce,zscore_reversion,stoch_rsi] — best: z-score short z=2.58 mean=655.6885

### Parsed signal features
- **z_score**: 2.58
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 678.4613383025901,
  "atr_tp": 655.6885000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 672.08
- exit_price: 671.87
- tp_price: 655.69
- sl_price: 678.46
- qty: 8.0 · notional: 53.766400000000004
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 2.4387
- **planned_sl_distance_pct**: 0.9493
- **planned_r_multiple**: 2.569
- **planned_risk_usd**: 51.04
- **planned_reward_usd**: 131.12
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.4075
- **exit_distance_from_sl_pct**: 0.9805
- **notional**: 53.766400000000004

### Market excursion (MFE / MAE proxy)
- high_water: 672.08 · low_water: 671.5
- current_stop_at_close: 678.46
- **mfe_pct**: 0.0863
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0551

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.4075%
- slippage vs planned SL: 0.9805%

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
  - strong planned R:R=2.569
  - multi-agent confluence

## 7 · Tags
`confluence`, `very_short_hold`, `short_win`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-25T23:01:34.905871Z · journaler v2*
