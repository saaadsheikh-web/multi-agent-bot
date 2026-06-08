#!/bin/bash
# Expand PATH so launchd can find claude / node / python
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.npm-global/bin:/usr/bin:/bin:$PATH"
set -a
[ -f "$HOME/multi_agent_bot/.env" ] && source "$HOME/multi_agent_bot/.env"
set +a
exec /opt/homebrew/Caskroom/miniconda/base/bin/conda run --no-capture-output -n base python "$HOME/multi_agent_bot/bot.py" "$@"
