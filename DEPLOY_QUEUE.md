# DEPLOY QUEUE

Strategies that have passed validation thresholds and are awaiting Saad's approval to flip live.

**Validation thresholds (PASS):** ExpR > +0.20R AND DD(pct_eq) < 40% AND total_trades >= 50

**Approval format:** Reply `deploy <name>` in Telegram to flip live with notional 0.10x. Reply `skip` to keep paper.

---

## Queue

### trend_pullback  🎯 READY FOR LIVE
- **Queued:** 2026-04-30
- **Source report:** BACKTEST_REPORT.md (2026-04-29T18:12:14Z)
- **Stats:** ExpR +0.204R · DD(pct_eq) -22.0% · n=2457 · WR 70.9% · PF 1.81 · Sharpe 4.83
- **Drawdown duration:** 2d
- **Best month:** +68.4% · **Worst month:** -11.3%
- **Avg hold:** 750 min
- **Top coins:** SUI-USDT (+0.36R, n=138), AVAX-USDT (+0.32R, n=113), ATOM-USDT (+0.30R, n=137), TIA-USDT (+0.29R, n=92), ADA-USDT (+0.28R, n=113)
- **Worst coins:** INJ-USDT (+0.11R, n=120), APT-USDT (+0.11R, n=123), ETH-USDT (+0.05R, n=129)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy trend_pullback` (notional 0.10x)
- **Note (2026-04-30 05:02 UTC re-validation):** In latest report ExpR slipped to +0.153R (n=649) — now WATCH-tier on the fresh universe, but kept queued pending Saad's review of the prior result.

### daily_breakout  🎯 READY FOR LIVE
- **Queued:** 2026-04-30
- **Source report:** BACKTEST_REPORT.md (2026-04-30T03:56:39Z)
- **Stats:** ExpR +0.417R · DD(pct_eq) -4.0% · n=290 · WR 83.1% · PF 3.98 · Sharpe 4.32
- **Drawdown duration:** 0d
- **Best month:** +38.4% · **Worst month:** -1.0%
- **Avg hold:** 1074 min
- **Top coins:** XRP-USDT (+0.56R, n=60), ETH-USDT (+0.43R, n=67), SOL-USDT (+0.43R, n=68), BNB-USDT (+0.35R, n=51), BTC-USDT (+0.26R, n=44)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout` (notional 0.10x)

### daily_breakout_24h  🎯 READY FOR LIVE
- **Queued:** 2026-04-30
- **Source report:** BACKTEST_REPORT.md (2026-04-30T03:56:39Z)
- **Stats:** ExpR +0.384R · DD(pct_eq) -5.2% · n=1009 · WR 78.6% · PF 3.97 · Sharpe 6.57
- **Drawdown duration:** 0d
- **Best month:** +65.6% · **Worst month:** +0.5%
- **Avg hold:** 357 min
- **Top coins:** XRP-USDT (+0.48R, n=217), SOL-USDT (+0.44R, n=225), ETH-USDT (+0.42R, n=233), BNB-USDT (+0.32R, n=156), BTC-USDT (+0.20R, n=178)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_24h` (notional 0.10x)

### daily_breakout_4h  🎯 READY FOR LIVE
- **Queued:** 2026-04-30
- **Source report:** BACKTEST_REPORT.md (2026-04-30T13:40:52Z)
- **Stats:** ExpR +0.501R · DD(pct_eq) -7.8% · n=2479 · WR 74.0% · PF 3.86 · Sharpe 10.36
- **Drawdown duration:** 0d
- **Best month:** +181.5% · **Worst month:** +7.3%
- **Avg hold:** 119 min
- **Top coins:** SOL-USDT (+0.65R, n=563), XRP-USDT (+0.54R, n=549), ETH-USDT (+0.48R, n=609), BNB-USDT (+0.48R, n=360), BTC-USDT (+0.30R, n=398)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_4h` (notional 0.10x)
- **Note:** Highest Sharpe (10.36) and ExpR (+0.501R) in the cohort — strongest signal in the report.

