# BACKTEST REPORT
Generated: 2026-06-03T00:33:40.582587+00:00

## Verdict Table
| AGENT | TRADES | WIN% | AVG_R | EXP_R | DD(fixed) | DD(pct_eq) | PF | SHARPE | VERDICT |
|-------|--------|------|-------|-------|-----------|------------|-----|--------|---------|
| daily_breakout_4h | 10058 | 74.5% | +0.622 | +0.622 | -5.7% | -23.2% | 4.14 | 5.45 | 🟢 KEEP & SCALE |
| daily_breakout | 1149 | 81.4% | +0.568 | +0.568 | -6.4% | -13.3% | 4.76 | 2.39 | 🟢 KEEP & SCALE |
| daily_breakout_2h | 10105 | 72.0% | +0.510 | +0.510 | -9.1% | -23.5% | 3.41 | 14.16 | 🟢 KEEP & SCALE |
| daily_breakout_24h | 3841 | 79.7% | +0.493 | +0.493 | -7.1% | -19.6% | 4.23 | 3.53 | 🟢 KEEP & SCALE |
| daily_breakout_12h | 5162 | 75.4% | +0.443 | +0.443 | -5.7% | -28.3% | 3.49 | 4.28 | 🟢 KEEP & SCALE |
| daily_breakout_8h | 1684 | 74.0% | +0.377 | +0.377 | -4.7% | -13.7% | 2.97 | 8.34 | 🟢 KEEP & SCALE |
| daily_breakout_48h | 940 | 70.7% | +0.356 | +0.356 | -11.9% | -28.9% | 2.44 | 2.62 | 🟢 KEEP & SCALE |
| asian_pump | 52 | 84.6% | +0.353 | +0.353 | -0.9% | -1.1% | 13.18 | 19.37 | 🟢 KEEP & SCALE |
| stoch_rsi | 5475 | 56.1% | +0.265 | +0.265 | -31.2% | -38.3% | 1.85 | 5.38 | 🟡 KEEP |
| trend_pullback | 2435 | 70.3% | +0.192 | +0.192 | -23.0% | -20.9% | 1.75 | 4.56 | 🟡 KEEP |
| macd_cross | 2356 | 73.1% | +0.191 | +0.191 | -6.3% | -11.9% | 2.01 | 7.20 | 🟡 KEEP |
| fibonacci | 2582 | 44.7% | +0.185 | +0.185 | -75.8% | -75.1% | 1.50 | 1.20 | 🟠 TUNE |
| donchian | 2140 | 50.9% | +0.071 | +0.071 | -21.8% | -36.9% | 1.20 | 1.37 | 🟠 TUNE |
| rsi_divergence | 1743 | 46.4% | +0.015 | +0.015 | -46.0% | -40.8% | 1.04 | 0.34 | 🟠 TUNE |
| funding_extremes | 6347 | 50.3% | -0.002 | -0.002 | -167.4% | -89.0% | 0.99 | -0.06 | 🔴 KILL |
| viki | 2410 | 64.7% | -0.028 | -0.028 | -71.7% | -57.8% | 0.91 | -1.22 | 🔴 KILL |
| hurst_regime | 547 | 48.6% | -0.035 | -0.035 | -37.5% | -39.8% | 0.92 | -0.65 | 🔴 KILL |
| ema_ribbon | 17436 | 43.6% | -0.082 | -0.082 | -1095.4% | -96.3% | 0.81 | -3.96 | 🔴 KILL |
| momentum | 27416 | 43.0% | -0.086 | -0.086 | -2207.3% | -95.4% | 0.80 | -4.56 | 🔴 KILL |
| golden_hour | 596 | 42.4% | -0.089 | -0.089 | -77.0% | -55.1% | 0.81 | -0.76 | 🔴 KILL |
| bb_squeeze | 4603 | 43.3% | -0.096 | -0.096 | -420.1% | -95.3% | 0.78 | -3.95 | 🔴 KILL |
| candlestick | 1885 | 39.9% | -0.098 | -0.098 | -203.4% | -89.9% | 0.80 | -2.05 | 🔴 KILL |
| meanrev | 76 | 46.1% | -0.114 | -0.114 | -16.1% | -15.0% | 0.76 | -1.67 | 🔴 KILL |
| asymmetric | 1757 | 41.0% | -0.186 | -0.186 | -317.2% | -95.2% | 0.71 | -3.91 | 🔴 KILL |
| zscore_reversion | 15840 | 44.2% | -0.226 | -0.226 | -3549.1% | -95.0% | 0.64 | -7.47 | 🔴 KILL |
| scalp | 74 | 41.9% | -0.233 | -0.233 | -22.9% | -22.1% | 0.60 | -3.35 | 🔴 KILL |
| swing | 249 | 32.5% | -0.295 | -0.295 | -77.0% | -59.4% | 0.49 | -5.18 | 🔴 KILL |
| bb_bounce | 8259 | 43.7% | -0.396 | -0.396 | -3273.4% | -95.0% | 0.50 | -2.31 | 🔴 KILL |
| volume_capitulation | 24 | 0.0% | -0.953 | -0.953 | -22.9% | -20.5% | 0.00 | -15.09 | 🔴 KILL |
| connors_rsi2 | 52075 | 33.7% | -1.119 | -1.119 | -53755.5% | -95.4% | 0.38 | -5.35 | 🔴 KILL |
| funding | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| daily_breakout_4h_trend | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| daily_breakout_7d | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| pump_dump_reversal | 0 | — | — | — | — | — | — | — | 🔴 KILL |
| supertrend | 0 | — | — | — | — | — | — | — | 🔴 KILL |

