#!/usr/bin/env python3
"""
FAST BACKTEST: MathMaster + QuantumMaster on BTC 1H data.

Optimizations vs v1:
1. STRIDE: sample every 4th bar instead of every bar (2250 samples instead of 9000)
2. SAMPLED DFA: only compute DFA every 20th bar, reuse for nearby bars
3. Only run BTC first (fast), then extend to others
4. Use print(flush=True) so we see output immediately
"""

import numpy as np
import pandas as pd
import math
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ========= MATH FUNCTIONS (unchanged from bot.py) =========
def _shannon_entropy(returns, bins=20):
    if len(returns) < 50: return 5.0
    hist, _ = np.histogram(returns, bins=bins, range=(-0.05, 0.05))
    hist = hist[hist > 0]
    probs = hist / hist.sum()
    return float(-np.sum(probs * np.log2(probs)))

def _bayesian_signal_prob(rsi_val, v_ratio, close_above_ema, vol_pct):
    prior = 0.55
    odds = prior / (1 - prior)
    if 30 <= rsi_val <= 55: odds *= 1.15
    elif rsi_val < 25: odds *= 0.85
    elif rsi_val > 70: odds *= 0.80
    if v_ratio >= 1.5: odds *= 1.25
    elif v_ratio >= 1.2: odds *= 1.10
    if close_above_ema: odds *= 1.20
    else: odds *= 0.85
    if vol_pct < 2.0: odds *= 1.10
    elif vol_pct > 3.0: odds *= 0.90
    return float(odds / (1 + odds))

def _monte_carlo_win_prob(closes, n_paths=200, horizon=5):
    if len(closes) < 50: return 0.5
    log_rets = np.diff(np.log(closes[-100:]))
    mu, sigma = log_rets.mean(), log_rets.std()
    np.random.seed(42)
    z = np.random.normal(0, 1, (n_paths, horizon))
    paths = np.exp(mu + sigma * z)
    end_prices = closes[-1] * np.cumprod(paths, axis=1)[:, -1]
    return float(np.mean(end_prices > closes[-1]))

def _lyapunov_exponent(prices, window=50):
    if len(prices) < window + 10: return 0.5
    rets = np.diff(np.log(prices[-window:]))
    if len(rets) < 10: return 0.5
    x, y = rets[:-1], rets[1:]
    if len(x) < 5: return 0.5
    divergences = []
    for i in range(min(len(x) - 2, 20)):  # SAMPLE: only 20 neighbors
        dists = np.sqrt((x - x[i])**2 + (y - y[i])**2)
        dists[i] = np.inf
        min_idx = np.argmin(dists)
        if min_idx < len(x) - 1:
            d0 = dists[min_idx]
            if d0 > 1e-10:
                d1 = np.sqrt((x[min_idx+1] - x[i+1])**2 +
                             (y[min_idx+1] if min_idx+1 < len(y) else y[-1] - y[i+1])**2)
                d1 = max(d1, 1e-10)
                divergences.append(np.log(d1 / d0))
    return float(np.mean(divergences)) if len(divergences) >= 3 else 0.5

def _wasserstein_1d(a, b):
    if len(a) < 5 or len(b) < 5: return 0.0
    a, b = np.sort(a), np.sort(b)
    n = min(len(a), len(b))
    a_s = a[np.linspace(0, len(a)-1, n).astype(int)]
    b_s = b[np.linspace(0, len(b)-1, n).astype(int)]
    return float(np.mean(np.abs(a_s - b_s)))

def _spectral_entropy(prices):
    if len(prices) < 30: return 0.5
    x = np.arange(len(prices))
    slope, intercept = np.polyfit(x, prices, 1)
    detrended = prices - (slope * x + intercept)
    windowed = detrended * np.hamming(len(detrended))
    fft = np.fft.rfft(windowed)
    power = np.abs(fft)**2
    if power.sum() < 1e-10: return 0.5
    p = power / power.sum()
    p = p[p > 1e-10]
    if len(p) < 2: return 0.5
    H = -np.sum(p * np.log2(p))
    H_max = np.log2(len(p))
    return float(H / H_max) if H_max > 0 else 0.5

