#!/usr/bin/env python3
"""
ceo_brief.py — deterministic precompute for the hourly CEO meeting.

Designed to take the heavy lifting (SQL queries, stats math, log scraping,
scanner-liveness checks) off the LLM so the hourly run can be short and cheap.

The LLM run reads this script's JSON output and only writes the narrative,
devil's-advocate, and the queued actions.

Outputs:
  stdout: JSON brief (one line, machine-readable)
  --human flag: pretty-printed for ad-hoc inspection

Usage from the scheduled task:
    python3 /Users/saad/multi_agent_bot/ceo_brief.py > /tmp/ceo_brief.json
    # then read /tmp/ceo_brief.json in the LLM run
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sqlite3
import statistics
import sys
import time
from datetime import datetime, timezone
from typing import Any

# Derive paths from this script's location so it works in sandbox and on the Mac.
_HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(_HERE, "bot.db")
LOG_PATH = os.path.join(_HERE, "bot.log")

# Same thresholds as SKILL.md so the LLM gets pre-evaluated gates.
WR_KILL_FLOOR        = 30.0   # already auto-killed by signal-time filter
N_HARD_FLOOR         = 5
PF_SUBPAR            = 0.8    # n>=5 and PF<this -> recommend size reduction
PF_KILL_LAST5        = 0.5    # n>=5 and PF<this over last 5 -> autonomous undeploy
CUM_PNL_KILL         = -10.0  # n>=5 and cum_pnl<this -> autonomous undeploy
SCALE_UP_N           = 10
SCALE_UP_PF          = 1.5
SCALE_UP_WR          = 55.0
TIER1_WR_UP          = 60.0   # >20 trades, >this WR + PF>1.7 -> propose +25%
TIER1_PF_UP          = 1.7
TIER1_WR_DOWN        = 45.0   # last 10 below this -> reduce 25%

ACCOUNT_BASE         = 2700.0   # midpoint of 2225-3200 range
EMERGENCY_DROP       = -50.0

MAKER_FEE_ADJ        = 0.0008   # per the SKILL.md note

def fetch_rows() -> list[tuple]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT agent, pnl, pnl_pct, closed_at
        FROM trades
        WHERE status='closed' AND pnl IS NOT NULL
        ORDER BY agent, closed_at
    """)
    rows = cur.fetchall()
    cur.execute("SELECT agent, symbol, side, entry_price, opened_at, notional FROM trades WHERE status='open'")
    opens = cur.fetchall()
    cur.execute("SELECT MAX(closed_at) FROM trades WHERE status='closed'")
    latest = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl IS NOT NULL")
    n_closed = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM trades WHERE status='open'")
    n_open = cur.fetchone()[0]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cur.execute("SELECT COUNT(*), COALESCE(SUM(pnl),0) FROM trades WHERE status='closed' AND pnl IS NOT NULL AND closed_at LIKE ?", (f"{today}%",))
    today_n, today_pnl = cur.fetchone()
    # Last 7 days bucketed
    cur.execute("""
        SELECT substr(closed_at,1,10) AS d, COUNT(*), COALESCE(SUM(pnl),0)
        FROM trades
        WHERE status='closed' AND pnl IS NOT NULL
              AND closed_at >= date('now','-7 days')
        GROUP BY d ORDER BY d
    """)
    last7 = [{"date": d, "n": n, "pnl": float(p)} for d, n, p in cur.fetchall()]
    con.close()
    return rows, opens, latest, n_closed, n_open, today_n, float(today_pnl or 0.0), last7

def per_agent_stats(rows: list[tuple]) -> list[dict]:
    by_agent: dict[str, list[tuple[float, float]]] = {}
    for a, p, pct, _t in rows:
        by_agent.setdefault(a, []).append((float(p), float(pct or 0.0)))
    out = []
    for a, lst in by_agent.items():
        n = len(lst)
        # Real n excludes pnl=0 phantom-init rows (hurst_regime suffers from these)
        real = [(p, pct) for p, pct in lst if p != 0.0]
        n_real = len(real)
        pnls = [p for p, _ in lst]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]   # treats 0 as non-win, conservative
        wr = (len(wins) / n * 100) if n else 0.0
        gw = sum(wins)
        gl = sum(losses)
        avg_w = (sum(wins) / len(wins)) if wins else 0.0
        avg_l = (sum(losses) / len(losses)) if losses else 0.0
        expR_per_trade = (wr/100.0)*avg_w + (1-wr/100.0)*avg_l - MAKER_FEE_ADJ
        sd = statistics.pstdev(pnls) if len(pnls) > 1 else 0.0
        sharpe = ((sum(pnls)/n)/sd*math.sqrt(252)) if sd else 0.0
        pf = (gw/abs(gl)) if gl else float("inf")
        # last 5 / 10 / 20 windows on REAL trades (exclude phantom zeroes)
        def window(lst_real, k):
            tail = lst_real[-k:]
            n_t = len(tail)
            w_t = [p for p, _ in tail if p > 0]
            l_t = [p for p, _ in tail if p <= 0]
            wr_t = (len(w_t)/n_t*100) if n_t else 0.0
            gw_t, gl_t = sum(w_t), sum(l_t)
            pf_t = (gw_t/abs(gl_t)) if gl_t else float("inf")
            return {"n": n_t, "wr": round(wr_t,1),
                    "pf": (round(pf_t,3) if pf_t != float("inf") else None),
                    "net": round(sum(p for p,_ in tail), 4)}
        out.append({
            "agent": a,
            "n": n,
            "n_real": n_real,                  # excludes pnl=0 phantom rows
            "wins": len(wins),
            "losses": len(losses),
            "wr": round(wr, 1),
            "gw": round(gw, 4),
            "gl": round(gl, 4),
            "avg_win": round(avg_w, 4),
            "avg_loss": round(avg_l, 4),
            "net": round(sum(pnls), 4),
            "pf": (round(pf, 3) if pf != float("inf") else None),
            "expR_per_trade": round(expR_per_trade, 5),
            "sharpe_annualized": round(sharpe, 2),
            "last5":  window(real, 5),
            "last10": window(real, 10),
            "last20": window(real, 20),
        })
    out.sort(key=lambda x: -x["n"])
    return out