## Auto-prune Actions
(none)

## Per-Agent Detail
### daily_breakout_4h  🟢 KEEP & SCALE
- Trades: 10058 W=7497 L=2561 WR=74.5%
- Exp: +0.622R  PF: 4.14  Sharpe: 5.45
- MaxDD(fixed): -5.7%  MaxDD(pct_eq): -23.2%  DDdur: 1d
- Best month: +1298.2%  Worst: +0.3%
- Avg hold: 79 min
- Top coins: ARB-USDT (+0.80R, n=500), OP-USDT (+0.78R, n=524), TIA-USDT (+0.77R, n=548), DOT-USDT (+0.74R, n=475), NEAR-USDT (+0.72R, n=521)
- Worst coins: ETH-USDT (+0.43R, n=504), BNB-USDT (+0.37R, n=323), BTC-USDT (+0.25R, n=326)

### daily_breakout  🟢 KEEP & SCALE
- Trades: 1149 W=935 L=214 WR=81.4%
- Exp: +0.568R  PF: 4.76  Sharpe: 2.39
- MaxDD(fixed): -6.4%  MaxDD(pct_eq): -13.3%  DDdur: 0d
- Best month: +299.1%  Worst: -1.7%
- Avg hold: 603 min
- Top coins: APT-USDT (+0.83R, n=52), TAO-USDT (+0.81R, n=59), INJ-USDT (+0.72R, n=61), TIA-USDT (+0.70R, n=58), DOT-USDT (+0.69R, n=65)
- Worst coins: ETH-USDT (+0.32R, n=66), BNB-USDT (+0.32R, n=46), BTC-USDT (+0.06R, n=40)

### daily_breakout_2h  🟢 KEEP & SCALE
- Trades: 10105 W=7276 L=2829 WR=72.0%
- Exp: +0.510R  PF: 3.41  Sharpe: 14.16
- MaxDD(fixed): -9.1%  MaxDD(pct_eq): -23.5%  DDdur: 1d
- Best month: +588.4%  Worst: +99.1%
- Avg hold: 33 min
- Top coins: TAO-USDT (+0.66R, n=740), ARB-USDT (+0.65R, n=451), INJ-USDT (+0.62R, n=590), SUI-USDT (+0.59R, n=603), NEAR-USDT (+0.56R, n=544)
- Worst coins: LTC-USDT (+0.39R, n=470), BNB-USDT (+0.27R, n=307), BTC-USDT (+0.24R, n=255)

