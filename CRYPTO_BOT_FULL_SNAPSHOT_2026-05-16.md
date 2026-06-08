# Crypto Bot — Full Snapshot

**Generated:** 2026-05-16
**Bot home:** `/Users/saad/multi_agent_bot/`
**Primary copy:** `/Users/saad/Documents/Claude/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md`
**This copy (backup):** `/Users/saad/multi_agent_bot/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md`

This single file consolidates everything Claude pulled out of Google Drive, the scheduled-tasks system, and the local bot directory. Use it as the one place to look. Detailed source files referenced below all live under `~/multi_agent_bot/`.

---

## 1. Executive summary

- The "crypto bot" = a multi-agent trading system at `~/multi_agent_bot/`. Python, paper + live perpetuals on BloFin. ~26 live agents (per SYSTEM_STATUS), 10 explicitly opted-in in the May 1 scorecard.
- **Health (today 14:33 UTC):** 1 open trade. Today's P&L **−$0.64**. Webhook secret set. Broker ID flag not set.
- **Equity:** ~$2,225 (varies hourly). Position cap: 5 concurrent. Min $50 notional/trade.
- **119 closed trades** in the latest learning window: WR **46.2%**, total **−$2.65**, avg/trade **−$0.02**. Effectively flat.
- **The big lever still unpulled:** maker orders (Drive doc, May 5). Fees ate ~100% of the edge — switching cuts fees ~70% and the same trade history flips from break-even to ~+$1.50 net.
- **9 strategies sitting in DEPLOY_QUEUE** waiting on Telegram approval. Strongest: `daily_breakout_4h` (Sharpe 10.36) and `daily_breakout_2h` (Sharpe 13.18, never a red month).
- **Hermes bridge is live** (file-based bus over `hermes_bridge/`), OpenRouter rotation across free-tier keys, model `openrouter/owl-alpha`, free-only guard on.

---

## 2. Live state (now)

From `~/multi_agent_bot/health.json` (2026-05-16T14:33:04Z):

```json
{
  "open_trades": 1,
  "today_pnl": -0.6425,
  "broker_id_set": false,
  "webhook_secret_set": true
}
```

From `eod_recap_2026-05-14.md`:
- P&L −$0.06, 0W / 1L. Single `connors_rsi2` trade closed for −$0.06.

---

## 3. Scheduled tasks (the "bot's brain" cron)

24 scheduled tasks, prompts live at `~/Documents/Claude/Scheduled/<taskId>/SKILL.md`.

### Currently enabled (5):

| Task | Cadence | Purpose |
|---|---|---|
| `ceo-accountability` | hourly | CEO agent, statistical, devil's advocate, Telegrams on real decisions |
| `auditor-agent` | every 30 min | Audits CEO + session for stale data, sloppy reasoning |
| `learning-agent` | every 4h | Reviews closed trades, writes LEARNINGS.md, feeds CEO |
| `nightly-strategy-hunter` | daily 04:08 | Full 365-day backtest → appends to BACKTEST_REPORT.md |
| `mab-weekly-revalidation` | Sundays 03:07 | Fresh backtest vs last week, alert on degradation |

### Disabled but configured (19):

- **Health/ops:** `mab-bot-health-check` (30min), `self-healer` (5min), `error-detective` (30min), `mab-deploy-approver` (2h), `telegram-deploy-responder` (1min).
- **Intel sweep:** `mab-news-scanner` (4h), `mab-coin-hunter` (2h), `mab-social-watcher` (2h), `mab-macro-news` (3x/day), `mab-technical-scout` (4h), `mab-market-intel` (4h all-in-one), `mab-research-agent` (4h).
- **Strategy:** `mab-strategy-validator` (6h), `hourly-strategy-lab` (30min — generates 5 parametric candidates per cycle, 240/day), `agent-scorecard` (6h), `board-meeting-5hr`.
- **Briefings:** `mab-morning-briefing` (07:00 BST daily).
- **One-shots already fired:** `deep-learning-session-2hr`, `deep-research-1hr-pro-traders`.

