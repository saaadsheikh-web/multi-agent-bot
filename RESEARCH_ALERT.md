# Research Agent — Novel Idea Alert
**Generated:** 2026-05-01 03:41 UTC
**From:** scheduled `mab-research-agent` run
**Why a file, not Telegram:** sandbox proxy blocks `api.telegram.org` (HTTP 403, `blocked-by-allowlist`). See RESEARCH_LOG.md §E for fix options.

---

## 🧠 NEW STRATEGY IDEA

**Name:** Strategy Decay Detection / Auto-Disable Overlay

**Premise (one line):** Rolling 30-trade ExpR + Sharpe per `strategy_id`; auto-pause any strategy whose edge drops below threshold (e.g. ExpR < 0.05R sustained over 20 trades), re-enable after walk-forward re-validation.

**Why it might work (vs already-tried):** MEGA_STRATEGY_CATALOG has #46 vol-targeting and #49 risk-parity overlays — both are *position-sizing* overlays. There is **no edge-monitoring overlay**. The alpha-decay literature (Vertoxquant; alpha-decay surveys 2025-2026) puts crypto-strat lifespans at days→months. A fixed-config portfolio quietly bleeds 30-50% of capital before anyone notices a strategy is dead. This protects every existing P0 strategy *and* every future addition.

**Difficulty:** **Low–Med** (~150-300 LOC). Hooks into trade-log, computes rolling stats per `strategy_id`, toggles an `is_paused` flag on the strategy registry. No model retraining required.

**Estimated edge:** Doesn't add per-trade alpha — preserves portfolio-level edge by killing dead strategies before they bleed capital. Plausible **10-30% reduction in max-DD** across the portfolio over a year, based on cited alpha-decay lifespans.

**Source:** vertoxquant.com "Strategy Decay Detection: Building a Warning System for Alpha Erosion"; "The Truth About Automated Forex Strategies: Alpha, Decay, and the Hunt for the Edge".

**Full detail + 4 other (lower-priority) ideas:** `RESEARCH_LOG.md` entry `2026-05-01 03:41 UTC`.