### daily_breakout_24h  🟢 KEEP & SCALE
- Trades: 3841 W=3060 L=781 WR=79.7%
- Exp: +0.493R  PF: 4.23  Sharpe: 3.53
- MaxDD(fixed): -7.1%  MaxDD(pct_eq): -19.6%  DDdur: 0d
- Best month: +518.0%  Worst: -0.3%
- Avg hold: 219 min
- Top coins: TIA-USDT (+0.73R, n=195), ARB-USDT (+0.67R, n=215), DOT-USDT (+0.59R, n=197), DOGE-USDT (+0.57R, n=208), OP-USDT (+0.57R, n=182)
- Worst coins: SOL-USDT (+0.37R, n=207), BNB-USDT (+0.29R, n=134), BTC-USDT (+0.14R, n=161)

### daily_breakout_12h  🟢 KEEP & SCALE
- Trades: 5162 W=3894 L=1268 WR=75.4%
- Exp: +0.443R  PF: 3.49  Sharpe: 4.28
- MaxDD(fixed): -5.7%  MaxDD(pct_eq): -28.3%  DDdur: 1d
- Best month: +525.6%  Worst: +10.5%
- Avg hold: 113 min
- Top coins: DOT-USDT (+0.67R, n=221), APT-USDT (+0.60R, n=291), ADA-USDT (+0.53R, n=262), ATOM-USDT (+0.52R, n=203), ARB-USDT (+0.52R, n=267)
- Worst coins: ETH-USDT (+0.30R, n=228), BNB-USDT (+0.20R, n=151), BTC-USDT (+0.17R, n=140)

### daily_breakout_8h  🟢 KEEP & SCALE
- Trades: 1684 W=1246 L=438 WR=74.0%
- Exp: +0.377R  PF: 2.97  Sharpe: 8.34
- MaxDD(fixed): -4.7%  MaxDD(pct_eq): -13.7%  DDdur: 1d
- Best month: +79.0%  Worst: +13.9%
- Avg hold: 76 min
- Top coins: ARB-USDT (+0.69R, n=84), DOT-USDT (+0.53R, n=68), INJ-USDT (+0.51R, n=110), TAO-USDT (+0.41R, n=150), TIA-USDT (+0.41R, n=110)
- Worst coins: LINK-USDT (+0.23R, n=72), BNB-USDT (+0.20R, n=32), BTC-USDT (+0.18R, n=19)

### daily_breakout_48h  🟢 KEEP & SCALE
- Trades: 940 W=665 L=275 WR=70.7%
- Exp: +0.356R  PF: 2.44  Sharpe: 2.62
- MaxDD(fixed): -11.9%  MaxDD(pct_eq): -28.9%  DDdur: 0d
- Best month: +123.9%  Worst: -0.8%
- Avg hold: 378 min
- Top coins: ARB-USDT (+1.02R, n=35), ADA-USDT (+0.93R, n=31), ATOM-USDT (+0.72R, n=41), OP-USDT (+0.52R, n=73), DOT-USDT (+0.44R, n=41)
- Worst coins: BNB-USDT (+0.14R, n=34), AVAX-USDT (+0.13R, n=31), BTC-USDT (+0.06R, n=29)

### asian_pump  🟢 KEEP & SCALE
- Trades: 52 W=44 L=8 WR=84.6%
- Exp: +0.353R  PF: 13.18  Sharpe: 19.37
- MaxDD(fixed): -0.9%  MaxDD(pct_eq): -1.1%  DDdur: 0d
- Best month: +2.8%  Worst: +0.4%
- Avg hold: 114 min
- Top coins: ARB-USDT (+0.61R, n=7), TAO-USDT (+0.61R, n=5), SOL-USDT (+0.50R, n=1), DOT-USDT (+0.48R, n=5), SUI-USDT (+0.40R, n=2)
- Worst coins: BTC-USDT (+0.03R, n=1), ETH-USDT (-0.05R, n=1), INJ-USDT (-0.40R, n=2)

### stoch_rsi  🟡 KEEP
- Trades: 5475 W=3073 L=2402 WR=56.1%
- Exp: +0.265R  PF: 1.85  Sharpe: 5.38
- MaxDD(fixed): -31.2%  MaxDD(pct_eq): -38.3%  DDdur: 3d
- Best month: +273.3%  Worst: -0.0%
- Avg hold: 286 min
- Top coins: TIA-USDT (+0.59R, n=334), ARB-USDT (+0.56R, n=288), DOGE-USDT (+0.42R, n=287), TAO-USDT (+0.41R, n=317), OP-USDT (+0.39R, n=312)
- Worst coins: LINK-USDT (+0.10R, n=263), BTC-USDT (+0.07R, n=185), BNB-USDT (+0.02R, n=203)

