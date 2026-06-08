# Trade #281 — HYPE-USDT short (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.8085 (+0.755% if pct available) · **Decision grade:** A (100/100) · **Hold:** 6.75 min

> Short trailed into profit on HYPE-USDT (stoch_rsi, +0.76%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOHYPEUS62680`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `HYPE-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-31T21:24:41.541608+00:00`
- closed: `2026-05-31T21:31:26.432186+00:00` · hour UTC 21 (Sun)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [bb_bounce,stoch_rsi] — best: StochRSI short stoch=1.00 rsi=72

### Parsed signal features
- **rsi**: 72.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 72.1342,
  "atr_tp": 70.3487,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 71.365
- exit_price: 70.826
- tp_price: 70.349
- sl_price: 72.134
- qty: 15.0 · notional: 107.04749999999999
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.4237
- **planned_sl_distance_pct**: 1.0776
- **planned_r_multiple**: 1.321
- **planned_risk_usd**: 11.535
- **planned_reward_usd**: 15.24
- **realized_r_multiple**: 0.07
- **exit_distance_from_tp_pct**: 0.6684
- **exit_distance_from_sl_pct**: 1.8328
- **notional**: 107.04749999999999

### Market excursion (MFE / MAE proxy)
- high_water: 71.365 · low_water: 70.859
- current_stop_at_close: 71.21329499999999
- **mfe_pct**: 0.709
- **mae_pct**: 0.0
- **trail_gave_back_pct**: -0.0462

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.07
- slippage vs planned TP: 0.6684%
- slippage vs planned SL: 1.8328%

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
`confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617458+00:00Z · journaler v2*
