# State of the Bot — 2026-05-06 21:25 UTC (evening update)
*Continuation of STATE_OF_THE_BOT_2026-05-06.md. Captures everything that happened in the evening session: bugs found, fixes shipped, TV integration status, what's pending Saad's hands.*

---

## TL;DR

- Found and fixed **two real bugs** in `bot.py` (both compile-clean, both surgical, no new strategy).
- TV → bot webhook end-to-end is **healthy** (confirmed via curl: `vetoed: exchange position exists`).
- Bot is **still running on old code** until Saad restarts the process — fixes don't activate until reload.
- Saad's TV alert in TradingView is **mis-configured** — picked "0.786 Fib Crossing" instead of "Any alert() function call". Easy 3-click fix.
- Did **not** touch any new strategy / data / indicator code — per the morning State doc's own warning ("don't ship more code in the same window, we won't be able to attribute results").

---

## 🐛 Bug 1: Permanent revenge lockout (HIGH severity — bot was inert all afternoon)

### Symptom
Bot's `bot.log` showed `ANTI_REVENGE_LOCKOUT triggered — pausing 30 min` firing every 30 minutes on the dot, starting 15:08 BST and continuing through 17:38+. Bot had been doing zero scan-loop trades since 15:06.

### Root cause
`Database.recent_two_losses()` checked the latest 2 closed trades regardless of age. The 14:08 TAO + 14:42 ZEC + 15:06 YFI loss cluster (all `connors_rsi2`, all trail-stopped) tripped the lockout. After 30 min the lockout expired — but `recent_two_losses()` re-evaluated, saw the same 2 stale losses still as the most recent in the DB, and re-fired. **Permanent self-lock.** The only way out would have been 2 winning trades closing — impossible if the bot isn't trading.

### Fix shipped
- Added `since_iso` parameter to `recent_two_losses()` — when given, only counts losses with `closed_at > since_iso`.
- Added `state.anti_revenge_last_trigger` epoch field (initialized 0) — advanced to `now_t` whenever the lockout fires.
- Lockout check converts `last_trigger` → ISO timestamp and passes to `recent_two_losses()`. Old loss clusters no longer re-arm.

Files touched: `bot.py` lines 4318-4332 (function), 4969-4995 (call site), 6080-6086 (state init).

---

## 🐛 Bug 2: AI Arbiter silently auto-approving (MEDIUM severity)

### Symptom
15+ instances of `[WARNING] max-sdk arbiter: Command failed with exit code 1` across the day, every couple of hours. AI veto was supposed to gate high-conviction trades.

### Root cause
`_arbiter_via_max_sdk()` returned `(True, "max-sdk-error")` on any exception — i.e., **auto-approved** every trade. The OpenRouter fallback existed (`_arbiter_via_openrouter`) but was unreachable: the dispatch logic was `if HAS_CLAUDE_SDK: return _arbiter_via_max_sdk(...)` with no fall-through, so OpenRouter was only used when Claude SDK wasn't installed at all.

### Fix shipped
- `_arbiter_via_max_sdk()` now returns `Optional[Tuple[bool, str]]` — `None` on error, real result on success.
- `ai_arbiter()` checks for `None` and falls through to OpenRouter. Both paths preserved; OpenRouter is no longer dead code.

Files touched: `bot.py` lines 4554-4574 (max_sdk function), 4604-4614 (dispatch logic).

---

## ✅ Verified healthy

| Component | Status | How verified |
|---|---|---|
| ngrok tunnel `brigida-tristichic-janet.ngrok-free.dev` | ✅ live | Saad's curl returned `vetoed: exchange position exists` |
| Bot `/tv` endpoint | ✅ listening | Same curl — got bot-formatted response |
| `X-Secret` auth | ✅ enforced | Curl carried correct secret, accepted |
| JSON parse + strategy lookup | ✅ working | `fib_786_long` → matched profile, dispatched to risk vet |
| `state.risk.vet()` | ✅ catching position collisions | Refused to double-stack on existing BTC position |
| Pine Script `MAB_Fib_786_Setup.pine` | ✅ added to BTC chart | Saad's screenshot shows the 0.786 line and EMA200 plotted, 78,970.15 reading |
| `bot.py` after edits | ✅ compiles clean | `python3 -m py_compile bot.py` passed |

