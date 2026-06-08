# Trade #248 — HYPE-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.9200 (+0.895% if pct available) · **Decision grade:** A (100/100) · **Hold:** 30.74 min

> Short trailed into profit on HYPE-USDT (stoch_rsi, +0.89%) trail gave back 0.52% [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS4605`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-26T14:10:07.863420+00:00`
- closed: `2026-05-26T14:40:52.309778+00:00` · hour UTC 14 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=68

### Parsed signal features
- **rsi**: 68.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 64.8925,
  "atr_tp": 63.28625,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 64.26
- exit_price: 63.685
- tp_price: 63.286
- sl_price: 64.892
- qty: 16.0 · notional: 102.81600000000002
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5157
- **planned_sl_distance_pct**: 0.9835
- **planned_r_multiple**: 1.541
- **planned_risk_usd**: 10.112
- **planned_reward_usd**: 15.584
- **realized_r_multiple**: 0.091
- **exit_distance_from_tp_pct**: 0.6209
- **exit_distance_from_sl_pct**: 1.8783
- **notional**: 102.81600000000002

### Market excursion (MFE / MAE proxy)
- high_water: 64.26 · low_water: 63.354
- current_stop_at_close: 63.67076999999999
- **mfe_pct**: 1.4099
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.5151

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.091
- slippage vs planned TP: 0.6209%
- slippage vs planned SL: 1.8783%

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
`confluence`, `trail_too_loose`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-26T15:01:27.129070Z · journaler v2*
