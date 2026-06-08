#!/usr/bin/env python3
"""
strategy_lab.py — Hourly parametric strategy generator.

Every hour, generates 5 parameter mutations of proven base templates
(breakout, capitulation, momentum). Each variant is a JSON config that
the nightly hunter will consume to backtest against 365-day data.

Templates and parameter ranges are based on what's worked historically.
Avoids redundant variants by hashing the param tuple. Configs survive
across runs in strategy_pool.json. Pool size capped at 200 to avoid
backtest bloat.
"""
import os, sys, json, hashlib, random, datetime as dt
from pathlib import Path

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
POOL = WORK / "strategy_pool.json"
LAB_LOG = WORK / "strategy_lab.log"

POOL_CAP = 200
GENERATIONS_PER_RUN = 5

def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(LAB_LOG, "a") as f:
        f.write(line + "\n")

# Templates — each generates a config dict that the parametric backtester can run.
# Future expansion: add more templates as winning patterns are discovered.
TEMPLATES = {
    "breakout": {
        "params": {
            "lookback_bars": [2, 4, 6, 8, 12, 16, 24, 36, 48, 72, 96, 120, 168, 240, 336],
            "min_sl_pct":    [0.005, 0.008, 0.012, 0.015, 0.018, 0.025, 0.030, 0.040, 0.050, 0.070],
            "min_vol_ratio": [1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.9, 2.1, 2.5, 3.0],
            "atr_mult":      [0.9, 1.0, 1.05, 1.1, 1.2, 1.3, 1.5],
        },
        "base_profile": "daily_breakout",
    },
    "capitulation": {
        "params": {
            "bar_pct":      [0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.06, 0.08],
            "min_vol_ratio":[2.5, 3.0, 4.0, 5.0, 6.0, 8.0],
            "rsi_extreme":  [15, 20, 25, 30, 35],
        },
        "base_profile": "volume_capitulation",
    },
    "extreme_fade": {
        "params": {
            "extreme_pct": [0.05, 0.06, 0.08, 0.10, 0.12, 0.15],
            "min_vol_ratio":[2.0, 3.0, 4.0, 5.0],
            "rsi_ob": [70, 75, 80, 85],
            "rsi_os": [15, 20, 25, 30],
            "sl_pct": [0.025, 0.03, 0.04, 0.05, 0.06],
        },
        "base_profile": "pump_dump_reversal",
    },
    "macd": {
        "params": {
            "fast":      [8, 10, 12, 15],
            "slow":      [21, 26, 32, 50],
            "signal":    [7, 9, 11],
            "min_vol_ratio": [1.0, 1.2, 1.3, 1.5, 2.0],
            "atr_sl_mult":   [1.0, 1.5, 2.0, 2.5],
            "atr_tp_mult":   [2.0, 3.0, 4.0, 5.0],
        },
        "base_profile": "macd_cross",
    },
}

def fingerprint(template: str, params: dict) -> str:
    """Deterministic short id for dedup."""
    s = template + "|" + json.dumps(params, sort_keys=True)
    return hashlib.sha1(s.encode()).hexdigest()[:10]

def generate_one() -> dict:
    """Pick a random template and a random combination of its parameter ranges."""
    template = random.choice(list(TEMPLATES.keys()))
    spec = TEMPLATES[template]
    params = {k: random.choice(v) for k, v in spec["params"].items()}
    fid = fingerprint(template, params)
    name = f"{template}_{fid}"
    return {
        "id": fid,
        "name": name,
        "template": template,
        "base_profile": spec["base_profile"],
        "params": params,
        "created": dt.datetime.now().isoformat(),
        "status": "candidate",        # candidate → backtested → live | killed
        "backtest": None,
    }

def load_pool() -> list:
    if POOL.exists():
        try:
            return json.loads(POOL.read_text())
        except Exception as e:
            log(f"pool load failed: {e}; starting fresh")
    return []

def save_pool(pool: list):
    POOL.write_text(json.dumps(pool, indent=2))

def main():
    pool = load_pool()
    existing_ids = {c["id"] for c in pool}
    new = []
    attempts = 0
    while len(new) < GENERATIONS_PER_RUN and attempts < GENERATIONS_PER_RUN * 5:
        cand = generate_one()
        attempts += 1
        if cand["id"] in existing_ids:
            continue
        new.append(cand)
        existing_ids.add(cand["id"])

    pool = pool + new
    # Cap pool — drop oldest "candidate" status first, never drop "live" or "backtested" winners
    if len(pool) > POOL_CAP:
        pool.sort(key=lambda c: (
            0 if c["status"] == "live" else (1 if c["status"] == "backtested" else 2),
            c["created"],
        ))
        # Keep top POOL_CAP after sort
        pool = pool[:POOL_CAP]

    save_pool(pool)
    log(f"generated {len(new)} new candidates. pool size: {len(pool)}")
    for c in new:
        log(f"  + {c['name']}  template={c['template']}  params={c['params']}")

if __name__ == "__main__":
    main()
