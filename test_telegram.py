#!/usr/bin/env python3
"""Quick test — send the new deploy proposal Telegram format to Saad."""
import urllib.request, urllib.parse
from pathlib import Path

env = {}
for line in (Path(__file__).parent / ".env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

text = (
    "\U0001F3AF I have found a new trade!\n\n"
    "wide_candle_test at 0.05x\n"
    "Sharpe 4.2, ExpR +0.28R, 187 trades\n\n"
    "Please say YES if you want me to deploy the trade.\n\n"
    "(TEST - do not reply)"
)
data = urllib.parse.urlencode({"chat_id": env["TELEGRAM_CHAT_ID"], "text": text}).encode()
r = urllib.request.urlopen(
    f"https://api.telegram.org/bot{env['TELEGRAM_BOT_TOKEN']}/sendMessage",
    data=data, timeout=10
)
print("sent:", r.status)
