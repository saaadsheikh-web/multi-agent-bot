#!/usr/bin/env python3
"""Run the coin scout against live BloFin data."""
import os, sys, time

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
sys.path.insert(0, WORK_DIR)
os.chdir(WORK_DIR)

# Load .env
env_path = os.path.join(WORK_DIR, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

import pandas as pd
import numpy as np
from coin_scout import score_coin, assign_strategies, STRATEGY_MATCH, WEIGHTS

# Import bot's BloFin wrapper
import importlib.util
spec = importlib.util.spec_from_file_location("bot", os.path.join(WORK_DIR, "bot.py"))
bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot)


def main():
    print("=" * 80)
    print("COIN SCOUT — Live BloFin Scan")
    print("=" * 80)

    # Init exchange
    bf = bot.BloFin()
    balance = bf.balance()
    print(f"Connected. Balance: ${balance:,.2f}")

    # Get all tickers
    print("\nFetching tickers...", end=" ", flush=True)
    t0 = time.time()
    tickers = bf.tickers()
    print(f"{len(tickers)} pairs in {time.time()-t0:.1f}s")

    # Filter USDT pairs
    usdt_pairs = []
    for t in tickers:
        sym = t.get("instId") or ""
        if not sym.endswith("-USDT"):
            continue
        base = sym.split("-")[0]
        if base in ("USDC", "DAI", "BUSD", "TUSD", "USDP", "FDUSD"):
            continue
        if "1000" in base or "10000" in base:
            continue
        usdt_pairs.append((sym, t))

    print(f"\nScouting {len(usdt_pairs)} USDT pairs...")
    print(f"Scoring: {list(WEIGHTS.keys())}")
    print()

    results = []
    errors = 0

    for i, (sym, ticker) in enumerate(usdt_pairs):
        try:
            df_1h = bf.candles(sym, "1H", 200)
            if df_1h is None or len(df_1h) < 100:
                continue

            result = score_coin(sym, df_1h, ticker_info=ticker)
            if result["total_score"] >= 35:  # show borderline+ coins
                results.append(result)

                strats = ", ".join(result.get("matched_strategies", [])[:3])
                score = result["total_score"]
                bar = "█" * (score // 5)
                print(f"  {sym:<15s} score={score:3d} {bar:<20s} {strats}")

        except Exception as e:
            errors += 1
            if errors <= 3:
                print(f"  {sym:<15s} ERROR: {e}")

        # Progress
        if (i + 1) % 50 == 0:
            print(f"  ... {i+1}/{len(usdt_pairs)} scanned, {len(results)} qualified")

    # Sort and take top 30
    results.sort(key=lambda x: -x["total_score"])
    top = results[:30]

    # Print report
    print(f"\n{'='*80}")
    print(f"TOP 30 COINS — Scored for Backtest-Winning Strategies")
    print(f"{'='*80}")
    print(f"{'Rank':<6} {'Symbol':<15} {'Score':<8} {'Range%':<10} {'ADX':<8} {'Vol':<8} {'Strategies'}")
    print(f"{'─'*6} {'─'*15} {'─'*8} {'─'*10} {'─'*8} {'─'*8} {'─'*40}")

    for i, coin in enumerate(top, 1):
        sym = coin["symbol"]
        score = coin["total_score"]
        s = coin.get("scores", {})
        dr = s.get("daily_range", 0)
        adx_s = s.get("adx_trend", 0)
        vol = s.get("volume_health", 0)
        strats = ", ".join(coin.get("matched_strategies", [])[:3])
        flags = []
        if score >= 70: flags.append("🔥")
        if score >= 60: flags.append("✅")
        flag = " ".join(flags)
        print(f"{i:<6} {sym:<15} {score:<8} {dr:<10} {adx_s:<8} {vol:<8} {strats:<30s} {flag}")

    # Strategy assignments
    assignments = assign_strategies(top)
    print(f"\n{'='*80}")
    print("STRATEGY → COIN ASSIGNMENTS")
    print(f"{'='*80}")
    for strategy, symbols in sorted(assignments.items(), key=lambda x: -len(x[1])):
        print(f"  {strategy:<25s} ({len(symbols)} coins): {', '.join(symbols[:8])}")

    # Compare with backtest winners
    backtest_winners = {"SUI-USDT", "DOGE-USDT", "BNB-USDT", "XRP-USDT", "ADA-USDT",
                        "TAO-USDT", "TIA-USDT", "APT-USDT", "LINK-USDT", "NEAR-USDT"}
    scouted = {c["symbol"] for c in top}
    overlap = backtest_winners & scouted
    new_finds = scouted - backtest_winners

    print(f"\n{'='*80}")
    print("BACKTEST VALIDATION")
    print(f"{'='*80}")
    print(f"  Backtest winners found in scout: {len(overlap)}/{len(backtest_winners)} — {', '.join(sorted(overlap))}")
    print(f"  New coins not in backtest:       {len(new_finds)} — {', '.join(sorted(new_finds)[:10])}")

    print(f"\n{'='*80}")
    print(f"Scout complete. {len(top)} coins qualified. {errors} errors.")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
