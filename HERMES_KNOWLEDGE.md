# HERMES KNOWLEDGE SCAN — 2026-06-09 02:21 UTC

## 📁 FILESYSTEM SCAN

**19 sources available, 0 missing**

- ✅ **drive_backup** (0.01 MB)
- ✅ **chrome_blofin** (1.18 MB)
- ✅ **chrome_binance** (0.22 MB)
- ✅ **chrome_hyperliquid** (0.04 MB)
- ✅ **chrome_polymarket** (2.12 MB)
- ✅ **chrome_goatfunded** (0.01 MB)
- ✅ **hyperliquid_bot** (39.89 MB)
- ✅ **polymarket_bot** (0.0 MB)
- ✅ **blofin_bot** (0.01 MB)
- ✅ **clawbot** (0.0 MB)
- ✅ **shams_bot** (0.0 MB)
- ✅ **trading_bot** (0.0 MB)
- ✅ **bot_brain** (0.0 MB)
- ✅ **hermes_master** (0.0 MB)
- ✅ **backtests** (112.93 MB)
- ✅ **trade_journal** (1.14 MB)
- ✅ **strategy_pool** (0.03 MB)
- ✅ **db** (1.48 MB)
- ✅ **hyperliquid_db** (0.0 MB)

## 🤖 OTHER TRADING BOTS

### hyperliquid

### hyperliquid_log_tail

### polymarket
  Files: 

### blofin_bot
  Size: 8 KB

### clawbot
  Size: 3 KB

### shams_bot
  Size: 4 KB

### trading_bot
  Size: 0 KB

## 📄 GOOGLE DRIVE DOCUMENTS

### 00_INDEX.md
```
# Google Drive Backup — Index

**Saved:** 2026-05-18
**Source account:** saaadsheikh@gmail.com
**Saved by:** Claude (Cowork mode)

This folder is a local backup of all crypto-bot-related files from Google Drive.

---

## Files in this folder

| # | File | What it is | Date in Drive |
|---|---|---|---|
| 01 | Trading_Bot_Optimization_Strategy_2026-05-05.md | The May 5 post-mortem — fees ate 100% of edge, recommends maker orders | 2026-05-05 |
| 02 | BACKTEST_REPORT_2026-05-16.md | Nightly hunter's KEEP/TUNE/KILL verdict table | 2026-05-16 |
| 03 | HUNTER_BRIEF_note.md | Pointer to ~/multi_agent_bot/HUNTER_BRIEF.md (too big to inline) | 2026-05-16 |

---

## Drive files NOT crypto-related (skipped)

- `Infinity Lux — Business Memory (Claude)` — separate business project
- `fix_deploy.txt` x2 — old base64+gzip installers from 2026-04-28
- `one_liner.txt` — old self-extracting installer from 2026-04-28
- `leads_year_long.json` — Infinity Lux leads database

These exist in Drive but aren't part of the trading bot.

---

## How to refresh this backup

In a new Claude chat, say:
> "Pull all crypto-bot files from Google Drive and refresh ~/multi_agent_bot/drive_backup/"

Claude will re-fetch and update.

```

### 01_Trading_Bot_Optimization_Strategy_2026-05-05.md
```
# Trading Bot Optimization Strategy

**Source:** Google Drive (2026-05-05) — saaadsheikh@gmail.com
**Drive URL:** https://docs.google.com/document/d/1Zxg6jINLxyQgtZR6T-ZKRo6YQrU6piEKKRlOXH7BYHw/edit
**Saved locally:** 2026-05-18 by Claude (Cowork)

---

## The Fee Answer (and a Shocking Finding)

**Fees:** $2.51 estimated total (mixed taker/maker rate)

| Scenario | Fee Cost |
|---|---|
| Worst case (all taker, 0.06% × 2 sides) | $3.77 |
| Real-world mixed (0.04% × 2 sides) | $2.51 |
| Best case (all maker, 0.02% × 2 sides) | $1.26 |

**Pre-fee gross profit:** +$2.33
**After realistic fees:** −$0.18 to +$1.08

The bot is roughly break-even after fees. Fees ate ~100% of the edge. This is the single biggest leak.

---

## The Shocking Confidence Finding

| Confidence | n | WR | PnL | Avg/trade |
|---|---|---|---|---|
| ≤7 (low) | 3 | 100% | +$2.21 | +$0.74 |
| 8 | 9 | 11% | −$0.02 | −$0.00 |
| 9 | 1 | 100% | +$0.43 | +$0.43 |
| 10 (highest) | 23 | 39% | −$0.28 | −$0.01 |

**Confidence is inverted.** The "10/10 conviction" trades LOST money on average. Scaling up high-conf trades right now would lose more, not less.

---

## Should you size up to $200/trade? Use 10–30x leverage?

**Short answer: NO. Not yet.**

### Bigger trades scale fees linearly

| Avg/trade | Gross | Fees | Net |
|---|---|---|---|
| $87 (current) | +$2.33 | $2.51 | −$0.18 |
| $200 | +$5.36 | $5.77 | −$0.41 |
| $500 | +$13.30 | $14.40 | −$1.10 |

Doubling size doesn't double profit — it doubles fees too.

### Higher leverage doesn't make winners bigger — it makes losers fatal

- 5× leverage → liquidation at ~20% adverse move (huge buffer)
- 10× → liq at ~10% (safe)
- 20× → liq at ~5% (one wick wipes you)
- 30× → liq at ~3.3% (one bad candle = wiped)
- 50×+ → suicide

Worst single-trade move on the bot was −2.27%. At 30× a 3.5% wick liquidates before SL fires.

---

## What WILL make more money — ranked

1. **Make the bot use MAKER orders** ⭐ BIGGEST LEVER
   - Cuts fees ~70% ($2.51 → $0.83)
   - Sam
```

