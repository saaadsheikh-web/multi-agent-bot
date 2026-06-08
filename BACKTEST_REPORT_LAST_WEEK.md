# BACKTEST REPORT
Generated: 2026-05-17T03:33:37.934428+00:00

## Verdict Table
| AGENT | TRADES | WIN% | AVG_R | EXP_R | DD(fixed) | DD(pct_eq) | PF | SHARPE | VERDICT |
|-------|--------|------|-------|-------|-----------|------------|-----|--------|---------|
| daily_breakout_4h | 3606 | 77.5% | +0.761 | +0.761 | -4.3% | -12.4% | 5.11 | 6.32 | 🟢 KEEP & SCALE |
| daily_breakout | 368 | 83.7% | +0.681 | +0.681 | -2.8% | -7.0% | 6.14 | 3.35 | 🟢 KEEP & SCALE |
| daily_breakout_2h | 4262 | 74.2% | +0.645 | +0.645 | -5.6% | -13.7% | 4.12 | 15.64 | 🟢 KEEP & SCALE |
| daily_breakout_24h | 1296 | 84.1% | +0.601 | +0.601 | -3.6% | -8.1% | 5.79 | 4.62 | 🟢 KEEP & SCALE |
| daily_breakout_12h | 2188 | 81.5% | +0.562 | +0.562 | -3.5% | -11.6% | 5.15 | 8.09 | 🟢 KEEP & SCALE |
| daily_breakout_8h | 1154 | 78.7% | +0.528 | +0.528 | -5.0% | -5.6% | 4.28 | 11.03 | 🟢 KEEP & SCALE |
| daily_breakout_48h | 519 | 79.0% | +0.484 | +0.484 | -5.2% | -10.8% | 3.67 | 5.04 | 🟢 KEEP & SCALE |
| asian_pump | 27 | 85.2% | +0.454 | +0.454 | -0.0% | -0.0% | 164.59 | 23.50 | 🟠 TUNE |
| trend_pullback | 731 | 74.4% | +0.207 | +0.207 | -6.2% | -10.5% | 1.99 | 5.11 | 🟡 KEEP |
| macd_cross | 854 | 76.2% | +0.200 | +0.200 | -4.4% | -7.0% | 2.22 | 6.73 | 🟡 KEEP |
| donchian | 756 | 52.1% | +0.043 | +0.043 | -16.8% | -19.9% | 1.13 | 0.94 | 🟠 TUNE |
| rsi_divergence | 646 | 46.3% | +0.034 | +0.034 | -19.3% | -18.4% | 1.08 | 0.70 | 🟠 TUNE |
| candlestick | 826 | 42.1% | -0.065 | -0.065 | -68.1% | -53.6% | 0.86 | -1.26 | 🔴 KILL |
| momentum | 9683 | 43.7% | -0.085 | -0.085 | -748.7% | -95.4% | 0.81 | -4.13 | 🔴 KILL |
| scalp | 32 | 50.0% | -0.089 | -0.089 | -8.6% | -8.9% | 0.84 | -1.49 | 🔴 KILL |
| ema_ribbon | 6689 | 43.6% | -0.095 | -0.095 | -527.8% | -96.0% | 0.79 | -4.29 | 🔴 KILL |
| meanrev | 38 | 42.1% | -0.123 | -0.123 | -10.2% | -9.8% | 0.75 | -1.88 | 🔴 KILL |
| bb_squeeze | 1508 | 41.2% | -0.135 | -0.135 | -204.0% | -90.4% | 0.72 | -4.09 | 🔴 KILL |
| asymmetric | 595 | 39.7% | -0.184 | -0.184 | -108.5% | -70.8% | 0.72 | -3.06 | 🔴 KILL |
| swing | 62 | 30.6% | -0.423 | -0.423 | -28.9% | -25.8% | 0.36 | -9.63 | 🔴 KILL |
| volume_capitulation | 7 | 0.0% | -0.935 | -0.935 | -6.5% | -6.4% | 0.00 | -49.60 | 🔴 KILL |
| funding | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| daily_breakout_4h_trend | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| daily_breakout_7d | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| pump_dump_reversal | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| supertrend | 0 | — | — | — | — | — | — | — | 🔴 KILL |

