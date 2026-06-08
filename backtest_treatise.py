#!/usr/bin/env python3
"""
Treatise-driven backtest — test what the new research said might work.

Tests:
  TEST 1: Multi-factor zone score (count + freshness + wick density + vol POC)
  TEST 2: 0.786 with extra filters (freshness, EMA200, volume)
  TEST 3: Log-scale trend channel for BTC (200-bar fit)
  TEST 4: Wedge patterns (rising = short, falling = long)
  TEST 5: Cross-asset Fib confluence (BTC+ETH+SOL simultaneously)

Period: 90 days, 12 symbols, 1H bars. Fees 0.04%. TP 2.0%/SL 1.0%/24-bar timeout.
"""
import os
import pandas as pd
import numpy as np
from collections import defaultdict

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
ROUND_TRIP_PCT = 0.04
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
           "AVAX-USDT","LINK-USDT","TAO-USDT"]
DAYS = 60

def load(sym, tf="1H"):
    f = os.path.join(CACHE, f"{sym.replace('-','_')}_{tf}_365d.parquet")
    if not os.path.exists(f): return None
    df = pd.read_parquet(f)
    df.columns = [c.lower() for c in df.columns]
    return df.iloc[-DAYS*24:].reset_index(drop=True)

def rsi(s, n=14):
    d = s.diff()
    up = d.where(d>0,0).rolling(n).mean()
    dn = (-d.where(d<0,0)).rolling(n).mean()
    return 100 - 100/(1 + up/dn)

def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def simulate(df, i, side, tp_pct, sl_pct, max_bars=24):
    entry = df["close"].iloc[i]
    if side == "long":
        tp = entry * (1+tp_pct/100); sl = entry * (1-sl_pct/100)
    else:
        tp = entry * (1-tp_pct/100); sl = entry * (1+sl_pct/100)
    end = min(i + max_bars, len(df) - 1)
    for j in range(i+1, end+1):
        h, l = df["high"].iloc[j], df["low"].iloc[j]
        if side == "long":
            if l <= sl: return ("SL", sl)
            if h >= tp: return ("TP", tp)
        else:
            if h >= sl: return ("SL", sl)
            if l <= tp: return ("TP", tp)
    return ("TIME", df["close"].iloc[end])

def pct_pnl(side, entry, exit_p):
    p = (exit_p - entry)/entry*100 if side=="long" else (entry - exit_p)/entry*100
    return p - ROUND_TRIP_PCT

# ============================================================================
# TEST 1 — Multi-factor zone scoring
# ============================================================================
def test_zone_scoring(df):
    """Score each candidate zone on multiple factors, only trade score >= 6."""
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    fib_levels = [0.236, 0.382, 0.500, 0.618, 0.786]
    for i in range(250, len(df)-5):
        if i - last_fire < 12: continue
        last = df["close"].iloc[i]
        # Build candidate zones from multiple swing windows
        all_fibs = []
        for w in [30, 60, 120, 240]:
            if i < w + 5: continue
            wh = df["high"].iloc[i-w:i].max(); wl = df["low"].iloc[i-w:i].min()
            if wh <= wl or (wh-wl)/wl < 0.015: continue
            sh_idx = df["high"].iloc[i-w:i].idxmax(); sl_idx = df["low"].iloc[i-w:i].idxmin()
            upt = sh_idx > sl_idx
            move = wh - wl
            for f in fib_levels:
                all_fibs.append((wh - move*f) if upt else (wl + move*f))
        if len(all_fibs) < 4: continue
        # Cluster
        sp = sorted(all_fibs)
        clusters = [[sp[0]]]
        for p in sp[1:]:
            cm = sum(clusters[-1]) / len(clusters[-1])
            if abs(p - cm) / cm <= 0.004:
                clusters[-1].append(p)
            else:
                clusters.append([p])
        zones = sorted([(sum(c)/len(c), len(c)) for c in clusters if len(c) >= 2],
                       key=lambda x: -x[1])
        if not zones: continue
        zones.sort(key=lambda z: abs(z[0] - last))
        nearest, count = zones[0]
        if abs(last - nearest)/nearest > 0.006: continue
        # Build score
        score = 0
        # Fib count factor
        if count >= 6: score += 4
        elif count >= 4: score += 3
        elif count >= 3: score += 2
        else: score += 1
        # Freshness — has price visited the zone in last 50 bars?
        recent_lows  = df["low"].iloc[i-50:i]
        recent_highs = df["high"].iloc[i-50:i]
        within_zone = ((recent_lows <= nearest * 1.003) & (recent_highs >= nearest * 0.997)).any()
        if not within_zone: score += 2  # fresh = institutional orders still resting
        # Wick density at level — count bars where wick (high-close OR open-low) reached level
        wick_count = 0
        for j in range(max(0,i-50), i):
            if df["low"].iloc[j] <= nearest * 1.005 and df["close"].iloc[j] > nearest * 1.002:
                wick_count += 1
            elif df["high"].iloc[j] >= nearest * 0.995 and df["close"].iloc[j] < nearest * 0.998:
                wick_count += 1
        if wick_count >= 3: score += 2
        # Volume on test bar
        avg_v = df["volume"].iloc[i-19:i].mean()
        v_ratio = df["volume"].iloc[i] / avg_v if avg_v > 0 else 0
        if v_ratio > 1.5: score += 2
        elif v_ratio > 1.0: score += 1
        # Trade only if score >= 6
        score_bucket = "score_6plus" if score >= 6 else ("score_4-5" if score >= 4 else "score_<4")
        if score < 4: continue   # skip weakest
        side = "long" if last > nearest else "short"
        # In our hot-zone logic: bounce off support / rejection at resistance
        side = "long" if last > nearest else "short"  # nearest zone below = support bounce
        _, ex = simulate(df, i, side, 2.0, 1.0)
        pct = pct_pnl(side, last, ex)
        res[score_bucket]["n"] += 1
        if pct > 0: res[score_bucket]["w"] += 1
        res[score_bucket]["pnl"] += pct
        last_fire = i
    return res

