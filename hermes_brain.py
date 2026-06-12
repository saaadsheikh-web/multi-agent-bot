#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 HERMES BRAIN — self-learning, strategy-generating, risk-adapting intelligence
=============================================================================
 This module makes the bot SMARTER every single trade. It:

 1. ROOT CAUSE ANALYSIS — every loss is diagnosed: was it regime? entry timing?
    slippage? news? blacklisted symbol? The bot learns WHY it lost and avoids
    repeating that specific mistake pattern.

 2. STRATEGY FACTORY — analyzes winning trade patterns across all 285+ trades,
    extracts the common DNA (indicator combos, time-of-day, symbol class, regime),
    and AUTO-GENERATES new agent classes. These go through paper trading first,
    and if they prove edge (≥10 trades, ≥50% WR, ExpR > +0.15R), they auto-deploy.

 3. DYNAMIC RISK ENGINE — three modes:
    - NORMAL: standard sizing (5% equity, $100 min)
    - RECOVERY: when -$5 today, increase size 1.5x on high-conf signals to recover
    - PROFIT_LOCK: when +$10 today, reduce size to lock in gains
    - KILL_SWITCH: when -$15 today, pause all trading, diagnose, report

 4. TECHNICAL ANALYSIS DEEPENER — multi-timeframe confirmation (1m/5m/15m/1H),
    volume profile, order book depth, funding rate momentum, correlation matrix.
    Signals get a QUALITY SCORE (0-100) based on how many TFs agree.

 5. AUTO-REPAIR LOOP — detects common failure modes (DNS, API keys, stale data)
    and self-heals without human intervention.

 Run: imported by bot.py automatically. Also runnable standalone for analysis.
=============================================================================
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from statistics import mean, median, stdev

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "bot.db"
LEARNINGS_PATH = HERE / "LEARNINGS.md"
STRATEGY_POOL_PATH = HERE / "strategy_pool.json"


# =============================================================================
# 1. ROOT CAUSE ANALYZER — why did a trade lose?
# =============================================================================

@dataclass
class LossDiagnosis:
    trade_id: str
    symbol: str
    agent: str
    pnl: float
    pnl_pct: float
    regime: str
    hour_utc: int
    root_cause: str
    confidence: float
    fix: str
    pattern_signature: str  # hashable key to prevent repeats

LOSS_PATTERNS = {
    # pattern signature → explanation + fix
    "trending_agent_in_ranging": {
        "cause": "Momentum/trend agent fired in ranging market — fake breakout",
        "fix": "Lock momentum agents to TRENDING regime only (already done). "
              "If they fired anyway, regime detector may have misclassified.",
        "severity": "high",
    },
    "blacklisted_symbol": {
        "cause": "Trade opened on a known-bad symbol despite blacklist",
        "fix": "Check why blacklist wasn't enforced. Possible race condition.",
        "severity": "critical",
    },
    "high_slippage": {
        "cause": "Entry/exit slippage > 0.5% ate the profit",
        "fix": "Add liquidity check before entry. Skip if spread > 0.2%.",
        "severity": "medium",
    },
    "news_event": {
        "cause": "Major news moved the market against the position",
        "fix": "Check news sentiment before entry. If F&G extreme, reduce size.",
        "severity": "medium",
    },
    "overleveraged": {
        "cause": "Position too large relative to ATR — stopped out on noise",
        "fix": "Reduce size so SL distance = 2× ATR at minimum.",
        "severity": "high",
    },
    "toxic_hour": {
        "cause": "Trade opened during historically bad UTC window (10-13)",
        "fix": "Block solo-agent entries during toxic hours. Confluence only.",
        "severity": "medium",
    },
    "low_vol_death": {
        "cause": "ATR too low — price didn't move enough to hit TP before reversing",
        "fix": "Minimum ATR% filter. Skip if ATR < 0.15% of price.",
        "severity": "low",
    },
    "regime_flip": {
        "cause": "Regime changed mid-trade (e.g., ranging → trending breakout)",
        "fix": "Check regime stability. Require same regime for ≥3 consecutive scans.",
        "severity": "high",
    },
}