## Auto-prune Actions
(none)

## Per-Agent Detail
### daily_breakout_4h  🟢 KEEP & SCALE
- Trades: 3606 W=2794 L=812 WR=77.5%
- Exp: +0.761R  PF: 5.11  Sharpe: 6.32
- MaxDD(fixed): -4.3%  MaxDD(pct_eq): -12.4%  DDdur: 0d
- Best month: +517.9%  Worst: +32.4%
- Avg hold: 56 min
- Top coins: OP-USDT (+0.83R, n=550), ARB-USDT (+0.82R, n=546), TIA-USDT (+0.78R, n=570), SUI-USDT (+0.75R, n=675), TAO-USDT (+0.71R, n=669)
- Worst coins: SUI-USDT (+0.75R, n=675), TAO-USDT (+0.71R, n=669), INJ-USDT (+0.70R, n=596)

### daily_breakout  🟢 KEEP & SCALE
- Trades: 368 W=308 L=60 WR=83.7%
- Exp: +0.681R  PF: 6.14  Sharpe: 3.35
- MaxDD(fixed): -2.8%  MaxDD(pct_eq): -7.0%  DDdur: 0d
- Best month: +107.7%  Worst: +3.4%
- Avg hold: 323 min
- Top coins: TAO-USDT (+0.86R, n=56), INJ-USDT (+0.78R, n=60), TIA-USDT (+0.69R, n=59), ARB-USDT (+0.66R, n=68), OP-USDT (+0.61R, n=59)
- Worst coins: ARB-USDT (+0.66R, n=68), OP-USDT (+0.61R, n=59), SUI-USDT (+0.51R, n=66)

### daily_breakout_2h  🟢 KEEP & SCALE
- Trades: 4262 W=3163 L=1099 WR=74.2%
- Exp: +0.645R  PF: 4.12  Sharpe: 15.64
- MaxDD(fixed): -5.6%  MaxDD(pct_eq): -13.7%  DDdur: 0d
- Best month: +271.1%  Worst: +53.7%
- Avg hold: 26 min
- Top coins: INJ-USDT (+0.71R, n=695), TAO-USDT (+0.69R, n=882), OP-USDT (+0.66R, n=709), ARB-USDT (+0.65R, n=551), SUI-USDT (+0.61R, n=772)
- Worst coins: ARB-USDT (+0.65R, n=551), SUI-USDT (+0.61R, n=772), TIA-USDT (+0.55R, n=653)

### daily_breakout_24h  🟢 KEEP & SCALE
- Trades: 1296 W=1090 L=206 WR=84.1%
- Exp: +0.601R  PF: 5.79  Sharpe: 4.62
- MaxDD(fixed): -3.6%  MaxDD(pct_eq): -8.1%  DDdur: 0d
- Best month: +189.9%  Worst: +3.2%
- Avg hold: 126 min
- Top coins: TIA-USDT (+0.75R, n=200), ARB-USDT (+0.70R, n=220), OP-USDT (+0.63R, n=187), SUI-USDT (+0.55R, n=267), TAO-USDT (+0.51R, n=231)
- Worst coins: SUI-USDT (+0.55R, n=267), TAO-USDT (+0.51R, n=231), INJ-USDT (+0.49R, n=191)

### daily_breakout_12h  🟢 KEEP & SCALE
- Trades: 2188 W=1784 L=404 WR=81.5%
- Exp: +0.562R  PF: 5.15  Sharpe: 8.09
- MaxDD(fixed): -3.5%  MaxDD(pct_eq): -11.6%  DDdur: 0d
- Best month: +179.6%  Worst: +8.3%
- Avg hold: 75 min
- Top coins: TIA-USDT (+0.60R, n=357), SUI-USDT (+0.57R, n=419), ARB-USDT (+0.57R, n=329), OP-USDT (+0.56R, n=341), INJ-USDT (+0.54R, n=325)
- Worst coins: OP-USDT (+0.56R, n=341), INJ-USDT (+0.54R, n=325), TAO-USDT (+0.53R, n=417)