---

## 4. Learning Agent — latest report (2026-05-16, 119 trades)

### Overall

| Metric | Value |
|---|---|
| Closed trades | 119 |
| Win rate | 46.2% |
| Total P&L | −$2.65 |
| Avg/trade | −$0.02 |
| Avg win | +$0.35 |
| Avg loss | −$0.35 |

### Per-agent

| Agent | Trades | WR | Total | Avg |
|---|---|---|---|---|
| connors_rsi2 | 74 | 48.6% | +$1.03 | +$0.01 |
| fibonacci | 4 | 50.0% | +$0.79 | +$0.20 |
| bb_bounce | 2 | 100.0% | +$0.44 | +$0.22 |
| tradingview | 1 | 100.0% | +$0.43 | +$0.43 |
| macd_cross | 2 | 100.0% | +$0.31 | +$0.15 |
| funding_extremes | 5 | 40.0% | +$0.27 | +$0.05 |
| daily_breakout_2h | 2 | 100.0% | +$0.22 | +$0.11 |
| zscore_reversion | 2 | 50.0% | +$0.08 | +$0.04 |
| daily_breakout_4h | 2 | 50.0% | −$0.39 | −$0.20 |
| daily_breakout_24h | 3 | 0.0% | −$0.93 | −$0.31 |
| vwap_reversion | 2 | 50.0% | −$1.43 | −$0.71 |
| hurst_regime | 20 | 25.0% | −$3.47 | −$0.17 |

### Per-symbol (top)

| Symbol | Trades | WR | Total |
|---|---|---|---|
| GIGGLE-USDT | 5 | 80.0% | +$1.95 |
| BTC-USDT | 7 | 85.7% | +$1.29 |
| CL-USDT | 5 | 40.0% | +$1.17 |
| XPT-USDT | 2 | 50.0% | +$0.71 |
| XAG-USDT | 2 | 50.0% | +$0.46 |
| DASH-USDT | 1 | 100.0% | +$0.39 |
| BCH-USDT | 12 | 50.0% | +$0.27 |
| HYPE-USDT | 2 | 50.0% | +$0.26 |
| SOL-USDT | 5 | 60.0% | +$0.22 |
| BNB-USDT | 4 | 50.0% | +$0.18 |

### Long vs short

- **Shorts** — 48 trades, 45.8% WR, total +$0.63
- **Longs** — 71 trades, 46.5% WR, total **−$3.29** (the bleed)

### Time-of-day (UTC)

Best hours: 01:00 (+$2.95 / 10), 19:00 (+$1.36 / 9), 18:00 (+$1.14 / 3), 00:00 (+$1.11 / 5), 05:00 (+$1.06 / 3).
Worst: 08:00 (−$3.89 / 4), 03:00 (−$1.66 / 10), 10:00 (−$1.66 / 8). Window 08:00–11:00 UTC bled −$6.86 over 19 trades.

### Actionable insights (verbatim)

- **KILL/RESTRICT** `hurst_regime` — 20 trades, WR 25%, net −$3.47, worst −502%. Disable or paper-only.
- **KILL/RESTRICT** `daily_breakout_24h` — 3 trades, 0% WR, net −$0.93, worst −185%. Disable or paper-only.
- **SCALE UP** `connors_rsi2` — 74 trades, 49% WR, net +$1.03. Increase notional_multiplier 1.5×.
- **SYMBOL BLACKLIST** ZEC, ONDO, SUI, TON, YFI, TAO, ETH (loss-per-trade between −58% and −205% on small samples).
- **HOUR GATE** 08:00–11:00 UTC: require ≥2-agent confluence in this window.

---

## 5. Deploy Queue — 9 strategies awaiting approval

Validation thresholds: ExpR > +0.20R AND DD(pct_eq) < 40% AND n ≥ 50.
Approval format: reply `deploy <name>` in Telegram to flip live at 0.10× notional.

