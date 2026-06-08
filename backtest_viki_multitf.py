#!/usr/bin/env python3
"""Backtest Viki across multiple timeframes — 5m, 15m, 30m, 1h"""

import os, sys
import numpy as np
import pandas as pd

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")

UNIVERSE = ["SOL-USDT", "TAO-USDT", "TIA-USDT"]

DAYS = 365
STARTING_BALANCE = 100.0
LEVERAGE = 10
RISK_FRACTION = 0.10
SL_PCT = 0.07
TRAIL_ACTIVATE = 0.03
TRAIL_DISTANCE = 0.015


def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def simulate_trades(df, symbol, tf_minutes):
    if len(df) < 60:
        return []
    c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]; ts = df["ts"]
    e9 = ema(c, 9); e21 = ema(c, 21); e50 = ema(c, 50)

    # MAX_HOLD_BARS: 4 days worth of bars at this timeframe
    max_hold_bars = int((4 * 24 * 60) / tf_minutes)

    trades = []
    in_trade = None

    for i in range(52, len(df)):
        if any(pd.isna(x) for x in [e9.iloc[i], e21.iloc[i], e50.iloc[i],
                                     e9.iloc[i-1], e21.iloc[i-1]]):
            continue
        if c.iloc[i] <= 0:
            continue

        vol_ok = v.iloc[i] > 0 and not pd.isna(v.iloc[i])
        avg_v = v.iloc[i-20:i].mean() if i >= 20 else v.iloc[:i].mean()
        v_ratio = v.iloc[i] / avg_v if avg_v > 0 else 0
        vol_filter = v_ratio >= 0.8

        prev_diff = e9.iloc[i-1] - e21.iloc[i-1]
        cur_diff = e9.iloc[i] - e21.iloc[i]
        bullish_x = prev_diff <= 0 and cur_diff > 0
        bearish_x = prev_diff >= 0 and cur_diff < 0
        e50_now = e50.iloc[i]
        entry_price = c.iloc[i]

        # Exit check
        if in_trade:
            side = in_trade["side"]
            bars_held = i - in_trade["entry_bar"]

            if side == "long":
                in_trade["high_water"] = max(in_trade["high_water"], h.iloc[i])
            else:
                in_trade["low_water"] = min(in_trade["low_water"], l.iloc[i])

            if not in_trade["trail_active"]:
                if side == "long":
                    profit_pct = (in_trade["high_water"] - in_trade["entry"]) / in_trade["entry"]
                    if profit_pct >= TRAIL_ACTIVATE:
                        in_trade["trail_active"] = True
                        in_trade["trail_stop"] = in_trade["high_water"] * (1 - TRAIL_DISTANCE)
                else:
                    profit_pct = (in_trade["entry"] - in_trade["low_water"]) / in_trade["entry"]
                    if profit_pct >= TRAIL_ACTIVATE:
                        in_trade["trail_active"] = True
                        in_trade["trail_stop"] = in_trade["low_water"] * (1 + TRAIL_DISTANCE)

            if in_trade["trail_active"]:
                if side == "long":
                    new_stop = in_trade["high_water"] * (1 - TRAIL_DISTANCE)
                    in_trade["trail_stop"] = max(in_trade["trail_stop"], new_stop)
                else:
                    new_stop = in_trade["low_water"] * (1 + TRAIL_DISTANCE)
                    in_trade["trail_stop"] = min(in_trade["trail_stop"], new_stop)

            if side == "long":
                hard_sl = in_trade["entry"] * (1 - SL_PCT)
                effective_sl = max(hard_sl, in_trade.get("trail_stop", hard_sl))
            else:
                hard_sl = in_trade["entry"] * (1 + SL_PCT)
                effective_sl = min(hard_sl, in_trade.get("trail_stop", hard_sl))

            exit_price = None; exit_reason = None

            if side == "long" and l.iloc[i] <= effective_sl:
                exit_price = effective_sl
                exit_reason = "TRAIL_STOP" if in_trade.get("trail_active") else "SL_HIT"
            elif side == "short" and h.iloc[i] >= effective_sl:
                exit_price = effective_sl
                exit_reason = "TRAIL_STOP" if in_trade.get("trail_active") else "SL_HIT"

            if bars_held >= max_hold_bars:
                exit_price = c.iloc[i]; exit_reason = "TIMEOUT"

            if exit_price is not None:
                e = in_trade["entry"]; s = in_trade["side"]
                pnl_pct = (exit_price - e) / e if s == "long" else (e - exit_price) / e
                trades.append({
                    "symbol": symbol, "side": s, "entry": e, "exit": exit_price,
                    "pnl_pct": pnl_pct, "exit_reason": exit_reason,
                    "entry_bar": in_trade["entry_bar"], "exit_bar": i,
                    "bars_held": bars_held, "trailed": in_trade.get("trail_active", False),
                    "high_w": in_trade.get("high_water", e),
                    "low_w": in_trade.get("low_water", e),
                    "entry_time": ts.iloc[in_trade["entry_bar"]],
                    "exit_time": ts.iloc[i],
                })
                in_trade = None
                continue

        # Entry check
        if in_trade is None and vol_filter:
            if bullish_x and e9.iloc[i] > e50_now and e21.iloc[i] > e50_now:
                in_trade = {"side": "long", "entry": entry_price, "entry_bar": i,
                            "high_water": entry_price, "low_water": entry_price,
                            "trail_active": False, "trail_stop": entry_price * (1 - SL_PCT)}
            elif bearish_x and e9.iloc[i] < e50_now and e21.iloc[i] < e50_now:
                in_trade = {"side": "short", "entry": entry_price, "entry_bar": i,
                            "high_water": entry_price, "low_water": entry_price,
                            "trail_active": False, "trail_stop": entry_price * (1 + SL_PCT)}

    if in_trade:
        e = in_trade["entry"]; s = in_trade["side"]; xp = c.iloc[-1]
        pnl_pct = (xp - e) / e if s == "long" else (e - xp) / e
        trades.append({
            "symbol": symbol, "side": s, "entry": e, "exit": xp,
            "pnl_pct": pnl_pct, "exit_reason": "EOD_FORCED",
            "entry_bar": in_trade["entry_bar"], "exit_bar": len(df) - 1,
            "bars_held": len(df) - 1 - in_trade["entry_bar"],
            "trailed": in_trade.get("trail_active", False),
            "high_w": in_trade.get("high_water", e),
            "low_w": in_trade.get("low_water", e),
            "entry_time": ts.iloc[in_trade["entry_bar"]],
            "exit_time": ts.iloc[-1],
        })
    return trades


