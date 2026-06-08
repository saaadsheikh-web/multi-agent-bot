# Trade #49 — XMR-USDT short (funding_extremes)

**Outcome:** WIN · **PnL:** +0.3419 (+0.639% if pct available) · **Decision grade:** A (100/100) · **Hold:** 13.18 min

> Short trailed into profit on XMR-USDT (funding_extremes, +0.64%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNXMRUSD27001`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `XMR-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-06T00:23:22.600888+00:00`
- closed: `2026-05-06T00:36:33.534577+00:00` · hour UTC 00 (Wed)

## 2 · Hypothesis (why we entered)
> 2 agents agree (same-family) [funding,funding_extremes] — best: Funding extremes SHORT: fr=0.1043%/8h (annual≈114%), RSI=54, EMA50 slope=+0.42%

### Parsed signal features
- **rsi**: 53.59407122701259
- **atr_pct**: 1.3980562850955764
- **funding_rate**: 0.001043425148913029
- **ema_slope**: 0.4245638278977948
- **trend_score**: 0
- **trend_dir**: FLAT
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "funding_rate": 0.001043425148913029,
  "rsi": 53.59407122701259,
  "ema_slope": 0.4245638278977948,
  "atr_pct": 1.3980562850955764,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 411.44
- exit_price: 408.81
- tp_price: 404.03
- sl_price: 415.55
- qty: 1.3 · notional: 53.4872
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 1.801
- **planned_sl_distance_pct**: 0.9989
- **planned_r_multiple**: 1.803
- **planned_risk_usd**: 5.343
- **planned_reward_usd**: 9.633
- **realized_r_multiple**: 0.064
- **exit_distance_from_tp_pct**: 1.1618
- **exit_distance_from_sl_pct**: 1.6381
- **notional**: 53.4872

### Market excursion (MFE / MAE proxy)
- high_water: 411.44 · low_water: 408.37
- current_stop_at_close: 411.63696
- **mfe_pct**: 0.7462
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.1069

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.064
- slippage vs planned TP: 1.1618%
- slippage vs planned SL: 1.6381%

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
*journaled_at 2026-05-17T03:54:39.559526Z · journaler v2*
