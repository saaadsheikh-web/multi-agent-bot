# Trade #46 — XMR-USDT short (funding_extremes)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (100/100) · **Hold:** 4.41 min

> Short flat exit (scratch) on XMR-USDT (funding_extremes, +0.00%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNXMRUSD17424`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-05T21:43:44.892617+00:00`
- closed: `2026-05-05T21:48:09.677565+00:00` · hour UTC 21 (Tue)

## 2 · Hypothesis (why we entered)
> 4 agents agree (cross-family) [bb_bounce,zscore_reversion,stoch_rsi,funding_extremes] — best: Funding extremes SHORT: fr=0.0561%/8h (annual≈61%), RSI=69, EMA50 slope=+0.52%

### Parsed signal features
- **rsi**: 68.82748472192615
- **atr_pct**: 1.2854105748508706
- **funding_rate**: 0.0005612446754578626
- **ema_slope**: 0.519070981893055
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.0005612446754578626,
  "rsi": 68.82748472192615,
  "ema_slope": 0.519070981893055,
  "atr_pct": 1.2854105748508706
}
```

## 3 · Plan vs Execution
- entry_price: 422.32
- exit_price: 422.32
- tp_price: 414.72
- sl_price: 426.54
- qty: 1.2 · notional: 50.678399999999996
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.7996
- **planned_sl_distance_pct**: 0.9992
- **planned_r_multiple**: 1.801
- **planned_risk_usd**: 5.064
- **planned_reward_usd**: 9.12
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 1.7996
- **exit_distance_from_sl_pct**: 0.9992
- **notional**: 50.678399999999996

### Market excursion (MFE / MAE proxy)
- high_water: 422.32 · low_water: 421.33
- current_stop_at_close: 426.54
- **mfe_pct**: 0.2344
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2344

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 1.7996%
- slippage vs planned SL: 0.9992%

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
`confluence`, `very_short_hold`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559434Z · journaler v2*
