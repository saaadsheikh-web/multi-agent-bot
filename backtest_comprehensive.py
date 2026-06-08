#!/usr/bin/env python3
"""
COMPREHENSIVE BACKTEST — ALL agents (live + dead) × ALL timeframes × ALL symbols
+ Lower-TF confirmation testing
Pre-loads all data once → tests all agents → saves structured JSON/CSV.
"""

import os, sys, json, math, time as _time, inspect
from collections import defaultdict
import numpy as np
import pandas as pd

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")
sys.path.insert(0, WORK_DIR)

ENV_PATH = os.path.join(WORK_DIR, ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

import importlib.util
spec = importlib.util.spec_from_file_location("bot", os.path.join(WORK_DIR, "bot.py"))
bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
DAYS = 365
STARTING_BALANCE = 100.0
LEVERAGE = 5
RISK_FRACTION = 0.10

SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","XRP-USDT","BNB-USDT",
           "DOGE-USDT","ADA-USDT","AVAX-USDT","DOT-USDT","LINK-USDT",
           "LTC-USDT","ATOM-USDT","NEAR-USDT","APT-USDT","SUI-USDT",
           "INJ-USDT","TAO-USDT","ARB-USDT","OP-USDT","TIA-USDT"]

ALL_TFS = ["5m", "15m", "30m", "1H"]
TF_MINUTES = {"5m": 5, "15m": 15, "30m": 30, "1H": 60}
TF_STEP = {"5m": 12, "15m": 4, "30m": 2, "1H": 1}
WINDOW_SIZE = 1000

OUTPUT_DIR = os.path.join(WORK_DIR, "backtest_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PRE-LOAD ALL DATA
# ═══════════════════════════════════════════════════════════════════════════════
def preload_all_data():
    """Load all symbol×TF data once. Returns {(sym, tf): df}."""
    cache = {}
    print("Pre-loading data...", flush=True, end=" ")
    t0 = _time.time()
    for sym in SYMBOLS:
        for tf in ALL_TFS:
            fname = f"{sym.replace('-','_')}_{tf}_365d.parquet"
            path = os.path.join(CACHE_DIR, fname)
            if not os.path.exists(path):
                continue
            try:
                df = pd.read_parquet(path).sort_values("ts").reset_index(drop=True)
                cutoff = df["ts"].max() - (DAYS * 24 * 3600 * 1000)
                df = df[df["ts"] >= cutoff].copy()
                if len(df) >= 200:
                    cache[(sym, tf)] = df
            except Exception:
                pass
    elapsed = _time.time() - t0
    total = sum(len(v) for v in cache.values())
    print(f"{len(cache)} datasets ({total:,} total bars) in {elapsed:.1f}s", flush=True)
    return cache


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def get_all_agents():
    """Return list of (agent_instance, native_tfs) for ALL agent classes."""
    agents = []
    skip = {"Agent", "_DailyBreakoutBase", "LearningAgent"}
    seen = set()
    for cls in bot.Agent.__subclasses__():
        if cls.__name__ in skip:
            continue
        try:
            inst = cls()
            if inst.name in seen:
                continue
            seen.add(inst.name)
            src = inspect.getsource(inst.analyze)
            native_tfs = []
            if "df_5m" in src: native_tfs.append("5m")
            if "df_15m" in src: native_tfs.append("15m")
            if "df_1h" in src: native_tfs.append("1h")
            if not native_tfs:
                native_tfs = ["1h"]
            agents.append((inst, native_tfs))
        except Exception as e:
            print(f"  SKIP {cls.__name__}: {e}")
    return agents


def generate_signals(agent, df, sym, tf):
    """Run agent.analyze() on stepped bars using rolling 1000-bar window."""
    signals = []

    class FakeCtx:
        pass

    step = TF_STEP.get(tf, 1)
    for i in range(WINDOW_SIZE, len(df), step):
        window = df.iloc[i-WINDOW_SIZE:i+1]
        ctx = FakeCtx()
        ctx.df_5m = window
        ctx.df_15m = window
        ctx.df_1h = window

        try:
            result = agent.analyze(sym, ctx)
            if result is not None:
                signals.append({
                    "agent": agent.name, "symbol": sym,
                    "side": result.side, "confidence": result.confidence,
                    "bar": i, "time": df["ts"].iloc[i],
                })
        except Exception:
            pass

    return signals


def sim_trades(signals, profile, df, tf_min):
    """Walk forward through signals, simulate exits. Returns list of trade dicts."""
    if not signals:
        return []

    c = df["close"]; h = df["high"]; l = df["low"]
    tp_pct = profile.get("tp", 99.0) / 100
    sl_pct = profile.get("sl", 2.0) / 100
    trail_pct = profile.get("trail", 1.0) / 100
    activate_pct = profile.get("activate", 1.0) / 100
    max_hold_min = profile.get("max_hold_min", 720)
    max_bars = max(int(max_hold_min / tf_min), 1)
    if tp_pct > 0.98: tp_pct = None

    trades = []
    in_trade = None

    for sig in signals:
        if in_trade:
            continue

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

        for i in range(entry_bar + 1, len(df)):
            bars_held = i - entry_bar

            if side == "long":
                in_trade["high_water"] = max(in_trade["high_water"], h.iloc[i])
            else:
                in_trade["low_water"] = min(in_trade["low_water"], l.iloc[i])

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

            if in_trade["trail_active"]:
                if side == "long":
                    new_stop = in_trade["high_water"] * (1 - trail_pct)
                    in_trade["trail_stop"] = max(in_trade.get("trail_stop", 0), new_stop)
                else:
                    new_stop = in_trade["low_water"] * (1 + trail_pct)
                    in_trade["trail_stop"] = min(in_trade.get("trail_stop", float("inf")), new_stop)

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
                    "entry": float(entry_price), "exit": float(exit_price),
                    "pnl_pct": float(pnl_pct), "exit_reason": exit_reason,
                    "bars_held": bars_held, "trailed": in_trade["trail_active"],
                    "entry_time": int(in_trade["entry_time"]),
                    "exit_time": int(df["ts"].iloc[i]),
                })
                in_trade = None
                break

    return trades


