#!/bin/bash
TOKEN=$(grep TELEGRAM_BOT_TOKEN /Users/saad/multi_agent_bot/.env | cut -d= -f2 | tr -d '\r\n ')
CHAT=$(grep TELEGRAM_CHAT_ID /Users/saad/multi_agent_bot/.env | cut -d= -f2 | tr -d '\r\n ')
MSG=$(cat /Users/saad/multi_agent_bot/auditor_telegram.txt)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" -d "chat_id=${CHAT}" --data-urlencode "text=${MSG}"
