#!/usr/bin/env python3
"""Check BTC short position"""
import os, sys, json, subprocess

# Source the .env directly
here = os.path.dirname(os.path.abspath(__file__))
result = subprocess.run(
    f'source {here}/.env 2>/dev/null; env | grep -i "BLOFIN\|API\|KEY\|SECRET"',
    shell=True, capture_output=True, text=True, executable='/bin/bash'
)
print("Env vars found:", result.stdout[:500] if result.stdout else "NONE")
