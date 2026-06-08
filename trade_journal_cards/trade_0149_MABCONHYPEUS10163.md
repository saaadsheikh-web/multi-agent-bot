# Trade #149 — HYPE-USDT long (connors_rsi2)

**Outcome:** WIN · **PnL:** +0.9290 (+1.787% if pct available) · **Decision grade:** A (100/100) · **Hold:** 70.52 min

> Long trailed into profit on HYPE-USDT (connors_rsi2, +1.79%) [grade A / 100].

## 1 · Identity
- custom_id: `MABCONHYPEUS10163`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `HYPE-USDT` · side: `long`
- confidence: 9
- opened: `2026-05-20T20:49:25.049097+00:00`
- closed: `2026-05-20T21:59:56.019768+00:00` · hour UTC 21 (Wed)

## 2 · Hypothesis (why we entered)
> [trend+] Connors RSI2 long: RSI2=4.7, ATR%=0.45, uptrend slope-up

### Parsed signal features
- **rsi2**: 4.7
- **atr_pct**: 0.45
- **trend_score**: 3
- **trend_dir**: UP
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 51.213105,
  "atr_tp": 53.03286000000001,
  "_trend_score": 3,
  "_trend_dir": "UP"
}
```

## 3 · Plan vs Execution
- entry_price: 51.99
- exit_price: 52.919
- tp_price: 53.033
- sl_price: 51.213
- qty: 10.0 · notional: 51.99
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0062
- **planned_sl_distance_pct**: 1.4945
- **planned_r_multiple**: 1.342
- **planned_risk_usd**: 7.77
- **planned_reward_usd**: 10.43
- **realized_r_multiple**: 0.12
- **exit_distance_from_tp_pct**: 0.2193
- **exit_distance_from_sl_pct**: 3.2814
- **notional**: 51.99

### Market excursion (MFE / MAE proxy)
- high_water: 53.028 · low_water: 51.99
- current_stop_at_close: 52.709832
- **mfe_pct**: 1.9965
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.2097

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.12
- slippage vs planned TP: 0.2193%
- slippage vs planned SL: 3.2814%

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
`trail_stop`, `grade_A`

---
*journaled_at 2026-05-20T23:48:02.584841Z · journaler v2*
