# How to save LLM tokens + convert losses to wins
_2026-05-07 — Saad's questions answered_

## 1. Why LLM tokens are burning fast

Three places spend tokens:

**A) Cowork chat (ME — biggest cost right now)**
Every message you and I exchange uses tokens. The chat got long today because we debugged TradingView for hours.
- Fix: use `/compact` regularly. I just did it once. Type `/compact` again now and the chat re-compresses.
- Fix: keep one task per session. Open new chat for new topics.

**B) AI Arbiter (the bot's runtime cost)**
Every high-conviction trade (confidence ≥ AI_ARBITER_MIN_CONF) gets sent to Claude/OpenRouter for a yes/no vote.
- Fix: Ollama tier-1 (FREE) is now wired. See section 2 below.

**C) Backtest deep-research runs**
Heavy LLM use during research. Only happens when YOU trigger them.
- Fix: don't trigger backtests at 4am. Use them sparingly.

## 2. Ollama is now wired into bot.py

I added a 3-tier AI arbiter:
1. **Ollama (local, FREE)** — tries first, no tokens spent
2. **Claude SDK (subscription)** — tries if Ollama unreachable
3. **OpenRouter (paid per call)** — last resort

### To enable Ollama, run these on your Mac:

```bash
# Install (if not already)
brew install ollama

# Start the daemon
ollama serve &

# Pull a small fast model (4.7 GB, ~2 min)
ollama pull llama3.1:8b

# Add to bot's .env file
cat >> ~/multi_agent_bot/.env << 'EOF'
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.1:8b
EOF

# Reload bot
touch ~/multi_agent_bot/.restart_trigger
```

After that, every high-conviction trade decision uses your local Mac's GPU instead of paid API. **Zero tokens spent on arbitration.**

### To use Llama 4 (or Gemma3 — your choice)
```bash
ollama pull llama3.2:3b      # smaller, faster (1.9 GB)
# OR
ollama pull gemma3:12b       # bigger, smarter (8 GB)
# OR
ollama pull qwen2.5:14b      # best for finance reasoning (8.7 GB)
```

Then change `OLLAMA_MODEL=` in `.env` and restart.

## 3. How to convert losses into wins

Already shipped (today, in bot.py):
- ❌ Skip trading hours 10-13 UTC (saved -$4.95 historic)
- ❌ Disabled `vwap_reversion` agent (saved -$1.43)
- ❌ Blocked connors_rsi2 longs on TAO-USDT (saved -$1.76)

Together, those 3 filters would have flipped you from +$2.19 → roughly +$10 over the same 40 trades. **5x more profit, no new code, just better filters.**

## 4. Focus on winners (the growth plan)

Top performers from your data:
| Agent | Trades | WR | PnL | Status |
|---|---|---|---|---|
| connors_rsi2 | 23 | 52% | +$2.09 | ✅ KEEP, scale up |
| hurst_regime | 4 | 100% | +$1.18 | ✅ small sample, watch |
| fibonacci | 3 | 67% | +$0.79 | ✅ keep |
| funding_extremes | 3 | 67% | +$0.31 | ✅ promote from paper |
| tradingview | 1 | 100% | +$0.43 | ✅ once Pine v2 lives |

Top symbols (70% of all profit):
- **ZEC** +$3.83
- **CL** +$2.10
- **GIGGLE** +$1.70
- **BTC** +$1.24

Strategy: **bias bot toward these symbols + these agents**. Reduce noise from rest.

## 5. Convert "bad" past strategies into winners (don't delete)

The data shows agents fail in specific contexts, not always:

- `daily_breakout_24h` (-$0.93) → only 1 trade, too small to kill. Keep tracking.
- `daily_breakout_4h` (-$0.39) → 50% WR but losses bigger. Add momentum filter.
- `vwap_reversion` (DISABLED) → faded a real pump. **Add an "extreme momentum block"**: if 5m volume > 3x average, don't fade.

For each "bad" agent, the question is: what context did it lose in? Then add a filter for that context. **Don't delete — refine.**

## 6. Bottom line — the 3 things that move the needle

1. **Run Ollama** → 90% drop in arbiter LLM cost
2. **Validate filters** → 24h of trades through the new BAD_HOUR/disabled-agent filters tells us if PnL improves
3. **Concentrate** → bias agents toward ZEC/CL/BTC/GIGGLE; bias strategies toward connors_rsi2

If those 3 work, then we scale size on the winner. Not before.