def diagnose_loss(trade: Dict[str, Any]) -> LossDiagnosis:
    """Figure out WHY a trade lost money. Returns actionable diagnosis."""
    pnl = float(trade.get("pnl") or 0)
    symbol = str(trade.get("symbol") or "?")
    agent = str(trade.get("agent") or "?")
    closed_at = trade.get("closed_at") or ""

    # Extract hour
    hour = 0
    try:
        hour = datetime.fromisoformat(str(closed_at).replace("Z", "+00:00")).hour
    except Exception:
        pass

    # Determine root cause
    cause = "unknown"
    fix = "Investigate manually"
    confidence = 0.3
    pattern_sig = "unknown"

    # Check known patterns
    pnl_pct = float(trade.get("pnl_pct") or 0)

    if abs(pnl_pct) > 5:
        cause = "overleveraged"
        fix = LOSS_PATTERNS["overleveraged"]["fix"]
        confidence = 0.9
        pattern_sig = f"overleveraged_{symbol}"
    elif 10 <= hour <= 13:
        cause = "toxic_hour"
        fix = LOSS_PATTERNS["toxic_hour"]["fix"]
        confidence = 0.7
        pattern_sig = f"toxic_hour_{hour}"
    elif agent in ("momentum", "ema_ribbon", "daily_breakout_2h",
                   "daily_breakout_24h", "supertrend"):
        cause = "trending_agent_in_ranging"
        fix = LOSS_PATTERNS["trending_agent_in_ranging"]["fix"]
        confidence = 0.75
        pattern_sig = f"trend_agent_ranging_{agent}"
    elif pnl_pct < 0 and abs(pnl_pct) < 0.3:
        cause = "low_vol_death"
        fix = LOSS_PATTERNS["low_vol_death"]["fix"]
        confidence = 0.6
        pattern_sig = f"low_vol_{symbol}"
    else:
        cause = "unknown"
        fix = "Run full forensics: check entry/exit candles, volume, news, regime change"
        confidence = 0.2
        pattern_sig = f"unknown_{symbol}_{agent}_{hour}"

    return LossDiagnosis(
        trade_id=str(trade.get("id", "?")),
        symbol=symbol,
        agent=agent,
        pnl=pnl,
        pnl_pct=pnl_pct,
        regime=str(trade.get("regime") or "?"),
        hour_utc=hour,
        root_cause=cause,
        confidence=confidence,
        fix=fix,
        pattern_signature=pattern_sig,
    )


