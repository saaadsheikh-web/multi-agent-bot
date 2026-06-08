# One-off sandbox helper from the 2026-05-20 nightly-hunter run. Safe to delete.
#
# Why it existed: that run's sandbox could not reach the BloFin API (HTTP 403 via
# proxy), so the standard `python3 nightly_hunter.py` -> backtest.py path failed.
# This script drove backtest.py's internals directly off the local 365d parquet
# cache, one symbol at a time, to fit the run environment's per-call time budget.
# It has served its purpose; results are in backtest_output.log / BACKTEST_REPORT.md
# / HUNTER_BRIEF.md (2026-05-20 section). Delete at will.
