#!/usr/bin/env python3
"""Full backtest of ALL live agents across timeframes — 1 year, compounding, per-agent stats."""

import os, sys, json, math, time as _time
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import numpy as np
import pandas as pd

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")
ENV_PATH = os.path.join(WORK_DIR, ".env")
sys.path.insert(0, WORK_DIR)

if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# Import agent classes
import importlib.util
spec = importlib.util.spec_from_file_location("bot", os.path.join(WORK_DIR, "bot.py"))
bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot)

# ── Config ───────────────────────────────────────────────────────────────────
DAYS = 365
STARTING_BALANCE = 100.0
LEVERAGE = 5
RISK_FRACTION = 0.10
SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT","BNB-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT",
           "LTC-USDT","ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT",
           "INJ-USDT","TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT"]

# Find all Agent subclasses that are enabled (live)
def get_live_agents():
    """Return list of (agent_instance, timeframes_to_test)."""
    agents = []
    for cls in bot.Agent.__subclasses__():
        try:
            inst = cls()
            if not inst.enabled:
                continue
            # Determine which timeframe this agent uses
            src = inspect.getsource(inst.analyze)
            tfs = []
            if "df_5m" in src: tfs.append("5m")
            if "df_15m" in src: tfs.append("15m")
            if "df_1h" in src: tfs.append("1h")
            if not tfs:
                tfs = ["1h"]  # fallback
            agents.append((inst, tfs))
        except Exception as e:
            print(f"  SKIP {cls.__name__}: {e}")
    return agents

import inspect

# ── Indicator helpers ─────────────────────────────────────────────────────────
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

# ── Trade simulator ──────────────────────────────────────────────────────────
def sim_trades(signals, profile, df):
    """Run signals through a trade simulator. Returns list of trade dicts."""
    if not signals:
        return []

    c = df["close"]; h = df["high"]; l = df["low"]
    tp_pct = profile.get("tp", 99.0) / 100
    sl_pct = profile.get("sl", 2.0) / 100
    trail_pct = profile.get("trail", 1.0) / 100
    activate_pct = profile.get("activate", 1.0) / 100
    max_bars = profile.get("max_hold_min", 720) // 5  # convert to bars (approx)

    if tp_pct > 0.98: tp_pct = None  # "99.0" = trailing only

    trades = []
    in_trade = None

    for sig in signals:
        if in_trade:
            continue  # one trade at a time per symbol

        entry_bar = sig["bar"]
        entry_price = c.iloc[entry_bar]
        side = sig["side"]

        in_trade = {
            "side": side, "entry": entry_price, "entry_bar": entry_bar,
            "high_water": entry_price, "low_water": entry_price,
            "trail_active": False, "trail_stop": None,
            "agent": sig["agent"], "symbol": sig["symbol"],
            "entry_time": df["ts"].iloc[entry_bar],
        }

        # Walk forward from entry
        for i in range(entry_bar + 1, len(df)):
            bars_held = i - entry_bar

            if side == "long":
                in_trade["high_water"] = max(in_trade["high_water"], h.iloc[i])
            else:
                in_trade["low_water"] = min(in_trade["low_water"], l.iloc[i])

            # Trail activation
            if not in_trade["trail_active"]:
                if side == "long":
                    profit = (in_trade["high_water"] - entry_price) / entry_price
                    if profit >= activate_pct:
                        in_trade["trail_active"] = True
                        in_trade["trail_stop"] = in_trade["high_water"] * (1 - trail_pct)
                else:
                    profit = (entry_price - in_trade["low_water"]) / entry_price
                    if profit >= activate_pct:
                        in_trade["trail_active"] = True
                        in_trade["trail_stop"] = in_trade["low_water"] * (1 + trail_pct)

            # Update trail
            if in_trade["trail_active"]:
                if side == "long":
                    new_stop = in_trade["high_water"] * (1 - trail_pct)
                    in_trade["trail_stop"] = max(in_trade.get("trail_stop", 0), new_stop)
                else:
                    new_stop = in_trade["low_water"] * (1 + trail_pct)
                    in_trade["trail_stop"] = min(in_trade.get("trail_stop", float("inf")), new_stop)

            # Exit checks
            exit_price = None; exit_reason = None

            if side == "long":
                hard_sl = entry_price * (1 - sl_pct)
                eff_sl = max(hard_sl, in_trade.get("trail_stop", hard_sl)) if in_trade["trail_active"] else hard_sl
                if tp_pct:
                    tp = entry_price * (1 + tp_pct)
                    if h.iloc[i] >= tp:
                        exit_price = tp; exit_reason = "TP_HIT"
                if exit_price is None and l.iloc[i] <= eff_sl:
                    exit_price = eff_sl
                    exit_reason = "TRAIL_STOP" if in_trade["trail_active"] else "SL_HIT"
            else:
                hard_sl = entry_price * (1 + sl_pct)
                eff_sl = min(hard_sl, in_trade.get("trail_stop", hard_sl)) if in_trade["trail_active"] else hard_sl
                if tp_pct:
                    tp = entry_price * (1 - tp_pct)
                    if l.iloc[i] <= tp:
                        exit_price = tp; exit_reason = "TP_HIT"
                if exit_price is None and h.iloc[i] >= eff_sl:
                    exit_price = eff_sl
                    exit_reason = "TRAIL_STOP" if in_trade["trail_active"] else "SL_HIT"

            if bars_held >= max_bars:
                exit_price = c.iloc[i]; exit_reason = "TIMEOUT"

            if exit_price is not None:
                pnl_pct = (exit_price - entry_price) / entry_price if side == "long" else (entry_price - exit_price) / entry_price
                trades.append({
                    "agent": sig["agent"], "symbol": sig["symbol"], "side": side,
                    "entry": entry_price, "exit": exit_price, "pnl_pct": pnl_pct,
                    "exit_reason": exit_reason, "bars_held": bars_held,
                    "trailed": in_trade["trail_active"],
                    "entry_time": in_trade["entry_time"], "exit_time": df["ts"].iloc[i],
                })
                in_trade = None
                break

    return trades


