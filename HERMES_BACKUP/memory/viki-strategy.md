---
name: viki-strategy
description: "Viki agent — triple EMA 9/21/50 crossover strategy, backtest results, optimal settings"
metadata:
  node_type: memory
  type: project
  originSessionId: 73dd1ee7-dcaa-48f6-8b8b-6037cf11546f
---

Viki is a triple EMA crossover agent deployed in the multi_agent_bot.

**Strategy:** 9 EMA crosses 21 EMA, both on same side of 50 EMA. 15-minute candles.

**Backtest results (original):**
- 2 months (Feb-May 2026): +68% return, 81.5% WR, 65 trades
- 1 year: −77% — degrades in choppy markets, only works in trending regimes

**Comprehensive backtest 2026-06-03 — ALL timeframes:**
- 5m: -38.0% ❌
- 15m (native): -31.4% ❌
- 15m + 5m confirm: -27.4% ❌
- **30m: +8.0% ✅** (51 trades, 72.5% WR, 8.1% DD)
- **30m + 5m confirm: +14.5% 🔥** (34 trades, 79.4% WR, 6.9% DD) ← BEST
- 1H: -29.9% ❌
- 1H + 15m confirm: -31.7% ❌

**New optimal settings**: 30m candles with 5m confirmation. Move from 15m → 30m.

**Live settings:**
- Symbols: SOL-USDT, TAO-USDT, TIA-USDT (whitelist)
- Profile: 7% SL, trail activates at +3% with 1.5% distance
- Timeframe: 15m (ctx.df_15m) — **SHOULD BE 30m per comprehensive backtest**
- Leverage: account-level (bot uses exchange setting)
- Status: LIVE, enabled, paper_only=False

**Key weakness:** 7% SL gets clipped in choppy/ranging. Needs TRENDING-only regime filter.
**Key strength:** Trail mechanism is perfect — 292/292 trail exits were winners (100% WR).

**Files:** bot.py (VikiAgent class), backtest_viki.py, VIKI_BACKTEST.md
**Related:** [[comprehensive-backtest-20260603]]
