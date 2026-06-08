#!/usr/bin/env python3
"""
error_detective.py — runs every 30 min. Scans bot.log for errors.

For KNOWN errors (already-fixed): silent.
For NEW/UNKNOWN errors: Telegram alert to Saad with suggested fix.

This way you never see spam about old issues, but get pinged when
something new breaks that needs investigation.
"""
import os, re, urllib.request, urllib.parse, json, datetime as dt
from pathlib import Path
from collections import Counter

WORK = Path(os.path.expanduser("~/multi_agent_bot"))
BOT_LOG = WORK / "bot.log"
DETECT_LOG = WORK / "error_detective.log"
SEEN_FILE = WORK / "error_detective_seen.json"
WINDOW_MIN = 30

env = {}
if (WORK / ".env").exists():
    for line in (WORK / ".env").read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

# KNOWN errors — already understood and fixed (or expected behavior).
# When these appear, do nothing. As I patch new ones, add codes here.
KNOWN_ERROR_CODES = {
    "152011",  # Transaction API key brokerId — fixed
    "152012",  # brokerId required — bot's fallback handles
    "152013",  # Unmatched brokerId — fallback handles
    "152002",  # Parameter size error — fixed via lot_size rounding
    "102016",  # Precision does not match — fixed via tick_size rounding
}
KNOWN_PATTERNS = [
    "BLOFIN_BROKER_ID not set",         # warning, not error
    "Failed to resolve",                 # transient DNS, retry handles
    "Connection reset by peer",          # transient network
    "SSL: UNEXPECTED_EOF",               # transient
    "Tunnel connection failed",          # transient (sandbox-side)
    "max-sdk arbiter:",                  # arbiter retry handles
    "PublicAPI.get_tickers() got",       # SDK signature, fallback handles
    "PublicAPI.get_candlesticks() got",  # ditto
    "candles .* 5m: '>' not supported",  # ditto
    "got an unexpected keyword argument",  # SDK retry path
]

def log(msg):
    line = f"{dt.datetime.now().isoformat()}  {msg}"
    print(line)
    with open(DETECT_LOG, "a") as f:
        f.write(line + "\n")

def telegram(text):
    token = env.get("TELEGRAM_BOT_TOKEN")
    chat = env.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return
    try:
        data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, timeout=10
        )
    except Exception as e:
        log(f"telegram failed: {e}")

def load_seen():
    if SEEN_FILE.exists():
        try:
            return json.loads(SEEN_FILE.read_text())
        except Exception:
            return {}
    return {}

def save_seen(d):
    SEEN_FILE.write_text(json.dumps(d))

def scan_recent_errors():
    """Read last WINDOW_MIN of bot.log, return list of error lines."""
    if not BOT_LOG.exists():
        return []
    cutoff = dt.datetime.now() - dt.timedelta(minutes=WINDOW_MIN)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M")
    errors = []
    try:
        with open(BOT_LOG) as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 2_000_000))   # tail 2MB
            for line in f:
                if "ERROR" not in line and "WARNING" not in line:
                    continue
                # Time filter
                if line[:16] < cutoff_str:
                    continue
                errors.append(line.rstrip())
    except Exception as e:
        log(f"scan failed: {e}")
    return errors

def is_known(line: str) -> bool:
    for code in KNOWN_ERROR_CODES:
        if f"'code': '{code}'" in line or f"code={code}" in line:
            return True
    for pat in KNOWN_PATTERNS:
        if re.search(pat, line):
            return True
    return False

def fingerprint(line: str) -> str:
    """Reduce a log line to its signature so we don't repeat-alert."""
    # Strip timestamps + symbol-specific stuff
    sig = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+", "", line)
    sig = re.sub(r"\b[A-Z]+-USDT\b", "SYM", sig)
    sig = re.sub(r"\b[a-f0-9]{8,}\b", "HASH", sig)
    sig = re.sub(r"\b\d+\.\d+\b", "N", sig)
    sig = re.sub(r"\b\d{4,}\b", "N", sig)
    return sig.strip()[:200]

def main():
    log("=== error_detective scan ===")
    errors = scan_recent_errors()
    log(f"scanned {len(errors)} ERROR/WARNING lines from last {WINDOW_MIN}min")

    known = [e for e in errors if is_known(e)]
    unknown = [e for e in errors if not is_known(e)]

    # Build summary always — Saad wants to see activity
    known_codes = Counter()
    for e in known:
        m = re.search(r"'code': '(\d+)'", e)
        if m:
            known_codes[m.group(1)] += 1
        elif "Failed to resolve" in e:
            known_codes["DNS"] += 1
        elif "Connection reset" in e or "SSL: UNEXPECTED" in e:
            known_codes["NETWORK"] += 1
        elif "max-sdk arbiter" in e:
            known_codes["ARBITER"] += 1
        else:
            known_codes["OTHER_KNOWN"] += 1

    unknown_counts = Counter(fingerprint(e) for e in unknown)

    # Build telegram message
    lines = [f"\U0001F50D Error Scan ({WINDOW_MIN}min):"]
    if not errors:
        lines.append("  ✅ No errors")
    else:
        lines.append(f"  Total: {len(errors)} ({len(known)} known, {len(unknown)} unknown)")
        if known_codes:
            kn_str = ", ".join(f"{k}×{v}" for k, v in known_codes.most_common(5))
            lines.append(f"  Known: {kn_str}")
        if unknown_counts:
            lines.append("  🆕 NEW UNKNOWN:")
            for sig, count in unknown_counts.most_common(3):
                lines.append(f"    ×{count}: {sig[:100]}")
            lines.append("  → fix these and I'll add to known list")

    telegram("\n".join(lines))
    log(f"sent: known={len(known)} unknown={len(unknown)}")

    # Track seen signatures (for future ref)
    seen = load_seen()
    for sig in unknown_counts:
        seen[sig] = {"first_seen": dt.datetime.now().isoformat(), "count": unknown_counts[sig]}
    save_seen(seen)


if __name__ == "__main__":
    main()