### trend_pullback  🟡 KEEP
- Trades: 2435 W=1711 L=724 WR=70.3%
- Exp: +0.192R  PF: 1.75  Sharpe: 4.56
- MaxDD(fixed): -23.0%  MaxDD(pct_eq): -20.9%  DDdur: 2d
- Best month: +72.3%  Worst: -12.2%
- Avg hold: 732 min
- Top coins: AVAX-USDT (+0.32R, n=112), SUI-USDT (+0.32R, n=135), ATOM-USDT (+0.29R, n=137), ADA-USDT (+0.28R, n=109), NEAR-USDT (+0.27R, n=116)
- Worst coins: APT-USDT (+0.11R, n=119), INJ-USDT (+0.10R, n=119), ETH-USDT (+0.01R, n=125)

### macd_cross  🟡 KEEP
- Trades: 2356 W=1723 L=633 WR=73.1%
- Exp: +0.191R  PF: 2.01  Sharpe: 7.20
- MaxDD(fixed): -6.3%  MaxDD(pct_eq): -11.9%  DDdur: 1d
- Best month: +55.1%  Worst: +14.4%
- Avg hold: 129 min
- Top coins: ADA-USDT (+0.29R, n=110), TAO-USDT (+0.25R, n=124), AVAX-USDT (+0.24R, n=116), APT-USDT (+0.23R, n=122), XRP-USDT (+0.23R, n=122)
- Worst coins: NEAR-USDT (+0.14R, n=108), ETH-USDT (+0.14R, n=136), TIA-USDT (+0.09R, n=123)

### fibonacci  🟠 TUNE
- Trades: 2582 W=1153 L=1429 WR=44.7%
- Exp: +0.185R  PF: 1.50  Sharpe: 1.20
- MaxDD(fixed): -75.8%  MaxDD(pct_eq): -75.1%  DDdur: 9d
- Best month: +433.8%  Worst: -57.3%
- Avg hold: 591 min
- Top coins: TIA-USDT (+1.37R, n=129), DOT-USDT (+1.10R, n=126), SUI-USDT (+0.78R, n=121), XRP-USDT (+0.24R, n=142), BNB-USDT (+0.22R, n=163)
- Worst coins: SOL-USDT (-0.10R, n=126), OP-USDT (-0.15R, n=112), AVAX-USDT (-0.17R, n=108)

### donchian  🟠 TUNE
- Trades: 2140 W=1089 L=1051 WR=50.9%
- Exp: +0.071R  PF: 1.20  Sharpe: 1.37
- MaxDD(fixed): -21.8%  MaxDD(pct_eq): -36.9%  DDdur: 8d
- Best month: +58.0%  Worst: -37.1%
- Avg hold: 411 min
- Top coins: ETH-USDT (+0.13R, n=231), AVAX-USDT (+0.12R, n=223), DOT-USDT (+0.10R, n=230), INJ-USDT (+0.06R, n=233), NEAR-USDT (+0.06R, n=241)
- Worst coins: TIA-USDT (+0.05R, n=239), LINK-USDT (+0.04R, n=231), ADA-USDT (+0.03R, n=229)

### rsi_divergence  🟠 TUNE
- Trades: 1743 W=809 L=934 WR=46.4%
- Exp: +0.015R  PF: 1.04  Sharpe: 0.34
- MaxDD(fixed): -46.0%  MaxDD(pct_eq): -40.8%  DDdur: 13d
- Best month: +25.1%  Worst: -13.3%
- Avg hold: 468 min
- Top coins: BNB-USDT (+0.30R, n=58), LINK-USDT (+0.27R, n=97), DOT-USDT (+0.23R, n=73), XRP-USDT (+0.16R, n=53), TAO-USDT (+0.11R, n=141)
- Worst coins: AVAX-USDT (-0.13R, n=73), DOGE-USDT (-0.19R, n=101), ADA-USDT (-0.24R, n=79)

