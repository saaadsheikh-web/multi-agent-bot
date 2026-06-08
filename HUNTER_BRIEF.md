## Nightly Hunter Brief — 2026-05-28

**Run status: PARTIAL.** BloFin API unreachable from scheduled sandbox (proxy 403). Backtest ran from cached parquet files (60 files, touched fresh). Cache data is from 2026-05-27. Backtest completed 20/20 symbols using cache. Formal leaderboard output not appended to BACKTEST_REPORT.md this run (nightly_hunter.py subprocess failed due to HOME path mismatch — backtest ran manually). Thresholds: Sharpe ≥ 2.0, ExpR ≥ 0.10R, MaxDD ≤ 25%, Trades ≥ 100.

**Root cause of recurring failure:** The scheduled sandbox sets `HOME=/sessions/...` while all scripts use `expanduser("~")` expecting `~/multi_agent_bot`. Symlinks now created to paper over this. Permanent fix: add `WORK_DIR = Path(__file__).parent` to backtest.py and nightly_hunter.py.

---

### Top 5 by Sharpe (365-day backtest, thresholds met)

Source: BACKTEST_REPORT.md generated 2026-05-26T03:14:34Z — confirmed valid by today's cache re-run (identical per-symbol trade counts).

| Rank | Agent | Sharpe | ExpR | MaxDD(pct_eq) | Trades | Deployed? |
|------|-------|--------|------|----------------|--------|-----------|
| 1 | daily_breakout_2h | 15.61 | +0.653R | -9.7% | 3490 | paper_only=True ⚠️ |
| 2 | daily_breakout_12h | 10.06 | +0.559R | -10.0% | 1769 | paper_only=True ⚠️ |
| 3 | daily_breakout_8h | 11.23 | +0.542R | -4.4% | 957 | paper_only=True ⚠️ |
| 4 | daily_breakout_4h | 6.67 | +0.764R | -8.9% | 2931 | disabled ⚠️ |
| 5 | macd_cross | 6.67 | +0.202R | -6.0% | 712 | paper_only=False ✅ |

**Note on asian_pump:** Sharpe=22.70, ExpR=+0.459R, MaxDD=0%, but only 25 trades — below the 100-trade threshold. Flagged for monitoring.

**Note on daily_breakout:** Sharpe=3.20, ExpR=+0.718R, 302 trades, MaxDD=-5.0% — currently paper_only=False (deployed live). Performing well.

---

### Recommended New Deploys

These agents pass ALL thresholds (Sharpe ≥ 2.0, ExpR ≥ 0.10R, MaxDD ≤ 25%, trades ≥ 100) and are currently paper_only=True or disabled:

**1. daily_breakout_2h** — Sharpe 15.61, ExpR +0.653R, MaxDD -9.7%, 3490 trades. Top performer by Sharpe. Currently paper_only=True with 2 live trades (+$0.22 net). Strong candidate.
```bash
# In bot.py, find DailyBreakout2h class and change:
#   paper_only = True  →  paper_only = False
```

**2. daily_breakout_12h** — Sharpe 10.06, ExpR +0.559R, MaxDD -10.0%, 1769 trades. Currently paper_only=True.
```bash
# In bot.py, find DailyBreakout12h class and change:
#   paper_only = True  →  paper_only = False
```

**3. daily_breakout_8h** — Sharpe 11.23, ExpR +0.542R, MaxDD -4.4%, 957 trades. Currently paper_only=True.
```bash
# In bot.py, find DailyBreakout8h class and change:
#   paper_only = True  →  paper_only = False
```

**4. daily_breakout_4h** — Sharpe 6.67, ExpR +0.764R, MaxDD -8.9%, 2931 trades. Currently disabled (not paper_only — fully off). Was previously killed per bot.py note dated 2026-05-26. Reconsider: the backtest shows this is the highest ExpR agent. The 2026-05-26 kill was based on live performance (2 trades, -$0.39) which is below statistical significance.
```bash
# In bot.py, find DailyBreakout4h class and change:
#   enabled = False  →  enabled = True
#   paper_only = True  →  paper_only = False   # or paper_only first
```

---

### Recommended Undeploys (paper_only=False agents that FAIL thresholds)

