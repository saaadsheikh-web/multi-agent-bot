# Trade #225 — BCH-USDT long (funding_extremes)

**Outcome:** WIN · **PnL:** +0.1050 (+0.204% if pct available) · **Decision grade:** A (100/100) · **Hold:** 5.33 min

> Long trailed into profit on BCH-USDT (funding_extremes, +0.20%) [grade A / 100].

## 1 · Identity
- custom_id: `MABFUNBCHUSD78000`
- agent: `funding_extremes` · profile: `meanrev`
- symbol: `BCH-USDT` · side: `long`
- confidence: 6
- opened: `2026-05-25T03:00:01.569835+00:00`
- closed: `2026-05-25T03:05:21.211782+00:00` · hour UTC 03 (Mon)

## 2 · Hypothesis (why we entered)
> Funding extremes LONG: fr=-0.0509%/8h (annual≈-56%), RSI=36, EMA50 slope=-0.41%

### Parsed signal features
- **rsi**: 36.42043265626609
- **ema_slope**: -0.40551722728062733
- **atr_pct**: 0.9274659336008388
- **funding_rate**: -0.000509408982251589
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "funding_rate": -0.000509408982251589,
  "rsi": 36.42043265626609,
  "ema_slope": -0.40551722728062733,
  "atr_pct": 0.9274659336008388,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 343.7
- exit_price: 344.4
- tp_price: 352.29
- sl_price: 338.54
- qty: 1.5 · notional: 51.55500000000001
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4993
- **planned_sl_distance_pct**: 1.5013
- **planned_r_multiple**: 1.665
- **planned_risk_usd**: 7.74
- **planned_reward_usd**: 12.885
- **realized_r_multiple**: 0.014
- **exit_distance_from_tp_pct**: 2.2956
- **exit_distance_from_sl_pct**: 1.705
- **notional**: 51.55500000000001

### Market excursion (MFE / MAE proxy)
- high_water: 344.6 · low_water: 343.7
- current_stop_at_close: 338.54
- **mfe_pct**: 0.2619
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 0.0582

## 4 · Forensics
- **exit_reason:** `TRAIL_STOP`
- realized_r_multiple: 0.014
- slippage vs planned TP: 2.2956%
- slippage vs planned SL: 1.705%

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
*journaled_at 2026-05-25T23:01:34.905769Z · journaler v2*
