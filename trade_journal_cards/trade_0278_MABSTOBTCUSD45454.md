# Trade #278 — BTC-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.0645 (+0.063% if pct available) · **Decision grade:** A (100/100) · **Hold:** 2.58 min

> Long trailed into profit on BTC-USDT (stoch_rsi, +0.06%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBTCUSD45454`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BTC-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-31T16:37:36.327333+00:00`
- closed: `2026-05-31T16:40:11.197545+00:00` · hour UTC 16 (Sun)

## 2 · Hypothesis (why we entered)
> StochRSI long stoch=0.00 rsi=34

### Parsed signal features
- **rsi**: 34.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 72678.96900000001,
  "atr_tp": 74514.2965,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 73413.1
- exit_price: 73459.2
- tp_price: 74514.3
- sl_price: 72679.0
- qty: 1.4 · notional: 102.77834
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5
- **planned_sl_distance_pct**: 1.0
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 1027.74
- **planned_reward_usd**: 1541.68
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.4372
- **exit_distance_from_sl_pct**: 1.0628
- **notional**: 102.77834

### Market excursion (MFE / MAE proxy)
- high_water: 73509.6 · low_water: 73413.1
- current_stop_at_close: 72679.0
- **mfe_pct**: 0.1314
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0687

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.4372%
- slippage vs planned SL: 1.0628%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - (no notable factors)

## 7 · Tags
`very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617400+00:00Z · journaler v2*
