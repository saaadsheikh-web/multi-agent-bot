#!/usr/bin/env python3
"""
parametric_backtest.py — Backtests every candidate in strategy_pool.json
using the existing backtest.py engine, then writes results back to the pool.

Variants of templates ('breakout', 'capitulation', 'extreme_fade', 'macd')
each map to a generic signal generator that takes parameters at call time.

Run nightly via the hunter. Each backtested config gets:
  status: candidate → backtested
  backtest: { trades, win_rate, expR, sharpe, max_dd_pct, total_pnl }

Strategies that hit the promotion threshold are flagged for Saad to deploy.
"""
import os, sys, json, math, datetime as dt
from pathlib import Path
from statistics import mean, stdev

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
sys.path.insert(0, str(WORK))

POOL = WORK / "strategy_pool.json"
PARAM_BT_LOG = WORK / "parametric_backtest.log"

# Promotion thresholds — strategies above these are flagged ready-to-deploy
PROMOTE_SHARPE = 2.5
PROMOTE_EXPR = 0.15
PROMOTE_MAXDD = 30.0
PROMOTE_TRADES = 50

def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(PARAM_BT_LOG, "a") as f:
        f.write(line + "\n")

def load_pool() -> list:
    if not POOL.exists():
        return []
    return json.loads(POOL.read_text())

def save_pool(pool: list):
    POOL.write_text(json.dumps(pool, indent=2))

def backtest_breakout(p, params: dict, taker_fee: float = 0.0006):
    """Run a generic breakout backtest using the precomputed data on a single symbol.
    Returns trades list."""
    from backtest import _generic_breakout
    trades = []
    if not p.has_1h:
        return trades
    lookback = int(params["lookback_bars"])
    sl_pct = float(params["min_sl_pct"])
    vr = float(params["min_vol_ratio"])
    atr_mult = float(params["atr_mult"])
    if len(p.c1h) < lookback + 30:
        return trades
    open_trade = None
    for i in range(lookback + 30, len(p.c1h) - 1):
        last_px = p.c1h[i]
        if last_px <= 0:
            continue
        # Manage existing trade
        if open_trade:
            sign = 1 if open_trade["side"] == "long" else -1
            adv = sign * (last_px - open_trade["entry"]) / open_trade["entry"]
            risk = abs(open_trade["entry"] - open_trade["sl"]) / open_trade["entry"]
            # SL hit?
            if (open_trade["side"] == "long" and last_px <= open_trade["sl"]) or \
               (open_trade["side"] == "short" and last_px >= open_trade["sl"]):
                r = -1.0 - (taker_fee * 2 / risk if risk > 0 else 0)
                trades.append(r)
                open_trade = None
                continue
            # Trailing exit at +2R favorable
            if adv >= 2 * risk:
                r = (adv - taker_fee * 2) / risk if risk > 0 else 0
                trades.append(r)
                open_trade = None
                continue
            # Max hold (1 week)
            if i - open_trade["open_i"] > 168:
                r = (adv - taker_fee * 2) / risk if risk > 0 else 0
                trades.append(r)
                open_trade = None
                continue
        if open_trade:
            continue
        # Try open
        sig = _generic_breakout(p, i, last_px, lookback, sl_pct, vr, atr_mult, "param")
        if sig is None:
            continue
        _, side, tp, sl, _ = sig
        open_trade = {"side": side, "entry": last_px, "sl": sl, "tp": tp, "open_i": i}
    return trades

def backtest_capitulation(p, params: dict, taker_fee: float = 0.0006):
    trades = []
    if not p.has_1h or len(p.c1h) < 30:
        return trades
    bar_pct = float(params["bar_pct"])
    vr = float(params["min_vol_ratio"])
    rsi_ext = float(params["rsi_extreme"])
    open_trade = None
    for i in range(30, len(p.c1h) - 1):
        last = p.c1h[i]; prev = p.c1h[i - 1]
        if last <= 0 or prev <= 0:
            continue
        if open_trade:
            sign = 1 if open_trade["side"] == "long" else -1
            adv = sign * (last - open_trade["entry"]) / open_trade["entry"]
            risk = abs(open_trade["entry"] - open_trade["sl"]) / open_trade["entry"]
            if (open_trade["side"] == "long" and last <= open_trade["sl"]) or \
               (open_trade["side"] == "short" and last >= open_trade["sl"]):
                trades.append(-1.0 - taker_fee * 2 / risk if risk > 0 else -1.0)
                open_trade = None
                continue
            if (open_trade["side"] == "long" and last >= open_trade["tp"]) or \
               (open_trade["side"] == "short" and last <= open_trade["tp"]):
                trades.append((adv - taker_fee * 2) / risk if risk > 0 else 0)
                open_trade = None
                continue
            if i - open_trade["open_i"] > 12:   # 12-hour max hold
                trades.append((adv - taker_fee * 2) / risk if risk > 0 else 0)
                open_trade = None
                continue
        if open_trade:
            continue
        chg = (last - prev) / prev
        if abs(chg) < bar_pct:
            continue
        avg_v = p.avg_v1h[i]
        if avg_v <= 0:
            continue
        v_ratio = p.v1h[i] / avg_v
        if v_ratio < vr:
            continue
        r = p.rsi1h[i]
        if chg < -bar_pct and r < rsi_ext:
            sl = last * 0.985; tp = last * 1.015
            open_trade = {"side": "long", "entry": last, "sl": sl, "tp": tp, "open_i": i}
        elif chg > bar_pct and r > (100 - rsi_ext):
            sl = last * 1.015; tp = last * 0.985
            open_trade = {"side": "short", "entry": last, "sl": sl, "tp": tp, "open_i": i}
    return trades

