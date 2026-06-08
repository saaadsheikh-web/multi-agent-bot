# Trade #60 — YFI-USDT long (vwap_reversion)

**Outcome:** WIN · **PnL:** +0.1302 (+0.260% if pct available) · **Decision grade:** D (45/100) · **Hold:** 7.05 min

> Long trailed into profit on YFI-USDT (vwap_reversion, +0.26%) [flagged-losing-symbol] [killed-agent] [grade D / 45].

## 1 · Identity
- custom_id: `MABVWAYFIUSD21174`
- agent: `vwap_reversion` · profile: `meanrev`
- symbol: `YFI-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-07T02:32:55.478058+00:00`
- closed: `2026-05-07T02:39:58.370737+00:00` · hour UTC 02 (Thu)

## 2 · Hypothesis (why we entered)
> VWAP fade long z=-2.38σ RSI 26 vol_recent=0.0x

### Parsed signal features
- **z_score**: -2.38
- **rsi**: 26.454583565767877
- **z**: -2.375052795700435
- **trend_score**: 0
- **trend_dir**: FLAT
- **vwap**: 2731.7509800392013

### Raw meta from agent
```json
{
  "vwap": 2731.7509800392013,
  "z": -2.375052795700435,
  "rsi": 26.454583565767877,
  "tp_price": 2731.7509800392013,
  "sl_price": 2687.2631235596673,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 2695.0
- exit_price: 2702.0
- tp_price: 2762.0
- sl_price: 2655.0
- qty: 186.0 · notional: 50.127
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4861
- **planned_sl_distance_pct**: 1.4842
- **planned_r_multiple**: 1.675
- **planned_risk_usd**: 7440.0
- **planned_reward_usd**: 12462.0
- **realized_r_multiple**: 0.0
- **exit_distance_from_tp_pct**: 2.2263
- **exit_distance_from_sl_pct**: 1.744
- **notional**: 50.127

### Market excursion (MFE / MAE proxy)
- high_water: 2702.0 · low_water: 2695.0
- current_stop_at_close: 2655.0
- **mfe_pct**: 0.2597
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.0
- slippage vs planned TP: 2.2263%
- slippage vs planned SL: 1.744%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: True
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** D (45/100)
- factors:
  - flagged-losing-symbol
  - agent-on-kill-list

## 7 · Tags
`losing_symbol`, `killed_agent`, `trail_stop`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.559909Z · journaler v2*
