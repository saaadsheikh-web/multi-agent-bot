#!/usr/bin/env python3
"""
Backtest the agents that matter MOST (post-2026-05-06 changes):
  - connors_rsi2 (proven live winner)
  - fibonacci (with zone_price)
  - fib_hotzone (NEW)
  - williams_r (NEW)

Fees: 0.02% maker per side (post-maker-order-fix).
Period: 90 days of cached 1H candles.
Universe: 12 high-liquidity symbols.

Outputs per-agent stats: trades, WR, profit factor, ExpR, total PnL ($/100 notional).
"""
import os, sys, json, math
import pandas as pd
import numpy as np
from glob import glob

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")

# Post-maker fix
MAKER_FEE = 0.0002
ROUND_TRIP = MAKER_FEE * 2  # 0.04%

NOTIONAL = 100.0

# Test universe — same liquid symbols where we have data
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
           "AVAX-USDT","ADA-USDT","LINK-USDT","TAO-USDT","INJ-USDT",
           "APT-USDT","ARB-USDT"]

DAYS = 90

def load(sym, tf="1H"):
    f = os.path.join(CACHE, f"{sym.replace('-','_')}_{tf}_365d.parquet")
    if not os.path.exists(f):
        return None
    df = pd.read_parquet(f)
    # Normalize columns
    cols = {c.lower(): c for c in df.columns}
    df.columns = [c.lower() for c in df.columns]
    return df.iloc[-DAYS*24:].reset_index(drop=True)

def rsi(series, n=14):
    delta = series.diff()
    up = delta.where(delta > 0, 0).rolling(n).mean()
    dn = (-delta.where(delta < 0, 0)).rolling(n).mean()
    rs = up / dn
    return 100 - 100 / (1 + rs)

def ema(series, n):
    return series.ewm(span=n, adjust=False).mean()

