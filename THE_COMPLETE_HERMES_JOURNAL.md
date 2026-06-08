# THE COMPLETE HERMES JOURNAL
## Everything We Learned, Did, Won, Lost, and Fixed
### 379 Trades · 6 Days · June 2026

---

# PART 1: THE JOURNEY

## How It Started

Hermes is an autonomous crypto trading bot running on BloFin exchange. It started with 44 agents across multiple timeframes. After comprehensive backtesting, we killed 38 losing agents and kept 6 survivors. The bot trades 25 symbols with 5x leverage, using a composite signal engine powered by DeepSeek AI.

## The Dark Days (June 3-5)

For 2 full days, the bot generated ZERO trades. We debugged frantically — port conflicts, IP restrictions, duplicate processes. The real culprit was buried deep: a single undefined variable `vol_score_short` in `hermes_signals.py` that crashed every composite signal silently. One bug. Two days. Zero trades.

## The Breakthrough (June 6)

After fixing the crash, trades started flowing. 32 trades in 48 hours. But 15 were losers. Deep analysis revealed the root causes, and we systematically fixed every single one.

---

# PART 2: THE TRADES (379 TOTAL)

## All-Time Performance

| Metric | Value |
|--------|-------|
| Total Trades | 379 |
| Win Rate | 50.4% |
| Total P&L | -$17.09 |
| Average Win | +$0.72 |
| Average Loss | -$0.98 |
| Best Agent | macd_cross (71% WR, +$32.37) |
| Worst Agent | stoch_rsi (70 trades, -$11.33) |

## Daily Breakdown

| Day | Trades | P&L | Notes |
|-----|--------|-----|-------|
| June 6 (early) | 17 | -$40.56 | Shorts killed us — ICP, XMR, BTC |
| June 6 (late) | 4 | +$3.18 | Recovery starting |
| June 7 | 15 | +$24.66 | Shorts blocked, only longs |
| June 8 | 0 | $0.00 | New day, quality filter active |

## The 7 Big Losers Analyzed

| # | Symbol | Side | Loss | Root Cause |
|---|--------|------|------|------------|
| 1 | SOL-USDT | SHORT | -$13.30 | Never went positive — bad entry |
| 2 | XMR-USDT | SHORT | -$13.28 | Had +0.4% profit — trail too loose |
| 3 | BTC-USDT | LONG | -$12.79 | Never went positive — bad entry |
| 4 | ICP-USDT | SHORT | -$12.75 | Had +0.3% — breakeven never triggered |
| 5 | ICP-USDT | SHORT | -$12.71 | Never went positive — bad entry |
| 6 | ONDO-USDT | LONG | -$12.58 | Never went positive — bad entry |
| 7 | CL-USDT | SHORT | -$5.70 | Had +0.3% — breakeven never triggered |

**Pattern:** 5 of 7 were SHORTS. 4 of 7 never went positive. 3 of 7 had profit but protection never kicked in. ALL were confidence=3.

## The 15 Small Losers Analyzed

| Category | Count | Root Cause |
|----------|-------|------------|
| Had profit — trail gave it back | 6 (40%) | Trail activated at +1%, wins peaked at +0.6-0.8% |
| Breakeven scratch | 5 (33%) | Breakeven needed +0.5%, wins peaked at +0.1-0.3% |
| Never profitable — bad entry | 4 (27%) | Immediate reversal after entry |

**Key insight:** 40% of ALL losing trades had profit at some point but the trail/breakeven protection didn't activate in time. This was the single biggest leak.

---

# PART 3: THE AGENTS

## 6 Survivors (Currently Live)

### 1. macd_cross — THE GOLDEN CHILD ⭐
- **31 trades, 71% WR, +$32.37 live profit**
- Timeframe: 15m primary + 5m confirmation
- Strategy: MACD 24/52/18 crossover with volume confirmation
- Crypto-optimized: standard 12/26/9 is too slow for 24/7 crypto
- Risk: 6% per trade (doubled from 3% after proving edge)
- **The ONLY agent with proven live edge**
- Backtest: +29% at 15m+5m, -49.5% at 1H alone
- **Lesson:** Timeframe is everything. 1H MACD loses 50%. 15m+5m makes 30%.

