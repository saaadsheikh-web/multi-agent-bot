# 🚨 AUDITOR ALERT — 2026-05-07 02:42Z UTC

## Headline

**17 phantom $0.00 closes are corrupting per-agent stats. The kill-switch is muting hurst_regime — the agent with the BEST true win rate (80% on 5 real trades) — because its reported lifetime WR is 28.6% (averaged in 9 phantom closes from `reconcile_sync` bulk-syncs).**

## What's broken

`reconcile_sync` in bot.py records a CLOSE in the trades table even when:
1. The exchange `positions` API call THREW AN EXCEPTION (treated as "no position found"), AND
2. The follow-up `close_position` API call ALSO failed.

Two confirmed instances today:
- **2026-05-06 23:49:43 UTC** — connors_rsi2 ZEC-USDT marked closed at pnl=$0 (exit=entry=$551.73) **during the BloFin DNS outage** that ran 23:48Z May 6 → 02:30Z May 7. The position was likely still open on the exchange.
- **2026-05-07 02:39:58 UTC** — vwap_reversion YFI-USDT marked closed at pnl=+$0.13 via reconcile_sync ~7m after open. The trade was a FIB-LIMIT at $2688.82 that almost certainly never filled — agent gets credited a "win" on a phantom fill.

12 historic phantoms on the same code path:
- 2026-05-04 19:19:10 (3 phantoms in 25ms — hurst_regime BTCDOM/TAO/BTC)
- 2026-05-05 01:17:40 (5 phantoms in 70ms — hurst_regime GIGGLE/XPT/CL/BCH/XAG)
- 2026-05-05 21:48:09 (5 phantoms in 30ms — connors_rsi2 HYPE/BNB/ETH + fibonacci TAO + funding_extremes XMR + 2 daily_breakout_24h)
- 2026-05-02 10:12:25 (1 phantom — hurst_regime CL)

## Real vs reported per-agent stats

| agent | reported n | real n | reported WR | real WR | net (unchanged) |
|-------|-----------:|-------:|------------:|--------:|----------------:|
| hurst_regime | 14 | **5** | 28.6% | **80.0%** | +$1.12 |
| connors_rsi2 | 27 | 23 | 48.1% | 56.5% | +$2.29 |
| funding_extremes | 4 | 3 | 50.0% | 66.7% | +$0.31 |
| fibonacci | 4 | 3 | 50.0% | 66.7% | +$0.79 |
| daily_breakout_24h | 3 | 1 | 0.0% | 0.0% | -$0.93 |

## Money-cost

- The kill-switch has been muting hurst_regime signals on every scan loop since the WR-weight gate was added. hurst_regime's true performance is **80% WR / 4W-1L / +$1.12 net** — it should NOT be muted.
- The CEO's 02:35Z A-grade entry uses the corrupted stats for its Step 4 / Step 6 / Tier classifications on connors_rsi2.
- Lifetime bot PnL number (+$3.84) is correct (phantoms are $0); but trade count, win rates, per-agent rankings are all wrong.

## Recommended actions (priority order)

1. **Fix `reconcile_sync` to NOT mark a position closed when the exchange API call errored.** Treat "API exception" as "unknown" not "absent." Only mark closed if positions API succeeded AND returned a list NOT containing the symbol.
2. **Refuse to write a CLOSE record when `close_position` itself returned an error.** The current code ignores the close failure and stamps pnl=$0 with exit=entry. Should instead leave the position as `status=open` with a sticky `reconcile_pending` flag and alert.
3. **Quarantine the 17 phantom rows** (`UPDATE trades SET status='phantom' WHERE entry_price=exit_price AND pnl=0.0` or similar) and recompute kill-switch tables. hurst_regime in particular needs its real n=5 / WR=80% / +$1.12 used by gates.
4. **Tell the CEO prompt to exclude phantoms** from per-agent stats: `WHERE NOT (entry_price=exit_price AND pnl=0.0)` in every gate calculation.
5. **Investigate vwap_reversion's YFI-USDT 02:32–02:39Z trade** — confirm with the exchange whether the FIB-LIMIT at $2688.82 ever filled. If not, the trade should be deleted, not closed at +$0.13.

## Telegram status

Attempted, **failed**: HTTP 403 from outbound proxy in this audit sandbox. Bot's own Telegram pipe was down at 23:48Z+ due to the DNS outage. Saad will see this only by reading `AUDITOR_LOG.md` or this file. Recommend adding a bot-boot hook that ships `auditor_telegram.txt` to Telegram so the SKILL's alert path becomes reliable.

—Auditor (2026-05-07 02:42Z UTC)

---
## 🚨 ALERT — 2026-05-23T18:35:00Z

**CEO UNDEPLOY DID NOT EXECUTE — connors_rsi2 STILL LIVE**

CEO log at 17:07:27Z: *"ACTION: UNDEPLOY connors_rsi2 — Executing undeploy curl now."*  
CEO self-graded this as ✅ DONE.

**EVIDENCE IT DID NOT HAPPEN:**
- `bot.log 18:18:41Z`: agents enabled: `[...'connors_rsi2'...]` — still in list
- `bot.log 18:26:35Z`: agents enabled: `[...'connors_rsi2'...]` — still in list  
- `bot.db`: connors_rsi2 opened **new SOL-USDT SHORT at 18:20:37Z** (73 min post-declaration)
- `pending_undeploy.txt`: contains only `hurst_regime`, NOT `connors_rsi2`
- No UNDEPLOY log line for connors_rsi2 anywhere in bot.log

**CURRENT RISK:**
- 2 open connors_rsi2 shorts: AAVE-USDT (opened 14:44Z), BCH-USDT (opened 14:55Z)
- Regime is TRENDING — mean-reversion shorts are wrong-regime
- Agent is STILL firing (fired SOL short at 18:20Z)

**ACTION REQUIRED FROM SAAD:**
```
curl -X POST -H "X-Secret: 178f9024586197ca101fac18fdb8796579165984f3e5058b" \
  "https://brigida-tristichic-janet.ngrok-free.dev/undeploy?agent=connors_rsi2"
```

Telegram delivery attempted but blocked (sandbox egress restriction). Alert written to file.
