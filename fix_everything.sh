#!/bin/bash
# fix_everything.sh — one button to clean + restart + verify.
# Saad runs this when anything feels off. No thinking required.
set +e
cd ~/multi_agent_bot || exit 1

echo "═══ 1. CLEANING TEMP FILES ═══"
rm -f .env.tmp 2>/dev/null

echo "═══ 2. COMPILING ALL PYTHON ═══"
python3 -m py_compile bot.py hermes.py hermes_telegram.py hermes_bridge.py || {
  echo "❌ compile failed — abort, code has a syntax error"; exit 1; }
echo "✅ compile OK"

echo "═══ 3. HARD RESTART BOT ═══"
launchctl kickstart -k gui/$(id -u)/com.saad.multiagentbot
sleep 50

echo "═══ 4. VERIFY ═══"
echo "--- bot.log freshness ---"
LOG_AGE=$(( $(date +%s) - $(stat -f %m bot.log 2>/dev/null || stat -c %Y bot.log) ))
echo "log last write: ${LOG_AGE}s ago"
if [ "$LOG_AGE" -gt 120 ]; then
  echo "🔴 STALL — log silent >2 min"
else
  echo "🟢 bot is scanning"
fi

echo ""
echo "--- last scan line ---"
grep "scan:" bot.log | tail -1 | cut -c1-60

echo ""
echo "--- $100 floor locked? ---"
grep "MIN_NOTIONAL_USD          =" bot.py | head -1

echo ""
echo "--- killed agents (must be 3) ---"
grep -c "KILLED" bot.py

echo ""
echo "--- today P&L ---"
python3 -c "import sqlite3;c=sqlite3.connect('bot.db');print('\$',c.execute(\"SELECT ROUND(SUM(pnl),2) FROM trades WHERE opened_at>datetime('now','start of day')\").fetchone()[0])"

echo ""
echo "--- broker_id ---"
grep BLOFIN_BROKER_ID .env

echo ""
echo "═══ 5. HERMES SELF-CHECK ═══"
python3 hermes.py auto "One-line health report. Format: '🟢 alive, Xs scan, \$Y today, Z live agents.' Nothing else." 2>/dev/null | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('reply','(no reply)'))" 2>/dev/null

echo ""
echo "═══ DONE ═══"
