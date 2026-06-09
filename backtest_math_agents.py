#!/usr/bin/env python3
"""
BACKTEST: MathMaster + QuantumMaster agents on 1Y crypto 1H data.

Reproduces every math layer EXACTLY as written in bot.py.
Tests each layer individually + the combined vote at multiple
forward horizons (5h, 12h, 24h) to see which layers actually
predict profit DIRECTION, not micro-movement.
"""

import numpy as np
import pandas as pd
import math
import json
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict

# ============================================================
# IMPORT from bot.py — exact same functions
# ============================================================
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _shannon_entropy(returns: np.ndarray, bins: int = 20) -> float:
    if len(returns) < 50:
        return 5.0
    hist, _ = np.histogram(returns, bins=bins, range=(-0.05, 0.05))
    hist = hist[hist > 0]
    probs = hist / hist.sum()
    return float(-np.sum(probs * np.log2(probs)))

def _bayesian_signal_prob(rsi_val, v_ratio, close_above_ema, vol_pct) -> float:
    prior = 0.55
    odds = prior / (1 - prior)
    if 30 <= rsi_val <= 55:
        odds *= 1.15
    elif rsi_val < 25:
        odds *= 0.85
    elif rsi_val > 70:
        odds *= 0.80
    if v_ratio >= 1.5:
        odds *= 1.25
    elif v_ratio >= 1.2:
        odds *= 1.10
    if close_above_ema:
        odds *= 1.20
    else:
        odds *= 0.85
    if vol_pct < 2.0:
        odds *= 1.10
    elif vol_pct > 3.0:
        odds *= 0.90
    posterior = odds / (1 + odds)
    return float(posterior)

def _monte_carlo_win_prob(closes: np.ndarray, n_paths: int = 200,
                           horizon: int = 5) -> float:
    if len(closes) < 50:
        return 0.5
    log_rets = np.diff(np.log(closes[-100:]))
    mu = log_rets.mean()
    sigma = log_rets.std()
    last_price = closes[-1]
    np.random.seed(42)
    z = np.random.normal(0, 1, (n_paths, horizon))
    paths = np.exp(mu + sigma * z)
    end_prices = last_price * np.cumprod(paths, axis=1)[:, -1]
    win_prob = np.mean(end_prices > last_price)
    return float(win_prob)

def _lyapunov_exponent(prices: np.ndarray, window: int = 50) -> float:
    if len(prices) < window + 10:
        return 0.5
    rets = np.diff(np.log(prices[-window:]))
    if len(rets) < 10:
        return 0.5
    x = rets[:-1]
    y = rets[1:]
    if len(x) < 5:
        return 0.5
    divergences = []
    for i in range(len(x) - 2):
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
    if len(divergences) < 3:
        return 0.5
    return float(np.mean(divergences))

def _wasserstein_1d(sample_a: np.ndarray, sample_b: np.ndarray) -> float:
    if len(sample_a) < 5 or len(sample_b) < 5:
        return 0.0
    a_sorted = np.sort(sample_a)
    b_sorted = np.sort(sample_b)
    n = min(len(a_sorted), len(b_sorted))
    a_idx = np.linspace(0, len(a_sorted) - 1, n).astype(int)
    b_idx = np.linspace(0, len(b_sorted) - 1, n).astype(int)
    a_sampled = a_sorted[a_idx]
    b_sampled = b_sorted[b_idx]
    return float(np.mean(np.abs(a_sampled - b_sampled)))

def _spectral_entropy(prices: np.ndarray) -> float:
    if len(prices) < 30:
        return 0.5
    x = np.arange(len(prices))
    slope, intercept = np.polyfit(x, prices, 1)
    detrended = prices - (slope * x + intercept)
    windowed = detrended * np.hamming(len(detrended))
    fft = np.fft.rfft(windowed)
    power = np.abs(fft)**2
    if power.sum() < 1e-10:
        return 0.5
    p = power / power.sum()
    p = p[p > 1e-10]
    if len(p) < 2:
        return 0.5
    H = -np.sum(p * np.log2(p))
    H_max = np.log2(len(p))
    return float(H / H_max) if H_max > 0 else 0.5