def compute_stats(trades):
    """Compute summary stats from a list of trades with compounding."""
    if not trades:
        return None

    balance = STARTING_BALANCE
    peak = balance; dd = 0
    wins = 0; losses = 0; be = 0
    losers_row = 0; max_losers_row = 0
    trailed_wins = 0; trailed_losses = 0

    sorted_trades = sorted(trades, key=lambda t: t["entry_time"])

    for t in sorted_trades:
        margin = balance * RISK_FRACTION
        notional = margin * LEVERAGE
        pnl_usd = notional * t["pnl_pct"]
        balance += pnl_usd
        if balance <= 0: balance = 0; break
        t["pnl_usd"] = float(pnl_usd)
        t["balance_after"] = float(balance)
        if t["pnl_pct"] > 0.0001:
            wins += 1; losers_row = 0
            if t["trailed"]: trailed_wins += 1
        elif t["pnl_pct"] < -0.0001:
            losses += 1; losers_row += 1
            max_losers_row = max(max_losers_row, losers_row)
            if t["trailed"]: trailed_losses += 1
        else:
            be += 1; losers_row = 0
        if balance > peak: peak = balance
        dd = max(dd, (peak - balance) / peak * 100 if peak > 0 else 0)

    total = len(sorted_trades)
    wr = wins / total * 100 if total else 0
    avg_win = sum(t["pnl_usd"] for t in sorted_trades if t["pnl_pct"] > 0.0001) / max(wins, 1)
    avg_loss = sum(t["pnl_usd"] for t in sorted_trades if t["pnl_pct"] < -0.0001) / max(losses, 1)
    avg_win_pct = sum(t["pnl_pct"] * 100 for t in sorted_trades if t["pnl_pct"] > 0.0001) / max(wins, 1)
    avg_loss_pct = sum(t["pnl_pct"] * 100 for t in sorted_trades if t["pnl_pct"] < -0.0001) / max(losses, 1)
    avg_bars = sum(t["bars_held"] for t in sorted_trades) / total

    by_sym = {}
    for t in sorted_trades:
        s = t["symbol"]
        by_sym.setdefault(s, {"t": 0, "w": 0, "l": 0, "pnl": 0})
        by_sym[s]["t"] += 1; by_sym[s]["pnl"] += t.get("pnl_usd", 0)
        if t["pnl_pct"] > 0: by_sym[s]["w"] += 1
        elif t["pnl_pct"] < 0: by_sym[s]["l"] += 1

    by_reason = {}
    for t in sorted_trades:
        r = t["exit_reason"]
        by_reason.setdefault(r, {"count": 0, "pnl": 0, "w": 0, "l": 0})
        by_reason[r]["count"] += 1; by_reason[r]["pnl"] += t.get("pnl_usd", 0)
        if t["pnl_pct"] > 0: by_reason[r]["w"] += 1
        elif t["pnl_pct"] < 0: by_reason[r]["l"] += 1

    longs = [t for t in sorted_trades if t["side"] == "long"]
    shorts = [t for t in sorted_trades if t["side"] == "short"]

    return {
        "balance": round(balance, 2),
        "return_pct": round((balance / STARTING_BALANCE - 1) * 100, 1),
        "total": total, "wins": wins, "losses": losses, "be": be,
        "wr": round(wr, 1),
        "max_dd": round(dd, 1), "peak": round(peak, 2),
        "avg_win": round(avg_win, 2), "avg_loss": round(avg_loss, 2),
        "avg_win_pct": round(avg_win_pct, 3), "avg_loss_pct": round(avg_loss_pct, 3),
        "max_losers_row": max_losers_row, "avg_bars": round(avg_bars, 1),
        "trailed_wins": trailed_wins, "trailed_losses": trailed_losses,
        "long_pnl": round(sum(t.get("pnl_usd", 0) for t in longs), 2),
        "short_pnl": round(sum(t.get("pnl_usd", 0) for t in shorts), 2),
        "nlongs": len(longs), "nshorts": len(shorts),
        "by_symbol": {s: {"trades": d["t"], "wins": d["w"], "losses": d["l"],
                          "pnl": round(d["pnl"], 2)} for s, d in by_sym.items()},
        "by_reason": by_reason,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# LOWER-TF CONFIRMATION
# ═══════════════════════════════════════════════════════════════════════════════
TF_CONFIRM_MAP = {"15m": "5m", "30m": "5m", "1H": "15m"}


def filter_signals_with_confirmation(signals, df_lower):
    """Filter signals: only keep those where lower TF confirms trend.
    Uses binary search for O(log n) timestamp lookup instead of O(n) boolean mask."""
    if df_lower is None or len(df_lower) < 100:
        return signals, 0

    filtered = []
    max_idx = len(df_lower) - 1
    lt = df_lower["ts"].values  # numpy array for searchsorted
    lc = df_lower["close"]
    le50 = ema(lc, 50)
    filtered_count = 0

    for sig in signals:
        bar_time = sig["time"]
        # Binary search for the most recent bar at or before signal time
        pos = np.searchsorted(lt, bar_time, side="right") - 1
        if pos < 50 or pos > max_idx:
            filtered_count += 1
            continue

        price = lc.iloc[pos]
        e50 = le50.iloc[pos]

        if pd.isna(e50):
            filtered_count += 1
            continue

        if (sig["side"] == "long" and price > e50) or (sig["side"] == "short" and price < e50):
            filtered.append(sig)
        else:
            filtered_count += 1

    return filtered, filtered_count


# ␐══════════════════════════════════════════════════════════════════════════════
# SPEED-TIERED SYMBOL ALLOCATION
# ═══════════════════════════════════════════════════════════════════════════════
AGENT_SPEED = {
    "whale": 0.2, "news": 0.2, "donchian": 0.2, "funding": 0.2,
    "asian_pump": 0.5, "pump_dump_reversal": 0.6, "zscore_reversion": 0.6,
    "kalman_trend": 0.7, "volume_capitulation": 1.0, "golden_cross": 1.0,
    "liquidity_sweep": 1.5, "raschke_retest": 1.5, "funding_extremes": 0.2,
    "viki": 1.5, "macd_cross": 1.7,
    "fib_786_oversold": 3.1, "fib_hotzone": 3.2, "daily_breakout": 3.2,
    "williams_r": 3.0, "daily_breakout_24h": 3.5, "asymmetric": 4.2, "fibonacci": 5.0,
    "rsi_divergence": 5.2, "bb_squeeze": 5.3, "supertrend": 5.5,
    "stoch_rsi": 5.5, "scalp": 5.9, "vwap_reversion": 6.1,
    "volume_profile": 6.2, "fib_confluence": 6.6,
    "meanrev": 6.7, "bb_bounce": 6.7, "candlestick": 6.9,
    "swing": 7.1, "momentum": 7.2, "ema_ribbon": 8.0,
    "smart_scalp": 8.7, "wide_scalp": 9.1,
    "connors_rsi2": 10.5, "trend_pullback": 11.4,
    "utbot_mtf": 24.2, "utbot_v3": 24.7,
    "wide_candle": 29.0, "hurst_regime": 33.8,
}

TOP_SYMBOLS = ["BTC-USDT","ETH-USDT","SOL-USDT","BNB-USDT","XRP-USDT",
               "DOGE-USDT","ADA-USDT","AVAX-USDT","LINK-USDT","SUI-USDT"]


def get_symbols_for_agent(agent, speed):
    """Return (symbols, tfs_to_skip)."""
    syms = list(getattr(agent, 'WHITELIST', SYMBOLS)) if hasattr(agent, 'WHITELIST') else SYMBOLS
    skip_tfs = set()
    if speed < 2:
        pass
    elif speed < 5:
        syms = [s for s in TOP_SYMBOLS if s in syms]
    elif speed < 15:
        syms = [s for s in TOP_SYMBOLS[:5] if s in syms]
    else:
        syms = [s for s in TOP_SYMBOLS[:5] if s in syms]
        skip_tfs.add("5m")
    return syms, skip_tfs


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def run_agent_tf(agent, tf, syms, profile, data_cache, use_confirmation=False):
    """Test one agent×TF combination. Returns (trades, stats)."""
    tf_min = TF_MINUTES[tf]
    all_trades = []
    total_signals = 0
    filtered_count = 0
    confirm_tf = TF_CONFIRM_MAP.get(tf) if use_confirmation else None

    for sym in syms:
        if hasattr(agent, 'WHITELIST') and sym not in agent.WHITELIST:
            continue

        df = data_cache.get((sym, tf))
        if df is None:
            continue

        signals = generate_signals(agent, df, sym, tf)
        total_signals += len(signals)

        if confirm_tf:
            df_lower = data_cache.get((sym, confirm_tf))
            signals, fc = filter_signals_with_confirmation(signals, df_lower)
            filtered_count += fc

        trades = sim_trades(signals, profile, df, tf_min)
        all_trades.extend(trades)

    if not all_trades:
        return None, None, total_signals, filtered_count

    stats = compute_stats(all_trades)
    if stats:
        stats["confirmation"] = use_confirmation
        stats["confirm_tf"] = confirm_tf
        stats["signals_total"] = total_signals
        stats["signals_filtered"] = filtered_count
    return all_trades, stats, total_signals, filtered_count


def main():
    t0 = _time.time()
    print("=" * 100)
    print("COMPREHENSIVE BACKTEST — ALL Agents × ALL Timeframes × ALL Symbols")
    print(f"1 Year | {LEVERAGE}× | ${STARTING_BALANCE} start | {RISK_FRACTION*100:.0f}% risk/trade")
    print("=" * 100)

    # Pre-load all data
    data_cache = preload_all_data()
    if not data_cache:
        print("ERROR: No data loaded!")
        return

    all_agents = get_all_agents()
    print(f"\nTesting {len(all_agents)} agents across {len(ALL_TFS)} timeframes")
    print(f"With lower-TF confirmation: 15m→5m, 30m→5m, 1H→15m")
    print(f"Window: {WINDOW_SIZE} bars | Steps: {TF_STEP}")
    print(f"{'─' * 100}")

    all_results = []
    agent_count = len(all_agents)

    for idx, (agent, native_tfs) in enumerate(all_agents):
        name = agent.name
        enabled = agent.enabled
        profile_key = agent.profile
        profile = bot.PROFILES.get(profile_key,
                    bot.PROFILES.get("momentum", {"tp": 3, "sl": 1.2, "trail": 1.0,
                                                   "activate": 0.8, "max_hold_min": 360}))

        speed = AGENT_SPEED.get(name, 5.0)
        syms, skip_tfs = get_symbols_for_agent(agent, speed)

        status = "🟢" if enabled else "⚫"
        tier = "⚡" if speed < 2 else ("🟡" if speed < 5 else ("🟠" if speed < 15 else "🔴"))
        print(f"\n[{idx+1}/{agent_count}] {tier} {status} {name:28s} profile={profile_key:20s} "
              f"native={native_tfs} | {len(syms)} syms | ~{speed:.0f}s/sym", flush=True)

        for tf in ALL_TFS:
            if tf in skip_tfs:
                continue
            tf_min = TF_MINUTES[tf]

            # Standard
            a_t0 = _time.time()
            trades, stats, total_sigs, _ = run_agent_tf(agent, tf, syms, profile, data_cache, use_confirmation=False)
            a_elapsed = _time.time() - a_t0

            if stats:
                stats.update({"agent": name, "tf": tf, "tf_min": tf_min,
                              "enabled": enabled, "profile": profile_key,
                              "native": tf in native_tfs, "test_type": "standard",
                              "elapsed": round(a_elapsed, 1)})
                all_results.append(stats)
                arrow = "▲" if stats["return_pct"] > 0 else "▼"
                print(f"    {tf:5s} standard       {stats['total']:5d}t | WR {stats['wr']:5.1f}% | "
                      f"${stats['balance']:8.2f} ({stats['return_pct']:+6.1f}%) {arrow} | "
                      f"DD {stats['max_dd']:5.1f}% | {a_elapsed:.0f}s", flush=True)

            # Confirmed
            if tf in TF_CONFIRM_MAP:
                a_t0 = _time.time()
                trades_c, stats_c, total_sigs, fc = run_agent_tf(agent, tf, syms, profile, data_cache, use_confirmation=True)
                a_elapsed = _time.time() - a_t0

                if stats_c:
                    stats_c.update({"agent": name, "tf": tf, "tf_min": tf_min,
                                    "enabled": enabled, "profile": profile_key,
                                    "native": tf in native_tfs, "test_type": "confirmed",
                                    "elapsed": round(a_elapsed, 1)})
                    all_results.append(stats_c)
                    arrow = "▲" if stats_c["return_pct"] > 0 else "▼"
                    print(f"    {tf:5s} confirmed {TF_CONFIRM_MAP[tf]:>2s}      {stats_c['total']:5d}t | WR {stats_c['wr']:5.1f}% | "
                          f"${stats_c['balance']:8.2f} ({stats_c['return_pct']:+6.1f}%) {arrow} | "
                          f"DD {stats_c['max_dd']:5.1f}% | filtered {fc}/{total_sigs}sigs | {a_elapsed:.0f}s", flush=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════════════════════════════════════
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = os.path.join(OUTPUT_DIR, f"comprehensive_backtest_{ts}.json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n✅ Full JSON: {json_path}")

    csv_fields = ["agent", "tf", "test_type", "enabled", "native", "profile",
                  "total", "wr", "balance", "return_pct", "max_dd",
                  "avg_win", "avg_loss", "avg_win_pct", "avg_loss_pct",
                  "max_losers_row", "trailed_wins", "trailed_losses",
                  "long_pnl", "short_pnl", "nlongs", "nshorts", "avg_bars", "elapsed"]
    csv_path = os.path.join(OUTPUT_DIR, f"comprehensive_backtest_{ts}.csv")
    with open(csv_path, "w") as f:
        f.write(",".join(csv_fields) + "\n")
        for r in all_results:
            f.write(",".join(str(r.get(k, "")) for k in csv_fields) + "\n")
    print(f"✅ Summary CSV: {csv_path}")

    # ═══════════════════════════════════════════════════════════════════════════
    # RANKINGS
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 100)
    print("TOP 30 — All Agent×TF Combos (Standard)")
    print("=" * 100)
    standard = [r for r in all_results if r["test_type"] == "standard"]
    print(f"{'Agent':28s} {'TF':5s} {'Enbl':5s} {'Native':7s} {'Trades':6s} {'WR':6s} {'Final':9s} {'Return':8s} {'MaxDD':6s}")
    print(f"{'─'*28} {'─'*5} {'─'*5} {'─'*7} {'─'*6} {'─'*6} {'─'*9} {'─'*8} {'─'*6}")
    for r in sorted(standard, key=lambda x: x["return_pct"], reverse=True)[:30]:
        en = "✓" if r["enabled"] else "✗"
        nat = "✓" if r["native"] else ""
        print(f"{r['agent']:28s} {r['tf']:5s} {en:5s} {nat:7s} {r['total']:6d} {r['wr']:5.1f}% "
              f"${r['balance']:8.2f} {r['return_pct']:+7.1f}% {r['max_dd']:5.1f}%")

    # Best by TF
    print(f"\n{'─' * 100}")
    print("BEST AGENT PER TIMEFRAME (Standard)")
    print(f"{'─' * 100}")
    for tf in ALL_TFS:
        tf_results = [r for r in standard if r["tf"] == tf]
        if not tf_results: continue
        best = max(tf_results, key=lambda x: x["return_pct"])
        worst = min(tf_results, key=lambda x: x["return_pct"])
        profitable = [r for r in tf_results if r["return_pct"] > 0]
        print(f"  {tf:5s}: {len(profitable)}/{len(tf_results)} profitable")
        print(f"        Best:  {best['agent']:25s} ${best['balance']:.0f} ({best['return_pct']:+.1f}%) {best['total']}t {best['wr']:.0f}% WR")
        print(f"        Worst: {worst['agent']:25s} ${worst['balance']:.0f} ({worst['return_pct']:+.1f}%) {worst['total']}t {worst['wr']:.0f}% WR")

    # Confirmation comparison
    print(f"\n{'─' * 100}")
    print("CONFIRMATION EFFECT — Lower-TF confirmation impact")
    print(f"{'─' * 100}")
    confirmed = [r for r in all_results if r["test_type"] == "confirmed"]
    improvements = []
    for rc in confirmed:
        match = [r for r in standard if r["agent"] == rc["agent"] and r["tf"] == rc["tf"]]
        if match:
            delta = rc["return_pct"] - match[0]["return_pct"]
            dd_delta = match[0]["max_dd"] - rc["max_dd"]
            improvements.append({
                "agent": rc["agent"], "tf": rc["tf"],
                "std_return": match[0]["return_pct"], "conf_return": rc["return_pct"],
                "delta": delta, "dd_delta": dd_delta,
                "std_trades": match[0]["total"], "conf_trades": rc["total"],
            })

    improvements.sort(key=lambda x: x["delta"], reverse=True)
    print(f"{'Agent':28s} {'TF':5s} {'StdRet':8s} {'ConfRet':8s} {'Δ':8s} {'ΔDD':7s} {'Trades':12s}")
    print(f"{'─'*28} {'─'*5} {'─'*8} {'─'*8} {'─'*8} {'─'*7} {'─'*12}")
    for imp in improvements[:20]:
        print(f"{imp['agent']:28s} {imp['tf']:5s} {imp['std_return']:+7.1f}% {imp['conf_return']:+7.1f}% "
              f"{imp['delta']:+7.1f}% {imp['dd_delta']:+6.1f}% "
              f"{imp['std_trades']}→{imp['conf_trades']}")

    better = [i for i in improvements if i["delta"] > 0]
    worse = [i for i in improvements if i["delta"] < 0]
    if improvements:
        print(f"\n  Confirmation improved: {len(better)} | worsened: {len(worse)} | avg Δ: {np.mean([i['delta'] for i in improvements]):+.1f}%")

    elapsed = _time.time() - t0
    print(f"\n{'─' * 100}")
    print(f"Total: {elapsed/60:.1f} min | {len(all_results)} test results | {len(all_agents)} agents")
    print(f"{'─' * 100}")


if __name__ == "__main__":
    from datetime import datetime
    main()