### daily_breakout_8h  🟢 KEEP & SCALE
- Trades: 1154 W=908 L=246 WR=78.7%
- Exp: +0.528R  PF: 4.28  Sharpe: 11.03
- MaxDD(fixed): -5.0%  MaxDD(pct_eq): -5.6%  DDdur: 0d
- Best month: +71.1%  Worst: +14.7%
- Avg hold: 66 min
- Top coins: ARB-USDT (+0.63R, n=162), OP-USDT (+0.54R, n=197), INJ-USDT (+0.54R, n=183), TAO-USDT (+0.54R, n=231), TIA-USDT (+0.47R, n=184)
- Worst coins: TAO-USDT (+0.54R, n=231), TIA-USDT (+0.47R, n=184), SUI-USDT (+0.46R, n=197)

### daily_breakout_48h  🟢 KEEP & SCALE
- Trades: 519 W=410 L=109 WR=79.0%
- Exp: +0.484R  PF: 3.67  Sharpe: 5.04
- MaxDD(fixed): -5.2%  MaxDD(pct_eq): -10.8%  DDdur: 0d
- Best month: +53.2%  Worst: +3.1%
- Avg hold: 213 min
- Top coins: ARB-USDT (+1.08R, n=61), TIA-USDT (+0.66R, n=62), OP-USDT (+0.40R, n=99), TAO-USDT (+0.39R, n=114), INJ-USDT (+0.35R, n=56)
- Worst coins: TAO-USDT (+0.39R, n=114), INJ-USDT (+0.35R, n=56), SUI-USDT (+0.32R, n=127)

### asian_pump  🟠 TUNE
- Trades: 27 W=23 L=4 WR=85.2%
- Exp: +0.454R  PF: 164.59  Sharpe: 23.50
- MaxDD(fixed): -0.0%  MaxDD(pct_eq): -0.0%  DDdur: 0d
- Best month: +2.2%  Worst: +0.1%
- Avg hold: 119 min
- Top coins: ARB-USDT (+0.68R, n=6), TAO-USDT (+0.66R, n=5), SUI-USDT (+0.40R, n=2), OP-USDT (+0.38R, n=10), TIA-USDT (+0.11R, n=3)
- Worst coins: OP-USDT (+0.38R, n=10), TIA-USDT (+0.11R, n=3), INJ-USDT (-0.03R, n=1)

### trend_pullback  🟡 KEEP
- Trades: 731 W=544 L=187 WR=74.4%
- Exp: +0.207R  PF: 1.99  Sharpe: 5.11
- MaxDD(fixed): -6.2%  MaxDD(pct_eq): -10.5%  DDdur: 1d
- Best month: +23.6%  Worst: -5.2%
- Avg hold: 467 min
- Top coins: SUI-USDT (+0.35R, n=139), TIA-USDT (+0.29R, n=92), TAO-USDT (+0.22R, n=131), ARB-USDT (+0.17R, n=124), OP-USDT (+0.12R, n=125)
- Worst coins: ARB-USDT (+0.17R, n=124), OP-USDT (+0.12R, n=125), INJ-USDT (+0.11R, n=120)

### macd_cross  🟡 KEEP
- Trades: 854 W=651 L=203 WR=76.2%
- Exp: +0.200R  PF: 2.22  Sharpe: 6.73
- MaxDD(fixed): -4.4%  MaxDD(pct_eq): -7.0%  DDdur: 0d
- Best month: +29.9%  Worst: +1.1%
- Avg hold: 108 min
- Top coins: TAO-USDT (+0.27R, n=144), OP-USDT (+0.27R, n=157), SUI-USDT (+0.19R, n=142), INJ-USDT (+0.19R, n=133), ARB-USDT (+0.18R, n=136)
- Worst coins: INJ-USDT (+0.19R, n=133), ARB-USDT (+0.18R, n=136), TIA-USDT (+0.09R, n=142)

### donchian  🟠 TUNE
- Trades: 756 W=394 L=362 WR=52.1%
- Exp: +0.043R  PF: 1.13  Sharpe: 0.94
- MaxDD(fixed): -16.8%  MaxDD(pct_eq): -19.9%  DDdur: 2d
- Best month: +14.4%  Worst: -12.2%
- Avg hold: 351 min
- Top coins: INJ-USDT (+0.09R, n=239), TIA-USDT (+0.03R, n=236), ARB-USDT (+0.02R, n=281)

