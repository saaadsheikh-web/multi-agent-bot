#!/usr/bin/env python3
"""Market prediction using advanced math — entropy, DFA, Lyapunov, Bayes, Monte Carlo"""
import os, sys, numpy as np, math, pandas as pd

CACHE = os.path.expanduser('~/multi_agent_bot/backtest_data')
files = sorted(os.listdir(CACHE))
btc_file = [f for f in files if 'BTC' in f and '1H' in f]
if not btc_file:
    btc_file = [f for f in files if 'BTC' in f]
btc_path = os.path.join(CACHE, btc_file[0])
print(f'Data: {btc_path}')
df = pd.read_parquet(btc_path)
c = df['close'].values[-500:].astype(float)
last = c[-1]
print(f'BTC: ${last:.0f} | {len(c)} bars 1H')

# 1. SHANNON ENTROPY
rets = np.diff(np.log(c))
hist, _ = np.histogram(rets, bins=20, range=(-0.05, 0.05))
hist = hist[hist > 0]
p = hist / hist.sum()
entropy = float(-np.sum(p * np.log2(p)))
print(f'Entropy: {entropy:.3f} | {"Predictable" if entropy < 3.5 else "Chaotic"}')

# 2. SPECTRAL ENTROPY (FFT)
x = np.arange(len(c[-200:]))
slope, intercept = np.polyfit(x, c[-200:], 1)
detrended = c[-200:] - (slope * x + intercept)
windowed = detrended * np.hamming(len(detrended))
fft = np.fft.rfft(windowed)
power = np.abs(fft)**2
p_spec = power / power.sum()
p_spec = p_spec[p_spec > 1e-10]
spec_ent = float(-np.sum(p_spec * np.log2(p_spec)) / np.log2(len(p_spec)))
print(f'Spectral Ent: {spec_ent:.3f} | {"Has rhythm" if spec_ent < 0.8 else "Noise"}')