### 2. daily_breakout
- Timeframe: 1H + 5m confirmation
- Strategy: Range breakout above/below prior 24-bar range
- Backtest: **+2,310%** (#1 paper performer ever)
- Live: Not yet fired — needs very specific breakout conditions
- Profile: Wide stops (4%), trailing TP only (no fixed target)

### 3. asymmetric
- Timeframe: 1H + 15m confirmation
- Strategy: Bollinger squeeze breakout with multi-confluence
- Backtest: +15% at 1H, -17% at 15m
- Risk/reward: Best among all agents (10.7% max drawdown)
- Live: Not yet fired — BB squeeze conditions are rare

### 4. viki
- Timeframe: 30m + 5m confirmation (was 15m, moved after backtest)
- Strategy: Triple EMA 9/21/50 crossover
- Backtest: +14.5% at 30m+5m, -31.4% at 15m alone
- Symbols: SOL-USDT, TAO-USDT, TIA-USDT only (whitelist)
- Live: Not yet fired — needs 30m data (recently added to MarketContext)
- **Lesson:** 15m Viki loses 31%. 30m Viki makes 15%. Timeframe change = 46% swing.

### 5. fib_bounce
- Timeframe: 1H
- Strategy: Fibonacci 0.618 retracement bounce + ADX>20 filter
- Exhaustive backtest: 73% profitable cross-validated
- Best settings: Fib 0.618, SL=5%, Trail=6%, ADX>20
- Live: Not yet fired — specific fib level touches are uncommon

### 6. hermes_master (Composite Engine) 🔥
- **The real workhorse — 32 of 32 recent trades**
- Strategy: 6-indicator weighted consensus (RSI + MACD + BB + EMA + FIB + VOL)
- Signal threshold: 3/6 indicators agree, composite score ≥55%
- Current stats: 33 trades, 55% WR, -$15.50
- Issue: Most trades are conf=3 (minimum quality)
- Profiles: SL=2.5%, Trail=4%, Activate=1%, Max hold=12h

## 38 Killed Agents (Why They Died)

| Agent | Reason | Evidence |
|-------|--------|----------|
| stoch_rsi | Overtrading, consistent loser | 70 trades, -$11.33 |
| daily_breakout_24h | Backtest lied — lost live | 6 trades, -$10.89 |
| tv_fibonacci | Catastrophic loser | 2 trades, -$10.09 |
| connors_rsi2 | Massive overtrader | 162 trades, -$3.75 |
| hurst_regime | Terrible win rate | 20 trades, 25% WR, -$3.47 |
| ema_ribbon | Loses at ALL timeframes | -93% to -100% backtest |
| momentum | Loses at ALL timeframes | -53% to -94% backtest |
| golden_cross | Negative every TF | -17% to -100% |
| kalman_trend | All negative | -7% to -68% |
| bb_bounce | All negative | -13% to -66% |
| +28 more | No edge proven | Killed by backtest analysis |

---

# PART 4: TECHNICAL ANALYSIS DEEP DIVE

## The 6-Indicator Composite System

Our primary signal engine combines 6 technical indicators into a weighted consensus:

### 1. RSI (Relative Strength Index) — Period 14
- **Weight: 1.0**
- Long signal: RSI < 40 (approaching oversold)
- Short signal: RSI > 60 (approaching overbought)
- Score formula: Long = max(0, min(100, (40-RSI)×5))
- **What we learned:** RSI alone is useless. Combine with trend. RSI oversold in a downtrend is a trap.

### 2. MACD — Crypto-Optimized 24/52/18
- **Weight: 1.5 (highest weight — most reliable)**
- Fast EMA: 24, Slow EMA: 52, Signal: 18
- Standard 12/26/9 is too slow for crypto's 24/7 volatility
- Long: MACD line > Signal line AND histogram rising
- Short: MACD line < Signal line AND histogram falling
- **What we learned:** MACD at 1H loses 50%. At 15m+5m confirm, makes 30%. TF matters more than the indicator.

### 3. Bollinger Bands (20, 2)
- **Weight: 1.0**
- Long: Price near lower band (oversold bounce potential)
- Short: Price near upper band (overbought reversal potential)
- Position formula: (Price - Lower) / (Upper - Lower)
- **What we learned:** BB alone generates noise. Combine with volume spike for real signals.

### 4. EMA Stack (9/21/50)
- **Weight: 1.2**
- Bullish: 9 > 21 > 50 (all aligned up)
- Bearish: 9 < 21 < 50 (all aligned down)
- Partial credit: 9 > 21 gives 50% score
- **What we learned:** EMA stack is the best trend filter. When 9/21/50 align, the trend is real.

### 5. Fibonacci Retracement (0.382/0.5/0.618)
- **Weight: 1.3 (second highest)**
- Long: Price near 0.382-0.5 support of recent swing
- Short: Price near 0.5-0.618 resistance of recent swing
- Swing: 100-bar high/low
- **What we learned:** 0.618 is the magic level. Exhaustive backtest proved 73% profitable at 0.618 vs 48% at 0.5.

### 6. Volume Confirmation
- **Weight: 0.8**
- Score = min(100, volume/20avg × 50)
- Below 80% of average = no conviction
- 2x average = full conviction
- **What we learned:** Low volume signals are fakeouts. Require volume > 80% average.

## The Weighted Consensus Formula

```
Total Weight = 1.0 + 1.5 + 1.0 + 1.2 + 1.3 + 0.8 = 6.8

Long Score = (RSI_Long×1.0 + MACD_Long×1.5 + BB_Long×1.0 + EMA_Long×1.2 + FIB_Long×1.3 + VOL×0.8) / 6.8

Signal fires when:
- Score ≥ 55%
- 3+ indicators agree (out of 6)
- Score > opposite direction score
- Not in blocked hours (4, 6 UTC)
- Volume > 80% average
```

## The Stepped Trail Ladder (Our Secret Weapon)

This is the most sophisticated part of the system. Instead of a fixed percentage trail, we use a stepped ladder:

| Profit Reached | Stop Loss Moves To | Protection |
|---------------|-------------------|------------|
| +0.3% | Entry price | BREAKEVEN — can't lose |
| +0.7% | Entry + 0.3% | Lock 0.3% profit |
| +1.5% | Entry + 0.8% | Lock 0.8% profit |
| +2.5% | Entry + 1.5% | Lock 1.5% profit |
| +4.0% | Entry + 2.8% | Lock 2.8% profit |
| +10.0% | Entry + 8.0% | Lock 8.0% profit |
| >10% | Peak - 1% | Loose tail — let moonshots run |

Combined with linear trail (activate at +1.0%, distance 4%) — whichever is tighter wins.

**What we learned:** The old ladder (activate at +0.5%, breakeven at +1.0%) was too slow. 40% of losers went +0.6% then reversed with NO protection. Lowering to +0.3% breakeven catches those trades.

---

# PART 5: RISK MANAGEMENT

## Position Sizing
- Base: 5% of equity per trade
- macd_cross: 6% (proven winner, scaled up)
- Minimum notional: $500 (BloFin minimum)
- Maximum concurrent: 10 positions
- Daily loss limit: $100

## Stop Loss
- hermes_master: 2.5% hard SL
- Hard liquidation guard: 5% adverse = emergency close
- All stops are limit orders — no market orders ever

## Symbol Blacklist (Permanent)
- ICP-USDT: -$19.80 over 9 trades
- SOL-USDT: -$14.82 over 15 trades
- BCH-USDT: -$10.85 over 38 trades
- ZEC-USDT: -$3.11 over 64 trades
- BNB-USDT: -$1.27 over 21 trades
- TAO-USDT, YFI-USDT, TON-USDT, NVDA-USDT, MU-USDT
- INTC-USDT, AAVE-USDT, SUI-USDT, TSLA-USDT, ETH-USDT
- INJ-USDT, LINK-USDT

## Hour Gates
- BLOCKED: 04:00, 06:00 UTC
- BEST: 09:00, 14:00, 20:00 UTC
- All other hours: trade normally

---

# PART 6: THE AI BRAINS

## 4-Layer Intelligence Stack

| Layer | Model | Role | Cost |
|-------|-------|------|------|
| 1. DeepSeek | deepseek-chat | Primary arbiter + research | $0.50/M tokens |
| 2. Ollama Local | gemma4:4b + qwen3:4b | Free fallback | $0 |
| 3. OpenRouter | owl-alpha (free) | Cloud backup | $0 |
| 4. OpenRouter Fallbacks | DeepSeek-R1, Qwen-Max | Last resort | $0 |

## What The AI Does
1. **Signal Arbitration:** Reviews every signal before execution
2. **Research Briefs:** Reads news feeds, writes daily brief
3. **Deep Learn:** Analyzes every closed trade, finds patterns
4. **CEO Mode:** Autonomous decisions to deploy/kill/scale agents

## Arbiter Prompt Philosophy
- Changed from "strict reviewer" → "experienced reviewer"
- Changed from "approve only if clear edge" → "default approve, reject only extreme risk"
- DeepSeek is fast (5s timeout) and cheap enough to review every trade

---

# PART 7: THE BUGS WE FOUGHT

## Critical Bugs Found & Fixed

### 1. vol_score_short — THE 2-DAY KILLER
- **Symptom:** Zero trades for 48 hours
- **Cause:** `vol_score_short` undefined in hermes_signals.py line 135
- **Fix:** Changed to `vol_score` (the correct variable name)
- **Impact:** Every composite signal crashed silently
- **Lesson:** Add try/except logging. Silent failures kill bots.

### 2. Port 8787 Duplicate Processes
- **Symptom:** Webhook crashes every 5 seconds
- **Cause:** Launchd KeepAlive spawning multiple bot.py instances
- **Fix:** Kill duplicates, keep only port owner
- **Lesson:** Check process count in doctor agent

### 3. BloFin 429 Rate Limiting
- **Symptom:** All API calls failing
- **Cause:** 4 duplicate bots making 4× the API requests
- **Fix:** Kill duplicates, wait for rate limit reset
- **Lesson:** 1 bot = 1/4 the calls = no rate limits

### 4. Viki df_30m Not Available
- **Symptom:** Viki crashing on analyze
- **Cause:** Changed Viki to use 30m but MarketContext only had 5m/15m/1H
- **Fix:** Added df_30m to MarketContext and data pipeline
- **Lesson:** Test TF changes end-to-end before deploying

### 5. hermes_master Profile KeyError
- **Symptom:** Composite signals crashing on execution
- **Cause:** Profile "hermes_master" didn't exist in PROFILES dict
- **Fix:** Added hermes_master profile with proper SL/TP/trail
- **Lesson:** Profile lookup should have a default fallback

### 6. SPY-USDT IP Restriction Loop
- **Symptom:** Same symbol rejected 5+ times per session
- **Cause:** Cached df1h data bypassed the bad_symbols_cache
- **Fix:** Added cache check in place_market() + clear df1h cache on rejection
- **Lesson:** Two layers of protection: data fetch AND order placement

---

# PART 8: THE FILES

## Where Everything Lives

```
/Users/saad/multi_agent_bot/
├── bot.py                    # Main trading bot (8000+ lines)
├── hermes_signals.py         # Composite signal engine
├── learning_agent.py         # Daily trade analysis
├── deep_learn.py             # 2-hour deep research
├── doctor_agent.py           # 30-min health checks
├── trail_master.py           # Trail optimization
├── backtest_comprehensive.py # All agents × all TFs
├── .env                      # API keys and config
├── bot.db                    # Trade database (SQLite)
├── journal.db                # Trade journal
├── HERMES_LEARNING_DIRECTIVE.md  # 10 rules
├── HERMES_MASTER.pine        # TradingView script (220 lines)
├── HERMES_MULTI_TF.pine      # Multi-TF TradingView script
├── backtest_results/         # 10 JSON + CSV files
├── backtest_data/            # 100+ parquet files
└── HERMES_BACKUP/            # Complete backup copy

/Users/saad/Desktop/HERMES_COMPLETE_BACKUP_2026-06-08/
├── trades/       # 379 trades (CSV + JSON)
├── logs/         # All log files
├── configs/      # bot.py, .env, all .py files
├── learnings/    # LEARNINGS, DEEP_LEARNINGS, RESEARCH_REPORT
├── backtests/    # All backtest results
├── scripts/      # All Pine Scripts
└── memory/       # Claude memory files
```

---

# PART 9: TRADINGVIEW PINE SCRIPTS

## Saad Bot 007 — The Master Script
- 220 lines, production-ready
- 5 timeframes: 5m, 15m, 30m, 1H, 4H
- 6 indicators per TF with customizable weights
- Multi-TF confluence gate (2+ TFs must agree)
- Live dashboard table with scores per TF
- Stepped trail ladder mirroring the Python bot
- Webhook alerts ready for bot integration

## Available Scripts
1. `HERMES_MASTER.pine` — Single-chart, all TFs
2. `HERMES_MULTI_TF.pine` — Advanced multi-TF version
3. `MACD_CROSS.pine` — MACD 24/52/18 on 15m+5m
4. `DAILY_BREAKOUT.pine` — Range breakout on 1H
5. `FIB_BOUNCE.pine` — Fibonacci 0.618 + ADX filter
6. `HERMES_15m.pine` — MACD + Hermes on 15m
7. `HERMES_1H.pine` — Breakout + Fib on 1H
8. `HERMES_ALL_IN_ONE.pine` — 4 strategies combined

---

# PART 10: THE FUTURE

## What's Working
- hermes_master composite engine — generating consistent signals
- Stepped trail ladder — smarter than fixed percentage
- Multi-timeframe data pipeline — 5m/15m/30m/1H/4H
- Deep Learn auto-analysis every 2 hours
- Doctor health checks every 30 minutes
- AI arbiter with 4 fallback layers
- Symbol blacklist preventing repeat mistakes

## What Needs Improvement
- 5 survivor agents rarely fire — hermes_master does all the work
- Short signals need better trend detection
- viki needs real 30m data testing (just added)
- BloFin IP whitelist still needs `185.194.184.0/24` added
- VPS migration pending (Vultr account verification)
- macd_cross should generate MORE signals (only 31 in weeks)

## The Golden Rules
1. **Live P&L is the only truth.** Backtest can say +2,310%. Live can say -$10. Trust live.
2. **Timeframe is everything.** Same strategy at wrong TF loses 50%. At right TF makes 30%.
3. **Trail early.** Profits that aren't protected become losses.
4. **Shorts are harder than longs.** 148 shorts: -$26. 210 longs: -$2.
5. **One bot, one port.** Duplicates cause rate limits, crashes, and silent failures.
6. **Data beats opinion.** Every fix was backed by trade analysis, not guesswork.

---

*Journal compiled 2026-06-08 · 379 trades · 6 days of battle · Hermes Autonomous Trading System*
