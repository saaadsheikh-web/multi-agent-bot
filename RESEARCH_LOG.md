# Research Log — Trading Bot Strategy Ideation

Pure-research log. New strategy ideas, candidate coins, and academic findings.
Each entry timestamped (UTC). Cross-checked against MEGA_STRATEGY_CATALOG.md to flag novelty.

Telegram-worthy novel ideas marked with **[TG-NOVEL]**.

---

## 2026-05-01 03:41 UTC — Initial scan

### Search scope this run
- WebSearch: crypto perp strategies 2026, new altcoin perp listings (Binance/Bybit/BloFin), low-cap trending coins, arxiv crypto microstructure & funding-rate papers, alpha-decay literature, iceberg/hidden-liquidity detection, Hyperliquid HLP vault.
- WebFetch: blocked by network policy (medium.com, arxiv.org not on allowlist). Worked from search snippets only this run. Flag for Saad: enable WebFetch egress for arxiv.org + a few quant blogs to deepen future runs.

### A. Strategy ideas

#### A1. **[TG-NOVEL]** Strategy Decay Detection / Auto-Disable Overlay
- **Premise:** Track each live strategy's rolling edge (e.g. 30-trade trailing ExpR + Sharpe). Auto-pause any strategy whose rolling edge drops below a threshold (e.g. ExpR < 0.05R sustained over N=20 trades) or whose drawdown breaches a band. Re-enable after walk-forward re-validation.
- **Why it might work (vs already-tried):** Catalog has #46 volatility-targeting overlay and #49 risk-parity overlay — both *position-sizing* overlays. There is **no edge-monitoring / decay-detection overlay**. Vertoxquant ("Strategy Decay Detection") and the alpha-decay literature surveyed this run both flag that crypto-strat alpha decays in days-to-months; no real bot can run a fixed-config portfolio for 12+ months without monitoring. This protects every existing P0 strategy and every future addition.
- **Implementation difficulty:** **Low–Med.** New module that hooks into trade-log, computes rolling stats per strategy_id, and toggles a `is_paused` flag on the strategy registry. No model retraining required. ~150-300 LOC.
- **Estimated edge:** Doesn't add per-trade alpha; preserves portfolio-level edge by killing dead strategies before they bleed 30-50% of capital. Plausible 10-30% reduction in max-DD across the portfolio over a year, based on alpha-decay lifespans cited in the research.
- **Source:** vertoxquant.com "Strategy Decay Detection: Building a Warning System for Alpha Erosion"; "The Truth About Automated Forex Strategies: Alpha, Decay, and the Hunt for the Edge" (turmanaube on Medium).

#### A2. Iceberg / Refresh-Liquidity Absorption Detection
- **Premise:** Detect orderbook levels where size *keeps reappearing* after partial fills (resting iceberg). Big iceberg defending a price level = high-conviction defended floor/ceiling. Trade *with* the iceberg until it gets pulled.
- **Why it might work (vs already-tried):** Distinct from catalog #32 (whale-tracker = top-of-book imbalance, gameable) and #33 (liquidation sweep = swing-level taker sweep). Iceberg-refresh is a passive-maker pattern: harder to spoof because the size has to actually fill before refreshing. Bookmap and Exegy material both flag this as a primary "smart-size" tell on perps in 2026.
- **Implementation difficulty:** **Med–High.** Requires depth-of-book deltas (incremental L2 stream), not just snapshots. BloFin WS exposes depth but tick-rate may be aggressive enough that detection latency matters. Need to handle iceberg-refresh detection logic carefully (track per-price-level fill→refresh→fill cycles).
- **Estimated edge:** Per Bookmap reporting, iceberg-defended levels hold ~65-75% of the time intraday on BTC/ETH perps. If properly trade-able, could be a +0.10-0.20R per-trade edge with high WR but low frequency. Best paired as confirmation overlay for #15 S/R bounce or #33 liquidation sweep.
- **Caveat:** Catalog already de-prioritizes #39, #40 due to BloFin tick-data limits — same constraint applies here. Validate data quality before building.
- **Source:** Bookmap "How to Read and Trade Iceberg Orders"; Exegy "Hiding (and Seeking) Liquidity With Iceberg Orders".