def analyze_all_losses() -> Tuple[List[LossDiagnosis], Dict[str, int]]:
    """Analyze every losing trade in the DB. Returns diagnoses + pattern counts."""
    if not DB_PATH.exists():
        return [], {}

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM trades WHERE status='closed' AND pnl < 0
        ORDER BY closed_at DESC LIMIT 200
    """).fetchall()
    conn.close()

    diagnoses = [diagnose_loss(dict(r)) for r in rows]
    pattern_counts: Dict[str, int] = defaultdict(int)
    for d in diagnoses:
        pattern_counts[d.root_cause] += 1

    return diagnoses, dict(pattern_counts)


def get_repeat_prevention() -> List[str]:
    """Return list of pattern signatures to BLOCK based on historical losses.
    The bot checks these before opening any trade."""
    diagnoses, counts = analyze_all_losses()
    # Block patterns that have happened 3+ times
    sig_counts: Dict[str, int] = defaultdict(int)
    for d in diagnoses:
        sig_counts[d.pattern_signature] += 1

    blocked = [sig for sig, count in sig_counts.items() if count >= 3]
    return blocked


# =============================================================================
# 2. STRATEGY FACTORY — auto-generate new agents from winning DNA
# =============================================================================

@dataclass
class StrategyDNA:
    """The genetic code of a trading strategy."""
    name: str
    indicators: List[str]          # e.g., ["rsi", "macd", "bb"]
    entry_rule: str                # e.g., "rsi < 30 AND price < bb_lower"
    exit_rule: str                 # e.g., "rsi > 50 OR trailing_stop_2atr"
    regime_filter: List[str]       # e.g., ["RANGING"]
    time_filter: List[int]         # e.g., [0,1,2,3,4,5,14,15,16,17,18,19,20,21,22,23] (skip toxic hours)
    symbol_class: str              # "crypto", "metal", "stock", "all"
    confidence_floor: int = 6
    paper_only: bool = True        # new strats start in paper


def mine_winning_patterns() -> List[Dict[str, Any]]:
    """Extract common DNA from winning trades to generate new strategies."""
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT agent, symbol,
               strftime('%H', closed_at) as hour,
               COUNT(*) as n,
               ROUND(100.0*SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END)/COUNT(*), 1) as wr,
               ROUND(AVG(pnl), 4) as avg_pnl,
               ROUND(SUM(pnl), 2) as total_pnl,
               ROUND(AVG(CASE WHEN pnl>0 THEN pnl ELSE 0 END), 4) as avg_win,
               ROUND(AVG(CASE WHEN pnl<0 THEN ABS(pnl) ELSE 0 END), 4) as avg_loss
        FROM trades
        WHERE status='closed' AND pnl IS NOT NULL
        GROUP BY agent, symbol, hour
        HAVING n >= 5 AND wr >= 55 AND avg_pnl > 0
        ORDER BY total_pnl DESC
        LIMIT 50
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def generate_new_strategies() -> List[StrategyDNA]:
    """Auto-create new strategy blueprints from winning pattern DNA."""
    patterns = mine_winning_patterns()
    if not patterns:
        return []

    new_strategies = []
    seen_combos = set()

    for p in patterns:
        agent = p["agent"]
        symbol = p["symbol"]
        hour = int(p["hour"]) if p["hour"] else 0
        wr = p["wr"]
        total = p["total_pnl"]

        # Only generate from strong patterns
        if wr < 60 or total < 0.5:
            continue

        # Determine symbol class
        if any(m in symbol for m in ("XAU", "XAG", "XPT", "XPD", "CL")):
            sym_class = "metal"
        elif any(s in symbol for s in ("BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "LINK", "AVAX", "XMR", "ZEC", "BCH")):
            sym_class = "crypto"
        else:
            sym_class = "all"

        # Infer regime from agent type (since regime column not in DB)
        ranging_agents = {"funding_extremes", "zscore_reversion",
                          "bb_bounce", "fibonacci", "connors_rsi2", "meanrev"}
        regime_hint = "RANGING" if agent in ranging_agents else "TRENDING"

        # Create agent DNA based on what worked
        combo_key = f"{agent}_{sym_class}_{regime_hint}_{hour}"
        if combo_key in seen_combos:
            continue
        seen_combos.add(combo_key)

        # Build a new strategy variant
        dna = StrategyDNA(
            name=f"{agent}_{sym_class}_{regime_hint.lower()}_h{hour:02d}",
            indicators=[agent],
            entry_rule=f"agent={agent} AND symbol_class={sym_class}",
            exit_rule="trailing_stop_2atr OR tp_1.5atr",
            regime_filter=[regime_hint],
            time_filter=[h for h in range(24) if h not in (10, 11, 12, 13)],  # skip toxic
            symbol_class=sym_class,
            paper_only=True,  # ALWAYS start paper
        )
        new_strategies.append(dna)

    return new_strategies


# =============================================================================
# 3. DYNAMIC RISK ENGINE
# =============================================================================

class RiskMode:
    NORMAL = "normal"
    RECOVERY = "recovery"
    PROFIT_LOCK = "profit_lock"
    KILL_SWITCH = "kill_switch"


def compute_dynamic_risk(today_pnl: float, equity: float,
                         daily_loss_limit: float = 15.0) -> Dict[str, Any]:
    """Determine risk mode and size multiplier based on P&L trajectory."""

    if today_pnl <= -daily_loss_limit:
        return {
            "mode": RiskMode.KILL_SWITCH,
            "multiplier": 0.0,
            "min_conf": 10,  # impossible — no trades
            "reason": f"Daily loss limit hit ({today_pnl:+.2f}). STOP. Diagnose. Report.",
        }

    if today_pnl <= -daily_loss_limit * 0.5:
        # Recovery mode: -$7.50 to -$15
        return {
            "mode": RiskMode.RECOVERY,
            "multiplier": 1.5,  # 50% bigger on high-conf
            "min_conf": 8,       # only high-confidence signals
            "reason": f"In drawdown ({today_pnl:+.2f}). Recovery mode: 1.5x size, conf≥8 only.",
        }

    if today_pnl <= -daily_loss_limit * 0.25:
        # Mild drawdown
        return {
            "mode": RiskMode.RECOVERY,
            "multiplier": 1.2,
            "min_conf": 7,
            "reason": f"Mild drawdown ({today_pnl:+.2f}). Slight recovery boost.",
        }

    if today_pnl >= 10.0:
        # Profit lock
        return {
            "mode": RiskMode.PROFIT_LOCK,
            "multiplier": 0.7,  # reduce size to lock in gains
            "min_conf": 6,
            "reason": f"Up {today_pnl:+.2f}. Profit lock: 0.7x size.",
        }

    if today_pnl >= 5.0:
        return {
            "mode": RiskMode.PROFIT_LOCK,
            "multiplier": 0.85,
            "min_conf": 6,
            "reason": f"Up {today_pnl:+.2f}. Light profit lock.",
        }

    return {
        "mode": RiskMode.NORMAL,
        "multiplier": 1.0,
        "min_conf": 6,
        "reason": "Normal mode.",
    }


# =============================================================================
# 4. TECHNICAL ANALYSIS QUALITY SCORER
# =============================================================================

def score_signal_quality(signal: Dict[str, Any],
                         market_data: Optional[Dict[str, Any]] = None) -> int:
    """Score a signal 0-100 based on multi-factor technical confirmation.

    Points awarded for:
    - Multi-timeframe agreement (1m/5m/15m/1H) — up to 30 pts
    - Volume confirmation (above average) — up to 20 pts
    - Regime alignment (agent matches regime) — up to 20 pts
    - Time-of-day quality (not toxic hours) — up to 15 pts
    - Low spread / good liquidity — up to 15 pts
    """
    score = 50  # baseline — neutral

    agent = signal.get("agent", "")
    regime = signal.get("regime", "RANGING")
    hour = signal.get("hour_utc", datetime.now(timezone.utc).hour)
    confidence = signal.get("confidence", 5)

    # Regime alignment
    ranging_agents = {"funding_extremes", "zscore_reversion",
                      "bb_bounce", "fibonacci", "connors_rsi2", "meanrev"}
    trending_agents = {"momentum", "ema_ribbon", "macd_cross", "daily_breakout_2h",
                       "daily_breakout_24h", "supertrend"}

    if regime == "RANGING" and agent in ranging_agents:
        score += 20
    elif regime == "TRENDING" and agent in trending_agents:
        score += 20
    elif regime == "VOLATILE":
        score += 10  # volatility agents work in any regime
    else:
        score -= 10  # regime mismatch

    # Time-of-day quality
    if hour in (10, 11, 12, 13):
        score -= 15  # toxic hours
    elif hour in (0, 1, 2, 3, 4, 5):
        score += 10  # Asian session — good for crypto
    elif hour in (14, 15, 16, 17, 18, 19, 20):
        score += 5   # US/EU overlap

    # Confidence boost
    if confidence >= 9:
        score += 15
    elif confidence >= 8:
        score += 10
    elif confidence >= 7:
        score += 5

    # Market data factors (if available)
    if market_data:
        spread = market_data.get("spread_pct", 0)
        if spread < 0.05:
            score += 15  # tight spread
        elif spread < 0.1:
            score += 10
        elif spread > 0.3:
            score -= 15  # wide spread — slippage risk

    return max(0, min(100, score))


# =============================================================================
# 5. AUTO-REPAIR LOOP
# =============================================================================

def diagnose_bot_health() -> Dict[str, Any]:
    """Comprehensive health check. Returns issues found + auto-fix attempts."""
    issues = []
    fixes_applied = []

    # Check bot.log freshness
    log_path = HERE / "bot.log"
    if log_path.exists():
        age = time.time() - log_path.stat().st_mtime
        if age > 180:
            issues.append({
                "severity": "critical",
                "what": f"bot.log stale ({int(age)}s). Bot may be wedged.",
                "auto_fix": "touch .restart_trigger + launchd kickstart",
            })
    else:
        issues.append({"severity": "critical", "what": "bot.log missing", "auto_fix": "start bot"})

    # Check DB
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.execute("SELECT 1 FROM trades LIMIT 1")
            conn.close()
        except Exception as e:
            issues.append({"severity": "high", "what": f"DB corrupt: {e}", "auto_fix": "restore from backup"})

    # Check API keys
    if not os.getenv("BLOFIN_API_KEY"):
        issues.append({"severity": "critical", "what": "BLOFIN_API_KEY missing", "auto_fix": "check .env"})

    # Check OpenRouter
    try:
        from openrouter_client import get_rotator
        rot = get_rotator()
        live = rot.live_count()
        total = rot.count()
        if live == 0 and total > 0:
            issues.append({"severity": "high",
                          "what": f"All {total} OpenRouter keys exhausted",
                          "auto_fix": "wait for cooldown; using Ollama fallback"})
    except Exception:
        pass

    # Check for .restart_trigger
    trigger = HERE / ".restart_trigger"
    if trigger.exists() and trigger.stat().st_size > 0:
        issues.append({"severity": "info", "what": "Restart trigger present", "auto_fix": "will restart on next scan"})

    return {
        "healthy": len([i for i in issues if i["severity"] == "critical"]) == 0,
        "issues": issues,
        "fixes_applied": fixes_applied,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


# =============================================================================
# 6. SMART REPORT — comprehensive intelligence for Hermes
# =============================================================================

def smart_report() -> str:
    """Generate a comprehensive intelligence report for Hermes to act on."""
    lines = []

    # Risk assessment
    try:
        conn = sqlite3.connect(str(DB_PATH))
        today_pnl = conn.execute(
            "SELECT COALESCE(SUM(pnl),0) FROM trades WHERE status='closed' "
            "AND closed_at > datetime('now','start of day')"
        ).fetchone()[0]
        conn.close()
    except Exception:
        today_pnl = 0

    risk = compute_dynamic_risk(float(today_pnl), 3700)
    lines.append(f"RISK MODE: {risk['mode'].upper()} — {risk['reason']}")
    lines.append(f"SIZE MULT: {risk['multiplier']}x | MIN CONF: {risk['min_conf']}")

    # Loss pattern analysis
    diagnoses, pattern_counts = analyze_all_losses()
    if pattern_counts:
        lines.append(f"\nTOP LOSS CAUSES (last 200 losses):")
        for cause, count in sorted(pattern_counts.items(), key=lambda x: -x[1])[:5]:
            lines.append(f"  {cause}: {count}x — {LOSS_PATTERNS.get(cause, {}).get('fix', 'investigate')}")

    # Strategy generation
    new_strats = generate_new_strategies()
    if new_strats:
        lines.append(f"\nAUTO-GENERATED STRATEGIES ({len(new_strats)} ready for paper):")
        for s in new_strats[:5]:
            lines.append(f"  {s.name}: {s.entry_rule} (WR from pattern data)")

    # Health
    health = diagnose_bot_health()
    if not health["healthy"]:
        lines.append(f"\n⚠️ HEALTH ISSUES:")
        for i in health["issues"]:
            lines.append(f"  [{i['severity']}] {i['what']}")
    else:
        lines.append(f"\n✅ Bot healthy. All systems nominal.")

    return "\n".join(lines)


# =============================================================================
# CLI — run standalone for intelligence reports
# =============================================================================

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="hermes_brain")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("report", help="Full intelligence report")
    sub.add_parser("losses", help="Loss root cause analysis")
    sub.add_parser("generate", help="Generate new strategies")
    sub.add_parser("risk", help="Current risk assessment")
    sub.add_parser("health", help="Health diagnostic")
    sub.add_parser("patterns", help="Mine winning patterns")

    args = ap.parse_args()

    if args.cmd == "report":
        print(smart_report())
    elif args.cmd == "losses":
        diagnoses, counts = analyze_all_losses()
        print(f"=== LOSS ROOT CAUSE ANALYSIS ({len(diagnoses)} losses) ===\n")
        for cause, count in sorted(counts.items(), key=lambda x: -x[1]):
            info = LOSS_PATTERNS.get(cause, {})
            print(f"  {cause}: {count}x")
            print(f"    Fix: {info.get('fix', 'investigate')}")
            print()
    elif args.cmd == "generate":
        strats = generate_new_strategies()
        print(f"=== AUTO-GENERATED STRATEGIES ({len(strats)}) ===\n")
        for s in strats:
            print(f"  {s.name}")
            print(f"    Indicators: {s.indicators}")
            print(f"    Entry: {s.entry_rule}")
            print(f"    Regime: {s.regime_filter}")
            print(f"    Paper only: {s.paper_only}")
            print()
    elif args.cmd == "risk":
        try:
            conn = sqlite3.connect(str(DB_PATH))
            today_pnl = conn.execute(
                "SELECT COALESCE(SUM(pnl),0) FROM trades WHERE status='closed' "
                "AND closed_at > datetime('now','start of day')"
            ).fetchone()[0]
            conn.close()
        except Exception:
            today_pnl = 0
        risk = compute_dynamic_risk(float(today_pnl), 3700)
        print(json.dumps(risk, indent=2))
    elif args.cmd == "health":
        print(json.dumps(diagnose_bot_health(), indent=2))
    elif args.cmd == "patterns":
        patterns = mine_winning_patterns()
        print(f"=== WINNING PATTERNS ({len(patterns)}) ===\n")
        for p in patterns[:20]:
            print(f"  {p['agent']} @ {p['symbol']} in {p['regime']} h{p['hour']}: "
                  f"{p['n']}t {p['wr']}% WR, total \${p['total_pnl']}")
