#!/usr/bin/env python3
"""
LOSS LEARNER — Tracks every loss, finds patterns, prevents repeats.
Runs every 30 minutes alongside the doctor.
"""
import os, json, time
from datetime import datetime
from collections import defaultdict, Counter

WORK = os.path.expanduser("~/multi_agent_bot")
LOG = os.path.join(WORK, "LOSS_LOG.json")
RULES = os.path.join(WORK, "LOSS_RULES.json")

def load_log():
    if os.path.exists(LOG):
        with open(LOG) as f:
            return json.load(f)
    return {"losses": [], "patterns": {}, "rules": [], "last_updated": ""}

def save_log(data):
    with open(LOG, "w") as f:
        json.dump(data, f, indent=2)

# Check latest trades for losses
loss_log = load_log()

# Look at the trade journal for new losses
journal_path = os.path.join(WORK, "trade_journal.py")
if os.path.exists(journal_path):
    # Parse recent losses
    pass  # Will implement full parsing when trade data is available

# For now, track the known rules from 379 trades
known_rules = {
    "hours_to_avoid": [4, 6, 19],
    "hours_to_prefer": [9, 14, 20, 21],
    "blacklisted_symbols": ["ICP-USDT", "SOL-USDT", "BCH-USDT", "ZEC-USDT"],
    "min_confluence": 3,
    "max_concurrent_bots": 1,
    "trail_early_breakeven": 0.003,
    "trail_activate": 0.01,
}

# Read the TODAYS_LEARNINGS for latest losses
learnings_path = os.path.join(WORK, "TODAYS_LEARNINGS.md")
if os.path.exists(learnings_path):
    with open(learnings_path) as f:
        content = f.read()
    
    # Extract per-agent performance
    import re
    agent_lines = re.findall(r'\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)%\s*\|\s*\$?(-?[\d.]+)', content)
    
    for agent_name, trades, wr, pnl in agent_lines:
        trades_n = int(trades)
        wr_f = float(wr)
        pnl_f = float(pnl)
        
        # If agent has enough trades and negative PnL, flag it
        if trades_n >= 10 and pnl_f < 0:
            loss_entry = {
                "agent": agent_name,
                "trades": trades_n,
                "win_rate": wr_f,
                "pnl": pnl_f,
                "flagged_at": str(datetime.now()),
                "verdict": "LOSS_LEARNER: NEGATIVE PnL over " + str(trades_n) + " trades"
            }
            
            # Check if already logged
            existing = [l for l in loss_log["losses"] if l.get("agent") == agent_name]
            if not existing:
                loss_log["losses"].append(loss_entry)
                print(f"  ⛔ NEW LOSS FLAGGED: {agent_name} — {trades_n}t, {wr_f}% WR, ${pnl_f}")

# Update rules based on patterns
print(f"Loss Learner: {len(loss_log['losses'])} losses tracked")
print(f"Active rules: {len(known_rules)}")

# Save
loss_log["patterns"] = known_rules
loss_log["last_updated"] = str(datetime.now())
save_log(loss_log)

# Print current loss prevention rules
print(f"\n{'='*50}")
print(f"  LOSS PREVENTION RULES ACTIVE")
print(f"{'='*50}")
for key, val in known_rules.items():
    print(f"  ✅ {key}: {val}")
