# Setup: TradingView Feed + GitHub Auto-Update

Two things you (Saad) do once. After that, everything runs and updates from Telegram.

---

## 1. TRADINGVIEW — feed signals into the bot

The bot already listens at `/tv`. You just add alerts in TradingView.

**In TradingView, create an alert:**
1. Open a chart, click the alarm clock (Alerts) → Create Alert
2. Set your condition (e.g. RSI crossing, EMA cross — your strategy)
3. Under **Notifications → Webhook URL**, paste:
   ```
   https://brigida-tristichic-janet.ngrok-free.dev/tv
   ```
4. Add a **Header**: name `X-Secret`, value:
   ```
   178f9024586197ca101fac18fdb8796579165984f3e5058b
   ```
5. In the **Message** box paste:
   ```json
   {
     "secret": "178f9024586197ca101fac18fdb8796579165984f3e5058b",
     "symbol": "{{ticker}}-USDT",
     "side": "long",
     "confidence": 8,
     "strategy": "my_tv_strategy",
     "price": {{close}}
   }
   ```
6. Set `side` to `long` or `short`. Set `confidence` 6–10 (under 6 won't trade).
7. Save.

**Test it works:** message Hermes `/tvtest` on Telegram. He fires a fake low-confidence signal that gets auto-vetoed (no real trade) and confirms the pipe is alive.

---

## 2. GITHUB — auto-update the bot's code

Right now the bot folder is NOT a git repo, so `/update` just tells you that.
To turn on auto-update, do this once on your Mac:

```bash
cd ~/multi_agent_bot

# create a private repo on github.com first (e.g. "multi_agent_bot"), then:
git init
git add -A
git commit -m "initial bot snapshot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/multi_agent_bot.git
git push -u origin main
```

(Use a GitHub personal access token as the password when it prompts — github.com → Settings → Developer settings → Personal access tokens.)

**After that:**
- Edit code anywhere, push to GitHub.
- On Telegram, send Hermes `/update` → he runs `git pull` + restarts the bot with the new code.
- No Mac terminal needed ever again.

**⚠️ Never commit your `.env`** (it has your API keys). Add a `.gitignore`:
```bash
echo ".env" > ~/multi_agent_bot/.gitignore
echo "bot.db" >> ~/multi_agent_bot/.gitignore
echo "*.log" >> ~/multi_agent_bot/.gitignore
git rm --cached .env 2>/dev/null
```

---

## What you control from Telegram now (@hermes007saad_bot)

**Brain:** `/pnl` `/analyze` — real stats
**Trade:** `/kill` `/deploy` `/flatten` `/pause` `/resume` `/flatten_all` `/set_leverage`
**System:** `/health` `/logs` `/restart` `/update` `/tvtest`
**Anything else:** plain English — Hermes reads real data, decides, acts.

You no longer need Claude/Cowork for day-to-day. Hermes runs it.
