#!/usr/bin/env python3
"""
trade_journal.py — research-grade per-trade forensic journaler.

PHILOSOPHY
==========
Every closed trade is a data sample. We treat each one like a scientific
observation: capture the full pre-trade context, the plan, the execution, and
the post-trade forensics. Nothing is dropped. Everything is computed, scored,
and archived so future analysis can answer questions like:
  - Which agents have the best decision quality, controlling for symbol?
  - When TPs are missed, how far away from TP did we exit?
  - Does the trail-stop give back more than it protects?
  - Do high-confidence trades actually outperform low-confidence ones?
  - Which signal features correlate with winners vs losers?

OUTPUTS (all live in ~/multi_agent_bot)
=======================================
  trade_journal.jsonl       — one JSON record per trade, full data, machine-readable
  TRADE_JOURNAL.md          — human-readable ledger (one row per trade)
  trade_journal_cards/      — one detailed markdown card per trade (forensic detail)
  trade_journal.log         — run log

FIELDS PER RECORD
=================
  Identity:        trade_id, custom_id, agent, profile, symbol, side, confidence
  Plan:            entry_price, qty, notional, tp_price, sl_price, trail_pct,
                   planned_r_multiple, planned_risk_usd, planned_reward_usd
  Signal context:  reason text, signal_features (parsed: RSI, ATR%, hurst, fib,
                   trend_score, ema_slope, z, vwap, funding_rate, regime, etc.)
  Execution:       opened_at, closed_at, exit_price, high_water, low_water,
                   current_stop_at_close
  Outcome:         pnl, pnl_pct, outcome (WIN/LOSS/FLAT), r_multiple_realized
  Forensics:       exit_reason (TP_HIT/SL_HIT/TRAIL_STOP/TIME_OR_MANUAL),
                   mfe_pct, mae_pct, distance_to_tp_at_close, distance_to_sl_at_close,
                   trail_gave_back_pct, hold_minutes, hour_utc, dow,
                   slippage_vs_planned_tp, slippage_vs_planned_sl
  Quality:         decision_quality_grade (A/B/C/D/F) with explicit reason,
                   risk_plan_followed (bool), confidence_calibration (deviation)
  Context flags:   in_dead_zone, in_good_zone, symbol_blacklisted,
                   paper_only, multi_agent_confluence
  Lesson:          single-paragraph plain-English post-mortem ("note")
"""
from __future__ import annotations

import os
import re
import json
import sqlite3
import datetime as dt
from pathlib import Path
from typing import Any

# ──────────────────────────── paths ────────────────────────────
WORK = Path(os.path.expanduser("~/multi_agent_bot"))
DB = WORK / "bot.db"
JOURNAL_MD = WORK / "TRADE_JOURNAL.md"
JOURNAL_JSONL = WORK / "trade_journal.jsonl"
JOURNAL_LOG = WORK / "trade_journal.log"
CARDS_DIR = WORK / "trade_journal_cards"

# ──────────────────────────── context tables ────────────────────────────
# These come from the learning_agent's latest output. Kept in sync manually
# or via update_context_flags() once new learnings publish.
DEAD_HOURS_UTC = {8, 9, 10, 11}
GOOD_HOURS_UTC = {0, 1, 5, 18, 19}
LOSING_SYMBOLS = {"ONDO-USDT", "SUI-USDT", "TON-USDT", "YFI-USDT", "TAO-USDT", "ETH-USDT"}
KILLED_AGENTS = {"hurst_regime", "daily_breakout_24h", "vwap_reversion"}


# ──────────────────────────── logging ────────────────────────────
def log(msg: str) -> None:
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(JOURNAL_LOG, "a") as f:
        f.write(line + "\n")


