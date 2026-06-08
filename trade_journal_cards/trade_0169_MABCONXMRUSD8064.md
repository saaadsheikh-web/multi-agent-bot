# Trade #169 — XMR-USDT short (connors_rsi2)

**Outcome:** WIN · **PnL:** +1.0400 (+2.034% if pct available) · **Decision grade:** A (100/100) · **Hold:** 22.32 min

> Clean short TP hit on XMR-USDT (connors_rsi2, +2.03%) during good-zone hour 00:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONXMRUSD8064`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `XMR-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-22T00:01:06.105602+00:00`
- closed: `2026-05-22T00:23:25.420999+00:00` · hour UTC 00 (Fri)

## 2 · Hypothesis (why we entered)
> 3 agents agree (cross-family) [funding,connors_rsi2,hurst_regime] — best: Connors RSI2 short: RSI2=96.4, ATR%=0.28, downtrend slope-down

### Parsed signal features
- **rsi2**: 96.4
- **atr_pct**: 0.28
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: downtrend
- **multi_agent_confluence**: True

### Raw meta from agent
```json
{
  "atr_sl": 399.5852,
  "atr_tp": 385.8064,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 393.35
- exit_price: 385.35
- tp_price: 385.81
- sl_price: 399.59
- qty: 1.3 · notional: 51.13550000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 1.9169
- **planned_sl_distance_pct**: 1.5864
- **planned_r_multiple**: 1.208
- **planned_risk_usd**: 8.112
- **planned_reward_usd**: 9.802
- **realized_r_multiple**: 0.128
- **exit_distance_from_tp_pct**: -0.1169
- **exit_distance_from_sl_pct**: 3.6202
- **notional**: 51.13550000000001

### Market excursion (MFE / MAE proxy)
- high_water: 393.35 · low_water: 385.35
- current_stop_at_close: 387.6621
- **mfe_pct**: 2.0338
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `TP_HIT`
- realized_r_multiple: 0.128
- slippage vs planned TP: -0.1169%
- slippage vs planned SL: 3.6202%

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
`good_hour`, `confluence`, `short_win`, `tp_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570401Z · journaler v2*
