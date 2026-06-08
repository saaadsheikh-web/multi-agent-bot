# Trade #272 — BNB-USDT short (stoch_rsi)

**Outcome:** LOSS · **PnL:** -1.1024 (-1.064% if pct available) · **Decision grade:** A (100/100) · **Hold:** 20.13 min

> Short stopped out at full risk on BNB-USDT (stoch_rsi, -1.06%) [grade A / 100].

## 1 · Identity
- custom_id: `MABSTOBNBUSD5201`
- agent: `stoch_rsi` · profile: `stoch_rsi`
- symbol: `BNB-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-30T01:40:02.612533+00:00`
- closed: `2026-05-30T02:00:10.486255+00:00` · hour UTC 02 (Sat)

## 2 · Hypothesis (why we entered)
> StochRSI short stoch=1.00 rsi=65

### Parsed signal features
- **rsi**: 65.0
- **trend_score**: 0
- **trend_dir**: FLAT

### Raw meta from agent
```json
{
  "atr_sl": 654.3184,
  "atr_tp": 638.1224,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 647.84
- exit_price: 654.73
- tp_price: 638.12
- sl_price: 654.32
- qty: 16.0 · notional: 103.65440000000001
- trail_pct: 0.5

### Risk plan
- **planned_tp_distance_pct**: 1.5004
- **planned_sl_distance_pct**: 1.0002
- **planned_r_multiple**: 1.5
- **planned_risk_usd**: 103.68
- **planned_reward_usd**: 155.52
- **realized_r_multiple**: -0.011
- **exit_distance_from_tp_pct**: 2.5639
- **exit_distance_from_sl_pct**: -0.0633
- **notional**: 103.65440000000001

### Market excursion (MFE / MAE proxy)
- high_water: 647.84 · low_water: 647.84
- current_stop_at_close: 654.32
- **mfe_pct**: 0.0
- **mae_pct**: 0.0

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -0.011
- slippage vs planned TP: 2.5639%
- slippage vs planned SL: -0.0633%

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
  - high confidence (9) lost

## 7 · Tags
`sl_hit`, `grade_A`

---
*journaled_at 2026-06-05T21:57:18.617296+00:00Z · journaler v2*
