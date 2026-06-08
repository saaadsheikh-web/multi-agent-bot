#!/usr/bin/env python3
"""Hyperliquid → Hermes Bridge — streams market data to the bot's bridge."""

import os, sys, json, time, uuid
import requests
from datetime import datetime, timezone
from pathlib import Path

BRIDGE = Path.home() / "multi_agent_bot" / "hermes_bridge"
HL_INFO = "https://api.hyperliquid.xyz/info"

COINS = ["BTC","ETH","SOL","BNB","DOGE","ADA","AVAX","DOT","LINK",
         "LTC","ATOM","NEAR","APT","SUI","INJ","TAO","ARB","OP","TIA","XRP"]

def get_meta():
    resp = requests.post(HL_INFO, json={"type":"meta"}, timeout=10)
    return resp.json()

def get_funding():
    """Get current funding rates for all perps."""
    resp = requests.post(HL_INFO, json={"type":"metaAndAssetCtxs"}, timeout=10)
    data = resp.json()
    if not isinstance(data, list) or len(data) < 2: return {}
    universe = data[0].get("universe", [])
    ctxs = data[1]
    rates = {}
    for i, u in enumerate(universe):
        if i < len(ctxs) and u.get("name") in COINS:
            rates[u["name"]] = {
                "funding": float(ctxs[i].get("fundingRate", "0")) * 100,
                "premium": float(ctxs[i].get("premium", "0")) * 100,
                "open_interest": float(ctxs[i].get("openInterest", "0")),
            }
    return rates

def get_prices():
    """Get mid prices from recent trades."""
    prices = {}
    for coin in COINS[:5]:  # top 5 to avoid rate limits
        try:
            resp = requests.post(HL_INFO, json={
                "type": "candleSnapshot",
                "req": {"coin": coin, "interval": "5m", "startTime": int((time.time()-600)*1000), "endTime": int(time.time()*1000)}
            }, timeout=10)
            candles = resp.json()
            if isinstance(candles, list) and candles:
                prices[coin] = float(candles[-1]["c"])
        except:
            pass
        time.sleep(0.15)
    return prices

def send_to_hermes(data):
    """Push data to Hermes bridge."""
    cmd = {
        "id": str(uuid.uuid4()),
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "cmd": "say",
        "args": {"text": json.dumps(data, indent=2)},
        "source": "hl_bridge"
    }
    with open(BRIDGE / "commands.jsonl", "a") as f:
        f.write(json.dumps(cmd) + "\n")

def main():
    print("Hyperliquid → Hermes Bridge")
    print(f"Bridge: {BRIDGE}")

    # Get metadata
    meta = get_meta()
    perps = [u for u in meta.get("universe",[]) if not u.get("isDelisted")]
    print(f"Active markets: {len(perps)}")

    # Get funding rates
    funding = get_funding()
    print(f"Funding data: {len(funding)} coins")

    # Get prices
    prices = get_prices()
    print(f"Prices: {len(prices)} coins")

    # Compile report
    report = {
        "source": "hyperliquid",
        "ts": datetime.now(timezone.utc).isoformat(),
        "active_markets": len(perps),
        "top_markets": [u["name"] for u in perps[:20]],
        "funding_rates": funding,
        "prices": prices,
    }

    send_to_hermes(report)
    print(f"Report sent to Hermes at {datetime.now(timezone.utc).isoformat()}")
    print(json.dumps(report, indent=2)[:500])

if __name__ == "__main__":
    main()
