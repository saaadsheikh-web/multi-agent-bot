# Trading Mathematics — Reference

## RSI = 100 - 100/(1 + RS)
- RS = avg_gain(14) / avg_loss(14)
- 0-30 oversold, 70-100 overbought
- Wilder's smoothing: subsequent RS uses prior avg_gain × 13 + current_gain / 14

## MACD = EMA(fast) - EMA(slow)
- Crypto-optimized: 24/52/18 (standard 12/26/9 too slow)
- Signal line = EMA(MACD, 18)
- Histogram = MACD - Signal

## Bollinger Bands
- Middle = SMA(20)
- Upper = Middle + 2×σ, Lower = Middle - 2×σ
- σ = sqrt(Σ(close - SMA)² / 20)

## ATR (Average True Range)
- TR = max(high-low, |high-prev_close|, |low-prev_close|)
- ATR = Wilder's smooth(TR, 14)
- SL = entry ± 2×ATR (wider for crypto)

## Fibonacci Levels
- 0.618 = 1/φ (φ = golden ratio = 1.618)
- 0.382 = 1 - 0.618
- 0.236 = 0.382 × 0.618
- Self-fulfilling prophecy: wide usage creates support/resistance

## Kelly Criterion: f* = (bp - q)/b
- f* = optimal fraction of capital
- b = net odds (reward:risk ratio)
- p = win probability, q = loss probability
- Use HALF or QUARTER Kelly to reduce drawdowns
