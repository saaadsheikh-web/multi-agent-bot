# Trade #63 — TON-USDT short (vwap_reversion)

**Outcome:** LOSS · **PnL:** -1.5580 (-3.059% if pct available) · **Decision grade:** D (45/100) · **Hold:** 2.04 min

> Short stopped out at full risk on TON-USDT (vwap_reversion, -3.06%) [flagged-losing-symbol] [killed-agent] trail gave back 3.17% [grade D / 45].

## 1 · Identity
- custom_id: `MABVWATONUSD23257`
- agent: `vwap_reversion` · profile: `meanrev`
- symbol: `TON-USDT` · side: `short`
- confidence: 9
- opened: `2026-05-07T03:07:38.418991+00:00`
- closed: `2026-05-07T03:09:40.617474+00:00` · hour UTC 03 (Thu)

## 2 · Hypothesis (why we entered)
> VWAP fade short z=+4.75σ RSI 76 vol_recent=0.2x

### Parsed signal features
- **rsi**: 75.90752715647125
- **z**: 4.7515128828077575
- **trend_score**: 0
- **trend_dir**: FLAT
- **vwap**: 2.3741485456035747

### Raw meta from agent
```json
{
  "vwap": 2.3741485456035747,
  "z": 4.7515128828077575,
  "rsi": 75.90752715647125,
  "tp_price": 2.3741485456035747,
  "sl_price": 2.7077637205076943,
  "_trend_score": 0,
  "_trend_dir": "FLAT"
}
```

## 3 · Plan vs Execution
- entry_price: 2.681
- exit_price: 2.763
- tp_price: 2.614
- sl_price: 2.7212
- qty: 19.0 · notional: 50.939
- trail_pct: 1.0

### Risk plan
- **planned_tp_distance_pct**: 2.4991
- **planned_sl_distance_pct**: 1.4994
- **planned_r_multiple**: 1.667
- **planned_risk_usd**: 0.7638
- **planned_reward_usd**: 1.273
- **realized_r_multiple**: -2.04
- **exit_distance_from_tp_pct**: 5.5576
- **exit_distance_from_sl_pct**: -1.5591
- **notional**: 50.939

### Market excursion (MFE / MAE proxy)
- high_water: 2.681 · low_water: 2.678
- current_stop_at_close: 2.7212
- **mfe_pct**: 0.1119
- **mae_pct**: 0.0
- **trail_gave_back_pct**: 3.1705

## 4 · Forensics
- **exit_reason:** `SL_HIT`
- realized_r_multiple: -2.04
- slippage vs planned TP: 5.5576%
- slippage vs planned SL: -1.5591%

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
  - high confidence (9) lost

## 7 · Tags
`losing_symbol`, `killed_agent`, `trail_too_loose`, `very_short_hold`, `sl_hit`, `grade_D`

---
*journaled_at 2026-05-17T03:54:39.559981Z · journaler v2*
