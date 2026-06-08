# Trade #70 — TON-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.8170 (-1.584% if pct available) · **Decision grade:** D (55/100) · **Hold:** 7.96 min

> Long stopped out at full risk on TON-USDT (connors_rsi2, -1.58%) during dead-zone hour 09:00 UTC [flagged-losing-symbol] trail gave back 1.84% [grade D / 55].

## 1 · Identity
- custom_id: `MABCONTONUSD30609`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `TON-USDT` · side: `long`
- confidence: 6
- opened: `2026-05-08T08:56:50.348760+00:00`
- closed: `2026-05-08T09:04:48.245311+00:00` · hour UTC 09 (Fri)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=3.7, in uptrend

### Parsed signal features
- **rsi2**: 3.7
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 2.67526,
  "atr_tp": 2.7703200000000003,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 2.715
- exit_price: 2.672
- tp_price: 2.7703
- sl_price: 2.6753
- qty: 19.0 · notional: 51.584999999999994
- trail_pct: 1.5

### Risk plan
- **planned_tp_distance_pct**: 2.0368
- **planned_sl_distance_pct**: 1.4622
- **planned_r_multiple**: 1.393
- **planned_risk_usd**: 0.7543
- **planned_reward_usd**: 1.0507
- **realized_r_multiple**: -1.083
- **exit_distance_from_tp_pct**: 3.6206
- **exit_distance_from_sl_pct**: -0.1215
- **notional**: 51.584999999999994

### Market excursion (MFE / MAE proxy)
- high_water: 2.722 · low_water: 2.715
- current_stop_at_close: 2.6753
- **mfe_pct**: 0.2578
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 1.8416

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -1.083
- slippage vs planned TP: 3.6206%
- slippage vs planned SL: -0.1215%

## 5 · Context flags
- **in_dead_zone**: True
- **in_good_zone**: False
- **symbol_blacklisted**: True
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** D (55/100)
- factors:
  - flagged-losing-symbol
  - dead-zone-hour

## 7 · Tags
`dead_hour`, `losing_symbol`, `trail_too_loose`, `long_loss`, `sl_hit`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.560257Z · journaler v2*
