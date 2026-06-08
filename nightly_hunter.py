#!/usr/bin/env python3
"""
nightly_hunter.py — Re-validates every agent against fresh market data.

Run nightly via scheduled-tasks. Steps:
  1. Refresh 365-day candle cache (BloFin public API)
  2. Run full backtest across all agents × 20 symbols
  3. Compute leaderboard with Sharpe / WR / ExpR / MaxDD
  4. Append timestamped section to BACKTEST_REPORT.md
  5. Telegram-ping with top 5 + bottom 5 changes vs. last run

If a previously-deployed agent drops below acceptable thresholds, surface a
recommendation to undeploy. Never auto-undeploys without user confirmation.
"""
import os, sys, json, subprocess, datetime as dt
from pathlib import Path

# json may be unused without parametric — keep for future

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
REPORT = WORK / "BACKTEST_REPORT.md"
HUNTER_LOG = WORK / "nightly_hunter.log"

# Acceptance thresholds — agents below these get flagged
MIN_SHARPE = 2.0
MIN_EXPR = 0.10
MAX_DD_PCT = 25.0
MIN_TRADES = 100

def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(HUNTER_LOG, "a") as f:
        f.write(line + "\n")

def run_backtest():
    log("Starting 365-day backtest across all agents × 20 symbols...")
    cmd = ["python3", str(WORK / "backtest.py"), "--days", "365", "--symbols", "all"]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORK))
    if out.returncode != 0:
        log(f"BACKTEST FAILED rc={out.returncode}")
        log(out.stderr[-2000:])
        return False
    # Save raw output for forensics
    (WORK / "backtest_output.log").write_text(out.stdout)
    log(f"Backtest done — {len(out.stdout.splitlines())} lines of output")
    return True

def telegram(text):
    """Best-effort telegram ping using same creds as bot."""
    try:
        from dotenv import load_dotenv
        load_dotenv(WORK / ".env")
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat = os.environ.get("TELEGRAM_CHAT_ID")
        if not token or not chat:
            return
        import urllib.request, urllib.parse
        data = urllib.parse.urlencode({
            "chat_id": chat, "text": text, "parse_mode": "HTML"
        }).encode()
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, timeout=10
        )
    except Exception as e:
        log(f"telegram failed: {e}")

def run_parametric():
    """Run parametric_backtest.py to test all candidates in strategy_pool.json."""
    log("Running parametric backtest on strategy pool...")
    cmd = ["python3", str(WORK / "parametric_backtest.py"), "365"]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORK))
    if out.returncode != 0:
        log(f"PARAMETRIC FAILED rc={out.returncode}")
        log(out.stderr[-2000:])
        return None
    # Read pool to find promoted candidates
    pool_path = WORK / "strategy_pool.json"
    if not pool_path.exists():
        return []
    pool = json.loads(pool_path.read_text())
    return [c for c in pool if c.get("recommended")]

def main():
    log("=" * 60)
    log("NIGHTLY HUNTER — start")
    ok = run_backtest()
    if not ok:
        # Silent mode — log only, no Telegram.
        return
    # Run parametric pool backtest
    promoted = run_parametric()
    # Append section to BACKTEST_REPORT.md
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"\n\n## Nightly run — {ts}\n\nThresholds: Sharpe ≥ {MIN_SHARPE}, ExpR ≥ {MIN_EXPR}R, MaxDD ≤ {MAX_DD_PCT}%, Trades ≥ {MIN_TRADES}\n"
    if promoted:
        header += f"\n**Parametric pool: {len(promoted)} new candidates promoted**\n\n"
        for c in promoted[:10]:
            bt = c.get("backtest", {})
            header += f"- `{c['name']}` ({c['template']}): Sharpe={bt.get('sharpe')} ExpR={bt.get('expR')}R trades={bt.get('trades')}\n"
            header += f"  params: `{json.dumps(c['params'])}`\n"
    header += "\nSee `backtest_output.log` for the full agent leaderboard, `strategy_pool.json` for parametric pool.\n"
    with open(REPORT, "a") as f:
        f.write(header)
    # Silent mode: skip Telegram entirely. CEO will read BACKTEST_REPORT.md
    # and propose deploys via the Telegram-reply system if anything is worthy.
    log(f"Done. Promoted candidates: {len(promoted) if promoted else 0}")

if __name__ == "__main__":
    main()