def evaluate_gates(stats: list[dict]) -> dict:
    """Pre-compute the SKILL.md gates so the LLM doesn't have to.

    Returns a dict with three queues: undeploy_candidates, scale_up_candidates,
    scale_down_candidates. Each entry has a short 'reason' the LLM can quote.
    """
    undeploy = []
    scale_up = []
    scale_down = []
    insufficient = []
    for s in stats:
        a = s["agent"]; n = s["n"]; n_real = s["n_real"]
        wr = s["wr"]; pf = s["pf"] if s["pf"] is not None else 99.0
        net = s["net"]
        last5 = s["last5"]; last10 = s["last10"]; last20 = s["last20"]
        # n-floor uses n_real to avoid acting on phantom-row inflation
        if n_real < N_HARD_FLOOR:
            insufficient.append({"agent": a, "n_real": n_real,
                "reason": f"n_real={n_real} below hard floor {N_HARD_FLOOR}"})
            continue
        if wr < WR_KILL_FLOOR:
            # already filtered at signal-time, but worth recording the formal kill too
            last5_pf = (last5["pf"] if last5["pf"] is not None else 99.0)
            undeploy.append({"agent": a,
                "reason": f"WR={wr}% < {WR_KILL_FLOOR}% (n_real={n_real}); last5 PF={last5_pf}; auto-killed at signal time but a formal undeploy closes the loop"})
            continue
        last5_pf = (last5["pf"] if last5["pf"] is not None else 99.0)
        if last5_pf < PF_KILL_LAST5 or net < CUM_PNL_KILL:
            undeploy.append({"agent": a,
                "reason": f"last5 PF={last5_pf} (<{PF_KILL_LAST5}) or net=${net} (<${CUM_PNL_KILL}); n_real={n_real}"})
            continue
        if pf < PF_SUBPAR:
            scale_down.append({"agent": a,
                "reason": f"lifetime PF={pf} (<{PF_SUBPAR}) with n_real={n_real} — recommend -25% size"})
        # scale-up gate
        if (n_real >= SCALE_UP_N and pf > SCALE_UP_PF and wr > SCALE_UP_WR):
            scale_up.append({"agent": a,
                "reason": f"n_real={n_real}, PF={pf}, WR={wr}% — meets scale-up gate (PF>{SCALE_UP_PF}, WR>{SCALE_UP_WR}%)"})
        # Tier-1 last-20 size signals
        if last20["n"] >= 20:
            l20_pf = last20["pf"] if last20["pf"] is not None else 99.0
            if last20["wr"] > TIER1_WR_UP and l20_pf > TIER1_PF_UP:
                scale_up.append({"agent": a,
                    "reason": f"last20 WR={last20['wr']}% PF={l20_pf} — Tier-1 +25% candidate"})
        if last10["n"] >= 10 and last10["wr"] < TIER1_WR_DOWN:
            scale_down.append({"agent": a,
                "reason": f"last10 WR={last10['wr']}% (<{TIER1_WR_DOWN}%) — auto -25%"})
    return {
        "undeploy_candidates": undeploy,
        "scale_up_candidates": scale_up,
        "scale_down_candidates": scale_down,
        "insufficient_data": insufficient,
    }

_SCAN_RE   = re.compile(r"^([\d\- :,]+) \[INFO\] scan: ")
_SIGNAL_RE = re.compile(r"^([\d\- :,]+) \[INFO\] signals: ")
_REGIME_RE = re.compile(r"^([\d\- :,]+) \[INFO\] regime: (\w+)\s+ADX=([\d\.]+)\s+ATR=([\d\.]+)")
_ERROR_RE  = re.compile(r"^([\d\- :,]+) \[ERROR\] (.+)$")