| Strategy | ExpR | DD | n | WR | PF | Sharpe | Worst month | Note |
|---|---|---|---|---|---|---|---|---|
| `daily_breakout_4h` | +0.501R | −7.8% | 2479 | 74.0% | 3.86 | **10.36** | +7.3% | Strongest signal in cohort |
| `daily_breakout_2h` | +0.466R | −10.7% | 3734 | 71.7% | 3.45 | **13.18** | +26.1% | Top Sharpe overall, never red |
| `daily_breakout_8h` | +0.352R | −5.7% | 785 | 72.1% | 2.98 | 8.42 | +1.7% | Cleanest DD, never red |
| `daily_breakout_12h` | +0.391R | −8.8% | 1869 | 76.3% | 3.37 | 5.81 | +0.8% | |
| `daily_breakout` | +0.417R | −4.0% | 290 | 83.1% | 3.98 | 4.32 | −1.0% | |
| `daily_breakout_24h` | +0.384R | −5.2% | 1009 | 78.6% | 3.97 | 6.57 | +0.5% | **Conflict:** live data says KILL |
| `daily_breakout_7d` | +0.283R | −3.7% | 195 | 75.9% | 2.41 | 3.63 | −1.0% | n=0 in latest re-test |
| `daily_breakout_48h` | +0.201R | −7.8% | 467 | 73.2% | 1.92 | 3.85 | −4.0% | Marginal PASS, 🟡 KEEP |
| `trend_pullback` | +0.204R → +0.153R | −22.0% | 2457 | 70.9% | 1.81 | 4.83 | −11.3% | Degraded on re-validation |

**Key tension:** the deploy queue still lists `daily_breakout_24h` as ready, but the May 16 learning report says KILL it (0% WR, −$0.93 live). Live evidence is overriding the backtest. Trust live.

---

## 6. Drive doc — Trading Bot Optimization Strategy (May 5, 2026)

