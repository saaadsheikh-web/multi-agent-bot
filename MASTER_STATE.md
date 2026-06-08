# MASTER STATE — Saad's Crypto Bot + Hermes

**Last updated:** 2026-05-20
**Owner:** Saad
**This file = the single source of truth. Read it first.**

---

## WHO WE ARE & WHAT WE'RE DOING

- **The bot:** a multi-agent crypto trading system at `~/multi_agent_bot/`, trading BloFin perpetual futures.
- **Hermes:** the CEO/brain on top of the bot. Reads the sub-agents' work, briefs Saad in plain English, controls everything. Talk to him on Telegram @hermes007saad_bot.
- **Mission:** make money slowly and safely. Cut losers fast, ride winners, keep fees low. Target +$10–30/week, compound once edge is proven.
- **Equity:** ~$3,450. Lifetime P&L: −$3.31 (144 trades) — roughly break-even.

---

## CURRENT STATE (2026-05-20)

- Bot: live, scanning every minute, 9 live agents + 1 new paper agent.
- **Live agents:** connors_rsi2 (workhorse +$3.7), stoch_rsi, fibonacci, macd_cross, funding_extremes, zscore_reversion, bb_bounce, daily_breakout_2h.
- **Paper agents:** hurst_regime (killed — losing), fib_confluence (NEW, proving edge).
- Min trade: $50. Per-trade cap: 50% of equity. Leverage: 5×.

---

## WHAT WE BUILT (chronological)

1. **Hermes doctrine** (7 files): BRIEFING, TRAINING, GUARDRAILS, CONTROL_SURFACE, DAILY_PLAYBOOK, HISTORY_LESSONS, LEARNING. Full autonomy mandate, dyslexia-friendly voice, kill rules, pyramiding doctrine.
2. **Fixed crash loop:** aiohttp/Python 3.14 bug, webhook supervised + reuse_address, killed rogue hermes-agent gateway.
3. **DNS auto-heal:** bot resolves via 8.8.8.8/1.1.1.1 if Mac DNS drops (Virgin Media keeps dropping).
4. **.env auto-loader:** keys load even from a clean shell.
5. **Killed 26 dead agents** (never fired) — lean roster of 9.
6. **CEO mode:** Hermes briefs like a human boss, reads sub-agents (CEO/Auditor/Learning/research).
7. **Research loop:** every 6h reads CoinDesk/Cointelegraph/Decrypt → HERMES_RESEARCH_BRIEF.md.
8. **New agent fib_confluence:** multi-swing Fibonacci hot-zone, limit-order bounces (paper).
9. **Sizing fix:** $50 hard minimum, 50% per-trade cap.
10. **20 Telegram commands** for full phone control.

---

## PHONE CONTROL (@hermes007saad_bot)

- **Brain:** `/pnl` `/analyze` `/research`
- **Trade:** `/kill AGENT` `/deploy AGENT [size]` `/flatten SYMBOL` `/pause` `/resume` `/flatten_all` `/set_leverage N`
- **System:** `/health` `/logs [N]` `/restart` `/update` `/tvtest`
- **CEO:** `/ceo [question]` or just talk normally ("how's trading?")

---

## KEY FILES

**Doctrine (read these):** HERMES_BRIEFING.md, HERMES_TRAINING.md, HERMES_HISTORY_LESSONS.md, HERMES_GUARDRAILS.md, HERMES_CONTROL_SURFACE.md, HERMES_DAILY_PLAYBOOK.md, HERMES_MEMORY.md (diary)

**Code:** bot.py (main), hermes.py (CEO brain), hermes_telegram.py (phone), hermes_bridge.py (command bus), openrouter_client.py (free LLM)

**Data:** bot.db (all trades — source of truth), health.json (live state), .env (API keys — NEVER share/commit), market_context.json

**Setup guides:** SETUP_TRADINGVIEW_AND_GITHUB.md, HANDOFF_PROMPT.md

---

## TODO / OPEN ITEMS

- Watch fib_confluence ~50 paper trades → `/deploy fib_confluence` if edge positive.
- Set up GitHub repo to enable `/update` from phone (guide in SETUP_TRADINGVIEW_AND_GITHUB.md).
- Add TradingView alerts pointing at the /tv webhook (same guide).
- Watch 50% cap for drawdown spikes.
- Maker-order routing already enforced (limit-only). Biggest fee lever already pulled.

---

## HARD LIMITS (never cross)

- No money movement (withdrawals/transfers). Trading API only.
- No leverage above 10×.
- No Twitter/X scraping (no free API + ToS).
- No profit guarantee — better data improves odds, not certainty.

---

## HOW TO CHECK IT'S ALIVE

```
cd ~/multi_agent_bot && tail -5 bot.log && cat health.json
```