def _parse_ts(s: str) -> float:
    s = s.strip().replace(",", ".")
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()

def scrape_log(tail_bytes: int = 400_000) -> dict:
    """Scan the tail of bot.log for the most recent scan/signals/regime/error lines.

    bot.log is written without timezone info. We don't try to guess the host's
    TZ; instead, we use the **latest log line we saw** as the "now" reference
    for liveness math. That makes the freshness measurements correct regardless
    of whether the bot host writes timestamps in UTC, PDT, or anything else,
    because we're measuring "time since the most recent log line of type X"
    against "time of the most recent log line of any type."
    """
    if not os.path.exists(LOG_PATH):
        return {"error": "bot.log not found"}
    sz = os.path.getsize(LOG_PATH)
    with open(LOG_PATH, "rb") as f:
        f.seek(max(0, sz - tail_bytes))
        chunk = f.read().decode(errors="replace")
    lines = chunk.split("\n")
    last_scan_ts = last_signals_ts = last_regime_ts = None
    last_any_ts = None
    last_regime = None
    last_adx = last_atr = None
    recent_errors = []
    _GENERIC_TS = re.compile(r"^([\d\- :,]+) \[")
    for ln in lines:
        g = _GENERIC_TS.match(ln)
        if g:
            try:
                last_any_ts = _parse_ts(g.group(1))
            except ValueError:
                pass
        m = _SCAN_RE.match(ln)
        if m:
            last_scan_ts = _parse_ts(m.group(1)); continue
        m = _SIGNAL_RE.match(ln)
        if m:
            last_signals_ts = _parse_ts(m.group(1)); continue
        m = _REGIME_RE.match(ln)
        if m:
            last_regime_ts = _parse_ts(m.group(1))
            last_regime = m.group(2)
            last_adx = float(m.group(3))
            last_atr = float(m.group(4))
            continue
        m = _ERROR_RE.match(ln)
        if m:
            recent_errors.append({"ts": m.group(1).strip(), "msg": m.group(2).strip()[:200]})
    # Use latest log line as reference. Falls back to wall clock if no parse.
    ref = last_any_ts if last_any_ts is not None else time.time()
    def _age(ts):
        if ts is None: return None
        a = ref - ts
        return round(a, 1) if a >= 0 else 0.0   # clamp tiny negatives from ordering
    return {
        "ref_ts": ref,
        "last_scan_age_sec": _age(last_scan_ts),
        "last_signals_age_sec": _age(last_signals_ts),
        "last_regime_age_sec": _age(last_regime_ts),
        "regime": last_regime,
        "adx": last_adx,
        "atr": last_atr,
        "recent_errors": recent_errors[-5:],
    }

def liveness_flags(live: dict) -> list[str]:
    flags = []
    s_age = live.get("last_scan_age_sec")
    r_age = live.get("last_regime_age_sec")
    if s_age is None or s_age > 600:
        # 10× the 60s scan interval is unambiguously broken
        if r_age is not None and r_age < 1800:
            flags.append(f"SCANNER DEAD: last scan {s_age/60:.0f}min ago but regime loop alive ({r_age/60:.1f}min ago) — restart needed")
        else:
            flags.append(f"BOT POSSIBLY DOWN: last scan {s_age/60:.0f}min ago, last regime poll {('?' if r_age is None else f'{r_age/60:.0f}min ago')}")
    sig_age = live.get("last_signals_age_sec")
    if sig_age is not None and sig_age > 600:
        flags.append(f"NO SIGNALS in {sig_age/60:.0f}min — confirm symbols list and scanner")
    return flags

def build_brief() -> dict[str, Any]:
    rows, opens, latest, n_closed, n_open, today_n, today_pnl, last7 = fetch_rows()
    stats = per_agent_stats(rows)
    gates = evaluate_gates(stats)
    live = scrape_log()
    flags = liveness_flags(live)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "db_latest_closed_at": latest,
        "n_closed_total": n_closed,
        "n_open": n_open,
        "open_positions": [
            {"agent": a, "symbol": s, "side": sd, "entry": ep, "opened_at": ot, "notional": nt}
            for a, s, sd, ep, ot, nt in opens
        ],
        "today_n": today_n,
        "today_pnl": round(today_pnl, 4),
        "last7_days": last7,
        "emergency_drawdown_triggered": today_pnl < EMERGENCY_DROP,
        "per_agent": stats,
        "gates": gates,
        "liveness": live,
        "liveness_flags": flags,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", action="store_true",
                    help="Pretty-print JSON to stderr in addition to the machine output")
    args = ap.parse_args()
    brief = build_brief()
    if args.human:
        print(json.dumps(brief, indent=2, default=str))
    else:
        print(json.dumps(brief, default=str))

if __name__ == "__main__":
    main()
