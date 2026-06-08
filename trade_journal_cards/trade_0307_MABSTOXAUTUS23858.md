# Trade #307 — XAUT-USDT long (stoch_rsi)

**Outcome:** WIN · **PnL:** +0.4485 (+0.438% if pct available) · **Decision grade:** A (100/100) · **Hold:** 360.06 min

> Long trailed into profit on XAUT-USDT (stoch_rsi, +0.44%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOXAUTUS23858`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `XAUT-USDT` · side: `long`
- confidence: 9
- opened: `2026-06-01T14:24:19.811436+00:00`
- closed: `2026-06-01T20:24:23.470526+00:00` · hour UTC 20 (Mon)

## 2 · Hypothesis (why we entered)
> 3 agents agree (same-family) [vwap_reversion,bb_bounce,stoch_rsi] — best: StochRSI long stoch=0.36 (was 0.00) rsi=23

### Parsed signal features
- **rsi**: 23.0
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 4403.619000000001,
  "atr_tp": 4514.8215,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 4448.1
- exit_price: 4467.6
- tp_price: 4514.8
- sl_price: 4403.6
- qty: 23.0 · notional: 102.30630000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 1.4995
- **planned_sl_distance_pct**: 1.0004
- **planned_r_multiple**: 1.499
- **planned_risk_usd**: 1023.5
- **planned_reward_usd**: 1534.1
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.0611
- **exit_distance_from_sl_pct**: 1.4388
- **notional**: 102.30630000000001

### Market excursion (MFE / MAE proxy)
- high_water: 4480.0 · low_water: 4448.1
- current_stop_at_close: 4448.1
- **mfe_pct**: 0.7172
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2788

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.0611%
- slippage vs planned SL: 1.4388%

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
*journaled_at 2026-06-05T21:57:18.618088+00:00Z · journaler v2*