def run_tf(tf_label, tf_minutes, filenames=None):
    """Run backtest for a given timeframe across all symbols with data."""
    all_raw = []
    for sym in UNIVERSE:
        if filenames:
            fname = filenames.get(sym)
            if not fname:
                continue
            path = os.path.join(CACHE_DIR, fname)
        else:
            # Standard naming
            fname = f"{sym.replace('-', '_')}_{tf_label}_365d.parquet"
            path = os.path.join(CACHE_DIR, fname)
        if not os.path.exists(path):
            continue
        df = pd.read_parquet(path).sort_values("ts").reset_index(drop=True)
        cutoff = df["ts"].max() - (DAYS * 24 * 3600 * 1000)
        df = df[df["ts"] >= cutoff].copy()
        if len(df) < 300:
            continue
        all_raw.extend(simulate_trades(df, sym, tf_minutes))

    if not all_raw:
        return None

    all_raw.sort(key=lambda t: t["entry_time"])

    balance = STARTING_BALANCE
    peak = balance; dd_pct = 0
    wins = 0; losses = 0; be = 0
    losers_row = 0; max_losers_row = 0
    trailed_wins = 0; trailed_losses = 0
    best_trade_pnl = 0; worst_trade_pnl = 0
    closed = []

    for t in all_raw:
        margin = balance * RISK_FRACTION
        notional = margin * LEVERAGE
        pnl_usd = notional * t["pnl_pct"]
        balance += pnl_usd
        if balance <= 0:
            balance = 0; break
        t["balance_after"] = balance; t["pnl_usd"] = pnl_usd; t["notional"] = notional
        closed.append(t)
        if t["pnl_pct"] > 0.0001:
            wins += 1; losers_row = 0
            if t["trailed"]: trailed_wins += 1
        elif t["pnl_pct"] < -0.0001:
            losses += 1; losers_row += 1; max_losers_row = max(max_losers_row, losers_row)
            if t["trailed"]: trailed_losses += 1
        else:
            be += 1; losers_row = 0
        best_trade_pnl = max(best_trade_pnl, pnl_usd)
        worst_trade_pnl = min(worst_trade_pnl, pnl_usd)
        if balance > peak: peak = balance
        dd = (peak - balance) / peak * 100 if peak > 0 else 0
        dd_pct = max(dd_pct, dd)

    total = len(closed)
    wr = wins / total * 100 if total else 0
    avg_win = sum(t["pnl_usd"] for t in closed if t["pnl_pct"] > 0.0001) / max(wins, 1)
    avg_loss = sum(t["pnl_usd"] for t in closed if t["pnl_pct"] < -0.0001) / max(losses, 1)
    avg_win_pct = sum(t["pnl_pct"] * 100 for t in closed if t["pnl_pct"] > 0.0001) / max(wins, 1)
    avg_loss_pct = sum(t["pnl_pct"] * 100 for t in closed if t["pnl_pct"] < -0.0001) / max(losses, 1)

    longs = [t for t in closed if t["side"] == "long"]
    shorts = [t for t in closed if t["side"] == "short"]

    avg_bars = sum(t["bars_held"] for t in closed) / total
    avg_hold_min = avg_bars * tf_minutes

    by_sym = {}
    for t in closed:
        s = t["symbol"]
        by_sym.setdefault(s, {"t": 0, "w": 0, "l": 0, "pnl": 0})
        by_sym[s]["t"] += 1; by_sym[s]["pnl"] += t["pnl_usd"]
        if t["pnl_pct"] > 0: by_sym[s]["w"] += 1
        elif t["pnl_pct"] < 0: by_sym[s]["l"] += 1

    by_reason = {}
    for t in closed:
        r = t["exit_reason"]
        by_reason.setdefault(r, {"count": 0, "pnl": 0, "w": 0, "l": 0})
        by_reason[r]["count"] += 1; by_reason[r]["pnl"] += t["pnl_usd"]
        if t["pnl_pct"] > 0: by_reason[r]["w"] += 1
        elif t["pnl_pct"] < 0: by_reason[r]["l"] += 1

    lpnl = sum(t["pnl_usd"] for t in longs)
    spnl = sum(t["pnl_usd"] for t in shorts)
    lwr = sum(1 for t in longs if t["pnl_pct"] > 0) / max(len(longs), 1) * 100
    swr = sum(1 for t in shorts if t["pnl_pct"] > 0) / max(len(shorts), 1) * 100

    return {
        "tf": tf_label, "tf_min": tf_minutes,
        "balance": balance, "start": STARTING_BALANCE,
        "pnl_pct": (balance / STARTING_BALANCE - 1) * 100,
        "total": total, "wr": wr, "wins": wins, "losses": losses, "be": be,
        "dd_pct": dd_pct, "peak": peak,
        "avg_win": avg_win, "avg_loss": avg_loss,
        "avg_win_pct": avg_win_pct, "avg_loss_pct": avg_loss_pct,
        "max_losers_row": max_losers_row,
        "avg_hold_min": avg_hold_min, "avg_bars": avg_bars,
        "trailed_wins": trailed_wins, "trailed_losses": trailed_losses,
        "lpnl": lpnl, "spnl": spnl, "lwr": lwr, "swr": swr,
        "nlongs": len(longs), "nshorts": len(shorts),
        "by_sym": by_sym, "by_reason": by_reason,
    }


