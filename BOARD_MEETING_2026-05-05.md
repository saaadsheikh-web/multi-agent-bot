> # ⚠️ SUPERSEDED — 2026-05-19
> The `d -k fibonacci` recommendation in this file contradicts live data (fibonacci is n=4, WR 50%, +$0.79, PF 3.39). The Auditor agent has carried this contradiction for 12+ days. **Ignore the kill list in this file.** Use live `bot.db` queries via the CEO's per-agent table.
> Marked SUPERSEDED by Claude/Cowork on Saad's request, 2026-05-19.

---

# Board Meeting — 2026-05-05, 21:00 UTC [SUPERSEDED]
**Owner:** Saad · **Lead Quant + CTO:** Claude

## Single objective
Make this bot profitable, on purpose, with a measurable plan.

---

## Hard facts on the table

| Fact | Number |
|---|---|
| Bot closed P&L (35 trades) | +$2.44 pre-fee, ~break-even post-fee |
| Profit factor | 1.46× |
| Best agent | connors_rsi2 — 57% WR, PF 1.66, +$2.29 |
| Worst agent | hurst_regime — 28% WR, 9 of 14 closed at $0 (auto-killed today) |
| Best symbols | BTC, GIGGLE, CL, XAG (range-bound) |
| Best hour | 08:00 UTC — 100% WR, +$2.80 |
| Worst hour | 10:00 UTC — 0% WR, −$2.80 |
| Long PnL vs Short PnL | +$0.03 vs +$2.42 |

**We have ONE proven edge (connors_rsi2). Everything else is unproven.**

---

## Decisions

### 1. Stop pretending we have 37 strategies. We have 1 + a bench.
- Tier 1 (production): connors_rsi2, funding_extremes
- Tier 2 (probation, n<5): williams_r, bb_bounce, daily_breakout_2h, tradingview
- Tier 3 (auto-killed at WR<30% n>=5): handled by the WR-weighted kill-switch

### 2. Honest weekly P&L targets
- Week 1: +$5 net (prove fee cut + confidence fix work)
- Week 2: +$10 net (after session filter + EMA200 long filter)
- Week 3: +$20 net (after scaling connors_rsi2 up)
- Week 4: +$30-40 net with 50%+ WR

If PF after fees < 1.5× by end of month, shrink size and rebuild. No emotion.

### 3. Risk lines we will not cross
- Leverage: 5–10x max
- Max single trade: 5% of equity ($110 at $2,225)
- Daily loss cap: −$50, then 12h pause
- Equity floor: $2,000. Below = halt + manual restart only.
- INJ-USDT: permanent blacklist

### 4. Four daily metrics — nothing else
- WR over last 30 trades (target: rising toward 55%)
- Profit factor after fees (target: 1.5×+)
- Net P&L per trade (target: +$0.30 by month-end)
- Avg hold of winners vs losers

### 5. Stop building for 48 hours
5 changes shipped today. No more code until we have 24h of data on what they do.

---

## NOT doing (and why)
- Higher leverage → liquidation = account-killer
- Bigger blanket trade size → fees scale linearly, amplifies thin-edge losses
- More agents this week → already saturated; need clean attribution
- Manual signal overrides → unreproducible experiments
- Trading out of a drawdown → if down $100/day, stop and audit

---

## 30-day target state

A week of 25-35 trades that produces:
- $20-50 net after all fees
- 50%+ WR
- 1.7×+ profit factor
- Zero days losing >$25
- connors_rsi2 + funding_extremes = 70%+ of volume
- Kill-switch has auto-retired 2-3 underperformers

---

## Tonight's action — 5 commands, then walk away 24h

```bash
~/multi_agent_bot/d -k daily_breakout_24h
~/multi_agent_bot/d -k daily_breakout_4h
~/multi_agent_bot/d -k fibonacci
~/multi_agent_bot/d connors_rsi2 0.10
~/multi_agent_bot/d funding_extremes 0.04
```

Telegram for OPENs/CLOSEs only. Ignore everything else.

Next meeting: tomorrow same time. Review 24h data. Decide next move.

---

## Code shipped this session (recap)

1. **Maker orders** — passive limit placement, ~70% fee cut
2. **Confidence cap at 9** — was 10, broken by headcount inflation
3. **Cross-family confluence rule** — only boost when DIFFERENT strategy types agree
4. **WR-weighted kill-switch** — agents below 30% WR auto-dropped
5. **Confidence-graded sizing** — conf 6/7/8/9 → 0.6×/0.8×/1.0×/1.4×
6. **funding_extremes agent** — fades extreme funding rates with EMA50 + RSI confluence
7. **williams_r agent** (earlier today) — Williams %R + EMA200 mean-rev

All in `bot.py`, syntax-validated, hot-reloaded. Backup snapshot in `backups/20260505_190339/`.

---

End of meeting. Run the 5 commands. Walk away.
