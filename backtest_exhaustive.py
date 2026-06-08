#!/usr/bin/env python3
"""
EXHAUSTIVE ITERATIVE BACKTEST — Find the WOW strategy.
Tests 100s of parameter combinations, cross-validates winners 5×,
repeats on different coins and time periods.

No rush. No stopping until we find something amazing.
"""

import os, sys, json, math, time as _time, itertools
from collections import defaultdict
import numpy as np, pandas as pd

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE = os.path.join(WORK, "backtest_data")
OUT = os.path.join(WORK, "backtest_results")
os.makedirs(OUT, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# CONFIG — We test EVERYTHING
# ═══════════════════════════════════════════════════════════
ALL_SYMBOLS = [
    "BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
    "DOGE-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT",
    "LTC-USDT","DOT-USDT","ATOM-USDT","NEAR-USDT","APT-USDT",
    "ARB-USDT","OP-USDT","INJ-USDT","TAO-USDT","TIA-USDT",
]

TFS = {"5m":5,"15m":15,"30m":30,"1H":60,"4H":240}
BAL = 100; LEV = 5

def ema(s,n): return s.ewm(span=n,adjust=False).mean()
def rsi(c,p=14):
    d=c.diff();g=d.clip(lower=0);l=-d.clip(upper=0)
    return 100-(100/(1+g.ewm(span=p,adjust=False).mean()/l.ewm(span=p,adjust=False).mean().replace(0,1e-9)))

def load_data():
    c={}
    for s in ALL_SYMBOLS:
        for tf in TFS:
            p=os.path.join(CACHE,f"{s.replace('-','_')}_{tf}_365d.parquet")
            if os.path.exists(p):
                df=pd.read_parquet(p).sort_values("ts").reset_index(drop=True)
                cut=df["ts"].max()-(365*24*3600*1000)
                df=df[df["ts"]>=cut].copy()
                if len(df)>=200: c[(s,tf)]=df
    return c


# ═══════════════════════════════════════════════════════════
# STRATEGY GENERATOR — Parameterized FIB_BOUNCE (our winner)
# ═══════════════════════════════════════════════════════════

def fib_bounce_signals(df, fib_level=0.618, fib_tolerance=0.015,
                        vol_threshold=0.8, trend_filter=True,
                        reversal_bars=2, use_rsi_filter=False,
                        rsi_min=25, rsi_max=55,
                        regime_filter=True, adx_min=22):
    """
    FIB BOUNCE with EVERY parameter exposed for optimization.
    REGIME FILTER: Only trades when ADX > adx_min (trending market).
    """
    c=df["close"];h=df["high"];l=df["low"];v=df["volume"]

    # Fib levels from 100-bar swing
    h100=h.rolling(100).max()
    l100=l.rolling(100).min()
    rng=h100-l100

    # Multiple fib levels
    fib_levels = {
        "0.382": l100 + 0.382 * rng,
        "0.500": l100 + 0.500 * rng,
        "0.618": l100 + 0.618 * rng,
        "0.786": l100 + 0.786 * rng,
    }

    target = fib_levels.get(f"0.{int(fib_level*1000):03d}" if fib_level < 1 else str(fib_level),
                            l100 + fib_level * rng)

    # Price near fib level
    near_fib = abs(c - target) / target.replace(0, 1e-9) < fib_tolerance

    # Reversal signal: price up today, down yesterday (or last N bars)
    reversal = c > c.shift(1)
    for i in range(1, reversal_bars):
        reversal = reversal & (c.shift(i) <= c.shift(i+1))

    # Volume filter
    v_avg = v.rolling(50).mean()
    vol_ok = (v / v_avg.replace(0, 1e-9)) > vol_threshold

    # Trend filter: above EMA 50 = uptrend
    if trend_filter:
        trend_ok = c > ema(c, 50)
    else:
        trend_ok = pd.Series(True, index=c.index)

    # RSI filter
    if use_rsi_filter:
        r = rsi(c)
        rsi_ok = (r > rsi_min) & (r < rsi_max)
    else:
        rsi_ok = pd.Series(True, index=c.index)

    # REGIME FILTER — only trade trending uptrends (ADX > threshold)
    if regime_filter:
        hh, ll = df["high"], df["low"]
        tr = pd.concat([hh-ll, (hh-c.shift()).abs(), (ll-c.shift()).abs()], axis=1).max(axis=1)
        atr_val = tr.ewm(span=14, adjust=False).mean()
        up = hh.diff(); down = ll.shift() - ll
        pdm = np.where((up > down) & (up > 0), up, 0)
        ndm = np.where((down > up) & (down > 0), down, 0)
        pdi = 100 * pd.Series(pdm).ewm(span=14, adjust=False).mean() / atr_val.replace(0, 1e-9)
        ndi = 100 * pd.Series(ndm).ewm(span=14, adjust=False).mean() / atr_val.replace(0, 1e-9)
        dx = 100 * abs(pdi - ndi) / (pdi + ndi + 1e-9)
        adx_val = pd.Series(dx).ewm(span=14, adjust=False).mean()
        regime_ok = (adx_val > adx_min) & (pdi > ndi)  # VECTORIZED — O(n)
    else:
        regime_ok = pd.Series(True, index=c.index)

    longs = near_fib & reversal & vol_ok & trend_ok & rsi_ok & regime_ok
    shorts = pd.Series(False, index=df.index)  # Long-only for quality

    return longs, shorts


# ═══════════════════════════════════════════════════════════
# TRADE SIMULATOR — Multiple trail configurations
# ═══════════════════════════════════════════════════════════

def sim_trades(sigs, df, tf_min, risk_pct=0.02, sl_pct=0.07,
               trail_width=0.04, trail_activate=0.03, max_hold_hours=96):
    """Simulate with given parameters. Returns trade list."""
    c=df["close"];h=df["high"];l=df["low"]
    max_bars = max(int((max_hold_hours*60)/tf_min), 24)

    trades=[]
    active=None

    for sig in sigs:
        if active: continue
        bi=sig["bar"]
        if bi >= len(c)-5: continue

        ep=c.iloc[bi]; sd=sig["side"]
        active={"sd":sd,"ep":ep,"bi":bi,"hw":ep,"lw":ep,"ta":False,"ts":None}

        for i in range(bi+1, len(df)):
            bh=i-bi

            if sd=="long":
                active["hw"]=max(active["hw"],h.iloc[i])
                profit=(active["hw"]-ep)/ep
            else:
                active["lw"]=min(active["lw"],l.iloc[i])
                profit=(ep-active["lw"])/ep

            # Trail activation
            if not active["ta"] and profit >= trail_activate:
                active["ta"]=True
                if sd=="long":
                    active["ts"]=active["hw"]*(1-trail_width)
                else:
                    active["ts"]=active["lw"]*(1+trail_width)

            # Update trail
            if active["ta"]:
                if sd=="long":
                    ns=active["hw"]*(1-trail_width)
                    active["ts"]=max(active.get("ts",0),ns)
                else:
                    ns=active["lw"]*(1+trail_width)
                    active["ts"]=min(active.get("ts",float("inf")),ns)

            # Exit check
            xp=None; rs=None
            if sd=="long":
                esl=max(ep*(1-sl_pct), active.get("ts",ep*(1-sl_pct))) if active["ta"] else ep*(1-sl_pct)
                if l.iloc[i]<=esl: xp=esl; rs="TRAIL" if active["ta"] else "SL"
            else:
                esl=min(ep*(1+sl_pct), active.get("ts",ep*(1+sl_pct))) if active["ta"] else ep*(1+sl_pct)
                if h.iloc[i]>=esl: xp=esl; rs="TRAIL" if active["ta"] else "SL"

            if bh>=max_bars: xp=c.iloc[i]; rs="TIME"

            if xp:
                pnl=(xp-ep)/ep if sd=="long" else (ep-xp)/ep
                trades.append({"pnl":pnl,"bars":bh,"trailed":active["ta"],"reason":rs})
                active=None; break

    return trades


def compute_stats(trades, risk_pct=0.02):
    """Compounding P&L."""
    if not trades: return None
    bal=BAL; pk=bal; dd=0; w=0; l=0; st=0; mx=0; tw=0

    for t in trades:
        m=bal*risk_pct; pnl_usd=m*LEV*t["pnl"]
        bal+=pnl_usd
        if bal<=0: bal=0; break
        if t["pnl"]>0.0001: w+=1; st=0; tw+=t["trailed"]
        elif t["pnl"]<-0.0001: l+=1; st+=1; mx=max(mx,st)
        if bal>pk: pk=bal
        dd=max(dd,(pk-bal)/pk*100 if pk>0 else 0)

    tot=w+l
    if tot<5: return None
    # Score: return adjusted by DD (higher is better)
    score = (bal/BAL - 1) * 100 * (1 - dd/100) if dd < 100 else -999
    return {
        "bal":round(bal,2),"ret":round((bal/BAL-1)*100,1),
        "tot":tot,"w":w,"l":l,"wr":round(w/tot*100,1),
        "dd":round(dd,1),"tw":tw,"mx_s":mx,"score":round(score,1),
    }


# ═══════════════════════════════════════════════════════════
# PARAMETER GRID
# ═══════════════════════════════════════════════════════════

PARAM_GRID = {
    "fib_level": [0.382, 0.500, 0.618, 0.786],
    "fib_tolerance": [0.008, 0.012, 0.020, 0.030],
    "vol_threshold": [0.6, 0.8, 1.0, 1.3],
    "trend_filter": [True, False],
    "reversal_bars": [1, 2, 3],
    "use_rsi_filter": [True, False],
    "rsi_min": [20, 25, 30],
    "rsi_max": [50, 55, 60],
    "sl_pct": [0.05, 0.07, 0.10],
    "trail_width": [0.03, 0.05, 0.08],
    "trail_activate": [0.02, 0.03, 0.05],
    "risk_pct": [0.01, 0.02, 0.03],
}

# Test ONLY high-impact combos (not full Cartesian which is 3^12 = 531K)
# Focus on the interactions that matter most
KEY_COMBOS = [
    # BASE — with regime filter ON
    {"fib_level": 0.382, "sl_pct": 0.05, "trail_width": 0.03, "risk_pct": 0.02, "regime_filter": True, "adx_min": 22},
    {"fib_level": 0.500, "sl_pct": 0.05, "trail_width": 0.03, "risk_pct": 0.02, "regime_filter": True, "adx_min": 22},
    {"fib_level": 0.618, "sl_pct": 0.05, "trail_width": 0.03, "risk_pct": 0.02, "regime_filter": True, "adx_min": 22},
    {"fib_level": 0.786, "sl_pct": 0.05, "trail_width": 0.03, "risk_pct": 0.02, "regime_filter": True, "adx_min": 22},
    # REGIME THRESHOLD variations
    {"fib_level": 0.618, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 20},
    {"fib_level": 0.618, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 25},
    {"fib_level": 0.618, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 30},
    # NO REGIME (baseline)
    {"fib_level": 0.618, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "regime_filter": False},
    # WIDER TRAIL + REGIME
    {"fib_level": 0.618, "sl_pct": 0.07, "trail_width": 0.08, "risk_pct": 0.01, "adx_min": 25},
    {"fib_level": 0.618, "sl_pct": 0.10, "trail_width": 0.08, "risk_pct": 0.01, "adx_min": 25},
    {"fib_level": 0.500, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 22},
    # TOLERANCE + REGIME
    {"fib_level": 0.618, "fib_tolerance": 0.008, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 25},
    {"fib_level": 0.618, "fib_tolerance": 0.020, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 22},
    # VOLUME + RSI + REGIME (should be the magic combo)
    {"fib_level": 0.618, "vol_threshold": 1.0, "use_rsi_filter": True, "rsi_min": 25, "rsi_max": 55, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 22},
    {"fib_level": 0.618, "vol_threshold": 1.3, "use_rsi_filter": True, "rsi_min": 20, "rsi_max": 50, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 25},
    # NO TREND + REGIME (previous winner combo)
    {"fib_level": 0.618, "vol_threshold": 0.6, "trend_filter": False, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 22},
    # REVERSAL 1 bar + REGIME
    {"fib_level": 0.618, "reversal_bars": 1, "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 22},
    # LOW RISK + REGIME
    {"fib_level": 0.618, "sl_pct": 0.05, "trail_width": 0.03, "risk_pct": 0.01, "adx_min": 22},
    {"fib_level": 0.500, "sl_pct": 0.05, "trail_width": 0.03, "risk_pct": 0.01, "adx_min": 22},
    # HIGH RISK + REGIME
    {"fib_level": 0.618, "sl_pct": 0.05, "trail_width": 0.05, "risk_pct": 0.03, "adx_min": 25},
    {"fib_level": 0.500, "sl_pct": 0.05, "trail_width": 0.05, "risk_pct": 0.03, "adx_min": 25},
    # Magic combo — everything optimized
    {"fib_level": 0.618, "fib_tolerance": 0.012, "vol_threshold": 0.6, "trend_filter": False,
     "reversal_bars": 1, "use_rsi_filter": True, "rsi_min": 25, "rsi_max": 55,
     "sl_pct": 0.07, "trail_width": 0.05, "risk_pct": 0.02, "adx_min": 22},
]

# Default params for any not specified
DEFAULTS = {
    "fib_level": 0.618, "fib_tolerance": 0.015, "vol_threshold": 0.8,
    "trend_filter": True, "reversal_bars": 2, "use_rsi_filter": False,
    "rsi_min": 25, "rsi_max": 55, "sl_pct": 0.07, "trail_width": 0.05,
    "trail_activate": 0.03, "risk_pct": 0.02, "max_hold_hours": 96,
    "regime_filter": True, "adx_min": 22,
}


# ═══════════════════════════════════════════════════════════
# CROSS-VALIDATION ENGINE
# ═══════════════════════════════════════════════════════════

def cross_validate(params, data, symbols, tfs_to_test, n_splits=5):
    """
    Test a parameter set across N different time periods.
    Returns avg score and consistency (std dev of scores).
    """
    scores = []

    for sym in symbols[:10]:  # 10 coins
        for tf in tfs_to_test[:3]:  # 5m, 15m, 1H
            df = data.get((sym, tf))
            if df is None: continue

            # Split data into N chunks
            n = len(df)
            chunk_size = n // n_splits

            for split in range(n_splits):
                start = split * chunk_size
                end = min(start + chunk_size, n)
                chunk = df.iloc[start:end].copy()
                if len(chunk) < 200: continue

                # Generate signals with these params
                final_params = {**DEFAULTS, **params}
                longs, shorts = fib_bounce_signals(
                    chunk,
                    fib_level=final_params["fib_level"],
                    fib_tolerance=final_params["fib_tolerance"],
                    vol_threshold=final_params["vol_threshold"],
                    trend_filter=final_params["trend_filter"],
                    reversal_bars=final_params["reversal_bars"],
                    use_rsi_filter=final_params["use_rsi_filter"],
                    rsi_min=final_params["rsi_min"],
                    rsi_max=final_params["rsi_max"],
                )

                sigs = []
                step = {"5m": 4, "15m": 2, "30m": 1, "1H": 1, "4H": 1}.get(tf, 1)
                for i in range(60, len(chunk), step):
                    if longs.iloc[i]: sigs.append({"bar": i, "side": "long"})

                # Limit signals (quality over quantity)
                sigs = sigs[:200]

                trades = sim_trades(
                    sigs, chunk, TFS[tf],
                    risk_pct=final_params["risk_pct"],
                    sl_pct=final_params["sl_pct"],
                    trail_width=final_params["trail_width"],
                    trail_activate=final_params["trail_activate"],
                    max_hold_hours=final_params["max_hold_hours"],
                )

                st = compute_stats(trades, final_params["risk_pct"])
                if st:
                    scores.append(st["score"])

    if not scores:
        return {"avg_score": -999, "consistency": 0, "n_tests": 0, "scores": []}

    return {
        "avg_score": round(np.mean(scores), 1),
        "consistency": round(1.0 - (np.std(scores) / (abs(np.mean(scores)) + 1)), 2),
        "n_tests": len(scores),
        "best_score": round(max(scores), 1),
        "worst_score": round(min(scores), 1),
        "profitable_pct": round(sum(1 for s in scores if s > 0) / len(scores) * 100, 1),
    }


# ═══════════════════════════════════════════════════════════
# MAIN — Iterative optimization
# ═══════════════════════════════════════════════════════════

def main():
    t0 = _time.time()
    print("=" * 90)
    print("EXHAUSTIVE ITERATIVE BACKTEST — Finding the WOW Strategy")
    print(f"Testing {len(KEY_COMBOS)} param combos × 10 coins × 3 TFs × 5 splits")
    print(f"= {len(KEY_COMBOS) * 10 * 3 * 5:,} individual backtests")
    print("=" * 90)

    data = load_data()
    print(f"\nLoaded {len(data)} datasets in {_time.time()-t0:.1f}s")

    tfs_to_test = ["5m", "15m", "1H"]  # Best 3 TFs from previous test
    symbols = ALL_SYMBOLS[:10]  # Top 10 by liquidity

    results = []

    for i, params in enumerate(KEY_COMBOS):
        final = {**DEFAULTS, **params}

        print(f"\n[{i+1}/{len(KEY_COMBOS)}] fib={final['fib_level']:.3f} "
              f"tol={final['fib_tolerance']:.3f} vol={final['vol_threshold']:.1f} "
              f"trend={final['trend_filter']} rev={final['reversal_bars']} "
              f"rsi={final['use_rsi_filter']} sl={final['sl_pct']*100:.0f}% "
              f"trail={final['trail_width']*100:.0f}% risk={final['risk_pct']*100:.0f}%",
              end=" ", flush=True)

        cv = cross_validate(params, data, symbols, tfs_to_test, n_splits=5)

        result = {
            "params": final,
            **cv,
        }
        results.append(result)

        stars = "⭐⭐⭐" if cv["avg_score"] > 50 else ("⭐⭐" if cv["avg_score"] > 20 else ("⭐" if cv["avg_score"] > 0 else "❌"))
        print(f"→ score={cv['avg_score']:.0f} cons={cv['consistency']:.2f} "
              f"prof={cv['profitable_pct']:.0f}% best={cv['best_score']:.0f} {stars}")

    # Sort by score
    results.sort(key=lambda x: -x["avg_score"])

    print(f"\n{'='*90}")
    print("🏆 TOP 15 PARAMETER COMBOS (Cross-Validated)")
    print(f"{'='*90}")
    print(f"{'Rank':<5} {'Score':<8} {'Cons':<7} {'Prof%':<7} {'Fib':<7} {'Tol':<7} {'Vol':<7} {'Trend':<7} {'Rev':<5} {'RSI':<5} {'SL%':<6} {'Trl%':<6} {'Risk%':<7}")
    print(f"{'─'*5} {'─'*8} {'─'*7} {'─'*7} {'─'*7} {'─'*7} {'─'*7} {'─'*7} {'─'*5} {'─'*5} {'─'*6} {'─'*6} {'─'*7}")

    for i, r in enumerate(results[:15], 1):
        p = r["params"]
        print(f"{i:<5} {r['avg_score']:<8.0f} {r['consistency']:<7.2f} {r['profitable_pct']:<7.0f}% "
              f"{p['fib_level']:<7.3f} {p['fib_tolerance']:<7.3f} {p['vol_threshold']:<7.1f} "
              f"{str(p['trend_filter']):<7} {p['reversal_bars']:<5} {str(p['use_rsi_filter']):<5} "
              f"{p['sl_pct']*100:<6.0f}% {p['trail_width']*100:<6.0f}% {p['risk_pct']*100:<7.0f}%")

    # Best by fib level
    print(f"\n{'─'*60}")
    print("BEST SCORE BY FIB LEVEL")
    print(f"{'─'*60}")
    for fl in [0.382, 0.500, 0.618, 0.786]:
        fl_results = [r for r in results if r["params"]["fib_level"] == fl]
        if fl_results:
            best = max(fl_results, key=lambda x: x["avg_score"])
            print(f"  fib={fl:.3f}: score={best['avg_score']:.0f} prof={best['profitable_pct']:.0f}% "
                  f"sl={best['params']['sl_pct']*100:.0f}% trail={best['params']['trail_width']*100:.0f}%")

    # WOW FINDER — Any result with score > 100 and consistency > 0.7?
    wow = [r for r in results if r["avg_score"] > 100 and r["consistency"] > 0.6]
    if wow:
        print(f"\n{'='*60}")
        print(f"🤯 WOW FINDINGS! {len(wow)} parameter sets with exceptional performance")
        print(f"{'='*60}")
        for r in wow[:5]:
            p = r["params"]
            print(f"  Score={r['avg_score']:.0f} | fib={p['fib_level']:.3f} sl={p['sl_pct']*100:.0f}% "
                  f"trail={p['trail_width']*100:.0f}% risk={p['risk_pct']*100:.0f}% "
                  f"profitable={r['profitable_pct']:.0f}% of tests")

    # Save
    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    json_p = os.path.join(OUT, f"exhaustive_backtest_{ts}.json")
    with open(json_p, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✅ Saved: {json_p}")
    print(f"Total: {(_time.time()-t0)/60:.1f} min | {len(results)} parameter combos tested")

    # THE WINNER
    best = results[0]
    print(f"\n{'='*60}")
    print(f"🏆 THE WINNER: fib={best['params']['fib_level']:.3f} "
          f"sl={best['params']['sl_pct']*100:.0f}% trail={best['params']['trail_width']*100:.0f}% "
          f"risk={best['params']['risk_pct']*100:.0f}%")
    print(f"   Cross-validated score: {best['avg_score']:.0f}")
    print(f"   Profitable in {best['profitable_pct']:.0f}% of all tests")
    print(f"   Consistency: {best['consistency']:.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