#### A3. HLP-Aware Liquidation Cascade Anticipator
- **Premise:** Hyperliquid's HLP vault publishes positioning data (often net-short). When HLP net-short is extreme AND BTC/ETH funding is positive AND price is near a known liquidation cluster (from Coinglass heatmap), expect a downside cascade — short into the cluster, cover at the next liquidity pocket.
- **Why it might work (vs already-tried):** Catalog #33 (liquidation sweep + reversal) trades the *aftermath* (mean-reversion off the wick). This trades the *anticipation* (joining the cascade direction one step early). Different side of the same event. The Feb 1 2026 $700M long blow-up flagged in research was a textbook setup for this.
- **Implementation difficulty:** **Med.** Requires polling HLP positioning (Hyperliquid REST), Coinglass liquidation heatmap (paid tier), and BloFin funding for the same symbol. No need to actually trade on Hyperliquid — it's just a signal source.
- **Estimated edge:** Highly event-driven. Maybe 2-5 setups/month per major coin. When it works, +0.5-1.5R single-trade. When it fails, flat (cascade doesn't trigger) — *not* the inverted bath-trap that #43 funding-fade can be.
- **Caveat:** Coinglass heatmap data has a paywall; HLP data is free. Spec out data sourcing before committing.
- **Source:** KuCoin / ChainCatcher / PANews coverage of HLP "Liquidation Alpha"; CoinGlass liquidation heatmap.

#### A4. Path-Dependent Funding Forecast Overlay (academic)
- **Premise:** Kim & Park (arxiv 2506.08573, 2025) derive path-dependent funding-rate models via infinite-horizon BSDEs. The practical takeaway: next-cycle funding can be forecast from realized funding *path*, not just current snapshot. Use this forecast to filter catalog #43 (funding fade) entries — only fade when forecast funding for the next cycle is *also* extreme (avoiding the fade-then-funding-flips-to-zero trap).
- **Why it might work (vs already-tried):** Catalog #43 enters on snapshot funding > 0.20%. This adds a 1-cycle-ahead filter. Could meaningfully improve #43 hit-rate by 5-15%.
- **Implementation difficulty:** **Med.** Don't need to implement full BSDE — a simple AR(2) or path-feature regression on rolling funding-rate history would capture most of the signal at <50 LOC.
- **Estimated edge:** Overlay on existing #43, not standalone. Modest improvement to a P0 strategy.
- **Source:** arxiv.org/abs/2506.08573 (Kim & Park, "Designing Funding Rates for Perpetual Futures in Cryptocurrency Markets").

#### A5. CEX→DEX Lead-Lag (informational only)
- **Premise:** Recent microstructure research (cited in MDPI two-tiered crypto funding-rate paper) shows CEX leads DEX with ~61% higher integration; "all significant information flow runs CEX-to-DEX with zero reverse causality." A trader on Hyperliquid/Lighter could trade DEX off Binance signals.
- **Why it might NOT apply to us:** Saad's bot is on BloFin (CEX). We are on the *leading* side; no lead-lag arb to harvest. Logging for completeness.
- **Implementation difficulty:** N/A.

### B. New listings / coins surfaced

These are *coins discovered*, not endorsements. Volatility ≠ edge.

| Symbol | Venue / status | Note |
|---|---|---|
| HYPE | Hyperliquid native, on multiple CEXs; Binance listing speculated | $15B mkt cap, $190M+ daily vol — already past the early-stage window |
| MON  | Binance pre-market perp live | Monad mainnet pending; high vol expected at TGE |
| HYPER (Bitcoin Hyper) | Bybit listing speculated | BTC-L2; presale-stage, high execution risk |
| MAXI (Maxi Doge) | Bybit listing speculated | Memecoin; only useful for short-vol post-listing setups |
| FLUID, REI, ZETA | Highlighted as low-cap "gems" Q1-Q2 2026 | Not yet on BloFin — out of scope for now |
| AAPLUSDT, AMZNUSDT, SNDKUSDT | Bybit added equity-perp pairs | Trad-fi-on-perps trend; not on BloFin yet |

**Action item:** None of these are urgent for the bot. Worth checking BloFin perp-listing announcements weekly for HYPE / MON additions — those are the most likely to affect us.

### C. Macro / regime context (May 2026)

- Crypto Twitter sentiment: BTC-favored, broad-altcoin pressure expected. Funding rates likely to compress on alts as long-positioning thins out.
- Q1 2026 derivatives volume ≈ $18.6T (90% of total crypto volume). Perp-market structure dominant — funding-based strategies remain core.
- "Altseason 2021-style" widely doubted. Implication: cross-sectional momentum (#47) probably underperforms; pairs trading (#41) and funding-carry (#48) probably overperform.

### D. Verdict for this run

- **One TG-novel idea queued:** A1 (Strategy Decay Detection overlay) — most actionable, fills a real gap in catalog overlays, low implementation cost.
- **Logged but not TG'd:** A2, A3, A4, A5 — interesting, but A2/A3 are differentiated *extensions* of catalog items rather than orthogonal new edge; A4 is an overlay on existing #43; A5 doesn't apply to BloFin.
- **No coin-level alerts sent.** New listings are speculation-stage; nothing meets a trade-now bar.

### E. Telegram delivery — BLOCKED this run
- Attempted to POST to `api.telegram.org/bot.../sendMessage` from the sandbox shell.
- Result: `HTTP 403 Forbidden` from the local egress proxy with `X-Proxy-Error: blocked-by-allowlist`. `api.telegram.org` is not on the workspace's allowlisted hosts.
- Fallback: dropped `RESEARCH_ALERT.md` in the project root (matches existing SAAD_WAKE_UP / URGENT_ALERT convention) so Saad sees the A1 idea on next sync.
- **Action for Saad:** to enable in-band Telegram from this scheduled task, either (a) allowlist `api.telegram.org` in workspace egress settings, or (b) point this task at the bot.py `tg()` helper (e.g. via a small `outbox/` file the bot tails and forwards), or (c) accept the alert-file fallback as the default delivery path.

---
