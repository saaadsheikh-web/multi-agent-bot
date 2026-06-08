#!/usr/bin/env python3
"""Fast backtest for UTBotMTF v2 (Saad's design + 4 math layers).

Pre-computes UT Bot history ONCE per symbol, then walks bars in O(n).
"""
import os, sys, math, time
from pathlib import Path
from statistics import mean, stdev

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
sys.path.insert(0, str(WORK))

from dotenv import load_dotenv
load_dotenv(WORK / ".env")

import pandas as pd
import numpy as np

from bot import _utbot_full_history, _adaptive_key_value, _realized_vol_annualized

TAKER_FEE = 0.0006
SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "BNB-USDT",
           "DOGE-USDT", "AVAX-USDT", "LINK-USDT"]
DAYS = 365
ATR_PERIOD = 10
MAX_BARS_SINCE_CROSS = 3
MIN_5M_VOL_RATIO = 1.2


def load_parquet(sym, tf):
    p = WORK / "backtest_data" / f"{sym.replace('-', '_')}_{tf}_365d.parquet"
    if not p.exists():
        return None
    return pd.read_parquet(p)


def precompute(df, atr_period: int):
    """Run UT Bot once over the WHOLE series with a fixed mid kv (2.0). Then
    locally we'll use this for `position` lookup. Returns positions array
    (+1/-1 per bar) and stops array.

    For adaptive kv we'd need recomputing per window — too slow. Compromise:
    use kv=2.0 for backtest, accept that adaptive layer 1 isn't fully tested here.
    """
    c = df["close"].values; h = df["high"].values; l = df["low"].values
    _, stops = _utbot_full_history(c, h, l, atr_period, 2.0)
    pos = np.where(c > stops, 1, -1)
    return pos, stops


def bars_since_cross_vec(pos):
    """For each bar, count how many bars ago the position last flipped."""
    out = np.zeros(len(pos), dtype=int)
    cnt = 0
    last = pos[0]
    for i in range(len(pos)):
        if pos[i] != last:
            cnt = 0
            last = pos[i]
        else:
            cnt += 1
        out[i] = cnt
    return out


def simulate(df15, df5):
    trades = []
    pos15, stops15 = precompute(df15, ATR_PERIOD)
    pos5, stops5 = precompute(df5, ATR_PERIOD)
    bsc15 = bars_since_cross_vec(pos15)
    bsc5 = bars_since_cross_vec(pos5)
    ts5 = df5["ts"].values
    ts15 = df15["ts"].values
    closes15 = df15["close"].values
    v5 = df5["volume"].values
    avg_v5 = pd.Series(v5).rolling(20).mean().values
    rolling_log_ret = np.diff(np.log(np.where(closes15 > 0, closes15, 1)))
    open_t = None
    for i in range(80, len(df15) - 1):
        last = closes15[i]
        if last <= 0: continue
        # Find aligned 5m index
        idx5 = int(np.searchsorted(ts5, ts15[i], side="right") - 1)
        if idx5 < 100: continue
        # ── Manage open trade ──
        if open_t:
            sign = 1 if open_t["side"] == "long" else -1
            adv = sign * (last - open_t["entry"]) / open_t["entry"]
            risk = abs(open_t["entry"] - open_t["sl"]) / open_t["entry"]
            if adv > open_t["best"]: open_t["best"] = adv
            stop_hit = (open_t["side"] == "long" and last <= open_t["sl"]) or \
                       (open_t["side"] == "short" and last >= open_t["sl"])
            if stop_hit:
                actual = sign * (open_t["sl"] - open_t["entry"]) / open_t["entry"]
                if risk > 0:
                    r_val = (actual - TAKER_FEE * 2) / risk
                    if np.isfinite(r_val):
                        trades.append(float(r_val))
                open_t = None; continue
            # Breakeven lock + trail
            if open_t["best"] >= 0.005:
                if open_t["side"] == "long":
                    new_sl = max(open_t["entry"], last * (1 - 0.005))
                    if new_sl > open_t["sl"]: open_t["sl"] = new_sl
                else:
                    new_sl = min(open_t["entry"], last * (1 + 0.005))
                    if new_sl < open_t["sl"]: open_t["sl"] = new_sl
            # Both-TF flip exit
            cur15 = pos15[i]; cur5 = pos5[idx5]
            if open_t["side"] == "long" and cur15 < 0 and cur5 < 0:
                actual = sign * (last - open_t["entry"]) / open_t["entry"]
                if risk > 0:
                    r_val = (actual - TAKER_FEE * 2) / risk
                    if np.isfinite(r_val):
                        trades.append(float(r_val))
                open_t = None; continue
            if open_t["side"] == "short" and cur15 > 0 and cur5 > 0:
                actual = sign * (last - open_t["entry"]) / open_t["entry"]
                if risk > 0:
                    r_val = (actual - TAKER_FEE * 2) / risk
                    if np.isfinite(r_val):
                        trades.append(float(r_val))
                open_t = None; continue
            # Max hold
            if i - open_t["open_i"] > 96:
                actual = sign * (last - open_t["entry"]) / open_t["entry"]
                if risk > 0:
                    r_val = (actual - TAKER_FEE * 2) / risk
                    if np.isfinite(r_val):
                        trades.append(float(r_val))
                open_t = None; continue
        if open_t: continue
        # ── Try entry ──
        cur15 = pos15[i]; cur5 = pos5[idx5]
        if cur15 != cur5: continue
        # Fresh cross check
        if bsc15[i] > MAX_BARS_SINCE_CROSS or bsc5[idx5] > MAX_BARS_SINCE_CROSS:
            continue
        # Volume gate
        if avg_v5[idx5] <= 0 or np.isnan(avg_v5[idx5]): continue
        v_ratio = v5[idx5] / avg_v5[idx5]
        if v_ratio < MIN_5M_VOL_RATIO: continue
        # Open trade
        if cur15 > 0:
            sl = last * 0.975
            open_t = {"side": "long", "entry": last, "sl": sl,
                      "open_i": i, "best": 0.0}
        else:
            sl = last * 1.025
            open_t = {"side": "short", "entry": last, "sl": sl,
                      "open_i": i, "best": 0.0}
    return trades


