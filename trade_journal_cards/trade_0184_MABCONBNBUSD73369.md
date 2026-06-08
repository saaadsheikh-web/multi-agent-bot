# Trade #184 — BNB-USDT long (connors_rsi2)

**Outcome:** LOSS · **PnL:** -0.7928 (-1.503% if pct available) · **Decision grade:** A (100/100) · **Hold:** 81.5 min

> Long stopped out at full risk on BNB-USDT (connors_rsi2, -1.50%) during good-zone hour 19:00 UTC [grade A / 100].

## 1 · Identity
- custom_id: `MABCONBNBUSD73369`
- agent: `connors_rsi2` · profile: `connors_rsi2`
- symbol: `BNB-USDT` · side: `long`
- confidence: 8
- opened: `2026-05-22T18:09:31.358229+00:00`
- closed: `2026-05-22T19:31:01.178585+00:00` · hour UTC 19 (Fri)

## 2 · Hypothesis (why we entered)
> Connors RSI2 long: RSI2=3.6, ATR%=0.14, uptrend slope-up

### Parsed signal features
- **rsi2**: 3.6
- **atr_pct**: 0.14
- **trend_score**: 0
- **trend_dir**: FLAT
- **regime_hint**: uptrend

### Raw meta from agent
```json
{
  "atr_sl": 649.4499000000001,
  "atr_tp": 672.5268000000001,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 659.34
- exit_price: 649.43
- tp_price: 672.53
- sl_price: 649.45
- qty: 8.0 · notional: 52.74720000000001
- trail_pct: 0.6

### Risk plan
- **planned_tp_distance_pct**: 2.0005
- **planned_sl_distance_pct**: 1.5
- **planned_r_multiple**: 1.334
- **planned_risk_usd**: 79.12
- **planned_reward_usd**: 105.52
- **realized_r_multiple**: -0.01
- **exit_distance_from_tp_pct**: 3.5035
- **exit_distance_from_sl_pct**: -0.003
- **notional**: 52.74720000000001

### Market excursion (MFE / MAE proxy)
- high_water: 659.34 · low_water: 659.34
- current_stop_at_close: 649.45
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.01
- slippage vs planned TP: 3.5035%
- slippage vs planned SL: -0.003%

## 5 · Context flags
- **in_dead_zone**: False
- **in_good_zone**: True
- **symbol_blacklisted**: False
- **agent_killed**: False
- **paper_only**: False
- **multi_agent_confluence**: False

## 6 · Decision quality
- **grade:** A (100/100)
- factors:
  - high confidence (8) lost

## 7 · Tags
`good_hour`, `long_loss`, `sl_hit`, `grade_A`

---
*journaled_at 2026-05-23T15:00:56.570682Z · journaler v2*