### funding_extremes  🔴 KILL
- Trades: 6347 W=3193 L=3154 WR=50.3%
- Exp: -0.002R  PF: 0.99  Sharpe: -0.06
- MaxDD(fixed): -167.4%  MaxDD(pct_eq): -89.0%  DDdur: 49d
- Best month: +133.8%  Worst: -73.2%
- Avg hold: 382 min
- Top coins: DOT-USDT (+0.06R, n=278), ATOM-USDT (+0.03R, n=297), TIA-USDT (+0.03R, n=330), SOL-USDT (+0.03R, n=333), ARB-USDT (+0.02R, n=315)
- Worst coins: LINK-USDT (-0.05R, n=311), XRP-USDT (-0.06R, n=319), APT-USDT (-0.07R, n=317)

### viki  🔴 KILL
- Trades: 2410 W=1560 L=850 WR=64.7%
- Exp: -0.028R  PF: 0.91  Sharpe: -1.22
- MaxDD(fixed): -71.7%  MaxDD(pct_eq): -57.8%  DDdur: 0d
- Best month: +4.5%  Worst: -20.9%
- Avg hold: 2029 min
- Top coins: NEAR-USDT (+0.04R, n=138), OP-USDT (+0.03R, n=121), ETH-USDT (+0.02R, n=115), DOT-USDT (+0.02R, n=116), APT-USDT (+0.02R, n=123)
- Worst coins: XRP-USDT (-0.09R, n=110), BNB-USDT (-0.12R, n=79), ATOM-USDT (-0.13R, n=93)

### hurst_regime  🔴 KILL
- Trades: 547 W=266 L=281 WR=48.6%
- Exp: -0.035R  PF: 0.92  Sharpe: -0.65
- MaxDD(fixed): -37.5%  MaxDD(pct_eq): -39.8%  DDdur: 1d
- Best month: +24.3%  Worst: -15.9%
- Avg hold: 76 min
- Top coins: ARB-USDT (+0.48R, n=16), ATOM-USDT (+0.47R, n=16), APT-USDT (+0.40R, n=22), LTC-USDT (+0.14R, n=23), ADA-USDT (+0.12R, n=37)
- Worst coins: SOL-USDT (-0.28R, n=28), TIA-USDT (-0.28R, n=22), TAO-USDT (-0.32R, n=30)

### ema_ribbon  🔴 KILL
- Trades: 17436 W=7609 L=9827 WR=43.6%
- Exp: -0.082R  PF: 0.81  Sharpe: -3.96
- MaxDD(fixed): -1095.4%  MaxDD(pct_eq): -96.3%  DDdur: 7d
- Best month: +1.6%  Worst: -230.4%
- Avg hold: 133 min
- Top coins: SOL-USDT (+0.00R, n=809), BNB-USDT (-0.03R, n=580), XRP-USDT (-0.04R, n=775), AVAX-USDT (-0.05R, n=824), ADA-USDT (-0.06R, n=338)
- Worst coins: TIA-USDT (-0.12R, n=1261), BTC-USDT (-0.12R, n=528), LTC-USDT (-0.16R, n=729)

### momentum  🔴 KILL
- Trades: 27416 W=11795 L=15621 WR=43.0%
- Exp: -0.086R  PF: 0.80  Sharpe: -4.56
- MaxDD(fixed): -2207.3%  MaxDD(pct_eq): -95.4%  DDdur: 0d
- Best month: +1.0%  Worst: -292.2%
- Avg hold: 147 min
- Top coins: DOGE-USDT (-0.03R, n=1346), SOL-USDT (-0.04R, n=1258), XRP-USDT (-0.05R, n=1181), AVAX-USDT (-0.05R, n=1339), INJ-USDT (-0.06R, n=1541)
- Worst coins: TIA-USDT (-0.12R, n=1751), BTC-USDT (-0.12R, n=908), LTC-USDT (-0.13R, n=1228)

