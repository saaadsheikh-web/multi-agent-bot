# Trade #18 — SOL-USDT long (daily_breakout_2h)

**Outcome:** WIN · **PnL:** +0.1380 (+0.272% if pct available) · **Decision grade:** A (100/100) · **Hold:** 16.94 min

> Long trailed into profit on SOL-USDT (daily_breakout_2h, +0.27%) [grade A / 100].

## 1 · Identity
- custom_id: `MABDAISOLUSD5616`
- agent: `daily_breakout_2h` · profile: `daily_breakout_2h`
- symbol: `SOL-USDT` · side: `long`
- confidence: 10
- opened: `2026-05-04T14:40:17.348940+00:00`
- closed: `2026-05-04T14:57:13.866901+00:00` · hour UTC 14 (Mon)

## 2 · Hypothesis (why we entered)
> 2 agents agree [daily_breakout_2h,hurst_regime] — best: 2h-high break long (84.2700) vol 1.4x

### Parsed signal features
- **atr_val**: 0.60295596171905
- **v_ratio**: 1.4391315559285869
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 84.03232,
  "atr_tp": 168.57289999999998,
  "atr_val": 0.60295596171905,
  "v_ratio": 1.4391315559285869
}
```

## 3 · Plan vs Execution
- entry_price: 84.69
- exit_price: 84.92
- tp_price: 168.57289999999998
- sl_price: 84.03232
- qty: 0.6 · notional: 50.814
- trail_pct: 0.4

### Risk plan
- **planned_tp_distance_pct**: 99.047
- **planned_sl_distance_pct**: 0.7766
- **planned_r_multiple**: 127.539
- **planned_risk_usd**: 0.3946
- **planned_reward_usd**: 50.3297
- **realized_r_multiple**: 0.35
- **exit_distance_from_tp_pct**: 98.7754
- **exit_distance_from_sl_pct**: 1.0482
- **notional**: 50.814

### Market excursion (MFE / MAE proxy)
- high_water: 85.27 · low_water: 84.69
- current_stop_at_close: 84.92891999999999
- **mfe_pct**: 0.6849
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.4133

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.35
- slippage vs planned TP: 98.7754%
- slippage vs planned SL: 1.0482%

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
  - strong planned R:R=127.539
  - multi-agent confluence

## 7 · Tags
`confluence`, `trail_stop`, `grade_A`

---
*journaled_at 2026-05-17T03:54:39.558312Z · journaler v2*