# ──────────────────────────── persistence ────────────────────────────
def load_journaled_ids() -> set[int]:
    ids: set[int] = set()
    if not JOURNAL_JSONL.exists():
        return ids
    with open(JOURNAL_JSONL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "trade_id" in obj:
                    ids.add(obj["trade_id"])
            except json.JSONDecodeError:
                continue
    return ids


# ──────────────────────────── signal feature parser ────────────────────────────
# The bot writes prose like "Connors RSI2 short: RSI2=97.4, ATR%=0.28, downtrend
# slope-down" into trades.reason. We extract structured features.
SIGNAL_PATTERNS = [
    ("rsi2",          re.compile(r"RSI2\s*=\s*([-\d.]+)", re.I)),
    ("rsi",           re.compile(r"\bRSI\s*=\s*([-\d.]+)", re.I)),
    ("atr_pct",       re.compile(r"ATR%\s*=\s*([-\d.]+)", re.I)),
    ("atr_val",       re.compile(r"\bATR\s*=\s*([-\d.]+)", re.I)),
    ("hurst",         re.compile(r"\bH\s*=\s*([-\d.]+)")),
    ("z_score",       re.compile(r"\bz\s*=\s*([-\d.]+)", re.I)),
    ("ema21",         re.compile(r"EMA21\s*=\s*([-\d.]+)", re.I)),
    ("ema_slope",     re.compile(r"slope\s*=\s*([-\d.]+)", re.I)),
    ("v_ratio",       re.compile(r"v_ratio\s*=\s*([-\d.]+)", re.I)),
    ("funding_rate",  re.compile(r"funding\s*=\s*([-\d.eE+]+)", re.I)),
]
REGIME_KEYWORDS = ["uptrend", "downtrend", "trending", "ranging", "volatile", "flat"]


def parse_signal_features(reason: str | None, meta: dict) -> dict:
    """Extract numeric signal features from prose reason + meta JSON."""
    features: dict[str, Any] = {}
    text = reason or ""
    for name, pat in SIGNAL_PATTERNS:
        m = pat.search(text)
        if m:
            try:
                features[name] = float(m.group(1))
            except ValueError:
                pass
    # Layer in meta fields (these are authoritative when present)
    for key in ("rsi", "atr_val", "atr_pct", "hurst", "z", "v_ratio",
                "funding_rate", "ema_slope", "_trend_score", "_trend_dir",
                "fib_level", "swing_high", "swing_low", "vwap", "strategy"):
        if key in meta:
            features[key.lstrip("_")] = meta[key]
    # Regime: look for keywords in reason
    low = text.lower()
    for kw in REGIME_KEYWORDS:
        if kw in low:
            features.setdefault("regime_hint", kw)
            break
    # Multi-agent confluence in reason text
    if "agents agree" in low or "2 agents" in low or "3 agents" in low:
        features["multi_agent_confluence"] = True
    return features


# ──────────────────────────── classifiers ────────────────────────────
def classify_exit(t: dict) -> str:
    side = (t.get("side") or "").lower()
    exit_price = t.get("exit_price")
    tp = t.get("tp_price")
    sl = t.get("sl_price")
    if exit_price is None:
        return "UNKNOWN"
    tol = max(abs(exit_price) * 0.0005, 1e-8)
    if side == "long":
        if tp is not None and exit_price >= tp - tol:
            return "TP_HIT"
        if sl is not None and exit_price <= sl + tol:
            return "SL_HIT"
    elif side == "short":
        if tp is not None and exit_price <= tp + tol:
            return "TP_HIT"
        if sl is not None and exit_price >= sl - tol:
            return "SL_HIT"
    entry = t.get("entry_price") or 0
    hw = t.get("high_water") or entry
    lw = t.get("low_water") or entry
    if side == "long" and hw > entry * 1.001:
        return "TRAIL_STOP"
    if side == "short" and lw and lw < entry * 0.999:
        return "TRAIL_STOP"
    return "TIME_OR_MANUAL"


# ──────────────────────────── numeric helpers ────────────────────────────
def safe_div(a, b):
    try:
        if b is None or b == 0:
            return None
        return a / b
    except Exception:
        return None


def hold_minutes(t: dict):
    try:
        a = dt.datetime.fromisoformat(t["opened_at"].replace("Z", "+00:00"))
        b = dt.datetime.fromisoformat(t["closed_at"].replace("Z", "+00:00"))
        return round((b - a).total_seconds() / 60.0, 2)
    except Exception:
        return None


def compute_risk_metrics(t: dict) -> dict:
    """Risk plan: how far is TP and SL from entry, what R:R was planned,
    what fraction of risk was actually realized."""
    side = (t.get("side") or "").lower()
    entry = t.get("entry_price")
    tp = t.get("tp_price")
    sl = t.get("sl_price")
    qty = t.get("qty") or 0
    notional = t.get("notional") or 0
    exit_price = t.get("exit_price")
    pnl = t.get("pnl") or 0

    out: dict[str, Any] = {
        "planned_tp_distance_pct": None,
        "planned_sl_distance_pct": None,
        "planned_r_multiple": None,
        "planned_risk_usd": None,
        "planned_reward_usd": None,
        "realized_r_multiple": None,
        "exit_distance_from_tp_pct": None,
        "exit_distance_from_sl_pct": None,
        "slippage_vs_tp_pct": None,
        "slippage_vs_sl_pct": None,
    }
    if not entry:
        return out

    if side == "long":
        if tp:
            out["planned_tp_distance_pct"] = round(((tp - entry) / entry) * 100, 4)
        if sl:
            out["planned_sl_distance_pct"] = round(((entry - sl) / entry) * 100, 4)
        if exit_price and tp:
            out["exit_distance_from_tp_pct"] = round(((tp - exit_price) / entry) * 100, 4)
        if exit_price and sl:
            out["exit_distance_from_sl_pct"] = round(((exit_price - sl) / entry) * 100, 4)
    elif side == "short":
        if tp:
            out["planned_tp_distance_pct"] = round(((entry - tp) / entry) * 100, 4)
        if sl:
            out["planned_sl_distance_pct"] = round(((sl - entry) / entry) * 100, 4)
        if exit_price and tp:
            out["exit_distance_from_tp_pct"] = round(((exit_price - tp) / entry) * 100, 4)
        if exit_price and sl:
            out["exit_distance_from_sl_pct"] = round(((sl - exit_price) / entry) * 100, 4)

    # Planned R-multiple (reward / risk)
    if out["planned_tp_distance_pct"] and out["planned_sl_distance_pct"]:
        out["planned_r_multiple"] = round(
            out["planned_tp_distance_pct"] / out["planned_sl_distance_pct"], 3
        )
    # Dollar risk / reward (sign-naive)
    if tp and sl and qty:
        out["planned_risk_usd"] = round(abs(entry - sl) * qty, 4)
        out["planned_reward_usd"] = round(abs(tp - entry) * qty, 4)
    # Realized R-multiple = pnl / planned_risk_usd
    if out["planned_risk_usd"]:
        out["realized_r_multiple"] = round(pnl / out["planned_risk_usd"], 3)
    out["notional"] = notional
    return out


def compute_mfe_mae_proxy(t: dict) -> dict:
    """
    Maximum favorable / adverse excursion proxy from high_water / low_water.

    high_water / low_water are the best/worst prices observed during the
    trade's lifetime. From them we approximate MFE (best unrealized profit)
    and MAE (worst unrealized drawdown) in pct of entry.
    """
    side = (t.get("side") or "").lower()
    entry = t.get("entry_price")
    hw = t.get("high_water")
    lw = t.get("low_water")
    out = {"mfe_pct": None, "mae_pct": None, "trail_gave_back_pct": None}
    if not entry or hw is None or lw is None:
        return out
    if side == "long":
        out["mfe_pct"] = round(((hw - entry) / entry) * 100, 4)
        out["mae_pct"] = round(((lw - entry) / entry) * 100, 4)
        exit_price = t.get("exit_price")
        if exit_price and hw > entry:
            out["trail_gave_back_pct"] = round(((hw - exit_price) / entry) * 100, 4)
    elif side == "short":
        out["mfe_pct"] = round(((entry - lw) / entry) * 100, 4)
        out["mae_pct"] = round(((entry - hw) / entry) * 100, 4)
        exit_price = t.get("exit_price")
        if exit_price and lw and lw < entry:
            out["trail_gave_back_pct"] = round(((exit_price - lw) / entry) * 100, 4)
    return out


def grade_decision(t: dict, exit_reason: str, risk: dict, mfe_mae: dict, flags: dict) -> dict:
    """
    Assign a decision-quality letter grade A-F with explicit reason.

    Grade is about decision quality independent of outcome:
      - Entering with positive expectancy (good R:R, agent confluence, no flagged
        symbol, not in dead zone) and respecting risk plan = high grade.
      - Entering on a flagged symbol in a dead zone with a thin TP = low grade,
        even if it happened to win.
    """
    score = 100
    reasons = []
    if flags.get("symbol_blacklisted"):
        score -= 30; reasons.append("flagged-losing-symbol")
    if flags.get("in_dead_zone"):
        score -= 15; reasons.append("dead-zone-hour")
    if flags.get("agent_killed"):
        score -= 25; reasons.append("agent-on-kill-list")
    rr = risk.get("planned_r_multiple")
    if rr is not None:
        if rr < 1.0:
            score -= 20; reasons.append(f"poor planned R:R={rr}")
        elif rr >= 2.0:
            score += 10; reasons.append(f"strong planned R:R={rr}")
    if flags.get("multi_agent_confluence"):
        score += 10; reasons.append("multi-agent confluence")
    if exit_reason == "SL_HIT" and (risk.get("planned_sl_distance_pct") or 0) > 5:
        score -= 10; reasons.append("wide stop hit")
    if exit_reason == "TIME_OR_MANUAL" and (t.get("pnl") or 0) < 0:
        score -= 10; reasons.append("timed-out loser (no clean exit signal)")
    conf = t.get("confidence")
    if conf is not None:
        pnl = t.get("pnl") or 0
        if conf >= 8 and pnl < 0:
            reasons.append(f"high confidence ({conf}) lost")
        if conf <= 4 and pnl > 0:
            reasons.append(f"low confidence ({conf}) won")
    score = max(0, min(100, score))
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 45 else "F"
    return {"decision_score": score, "decision_grade": grade, "decision_reasons": reasons}


# ──────────────────────────── narrative ────────────────────────────
def make_note(t: dict, outcome: str, exit_reason: str, hour: int,
              hold: float | None, risk: dict, mfe_mae: dict,
              flags: dict, decision: dict, features: dict) -> tuple[str, list[str]]:
    tags: list[str] = []
    pieces: list[str] = []
    side = (t.get("side") or "").lower()
    agent = t.get("agent") or "?"
    symbol = t.get("symbol") or "?"
    pnl_pct = t.get("pnl_pct")

    # Opener
    if outcome == "WIN":
        if exit_reason == "TP_HIT":
            pieces.append(f"Clean {side} TP hit")
        elif exit_reason == "TRAIL_STOP":
            pieces.append(f"{side.title()} trailed into profit")
        else:
            pieces.append(f"{side.title()} timed out in profit")
    elif outcome == "LOSS":
        if exit_reason == "SL_HIT":
            pieces.append(f"{side.title()} stopped out at full risk")
        elif exit_reason == "TRAIL_STOP":
            pieces.append(f"{side.title()} gave back gains on trail")
        else:
            pieces.append(f"{side.title()} closed in the red without clean exit")
    else:
        pieces.append(f"{side.title()} flat exit (scratch)")

    pieces.append(f"on {symbol} ({agent}, {pnl_pct:+.2f}%)" if pnl_pct is not None else f"on {symbol} ({agent})")

    # Hour
    if hour in DEAD_HOURS_UTC:
        pieces.append(f"during dead-zone hour {hour:02d}:00 UTC"); tags.append("dead_hour")
    elif hour in GOOD_HOURS_UTC:
        pieces.append(f"during good-zone hour {hour:02d}:00 UTC"); tags.append("good_hour")

    # Symbol flag
    if flags.get("symbol_blacklisted"):
        pieces.append("[flagged-losing-symbol]"); tags.append("losing_symbol")
    if flags.get("agent_killed"):
        pieces.append("[killed-agent]"); tags.append("killed_agent")
    if flags.get("multi_agent_confluence"):
        tags.append("confluence")

    # MFE/MAE color
    if mfe_mae.get("mfe_pct") is not None and outcome == "LOSS":
        if mfe_mae["mfe_pct"] > 0.5:
            pieces.append(f"(was up {mfe_mae['mfe_pct']:.2f}% before reversing)")
            tags.append("gave_back_winner")
    if mfe_mae.get("trail_gave_back_pct") is not None and mfe_mae["trail_gave_back_pct"] > 0.5:
        pieces.append(f"trail gave back {mfe_mae['trail_gave_back_pct']:.2f}%")
        tags.append("trail_too_loose")

    # Hold-time
    if hold is not None:
        if hold < 5:
            tags.append("very_short_hold")
        elif hold > 240:
            tags.append("long_hold")

    # Side / outcome cross-tags
    if side == "long" and outcome == "LOSS":
        tags.append("long_loss")
    if side == "short" and outcome == "WIN":
        tags.append("short_win")
    tags.append(exit_reason.lower())

    # Grade
    pieces.append(f"[grade {decision['decision_grade']} / {decision['decision_score']}]")
    tags.append(f"grade_{decision['decision_grade']}")

    return " ".join(pieces) + ".", tags


# ──────────────────────────── builder ────────────────────────────
def build_entry(t: dict) -> dict:
    pnl = float(t.get("pnl") or 0)
    outcome = "WIN" if pnl > 0 else ("LOSS" if pnl < 0 else "FLAT")
    exit_reason = classify_exit(t)
    hold = hold_minutes(t)
    try:
        hour = int(t["closed_at"][11:13])
    except Exception:
        hour = -1
    try:
        dow = dt.datetime.fromisoformat(t["closed_at"].replace("Z", "+00:00")).strftime("%a")
    except Exception:
        dow = "?"

    meta = {}
    try:
        meta = json.loads(t.get("meta") or "{}")
    except Exception:
        pass

    features = parse_signal_features(t.get("reason"), meta)
    risk = compute_risk_metrics(t)
    mfe_mae = compute_mfe_mae_proxy(t)

    flags = {
        "in_dead_zone": hour in DEAD_HOURS_UTC,
        "in_good_zone": hour in GOOD_HOURS_UTC,
        "symbol_blacklisted": (t.get("symbol") or "") in LOSING_SYMBOLS,
        "agent_killed": (t.get("agent") or "") in KILLED_AGENTS,
        "paper_only": bool(meta.get("_paper_only")),
        "multi_agent_confluence": bool(features.get("multi_agent_confluence")),
    }
    decision = grade_decision(t, exit_reason, risk, mfe_mae, flags)
    note, tags = make_note(t, outcome, exit_reason, hour, hold, risk, mfe_mae, flags, decision, features)

    return {
        # Identity
        "trade_id": t["id"],
        "custom_id": t.get("custom_id"),
        "agent": t.get("agent"),
        "profile": t.get("profile"),
        "symbol": t.get("symbol"),
        "side": t.get("side"),
        "confidence": t.get("confidence"),
        "reason_text": t.get("reason"),
        # Plan
        "entry_price": t.get("entry_price"),
        "exit_price": t.get("exit_price"),
        "tp_price": t.get("tp_price"),
        "sl_price": t.get("sl_price"),
        "qty": t.get("qty"),
        "notional": t.get("notional"),
        "trail_pct": t.get("trail_pct"),
        "high_water": t.get("high_water"),
        "low_water": t.get("low_water"),
        "current_stop_at_close": t.get("current_stop"),
        # Timing
        "opened_at": t.get("opened_at"),
        "closed_at": t.get("closed_at"),
        "hour_utc": hour,
        "dow": dow,
        "hold_minutes": hold,
        # Outcome
        "outcome": outcome,
        "pnl": pnl,
        "pnl_pct": t.get("pnl_pct"),
        # Forensics
        "exit_reason": exit_reason,
        "risk": risk,
        "mfe_mae": mfe_mae,
        # Signal context
        "signal_features": features,
        "meta_raw": meta,
        # Decision quality
        "flags": flags,
        "decision": decision,
        # Narrative
        "note": note,
        "tags": tags,
        # Provenance
        "journaled_at": dt.datetime.now(dt.timezone.utc).isoformat() + "Z",
        "journaler_version": 2,
    }


# ──────────────────────────── writers ────────────────────────────
def append_jsonl(rows: list[dict]) -> None:
    if not rows:
        return
    with open(JOURNAL_JSONL, "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def append_md(rows: list[dict]) -> None:
    if not rows:
        return
    new_file = not JOURNAL_MD.exists()
    with open(JOURNAL_MD, "a") as f:
        if new_file:
            f.write("# Trade Journal\n\n")
            f.write("Auto-generated per-trade ledger. See `trade_journal_cards/` for full forensic detail per trade.\n\n")
            f.write("| closed_at | id | grade | outcome | reason | pnl | hold(min) | note |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            closed = (r.get("closed_at") or "")[:19]
            f.write(
                f"| {closed} | {r['trade_id']} | {r['decision']['decision_grade']} | "
                f"{r['outcome']} | {r['exit_reason']} | {r['pnl']:+.2f} | "
                f"{r['hold_minutes']} | {r['note']} |\n"
            )


def write_card(r: dict) -> None:
    """Per-trade forensic markdown card."""
    CARDS_DIR.mkdir(exist_ok=True)
    path = CARDS_DIR / f"trade_{r['trade_id']:04d}_{r['custom_id'] or 'na'}.md"

    risk = r["risk"]; mfe = r["mfe_mae"]; flags = r["flags"]; dec = r["decision"]

    def kv(d: dict) -> str:
        return "\n".join(f"- **{k}**: {v}" for k, v in d.items() if v is not None and v != [])

    md = f"""# Trade #{r['trade_id']} — {r['symbol']} {r['side']} ({r['agent']})

**Outcome:** {r['outcome']} · **PnL:** {r['pnl']:+.4f} ({r['pnl_pct']:+.3f}% if pct available) · **Decision grade:** {dec['decision_grade']} ({dec['decision_score']}/100) · **Hold:** {r['hold_minutes']} min

> {r['note']}

## 1 · Identity
- custom_id: `{r['custom_id']}`
- agent: `{r['agent']}` · profile: `{r['profile']}`
- symbol: `{r['symbol']}` · side: `{r['side']}`
- confidence: {r['confidence']}
- opened: `{r['opened_at']}`
- closed: `{r['closed_at']}` · hour UTC {r['hour_utc']:02d} ({r['dow']})

## 2 · Hypothesis (why we entered)
> {r['reason_text']}

### Parsed signal features
{kv(r['signal_features']) or '_(none parseable)_'}

### Raw meta from agent
```json
{json.dumps(r['meta_raw'], indent=2)}
```

## 3 · Plan vs Execution
- entry_price: {r['entry_price']}
- exit_price: {r['exit_price']}
- tp_price: {r['tp_price']}
- sl_price: {r['sl_price']}
- qty: {r['qty']} · notional: {r['notional']}
- trail_pct: {r['trail_pct']}

### Risk plan
{kv(risk)}

### Market excursion (MFE / MAE proxy)
- high_water: {r['high_water']} · low_water: {r['low_water']}
- current_stop_at_close: {r['current_stop_at_close']}
{kv(mfe)}

## 4 · Forensics
- **exit_reason:** `{r['exit_reason']}`
- realized_r_multiple: {risk.get('realized_r_multiple')}
- slippage vs planned TP: {risk.get('exit_distance_from_tp_pct')}%
- slippage vs planned SL: {risk.get('exit_distance_from_sl_pct')}%

## 5 · Context flags
{kv(flags)}

## 6 · Decision quality
- **grade:** {dec['decision_grade']} ({dec['decision_score']}/100)
- factors:
"""
    for line in dec["decision_reasons"] or ["(no notable factors)"]:
        md += f"  - {line}\n"
    md += "\n## 7 · Tags\n"
    md += ", ".join(f"`{t}`" for t in r["tags"]) + "\n"
    md += f"\n---\n*journaled_at {r['journaled_at']} · journaler v{r['journaler_version']}*\n"

    with open(path, "w") as f:
        f.write(md)


# ──────────────────────────── runner ────────────────────────────
def run() -> dict:
    log("=== trade journal v2 run start ===")
    if not DB.exists():
        log("no bot.db; nothing to journal")
        return {"new": 0, "total": 0}

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM trades WHERE status='closed' AND closed_at IS NOT NULL ORDER BY closed_at ASC"
    ).fetchall()]
    conn.close()

    already = load_journaled_ids()
    new_trades = [t for t in rows if t["id"] not in already]
    log(f"closed trades: {len(rows)} · already journaled: {len(already)} · new: {len(new_trades)}")

    entries = [build_entry(t) for t in new_trades]
    append_jsonl(entries)
    append_md(entries)
    for e in entries:
        try:
            write_card(e)
        except Exception as ex:
            log(f"card write failed for trade {e.get('trade_id')}: {ex!r}")

    log(f"journaled {len(entries)} new trades. Total in journal: {len(already)+len(entries)}.")
    log("=== done ===")
    return {"new": len(entries), "total": len(already) + len(entries), "all_closed": len(rows)}


if __name__ == "__main__":
    run()