def print_result(r):
    if r is None:
        print("  NO TRADES\n")
        return
    print(f"  {'Final:':20s} ${r['balance']:,.2f} ({r['pnl_pct']:+.1f}%)")
    print(f"  {'Peak:':20s} ${r['peak']:,.2f}")
    print(f"  {'Max DD:':20s} {r['dd_pct']:.1f}%")
    print(f"  {'Trades:':20s} {r['total']}")
    print(f"  {'Win rate:':20s} {r['wr']:.1f}% ({r['wins']}W/{r['losses']}L/{r['be']}BE)")
    print(f"  {'Avg win:':20s} ${r['avg_win']:+,.2f} ({r['avg_win_pct']:+.3f}%)")
    print(f"  {'Avg loss:':20s} ${r['avg_loss']:+,.2f} ({r['avg_loss_pct']:+.3f}%)")
    print(f"  {'Max L streak:':20s} {r['max_losers_row']}")
    print(f"  {'Avg hold:':20s} {r['avg_hold_min']:.0f} min ({r['avg_bars']:.1f} bars)")
    print(f"  {'Trailed:':20s} {r['trailed_wins']+r['trailed_losses']} ({r['trailed_wins']}W/{r['trailed_losses']}L)")
    print(f"  {'Longs:':20s} {r['nlongs']} | {r['lwr']:.0f}% WR | ${r['lpnl']:+,.2f}")
    print(f"  {'Shorts:':20s} {r['nshorts']} | {r['swr']:.0f}% WR | ${r['spnl']:+,.2f}")
    for s in sorted(r["by_sym"], key=lambda x: r["by_sym"][x]["pnl"], reverse=True):
        d = r["by_sym"][s]
        wrs = d["w"] / max(d["t"], 1) * 100
        print(f"    {s:15s}: {d['t']:3d}t | {wrs:.0f}% WR | ${d['pnl']:+,.2f}")
    print()