### 02_BACKTEST_REPORT_2026-05-16.md
```
# BACKTEST REPORT — From Google Drive

**Source:** Google Drive (2026-05-16) — saaadsheikh@gmail.com
**Drive URL:** https://docs.google.com/document/d/1CQsG9oPeZaCHWVSjKuMGkI1hfo11eWA_C2BMKXL5YlM/edit
**Generated:** 2026-05-16T03:15:49Z
**Saved locally:** 2026-05-18 by Claude (Cowork)

---

## Verdict Table — Agents to KEEP & SCALE 🟢

| Agent | Trades | WR | Exp_R | DD(eq) | PF | Sharpe |
|---|---|---|---|---|---|---|
| daily_breakout_4h | 5,696 | 77.2% | +0.726 | −20.7% | 4.98 | 6.00 |
| daily_breakout | 576 | 82.1% | +0.670 | −9.8% | 5.83 | 2.88 |
| daily_breakout_2h | 6,900 | 74.0% | +0.604 | −17.5% | 3.99 | **15.84** |
| daily_breakout_24h | 2,014 | 82.6% | +0.573 | −11.9% | 5.22 | 3.95 |
| daily_breakout_12h | 3,437 | 79.9% | +0.548 | −17.5% | 4.81 | 6.22 |
| daily_breakout_48h | 805 | 78.3% | +0.507 | −15.3% | 3.71 | 3.46 |
| daily_breakout_8h | 1,736 | 77.8% | +0.488 | −6.2% | 4.02 | 10.75 |
| asian_pump | 36 | 83.3% | +0.399 | −0.3% | 37.49 | 23.20 |

## KEEP 🟡 (working but smaller edge)

| Agent | Trades | WR | Exp_R | PF | Sharpe |
|---|---|---|---|---|---|
| trend_pullback | 1,241 | 73.0% | +0.213 | 1.95 | 5.09 |
| macd_cross | 1,396 | 75.2% | +0.203 | 2.16 | 7.57 |

## TUNE 🟠 (marginal)

| Agent | Trades | WR | Exp_R | PF |
|---|---|---|---|---|
| donchian | 988 | 51.6% | +0.043 | 1.13 |
| rsi_divergence | 1,013 | 46.7% | +0.018 | 1.04 |

## KILL 🔴 (losers — backtest confirmed)

- meanrev (45.1% WR, -0.060 Exp_R)
- candlestick (42.0% WR, -0.061)
- momentum (43.1% WR, -0.091, 15K trades, −95% DD)
- ema_ribbon (43.4% WR, -0.097, 10K trades, −95% DD)
- bb_squeeze (41.3% WR, -0.136, 2K trades, −95% DD)
- scalp (46.2% WR, -0.179)
- asymmetric (40.0% WR, -0.188)
- swing (34.8% WR, -0.330)
- volume_capitulation (0% WR, -0.979, 10 trades)
- funding, daily_breakout_4h_trend, daily_breakout_7d, pump_dump_reversal, supertrend — 0 trades, dead code

---

## Combined 20-symbol leaderboard — appended 2026-05-16 03:17 UTC

| Agent | Trades | WR | Exp_R | DD(eq) | PF | 
```

### 03_HUNTER_BRIEF_note.md
```
# HUNTER_BRIEF.md (Drive copy) — Note

**Source:** Google Drive (2026-05-16) — saaadsheikh@gmail.com
**Drive URL:** https://docs.google.com/document/d/1LIDev8WAd64qtdhZ_L35IxxlbDbed_khKU5PCa0N0RE/edit
**Size:** 60,045 chars — too big to inline in this chat without burning tokens

---

## Status

This Drive file is a copy of `~/multi_agent_bot/HUNTER_BRIEF.md` which already exists locally. Both are the same content — Drive is just a backup.

**To read it:**
- Local: `cat ~/multi_agent_bot/HUNTER_BRIEF.md`
- Drive: open the URL above

**To re-sync from Drive if local is missing:**
- Ask Claude in a new chat: "Pull HUNTER_BRIEF.md from Drive (id 1LIDev8WAd64qtdhZ_L35IxxlbDbed_khKU5PCa0N0RE) and save it to ~/multi_agent_bot/drive_backup/"

---

## What's in it (from snapshot)

- Nightly strategy hunter's full 365-day backtest output
- Per-agent / per-symbol expected R, drawdown, Sharpe
- Originally recommended deploying daily_breakout_4h at 0.10x — live data has since contradicted some of these recommendations (live evidence overrides backtest)

```

### HUNTER_BRIEF_from_drive.md
```

```

## 📊 BACKTEST KNOWLEDGE

- Strategy pool: 75 variants
- Backtest CSV files: 0 (0.0 MB)

| Agent | Variants | Best WR | Best PF |
|-------|----------|---------|---------|
| ? | 75 | 0% | 0.0 |

## 💾 DATABASE SNAPSHOT

- Total trades: 381
- Closed: 380
- Lifetime P&L: $-15.10
- Best agent: macd_cross ($+32.37)