> # ⚠️ SUPERSEDED — 2026-05-19
> This file's `d -k` kill list (hurst_regime, daily_breakout_24h, daily_breakout_4h, **fibonacci**) is **NO LONGER CORRECT**. Live data as of 2026-05-19:
> - **fibonacci:** n=4, WR 50%, +$0.79, PF 3.39 — winner, do NOT kill (below n=5 floor anyway).
> - **daily_breakout_4h, daily_breakout_2h:** both n=2 — below floor, hold.
> - **hurst_regime:** n=20, PF 0.27 — kill IS warranted but must be done via the bot's API/undeploy, not by acting on this stale list.
>
> Hermes and CEO agents: **ignore the kill list in this file.** Use live `bot.db` queries via the CEO's per-agent table.
> Saad: this file is kept for historical context only.
> Marked SUPERSEDED by Claude/Cowork on Saad's request, 2026-05-19.

---

# Plan of Attack — 2026-05-05 (post-forensics) [SUPERSEDED]

## What I just shipped (no action needed from you)

### 1. Maker-order conversion ✅ (LIVE)
- `bot.py` line 4232-4244 — limit orders now sit PASSIVELY on the book
- Long orders place 2 ticks BELOW current price → fills as maker bid
- Short orders place 2 ticks ABOVE → fills as maker ask
- **Fee impact:** 0.06% taker → 0.02% maker per side. ~70% fee cut.
- **On 35 trades that's $2.51 → $0.83 in fees. The strategy goes from −$0.18 to +$1.50 net.**
- Trade-off: some signals may not fill if price moves away. Acceptable for mean-rev (we want better entries anyway).

### 2. Confidence scoring fix ✅ (LIVE)
- `bot.py` line 4476-4502 — multi-agent boost rewritten
- OLD: `conf += len(sigs)` → 2 agents = +2, capped at 10 → led to inverted curve where conf=10 had 39% WR vs conf<=7 at 100% WR
- NEW: capped at +1 boost, only when agreeing agents come from DIFFERENT strategy families (mean-rev + trend = real confluence; mean-rev + mean-rev = noise)
- Absolute confidence cap is now 9 (10 reserved for AI arbiter approval)

### 3. New agent: `funding_extremes` ✅ (LIVE in PAPER)
- Fades extreme funding rates — 8h funding > +0.05% → SHORT, < −0.05% → LONG
- Confluence: RSI threshold + EMA50 slope filter (don't fight ripping trends)
- 4-factor confidence grading, capped at 9
- Profile: meanrev (TP 1.8% / SL 1.2%)
- Per RESEARCH_REPORT_2.md, expected 62-73% WR — highest expected edge of any unbuilt agent

---

## What YOU need to paste (these are capital-allocation decisions, must be your call)

Run these in your terminal:

```bash
# 1. Kill the 4 bleeders (saves the −$1.65 drag)
~/multi_agent_bot/d -k hurst_regime
~/multi_agent_bot/d -k daily_breakout_24h
~/multi_agent_bot/d -k daily_breakout_4h
~/multi_agent_bot/d -k fibonacci

# 2. Scale up connors_rsi2 (the only proven edge) — from 0.05x to 0.10x
~/multi_agent_bot/d connors_rsi2 0.10

# 3. Promote funding_extremes from paper to live at 0.04x (small-size pilot)
~/multi_agent_bot/d funding_extremes 0.04
```

That's 6 commands. Each takes ~15 seconds for the bot to reload.

---

## What's next on the runway (NOT shipped — for your decision)

- **EMA200 trend filter on `connors_rsi2` longs** — kills falling-knife trades like the ZEC −$1.87 loss
- **Session filter (08:00–18:00 UTC only)** — skips the 10:00 chop window that ate −$2.80
- **Symbol whitelist for connors_rsi2** — concentrate on BTC, CL, XAG, GIGGLE, HYPE
- **SMC Order Block agent** (per RESEARCH_REPORT_2.md spec)
- **GARCH volatility-regime sizing layer**

Each of these is 30-100 lines of code. Tell me when you're ready and I'll build the next one.

---

## Why we're NOT sizing up further or using high leverage

Per the conversation:
- Doubling trade size doubles fees too — must fix fees first (done) before size goes up
- Higher leverage (20-30x) = liquidation on a 3-5% wick. We've seen 2.27% adverse moves; flash wicks can blow through SL.
- Keep leverage at **5-10x max** until profit factor is consistently 1.5×+ after fees over 100+ trades.
- Once edge is proven, confidence-graded sizing scales automatically (not blanket size-up)

---

## Live agent roster after this session

37 agents enabled — `funding_extremes` is the newest:
```
whale, news, donchian, candlestick, rsi_divergence, vwap_reversion, trend_pullback,
daily_breakout, daily_breakout_24h, daily_breakout_4h, daily_breakout_12h, daily_breakout_48h,
daily_breakout_7d, daily_breakout_2h, daily_breakout_8h, supertrend, volume_capitulation,
asian_pump, pump_dump_reversal, macd_cross, bb_bounce, zscore_reversion, stoch_rsi,
golden_cross, liquidity_sweep, connors_rsi2, raschke_retest, wide_scalp, wide_candle,
hurst_regime, kalman_trend, utbot_mtf, utbot_v3, smart_scalp, volume_profile,
williams_r, funding_extremes, fibonacci
```

(After you run the kill commands above, this drops to 33 enabled.)

---

## Backup snapshot

All current changes safe in `~/multi_agent_bot/backups/20260505_190339/` plus `.tar.gz`. To roll back any change:

```bash
cp ~/multi_agent_bot/backups/20260505_190339/bot.py ~/multi_agent_bot/bot.py
touch ~/multi_agent_bot/.restart_trigger
```

End of plan. Run those 6 commands and watch Telegram.