# ============================================================================
# TEST 2 — 0.786 with extra filters
# ============================================================================
def test_786_filters(df):
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    for i in range(250, len(df)-5):
        if i - last_fire < 12: continue
        wh = df["high"].iloc[i-50:i].max()
        wl = df["low"].iloc[i-50:i].min()
        if wh <= wl or (wh-wl)/wl < 0.025: continue
        sh_idx = df["high"].iloc[i-50:i].idxmax()
        sl_idx = df["low"].iloc[i-50:i].idxmin()
        upt = sh_idx > sl_idx
        move = wh - wl
        fp_786 = (wh - move*0.786) if upt else (wl + move*0.786)
        last = df["close"].iloc[i]
        if abs(last - fp_786)/fp_786 >= 0.004: continue
        # Filter A: freshness — not visited in last 50 bars (excluding this bar)
        recent_lows = df["low"].iloc[i-50:i-1]
        recent_highs = df["high"].iloc[i-50:i-1]
        was_visited = ((recent_lows <= fp_786 * 1.003) & (recent_highs >= fp_786 * 0.997)).any()
        # Filter B: EMA200 trend alignment
        e200 = ema(df["close"].iloc[:i+1], 200).iloc[-1]
        if pd.isna(e200): continue
        with_trend = (upt and last > e200) or (not upt and last < e200)
        # Filter C: volume confirmation
        avg_v = df["volume"].iloc[i-19:i].mean()
        v_ratio = df["volume"].iloc[i] / avg_v if avg_v > 0 else 0
        v_ok = v_ratio > 1.3
        # Build setups
        side = "long" if upt else "short"
        # Baseline (no filter)
        _, ex = simulate(df, i, side, 2.5, 1.5)
        pct = pct_pnl(side, last, ex)
        res["786_baseline"]["n"] += 1
        if pct > 0: res["786_baseline"]["w"] += 1
        res["786_baseline"]["pnl"] += pct
        # With freshness
        if not was_visited:
            res["786_fresh"]["n"] += 1
            if pct > 0: res["786_fresh"]["w"] += 1
            res["786_fresh"]["pnl"] += pct
        # With EMA200 trend
        if with_trend:
            res["786_with_trend"]["n"] += 1
            if pct > 0: res["786_with_trend"]["w"] += 1
            res["786_with_trend"]["pnl"] += pct
        # With volume
        if v_ok:
            res["786_volume"]["n"] += 1
            if pct > 0: res["786_volume"]["w"] += 1
            res["786_volume"]["pnl"] += pct
        # All three (TIER-1 setup)
        if not was_visited and with_trend and v_ok:
            res["786_TIER1_all_filters"]["n"] += 1
            if pct > 0: res["786_TIER1_all_filters"]["w"] += 1
            res["786_TIER1_all_filters"]["pnl"] += pct
        last_fire = i
    return res