### daily_breakout_7d  🎯 READY FOR LIVE
- **Queued:** 2026-04-30
- **Source report:** BACKTEST_REPORT.md (2026-04-30T13:40:52Z)
- **Stats:** ExpR +0.283R · DD(pct_eq) -3.7% · n=195 · WR 75.9% · PF 2.41 · Sharpe 3.63
- **Drawdown duration:** 0d
- **Best month:** +21.3% · **Worst month:** -1.0%
- **Avg hold:** 919 min
- **Top coins:** BNB-USDT (+0.39R, n=27), BTC-USDT (+0.36R, n=25), SOL-USDT (+0.33R, n=49), ETH-USDT (+0.28R, n=54), XRP-USDT (+0.11R, n=40)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_7d` (notional 0.10x)
- **Note:** Lower trade count (n=195) but very tight DD (-3.7%) and clean monthly profile (worst -1.0%).
- **Re-validation 2026-05-01 03:18 UTC:** Strategy reported n=0 in latest run (no fills on 6-symbol limited universe). Keep queued pending re-test on full universe.

### daily_breakout_2h  🎯 READY FOR LIVE
- **Queued:** 2026-05-01
- **Source report:** BACKTEST_REPORT.md (2026-05-01T03:18:35Z)
- **Stats:** ExpR +0.466R · DD(pct_eq) -10.7% · n=3734 · WR 71.7% · PF 3.45 · Sharpe 13.18
- **Drawdown duration:** 0d
- **Best month:** +215.4% · **Worst month:** +26.1%
- **Avg hold:** 43 min
- **Top coins:** DOGE-USDT (+0.56R, n=801), SOL-USDT (+0.51R, n=742), XRP-USDT (+0.49R, n=659), ETH-USDT (+0.47R, n=637), BNB-USDT (+0.33R, n=455)
- **Worst coins:** ETH-USDT (+0.47R, n=637), BNB-USDT (+0.33R, n=455), BTC-USDT (+0.32R, n=440)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_2h` (notional 0.10x)
- **Note:** Top Sharpe of the entire cohort (13.18). Very high trade count and tight monthly worst (+26.1%, never red).

### daily_breakout_12h  🎯 READY FOR LIVE
- **Queued:** 2026-05-01
- **Source report:** BACKTEST_REPORT.md (2026-05-01T03:18:35Z)
- **Stats:** ExpR +0.391R · DD(pct_eq) -8.8% · n=1869 · WR 76.3% · PF 3.37 · Sharpe 5.81
- **Drawdown duration:** 0d
- **Best month:** +147.3% · **Worst month:** +0.8%
- **Avg hold:** 172 min
- **Top coins:** DOGE-USDT (+0.53R, n=361), SOL-USDT (+0.45R, n=368), XRP-USDT (+0.41R, n=348), ETH-USDT (+0.40R, n=329), BNB-USDT (+0.27R, n=222)
- **Worst coins:** ETH-USDT (+0.40R, n=329), BNB-USDT (+0.27R, n=222), BTC-USDT (+0.16R, n=241)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_12h` (notional 0.10x)

### daily_breakout_8h  🎯 READY FOR LIVE
- **Queued:** 2026-05-01
- **Source report:** BACKTEST_REPORT.md (2026-05-01T03:18:35Z)
- **Stats:** ExpR +0.352R · DD(pct_eq) -5.7% · n=785 · WR 72.1% · PF 2.98 · Sharpe 8.42
- **Drawdown duration:** 0d
- **Best month:** +43.4% · **Worst month:** +1.7%
- **Avg hold:** 127 min
- **Top coins:** SOL-USDT (+0.43R, n=164), XRP-USDT (+0.42R, n=140), ETH-USDT (+0.38R, n=127), DOGE-USDT (+0.38R, n=188), BNB-USDT (+0.25R, n=88)
- **Worst coins:** DOGE-USDT (+0.38R, n=188), BNB-USDT (+0.25R, n=88), BTC-USDT (+0.08R, n=78)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_8h` (notional 0.10x)
- **Note:** Cleanest DD profile (-5.7%) of the new arrivals; never had a red month.

### daily_breakout_48h  🎯 READY FOR LIVE
- **Queued:** 2026-05-01
- **Source report:** BACKTEST_REPORT.md (2026-05-01T03:18:35Z)
- **Stats:** ExpR +0.201R · DD(pct_eq) -7.8% · n=467 · WR 73.2% · PF 1.92 · Sharpe 3.85
- **Drawdown duration:** 0d
- **Best month:** +24.5% · **Worst month:** -4.0%
- **Avg hold:** 574 min
- **Top coins:** DOGE-USDT (+0.32R, n=104), ETH-USDT (+0.26R, n=55), SOL-USDT (+0.21R, n=103), BNB-USDT (+0.16R, n=58), XRP-USDT (+0.11R, n=91)
- **Worst coins:** BNB-USDT (+0.16R, n=58), XRP-USDT (+0.11R, n=91), BTC-USDT (+0.09R, n=56)
- **Status:** AWAITING APPROVAL
- **Recommended action:** `deploy daily_breakout_48h` (notional 0.10x)
- **Note:** Marginal PASS — ExpR exactly at +0.201R threshold. Verdict in report is 🟡 KEEP rather than 🟢; consider smaller initial notional or paper-extend.