### rsi_divergence  🟠 TUNE
- Trades: 646 W=299 L=347 WR=46.3%
- Exp: +0.034R  PF: 1.08  Sharpe: 0.70
- MaxDD(fixed): -19.3%  MaxDD(pct_eq): -18.4%  DDdur: 2d
- Best month: +12.8%  Worst: -7.4%
- Avg hold: 334 min
- Top coins: TAO-USDT (+0.11R, n=142), TIA-USDT (+0.10R, n=69), SUI-USDT (+0.06R, n=103), INJ-USDT (+0.03R, n=121), ARB-USDT (-0.04R, n=104)
- Worst coins: INJ-USDT (+0.03R, n=121), ARB-USDT (-0.04R, n=104), OP-USDT (-0.06R, n=107)

### candlestick  🔴 KILL
- Trades: 826 W=348 L=478 WR=42.1%
- Exp: -0.065R  PF: 0.86  Sharpe: -1.26
- MaxDD(fixed): -68.1%  MaxDD(pct_eq): -53.6%  DDdur: 0d
- Best month: +9.8%  Worst: -18.2%
- Avg hold: 321 min
- Top coins: OP-USDT (+0.04R, n=140), TIA-USDT (+0.02R, n=169), SUI-USDT (-0.04R, n=133), TAO-USDT (-0.09R, n=141), ARB-USDT (-0.11R, n=120)
- Worst coins: TAO-USDT (-0.09R, n=141), ARB-USDT (-0.11R, n=120), INJ-USDT (-0.25R, n=123)

### momentum  🔴 KILL
- Trades: 9683 W=4231 L=5452 WR=43.7%
- Exp: -0.085R  PF: 0.81  Sharpe: -4.13
- MaxDD(fixed): -748.7%  MaxDD(pct_eq): -95.4%  DDdur: 4d
- Best month: +6.4%  Worst: -131.6%
- Avg hold: 109 min
- Top coins: INJ-USDT (-0.04R, n=1561), TAO-USDT (-0.08R, n=1699), OP-USDT (-0.08R, n=1590), ARB-USDT (-0.08R, n=1571), SUI-USDT (-0.10R, n=1495)
- Worst coins: ARB-USDT (-0.08R, n=1571), SUI-USDT (-0.10R, n=1495), TIA-USDT (-0.11R, n=1767)

### scalp  🔴 KILL
- Trades: 32 W=16 L=16 WR=50.0%
- Exp: -0.089R  PF: 0.84  Sharpe: -1.49
- MaxDD(fixed): -8.6%  MaxDD(pct_eq): -8.9%  DDdur: 0d
- Best month: +2.2%  Worst: -2.0%
- Avg hold: 7 min
- Top coins: ARB-USDT (+0.56R, n=3), TIA-USDT (+0.37R, n=3), SUI-USDT (+0.20R, n=5), INJ-USDT (+0.18R, n=8), TAO-USDT (-0.56R, n=6)
- Worst coins: INJ-USDT (+0.18R, n=8), TAO-USDT (-0.56R, n=6), OP-USDT (-0.68R, n=7)

### ema_ribbon  🔴 KILL
- Trades: 6689 W=2917 L=3772 WR=43.6%
- Exp: -0.095R  PF: 0.79  Sharpe: -4.29
- MaxDD(fixed): -527.8%  MaxDD(pct_eq): -96.0%  DDdur: 3d
- Best month: +8.4%  Worst: -79.8%
- Avg hold: 99 min
- Top coins: SUI-USDT (-0.07R, n=1010), TAO-USDT (-0.07R, n=1243), OP-USDT (-0.09R, n=1065), INJ-USDT (-0.10R, n=1033), ARB-USDT (-0.12R, n=1057)
- Worst coins: INJ-USDT (-0.10R, n=1033), ARB-USDT (-0.12R, n=1057), TIA-USDT (-0.12R, n=1281)