# ============================================================================
# TEST 3 — Log-scale trend channel
# ============================================================================
def test_log_channel(df):
    """Fit log(price) vs time linearly over 200 bars. When price touches upper=short, lower=long."""
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    for i in range(220, len(df)-5):
        if i - last_fire < 24: continue
        c = df["close"].iloc[i-200:i]
        if (c <= 0).any(): continue
        x = np.arange(200)
        y = np.log(c.values)
        slope, intercept = np.polyfit(x, y, 1)
        pred = slope * x + intercept
        residuals = y - pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - y.mean())**2)
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        if r2 < 0.5: continue   # need real trend
        std = np.std(residuals)
        # Channel = ±1.5 std
        upper_y = slope * 200 + intercept + 1.5 * std
        lower_y = slope * 200 + intercept - 1.5 * std
        upper_p = np.exp(upper_y); lower_p = np.exp(lower_y)
        last = df["close"].iloc[i]
        # Touch detection
        if abs(last - upper_p)/upper_p < 0.005:
            # Top of channel = short
            side = "short"
            _, ex = simulate(df, i, side, 2.0, 1.0)
            pct = pct_pnl(side, last, ex)
            tag = "log_channel_top_short"
            res[tag]["n"] += 1
            if pct > 0: res[tag]["w"] += 1
            res[tag]["pnl"] += pct
            last_fire = i
        elif abs(last - lower_p)/lower_p < 0.005:
            side = "long"
            _, ex = simulate(df, i, side, 2.0, 1.0)
            pct = pct_pnl(side, last, ex)
            tag = "log_channel_bottom_long"
            res[tag]["n"] += 1
            if pct > 0: res[tag]["w"] += 1
            res[tag]["pnl"] += pct
            last_fire = i
    return res

# ============================================================================
# TEST 4 — Wedge patterns
# ============================================================================
def test_wedges(df):
    """Rising wedge (converging up) → short on lower line break.
    Falling wedge (converging down) → long on upper line break."""
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    last_fire = -100
    for i in range(80, len(df)-5):
        if i - last_fire < 24: continue
        # Find swing highs and lows in last 50 bars
        h = df["high"].iloc[i-50:i]; l = df["low"].iloc[i-50:i]
        # Rolling local maxima/minima
        highs = []; lows = []
        for k in range(3, len(h)-3):
            if h.iloc[k] == h.iloc[k-3:k+4].max():
                highs.append((k, h.iloc[k]))
            elif l.iloc[k] == l.iloc[k-3:k+4].min():
                lows.append((k, l.iloc[k]))
        if len(highs) < 3 or len(lows) < 3: continue
        # Fit lines
        hx = np.array([p[0] for p in highs]); hy = np.array([p[1] for p in highs])
        lx = np.array([p[0] for p in lows]);  ly = np.array([p[1] for p in lows])
        h_slope, h_int = np.polyfit(hx, hy, 1)
        l_slope, l_int = np.polyfit(lx, ly, 1)
        # Rising wedge: both slopes positive, but high slope < low slope (converging)
        # Falling wedge: both slopes negative, high slope < low slope (converging up)
        last = df["close"].iloc[i]
        wedge_age_idx = 50  # current position in 50-bar window
        if h_slope > 0 and l_slope > 0 and h_slope < l_slope:
            # Rising wedge — short on break of lower line
            line_lo = l_slope * wedge_age_idx + l_int
            if last < line_lo * 0.998:  # broken below
                side = "short"
                _, ex = simulate(df, i, side, 2.0, 1.0)
                pct = pct_pnl(side, last, ex)
                res["rising_wedge_short"]["n"] += 1
                if pct > 0: res["rising_wedge_short"]["w"] += 1
                res["rising_wedge_short"]["pnl"] += pct
                last_fire = i
        elif h_slope < 0 and l_slope < 0 and h_slope < l_slope:
            # Falling wedge — long on break of upper line
            line_hi = h_slope * wedge_age_idx + h_int
            if last > line_hi * 1.002:  # broken above
                side = "long"
                _, ex = simulate(df, i, side, 2.0, 1.0)
                pct = pct_pnl(side, last, ex)
                res["falling_wedge_long"]["n"] += 1
                if pct > 0: res["falling_wedge_long"]["w"] += 1
                res["falling_wedge_long"]["pnl"] += pct
                last_fire = i
    return res