def generate_signals(agent, df, sym, tf):
    """Run agent.analyze() on each bar and collect signals."""
    signals = []

    class FakeCtx:
        pass

    for i in range(60, len(df), 1):  # step by 1 bar for thoroughness
        window = df.iloc[:i+1].copy()
        ctx = FakeCtx()
        if tf == "5m":
            ctx.df_5m = window
            ctx.df_15m = window  # fallback
            ctx.df_1h = window
        elif tf == "15m":
            ctx.df_15m = window
            ctx.df_1h = window  # fallback
            ctx.df_5m = window
        else:
            ctx.df_1h = window
            ctx.df_15m = window
            ctx.df_5m = window

        try:
            result = agent.analyze(sym, ctx)
            if result is not None:
                signals.append({
                    "agent": agent.name,
                    "symbol": sym,
                    "side": result.side,
                    "confidence": result.confidence,
                    "bar": i,
                    "time": df["ts"].iloc[i],
                })
        except Exception:
            pass

    return signals


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 90)
    print("FULL BACKTEST — All Live Agents × Timeframes × 365 Days")
    print("=" * 90)

    live_agents = get_live_agents()
    print(f"\nFound {len(live_agents)} live agents to test\n")

    all_results = []

    for agent, timeframes in live_agents:
        name = agent.name
        profile_key = agent.profile
        profile = bot.PROFILES.get(profile_key, bot.PROFILES.get("momentum", {"tp":3,"sl":1.2,"trail":1.0,"activate":0.8,"max_hold_min":360}))

        for tf in timeframes:
            print(f"  {name:25s} [{tf}] ...", end=" ", flush=True)

            agent_trades = []

            for sym in SYMBOLS:
                # Check whitelist if agent has one
                if hasattr(agent, 'WHITELIST') and sym not in agent.WHITELIST:
                    continue

                cache_file = os.path.join(CACHE_DIR, f"{sym.replace('-','_')}_{tf}_365d.parquet")
                if not os.path.exists(cache_file):
                    continue

                df = pd.read_parquet(cache_file).sort_values("ts").reset_index(drop=True)
                if len(df) < 100:
                    continue

                # Filter to last 365 days
                cutoff = df["ts"].max() - (DAYS * 24 * 3600 * 1000)
                df = df[df["ts"] >= cutoff].copy()
                if len(df) < 200:
                    continue

                # Generate signals from agent
                sigs = generate_signals(agent, df, sym, tf)

                # Simulate trades
                trades = sim_trades(sigs, profile, df)
                agent_trades.extend(trades)

            if not agent_trades:
                print("0 trades")
                continue

            # Run compounding simulation
            balance = STARTING_BALANCE
            peak = balance; dd = 0
            wins = 0; losses = 0
            agent_trades.sort(key=lambda t: t["entry_time"])

            for t in agent_trades:
                margin = balance * RISK_FRACTION
                notional = margin * LEVERAGE
                pnl_usd = notional * t["pnl_pct"]
                balance += pnl_usd
                if balance <= 0: balance = 0; break
                t["pnl_usd"] = pnl_usd; t["balance_after"] = balance
                if t["pnl_pct"] > 0.0001: wins += 1
                elif t["pnl_pct"] < -0.0001: losses += 1
                if balance > peak: peak = balance
                dd = max(dd, (peak - balance) / peak * 100 if peak > 0 else 0)

            wr = wins / len(agent_trades) * 100 if agent_trades else 0
            avg_w = sum(t["pnl_usd"] for t in agent_trades if t["pnl_pct"] > 0) / max(wins, 1)
            avg_l = sum(t["pnl_usd"] for t in agent_trades if t["pnl_pct"] < 0) / max(losses, 1)
            ret = (balance / STARTING_BALANCE - 1) * 100

            # Only show if enough trades
            status = "✅" if balance > STARTING_BALANCE else "❌"
            print(f"{len(agent_trades):4d}t | WR {wr:.0f}% | ${balance:.0f} ({ret:+.0f}%) | DD {dd:.0f}% {status}")

            all_results.append({
                "agent": name, "tf": tf, "trades": len(agent_trades),
                "wr": wr, "final": balance, "return": ret,
                "peak": peak, "max_dd": dd, "avg_win": avg_w, "avg_loss": avg_l,
                "wins": wins, "losses": losses, "profile": profile_key,
            })

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 90)
    print("RANKING — By Return %")
    print("=" * 90)
    print(f"\n  {'Agent':25s} {'TF':5s} {'Trades':6s} {'WR':6s} {'Final':8s} {'Return':8s} {'MaxDD':6s} {'Profile':15s}")
    print(f"  {'-'*25} {'-'*5} {'-'*6} {'-'*6} {'-'*8} {'-'*8} {'-'*6} {'-'*15}")

    for r in sorted(all_results, key=lambda x: x["return"], reverse=True):
        print(f"  {r['agent']:25s} {r['tf']:5s} {r['trades']:6d} {r['wr']:5.0f}% "
              f"${r['final']:7.0f} {r['return']:+7.0f}% {r['max_dd']:5.0f}% {r['profile']:15s}")

    # Winners/losers count
    profitable = [r for r in all_results if r["return"] > 0]
    print(f"\n  {len(profitable)}/{len(all_results)} agent×timeframe combos profitable")

    # Best by timeframe
    print(f"\n  Best by timeframe:")
    for tf in ["5m", "15m", "1h"]:
        tf_results = [r for r in all_results if r["tf"] == tf]
        if tf_results:
            best = max(tf_results, key=lambda x: x["return"])
            print(f"    {tf}: {best['agent']} — ${best['final']:.0f} ({best['return']:+.0f}%) {best['trades']}t {best['wr']:.0f}% WR")


if __name__ == "__main__":
    main()