def atr(df, n=14):
    h = df["high"]; l = df["low"]; c = df["close"]
    pc = c.shift(1)
    tr = pd.concat([(h-l).abs(), (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()

# ---------- AGENT IMPLEMENTATIONS (simplified, focused) ----------

def signal_connors_rsi2(df, i):
    """Connors RSI2: when 2-period RSI < 5 in uptrend → long. > 95 in downtrend → short.
    TP 1.8%, SL 1.0%."""
    if i < 100: return None
    c = df["close"]
    r2 = rsi(c.iloc[:i+1], 2).iloc[-1]
    e200 = ema(c.iloc[:i+1], 200).iloc[-1]
    last = c.iloc[i]
    if pd.isna(r2) or pd.isna(e200): return None
    if r2 < 5 and last > e200:
        return ("long", 1.8, 1.0)
    if r2 > 95 and last < e200:
        return ("short", 1.8, 1.0)
    return None

def signal_williams_r(df, i):
    """Williams %R + EMA200 trend filter. <-90 + uptrend → long; >-10 + downtrend → short."""
    if i < 200: return None
    h = df["high"]; l = df["low"]; c = df["close"]
    last = c.iloc[i]
    hh = h.iloc[i-13:i+1].max()
    ll = l.iloc[i-13:i+1].min()
    if hh == ll: return None
    wr = (hh - last) / (hh - ll) * -100
    e200 = ema(c.iloc[:i+1], 200).iloc[-1]
    if pd.isna(e200): return None
    avg_v = df["volume"].iloc[i-19:i+1].mean()
    v_ratio = df["volume"].iloc[i] / avg_v if avg_v > 0 else 0
    if v_ratio < 1.2: return None
    if wr < -90 and last > e200 * 1.005:
        return ("long", 2.0, 1.5)
    if wr > -10 and last < e200 * 0.995:
        return ("short", 2.0, 1.5)
    return None

def signal_fibonacci(df, i):
    """Standard Fib retracement bounce/rejection."""
    if i < 60: return None
    c = df["close"]; h = df["high"]; l = df["low"]
    last = c.iloc[i]
    win_h = h.iloc[i-50:i]
    win_l = l.iloc[i-50:i]
    sh = win_h.max(); sl_ = win_l.min()
    if sh <= sl_: return None
    if (sh - sl_) / sl_ < 0.02: return None
    move = sh - sl_
    sh_idx = win_h.idxmax(); sl_idx = win_l.idxmin()
    uptrend = sh_idx > sl_idx
    fib_levels = [0.382, 0.500, 0.618]
    fib_prices = {f: (sh - move * f) if uptrend else (sl_ + move * f) for f in fib_levels}
    avg_v = df["volume"].iloc[i-19:i+1].mean()
    if avg_v <= 0: return None
    v_ratio = df["volume"].iloc[i] / avg_v
    if v_ratio < 1.2: return None
    r = rsi(c.iloc[:i+1], 14).iloc[-1]
    if pd.isna(r): return None
    at_level = None
    for lvl, p in fib_prices.items():
        if abs(last - p) / p < 0.005:
            at_level = lvl; break
    if at_level is None: return None
    if uptrend and r < 45:
        return ("long", 2.5, 1.5)
    if not uptrend and r > 55:
        return ("short", 2.5, 1.5)
    return None

def signal_fib_hotzone(df, i):
    """Multi-swing Fib confluence. Returns long/short if price within 0.6% of a 2+ confluence zone."""
    if i < 250: return None
    c = df["close"]; h = df["high"]; l = df["low"]
    last = c.iloc[i]
    if last <= 0: return None
    fib_levels = [0.236, 0.382, 0.500, 0.618, 0.786]
    all_fibs = []
    for w in [30, 60, 120, 240]:
        if i < w + 5: continue
        wh = h.iloc[i-w:i].max(); wl = l.iloc[i-w:i].min()
        if wh <= wl or (wh - wl) / wl < 0.015: continue
        sh_idx = h.iloc[i-w:i].idxmax(); sl_idx = l.iloc[i-w:i].idxmin()
        upt = sh_idx > sl_idx
        move = wh - wl
        for f in fib_levels:
            all_fibs.append((wh - move * f) if upt else (wl + move * f))
    if len(all_fibs) < 6: return None
    # Cluster: within 0.4% of cluster mean
    sp = sorted(all_fibs)
    clusters = [[sp[0]]]
    for p in sp[1:]:
        cm = sum(clusters[-1]) / len(clusters[-1])
        if abs(p - cm) / cm <= 0.004:
            clusters[-1].append(p)
        else:
            clusters.append([p])
    zones = sorted([(sum(c)/len(c), len(c)) for c in clusters if len(c) >= 2], key=lambda x: -x[1])
    if not zones: return None
    # Find nearest zone
    zones.sort(key=lambda z: abs(z[0] - last))
    nearest, strength = zones[0]
    dist = (last - nearest) / nearest
    if abs(dist) > 0.006: return None
    avg_v = df["volume"].iloc[i-19:i+1].mean()
    if avg_v <= 0: return None
    v_ratio = df["volume"].iloc[i] / avg_v
    if v_ratio < 1.2: return None
    r = rsi(c.iloc[:i+1], 14).iloc[-1]
    if pd.isna(r): return None
    e50 = ema(c.iloc[:i+1], 50).iloc[-1]
    e50_5 = ema(c.iloc[:i+1], 50).iloc[-5]
    if pd.isna(e50) or pd.isna(e50_5) or e50_5 <= 0: return None
    slope = (e50 / e50_5 - 1) * 100
    if dist > 0 and r < 50 and slope > -0.8:  # long bounce
        return ("long", 2.0, 0.5)
    if dist < 0 and r > 50 and slope < 0.8:   # short rejection
        return ("short", 2.0, 0.5)
    return None

AGENTS = {
    "connors_rsi2":    signal_connors_rsi2,
    "williams_r":      signal_williams_r,
    "fibonacci":       signal_fibonacci,
    "fib_hotzone":     signal_fib_hotzone,
}

def simulate_trade(df, i, side, tp_pct, sl_pct, max_bars=48):
    """Walk forward from bar i+1. Use bar high/low to detect TP/SL hits.
    Returns (exit_idx, exit_price, outcome) or None if neither hit within max_bars."""
    entry = df["close"].iloc[i]
    if side == "long":
        tp_price = entry * (1 + tp_pct/100)
        sl_price = entry * (1 - sl_pct/100)
    else:
        tp_price = entry * (1 - tp_pct/100)
        sl_price = entry * (1 + sl_pct/100)
    end = min(i + max_bars, len(df) - 1)
    for j in range(i+1, end+1):
        bh = df["high"].iloc[j]; bl = df["low"].iloc[j]
        if side == "long":
            # Conservative: SL checked first if both hit in same bar
            if bl <= sl_price:
                return (j, sl_price, "SL")
            if bh >= tp_price:
                return (j, tp_price, "TP")
        else:
            if bh >= sl_price:
                return (j, sl_price, "SL")
            if bl <= tp_price:
                return (j, tp_price, "TP")
    # Time exit at last bar
    return (end, df["close"].iloc[end], "TIME")

def backtest():
    results = {a: {"trades": 0, "wins": 0, "gross_w": 0.0, "gross_l": 0.0, "by_sym": {}} for a in AGENTS}
    for sym in SYMBOLS:
        df = load(sym)
        if df is None or len(df) < 300:
            print(f"  skip {sym}: no data")
            continue
        # cooldown per agent per symbol — don't fire repeated signals on consecutive bars
        last_fire = {a: -100 for a in AGENTS}
        for i in range(250, len(df) - 5):
            for agent_name, sig_fn in AGENTS.items():
                if i - last_fire[agent_name] < 24:  # 24-bar cooldown per agent per symbol
                    continue
                try:
                    sig = sig_fn(df, i)
                except Exception:
                    sig = None
                if sig is None:
                    continue
                side, tp_pct, sl_pct = sig
                outcome = simulate_trade(df, i, side, tp_pct, sl_pct, max_bars=48)
                if outcome is None: continue
                exit_idx, exit_price, why = outcome
                entry = df["close"].iloc[i]
                if side == "long":
                    pct = (exit_price - entry) / entry * 100
                else:
                    pct = (entry - exit_price) / entry * 100
                # Apply fees
                pct -= ROUND_TRIP * 100
                pnl_usd = pct / 100 * NOTIONAL
                r = results[agent_name]
                r["trades"] += 1
                if pnl_usd > 0:
                    r["wins"] += 1
                    r["gross_w"] += pnl_usd
                else:
                    r["gross_l"] += pnl_usd
                r["by_sym"].setdefault(sym, {"n":0, "pnl":0})
                r["by_sym"][sym]["n"] += 1
                r["by_sym"][sym]["pnl"] += pnl_usd
                last_fire[agent_name] = i

    # Report
    print()
    print("="*80)
    print(f"BACKTEST RESULTS — {DAYS} days, {len(SYMBOLS)} symbols, ${NOTIONAL} notional/trade")
    print(f"Fees: {ROUND_TRIP*100:.3f}% round-trip (post-maker-fix)")
    print("="*80)
    print(f"{'agent':<18}{'n':>5}{'WR%':>7}{'PF':>7}{'GrossW':>10}{'GrossL':>10}{'NET':>10}{'avg/tr':>9}")
    print("-"*80)
    overall = {"n":0, "w":0, "gw":0, "gl":0}
    for a in AGENTS:
        r = results[a]
        n = r["trades"]
        if n == 0:
            print(f"{a:<18}{'0':>5}  no signals fired")
            continue
        wr = r["wins"] / n * 100
        pf = (r["gross_w"] / abs(r["gross_l"])) if abs(r["gross_l"]) > 0.001 else 99.0
        net = r["gross_w"] + r["gross_l"]
        avg = net / n
        overall["n"] += n; overall["w"] += r["wins"]
        overall["gw"] += r["gross_w"]; overall["gl"] += r["gross_l"]
        print(f"{a:<18}{n:>5}{wr:>6.1f}%{pf:>7.2f}{r['gross_w']:>+10.2f}{r['gross_l']:>+10.2f}{net:>+10.2f}{avg:>+9.3f}")
    print("-"*80)
    n = overall["n"]; w = overall["w"]
    if n > 0:
        wr_o = w/n*100
        pf_o = overall["gw"]/abs(overall["gl"]) if abs(overall["gl"])>0.001 else 99
        net_o = overall["gw"] + overall["gl"]
        avg_o = net_o / n
        print(f"{'COMBINED':<18}{n:>5}{wr_o:>6.1f}%{pf_o:>7.2f}{overall['gw']:>+10.2f}{overall['gl']:>+10.2f}{net_o:>+10.2f}{avg_o:>+9.3f}")
    print()
    # Per-symbol breakdown for top agents
    print("="*80)
    print("PER-SYMBOL BREAKDOWN — top 3 winners vs losers")
    print("="*80)
    for a in AGENTS:
        if results[a]["trades"] == 0: continue
        sym_data = sorted(results[a]["by_sym"].items(), key=lambda x: -x[1]["pnl"])
        if not sym_data: continue
        print(f"\n  {a}:")
        for sym, d in sym_data[:5]:
            print(f"    {sym:<11} n={d['n']:>3}  PnL ${d['pnl']:>+6.2f}")
    print()

if __name__ == "__main__":
    backtest()