def _dfa_alpha(prices: np.ndarray) -> float:
    if len(prices) < 100:
        return 0.5
    y = np.cumsum(prices - np.mean(prices))
    n_values = np.logspace(np.log10(10), np.log10(len(prices) // 4), 15).astype(int)
    n_values = np.unique(n_values)
    n_values = n_values[n_values >= 4]
    if len(n_values) < 3:
        return 0.5
    fluct = []
    for n in n_values:
        n_windows = len(y) // n
        if n_windows < 2:
            continue
        rms = 0.0
        for i in range(n_windows):
            segment = y[i*n:(i+1)*n]
            x_seg = np.arange(len(segment))
            A = np.vstack([x_seg, np.ones(len(x_seg))]).T
            coeffs, _, _, _ = np.linalg.lstsq(A, segment, rcond=None)
            trend = A @ coeffs
            detrended = segment - trend
            rms += np.mean(detrended**2)
        rms /= n_windows
        fluct.append(np.sqrt(rms))
    if len(fluct) < 3:
        return 0.5
    log_n = np.log(n_values[:len(fluct)])
    log_f = np.log(np.maximum(fluct, 1e-10))
    A = np.vstack([log_n, np.ones(len(log_n))]).T
    alpha, _ = np.linalg.lstsq(A, log_f, rcond=None)[:2]
    return float(alpha[0])

def _fisher_information(prices: np.ndarray, window: int = 30) -> float:
    if len(prices) < window + 5:
        return 0.0
    p = prices / np.sum(prices[-window:])
    if np.any(p <= 0):
        return 0.0
    dp = np.diff(p)
    fisher = np.sum(dp**2 / p[1:]) if np.all(p[1:] > 0) else 0
    fisher_hist = []
    for i in range(window, len(prices) - 1):
        p_slice = prices[i-window:i] / np.sum(prices[i-window:i])
        if np.all(p_slice[1:] > 0):
            dp_s = np.diff(p_slice)
            f = np.sum(dp_s**2 / p_slice[1:])
            fisher_hist.append(f)
    if len(fisher_hist) < 5:
        return float(fisher * 1000)
    fisher_hist = np.array(fisher_hist)
    mu = np.mean(fisher_hist)
    sigma = np.std(fisher_hist)
    if sigma < 1e-10:
        return 0.0
    return float((fisher - mu) / sigma)

def _renyi_entropy(prices: np.ndarray, q: float = 2.0) -> float:
    if len(prices) < 20:
        return 0.0
    rets = np.diff(np.log(prices[-100:]))
    if len(rets) < 10:
        return 0.0
    hist, _ = np.histogram(rets, bins=20, range=(-0.05, 0.05))
    hist = hist[hist > 0]
    if len(hist) < 2:
        return 0.0
    p = hist / hist.sum()
    if abs(q - 1.0) < 0.01:
        return float(-np.sum(p * np.log2(p)))
    else:
        sum_pq = np.sum(p**q)
        if sum_pq < 1e-10:
            return 0.0
        return float((1.0 / (1.0 - q)) * np.log2(sum_pq))

# ============================================================
# LOAD DATA
# ============================================================
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backtest_data")

def load_symbol(sym: str, tf: str = "1H") -> pd.DataFrame:
    path = os.path.join(DATA_DIR, f"{sym}_USDT_{tf}_365d.parquet")
    if not os.path.exists(path):
        print(f"  MISSING {path}")
        return None
    df = pd.read_parquet(path)
    if 'ts' in df.columns:
        df['timestamp'] = pd.to_datetime(df['ts'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.drop(columns=['ts'], inplace=True)
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    for extra in ['vc', 'vcq', 'confirm']:
        if extra in df.columns:
            df.drop(columns=[extra], inplace=True)
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
    high, low, close = df['high'], df['low'], df['close']
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def _normal_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ============================================================
# MATHMASTER BACKTEST
# ============================================================
def backtest_mathmaster(df: pd.DataFrame, horizons: list) -> dict:
    """Backtest each MathMaster layer at multiple forward horizons."""
    c = df['close'].values
    h = df['high'].values
    l = df['low'].values
    v = df['volume'].values

    results = {}
    for hz in horizons:
        results[hz] = {
            'entropy': [],
            'bayes': [],
            'monte_carlo': [],
            'max_entropy': [],
            'combined': [],
        }

    for i in range(200, len(c) - 24):
        window_c = c[:i+1]
        window_h = h[:i+1]
        window_l = l[:i+1]
        window_v = v[:i+1]
        last_c = window_c[-1]

        # -- Layer 1: ENTROPY --
        log_rets = np.diff(np.log(window_c[-100:]))
        entropy = _shannon_entropy(log_rets)
        entropy_ok = entropy < 3.5

        # -- Layer 2: BAYES --
        rsi_val = float(rsi(pd.Series(window_c)).iloc[-1])
        v_avg = float(pd.Series(window_v).rolling(20).mean().iloc[-1])
        v_ratio = window_v[-1] / v_avg if v_avg > 0 else 1.0
        e21 = float(ema(pd.Series(window_c), 21).iloc[-1])
        close_above_ema = last_c > e21
        atr_val = float(atr(pd.DataFrame({'high': window_h, 'low': window_l, 'close': window_c})).iloc[-1])
        atr_pct = (atr_val / last_c) * 100 if last_c > 0 else 99
        bayes_prob = _bayesian_signal_prob(rsi_val, v_ratio, close_above_ema, atr_pct)
        bayes_ok = bayes_prob >= 0.60

        # -- Layer 3: MONTE CARLO --
        mc_prob = _monte_carlo_win_prob(window_c, n_paths=200, horizon=5)
        mc_long = mc_prob >= 0.55
        mc_short = (1 - mc_prob) >= 0.55

        # -- Layer 4: MAX ENTROPY --
        mu = log_rets.mean()
        sigma = log_rets.std()
        me_prob = 1 - _normal_cdf(-mu / sigma) if sigma > 0 else 0.5
        me_long = me_prob >= 0.55
        me_short = me_prob <= 0.45

        # -- VOTE --
        votes_long, votes_short = 0, 0
        if entropy_ok:
            if close_above_ema: votes_long += 1
            else: votes_short += 1
        if bayes_ok:
            if close_above_ema: votes_long += 1
            else: votes_short += 1
        if mc_long: votes_long += 1
        elif mc_short: votes_short += 1
        if me_long: votes_long += 1
        elif me_short: votes_short += 1
        side = 'long' if votes_long >= 3 else ('short' if votes_short >= 3 else None)

        for hz in horizons:
            fwd_idx = min(i + hz, len(c) - 1)
            fwd_ret = (c[fwd_idx] - last_c) / last_c

            if entropy_ok:
                layer_side = 'long' if close_above_ema else 'short'
                results[hz]['entropy'].append((layer_side, fwd_ret))
            if bayes_ok:
                layer_side = 'long' if close_above_ema else 'short'
                results[hz]['bayes'].append((layer_side, fwd_ret))
            if mc_long or mc_short:
                layer_side = 'long' if mc_long else 'short'
                results[hz]['monte_carlo'].append((layer_side, fwd_ret))
            if me_long or me_short:
                layer_side = 'long' if me_long else 'short'
                results[hz]['max_entropy'].append((layer_side, fwd_ret))
            if side:
                results[hz]['combined'].append((side, fwd_ret))

    return results

# ============================================================
# QUANTUMMASTER BACKTEST
# ============================================================
def backtest_quantummaster(df: pd.DataFrame, horizons: list) -> dict:
    """Backtest each QuantumMaster layer at multiple forward horizons."""
    c = df['close'].values
    h = df['high'].values
    l = df['low'].values
    v = df['volume'].values

    results = {}
    for hz in horizons:
        results[hz] = {
            'lyapunov': [],
            'wasserstein': [],
            'spectral_entropy': [],
            'dfa': [],
            'fisher': [],
            'renyi': [],
            'combined': [],
        }

    for i in range(200, len(c) - 24):
        window_c = c[:i+1]
        window_h = h[:i+1]
        window_l = l[:i+1]
        window_v = v[:i+1]
        last_c = window_c[-1]

        # 6 layers
        lyap = _lyapunov_exponent(window_c)
        lyap_ok = lyap < 0.15

        recent_rets = np.diff(np.log(window_c[-30:]))
        old_rets = np.diff(np.log(window_c[-120:-30])) if len(window_c) >= 120 else recent_rets
        wass = _wasserstein_1d(recent_rets, old_rets)
        wass_ok = wass > 0.001

        spec_ent = _spectral_entropy(window_c[-200:])
        spec_ok = spec_ent < 0.80

        dfa_alpha = _dfa_alpha(window_c)
        dfa_trending = dfa_alpha > 0.6
        dfa_mr = dfa_alpha < 0.4
        dfa_ok = dfa_trending or dfa_mr

        fisher_z = _fisher_information(window_c)
        fisher_ok = fisher_z > -0.5

        h1 = _renyi_entropy(window_c, q=1.0)
        h2 = _renyi_entropy(window_c, q=2.0)
        renyi_gap = abs(h1 - h2)
        renyi_ok = renyi_gap < 0.5

        e21 = float(ema(pd.Series(window_c), 21).iloc[-1])
        close_above_ema = last_c > e21

        # Vote
        votes_long, votes_short = 0, 0
        if lyap_ok:
            if close_above_ema: votes_long += 1
            else: votes_short += 1
        if wass_ok:
            if wass > 0 and close_above_ema: votes_long += 1
            elif wass > 0: votes_short += 1
        if spec_ok:
            if close_above_ema: votes_long += 1
            else: votes_short += 1
        if dfa_ok:
            if dfa_trending and close_above_ema: votes_long += 1
            elif dfa_mr and not close_above_ema: votes_short += 1
            elif dfa_trending and not close_above_ema: votes_short += 1
            else: votes_long += 1
        if fisher_ok:
            if fisher_z > 1.0:
                if close_above_ema: votes_long += 2
                else: votes_short += 2
            else:
                if close_above_ema: votes_long += 1
                else: votes_short += 1
        if renyi_ok:
            if h1 > h2:
                if close_above_ema: votes_long += 1
                else: votes_short += 1

        side = 'long' if votes_long >= 3 else ('short' if votes_short >= 3 else None)

        # Determine layer signal directions
        lyap_side = 'long' if (close_above_ema and lyap_ok) else ('short' if not close_above_ema and lyap_ok else None)
        wass_side = 'long' if (wass > 0 and close_above_ema and wass_ok) else ('short' if wass > 0 and not close_above_ema and wass_ok else None)
        spec_side = 'long' if (close_above_ema and spec_ok) else ('short' if not close_above_ema and spec_ok else None)
        dfa_side = None
        if dfa_ok:
            if dfa_trending and close_above_ema: dfa_side = 'long'
            elif dfa_mr and not close_above_ema: dfa_side = 'short'
            elif dfa_trending and not close_above_ema: dfa_side = 'short'
            else: dfa_side = 'long'
        fisher_side = None
        if fisher_ok:
            if fisher_z > 1.0:
                fisher_side = 'long' if close_above_ema else 'short'
            else:
                fisher_side = 'long' if close_above_ema else 'short'
        renyi_side = 'long' if (h1 > h2 and renyi_ok and close_above_ema) else ('short' if h1 > h2 and renyi_ok and not close_above_ema else None)

        for hz in horizons:
            fwd_idx = min(i + hz, len(c) - 1)
            fwd_ret = (c[fwd_idx] - last_c) / last_c

            if lyap_side: results[hz]['lyapunov'].append((lyap_side, fwd_ret))
            if wass_side: results[hz]['wasserstein'].append((wass_side, fwd_ret))
            if spec_side: results[hz]['spectral_entropy'].append((spec_side, fwd_ret))
            if dfa_side: results[hz]['dfa'].append((dfa_side, fwd_ret))
            if fisher_side: results[hz]['fisher'].append((fisher_side, fwd_ret))
            if renyi_side: results[hz]['renyi'].append((renyi_side, fwd_ret))
            if side: results[hz]['combined'].append((side, fwd_ret))

    return results

# ============================================================
# ANALYZE
# ============================================================
def analyze_layer(predictions: list) -> dict:
    if not predictions:
        return {'n_trades': 0, 'win_rate': 0.0, 'avg_ret_pct': 0.0, 'total_ret_pct': 0.0, 'sharpe': 0.0}
    wins = 0
    rets = []
    for side, fwd_ret in predictions:
        ret = fwd_ret if side == 'long' else -fwd_ret
        rets.append(ret)
        if ret > 0:
            wins += 1
    rets = np.array(rets)
    n = len(rets)
    win_rate = wins / n
    avg_ret = float(rets.mean())
    total_ret = float(rets.sum())
    std_ret = float(rets.std()) if n > 1 else 0.001
    sharpe = avg_ret / std_ret if std_ret > 0 else 0.0
    return {
        'n_trades': n,
        'win_rate': round(win_rate, 4),
        'avg_ret_pct': round(avg_ret * 100, 4),
        'total_ret_pct': round(total_ret * 100, 4),
        'sharpe': round(sharpe, 4),
    }

# ============================================================
# RUN
# ============================================================
if __name__ == '__main__':
    symbols = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP']
    horizons = [5, 12, 24]  # 5h, 12h, 24h forward
    results = {}

    for sym in symbols:
        print(f"\n{'='*65}")
        print(f"Loading {sym}_USDT 1H...")
        df = load_symbol(sym)
        if df is None or len(df) < 500:
            print(f"  SKIP: insufficient data")
            continue
        print(f"  Bars: {len(df)}, {df.index[0].date()} to {df.index[-1].date()}")

        # MATHMASTER
        print(f"\n--- MATHMASTER ({sym}) ---")
        mm = backtest_mathmaster(df, horizons)
        mm_results = {}
        for hz in horizons:
            print(f"  Horizon {hz}h:")
            for layer_name, preds in mm[hz].items():
                res = analyze_layer(preds)
                if layer_name not in mm_results:
                    mm_results[layer_name] = {}
                mm_results[layer_name][hz] = res
                sig = "✅" if res['sharpe'] > 0.3 and res['n_trades'] > 30 else ("❌" if res['sharpe'] < -0.1 else "➖")
                print(f"    {sig} {layer_name:15s}: {res['n_trades']:5d} trades | "
                      f"WR {res['win_rate']:.1%} | avg {res['avg_ret_pct']:+.3f}% | "
                      f"total {res['total_ret_pct']:+.1f}% | Sharpe {res['sharpe']:.2f}")

        # QUANTUMMASTER
        print(f"\n--- QUANTUMMASTER ({sym}) ---")
        qm = backtest_quantummaster(df, horizons)
        qm_results = {}
        for hz in horizons:
            print(f"  Horizon {hz}h:")
            for layer_name, preds in qm[hz].items():
                res = analyze_layer(preds)
                if layer_name not in qm_results:
                    qm_results[layer_name] = {}
                qm_results[layer_name][hz] = res
                sig = "✅" if res['sharpe'] > 0.3 and res['n_trades'] > 30 else ("❌" if res['sharpe'] < -0.1 else "➖")
                print(f"    {sig} {layer_name:20s}: {res['n_trades']:5d} trades | "
                      f"WR {res['win_rate']:.1%} | avg {res['avg_ret_pct']:+.3f}% | "
                      f"total {res['total_ret_pct']:+.1f}% | Sharpe {res['sharpe']:.2f}")

        results[sym] = {
            'mathmaster': {k: {str(hz): v for hz, v in v.items()} for k, v in mm_results.items()},
            'quantummaster': {k: {str(hz): v for hz, v in v.items()} for k, v in qm_results.items()},
        }

    # Save
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "backtest_results",
        f"math_agents_backtest_{ts}.json"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n\nSaved to {output_path}")

    # High-level summary
    print(f"\n{'='*65}")
    print("TOP-LINE SUMMARY: LAYERS THAT ACTUALLY PREDICT")
    print(f"{'='*65}")
    for sym, data in results.items():
        best_mm = []
        best_qm = []
        for agent_type in ['mathmaster', 'quantummaster']:
            for layer, hz_data in data[agent_type].items():
                for hz, res in hz_data.items():
                    if res['sharpe'] > 0.3 and res['n_trades'] > 50:
                        entry = f"  {sym}/{agent_type}/{layer}@{hz}h: Sharpe {res['sharpe']:.2f}, WR {res['win_rate']:.1%}, +{res['total_ret_pct']:.1f}%"
                        if agent_type == 'mathmaster':
                            best_mm.append(entry)
                        else:
                            best_qm.append(entry)
        if best_mm:
            print(f"\n{sym} MathMaster winners:")
            for e in best_mm:
                print(e)
        if best_qm:
            print(f"\n{sym} QuantumMaster winners:")
            for e in best_qm:
                print(e)