### golden_hour  🔴 KILL
- Trades: 596 W=253 L=343 WR=42.4%
- Exp: -0.089R  PF: 0.81  Sharpe: -0.76
- MaxDD(fixed): -77.0%  MaxDD(pct_eq): -55.1%  DDdur: 1d
- Best month: +38.5%  Worst: -22.6%
- Avg hold: 195 min
- Top coins: TAO-USDT (+2.33R, n=35), ADA-USDT (+0.34R, n=26), TIA-USDT (-0.04R, n=31), SUI-USDT (-0.11R, n=34), OP-USDT (-0.14R, n=35)
- Worst coins: AVAX-USDT (-0.36R, n=29), ARB-USDT (-0.43R, n=30), NEAR-USDT (-0.49R, n=26)

### bb_squeeze  🔴 KILL
- Trades: 4603 W=1994 L=2609 WR=43.3%
- Exp: -0.096R  PF: 0.78  Sharpe: -3.95
- MaxDD(fixed): -420.1%  MaxDD(pct_eq): -95.3%  DDdur: 0d
- Best month: +9.7%  Worst: -78.0%
- Avg hold: 178 min
- Top coins: DOGE-USDT (+0.02R, n=224), ADA-USDT (+0.00R, n=92), ETH-USDT (-0.00R, n=304), SOL-USDT (-0.03R, n=280), APT-USDT (-0.04R, n=227)
- Worst coins: NEAR-USDT (-0.16R, n=228), BTC-USDT (-0.17R, n=218), TIA-USDT (-0.18R, n=187)

### candlestick  🔴 KILL
- Trades: 1885 W=752 L=1133 WR=39.9%
- Exp: -0.098R  PF: 0.80  Sharpe: -2.05
- MaxDD(fixed): -203.4%  MaxDD(pct_eq): -89.9%  DDdur: 0d
- Best month: +23.0%  Worst: -56.0%
- Avg hold: 375 min
- Top coins: BTC-USDT (+0.28R, n=17), LTC-USDT (+0.14R, n=57), OP-USDT (+0.03R, n=136), TIA-USDT (+0.01R, n=159), BNB-USDT (-0.02R, n=35)
- Worst coins: INJ-USDT (-0.28R, n=113), DOGE-USDT (-0.31R, n=87), XRP-USDT (-0.31R, n=76)

### meanrev  🔴 KILL
- Trades: 76 W=35 L=41 WR=46.1%
- Exp: -0.114R  PF: 0.76  Sharpe: -1.67
- MaxDD(fixed): -16.1%  MaxDD(pct_eq): -15.0%  DDdur: 0d
- Best month: +5.1%  Worst: -16.0%
- Avg hold: 30 min
- Top coins: LTC-USDT (+0.75R, n=3), ATOM-USDT (+0.42R, n=3), BNB-USDT (+0.36R, n=1), AVAX-USDT (+0.28R, n=4), BTC-USDT (+0.23R, n=1)
- Worst coins: SOL-USDT (-1.12R, n=2), ADA-USDT (-1.12R, n=1), DOT-USDT (-1.12R, n=1)

### asymmetric  🔴 KILL
- Trades: 1757 W=721 L=1036 WR=41.0%
- Exp: -0.186R  PF: 0.71  Sharpe: -3.91
- MaxDD(fixed): -317.2%  MaxDD(pct_eq): -95.2%  DDdur: 0d
- Best month: -0.0%  Worst: -67.9%
- Avg hold: 192 min
- Top coins: DOT-USDT (+0.01R, n=107), SOL-USDT (-0.03R, n=88), ATOM-USDT (-0.09R, n=88), LINK-USDT (-0.09R, n=90), TAO-USDT (-0.09R, n=114)
- Worst coins: ADA-USDT (-0.32R, n=89), DOGE-USDT (-0.33R, n=66), BTC-USDT (-0.36R, n=83)

### zscore_reversion  🔴 KILL
- Trades: 15840 W=6996 L=8844 WR=44.2%
- Exp: -0.226R  PF: 0.64  Sharpe: -7.47
- MaxDD(fixed): -3549.1%  MaxDD(pct_eq): -95.0%  DDdur: 0d
- Best month: +0.3%  Worst: -477.4%
- Avg hold: 76 min
- Top coins: SOL-USDT (-0.09R, n=804), DOT-USDT (-0.11R, n=814), BNB-USDT (-0.16R, n=639), TIA-USDT (-0.16R, n=934), LTC-USDT (-0.18R, n=724)
- Worst coins: ETH-USDT (-0.31R, n=738), ARB-USDT (-0.31R, n=900), TAO-USDT (-0.44R, n=944)

