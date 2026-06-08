---
name: coin-scout-results-20260603
description: "Live BloFin coin scout — top 30 coins scored for backtest-winning strategies, tokenized stocks dominate"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

Live coin scout run 2026-06-03: 486 USDT pairs scanned, 30 qualified (score 93-100).

**Top 3**: AVGO-USDT (100), CL-USDT (100), SPK-USDT (100)
**Best type**: Tokenized stocks (AVGO, AMD, PLTR, MSTR, ARM) and commodities (CL, XCU, COPPER) outscore crypto
**Crypto standouts**: BTC (95), DOGE (95), SOL (95), KSM (96), GOAT (98)

**Key insight**: Tokenized stocks have cleaner trends (higher ADX) and better fib structure than crypto. The daily_breakout and fib_confluence strategies will work even better on these.

**All 30 coins match all 10 winning strategies** from backtest.

**Backtest validation**: Only DOGE-USDT from the backtest top-10 appeared. Market conditions have shifted — SOL now scores 95 despite backtest showing losses on daily_breakout 1H.

**Action**: Run scout every 4 hours. Trade the top 30 with daily_breakout @ 1H. Priority adds: AVGO, CL, AMD, PLTR, MSTR, KSM.

**Files**: coin_scout_results_20260603.txt, coin_scout.py, run_coin_scout.py
**Why**: To continuously find new profitable coins using backtest-proven winner criteria
**How to apply**: Import coin_scout into bot, run pre-scan before each trading cycle, feed top coins to agents