def main():
    print("=" * 78)
    print("VIKI MULTI-TIMEFRAME BACKTEST — 7% SL | Trail @ +3% (1.5%) | 10× | $100")
    print("=" * 78)

    # We have: 5m, 15m, 30m (SOL only), 1h for SOL/TAO/TIA
    # 30m only exists for BTC, ETH, SOL
    tfs = [
        ("5m", 5),
        ("15m", 15),
        ("1H", 60),
    ]

    results = []

    for tf_label, tf_min in tfs:
        print(f"\n{'─' * 78}")
        print(f"  TIMEFRAME: {tf_label} ({tf_min}m candles)")
        print(f"{'─' * 78}")
        r = run_tf(tf_label, tf_min)
        results.append(r)
        print_result(r)

    # 30m — SOL only
    print(f"{'─' * 78}")
    print(f"  TIMEFRAME: 30m (SOL-USDT only, 30m data)")
    print(f"{'─' * 78}")
    r30 = run_tf("30m", 30, filenames={"SOL-USDT": "SOL_USDT_30m_365d.parquet"})
    results.append(r30)
    print_result(r30)

    # Summary comparison
    print("=" * 78)
    print("  SUMMARY COMPARISON")
    print("=" * 78)
    print(f"  {'TF':<8s} {'Return':>8s} {'WR':>7s} {'Trades':>7s} {'MaxDD':>7s} {'AvgHold':>9s} {'TrailW':>7s}")
    print(f"  {'─'*8} {'─'*8} {'─'*7} {'─'*7} {'─'*7} {'─'*9} {'─'*7}")
    for r in filter(None, results):
        print(f"  {r['tf']:<8s} {r['pnl_pct']:>+7.1f}% {r['wr']:>6.1f}% {r['total']:>6d}  {r['dd_pct']:>6.1f}% {r['avg_hold_min']:>7.0f}m {' ' + str(r['trailed_wins']):>6s}")
    print()


if __name__ == "__main__":
    main()
