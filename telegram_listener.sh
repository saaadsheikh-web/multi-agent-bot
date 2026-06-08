#!/bin/bash
# Watch Hermes bridge for Telegram commands and execute them via Claude Code
BRIDGE="/Users/saad/multi_agent_bot/hermes_bridge"
LAST_LINE=0

while true; do
    CURRENT=$(wc -l < "$BRIDGE/commands.jsonl" 2>/dev/null)
    if [ "$CURRENT" -gt "$LAST_LINE" ] 2>/dev/null; then
        NEW_CMD=$(tail -1 "$BRIDGE/commands.jsonl" 2>/dev/null)
        # Check if it's from Saad (chat_id check)
        echo "[$(date +%H:%M:%S)] New Telegram command: $NEW_CMD" >> "$BRIDGE/tg_listener.log"
        # Extract text and run via Claude
        TEXT=$(echo "$NEW_CMD" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text',''))" 2>/dev/null)
        if [ -n "$TEXT" ]; then
            echo "$TEXT" | claude --print 2>&1 >> "$BRIDGE/tg_responses.log"
        fi
        LAST_LINE=$CURRENT
    fi
    sleep 2
done