def stats(trades: list) -> dict:
    if not trades:
        return {"trades": 0, "win_rate": 0.0, "expR": 0.0, "sharpe": 0.0,
                "max_dd_pct": 0.0, "total_R": 0.0}
    wins = [t for t in trades if t > 0]
    win_rate = len(wins) / len(trades) * 100
    expR = mean(trades)
    s = stdev(trades) if len(trades) > 1 else 0.0
    sharpe = (expR / s * math.sqrt(252)) if s > 0 else 0.0
    # equity curve in R
    eq = []; cum = 0
    for t in trades:
        cum += t
        eq.append(cum)
    peak = eq[0]; max_dd = 0
    for x in eq:
        peak = max(peak, x)
        dd = peak - x
        max_dd = max(max_dd, dd)
    return {
        "trades": len(trades),
        "win_rate": round(win_rate, 1),
        "expR": round(expR, 4),
        "sharpe": round(sharpe, 2),
        "max_dd_pct": round(max_dd, 2),
        "total_R": round(sum(trades), 2),
    }

def main(days: int = 365):
    log(f"=== parametric_backtest.py start  days={days}  ===")
    pool = load_pool()
    if not pool:
        log("pool empty, nothing to do")
        return
    pending = [c for c in pool if c["status"] == "candidate"]
    log(f"pool size: {len(pool)}, pending candidates: {len(pending)}")
    if not pending:
        return
    # Read cached parquet files directly (no network needed)
    from backtest import DEFAULT_UNIVERSE, PrecomputedData
    import pandas as pd
    universe = DEFAULT_UNIVERSE
    cache_dir = WORK / "backtest_data"

    def load_cached(sym, bar, days):
        path = cache_dir / f"{sym.replace('-','_')}_{bar}_{days}d.parquet"
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path)

    promoted = []
    for cand in pending:
        all_trades = []
        for sym in universe:
            try:
                df5  = load_cached(sym, "5m", days)
                df15 = load_cached(sym, "15m", days)
                df1h = load_cached(sym, "1H", days)
                if df5.empty or df15.empty or df1h.empty:
                    continue
                p = PrecomputedData(df5, df15, df1h)
            except Exception as e:
                log(f"  data fail {sym}: {e}")
                continue
            try:
                if cand["template"] == "breakout":
                    t = backtest_breakout(p, cand["params"])
                elif cand["template"] == "capitulation":
                    t = backtest_capitulation(p, cand["params"])
                else:
                    t = []   # extreme_fade & macd backtester not implemented yet
                all_trades.extend(t)
            except Exception as e:
                log(f"  bt fail {sym} {cand['name']}: {e}")
        s = stats(all_trades)
        cand["backtest"] = s
        cand["status"] = "backtested"
        if (s["sharpe"] >= PROMOTE_SHARPE and s["expR"] >= PROMOTE_EXPR
                and s["max_dd_pct"] <= PROMOTE_MAXDD and s["trades"] >= PROMOTE_TRADES):
            cand["recommended"] = True
            promoted.append(cand)
            log(f"  ★ PROMOTE  {cand['name']}  Sharpe={s['sharpe']}  ExpR={s['expR']}R  trades={s['trades']}")
        else:
            log(f"    {cand['name']}  Sharpe={s['sharpe']}  ExpR={s['expR']}R  trades={s['trades']}")

    save_pool(pool)
    log(f"done. promoted: {len(promoted)} / {len(pending)} candidates")
    return promoted

if __name__ == "__main__":
    days = 365
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            pass
    main(days)