def _dfa_alpha(prices):
    if len(prices) < 100: return 0.5
    y = np.cumsum(prices - np.mean(prices))
    n_values = np.logspace(np.log10(10), np.log10(len(prices) // 4), 10).astype(int)
    n_values = np.unique(n_values)
    n_values = n_values[n_values >= 4]
    if len(n_values) < 3: return 0.5
    fluct = []
    for n in n_values:
        n_windows = len(y) // n
        if n_windows < 2: continue
        rms = 0.0
        for i in range(n_windows):
            seg = y[i*n:(i+1)*n]
            x_s = np.arange(len(seg))
            A = np.vstack([x_s, np.ones(len(x_s))]).T
            coeffs, _, _, _ = np.linalg.lstsq(A, seg, rcond=None)
            detrended = seg - A @ coeffs
            rms += np.mean(detrended**2)
        rms /= n_windows
        fluct.append(np.sqrt(rms))
    if len(fluct) < 3: return 0.5
    log_n = np.log(n_values[:len(fluct)])
    log_f = np.log(np.maximum(fluct, 1e-10))
    A = np.vstack([log_n, np.ones(len(log_n))]).T
    alpha, _ = np.linalg.lstsq(A, log_f, rcond=None)[:2]
    return float(alpha[0])

def _fisher_information(prices, window=30):
    if len(prices) < window + 5: return 0.0
    p = prices / np.sum(prices[-window:])
    if np.any(p <= 0): return 0.0
    dp = np.diff(p)
    fisher = np.sum(dp**2 / p[1:]) if np.all(p[1:] > 0) else 0
    fisher_hist = []
    for i in range(window, len(prices) - 1, 3):  # stride 3
        p_s = prices[i-window:i] / np.sum(prices[i-window:i])
        if np.all(p_s[1:] > 0):
            dp_s = np.diff(p_s)
            fisher_hist.append(np.sum(dp_s**2 / p_s[1:]))
    if len(fisher_hist) < 5: return float(fisher * 1000)
    fh = np.array(fisher_hist)
    mu, sigma = np.mean(fh), np.std(fh)
    return float((fisher - mu) / sigma) if sigma > 1e-10 else 0.0

def _renyi_entropy(prices, q=2.0):
    if len(prices) < 20: return 0.0
    rets = np.diff(np.log(prices[-100:]))
    if len(rets) < 10: return 0.0
    hist, _ = np.histogram(rets, bins=20, range=(-0.05, 0.05))
    hist = hist[hist > 0]
    if len(hist) < 2: return 0.0
    p = hist / hist.sum()
    if abs(q - 1.0) < 0.01:
        return float(-np.sum(p * np.log2(p)))
    sum_pq = np.sum(p**q)
    return float((1.0/(1.0-q)) * np.log2(sum_pq)) if sum_pq > 1e-10 else 0.0

def _normal_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ========= DATA =========
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backtest_data")

def load_symbol(sym, tf="1H"):
    path = os.path.join(DATA_DIR, f"{sym}_USDT_{tf}_365d.parquet")
    if not os.path.exists(path): return None
    df = pd.read_parquet(path)
    if 'ts' in df.columns:
        df['timestamp'] = pd.to_datetime(df['ts'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.drop(columns=['ts'], inplace=True)
    for col in ['open','high','low','close','volume']:
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
    for extra in ['vc','vcq','confirm']:
        if extra in df.columns: df.drop(columns=[extra], inplace=True)
    return df

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def atr(df, period=14):
    h, l, c = df['high'], df['low'], df['close']
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()

# ========= ANALYZE =========
def analyze_layer(predictions):
    if not predictions:
        return {'n_trades': 0, 'win_rate': 0.0, 'avg_ret_pct': 0.0, 'total_ret_pct': 0.0, 'sharpe': 0.0}
    rets = np.array([r if s == 'long' else -r for s, r in predictions])
    n = len(rets)
    wins = int(np.sum(rets > 0))
    avg = float(rets.mean())
    std = float(rets.std()) if n > 1 else 0.001
    return {
        'n_trades': n, 'win_rate': round(wins/n, 4),
        'avg_ret_pct': round(avg*100, 4), 'total_ret_pct': round(float(rets.sum())*100, 4),
        'sharpe': round(avg/std, 4),
    }

# ========= MAIN BACKTEST =========
def backtest_one(df, sym, horizons):
    c = df['close'].values
    h = df['high'].values
    l = df['low'].values
    v = df['volume'].values

    # Precompute EMA21 and close_above_ema for every bar
    c_series = pd.Series(c)
    e21_vals = ema(c_series, 21).values
    ca_ema = c > e21_vals

    # Precompute RSI for every bar
    rsi_vals = rsi(c_series).values

    # Precompute ATR for every bar (rough: 1 bar lag okay)
    atr_series = atr(pd.DataFrame({'high': np.where(h>0, h, c), 'low': np.where(l>0, l, c*0.99), 'close': c}))
    atr_vals = atr_series.values
    atr_pct = np.where(c > 0, (atr_vals / c) * 100, 99)
    atr_pct = np.nan_to_num(atr_pct, nan=99)

    # Precompute volume ratio
    v_avg = pd.Series(v).rolling(20).mean().values
    v_ratio = np.where(v_avg > 0, v / v_avg, 1.0)

    # Precompute log returns once
    log_rets_all = np.diff(np.log(c))

    # DFA is expensive — compute every 20 bars, cached
    dfa_cache = {}
    for i in range(200, len(c)):
        if i % 20 == 0:
            dfa_cache[i] = _dfa_alpha(c[:i+1])

    def get_dfa(i):
        # Find nearest cached DFA within 10 bars
        for j in range(i, i - 15, -1):
            if j in dfa_cache:
                return dfa_cache[j]
        return _dfa_alpha(c[:i+1])

    stride = 4  # sample every 4th bar
    io = 0

    print(f"  Running {sym}... (checking ~{len(range(200, len(c)-24, stride))} bars)", flush=True)

    mm_layers = {h: {k: [] for k in ['entropy','bayes','monte_carlo','max_entropy','combined']} for h in horizons}
    qm_layers = {h: {k: [] for k in ['lyapunov','wasserstein','spectral_entropy','dfa','fisher','renyi','combined']} for h in horizons}

    for i in range(200, len(c) - 24, stride):
        last_c = c[i]
        lr_window = log_rets_all[i-100:i]  # last 100 log returns

        # --- MATHMASTER ---
        entropy = _shannon_entropy(lr_window)
        entropy_ok = entropy < 3.5

        ri = i if i < len(rsi_vals) else len(rsi_vals) - 1
        rsi_v = float(rsi_vals[ri])
        vr = float(v_ratio[ri])
        ap = float(atr_pct[ri])
        bayes_prob = _bayesian_signal_prob(rsi_v, vr, ca_ema[ri], ap)
        bayes_ok = bayes_prob >= 0.60

        mc_prob = _monte_carlo_win_prob(c[:i+1], n_paths=200, horizon=5)
        mc_long = mc_prob >= 0.55
        mc_short = (1 - mc_prob) >= 0.55

        mu = lr_window.mean()
        sigma = lr_window.std()
        me_prob = 1 - _normal_cdf(-mu/sigma) if sigma > 0 else 0.5
        me_long = me_prob >= 0.55
        me_short = me_prob <= 0.45

        # MM vote
        ml, ms = 0, 0
        if entropy_ok:
            if ca_ema[ri]: ml += 1
            else: ms += 1
        if bayes_ok:
            if ca_ema[ri]: ml += 1
            else: ms += 1
        if mc_long: ml += 1
        elif mc_short: ms += 1
        if me_long: ml += 1
        elif me_short: ms += 1
        mm_side = 'long' if ml >= 3 else ('short' if ms >= 3 else None)

        # --- QUANTUMMASTER ---
        lyap = _lyapunov_exponent(c[:i+1])
        lyap_ok = lyap < 0.15

        recent_rets = log_rets_all[i-30:i]
        old_rets = log_rets_all[max(0,i-120):i-30]
        wass = _wasserstein_1d(recent_rets, old_rets)
        wass_ok = wass > 0.001

        spec_ent = _spectral_entropy(c[-200+i+1 if i >= 200 else i+1:][:200] if i >= 200 else c[:i+1])
        spec_ok = spec_ent < 0.80

        dfa_a = get_dfa(i)
        dfa_t = dfa_a > 0.6
        dfa_mr = dfa_a < 0.4
        dfa_ok = dfa_t or dfa_mr

        fz = _fisher_information(c[:i+1])
        fisher_ok = fz > -0.5

        h1 = _renyi_entropy(c[:i+1], q=1.0)
        h2 = _renyi_entropy(c[:i+1], q=2.0)
        rg = abs(h1 - h2)
        renyi_ok = rg < 0.5

        # QM vote
        ql, qs = 0, 0
        if lyap_ok:
            if ca_ema[ri]: ql += 1
            else: qs += 1
        if wass_ok:
            if wass > 0 and ca_ema[ri]: ql += 1
            elif wass > 0: qs += 1
        if spec_ok:
            if ca_ema[ri]: ql += 1
            else: qs += 1
        if dfa_ok:
            if dfa_t and ca_ema[ri]: ql += 1
            elif dfa_mr and not ca_ema[ri]: qs += 1
            elif dfa_t and not ca_ema[ri]: qs += 1
            else: ql += 1
        if fisher_ok:
            if fz > 1.0:
                if ca_ema[ri]: ql += 2
                else: qs += 2
            else:
                if ca_ema[ri]: ql += 1
                else: qs += 1
        if renyi_ok:
            if h1 > h2:
                if ca_ema[ri]: ql += 1
                else: qs += 1
        qm_side = 'long' if ql >= 3 else ('short' if qs >= 3 else None)

        for hz in horizons:
            fwd = min(i + hz, len(c) - 1)
            fwd_ret = (c[fwd] - last_c) / last_c

            if entropy_ok:
                lside = 'long' if ca_ema[ri] else 'short'
                mm_layers[hz]['entropy'].append((lside, fwd_ret))
            if bayes_ok:
                lside = 'long' if ca_ema[ri] else 'short'
                mm_layers[hz]['bayes'].append((lside, fwd_ret))
            if mc_long or mc_short:
                lside = 'long' if mc_long else 'short'
                mm_layers[hz]['monte_carlo'].append((lside, fwd_ret))
            if me_long or me_short:
                lside = 'long' if me_long else 'short'
                mm_layers[hz]['max_entropy'].append((lside, fwd_ret))
            if mm_side:
                mm_layers[hz]['combined'].append((mm_side, fwd_ret))

            # QM layers
            if lyap_ok:
                lside = 'long' if ca_ema[ri] else 'short'
                qm_layers[hz]['lyapunov'].append((lside, fwd_ret))
            if wass_ok:
                lside = 'long' if (wass > 0 and ca_ema[ri]) else 'short'
                qm_layers[hz]['wasserstein'].append((lside, fwd_ret))
            if spec_ok:
                lside = 'long' if ca_ema[ri] else 'short'
                qm_layers[hz]['spectral_entropy'].append((lside, fwd_ret))
            if dfa_ok:
                if dfa_t and ca_ema[ri]: lside = 'long'
                elif dfa_mr and not ca_ema[ri]: lside = 'short'
                elif dfa_t and not ca_ema[ri]: lside = 'short'
                else: lside = 'long'
                qm_layers[hz]['dfa'].append((lside, fwd_ret))
            if fisher_ok:
                lside = 'long' if ca_ema[ri] else 'short'
                qm_layers[hz]['fisher'].append((lside, fwd_ret))
            if renyi_ok:
                if h1 > h2:
                    lside = 'long' if ca_ema[ri] else 'short'
                    qm_layers[hz]['renyi'].append((lside, fwd_ret))
            if qm_side:
                qm_layers[hz]['combined'].append((qm_side, fwd_ret))

        io += 1
        if io % 100 == 0:
            print(f"    processed {io} bars...", flush=True)

    return mm_layers, qm_layers

# ========= MAIN =========
if __name__ == '__main__':
    symbols = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP']
    horizons = [5, 12, 24]
    results = {}

    for sym in symbols:
        print(f"\n{'='*65}", flush=True)
        print(f"Loading {sym}_USDT 1H...", flush=True)
        df = load_symbol(sym)
        if df is None or len(df) < 500:
            print(f"  SKIP: insufficient data", flush=True)
            continue
        print(f"  Bars: {len(df)}, {df.index[0].date()} to {df.index[-1].date()}", flush=True)

        mm, qm = backtest_one(df, sym, horizons)

        print(f"\n--- MATHMASTER ({sym}) ---", flush=True)
        mm_results = {}
        for hz in horizons:
            print(f"  Horizon {hz}h:", flush=True)
            for ln, preds in mm[hz].items():
                res = analyze_layer(preds)
                if ln not in mm_results: mm_results[ln] = {}
                mm_results[ln][hz] = res
                sig = "✅" if res['sharpe'] > 0.3 and res['n_trades'] > 30 else ("❌" if res['sharpe'] < -0.1 else "➖")
                print(f"    {sig} {ln:15s}: {res['n_trades']:5d} trades | "
                      f"WR {res['win_rate']:.1%} | avg {res['avg_ret_pct']:+.3f}% | "
                      f"total {res['total_ret_pct']:+.1f}% | Sharpe {res['sharpe']:.2f}", flush=True)

        print(f"\n--- QUANTUMMASTER ({sym}) ---", flush=True)
        qm_results = {}
        for hz in horizons:
            print(f"  Horizon {hz}h:", flush=True)
            for ln, preds in qm[hz].items():
                res = analyze_layer(preds)
                if ln not in qm_results: qm_results[ln] = {}
                qm_results[ln][hz] = res
                sig = "✅" if res['sharpe'] > 0.3 and res['n_trades'] > 30 else ("❌" if res['sharpe'] < -0.1 else "➖")
                print(f"    {sig} {ln:20s}: {res['n_trades']:5d} trades | "
                      f"WR {res['win_rate']:.1%} | avg {res['avg_ret_pct']:+.3f}% | "
                      f"total {res['total_ret_pct']:+.1f}% | Sharpe {res['sharpe']:.2f}", flush=True)

        results[sym] = {
            'mathmaster': {k: {str(hz): v for hz, v in v.items()} for k, v in mm_results.items()},
            'quantummaster': {k: {str(hz): v for hz, v in v.items()} for k, v in qm_results.items()},
        }

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backtest_results", f"math_agents_{ts}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved to {out}", flush=True)

    # Summary
    print(f"\n{'='*65}", flush=True)
    print("WINNERS: Sharpe > 0.3, >50 trades", flush=True)
    for sym, data in results.items():
        for at in ['mathmaster', 'quantummaster']:
            for layer, hz_data in data[at].items():
                for hz, res in hz_data.items():
                    if res['sharpe'] > 0.3 and res['n_trades'] > 50:
                        print(f"  ✅ {sym}/{at}/{layer}@{hz}h: Sharpe {res['sharpe']:.2f}, "
                              f"WR {res['win_rate']:.1%}, +{res['total_ret_pct']:.1f}% ({res['n_trades']} trades)", flush=True)