# ============================================================================
# TEST 5 — Cross-asset Fib confluence (BTC + ETH + SOL together)
# ============================================================================
def test_cross_asset(symbols=["BTC-USDT","ETH-USDT","SOL-USDT"]):
    """When BTC + ETH + SOL are ALL within 0.4% of a 0.618 retracement at the same bar."""
    res = defaultdict(lambda: {"n":0,"w":0,"pnl":0.0})
    dfs = {}
    for s in symbols:
        d = load(s)
        if d is None: return res
        dfs[s] = d
    n_bars = min(len(d) for d in dfs.values())
    last_fire = -100
    for i in range(60, n_bars - 5):
        if i - last_fire < 12: continue
        # For each symbol, check if at 0.618 retrace
        all_at_fib = True
        sides = []
        for s in symbols:
            d = dfs[s]
            wh = d["high"].iloc[i-50:i].max(); wl = d["low"].iloc[i-50:i].min()
            if wh <= wl or (wh-wl)/wl < 0.02: all_at_fib = False; break
            sh_idx = d["high"].iloc[i-50:i].idxmax(); sl_idx = d["low"].iloc[i-50:i].idxmin()
            upt = sh_idx > sl_idx
            fib618 = (wh - (wh-wl)*0.618) if upt else (wl + (wh-wl)*0.618)
            last = d["close"].iloc[i]
            if abs(last - fib618)/fib618 >= 0.004:
                all_at_fib = False; break
            sides.append("long" if upt else "short")
        if not all_at_fib: continue
        if len(set(sides)) > 1: continue   # need agreement on direction
        # Trade BTC
        btc = dfs["BTC-USDT"]
        last_btc = btc["close"].iloc[i]
        side = sides[0]
        _, ex = simulate(btc, i, side, 2.5, 1.5)
        pct = pct_pnl(side, last_btc, ex)
        res["3asset_618_confluence"]["n"] += 1
        if pct > 0: res["3asset_618_confluence"]["w"] += 1
        res["3asset_618_confluence"]["pnl"] += pct
        last_fire = i
    return res

# ============================================================================
# RUN
# ============================================================================
def run():
    g1 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g2 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g3 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    g4 = defaultdict(lambda:{"n":0,"w":0,"pnl":0.0})
    print("Running per-symbol...")
    for sym in SYMBOLS:
        df = load(sym)
        if df is None or len(df) < 300: continue
        for src, tgt in [(test_zone_scoring(df), g1),
                          (test_786_filters(df), g2),
                          (test_log_channel(df), g3),
                          (test_wedges(df), g4)]:
            for k, v in src.items():
                for kk in ("n","w","pnl"):
                    tgt[k][kk] += v[kk]
        print(f"  {sym}: done")
    # Cross-asset is one global test
    print("Running cross-asset...")
    g5 = test_cross_asset()

    def report(title, results):
        print()
        print("="*72)
        print(title)
        print("="*72)
        print(f"{'setup':<32}{'n':>6}{'WR%':>7}{'sum %':>9}{'avg %':>10}{'verdict':>10}")
        print("-"*72)
        for k in sorted(results.keys()):
            d = results[k]
            if d["n"] == 0:
                print(f"  {k:<30} no signals"); continue
            wr = d["w"]/d["n"]*100
            avg = d["pnl"]/d["n"]
            verdict = "✅ EDGE" if avg > 0.05 else ("⚠️ small" if avg > 0 else "❌ losing")
            print(f"  {k:<30}{d['n']:>6}{wr:>6.1f}%{d['pnl']:>+8.1f}%{avg:>+9.3f}%{verdict:>10}")

    report("TEST 1 — MULTI-FACTOR ZONE SCORE (count + freshness + wicks + volume)", g1)
    report("TEST 2 — 0.786 + EXTRA FILTERS", g2)
    report("TEST 3 — LOG-SCALE TREND CHANNELS (200-bar fit, ±1.5σ band)", g3)
    report("TEST 4 — WEDGE PATTERNS (rising→short, falling→long)", g4)
    report("TEST 5 — CROSS-ASSET 0.618 CONFLUENCE (BTC+ETH+SOL together)", g5)

if __name__ == "__main__":
    run()
