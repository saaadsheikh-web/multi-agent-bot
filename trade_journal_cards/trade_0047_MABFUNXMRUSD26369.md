# Trade #47 — XMR-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.1001 (+0.187% if pct available) · **Decision grade:** A (100/100) · **Hold:** 9.38 min

> Short trailed into profit on XMR-USDT (funding_extremes, +0.19%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNXMRUSD26369`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-06T00:12:50.958279+00:00`
- closed: `2026-05-06T00:22:14.039563+00:00` · hour UTC 00 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [funding,funding_extremes] — best: Funding extremes SHORT: fr=0.1015%/8h (annual≈111%), RSI=55, EMA50 slope=+0.43%

### Parsed signal features
- **rsi**: 54.85269823247769
- **atr_pct**: 1.3833285093447223
- **funding_rate**: 0.001014536549222931
- **ema_slope**: 0.4345091564936565
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.001014536549222931,
  "rsi": 54.85269823247769,
  "ema_slope": 0.4345091564936565,
  "atr_pct": 1.3833285093447223
}
```

## 3 · Plan vs Execution
- entry_price: 412.18
- exit_price: 411.41
- tp_price: 404.76
- sl_price: 416.3
- qty: 1.3 · notional: 53.583400000000005
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.8002
- **planned_sl_distance_pct**: 0.9996
- **planned_r_multiple**: 1.801
- **planned_risk_usd**: 5.356
- **planned_reward_usd**: 9.646
- **realized_r_multiple**: 0.019
- **exit_distance_from_tp_pct**: 1.6134
- **exit_distance_from_sl_pct**: 1.1864
- **notional**: 53.583400000000005

### Market excursion (MFE / MAE proxy)
- high_water: 412.18 · low_water: 410.35
- current_stop_at_close: 416.3
- **mfe_pct**: 0.444
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2572

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.019
- slippage vs planned TP: 1.6134%
- slippage vs planned SL: 1.1864%

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
`good_hour`, `confluence`, `short_win`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.559480Z · journaler v2*
