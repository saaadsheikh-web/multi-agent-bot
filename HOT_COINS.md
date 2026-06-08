# Hot Coins — Trending Baseline

Last updated: 2026-05-01 03:18 UTC (4H sweep run 5)

| Symbol | Name | Notes |
|--------|------|-------|
| ACN | AITECH Cloud Network | NEW #1 trending (returned from earlier runs) |
| PENGU | Pudgy Penguins | Persisting #2, was top in run 4 |
| MEGA | MegaETH | Persisting #3, post-TGE volatility easing |
| LUNC | Terra Luna Classic | Returning #4 (was in run 3) |
| ASTEROID | Asteroid Shiba | NEW #5 — meme appearance, fits risk-on |
| SOL | Solana | NEW #6 — major itself trending alongside +0.89% spot |
| AI | Gensyn | Persisting #7 |
| PROS | Pharos | Returning #8 (was in run 3) |
| HYPE | Hyperliquid | Returning #9 (was in run 3) |

Diff vs run 4: PERSIST = MEGA, AI, PENGU; RETURN = LUNC, PROS, HYPE, ACN; NEW = ASTEROID, SOL; DROPPED = TAO.
Coverage: Direct CoinGecko trending endpoint clean this run (Chrome MCP). Top 10 captured.
Notable: SOL itself trending = alt rotation broadening; ASTEROID meme entry consistent with mild risk-on confluence (BTC +1.27%, S&P record, RSI 64.9). HOT_COINS list growing to 9 unique persisting/returning entries — momentum building under the surface.

---

## Coin Hunter sweep — 2026-05-01 03:42 UTC

**Sources:** CoinGecko `/search/trending` (top 10), CoinGecko `/coins/markets` (volume_desc, 4 pages = 1000 coins, filtered: cap<$50M, 24h>+30%, vol>0.5×cap), BloFin `/market/instruments?instType=SWAP` (496 perps, last-14d listings cross-referenced against bot's NEWS_SYMBOLS at bot.py:171).
**Telegrams sent today by this agent:** 0/2.

### Trending diff vs run 5
| Symbol | Status | Notes |
|--------|--------|-------|
| MEGA | PERSIST | Now #1 trending; cap $180M; -29.2% 24h; vol/cap 2.64× — high-volume dump from highs, possible reload |
| PENGU | PERSIST | #2; cap $630M; +4.1% 24h |
| LUNC | PERSIST | #3 |
| ACN | PERSIST | #4 |
| ASTEROID | PERSIST | #5; cap $158M; +23.4% 24h |
| AI (Gensyn) | PERSIST | #6; cap $52.9M; -27.8% 24h post-pump dump; vol/cap 0.56× |
| SOL | PERSIST | #7 |
| **SKYAI** | **NEW** | **#8 trending**; cap $380M; **+32.4% 24h**; vol/cap 0.27×; **at ATH (-0.2% off)** — fresh breakout |
| HYPE | PERSIST | #9 |
| **USDM** (MegaUSD) | NEW | #10 trending — stablecoin, ignore for entry play |
| PROS | DROPPED | rolled out |

### New BloFin perp listings (last 14 days, not in bot's NEWS_SYMBOLS)
| Symbol | Listed | Note |
|--------|--------|------|
| **AIGENSYN** | 1.5d ago | Maps to trending #6 ($AI / Gensyn) — perp listing very fresh; underlying spot dumped -28% 24h, looks like post-listing distribution |
| **BLEND** | 1.7d ago | New BloFin perp — no signal in trending or gainers; isolated listing |
| **OPG** | 8.5d ago | Older perp, no momentum signal |
| AVGO | 10.6d ago | Broadcom tokenized stock perp — equity, not crypto-native (info only) |
| MSFT | 10.6d ago | Microsoft tokenized stock perp — equity, not crypto-native (info only) |

### Small-cap gainers (cap<$50M, 24h>+30%, vol>0.5×cap)
| Symbol | Name | Cap | 24h % | Vol/Cap | ATH off | Notes / Conviction |
|--------|------|-----|-------|---------|---------|---------------------|
| TIME | chrono.tech | $4.78M | +149.85% | 0.79× | -98.8% | Dead-coin revival pump; ATH -98.8% means 50× away from highs. Volume confirms but tells of speculative resurrection. **LOW** — looks like coordinated pump on illiquid name |
| UPEG | Unipeg | $13.3M | +84.1% | 0.90× | n/a | Solid vol/cap; obscure project; no other signals. **LOW-MED** |
| TDROP | ThetaDrop | $7.97M | +31.2% | 0.96× | -98.8% | Theta NFT marketplace token; legit ecosystem; modest move with confirmation. **LOW-MED** |
| ST | Sentio Token | $4.91M | +31.1% | **4.71×** | -32.5% | **Strongest vol/cap of any candidate** — heavy real interest; small cap; only -32% off ATH (not a dead-coin revival). **MED** |
| UNC | unc | $4.31M | +45.3% | 0.89× | -41.8% | Generic ticker, project unclear from API. **LOW** — too opaque |
| SCAM | Scam Altman | $1.09M | +78.0% | 5.56× | -91.0% | Name literally "Scam Altman" — joke/meme. **FLAG, do not recommend** per hard rules |

### Candidate summary (this sweep)
- **MED conviction:** ST (Sentio), SKYAI, AIGENSYN
  - **ST**: small-cap + 4.71× vol/cap is the standout signal among gainers; not at ATH so room to run
  - **SKYAI**: trending + breakout to ATH + +32% with healthy vol; cap $380M is mid not small, so capped upside vs micro-caps but stronger trend confirmation
  - **AIGENSYN**: trending + brand-new BloFin perp (only 1.5d old) — but already dumping -28% 24h, so the easy entry is gone; watch for stabilization
- **LOW-MED:** UPEG, TDROP
- **LOW:** TIME, UNC, BLEND, OPG
- **FLAGGED (do not recommend):** SCAM (Scam Altman)
- **HIGH conviction:** none this sweep — no candidate hits all four signals (trending + low cap + volume + new listing) simultaneously

### Action
- No Telegram sent (no HIGH-conviction trigger; quota 0/2 used today, preserved).
- Saad's bot does NOT auto-trade unlisted symbols. ST / SKYAI / AIGENSYN are spot-only manual considerations on BloFin (or whatever venue they're listed on) until Saad opts to add to NEWS_SYMBOLS in bot.py.
- Recommend re-running this sweep in ~4–8h to see whether ST sustains the vol/cap ratio or fades; whether AIGENSYN base-builds after its post-listing dump; whether SKYAI holds the ATH breakout.