# 3. DFA
y = np.cumsum(c - np.mean(c))
n_values = np.logspace(np.log10(10), np.log10(len(c)//4), 15).astype(int)
n_values = np.unique(n_values)[n_values >= 4]
fluct = []
for n in n_values:
    n_windows = len(y) // n
    if n_windows < 2: continue
    rms = 0.0
    for i in range(n_windows):
        seg = y[i*n:(i+1)*n]
        x_seg = np.arange(len(seg))
        A = np.vstack([x_seg, np.ones_like(x_seg)]).T
        coeffs = np.linalg.lstsq(A, seg, rcond=None)[0]
        trend = A @ coeffs
        detrended = seg - trend
        rms += np.mean(detrended**2)
    rms /= n_windows
    fluct.append(np.sqrt(rms))
log_n = np.log(n_values[:len(fluct)])
log_f = np.log(np.maximum(fluct, 1e-10))
A = np.vstack([log_n, np.ones_like(log_n)]).T
alpha = float(np.linalg.lstsq(A, log_f, rcond=None)[0][0])
regime = "TRENDING" if alpha > 0.6 else ("MEAN-REV" if alpha < 0.4 else "RANGING")
print(f'DFA alpha: {alpha:.3f} | {regime}')

# 4. LYAPUNOV
recent = rets[-50:]
xl = recent[:-1]; yl = recent[1:]
divs = []
for i in range(len(xl)-2):
    dists = np.sqrt((xl - xl[i])**2 + (yl - yl[i])**2)
    dists[i] = np.inf
    mi = np.argmin(dists)
    if mi < len(xl)-1:
        d0 = dists[mi]
        if d0 > 1e-10:
            d1 = np.sqrt((xl[mi+1] - xl[i+1])**2 + (yl[mi+1] if mi+1 < len(yl) else yl[-1] - yl[i+1])**2)
            d1 = max(d1, 1e-10)
            divs.append(np.log(d1/d0))
lyap = float(np.mean(divs)) if len(divs) > 3 else 0.5
print(f'Lyapunov: {lyap:.4f} | {"Orderly" if lyap < 0.15 else "Chaotic"}')

# 5. FISHER
window_f = 30
pn = c[-window_f:] / np.sum(c[-window_f:])
dp = np.diff(pn)
fisher = float(np.sum(dp**2 / pn[1:])) if np.all(pn[1:] > 0) else 0
fh = []
for i in range(window_f, len(c)-1):
    ps = c[i-window_f:i] / np.sum(c[i-window_f:i])
    if np.all(ps[1:] > 0):
        dps = np.diff(ps)
        fh.append(float(np.sum(dps**2 / ps[1:])))
fz = (fisher - np.mean(fh)) / max(np.std(fh), 1e-10) if len(fh) > 5 else 0
print(f'Fisher z: {fz:.2f} | {"New info" if fz > 0 else ("Stale" if fz < -0.5 else "Neutral")}')

# 6. RENYI
rets100 = np.diff(np.log(c[-100:]))
hist2, _ = np.histogram(rets100, bins=20, range=(-0.05, 0.05))
hist2 = hist2[hist2 > 0]
p2 = hist2 / hist2.sum()
h1 = float(-np.sum(p2 * np.log2(p2)))  # Shannon
h2 = float((1.0/(1.0-2.0)) * np.log2(np.sum(p2**2))) if len(p2) > 0 else 0  # Renyi q=2
print(f'Renyi H1-H2: {abs(h1-h2):.3f} | {"Fat tails" if abs(h1-h2) > 0.5 else "Normal"}')

# 7. BAYES
delta = np.diff(c)
gain = np.where(delta > 0, delta, 0)
loss = np.where(delta < 0, -delta, 0)
ag = pd.Series(gain).rolling(14).mean().iloc[-1]
al = pd.Series(loss).rolling(14).mean().iloc[-1]
rsi = 100 - 100/(1+ag/al) if al > 0 else 100
v = df['volume'].values[-200:].astype(float)
vr = v[-1] / max(np.mean(v[-20:]), 1e-10)
ema21 = float(pd.Series(c).ewm(span=21).mean().iloc[-1])
tr = pd.concat([pd.Series(c[-100:] - df['low'].values[-100:]), pd.Series(np.abs(c[-100:] - np.roll(c,1)[-100:])), pd.Series(np.abs(df['high'].values[-100:] - np.roll(c,1)[-100:]))], axis=1).max(axis=1)
atrp = float(tr.ewm(span=14).mean().iloc[-1]) / last * 100
o = 0.55 / 0.45
if 30 <= rsi <= 55: o *= 1.15
elif rsi < 25: o *= 0.85
elif rsi > 70: o *= 0.80
if vr >= 1.5: o *= 1.25
elif vr >= 1.2: o *= 1.10
o *= 1.20 if last > ema21 else 0.85
if atrp < 2.0: o *= 1.10
elif atrp > 3.0: o *= 0.90
bayes = o / (1 + o)
print(f'Bayes prob: {bayes:.0%} | RSI {rsi:.0f} Vol {vr:.1f}x ATR {atrp:.2f}%')

# 8. MONTE CARLO
mu = np.mean(rets[-100:])
sg = np.std(rets[-100:])
np.random.seed(42)
z = np.random.normal(0, 1, (500, 10))
mp = np.exp(mu + sg * z)
ends = last * np.cumprod(mp, axis=1)[:, -1]
mc_w = float(np.mean(ends > last))
mc_r = float(np.mean(ends / last - 1))
print(f'Monte Carlo: Win={mc_w:.0%} Avg={mc_r*100:+.2f}% (500 paths x 10 bars)')

# VOTE
long_v, short_v = 0, 0
if entropy < 3.5: long_v += (1 if last > ema21 else -1)
if bayes > 0.6: long_v += 2
elif bayes < 0.45: short_v += 2
if mc_w > 0.55: long_v += 1
elif mc_w < 0.45: short_v += 1
if alpha > 0.6 and last > ema21: long_v += 1
elif alpha > 0.6 and last < ema21: short_v += 1
elif alpha < 0.4: long_v += 1
if fz > 0.5: long_v += 1
elif fz < -0.5: short_v += 1

short_v = abs(min(0, long_v)) if long_v < 0 else short_v
long_v = max(0, long_v)

direction = "LONG" if long_v > short_v else ("SHORT" if short_v > long_v else "NEUTRAL")
conf = max(long_v, short_v) / max(long_v + short_v, 1) * 100

print('='*50)
print(f'PREDICTION: {direction} | Conf {conf:.0f}%')
print(f'Target: ${last * (1 + abs(mc_r)):.0f} ({mc_r*100:+.1f}%)')
print(f'Stop: ${last * (1 - 0.02):.0f} (-2.0%)')
print(f'Regime: {regime} | Vol: {atrp:.2f}%/bar | RSI: {rsi:.0f}')
