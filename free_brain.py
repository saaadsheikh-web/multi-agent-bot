#!/usr/bin/env python3
"""Free model brain — runs 24/7 on OpenRouter free models. Costs $0.
Researches, learns, generates strategies, analyzes markets constantly."""

import asyncio, json, logging, os, time, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from hermes import openrouter_chat

HERE = Path(__file__).parent
log = logging.getLogger("free_brain")

async def think_free(task: str, max_tokens: int = 300) -> str:
    """Use free models only — Qwen, DeepSeek free tier. Costs $0."""
    try:
        return openrouter_chat(
            [{"role": "user", "content": task}],
            model="qwen/qwen-2.5-72b-instruct:free",
            max_tokens=max_tokens, temperature=0.3, timeout=20,
            task_type="general"
        )
    except Exception as e:
        return f"[free brain offline: {e}]"

async def research_loop():
    """Every 2 hours: research new trading ideas using free models."""
    while True:
        try:
            # Read recent trades for context
            db = HERE / "bot.db"
            recent = ""
            if db.exists():
                conn = sqlite3.connect(str(db))
                rows = conn.execute("SELECT agent, symbol, side, pnl, pnl_pct FROM trades WHERE status='closed' ORDER BY closed_at DESC LIMIT 10").fetchall()
                recent = "\n".join(f"{r[0]} {r[1]} {r[2]} ${r[3]:+.2f} ({r[4]:+.2f}%)" for r in rows)
                conn.close()

            prompt = f"""Recent trades:\n{recent}\n\nBased on these results, suggest ONE concrete improvement to the trading bot.
Be specific: what parameter to change, what strategy to add, what's working and should be scaled up.
Reply in 2-3 lines max. No fluff."""

            insight = await think_free(prompt, max_tokens=200)
            if insight and "offline" not in insight:
                # Append to research log
                ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
                with open(HERE / "free_brain.log", "a") as f:
                    f.write(f"\n[{ts}] {insight.strip()}\n")
                log.info(f"free_brain insight: {insight[:120]}")
        except Exception as e:
            log.debug(f"research loop: {e}")
        await asyncio.sleep(7200)  # every 2 hours

async def strategy_hunt_loop():
    """Every 4 hours: hunt for new strategy ideas using free models."""
    while True:
        try:
            db = HERE / "bot.db"
            agents = ""
            if db.exists():
                conn = sqlite3.connect(str(db))
                rows = conn.execute("""SELECT agent, COUNT(*), ROUND(SUM(pnl),2), ROUND(100.0*SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END)/COUNT(*),1)
                    FROM trades WHERE status='closed' AND pnl IS NOT NULL GROUP BY agent HAVING COUNT(*)>=5 ORDER BY SUM(pnl) DESC LIMIT 8""").fetchall()
                agents = "\n".join(f"{r[0]}: {r[1]}t ${r[2]:+.2f} {r[3]:.1f}% WR" for r in rows)
                conn.close()

            prompt = f"""Agent performance:\n{agents}\n\nDesign ONE new trading strategy based on what's winning.
Name it, give the entry rule, stop loss, and confidence level. 3 lines max."""

            strat = await think_free(prompt, max_tokens=250)
            if strat and "offline" not in strat:
                ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
                with open(HERE / "strategy_ideas.md", "a") as f:
                    f.write(f"\n## {ts}\n{strat.strip()}\n")
        except Exception:
            pass
        await asyncio.sleep(14400)  # every 4 hours

async def market_watch_loop():
    """Every 30 min: analyze market with free models."""
    while True:
        try:
            fg = ""
            fg_path = HERE / "market_context.json"
            if fg_path.exists():
                data = json.loads(fg_path.read_text())
                fg = data.get("fear_greed", {}).get("value", "?")
                bias = data.get("market_bias", "?")

            prompt = f"Fear&Greed: {fg}. Bias: {bias}. In 1 line: what's the best trade RIGHT NOW for a crypto bot? Symbol, direction, one reason. No disclaimers."

            call = await think_free(prompt, max_tokens=100)
            if call and "offline" not in call:
                ts = datetime.now(timezone.utc).strftime("%H:%M")
                with open(HERE / "market_calls.md", "a") as f:
                    f.write(f"[{ts}] {call.strip()}\n")
        except Exception:
            pass
        await asyncio.sleep(1800)  # every 30 min

async def free_brain_loop():
    """Main loop — runs all free-model tasks 24/7. Costs $0."""
    log.info("🧠 Free Brain online — maxing free models 24/7")
    await asyncio.gather(
        research_loop(),
        strategy_hunt_loop(),
        market_watch_loop(),
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    asyncio.run(free_brain_loop())
