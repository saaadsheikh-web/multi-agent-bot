# Trade #28 — BCH-USDT short (hurst_regime)

**Outcome:** FLAT · **PnL:** +0.0000 (+0.000% if pct available) · **Decision grade:** A (95/100) · **Hold:** 25.66 min

> Short flat exit (scratch) on BCH-USDT (hurst_regime, +0.00%) during good-zone hour 01:00 UTC [killed-agent] [grade A / 95].

## 1 · Identity
- custom_id: `MABHURBCHUSD42319`
- agent: `hurst_regime` · profile: `hurst_regime`
- symbol: `BCH-USDT` · side: `short`
- confidence: 8
- opened: `2026-05-05T00:52:00.792506+00:00`
- closed: `2026-05-05T01:17:40.286005+00:00` · hour UTC 01 (Tue)

## 2 · Hypothesis (why we entered)
> 2 agents agree [connors_rsi2,hurst_regime] — best: Hurst trend-regime short H=0.967 below EMA21

### Parsed signal features
- **hurst**: 0.9667908275359981
- **atr_val**: 2.2142884874972557
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 447.4214327312459,
  "atr_tp": 4.441000000000001,
  "hurst": 0.9667908275359981,
  "atr_val": 2.2142884874972557
}
```

## 3 · Plan vs Execution
- entry_price: 444.1
- exit_price: 444.1
- tp_price: 4.44
- sl_price: 447.42
- qty: 1.2 · notional: 53.292
- trail_pct: 0.8

### Risk plan
- **planned_tp_distance_pct**: 99.0002
- **planned_sl_distance_pct**: 0.7476
- **planned_r_multiple**: 132.424
- **planned_risk_usd**: 3.984
- **planned_reward_usd**: 527.592
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 99.0002
- **exit_distance_from_sl_pct**: 0.7476
- **notional**: 53.292

### Market excursion (MFE / MAE proxy)
- high_water: 444.1 · low_water: 443.7
- current_stop_at_close: 447.42
- **mfe_pct**: 0.0901
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0901

## 4 · Forensics
- **exit_reason:** `TIME_OR_MANUAL`
- realized_r_multiple: 0.0
- slippage vs planned TP: 99.0002%
- slippage vs planned SL: 0.7476%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: True

## 6 · Decision quality
- **grade:** A (95/100)
- factors:
  - agent-on-kill-list
  - strong planned R:R=132.424
  - multi-agent confluence

## 7 · Tags
`good_hour`, `killed_agent`, `confluence`, `time_or_manual`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558815Z · journaler v2*
