#!/usr/bin/env bash
# Run this on your Mac to confirm everything is wired.
set -euo pipefail
cd "$(dirname "$0")"

echo "── 1. Rotator config ──"
python3 - <<'PY'
import os, pathlib
for line in pathlib.Path('.env').read_text().splitlines():
    if line.strip() and not line.startswith('#') and '=' in line:
        k,_,v = line.partition('='); os.environ.setdefault(k.strip(), v.strip())
from openrouter_client import get_rotator, is_free_slug
r = get_rotator()
print(f" keys      : {r.count()}")
print(f" model     : {os.getenv('OPENROUTER_MODEL')}")
print(f" free-only : {os.getenv('OPENROUTER_FREE_ONLY','1')}")
print(f" is_free   : {is_free_slug(os.getenv('OPENROUTER_MODEL',''))}")
PY

echo
echo "── 2. OpenRouter call (Owl Alpha, rotates on failure) ──"
python3 - <<'PY'
import os, pathlib
for line in pathlib.Path('.env').read_text().splitlines():
    if line.strip() and not line.startswith('#') and '=' in line:
        k,_,v = line.partition('='); os.environ.setdefault(k.strip(), v.strip())
from hermes import openrouter_chat, DEFAULT_MODEL
print(' model :', DEFAULT_MODEL)
out = openrouter_chat(
    [{"role":"user","content":"Reply with exactly: HERMES-WIRED-OK"}],
    max_tokens=20, temperature=0,
)
print(' reply :', out)
PY

echo
echo "── 3. Bridge round-trip ──"
python3 - <<'PY'
from hermes_bridge import Bridge, handle_command
class FakeState:
    paused = False
    def flatten(s,sym): return f"closed:{sym}"
    def flatten_all(s): return "closed:all"
    def set_leverage(s,v): return f"lev={v}"
    def set_risk(s,k,v): return f"{k}={v}"
    def reload_strategies(s): return "reloading"
b = Bridge()
cid = b.send_command('ping')
for c in b.drain_commands():
    ok, r = handle_command(c, ctx=FakeState())
    b.ack(c.id, ok=ok, result=r)
print(' ack   :', b.wait_ack(cid, timeout=1))
PY

echo
echo "── 4. Compact chart exists ──"
ls -la equity_curve_compact.png

echo
echo "✅ all checks passed"
