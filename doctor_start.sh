#!/bin/bash
# Start doctor in background. The doctor auto-detects dead bot and restarts it.
# Run this on login / after reboot.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.npm-global/bin:/usr/bin:/bin:$PATH"
cd "$HOME/multi_agent_bot" || exit 1
exec /opt/homebrew/Caskroom/miniconda/base/bin/python doctor_agent.py
