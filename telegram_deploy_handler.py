#!/usr/bin/env python3
"""
telegram_deploy_handler.py — polls Telegram for deploy approvals.

Saad's design:
  1. CEO writes a `pending_deploy.json` with one proposed deploy
     {"agent": "wide_candle", "size": 0.05, "created": "2026-05-02T03:30:00Z"}
  2. CEO sends Saad a Telegram message:
     "⚖️ Deploy wide_candle at 0.05x? Reply YES to fire."
  3. Saad replies "YES" (or Y / 1 / OK / DEPLOY) from his phone.
  4. This handler polls Telegram every 60s, sees the reply, fires the
     matching deploy curl, sends "✅ Deployed wide_candle live at 0.05x".
  5. If Saad replies NO/SKIP/N, marks skipped. If 24h pass, auto-skip.

Run via scheduled task every 1 minute. State files:
  pending_deploy.json   — single active offer (or empty)
  tg_offset.json        — Telegram update offset for incremental polling
  deploy_handler.log    — actions taken
"""
import os, sys, json, urllib.request, urllib.parse, datetime as dt
from pathlib import Path

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
PENDING = WORK / "pending_deploy.json"
OFFSET_FILE = WORK / "tg_offset.json"
LOG = WORK / "deploy_handler.log"

# Load env
ENV_PATH = WORK / ".env"
env = {}
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

TG_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = env.get("TELEGRAM_CHAT_ID", "")
TV_SECRET = env.get("TV_WEBHOOK_SECRET", "")
DEPLOY_URL = "https://brigida-tristichic-janet.ngrok-free.dev/deploy"

YES_TOKENS = {"YES", "Y", "1", "OK", "DEPLOY", "OKAY", "K", "GO", "FIRE"}
NO_TOKENS = {"NO", "N", "0", "SKIP", "PASS", "CANCEL", "STOP"}

OFFER_TIMEOUT_HOURS = 24

def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def http_get(url, timeout=15):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read())

def http_post(url, data=None, timeout=15):
    body = urllib.parse.urlencode(data or {}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()

def send_telegram(text):
    if not TG_TOKEN or not CHAT_ID:
        log("telegram creds missing — skipping send")
        return
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text}
        body = urllib.parse.urlencode(data).encode()
        urllib.request.urlopen(url, data=body, timeout=10)
    except Exception as e:
        log(f"send_telegram failed: {e}")

def fire_deploy(agent: str, size: float):
    """Fire the deploy curl. Returns response text."""
    if not TV_SECRET:
        log("TV_WEBHOOK_SECRET missing — cannot deploy")
        return None
    url = f"{DEPLOY_URL}?agent={agent}&size={size}"
    try:
        req = urllib.request.Request(
            url, method="POST",
            headers={"X-Secret": TV_SECRET},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode()
    except Exception as e:
        log(f"deploy fire failed: {e}")
        return f"error: {e}"

def load_offset() -> int:
    if OFFSET_FILE.exists():
        try:
            return int(json.loads(OFFSET_FILE.read_text()).get("offset", 0))
        except Exception:
            return 0
    return 0

def save_offset(offset: int):
    OFFSET_FILE.write_text(json.dumps({"offset": offset}))

def get_updates():
    """Pull new messages from Telegram since last offset."""
    if not TG_TOKEN:
        return []
    offset = load_offset()
    url = f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates"
    if offset > 0:
        url += f"?offset={offset + 1}"
    try:
        d = http_get(url)
    except Exception as e:
        log(f"getUpdates failed: {e}")
        return []
    if not d.get("ok"):
        return []
    updates = d.get("result", [])
    if updates:
        save_offset(max(u["update_id"] for u in updates))
    return updates

def load_pending():
    if not PENDING.exists():
        return None
    try:
        return json.loads(PENDING.read_text())
    except Exception:
        return None

def clear_pending():
    if PENDING.exists():
        PENDING.unlink()

def is_offer_expired(offer: dict) -> bool:
    try:
        created = dt.datetime.fromisoformat(offer["created"].replace("Z", "+00:00"))
        return (dt.datetime.now(dt.timezone.utc) - created).total_seconds() > OFFER_TIMEOUT_HOURS * 3600
    except Exception:
        return False

def main():
    if not TG_TOKEN or not CHAT_ID:
        log("telegram credentials not configured")
        return

    offer = load_pending()
    if not offer:
        log("no pending deploy — nothing to do")
        return

    if is_offer_expired(offer):
        log(f"offer expired (>{OFFER_TIMEOUT_HOURS}h): {offer.get('agent')} — clearing")
        send_telegram(f"⏳ Deploy offer for {offer.get('agent')} expired (24h). Skipped.")
        clear_pending()
        return

    log(f"pending offer: {offer.get('agent')} @ {offer.get('size')}x")

    updates = get_updates()
    if not updates:
        log("no new telegram messages")
        return

    # Look for YES/NO from chat_id since the offer was created
    offer_created = dt.datetime.fromisoformat(
        offer["created"].replace("Z", "+00:00")
    )
    decision = None
    for upd in updates:
        msg = upd.get("message") or upd.get("edited_message")
        if not msg:
            continue
        if str(msg.get("chat", {}).get("id")) != str(CHAT_ID):
            continue
        text = (msg.get("text") or "").strip().upper()
        msg_ts = dt.datetime.fromtimestamp(msg.get("date", 0), tz=dt.timezone.utc)
        if msg_ts < offer_created:
            continue
        if text in YES_TOKENS:
            decision = "yes"; break
        if text in NO_TOKENS:
            decision = "no"; break

    if decision == "yes":
        log(f"YES received — firing deploy {offer['agent']} @ {offer['size']}x")
        resp = fire_deploy(offer["agent"], offer["size"])
        send_telegram(f"✅ Deployed {offer['agent']} live at {offer['size']}x.\n→ {resp}")
        clear_pending()
    elif decision == "no":
        log(f"NO received — skipping {offer['agent']}")
        send_telegram(f"⏭ Skipped {offer['agent']}.")
        clear_pending()
    else:
        log("no decision yet — waiting")


if __name__ == "__main__":
    main()