[Doc link](https://docs.google.com/document/d/1Zxg6jINLxyQgtZR6T-ZKRo6YQrU6piEKKRlOXH7BYHw/edit)

### The fee answer (and the shocking finding)

- Pre-fee gross +$2.33 across 35 trades. After realistic fees: **−$0.18 to +$1.08**. Break-even, not profitable. Fees ate ~100% of edge.
- Worst-case fees (all taker, 0.06% × 2): $3.77. Best (all maker, 0.02% × 2): $1.26.

### Confidence is inverted

| Confidence | n | WR | Avg/trade |
|---|---|---|---|
| ≤7 (low) | 3 | 100% | +$0.74 |
| 8 | 9 | 11% | −$0.00 |
| 9 | 1 | 100% | +$0.43 |
| 10 (highest) | 23 | 39% | −$0.01 |

The "10/10 conviction" trades LOST money on average. Scaling up high-confidence trades right now loses more, not less. Likely cause: confluence boost (+1 conf per agreeing agent) games the score on bad signals.

### Sizing & leverage

- Sizing up at break-even just scales fees (linear). $87 → $200/trade: gross +$5.36 vs fees $5.77 = still net negative.
- Leverage doesn't change P&L for the same % move; it only changes liquidation distance. 30× ≈ liq at 3.3%. Worst single trade was −2.27%; a 3.5% wick at 30× wipes you.

### Roadmap (do in order)

1. **Switch to maker orders** → fees drop ~70%, strategy turns profitable (~+$1.50 net vs −$0.18). Biggest lever.
2. **Fix inverted confidence scoring** — weight by historical agent accuracy, not headcount.
3. **Confidence-graded sizing** AFTER #2. Conf 6-7: $50, conf 8: $80, conf 9: $120, conf 10: $180.
4. **Wider TPs on shorts** — shorts are where the edge is (30.8% WR, +$2.42 avg). Push from 2% → 3.5–4%. Est +$1–1.50 / 35 trades.
5. **Modest size-up only on `connors_rsi2`** on proven symbols (BTC, CL, XAG, GIGGLE, HYPE) at $120–150/trade.
6. **Keep leverage 5–10× max.**

Expected after all 5: **+$15–20 net per 35 trades** vs current break-even, no liquidation risk.

### Do NOT

- Don't go 20×+ leverage.
- Don't blanket-double trade size.
- Don't trust conf-10 trades right now.
- Don't size up untested agents.

---

## 7. Agent Scorecard (last full run: 2026-05-01)

Run window: ~2.3 days of `bot.log`. Live roster: 10 explicit `paper_only=False` agents.

| Agent | Signals | Fills | PnL | Status | Deployed (UTC) |
|---|---|---|---|---|---|
| trend_pullback | 0 | 0 | $0.00 | 🟡 | 2026-04-29 21:11 |
| daily_breakout_4h | 0 | 0 | $0.00 | 🟡 | 2026-04-30 23:16 |
| daily_breakout_24h | 0 | 0 | $0.00 | 🟡 | 2026-04-30 23:17 |
| daily_breakout | 0 | 0 | $0.00 | 🟡 | 2026-04-30 23:18 |
| daily_breakout_7d | 0 | 0 | $0.00 | 🟡 | 2026-04-30 23:18 |
| supertrend | 0 | 0 | $0.00 | 🟡 | 2026-05-01 04:33 |
| asian_pump | 0 | 0 | $0.00 | 🟡 | 2026-05-01 04:33 |
| macd_cross | 0 | 0 | $0.00 | 🟡 | 2026-05-01 04:34 |
| volume_capitulation | 0 | 0 | $0.00 | 🟡 | 2026-05-01 04:35 |
| pump_dump_reversal | 0 | 0 | $0.00 | 🟡 | 2026-05-01 04:35 |

Only firing in the window: 7× `tradingview/momentum` + 3× `tradingview/meanrev` (inbound webhooks). One CLOSE: BTC long +$0.43 via reconcile_sync. By the May 16 learning report, those agents have since traded.

---

## 8. Hermes bridge — what's wired (from SESSION_HANDOFF.md, May 16)

- **OpenRouter:** rotation across multiple free-tier keys.
  - `.env` → `OPENROUTER_API_KEYS=key1,key2`
  - `OPENROUTER_MODEL=openrouter/owl-alpha` (free 1M-context stealth)
  - `OPENROUTER_FREE_ONLY=1` (refuses paid slugs)
- **`openrouter_client.py`** — thread-safe `KeyRotator` + `chat()`. Round-robin, 60s cooldown on 429/5xx/401/403, free-only guard.
- **`hermes_bridge.py`** — file-based bus between Hermes and the bot.
  - `hermes_bridge/state.json`, `events.jsonl`, `commands.jsonl`, `ack.jsonl`
  - Commands: `pause`, `resume`, `flatten`, `flatten_all`, `set_leverage`, `set_risk`, `reload_strategies`, `ping`, `say`
- **`hermes.py`** — observer/controller. CLI:
  - `python3 hermes.py state | tail | ask "…" | auto "…" | exec pause | exec set_leverage --arg value=3 | ping`
- **`bot.py`** — runs `hermes_loop` alongside other supervised loops. Publishes a 5s snapshot, drains+acks Hermes commands. Arbiter routes through the rotator.

### Open todos

- Add more OpenRouter free keys to widen rate-limit headroom.
- (Optional) Wire Hermes into Telegram for phone commands.
- (Optional) Hermes auto-act on regime changes (e.g., `flatten_all` if BTC vol > N%).

### Smoketest

```bash
cd ~/multi_agent_bot
./hermes_smoketest.sh
```

---

## 9. Telegram alert types you'll see

- 🚀 OPEN — real fill
- 📉 CLOSE — exit with P&L
- ❌ REJECTED — rare (precision bugs fixed)
- 🛡 Anti-revenge lockout — paused after 2 losses
- 🎯 *new trade found* — CEO deploy proposal (reply YES)
- 🚨 EMERGENCY — account drop > $50
- 🔍 Error scan (every 30 min)
- 🦞 OpenClaw 2-hour learning report (one-time)

---

## 10. Operating quick-ref

```bash
# Manage agents
~/multi_agent_bot/d                 # list agents + status
~/multi_agent_bot/d AGENT 0.05      # deploy at 5% notional
~/multi_agent_bot/d -k AGENT        # kill

# Logs
tail -f ~/multi_agent_bot/bot.log
cat ~/multi_agent_bot/CEO_LOG.md
cat ~/multi_agent_bot/AGENT_SCORECARD.md
cat ~/multi_agent_bot/LEARNINGS.md
cat ~/multi_agent_bot/self_healer.log
cat ~/multi_agent_bot/error_detective.log

# If something breaks
touch ~/multi_agent_bot/.restart_trigger     # manual restart
python3 ~/multi_agent_bot/test_telegram.py   # test Telegram
```

---

## 11. File inventory — `~/multi_agent_bot/`

### State / logs

- `bot.db` — SQLite of every closed trade (the source of truth)
- `bot.log`, `bot.stdout.log`, `stdout.log`, `stderr.log`
- `learning_agent.log`, `error_detective.log`, `self_healer.log`, `nightly_hunter.log`, `nightly_hunter.bg.log`
- `deploy_handler.log`, `parametric_backtest.log`, `strategy_lab.log`, `market_context.log`
- `preflight.log`, `forensics_output.log`
- `ngrok.log`, `ngrok_stdout.log`, `ngrok_stderr.log`

### Markdown state files

- `SESSION_HANDOFF.md` — most recent (touched today)
- `TODAYS_LEARNINGS.md`, `LEARNINGS.md`
- `DEPLOY_QUEUE.md`, `DEPLOY_QUEUE_LOG.md`
- `BACKTEST_REPORT.md`, `BACKTEST_REPORT_LAST_WEEK.md`, `BACKTEST_FORENSICS.md`, `BACKTEST_2026-05-06.md`, `BACKTEST_FIB_TRENDLINES.md`, `BACKTEST_ADVANCED_FIB.md`, `BACKTEST_TREATISE.md`
- `AGENT_SCORECARD.md`, `VALIDATOR_LOG.md`, `BOARD_MINUTES.md`, `BOARD_MEETING_2026-05-05.md`
- `CEO_LOG_APPEND_2026-05-10T22-15Z.md`, `🚨_AUDITOR_ALERT.md`, `AUDIT_2026-05-08.md`
- `SYSTEM_STATUS.md`, `STATE_OF_THE_BOT_2026-05-06.md`, `STATE_OF_THE_BOT_2026-05-06_EVENING.md`
- `RESEARCH_LOG.md`, `RESEARCH_ALERT.md`, `RESEARCH_REPORT_2.md`, `DEEP_RESEARCH_1HR.md`
- `INTEL_LOG.md`, `NEWS_LOG.md`, `HOT_COINS.md`, `HOT_ZONES_EVERYTHING.md`, `HOT_ZONES_TREATISE.md`
- `STRATEGY_LIBRARY.md`, `PROFITABLE_STRATEGIES.md`, `MEGA_STRATEGY_CATALOG.md`
- `FIBONACCI_DEEP_DIVE.md`, `FIBONACCI_ADVANCED.md`, `FIBONACCI_TREATISE.md`, `TREND_LINES_TREATISE.md`
- `DCA_ANALYSIS.md`, `PERFECT_ENTRIES_RESEARCH.md`, `WHY_LOSE_HOW_WIN_2026-05-07.md`, `PROFIT_LOSS_FORENSICS.md`
- `PLAN_OF_ATTACK.md`, `PLAN_B_FALLBACK.md`, `SAAD_WAKE_UP.md`, `URGENT_ALERT.md`, `FIX_BROKER_NOW.md`
- `eod_recap_2026-05-12.md`, `eod_recap_2026-05-13.md`, `eod_recap_2026-05-14.md`
- `SESSION_LOG_2026-05-05.md`, `SESSION_STATE_2026-04-30.md`, `SESSION_MEMORY.md`
- `CONTEXT.md`, `CONTEXT_UPDATED.md`, `HUNTER_BRIEF.md`, `OVERNIGHT_LOG.md`
- `BRAINSTORM_2026-05-05.md`, `HOW_TO_SAVE_TOKENS.md`, `TEAM.md`, `TRADINGVIEW_SETUP.md`
- `health_check_2026-05-01_0034utc.md`, `infinity_lux_concierge_setup.md`

### JSON state

- `strategy_pool.json` — 240/day strategy candidates from the lab
- `market_context.json`, `health.json`, `broker_diag.json`
- `self_healer_state.json`, `error_detective_seen.json`, `.bt_merged.json`
- `hermes_bridge/state.json`

### Code (top-level)

- `bot.py` — main trading bot
- `backtest.py`, `parametric_backtest.py`, `nightly_hunter.py`, `strategy_lab.py`
- `bybit_wrapper.py`, `forensics.py`, `analyze_btc.py`
- `telegram_deploy_handler.py`, `self_healer.py`, `error_detective.py`
- `strategies_v2.py`
- Tests: `test_telegram.py`, `test_wide_candle.py`, `test_quant_agents.py`, `test_utbot_mtf.py`, `test_fibonacci_variants.py`
- `run.sh`, `d` (deploy script)

### Backups

- `backups/20260504_043354/` — code snapshot
- `backups/20260505_190339/` — full state snapshot (every .md + .env + bot.db)

---

## 12. What's in Google Drive

Only three crypto-related files synced to Drive (everything else is local):

| File | Type | Date | What it is |
|---|---|---|---|
| Trading Bot Optimization Strategy | Google Doc | 2026-05-05 | The May 5 post-mortem on 35 trades — summarized in §6 |
| `one_liner.txt` | text | 2026-04-28 | Base64+gzip self-extracting installer (`echo <payload> \| base64 -d \| gunzip \| bash`) |
| `fix_deploy.txt` ×2 | text | 2026-04-28 | Same shape — writes payload to `/tmp/d`, chmods, runs |

No Firestore export exists in Drive. The bot does not write to Firestore — its persistence layer is local SQLite (`bot.db`) + Markdown + JSON files in `~/multi_agent_bot/`.

---

## 13. Recommended next moves (priority order)

1. **Flip `daily_breakout_4h` or `daily_breakout_2h` live at 0.10× notional.** Highest Sharpe in the queue, never had a red backtest month. Reply `deploy daily_breakout_4h` in Telegram.
2. **Kill `hurst_regime` and `daily_breakout_24h`.** The May 16 learning report is unambiguous: −$3.47 and −$0.93 with terrible WRs. `~/multi_agent_bot/d -k hurst_regime`, same for `daily_breakout_24h`.
3. **Add the symbol blacklist** (ZEC, ONDO, SUI, TON, YFI, TAO, ETH) to `LOSING_SYMBOL_BLACKLIST` in `bot.py`.
4. **Implement maker-order routing.** This is the biggest single lever per the May 5 doc — fee cut of ~70%, strategy flips from break-even to profitable.
5. **Fix the inverted confidence model** — weight by historical agent accuracy, not headcount.
6. **Add an 08:00–11:00 UTC confluence gate** (≥2 agents to fire in that window).
7. Re-enable `agent-scorecard` and `mab-bot-health-check` so the supervisor agents have fresh inputs.

---

*Generated by Claude in Cowork mode, 2026-05-16. This file is mirrored at `~/Documents/Claude/CRYPTO_BOT_FULL_SNAPSHOT_2026-05-16.md`.*
