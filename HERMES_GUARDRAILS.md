# HERMES GUARDRAILS — Hard Limits

**Last updated:** 2026-05-18
**Purpose:** Non-negotiable boundaries. If any trips, Hermes pauses trading, logs, escalates to Saad.

---

## 1. DYNAMIC DAILY LOSS LIMIT (vol-adjusted)

Loss limit is NOT a fixed number — it scales with current BTC daily ATR.

```
Daily ATR % of BTC = (14d ATR / BTC price) × 100

Vol regime           Daily ATR %      Daily loss limit (% of equity)
Calm                 < 1.5%           1.5%
Normal               1.5% – 3.0%      2.5%
Active               3.0% – 5.0%      4.0%
High vol / crisis    > 5.0%           5.0% (then stop, regardless)
```

**On $2,225 equity that's $33 / $55 / $89 / $111.**

If today's realized loss ≥ limit → `pause`, `flatten_all`, log, escalate. Resume only after Saad's explicit OK OR next session boundary (00:00 UTC) AND vol regime check.

---

## 2. PER-TRADE RISK CAP

- Default per-trade risk: **1% of equity** (~$22 on $2,225).
- Hermes may set between **0.25% and 2%**.
- Above 2% → blocked. No exceptions.
- Pyramid adds are additive: original 1% + 0.5% + 0.25% = max 1.75% on a single name.

---

## 3. CONCURRENT POSITION CAP

- Max 5 concurrent positions (existing bot rule, do not change).
- Max 2 positions per side (long/short) until edge proven.
- Max 1 position per symbol.

---

## 4. LEVERAGE CAP

- Default 5×. Hermes may set 3×–10×.
- **Hard ceiling: 10×.** Anything above is blocked.
- Liquidation distance must be ≥ 2× worst single-trade loss in last 30 days.

---

## 5. DRAWDOWN CIRCUIT BREAKER

Three tiers, all measured from session-open equity:

| Drawdown | Action |
|---|---|
| 2% | Reduce per-trade risk by half. Log warning. |
| 4% | Pause new entries. Manage open positions only. |
| 6% | `flatten_all`. Stop. Escalate. No resume without Saad. |

---

## 6. LOSS-STREAK PAUSE

- 3 consecutive losses on any single strategy → pause that strategy for the session.
- 5 consecutive losses across all strategies → pause the whole bot for 2 hours.
- Resume requires (a) vol regime unchanged, AND (b) at least one paper signal confirming the strategy still fires correctly.

---

## 7. KILLER HOURS (UTC) — current gating

Historical bleed: 08:00–13:00 UTC = London open chop, −$6.86 across 19 trades.

Gating rule during 08:00–13:00 UTC:
- Require ≥2-agent confluence on signal.
- Per-trade risk halved (0.5% default instead of 1%).
- No new pyramid adds during this window.

Lift the gate only after 30+ trades in this window with positive expectancy.

---

## 8. SYMBOL BLACKLIST (current)

**Hard blacklist** — no trades, no overrides without Saad:
- ZEC, ONDO, SUI, TON, YFI, TAO, ETH

**Reason:** loss-per-trade −58% to −205% on May 16 learning report. Untradeable for this venue/size right now.

Re-evaluate monthly. Adding a symbol back requires 50+ paper trades positive.

---

## 9. SYSTEM HEALTH GUARDS

Auto-pause if any of these:
- `bot.log` silent > 5 minutes (bot may be dead).
- `health.json` older than 3 minutes.
- All 6 OpenRouter keys returning 429 simultaneously.
- BloFin API errors > 5 in 60 seconds.
- `bot.db` reports phantom $0 P&L closes within last 10 minutes (regression of May 16 fix).

---

## 10. THE MONEY-MOVEMENT BOUNDARY (absolute)

Hermes may **never**:
- Request, configure, or use an API key with withdrawal scope.
- Initiate a transfer between wallets, sub-accounts, or exchanges.
- Sign up for a new exchange.
- Move stablecoins on or off the exchange.

Trading API keys only. If a tool/process requires withdrawal permission, refuse and tell Saad.

---

## 11. ESCALATION FORMAT (when a guardrail trips)

Telegram message template:

```
🚨 GUARDRAIL TRIP

[GUARDRAIL NAME]
Equity: $X.XX (−Y.Y% session)
Open: N positions
Action taken: paused | flattened | gated

Reason: [one sentence]
Need from you: [resume? confirm? ignore?]
```

Short. Clear. Actionable. No paragraphs.

---

## 12. SELF-CHECK ON BOOT

On every Hermes start:
1. Read this file.
2. Confirm all guardrails active in code (read `.env`, bot config).
3. If any guardrail is missing or disabled, log to memory and ask Saad before resuming live trading.

End of guardrails. These exist to protect capital. They are not suggestions.
