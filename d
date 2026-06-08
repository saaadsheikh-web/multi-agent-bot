#!/usr/bin/env bash
# ./d AGENT [SIZE]      → deploy
# ./d -k AGENT          → undeploy (kill)
# ./d -l                → list all agents and their state
# ./d                   → list all agents (default if no args)

SECRET="178f9024586197ca101fac18fdb8796579165984f3e5058b"
URL="https://brigida-tristichic-janet.ngrok-free.dev"
SIZE="${2:-0.05}"

case "$1" in
  --all)
    SIZE="${2:-0.02}"
    echo ""
    echo "Deploying ALL paper agents at ${SIZE}x..."
    cd "$(dirname "$0")"
    # Get list of paper-only agent names from bot.py via the deploy endpoint's known list
    AGENTS="bb_bounce zscore_reversion stoch_rsi vwap_reversion wide_scalp wide_candle volume_profile smart_scalp liquidity_sweep connors_rsi2 raschke_retest macd_cross asian_pump pump_dump_reversal volume_capitulation supertrend hurst_regime kalman_trend golden_cross daily_breakout_2h daily_breakout_8h daily_breakout_12h daily_breakout_48h"
    for ag in $AGENTS; do
      printf "  %-22s ... " "$ag"
      RESP=$(curl -sS -X POST -H "X-Secret: $SECRET" "$URL/deploy?agent=$ag&size=$SIZE" 2>&1 | head -1)
      echo "$RESP"
      sleep 16   # let bot restart between deploys
    done
    echo ""
    echo "Done. All paper agents now live at ${SIZE}x."
    ;;

  -l|"")
    echo ""
    echo "=== AGENT ROSTER ==="
    cd "$(dirname "$0")"
    grep -E "^class .+Agent\(" bot.py | awk -F'[ (]' '{print $2}' | while read cls; do
      status=$(awk "/^class $cls/,/^class /" bot.py | grep "paper_only" | head -1 | awk '{print $3}')
      notional=$(awk "/^class $cls/,/^class /" bot.py | grep "notional_multiplier" | head -1 | awk '{print $3}')
      name=$(awk "/^class $cls/,/^class /" bot.py | grep "    name = " | head -1 | awk -F'"' '{print $2}')
      [ -z "$name" ] && continue
      if [ "$status" = "False" ]; then
        printf "  🟢 LIVE   %-22s  size=%s\n" "$name" "$notional"
      else
        printf "  ⚪ paper  %-22s\n" "$name"
      fi
    done
    echo ""
    echo "Usage:"
    echo "  ./d AGENT [SIZE]   → deploy (default size=0.05)"
    echo "  ./d -k AGENT       → kill (undeploy)"
    echo "  ./d -l             → this list"
    echo ""
    ;;

  -k)
    if [ -z "$2" ]; then
      echo "Usage: ./d -k AGENT_NAME"
      exit 1
    fi
    echo "Killing $2..."
    curl -sS -X POST -H "X-Secret: $SECRET" \
      "$URL/undeploy?agent=$2"
    echo ""
    ;;

  -h|--help)
    echo "./d AGENT [SIZE]   → deploy at SIZE (default 0.05)"
    echo "./d -k AGENT       → undeploy"
    echo "./d -l             → list all agents"
    ;;

  *)
    AGENT="$1"
    echo "Deploying $AGENT at ${SIZE}x..."
    curl -sS -X POST -H "X-Secret: $SECRET" \
      "$URL/deploy?agent=$AGENT&size=$SIZE"
    echo ""
    ;;
esac