def main():
    t0 = time.time()
    print("=" * 60)
    print(f"  UTBOT-MTF v2 BACKTEST — {DAYS}d, 8 syms, 15m/5m")
    print("=" * 60)
    all_trades = []
    for sym in SYMBOLS:
        df15 = load_parquet(sym, "15m")
        df5 = load_parquet(sym, "5m")
        if df15 is None or df5 is None:
            print(f"  {sym}: NO CACHED DATA"); continue
        ts = simulate(df15, df5)
        all_trades.extend(ts)
        print(f"  {sym:14s}  trades={len(ts):3d}")
    if not all_trades:
        print("\n❌ No trades generated"); return
    # Filter any nan/inf that may have slipped in
    all_trades = [t for t in all_trades if np.isfinite(t)]
    if not all_trades:
        print("\n❌ No valid trades after filtering"); return
    wins = [t for t in all_trades if t > 0]
    losses = [t for t in all_trades if t <= 0]
    wr = len(wins) / len(all_trades) * 100
    expR = float(np.mean(all_trades))
    s = float(np.std(all_trades, ddof=1)) if len(all_trades) > 1 else 0.0
    sharpe = (expR / s * math.sqrt(252)) if s > 0 else 0
    avg_w = mean(wins) if wins else 0
    avg_l = mean(losses) if losses else 0
    eq = []; cum = 0
    for t in all_trades: cum += t; eq.append(cum)
    peak = eq[0]; mdd = 0
    for x in eq:
        peak = max(peak, x); mdd = max(mdd, peak - x)
    print()
    print("=" * 60); print("  RESULTS"); print("=" * 60)
    print(f"  Trades:          {len(all_trades)}")
    print(f"  Win rate:        {wr:.1f}%")
    print(f"  Avg win:         {avg_w:+.2f}R")
    print(f"  Avg loss:        {avg_l:+.2f}R")
    if avg_l: print(f"  R:R realized:    {avg_w/abs(avg_l):.2f}:1")
    print(f"  ExpR per trade:  {expR:+.4f}R")
    print(f"  Sharpe:          {sharpe:.2f}")
    print(f"  Max DD:          {mdd:.2f}R")
    print(f"  Total return:    {sum(all_trades):+.2f}R")
    print(f"  Runtime:         {time.time()-t0:.1f}s")
    print()
    if wr >= 60.0 and len(all_trades) >= 30 and expR > 0:
        print("  🟢 PASS — WR ≥ 60%, deploy at 0.05x")
    elif wr >= 55.0 and expR > 0:
        print("  🟡 OK — close to threshold")
    elif expR > 0:
        print("  🟡 marginal — paper")
    else:
        print("  🔴 NEGATIVE — kill")


if __name__ == "__main__":
    main()
