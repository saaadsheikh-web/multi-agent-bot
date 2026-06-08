#!/usr/bin/env python3
"""
decision_log.py — capture every decision before it becomes a trade.

USAGE FROM AN AGENT
===================

    from decision_log import log_decision

    log_decision(
        agent="connors_rsi2",
        symbol="BTC-USDT",
        action="OPEN_LONG",                   # or OPEN_SHORT, SKIP, CLOSE, ADJUST_STOP
        hypothesis="RSI2=1.8 in uptrend, expect mean-revert bounce to EMA21",
        confidence=8,
        signal_features={                     # whatever the agent computed
            "rsi2": 1.8, "atr_pct": 0.31, "ema21": 65120.4, "trend_score": 0.62,
        },
        plan={
            "entry": 65010.0, "tp": 65380.0, "sl": 64810.0,
            "qty": 0.001, "notional": 65.01, "trail_pct": 0.6,
            "planned_r_multiple": 1.85,
        },
        alternatives_considered=[
            "wait for RSI2<1 — rejected, signal degrading",
            "open at market — chosen for fill certainty",
        ],
        market_context={
            "regime": "uptrend", "hour_utc": 1, "btc_dom": 54.2, "fear_greed": 62,
        },
        custom_id=None,                       # filled in if the trade goes through
    )

Every call appends one JSON line to ~/multi_agent_bot/decision_log.jsonl.
Later we can join decision_log to trade_journal by custom_id (or by
agent+symbol+time-window if custom_id isn't yet known).

The point: capture WHY we considered the trade — even decisions that
end in SKIP, so we can study what we passed on too.
"""
from __future__ import annotations

import os
import json
import datetime as dt
from pathlib import Path
from typing import Any

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
DECISION_LOG = WORK / "decision_log.jsonl"


def log_decision(
    *,
    agent: str,
    symbol: str,
    action: str,
    hypothesis: str,
    confidence: int | float | None = None,
    signal_features: dict[str, Any] | None = None,
    plan: dict[str, Any] | None = None,
    alternatives_considered: list[str] | None = None,
    market_context: dict[str, Any] | None = None,
    custom_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Record a decision. Returns the dict that was written."""
    record = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat() + "Z",
        "agent": agent,
        "symbol": symbol,
        "action": action,
        "hypothesis": hypothesis,
        "confidence": confidence,
        "signal_features": signal_features or {},
        "plan": plan or {},
        "alternatives_considered": alternatives_considered or [],
        "market_context": market_context or {},
        "custom_id": custom_id,
        "extra": extra or {},
    }
    try:
        with open(DECISION_LOG, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        # Never crash the bot because logging failed.
        print(f"[decision_log] failed to write: {e!r}")
    return record


def link_to_trade(custom_id: str, agent: str, symbol: str, ts_window_minutes: int = 5) -> int:
    """
    Backfill custom_id onto any earlier decision rows from the same agent+symbol
    within the last ts_window_minutes. Returns count updated.

    Used right after a trade is actually opened so the decision row gets the
    trade's custom_id stamped on it.
    """
    if not DECISION_LOG.exists():
        return 0
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=ts_window_minutes)
    rows = []
    with open(DECISION_LOG) as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append(r)
    updated = 0
    for r in rows:
        if r.get("custom_id"):
            continue
        if r.get("agent") != agent or r.get("symbol") != symbol:
            continue
        try:
            t = dt.datetime.fromisoformat(r["ts"].replace("Z", ""))
        except Exception:
            continue
        if t >= cutoff:
            r["custom_id"] = custom_id
            updated += 1
    if updated:
        tmp = DECISION_LOG.with_suffix(".jsonl.tmp")
        with open(tmp, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        # On the mount we can write but can't always rename; fall back to
        # overwriting in place if rename fails.
        try:
            os.replace(tmp, DECISION_LOG)
        except Exception:
            with open(DECISION_LOG, "w") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")
            try:
                os.remove(tmp)
            except Exception:
                pass
    return updated


if __name__ == "__main__":
    # Smoke test
    out = log_decision(
        agent="_smoke",
        symbol="TEST-USDT",
        action="SKIP",
        hypothesis="smoke-test entry to verify decision_log.py works",
        confidence=0,
    )
    print("wrote:", out)