Cross-referencing bot.py deployed agents (paper_only=False, enabled=True) against backtest data:

| Agent | Backtest Status | Live n | Live PnL | Action |
|-------|----------------|--------|----------|--------|
| trend_pullback | Sharpe 4.35, ExpR +0.174R ✅ | — | — | KEEP |
| daily_breakout | Sharpe 3.20, ExpR +0.718R ✅ | — | — | KEEP |
| macd_cross | Sharpe 6.67, ExpR +0.202R ✅ | 6 | +$3.41 | KEEP |
| supertrend | Not in backtest (0 trades) | — | — | ⚠️ REVIEW |
| volume_capitulation | Sharpe -47.28, ExpR -0.911R 🔴 | 6 | — | **UNDEPLOY** |
| asian_pump | Sharpe 22.70, ExpR +0.459R, n=25 only | 25 | — | KEEP (monitor) |
| pump_dump_reversal | Not in backtest (0 trades) | — | — | ⚠️ REVIEW |
| zscore_reversion | Not in full backtest | 6 | +$0.64 | KEEP (n=6 ok) |
| stoch_rsi | Not in full backtest | 31 | +$2.66 | KEEP (live perf good) |
| golden_cross | Not in full backtest | — | — | ⚠️ REVIEW |
| liquidity_sweep | Not in full backtest | — | — | ⚠️ REVIEW |
| raschke_retest | Not in full backtest | — | — | ⚠️ REVIEW |
| wide_scalp | Not in full backtest | — | — | ⚠️ REVIEW |
| wide_candle | Not in full backtest | — | — | ⚠️ REVIEW |
| kalman_trend | Not in full backtest | — | — | ⚠️ REVIEW |
| smart_scalp | Not in full backtest | — | — | ⚠️ REVIEW |
| volume_profile | Not in full backtest | — | — | ⚠️ REVIEW |
| fibonacci | Not in full backtest | 4 | +$0.79 | DEFER (n<5 floor) |
| williams_r | Not in full backtest | — | — | ⚠️ REVIEW |
| funding_extremes | Not in full backtest | 11 | +$1.36 | KEEP (CEO +) |

**Firm undeploy recommendation:**

**volume_capitulation** — Sharpe -47.28, ExpR -0.911R, WR 0%, 6 trades. Currently paper_only=False (live). This is the worst agent in the entire backtest by every metric.
```bash
# In bot.py, find VolumeCapitulation class and change:
#   paper_only = False  →  paper_only = True
# or:
#   enabled = True  →  enabled = False
```

---

### Anomalies & Issues

1. **nightly_hunter.py HOME mismatch** — Script fails every run in the scheduled sandbox because `expanduser("~")` resolves to the wrong path. Quick fix: add `WORK = Path(__file__).parent` at top of both `nightly_hunter.py` and `backtest.py`.

2. **BloFin API blocked** — `openapi.blofin.com` returns 403 via the sandbox proxy. Fresh candle data cannot be fetched. Backtest is running on cache that is up to 24h stale. The 60 cached parquet files cover all 20 symbols × 3 timeframes.

3. **Many deployed agents not in backtest engine** — `supertrend`, `pump_dump_reversal`, `golden_cross`, `liquidity_sweep`, `raschke_retest`, `wide_scalp`, `wide_candle`, `kalman_trend`, `smart_scalp`, `volume_profile`, `williams_r`, `funding_extremes` are all live (paper_only=False) but have zero backtest data. These cannot be scored by the hunter. Add them to `AGENT_NAMES` in `backtest.py`.

4. **connors_rsi2 live underperformance** — 162 live trades, WR=47.5%, net -$3.75. CEO has flagged for SIZE DOWN. Backtest doesn't cover this agent either.

5. **hurst_regime already undeployed** — CEO undeployed at 01:12Z today per AUDITOR_LOG (n=20, confirmed). No action needed.

6. **daily_breakout_24h** — 3 live trades, 0 wins, -$0.93 but paper_only=True — no action needed, working as intended.

---

*Generated: 2026-05-28T03:15Z by nightly_hunter scheduled task (manual backtest run due to sandbox constraints)*