### meanrev  🔴 KILL
- Trades: 38 W=16 L=22 WR=42.1%
- Exp: -0.123R  PF: 0.75  Sharpe: -1.88
- MaxDD(fixed): -10.2%  MaxDD(pct_eq): -9.8%  DDdur: 0d
- Best month: +3.2%  Worst: -8.2%
- Avg hold: 28 min
- Top coins: TIA-USDT (+0.22R, n=5), SUI-USDT (+0.14R, n=3), INJ-USDT (+0.12R, n=7), OP-USDT (-0.12R, n=7), TAO-USDT (-0.17R, n=7)
- Worst coins: OP-USDT (-0.12R, n=7), TAO-USDT (-0.17R, n=7), ARB-USDT (-0.55R, n=9)

### bb_squeeze  🔴 KILL
- Trades: 1508 W=622 L=886 WR=41.2%
- Exp: -0.135R  PF: 0.72  Sharpe: -4.09
- MaxDD(fixed): -204.0%  MaxDD(pct_eq): -90.4%  DDdur: 0d
- Best month: +7.4%  Worst: -33.4%
- Avg hold: 131 min
- Top coins: ARB-USDT (-0.10R, n=210), SUI-USDT (-0.11R, n=312), TAO-USDT (-0.12R, n=307), OP-USDT (-0.12R, n=216), INJ-USDT (-0.16R, n=264)
- Worst coins: OP-USDT (-0.12R, n=216), INJ-USDT (-0.16R, n=264), TIA-USDT (-0.20R, n=199)

### asymmetric  🔴 KILL
- Trades: 595 W=236 L=359 WR=39.7%
- Exp: -0.184R  PF: 0.72  Sharpe: -3.06
- MaxDD(fixed): -108.5%  MaxDD(pct_eq): -70.8%  DDdur: 0d
- Best month: +7.0%  Worst: -22.3%
- Avg hold: 166 min
- Top coins: TAO-USDT (-0.11R, n=120), ARB-USDT (-0.15R, n=84), TIA-USDT (-0.16R, n=82), SUI-USDT (-0.16R, n=88), OP-USDT (-0.23R, n=112)
- Worst coins: SUI-USDT (-0.16R, n=88), OP-USDT (-0.23R, n=112), INJ-USDT (-0.27R, n=109)

### swing  🔴 KILL
- Trades: 62 W=19 L=43 WR=30.6%
- Exp: -0.423R  PF: 0.36  Sharpe: -9.63
- MaxDD(fixed): -28.9%  MaxDD(pct_eq): -25.8%  DDdur: 0d
- Best month: +2.2%  Worst: -5.3%
- Avg hold: 197 min
- Top coins: INJ-USDT (-0.14R, n=7), SUI-USDT (-0.26R, n=17), ARB-USDT (-0.47R, n=16), TIA-USDT (-0.51R, n=10), OP-USDT (-0.63R, n=8)
- Worst coins: TIA-USDT (-0.51R, n=10), OP-USDT (-0.63R, n=8), TAO-USDT (-0.81R, n=4)

### volume_capitulation  🔴 KILL
- Trades: 7 W=0 L=7 WR=0.0%
- Exp: -0.935R  PF: 0.00  Sharpe: -49.60
- MaxDD(fixed): -6.5%  MaxDD(pct_eq): -6.4%  DDdur: 0d
- Best month: -1.1%  Worst: -2.2%
- Avg hold: 6 min
- Top coins: TAO-USDT (-0.57R, n=2), SUI-USDT (-1.08R, n=1), INJ-USDT (-1.08R, n=3), TIA-USDT (-1.08R, n=1)



## Nightly run — 2026-05-17 03:34

Thresholds: Sharpe ≥ 2.0, ExpR ≥ 0.10R, MaxDD ≤ 25%, Trades ≥ 100