---

## 🔍 Important architecture note discovered tonight

**TV alerts bypass the revenge lockout.** `_tv_handle()` calls `state.risk.vet()` only — it does NOT consult `state.anti_revenge_paused_until`. So:

- Scan-loop trades (every 60s, the 8 internal agents): gated by lockout.
- TV webhook trades: **never gated by lockout, ever**.

Possible interpretations:
1. **Intentional** — TV signals are higher-conviction (Saad-curated Pine Scripts), so we trust them past the bot's anti-tilt protection.
2. **Oversight** — should be gated.

Decision deferred. Worth discussing once we have ≥5 real TV-fired trades to attribute, not tonight.

---

## ⏳ Pending Saad-hands actions

### 1. Restart the bot
The two bugfixes are saved to disk but the running process is still on old code. Restart however you normally do (kill + relaunch, systemd, wrapper script). Without restart: lockout still permanent, arbiter still silently approving.

### 2. Verify after restart
Watch `bot.log` for the next minute or two. Expect to see:
- No more `ANTI_REVENGE_LOCKOUT active — Xs remaining` spam after the existing window expires.
- Normal scan output: `scan: N symbols regime: RANGING | learning: ...`
- Eventually, if a high-conviction signal fires, an arbiter call that succeeds (either via max-sdk OR via OpenRouter fallback — log will say which).

### 3. Fix the TradingView alert dropdown
Your last screenshot showed:
- Condition row 1: `MAB Bot — 0.7...` ✅ correct
- Condition row 2: `0.786 Fib` + `Crossing` + Value `78,970.15` ❌ **wrong path entirely**

This is TradingView's plot-value alert path — it would fire when *price* crosses the *plotted Fib line*, ignoring all our EMA200/RSI gates and never running our `alert()` JSON. To wire to the bot:

- Click the second dropdown (currently "0.786 Fib")
- Scroll the list, find **"Any alert() function call"**
- Select it. The "Crossing" + Value boxes disappear. Good.

Then Notifications tab:
- Webhook URL: `https://brigida-tristichic-janet.ngrok-free.dev/tv`
- Custom header: `X-Secret: 178f9024586197ca101fac18fdb8796579165984f3e5058b`
- Save.

### 4. (Optional) Test the saved alert manually
Right-click the alert in TradingView's alert panel → "Send notification" or similar. Should produce a `webhook: BTC-USDT long conf=9 strategy=fib_786_long` line in `bot.log` within 1-2 seconds.

---

## ❌ What I deliberately did NOT touch tonight

Per the morning State doc — *"Don't ship more code in the same window — we won't be able to attribute results."*

Held back from:
- 4H + 1D candle ingestion (still missing, still important — next session)
- BTC dominance filter (still missing, still important — next session)
- Reconcile race-condition tightening (last race was 14h ago; not currently active)
- Strategy profile retunes
- New agents (wedge, BTC-dom, log-channel) — Pine Scripts ready in concept; ship after fib_786 proves out
- Any change to position sizing, leverage, SL/TP defaults

The two edits tonight are **bug fixes** (restoring intended behavior), not new strategy. Attribution remains clean: any P&L change after restart is from "lockout no longer permanent" + "arbiter now actually vetoing."

---

## Files saved tonight

| File | Path | What |
|---|---|---|
| Bot source | `/Users/saad/multi_agent_bot/bot.py` | 5 surgical edits (lockout fix + arbiter fallback) |
| This state doc | `/Users/saad/multi_agent_bot/STATE_OF_THE_BOT_2026-05-06_EVENING.md` | What you're reading |
| Pine Script | `/Users/saad/multi_agent_bot/MAB_Fib_786_Setup.pine` | Already saved earlier today, unchanged |

---

## Tomorrow morning checklist

1. Pull `bot.log`, look at last 200 lines. Confirm lockout has cleared and bot is scanning normally.
2. Check `today_pnl=...` in the equity log line. Is the bot trading again?
3. If TV alert is wired: any `webhook:` lines in the log? Any `webhook VETO` or actual fills attributed to `agent='tradingview'`?
4. If everything stable, NEXT priorities (in order): 4H/1D candles → BTC dominance filter → wedge Pine Script #2.

Saved 2026-05-06 21:25 UTC.
