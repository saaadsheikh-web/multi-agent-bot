#!/usr/bin/env python3
"""Quick check of BloFin positions and account balance."""
import json, time, hashlib, hmac, base64, requests

# Read .env
env = {}
with open("/Users/saad/multi_agent_bot/.env") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

api_key = env.get("BLOFIN_API_KEY", "")
secret = env.get("BLOFIN_SECRET", "")
passphrase = env.get("BLOFIN_PASSPHRASE", "")

def sign(method, path, body=""):
    ts = str(int(time.time() * 1000))
    sig_str = ts + method.upper() + path + body
    sig = base64.b64encode(hmac.new(secret.encode(), sig_str.encode(), hashlib.sha256).digest()).decode()
    return ts, sig

base = "https://www.blofin.com"

# Account balance
ts, sig = sign("GET", "/api/v1/account/balance")
r = requests.get(f"{base}/api/v1/account/balance",
    headers={
        "API-KEY": api_key, "API-PASSPHRASE": passphrase,
        "API-TIMESTAMP": ts, "API-SIGN": sig,
        "Content-Type": "application/json"
    })
print("=== ACCOUNT BALANCE ===")
bal = r.json()
print(json.dumps(bal, indent=2)[:1000])

# Positions
ts, sig = sign("GET", "/api/v1/account/positions")
r = requests.get(f"{base}/api/v1/account/positions",
    headers={
        "API-KEY": api_key, "API-PASSPHRASE": passphrase,
        "API-TIMESTAMP": ts, "API-SIGN": sig,
        "Content-Type": "application/json"
    })
print("\n=== POSITIONS ===")
pos = r.json()
print(json.dumps(pos, indent=2)[:2000])

# Trade history (last 50)
ts, sig = sign("GET", "/api/v1/trade/fills?limit=50")
r = requests.get(f"{base}/api/v1/trade/fills?limit=50",
    headers={
        "API-KEY": api_key, "API-PASSPHRASE": passphrase,
        "API-TIMESTAMP": ts, "API-SIGN": sig,
        "Content-Type": "application/json"
    })
print("\n=== RECENT FILLS (last 50) ===")
fills = r.json()
print(json.dumps(fills, indent=2)[:3000])