### scalp  🔴 KILL
- Trades: 74 W=31 L=43 WR=41.9%
- Exp: -0.233R  PF: 0.60  Sharpe: -3.35
- MaxDD(fixed): -22.9%  MaxDD(pct_eq): -22.1%  DDdur: 0d
- Best month: +3.3%  Worst: -7.3%
- Avg hold: 11 min
- Top coins: SUI-USDT (+0.57R, n=4), ARB-USDT (+0.56R, n=3), TIA-USDT (+0.37R, n=3), LINK-USDT (+0.24R, n=3), INJ-USDT (+0.18R, n=8)
- Worst coins: OP-USDT (-0.68R, n=7), DOGE-USDT (-1.30R, n=3), ADA-USDT (-1.30R, n=2)

### swing  🔴 KILL
- Trades: 249 W=81 L=168 WR=32.5%
- Exp: -0.295R  PF: 0.49  Sharpe: -5.18
- MaxDD(fixed): -77.0%  MaxDD(pct_eq): -59.4%  DDdur: 0d
- Best month: +6.2%  Worst: -13.0%
- Avg hold: 463 min
- Top coins: DOT-USDT (+0.24R, n=5), LINK-USDT (+0.05R, n=17), ADA-USDT (+0.00R, n=11), XRP-USDT (-0.01R, n=14), LTC-USDT (-0.07R, n=13)
- Worst coins: OP-USDT (-0.63R, n=8), SOL-USDT (-0.80R, n=9), TAO-USDT (-0.81R, n=4)

### bb_bounce  🔴 KILL
- Trades: 8259 W=3612 L=4647 WR=43.7%
- Exp: -0.396R  PF: 0.50  Sharpe: -2.31
- MaxDD(fixed): -3273.4%  MaxDD(pct_eq): -95.0%  DDdur: 0d
- Best month: -4.9%  Worst: -1569.5%
- Avg hold: 103 min
- Top coins: DOT-USDT (-0.10R, n=441), ATOM-USDT (-0.10R, n=429), TAO-USDT (-0.11R, n=552), APT-USDT (-0.12R, n=512), SOL-USDT (-0.12R, n=419)
- Worst coins: ADA-USDT (-0.73R, n=160), AVAX-USDT (-0.78R, n=502), LTC-USDT (-3.18R, n=362)

### volume_capitulation  🔴 KILL
- Trades: 24 W=0 L=24 WR=0.0%
- Exp: -0.953R  PF: 0.00  Sharpe: -15.09
- MaxDD(fixed): -22.9%  MaxDD(pct_eq): -20.5%  DDdur: 0d
- Best month: -1.1%  Worst: -8.7%
- Avg hold: 7 min
- Top coins: TAO-USDT (-0.57R, n=2), DOT-USDT (-0.73R, n=3), LINK-USDT (-0.83R, n=4), SOL-USDT (-1.08R, n=2), XRP-USDT (-1.08R, n=2)
- Worst coins: SUI-USDT (-1.08R, n=1), INJ-USDT (-1.08R, n=3), TIA-USDT (-1.08R, n=1)

### connors_rsi2  🔴 KILL
- Trades: 52075 W=17561 L=34514 WR=33.7%
- Exp: -1.119R  PF: 0.38  Sharpe: -5.35
- MaxDD(fixed): -53755.5%  MaxDD(pct_eq): -95.4%  DDdur: 0d
- Best month: -14.0%  Worst: -10459.6%
- Avg hold: 68 min
- Top coins: TIA-USDT (-0.51R, n=2678), NEAR-USDT (-0.62R, n=3026), LINK-USDT (-0.64R, n=2573), INJ-USDT (-0.66R, n=3101), DOGE-USDT (-0.70R, n=2509)
- Worst coins: BTC-USDT (-2.14R, n=1819), BNB-USDT (-2.73R, n=2645), SOL-USDT (-3.89R, n=2378)

