#!/usr/bin/env python3
"""DOCTOR AGENT — permanently disabled.
This agent was killing the main bot process repeatedly.
The launchd plist (com.saad.doctor) has been removed.
The real bot manages its own lifecycle now.
"""
import sys
print("doctor_agent.py: permanently disabled — bot manages itself.")
sys.exit(0)