Backtest run as 3× ~7-symbol chunks (sandbox 45s bash cap won't fit single 20-symbol pass). Per-agent metrics merged via trade-weighted averages for ExpR/Sharpe/WR/PF and worst-case MaxDD across batches. Source batches stored in /tmp/report_batch_{majors,alts1,alts2}.md.

### Merged leaderboard (sorted by Sharpe)

| AGENT | TRADES | WIN% | EXP_R | DD(eq) | PF | SHARPE | STATUS |
|-------|-------:|-----:|------:|-------:|---:|-------:|--------|
| asian_pump | 49 | 85.7% | +0.392 | -0.3% | 107.33 | 21.06 | LIVE (n<100, keep) |
| daily_breakout_2h | 13146 | 73.7% | +0.560 | -13.7% | 3.89 | 14.70 | PAPER → deploy |
| daily_breakout_8h | 3129 | 76.3% | +0.449 | -7.3% | 3.73 | 9.88 | PAPER → deploy |
| macd_cross | 2826 | 74.0% | +0.221 | -7.3% | 2.19 | 7.21 | LIVE keep |
| daily_breakout_4h | 11096 | 76.4% | +0.673 | -12.4% | 4.74 | 6.53 | PAPER → deploy |
| daily_breakout_12h | 6555 | 78.5% | +0.497 | -13.6% | 4.31 | 6.05 | PAPER → deploy |
| daily_breakout_24h | 4048 | 81.2% | +0.520 | -8.1% | 4.79 | 4.34 | PAPER → deploy |
| trend_pullback | 2508 | ~70% | +0.193 | -11.6% | ~1.7 | 4.19 | LIVE keep |
| daily_breakout_48h | 1498 | 79.0% | +0.400 | -11.7% | 3.67 | 3.89 | PAPER → deploy |
| daily_breakout | 1169 | 83.7% | +0.595 | -7.0% | 5.78 | 3.30 | LIVE keep |
| donchian | 2154 | ~50% | +0.045 | -19.9% | 1.13 | 0.91 | PAPER tune |
| rsi_divergence | 1862 | ~47% | +0.034 | -18.4% | 1.08 | 0.70 | PAPER tune |
| candlestick | 2082 | 40.2% | -0.090 | -60.7% | 0.82 | -1.65 | PAPER broken |
| meanrev | 75 | 46.6% | -0.099 | -9.8% | 0.78 | -1.91 | PAPER broken |
| bb_squeeze | 5060 | 42.8% | -0.105 | -90.4% | 0.77 | -3.23 | PAPER broken |
| asymmetric | 1891 | 41.2% | -0.187 | -77.1% | 0.71 | -3.36 | PAPER broken |
| ema_ribbon | 18134 | 43.7% | -0.080 | -96.0% | 0.82 | -3.43 | PAPER broken |
| momentum | 28157 | 43.1% | -0.084 | -95.4% | 0.81 | -3.90 | PAPER broken |
| scalp | 79 | 39.2% | -0.302 | -17.0% | 0.54 | -4.91 | PAPER broken |
| swing | 253 | 32.8% | -0.294 | -34.4% | 0.50 | -5.52 | PAPER broken |
| volume_capitulation | 25 | 0.0% | -0.999 | -10.4% | 0.00 | -34.49 | **LIVE — UNDEPLOY** |
| funding, daily_breakout_4h_trend, daily_breakout_7d, pump_dump_reversal, supertrend | 0 | — | — | — | — | — | 0 trades (not coverable by backtest) |

**LIVE agents not in any batch** (deployed but unbacktested — must fix `backtest.py:AGENT_NAMES`): daily_breakout_7d, supertrend, pump_dump_reversal, bb_bounce, zscore_reversion, stoch_rsi, golden_cross, liquidity_sweep, connors_rsi2, raschke_retest, wide_scalp, wide_candle, hurst_regime, kalman_trend, smart_scalp, volume_profile, fibonacci, williams_r, funding_extremes.

See `HUNTER_BRIEF.md` for deploy/undeploy curl commands.


## Nightly run — 2026-05-18 03:10

Thresholds: Sharpe ≥ 2.0, ExpR ≥ 0.10R, MaxDD ≤ 25%, Trades ≥ 100

**FAILED — no leaderboard generated.** `backtest.py` returned rc=1 ("No trades generated at all"). Root cause: BloFin candle endpoint returned 403 Forbidden on every fetch (sandbox proxy block), and the local 365d parquet cache was empty/evicted, so all 20 symbols skipped with "only 0 15m bars". `blofin` and `fastparquet` were re-installed mid-run (python env had reset) but that didn't help — the bottleneck is network access. No new strategies promoted in parametric pool (parametric step skipped since main backtest failed).

Carrying forward the 2026-05-17 leaderboard. See `HUNTER_BRIEF.md` (2026-05-18 section) for the unchanged deploy/undeploy queue.
