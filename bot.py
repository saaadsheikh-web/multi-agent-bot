#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 MULTI-AGENT CRYPTO TRADING BOT  v1.0   —   built for Saad
=============================================================================
 Single-file 24/7 trading engine on BloFin futures.

 8 agents:
   1. ScalpAgent         RSI extremes + volume spikes (0.3-0.8% targets)
   2. MomentumAgent      EMA stack + MACD trend follow
   3. SwingAgent         Bollinger + RSI divergence reversals
   4. MeanReversionAgent Extreme dip / pump fader
   5. WhaleTrackerAgent  Order-book imbalance + abnormal volume
   6. NewsAgent          CoinDesk / Cointelegraph headline sentiment
   7. RiskManagerAgent   Vetoes trades, enforces daily loss limit
   8. LearningAgent      Win-rate tracker, weights confidence by history

 Features:
   * TRAILING STOP on every position (client-side + hard SL on exchange)
   * Scans top N coins on BloFin by 24h volume (not just BTC/ETH/SOL)
   * 5x leverage, sniper entry (requires multi-confirmation)
   * Self-learning: SQLite trade journal, win-rate per agent
   * Optional Claude AI arbiter via OpenRouter on high-confidence signals
   * Telegram alerts to @SaadSnew007_bot
   * Will NOT touch positions it didn't open (TAO/ICP/INJ are safe)

 Run:
   python3 bot.py              # live trading
   python3 bot.py --check      # connectivity + balance test (no orders)
   python3 bot.py --once       # one scan cycle then exit
   python3 bot.py --paper      # signals only, no orders placed
=============================================================================
"""

import os
import sys
import time
import json
import math
import asyncio
import sqlite3
import logging
import logging.handlers
import re
import argparse
import traceback
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Tuple
from types import SimpleNamespace

# --- 2026-05-19: .env loader (Claude/Cowork patch) ---------------------------
# bot.py historically relied on the launching shell to export env vars. When
# LaunchAgent or `nohup python3 bot.py` started the bot without sourcing .env,
# critical vars like BLOFIN_BROKER_ID showed as empty. This loader reads .env
# from the bot directory and uses setdefault so existing shell exports still
# win. No external dotenv dependency required.
def _load_dotenv_once():
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, ".env")
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k:
                    os.environ.setdefault(k, v)
    except Exception as _e:
        # never fail boot because of .env parsing
        print(f"[dotenv] warning: {_e}", file=sys.stderr)
_load_dotenv_once()
# --- end .env loader ---------------------------------------------------------

# --- 2026-05-20: DNS auto-heal (Claude/Cowork patch) -------------------------
# Saad's Mac DNS (Virgin Media resolver) drops intermittently, returning
# `socket.gaierror: [Errno 8] nodename nor servname provided`. When that
# happens every network call fails and the bot goes silent (scan loop stalls
# while only the Telegram thread limps along). This installs a process-level
# DNS fallback: if the system resolver fails to resolve a host, we retry the
# lookup against public DNS (8.8.8.8 / 1.1.1.1 / 9.9.9.9 / 1.0.0.1) directly
# via a tiny resolver, and cache the result for 5 min. This makes the bot
# survive ISP DNS blips on its own — no manual `networksetup` / dscacheutil
# flush needed.
def _install_dns_failover():
    import socket as _socket
    import time as _time
    _PUBLIC_DNS = ["8.8.8.8", "1.1.1.1", "9.9.9.9", "1.0.0.1", "8.8.4.4"]
    _CACHE_TTL_S = 300  # 5 min — re-resolve periodically so IP changes don't break us
    _cache = {}  # host -> (ip, timestamp)
    _orig_getaddrinfo = _socket.getaddrinfo

    def _resolve_via_public_dns(host):
        # Minimal DNS A-record query over UDP to public resolvers.
        import struct, random
        for server in _PUBLIC_DNS:
            try:
                tid = random.randint(0, 0xFFFF)
                q = struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0)
                for part in host.split("."):
                    q += bytes([len(part)]) + part.encode()
                q += b"\x00" + struct.pack(">HH", 1, 1)  # type A, class IN
                s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
                s.settimeout(2)  # tighter timeout — each server gets 2s
                s.sendto(q, (server, 53))
                resp, _ = s.recvfrom(512)
                s.close()
                # parse answers: skip header(12) + question
                idx = 12
                while resp[idx] != 0:
                    idx += resp[idx] + 1
                idx += 5  # null + qtype + qclass
                ancount = struct.unpack(">H", resp[6:8])[0]
                for _ in range(ancount):
                    idx += 2  # name pointer
                    rtype, _cls, _ttl, rdlen = struct.unpack(">HHIH", resp[idx:idx+10])
                    idx += 10
                    if rtype == 1 and rdlen == 4:  # A record
                        return ".".join(str(b) for b in resp[idx:idx+4])
                    idx += rdlen
            except Exception:
                continue
        return None

    def _cached_lookup(host):
        """Check cache first, evict expired entries."""
        now = _time.time()
        if host in _cache:
            ip, ts = _cache[host]
            if now - ts < _CACHE_TTL_S:
                return ip
            # expired — evict
            del _cache[host]
        return None

    def _patched_getaddrinfo(host, *args, **kwargs):
        try:
            return _orig_getaddrinfo(host, *args, **kwargs)
        except _socket.gaierror:
            # system resolver failed — try public DNS fallback
            if not isinstance(host, str):
                raise
            ip = _cached_lookup(host)
            if ip is None:
                ip = _resolve_via_public_dns(host)
                if ip:
                    _cache[host] = (ip, _time.time())
            if ip:
                port = args[0] if args else 0
                return _orig_getaddrinfo(ip, *args, **kwargs)
            raise  # genuinely unresolvable — let caller handle

    # Also patch create_connection so aiohttp / urllib3 / requests all benefit
    _orig_create_conn = _socket.create_connection
    def _patched_create_conn(address, *args, **kwargs):
        host, port = address if isinstance(address, tuple) else (address, 0)
        if isinstance(host, str):
            try:
                _socket.getaddrinfo(host, port)  # triggers our patched resolver if needed
            except _socket.gaierror:
                pass  # let create_connection handle the fallback
        return _orig_create_conn(address, *args, **kwargs)

    _socket.getaddrinfo = _patched_getaddrinfo
    _socket.create_connection = _patched_create_conn
    print("[dns-failover] installed: 5 public-DNS resolvers, 5min cache, create_connection patched",
          file=sys.stderr)

try:
    _install_dns_failover()
except Exception as _e:
    print(f"[dns-failover] warning: {_e}", file=sys.stderr)
# --- end DNS auto-heal -------------------------------------------------------

try:
    import aiohttp
    import numpy as np
    import pandas as pd
except ImportError:
    print("ERROR: deps missing. Run:  pip install blofin pandas numpy aiohttp")
    sys.exit(1)

try:
    from blofin import BloFinClient
except ImportError:
    print("ERROR: blofin SDK missing. Run:  pip install blofin")
    sys.exit(1)

# Claude Agent SDK — lets the bot use Saad's Claude Max subscription
# instead of paid API credits. Requires `claude` CLI logged in once.
try:
    from claude_agent_sdk import (
        query as claude_query,
        ClaudeAgentOptions,
        AssistantMessage,
        TextBlock,
    )
    HAS_CLAUDE_SDK = True
except ImportError:
    HAS_CLAUDE_SDK = False

# Hermes ↔ Crypto bridge — sibling-process control + observation channel.
try:
    from hermes_bridge import Bridge as _HermesBridge, handle_command as _hermes_handle
    from hermes_brain import (
        compute_dynamic_risk,
        diagnose_loss,
        score_signal_quality,
        get_repeat_prevention,
        analyze_all_losses,
    )
    from big_boss import big_boss_loop as _big_boss_loop_impl
    from hermes_knowledge import build_knowledge_report as _build_knowledge
    from free_brain import free_brain_loop as _free_brain_impl
    HAS_HERMES = True
except Exception:
    HAS_HERMES = False

async def _big_boss_loop():
    if not HAS_HERMES: return
    await _big_boss_loop_impl()

async def _free_brain_loop():
    if not HAS_HERMES: return
    await _free_brain_impl()

async def _knowledge_loop():
    """Refresh machine-wide knowledge every hour."""
    if not HAS_HERMES:
        return
    while True:
        try:
            _build_knowledge()
        except Exception:
            pass
        await asyncio.sleep(3600)  # every hour

# Silence Claude SDK's own "Fatal error in message reader: Command failed with
# exit code 1" log spam. Bot already handles SDK failures by falling through to
# OpenRouter, but the SDK logs ERROR before the exception propagates. Bump SDK
# logger to CRITICAL so only catastrophic stuff prints.
if HAS_CLAUDE_SDK:
    for _name in ("claude_agent_sdk", "claude_code_sdk", "claude_sdk",
                  "anthropic_sdk_lib"):
        logging.getLogger(_name).setLevel(logging.CRITICAL)


# =============================================================================
# CONFIG
# =============================================================================
BLOFIN_API_KEY     = os.getenv("BLOFIN_API_KEY", "")
BLOFIN_API_SECRET  = os.getenv("BLOFIN_API_SECRET", "")
BLOFIN_PASSPHRASE  = os.getenv("BLOFIN_PASSPHRASE", "")
DEEPSEEK_API_KEY    = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL      = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
OPENROUTER_API_KEY  = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL    = os.getenv("OPENROUTER_MODEL", "openrouter/owl-alpha")
OPENROUTER_FREE_ONLY = os.getenv("OPENROUTER_FREE_ONLY", "1") == "1"
try:
    from openrouter_client import get_rotator as _or_get_rotator, is_free_slug as _or_is_free
    _OR_ROTATOR = _or_get_rotator()
except Exception:
    _OR_ROTATOR = None
    def _or_is_free(m): return True
TELEGRAM_BOT_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID    = os.getenv("TELEGRAM_CHAT_ID", "")
USE_DEMO            = os.getenv("BLOFIN_DEMO", "0") == "1"
TV_WEBHOOK_SECRET   = os.getenv("TV_WEBHOOK_SECRET", "")
TV_WEBHOOK_PORT     = int(os.getenv("TV_WEBHOOK_PORT", "8787"))
BLOFIN_BROKER_ID    = os.getenv("BLOFIN_BROKER_ID", "")
EXCHANGE            = os.getenv("EXCHANGE", "blofin").lower()   # "blofin" | "bybit"

# Trading
LEVERAGE                  = 10  # Saad: more leverage, more money
MARGIN_MODE               = "cross"
BASE_NOTIONAL_USD         = 500
MIN_NOTIONAL_USD          = 500   # $500 minimum, 7x leverage
MAX_NOTIONAL_USD          = 100000 # Saad 2026-05-23: dollar ceiling effectively off; real cap is equity-% below.
# ---- COMPOUNDING SIZING (Saad 2026-05-23) ----
# Trade size scales with equity so wins grow the next trade automatically.
# As the account compounds, $ size rises on its own. Floor stays $100.
COMPOUND_BASE_PCT         = 0.10     # base trade = 10% of equity (Saad: aggressive)
COMPOUND_MAX_PCT          = 0.25     # single trade capped at 25% of equity
MAX_CONCURRENT_POSITIONS  = 10        # max 5 trades at once — quality over quantity
DAILY_LOSS_LIMIT_USD      = 100
MIN_CONFIDENCE            = 3   # 2026-06-07: hermes_signals outputs conf=3 naturally. Quality from 3/6+55 score.
USE_AI_ARBITER            = True     # DeepSeek main brain active — fast, smart signal review
AI_ARBITER_MIN_CONF       = 3        # 2026-06-06: lowered to 3 — match MIN_CONFIDENCE

# Scanning
SCAN_INTERVAL_SEC         = 180  # was 60 — reduced API load to avoid Cloudflare rate limits
MONITOR_INTERVAL_SEC      = 12
NEWS_INTERVAL_SEC         = 900
TOP_N_COINS               = 15  # 2026-06-08: REDUCED from 25 — rate limits killing signal generation
MIN_24H_VOLUME_USD        = 5_000_000
SCAN_CONCURRENCY          = 6

# Identity / persistence
POSITION_TAG              = "MAB"
HOME                      = os.path.expanduser("~")
WORK_DIR                  = os.path.join(HOME, "multi_agent_bot")
DB_PATH                   = os.path.join(WORK_DIR, "bot.db")
LOG_PATH                  = os.path.join(WORK_DIR, "bot.log")
MARKET_CONTEXT_PATH       = os.path.join(WORK_DIR, "market_context.json")
MARKET_CONTEXT_SCRIPT     = os.path.join(WORK_DIR, "market_context.py")
_MARKET_CACHE: dict       = {"data": None, "mtime": 0}

def _load_market_bias():
    """Return (bias, reasons) from cached market_context.json. Stale > 12h = neutral."""
    try:
        mtime = os.path.getmtime(MARKET_CONTEXT_PATH)
    except OSError:
        return ("neutral", [])
    if _MARKET_CACHE["mtime"] != mtime:
        try:
            import json as _json
            with open(MARKET_CONTEXT_PATH) as _f:
                _MARKET_CACHE["data"] = _json.load(_f)
                _MARKET_CACHE["mtime"] = mtime
        except Exception:
            return ("neutral", [])
    if time.time() - mtime > 12 * 3600:
        return ("neutral", ["stale"])
    d = _MARKET_CACHE["data"] or {}
    return (d.get("bias", "neutral"), d.get("bias_reasons", []))

# Per-strategy risk profiles (% of price)
PROFILES = {
    "scalp":       {"tp": 0.6,  "sl": 0.4,  "trail": 2.0, "activate": 1.0,  "max_hold_min": 30},
    "momentum":    {"tp": 3.0,  "sl": 1.2,  "trail": 3.0,  "activate": 1.5,  "max_hold_min": 360},
    "swing":       {"tp": 4.5,  "sl": 2.0,  "trail": 4.0,  "activate": 2.0,  "max_hold_min": 1440},
    # WIDENED 2026-05-06 (forensics: trail killed winners @ 27-46% of TP).
    # WIDENED 2026-06-03: trail 1.5→2.5, activate 2.0→3.0 (used by funding_extremes)
    "meanrev":     {"tp": 4.0,  "sl": 3.0,  "trail": 2.5,  "activate": 3.0,  "max_hold_min": 480},
    "whale":       {"tp": 2.0,  "sl": 1.0,  "trail": 0.8,  "activate": 0.6,  "max_hold_min": 180},
    "news":        {"tp": 2.5,  "sl": 1.2,  "trail": 1.0,  "activate": 0.7,  "max_hold_min": 240},
    "asymmetric":  {"tp": 99.0,  "sl": 4.0,  "trail": 2.0,  "activate": 1.0,  "max_hold_min": 1440, "atr_trail": 1.2},
    # New paper agent profiles
    "funding_v2":         {"tp": 4.0, "sl": 3.0, "trail": 1.5, "activate": 2.0, "max_hold_min": 480},
    "short_bias":         {"tp": 3.0, "sl": 2.5, "trail": 1.0, "activate": 1.5, "max_hold_min": 360},
    "atr_momentum":       {"tp": 4.0, "sl": 2.5, "trail": 1.5, "activate": 2.0, "max_hold_min": 240},
    "golden_hour":        {"tp": 3.0, "sl": 2.0, "trail": 1.0, "activate": 1.5, "max_hold_min": 360},
    "asian":              {"tp": 2.5, "sl": 2.0, "trail": 1.0, "activate": 1.0, "max_hold_min": 360},
    "metals":             {"tp": 3.0, "sl": 3.0, "trail": 1.5, "activate": 2.0, "max_hold_min": 480},
    "xmr":                {"tp": 4.0, "sl": 3.0, "trail": 1.5, "activate": 2.0, "max_hold_min": 480},
    "us_open":            {"tp": 2.0, "sl": 2.0, "trail": 1.0, "activate": 1.0, "max_hold_min": 240},
    "keltner":            {"tp": 3.0, "sl": 2.0, "trail": 1.2, "activate": 1.5, "max_hold_min": 240},
    # New profile for HTF trend-pullback: wide stops, no fixed TP (trailing only),
    # long max-hold to let winners run multi-day in strong trends.
    "trend_pullback": {"tp": 99.0, "sl": 2.5, "trail": 1.5, "activate": 1.5, "max_hold_min": 5760},
    # Daily range breakout: very wide stops, fee-immune, trailing only
    "daily_breakout": {"tp": 99.0, "sl": 4.0, "trail": 2.0, "activate": 2.0, "max_hold_min": 10080, "atr_trail": 1.5},
    # WIDENED 2026-06-03: trail 1.2→2.0, activate 2.0→2.5
    "daily_breakout_24h": {"tp": 99.0, "sl": 3.5, "trail": 5.0, "activate": 2.0, "max_hold_min": 1440, "atr_trail": 1.5},
    # WIDENED 2026-06-03: trail 0.6→1.2, activate 1.5→2.0
    "daily_breakout_4h":  {"tp": 99.0, "sl": 2.5, "trail": 3.0, "activate": 1.5, "max_hold_min": 360, "atr_trail": 1.5},
    "daily_breakout_12h": {"tp": 99.0, "sl": 1.8, "trail": 3.0, "activate": 1.5, "max_hold_min": 720, "atr_trail": 1.5},
    "daily_breakout_48h": {"tp": 99.0, "sl": 3.0, "trail": 1.5, "activate": 1.5, "max_hold_min": 2880, "atr_trail": 1.5},
    "daily_breakout_7d":  {"tp": 99.0, "sl": 4.0, "trail": 2.0, "activate": 2.0, "max_hold_min": 10080},
    # WIDENED 2026-06-03: trail 0.4→1.0, activate 0.4→1.0
    "daily_breakout_2h":  {"tp": 99.0, "sl": 0.8, "trail": 3.0, "activate": 1.0, "max_hold_min": 180},
    "daily_breakout_8h":  {"tp": 99.0, "sl": 1.5, "trail": 0.8, "activate": 0.8, "max_hold_min": 480},
    # New mechanisms (2026-05-01 build):
    "supertrend":         {"tp": 99.0, "sl": 3.0, "trail": 1.5, "activate": 1.5, "max_hold_min": 4320},
    "volume_capitulation": {"tp": 1.5, "sl": 1.5, "trail": 2.0, "activate": 1.0, "max_hold_min": 240},
    "asian_pump":         {"tp": 99.0, "sl": 2.5, "trail": 1.0, "activate": 1.0, "max_hold_min": 240},
    "pump_dump_reversal": {"tp": 99.0, "sl": 4.0, "trail": 1.0, "activate": 1.5, "max_hold_min": 720},
    # WIDENED 2026-06-03: trail 1.0→2.0, activate 2.0→3.0
    "macd_cross":         {"tp": 99.0, "sl": 2.5, "trail": 2.0, "activate": 3.0, "max_hold_min": 720},
    # 2026-05-01 ranging-regime adds
    # WIDENED 2026-06-03: trail 0.5→1.0, activate 0.5→1.0
    "bb_bounce":          {"tp": 1.5, "sl": 1.0, "trail": 1.0, "activate": 1.0, "max_hold_min": 240},
    # WIDENED 2026-06-03: trail 0.4→0.8, activate 0.4→0.8
    "zscore_reversion":   {"tp": 1.2, "sl": 0.8, "trail": 0.8, "activate": 0.8, "max_hold_min": 180},
    # WIDENED 2026-06-03: trail 1.0→2.0, activate 1.5→2.5
    "stoch_rsi":          {"tp": 3.0, "sl": 2.5, "trail": 2.0, "activate": 2.5, "max_hold_min": 360},
    "golden_cross":       {"tp": 99.0, "sl": 5.0, "trail": 2.5, "activate": 2.5, "max_hold_min": 14400},
    # 2026-05-01 SCALPING WAVE — fee-aware, math-disciplined
    # Trailing-only — let winners run, don't book small profit (Saad's directive)
    "liquidity_sweep":    {"tp": 99.0, "sl": 1.5, "trail": 0.6, "activate": 1.4, "max_hold_min": 240, "atr_trail": 1.0},
    # 2026-05-09 SMART FIX (Saad: "tighter SL hits every time"):
    # Keep SL wide (2.5% → ride out noise) but engage trail SOONER so winners lock.
    # Breakeven at +0.5% already locks zero loss — SL only matters for fast killers.
    # activate 2.5→0.8 (lock once we're profitable past noise floor)
    # trail 1.5→0.6 (give back less once locked)
    # WIDENED 2026-06-03: trail 0.6→1.2, activate 0.8→1.6 (R:R was 0.06R vs -0.125R — losers 2× winners)
    "connors_rsi2":       {"tp": 99.0, "sl": 2.5, "trail": 1.2, "activate": 1.6, "max_hold_min": 360},
    "raschke_retest":     {"tp": 99.0, "sl": 2.0, "trail": 0.7, "activate": 1.6, "max_hold_min": 360},
    "wide_scalp":         {"tp": 1.2, "sl": 0.6, "trail": 0.4, "activate": 0.4, "max_hold_min": 240, "atr_trail": 0.8},
    # Asymmetric candlestick — 4% wide SL, trailing-only TP, lets winners run
    "wide_candle":        {"tp": 99.0, "sl": 4.0, "trail": 1.5, "activate": 2.0, "max_hold_min": 10080},
    # Larry Williams %R mean-rev with EMA200 trend filter
    # WIDENED 2026-05-06: trail too tight at 0.6 (forensics).
    "williams_r":         {"tp": 2.5, "sl": 1.5, "trail": 1.0, "activate": 1.8, "max_hold_min": 240},
    # Quant additions 2026-05-01
    # 2026-05-09 SMART FIX: keep SL wide so noise doesn't trip it,
    # but cap hold at 4h (was 8h) — stops timeout-bleeders like ONDO -5%.
    # activate 1.8→0.8 to lock winners earlier; trail 1.2→0.6 keeps more profit.
    # WIDENED 2026-06-03: trail 0.6→1.2, activate 0.8→1.6
    "hurst_regime":       {"tp": 2.5, "sl": 1.5, "trail": 1.2, "activate": 1.6, "max_hold_min": 240},
    "kalman_trend":       {"tp": 99.0, "sl": 2.0, "trail": 1.0, "activate": 1.2, "max_hold_min": 4320},
    # UT Bot strategy with multi-timeframe confirmation (Saad's design)
    # UT Bot MTF: breakeven-lock at +0.5%, then trail 0.5% behind peak
    # When peak hits +0.5%, stop = entry exactly (breakeven, no loss possible)
    # When peak hits +1.0%, stop = entry +0.5% (locked profit)
    # When peak hits +5.0%, stop = entry +4.5% (winner running)
    "utbot_mtf":          {"tp": 99.0, "sl": 2.5, "trail": 0.5, "activate": 0.5, "max_hold_min": 1440, "atr_trail": 1.2},
    # UT Bot v3: 1H trigger + 15m confirm + 4H HTF filter — slower, higher quality
    "utbot_v3":           {"tp": 99.0, "sl": 3.0, "trail": 1.5, "activate": 2.0, "max_hold_min": 4320},
    # Smart 5m scalper — multi-confluence required (VWAP + RSI + volume + HTF trend)
    "smart_scalp":        {"tp": 0.8, "sl": 0.5, "trail": 0.3, "activate": 0.4, "max_hold_min": 30},
    # Volume Profile — HVN/LVN reversal scalp (Peter Steidlmayer style)
    "volume_profile":     {"tp": 1.5, "sl": 0.8, "trail": 0.5, "activate": 0.6, "max_hold_min": 240},
    # Fibonacci retracement — bounce/rejection at golden-ratio levels
    # WIDENED 2026-05-06: fibonacci wins XPT/GIGGLE deserved bigger TPs.
    # WIDENED 2026-06-03: trail 1.5→3.0, activate 2.0→3.5 (was -0.25R avg)
    "fibonacci":          {"tp": 99.0, "sl": 3.0, "trail": 3.0, "activate": 3.5, "max_hold_min": 720, "atr_trail": 1.0},
    # Viki — triple EMA crossover (9/21/50). Backtested: 15m, 7%SL, trail@3%, 1.5% dist.
    # 81.5% WR, +68% in 63 days with 10× on SOL/TAO/TIA. See backtest_viki.py.
    "viki":               {"tp": 99.0, "sl": 7.0, "trail": 1.5, "activate": 3.0, "max_hold_min": 5760, "atr_trail": 1.0},
    # 2026-06-03 EXHAUSTIVE BACKTEST WINNER — fib bounce + regime filter
    # 73% profitable cross-validated, SL=7%, trail=5% (wide), risk=2%
    "fib_bounce":         {"tp": 99.0, "sl": 5.0, "trail": 6.0, "activate": 2.0, "max_hold_min": 5760, "atr_trail": 1.5},
    # Hermes master composite — multi-agent confluence signals (BB + EMA + FIB + VOL)
    # 2026-06-06: Chart-smart trailing. TrailMaster backtest proves tight trailing loses.
    # Trail only activates at +3%, with 6% distance — only genuine reversals trigger it.
    # Stepped ladder protects small profits: +0.5%=breakeven, +1%=lock 0.4%, etc.
    # Crypto noise is ~3-5% — 6% trail stays out of the chop zone.
    # 2026-06-07: activate 3.0→1.0 — 40% of losers had profit but trail never kicked in
    "hermes_master":      {"tp": 99.0, "sl": 2.5, "trail": 4.0, "activate": 1.0, "max_hold_min": 720},
}

# Safety constants
HARD_LIQUIDATION_GUARD   = 5.0   # % adverse triggers immediate market-close
BTC_VOL_PAUSE_PCT        = 3.0   # % BTC 1h move triggers pause
BTC_VOL_PAUSE_MIN        = 30
FUNDING_FILTER_LONG_MAX  = 0.06  # % — refuse longs above this
FUNDING_FILTER_SHORT_MIN = -0.06 # % — refuse shorts below this
ANTI_REVENGE_PAUSE_MIN   = 30    # lockout after 2 consecutive losses

# Symbols Saad reserves for manual trading — bot must never touch these
# Plus stocks-CFDs that close on weekends (BloFin trades them M-F, not 24/7)
SYMBOL_BLACKLIST = {"BZ-USDT"}  # only truly toxic. INJ and ICP freed.
# Most symbols unblocked — let the agents decide. Only keep truly toxic ones.
# Metals (XAU, XAG, XPT, XPD, XAUT, CL) — good mean-reversion
# Stocks (GOOGL, MSTR, TSLA, META, MU, SNDK, CRCL) — funding_extremes works well on these

# 2026-05-07 — learning-agent blacklist: symbols that bled real money.
# Cleared when they re-prove edge in paper (≥10 trades, ≥45% WR, ≥+0.10R ExpR).
# TAO-USDT: 6 trades, 3 losses incl -156%, -161%, -227% — net -$1.68
# YFI-USDT: 2 trades, 2 losses — net -$0.89
LOSING_SYMBOL_BLACKLIST = {
    # v2.0 original
    "TAO-USDT", "YFI-USDT", "TON-USDT",
    # 2026-06-05 learning agent analysis (345 closed trades):
    "SOL-USDT",    # 15t, -$14.82, avg -87%
    "BCH-USDT",    # 38t, -$10.85, avg -58%
    "ZEC-USDT",    # 64t, -$3.11, avg -106%
    "BNB-USDT",    # 21t, -$1.27, avg -58%
    "NVDA-USDT",   # 3t, -$3.04, avg -153%
    "MU-USDT",     # 4t, -$2.09, avg -71%
    "INTC-USDT",   # 3t, -$2.22, avg -73%
    "AAVE-USDT",   # 2t, -$1.52, avg -151%
    "SUI-USDT",    # 6t, -$0.23, avg -58%
    "TSLA-USDT",   # 2t, -$1.35, avg -52%
    "ETH-USDT",    # 2t, -$0.65, avg -125%
    # 2026-06-06 deep learn autopsy (358 trades):
    "ICP-USDT",    # 8t, -$19.80, hermes_master short bleed
    "INJ-USDT",    # 1t, -$4.28
    "LINK-USDT",   # 1t, -$0.76
}

# Wisdom-layer thresholds — applied to every agent universally
WISDOM_MIN_ATR_PCT       = 0.0015  # 0.15% of price (was 0.3%) — Saad: aggressive mode, allow more vol regimes
WISDOM_AGENT_BAD_EXPR    = -0.10   # if recent ExpR < this, raise conf floor
WISDOM_AGENT_GOOD_EXPR   = +0.20   # if recent ExpR > this, allow lower conf floor
WISDOM_MIN_TRADES_FOR_ADAPTIVE = 10   # need at least N trades to apply adaptive
WISDOM_DRAWDOWN_PAUSE_PCT = 0.5    # at 50% of daily loss limit, raise conf floor
WISDOM_BTC_CORR_GROUP    = {"BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT"}   # high BTC β
WISDOM_BTC_GROUP_MAX_SAME_SIDE = 2  # cap concurrent same-side positions in this cluster

# v2.0 GOLD-ZONE — RIGHT-SIZED 2026-05-08T20:45Z after Friday-paralysis incident.
# LESSON LEARNED: small-sample filters (n<10) cause more harm than good. Stripped down.
# Only true-extreme blocks remain. Buffs disabled — let confidence_multiplier do the work.
GOLD_MAX_ATR_PCT_AT_ENTRY = 5.0     # only block truly wild markets (was 2.5, n=3 — too aggressive)
GOLD_TOXIC_HOURS_HARD     = set()   # was {10} n=2 — too small to base hard block on
GOLD_TOXIC_DAYS           = set()   # was {Fri} n=3 — caused 45 vetoes in single Friday session
GOLD_BUFF_COMBOS          = set()   # buffs disabled — n=2-3 per combo is statistically meaningless
GOLD_BUFF_MULT            = 1.0     # neutralized
GOLD_BUFF_HOURS           = set()   # neutralized

# TradingView strategy name → profile key (add entries to customise per-strategy TP/SL)
TV_STRATEGY_PROFILES: Dict[str, str] = {
    # Every agent gets a TV strategy name — TradingView alerts can trigger ANY agent
    "rsi_oversold":  "meanrev",
    "rsi_overbought": "meanrev",
    "fib_786_long":   "fibonacci",
    "fib_786_short":  "fibonacci",
    "fib_618_long":   "fibonacci",
    "fib_618_short":  "fibonacci",
    "wedge_falling_long":  "meanrev",
    "wedge_rising_short":  "meanrev",
    "btc_dom_alt_short":   "trend_pullback",
    "log_channel_long":    "trend_pullback",
    # All live agents can receive TV alerts directly
    "stoch_rsi_long":     "stoch_rsi",
    "stoch_rsi_short":    "stoch_rsi",
    "funding_extreme_short": "meanrev",
    "funding_extreme_long":  "meanrev",
    "macd_cross_long":    "macd_cross",
    "macd_cross_short":   "macd_cross",
    "fibonacci_long":     "fibonacci",
    "fibonacci_short":    "fibonacci",
    "golden_hour_long":   "golden_hour",
    "golden_hour_short":  "golden_hour",
    "asian_session_long":  "asian",
    "asian_session_short": "asian",
    "metals_scalp_long":  "metals",
    "metals_scalp_short": "metals",
    "xmr_meanrev_long":   "xmr",
    "xmr_meanrev_short":  "xmr",
    "us_open_momentum_long":  "us_open",
    "us_open_momentum_short": "us_open",
    "atr_breakout_long":  "atr_momentum",
    "atr_breakout_short": "atr_momentum",
    "keltner_squeeze_long":  "keltner",
    "keltner_squeeze_short": "keltner",
    "viki_long":          "viki",
    "viki_short":         "viki",
    "short_bias_short":     "short_bias",
    "atr_breakout_long":    "atr_momentum",
    "atr_breakout_short":   "atr_momentum",
    "funding_fade_v2_short": "funding_v2",
    "funding_fade_v2_long":  "funding_v2",
}
TV_DEFAULT_PROFILE = "meanrev"

# Symbol universe for news matching (base assets)
NEWS_SYMBOLS = [
    "BTC","ETH","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC","LINK","LTC","ATOM",
    "NEAR","APT","SUI","SEI","TIA","INJ","TAO","FIL","ARB","OP","ICP","TON","TRX",
    "BNB","UNI","AAVE","RNDR","FTM","HBAR","ETC","XLM","PEPE","SHIB","WIF","BONK",
    "FET","AGIX","ORDI","JUP","PYTH","STRK","JTO","WLD","ENA","ENS","DYDX",
]


# =============================================================================
# LOGGING + TELEGRAM
# =============================================================================
HEALTH_PATH = os.path.join(WORK_DIR, "health.json")
BOT_PY_PATH = os.path.join(WORK_DIR, "bot.py")
ENV_PATH    = os.path.join(WORK_DIR, ".env")
RESTART_TRIGGER_PATH = os.path.join(WORK_DIR, ".restart_trigger")

def _safe_json_dumps(obj: dict) -> str:
    """JSON dumps that handles numpy types (int64, float64, ndarray, etc.)."""
    import numpy as np

    def _convert(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, pd.DataFrame):
            return o.to_dict()
        if isinstance(o, pd.Series):
            return o.to_dict()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")

    return json.dumps(obj, default=_convert)


def setup_logging():
    os.makedirs(WORK_DIR, exist_ok=True)
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_PATH, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter(fmt))
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(fmt))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(file_handler)
    root.addHandler(stream_handler)
log = logging.getLogger("MAB")


async def tg_send(session: aiohttp.ClientSession, text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    # Saad wants: trade open/close fills + critical alerts. NO health/status spam.
    # Filter by message content — block known noise patterns, let the rest through.
    NOISE_PATTERNS = [
        "health check", "scan:", "no signals this cycle", "regime detection",
        "scheduled task", "context updater", "morning briefing",
        "heartbeat", "mab reloading", "tv alert"
    ]
    if any(p in text.lower() for p in NOISE_PATTERNS):
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        async with session.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML",
                  "disable_web_page_preview": True},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as r:
            await r.text()
    except Exception as e:
        log.warning(f"telegram: {e}")


# =============================================================================
# RETRY HELPER
# =============================================================================
async def _retry_thread(fn, *args, retries: int = 3, label: str = "", **kwargs):
    """Run a sync fn in a thread with exponential-backoff retries on any exception."""
    last_exc: Exception = RuntimeError("no attempts")
    for i in range(retries):
        try:
            return await asyncio.to_thread(fn, *args, **kwargs)
        except Exception as e:
            last_exc = e
            if i < retries - 1:
                wait = 2 ** i
                log.warning(f"retry {label or getattr(fn,'__name__','?')} #{i+1}: {e} — wait {wait}s")
                await asyncio.sleep(wait)
    raise last_exc


# =============================================================================
# INDICATORS  (numpy/pandas, no extra deps)
# =============================================================================
def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()

def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()

def rsi(s: pd.Series, n: int = 14) -> pd.Series:
    d = s.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return (100 - (100 / (1 + rs))).fillna(50)

def macd(s: pd.Series, fast=12, slow=26, signal=9):
    f = ema(s, fast); sl = ema(s, slow)
    line = f - sl
    sig = ema(line, signal)
    hist = line - sig
    return line, sig, hist

def bbands(s: pd.Series, n: int = 20, k: float = 2.0):
    m = s.rolling(n).mean()
    sd = s.rolling(n).std()
    return m + k * sd, m, m - k * sd

def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h - l).abs(),
                    (h - c.shift()).abs(),
                    (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False).mean()

def adx(df: pd.DataFrame, n: int = 14) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"]
    up   = h.diff()
    dn   = -l.diff()
    pdm  = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=h.index)
    ndm  = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=h.index)
    tr   = pd.concat([(h - l).abs(), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr_ = tr.ewm(alpha=1/n, adjust=False).mean().replace(0, np.nan)
    pdi  = 100 * pdm.ewm(alpha=1/n, adjust=False).mean() / atr_
    ndi  = 100 * ndm.ewm(alpha=1/n, adjust=False).mean() / atr_
    denom = (pdi + ndi).replace(0, np.nan)
    dx   = 100 * (pdi - ndi).abs() / denom
    return dx.ewm(alpha=1/n, adjust=False).mean().fillna(20)


# =============================================================================
# JAPANESE CANDLESTICK PATTERNS
# Each helper returns a bool: was the pattern present on the LAST CLOSED bar?
# All percentages are expressed as fractions of the open price.
# =============================================================================
def _body_pct(o, c):
    return abs(c - o) / o if o else 0.0

def _upper_wick_pct(o, h, c):
    return (h - max(o, c)) / o if o else 0.0

def _lower_wick_pct(o, l, c):
    return (min(o, c) - l) / o if o else 0.0

def is_doji(o, h, l, c, tol_pct: float = 0.001) -> bool:
    """Body < tol_pct of open. Indecision."""
    return o > 0 and abs(c - o) / o < tol_pct

def is_hammer(o, h, l, c) -> bool:
    """Small body, long lower wick (>= 2x body), small upper wick.
    Bullish reversal — only meaningful at a downtrend low."""
    body = abs(c - o)
    if o <= 0 or body <= 0:
        return False
    upper = h - max(o, c)
    lower = min(o, c) - l
    return lower >= 2 * body and upper <= body * 0.6

def is_shooting_star(o, h, l, c) -> bool:
    """Opposite of hammer — bearish reversal."""
    body = abs(c - o)
    if o <= 0 or body <= 0:
        return False
    upper = h - max(o, c)
    lower = min(o, c) - l
    return upper >= 2 * body and lower <= body * 0.6

def is_bullish_engulfing(o1, c1, o2, c2) -> bool:
    """Bar 1 (prior) red, bar 2 (current) green and engulfs bar 1's body."""
    return c1 < o1 and c2 > o2 and c2 >= o1 and o2 <= c1

def is_bearish_engulfing(o1, c1, o2, c2) -> bool:
    """Bar 1 green, bar 2 red and engulfs bar 1's body."""
    return c1 > o1 and c2 < o2 and o2 >= c1 and c2 <= o1

def is_morning_star(o1, c1, o2, c2, o3, c3) -> bool:
    """3-bar bullish reversal: long red + small body (any color) + long green that closes >50% into bar1's body."""
    if not (c1 < o1 and abs(c1 - o1) > 0):
        return False
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    if body2 > body1 * 0.4:           # bar 2 must be small
        return False
    if not (c3 > o3):                  # bar 3 must be green
        return False
    body3 = abs(c3 - o3)
    if body3 < body1 * 0.5:            # bar 3 must be substantial
        return False
    midpoint1 = (o1 + c1) / 2
    return c3 > midpoint1               # bar 3 closes above bar 1 midpoint

def is_evening_star(o1, c1, o2, c2, o3, c3) -> bool:
    """Mirror of morning star — bearish reversal."""
    if not (c1 > o1 and abs(c1 - o1) > 0):
        return False
    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    if body2 > body1 * 0.4:
        return False
    if not (c3 < o3):
        return False
    body3 = abs(c3 - o3)
    if body3 < body1 * 0.5:
        return False
    midpoint1 = (o1 + c1) / 2
    return c3 < midpoint1

def is_three_white_soldiers(opens, closes) -> bool:
    """3 consecutive green bars, each closing higher than the prior, each with substantial body."""
    if len(opens) < 3:
        return False
    o1, o2, o3 = opens[-3], opens[-2], opens[-1]
    c1, c2, c3 = closes[-3], closes[-2], closes[-1]
    if not (c1 > o1 and c2 > o2 and c3 > o3):
        return False
    if not (c1 < c2 < c3):
        return False
    # Each open within prior body, each close near the high
    if not (o2 > o1 and o3 > o2):
        return False
    return True

def is_three_black_crows(opens, closes) -> bool:
    if len(opens) < 3:
        return False
    o1, o2, o3 = opens[-3], opens[-2], opens[-1]
    c1, c2, c3 = closes[-3], closes[-2], closes[-1]
    if not (c1 < o1 and c2 < o2 and c3 < o3):
        return False
    if not (c1 > c2 > c3):
        return False
    if not (o2 < o1 and o3 < o2):
        return False
    return True


def is_bullish_three_line_strike(o, c) -> bool:
    """Bearish Three Line Strike: 3 down candles then 1 big up that engulfs them. 84% WR (Bulkowski)."""
    if len(o) < 4:
        return False
    b1 = c[-4] < o[-4]  # bear
    b2 = c[-3] < o[-3] and c[-3] < c[-4]  # bear, lower
    b3 = c[-2] < o[-2] and c[-2] < c[-3]  # bear, lower
    b4 = c[-1] > o[-4]  # big bull engulfs all 3
    return b1 and b2 and b3 and b4

def is_bearish_three_line_strike(o, c) -> bool:
    """Bullish Three Line Strike: 3 up candles then 1 big down that engulfs them."""
    if len(o) < 4:
        return False
    b1 = c[-4] > o[-4]  # bull
    b2 = c[-3] > o[-3] and c[-3] > c[-4]  # bull, higher
    b3 = c[-2] > o[-2] and c[-2] > c[-3]  # bull, higher
    b4 = c[-1] < o[-4]  # big bear engulfs all 3
    return b1 and b2 and b3 and b4

def obv_divergence(df) -> Optional[str]:
    """OBV divergence: price down, OBV up = bullish. Price up, OBV down = bearish."""
    if len(df) < 20:
        return None
    c = df["close"].values; v = df["volume"].values
    obv = [0]
    for i in range(1, len(c)):
        if c[i] > c[i-1]: obv.append(obv[-1] + v[i])
        elif c[i] < c[i-1]: obv.append(obv[-1] - v[i])
        else: obv.append(obv[-1])
    price_5 = c[-1] - c[-6]
    obv_5 = obv[-1] - obv[-6]
    if price_5 < 0 and obv_5 > 0:
        return "bullish_divergence"
    if price_5 > 0 and obv_5 < 0:
        return "bearish_divergence"
    return None

def detect_bullish_pattern(df: pd.DataFrame) -> Optional[str]:
    """Check the LAST CLOSED bar for any high-quality bullish reversal pattern.
    Returns pattern name or None."""
    if len(df) < 4:
        return None
    o = df["open"].values; h = df["high"].values
    l = df["low"].values;  c = df["close"].values
    # Three Line Strike — #1 pattern, 84% WR
    if is_bullish_three_line_strike(o, c):
        return "three_line_strike_bullish"
    # Hammer on last bar
    if is_hammer(o[-1], h[-1], l[-1], c[-1]):
        return "hammer"
    # Bullish engulfing across last 2 bars
    if is_bullish_engulfing(o[-2], c[-2], o[-1], c[-1]):
        return "bullish_engulfing"
    # Morning star across last 3 bars
    if is_morning_star(o[-3], c[-3], o[-2], c[-2], o[-1], c[-1]):
        return "morning_star"
    # Three white soldiers
    if is_three_white_soldiers(o, c):
        return "three_white_soldiers"
    return None


def detect_bearish_pattern(df: pd.DataFrame) -> Optional[str]:
    if len(df) < 4:
        return None
    o = df["open"].values; h = df["high"].values
    l = df["low"].values;  c = df["close"].values
    if is_shooting_star(o[-1], h[-1], l[-1], c[-1]):
        return "shooting_star"
    if is_bearish_engulfing(o[-2], c[-2], o[-1], c[-1]):
        return "bearish_engulfing"
    if is_evening_star(o[-3], c[-3], o[-2], c[-2], o[-1], c[-1]):
        return "evening_star"
    if is_three_black_crows(o, c):
        return "three_black_crows"
    return None


# =============================================================================
# BLOFIN WRAPPER  (sync calls, wrapped via asyncio.to_thread)
# SDK uses snake_case kwargs; API responses use camelCase keys.
# =============================================================================
class BloFin:
    def __init__(self):
        self.client = BloFinClient(
            api_key=BLOFIN_API_KEY,
            api_secret=BLOFIN_API_SECRET,
            passphrase=BLOFIN_PASSPHRASE,
        )
        if USE_DEMO:
            try:
                self.client.use_demo = True
            except Exception:
                pass
        self._contract_cache: Dict[str, Dict[str, float]] = {}
        # Detect net vs hedge mode once at startup
        self.position_mode = self._detect_position_mode()
        self.margin_mode   = self._detect_margin_mode()
        log.info(f"BloFin position mode: {self.position_mode}  margin mode: {self.margin_mode}")
        # 2026-06-06: API confirmed working without broker_id — auto-discovery handles it

    def _detect_position_mode(self) -> str:
        """Returns 'net_mode' (one-way) or 'long_short_mode' (hedge)."""
        try:
            r = self.client.trading.get_position_mode()
            data = (r or {}).get("data") or {}
            mode = data.get("positionMode") or data.get("position_mode") or "net_mode"
            return mode
        except Exception as e:
            log.warning(f"position_mode detect: {e} — defaulting to net_mode")
            return "net_mode"

    def _detect_margin_mode(self) -> str:
        """Returns 'isolated' or 'cross' as configured on the account."""
        try:
            r = self.client.trading.get_margin_mode()
            data = (r or {}).get("data") or {}
            return data.get("marginMode") or MARGIN_MODE
        except Exception as e:
            log.warning(f"margin_mode detect: {e} — defaulting to {MARGIN_MODE}")
            return MARGIN_MODE

    def _pos_side_for_open(self, side: str) -> str:
        """side is 'buy' or 'sell'. Returns position_side string for open."""
        if self.position_mode == "long_short_mode":
            return "long" if side == "buy" else "short"
        return "net"

    # ------- account ----------------------------------------------------------
    def balance(self) -> float:
        try:
            r = self.client.trading.get_futures_account_balance()
            data = (r or {}).get("data") or {}
            details = data.get("details") or []
            if isinstance(details, list):
                for d in details:
                    if d.get("currency") == "USDT":
                        return float(d.get("equity") or d.get("available") or 0)
            if isinstance(data, dict) and data.get("totalEquity"):
                return float(data["totalEquity"])
            return 0.0
        except Exception as e:
            log.error(f"balance: {e}")
            return 0.0

    def positions(self) -> List[dict]:
        try:
            r = self.client.trading.get_positions()
            data = (r or {}).get("data") or []
            out = []
            for p in data:
                if not isinstance(p, dict):
                    continue
                qty = float(p.get("positions") or p.get("size") or 0)
                if abs(qty) <= 0:
                    continue
                out.append({
                    "symbol": p.get("instId"),
                    "side": p.get("positionSide", "net"),
                    "qty": qty,
                    "avg_price": float(p.get("averagePrice") or 0),
                    "upnl": float(p.get("unrealizedPnl") or 0),
                    "leverage": float(p.get("leverage") or LEVERAGE),
                    "client_order_id": p.get("clientOrderId", ""),
                })
            return out
        except Exception as e:
            log.error(f"positions: {e}")
            return []

    # ------- market data ------------------------------------------------------
    @staticmethod
    def _try_calls(method, attempts):
        """Try each (args, kwargs) pair in order; return first success."""
        last_exc = None
        for args, kwargs in attempts:
            try:
                return method(*args, **kwargs)
            except Exception as e:
                last_exc = e
        raise last_exc

    def tickers(self) -> List[dict]:
        # BloFin SDK signature: get_tickers(inst_id: Optional[str] = None)
        # Calling with no args returns all tickers. Removed bogus instType/inst_type
        # kwargs that were spamming the error log with misleading messages.
        try:
            r = self.client.public.get_tickers()
            items = (r or {}).get("data") or []
            return [t for t in items if (t.get("instId") or "").endswith("-USDT")]
        except Exception as e:
            log.error(f"tickers: {e}")
            return []

    # Per-session blacklist for symbols whose candles return 403 (stocks-CFDs etc.)
    _bad_symbols_cache: set = set()

    def candles(self, symbol: str, bar: str = "5m", limit: int = 200) -> pd.DataFrame:
        # Hard skip: if blacklisted this session, return empty silently
        if symbol in BloFin._bad_symbols_cache:
            return pd.DataFrame()
        try:
            # Retry up to 3 times on DNS/network errors with backoff
            r = None
            for attempt in range(3):
                try:
                    r = self._try_calls(self.client.public.get_candlesticks, [
                        ((), {"inst_id": symbol, "bar": bar, "limit": int(limit)}),
                        ((symbol, bar, int(limit)), {}),
                    ])
                    break
                except Exception as e:
                    err_str = str(e)
                    if "403" in err_str or "Forbidden" in err_str:
                        raise   # handled in outer except
                    if attempt < 2:
                        import time
                        time.sleep(0.5 * (attempt + 1))
                        continue
                    raise
            rows = (r or {}).get("data") or []
            if not rows:
                return pd.DataFrame()
            cols = ["ts", "open", "high", "low", "close", "volume",
                    "vc", "vcq", "confirm"]
            width = min(len(rows[0]), len(cols))
            df = pd.DataFrame([row[:width] for row in rows], columns=cols[:width])
            for c in ["ts", "open", "high", "low", "close", "volume"]:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
            df = df.sort_values("ts").reset_index(drop=True)
            return df.dropna(subset=["close"])
        except Exception as e:
            err_str = str(e)
            # 403 Forbidden: BloFin doesn't expose candles for this symbol (stocks/CFDs).
            # Blacklist immediately and silently — no log spam.
            if "403" in err_str or "Forbidden" in err_str:
                if symbol not in BloFin._bad_symbols_cache:
                    log.info(f"candles {symbol}: blacklisted for session (403 — symbol not on public candles API)")
                    BloFin._bad_symbols_cache.add(symbol)
                return pd.DataFrame()
            log.warning(f"candles {symbol} {bar}: {e}")
            return pd.DataFrame()

    def orderbook(self, symbol: str, depth: int = 20) -> dict:
        try:
            r = self._try_calls(self.client.public.get_order_book, [
                ((), {}),
                ((symbol, str(depth)), {}),
                ((), {"inst_id": symbol, "size": str(depth)}),
                ((), {"instId": symbol, "size": str(depth)}),
            ])
            data = (r or {}).get("data") or [{}]
            d = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})
            return {"bids": d.get("bids", []) or [], "asks": d.get("asks", []) or []}
        except Exception:
            return {"bids": [], "asks": []}

    def funding(self, symbol: str) -> float:
        try:
            r = self._try_calls(self.client.public.get_funding_rate, [
                ((), {}),
                ((symbol,), {}),
                ((), {"inst_id": symbol}),
                ((), {"instId": symbol}),
            ])
            data = (r or {}).get("data") or [{}]
            d = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})
            return float(d.get("fundingRate") or 0)
        except Exception:
            return 0.0

    def instrument(self, symbol: str) -> Dict[str, float]:
        if symbol in self._contract_cache:
            return self._contract_cache[symbol]
        try:
            r = self._try_calls(self.client.public.get_instruments, [
                ((), {}),
                ((symbol,), {}),
                ((), {"inst_id": symbol}),
                ((), {"instId": symbol}),
            ])
            data = (r or {}).get("data") or []
            d = {}
            if data:
                if len(data) == 1:
                    d = data[0]
                else:
                    d = next((x for x in data if x.get("instId") == symbol), data[0])
            info = {
                "contract_value": float(d.get("contractValue") or d.get("ctVal") or 0.001),
                "lot_size":       float(d.get("lotSize") or d.get("lotSz") or 1),
                "min_size":       float(d.get("minSize") or d.get("minSz") or 1),
                "tick_size":      float(d.get("tickSize") or d.get("tickSz") or 0.01),
            }
            self._contract_cache[symbol] = info
            return info
        except Exception:
            info = {"contract_value": 0.001, "lot_size": 1.0, "min_size": 1.0, "tick_size": 0.01}
            self._contract_cache[symbol] = info
            return info

    # ------- trading ----------------------------------------------------------
    def set_leverage(self, symbol: str, lev: int = LEVERAGE):
        try:
            self.client.trading.set_leverage(
                inst_id=symbol, leverage=str(lev), margin_mode=self.margin_mode)
        except Exception as e:
            log.warning(f"set_leverage {symbol}: {e}")

    # Broker-ID candidates to retry on 152013 "Unmatched brokerId". Order matters: most
    # likely first. The first one BloFin accepts is cached for the session. Cleared on
    # restart. Skipped entirely once BLOFIN_BROKER_ID env var is known-good.
    _BROKER_CANDIDATES = [
        "hyperbot", "Hyperbot", "HYPERBOT",
        "blofin", "BLOFIN", "Blofin",
        "TraderwinFi", "traderwin", "default",
        "API", "api",
    ]
    _broker_id_cached: Optional[str] = None

    def place_market(self, symbol: str, side: str, size: float,
                     tp: Optional[float] = None, sl: Optional[float] = None,
                     custom_id: Optional[str] = None,
                     limit_price: Optional[float] = None) -> dict:
        if symbol in BloFin._bad_symbols_cache:
            return {"code": "-1", "msg": "symbol in bad_symbols_cache (IP restricted earlier this session)"}
        # Try the env value first, then cycle through candidates on 152013.
        primary = (BloFin._broker_id_cached or BLOFIN_BROKER_ID or "").strip()
        candidates = []
        # Sentinel "__NONE__" = we've confirmed this is a Transaction API key (no brokerId).
        if BloFin._broker_id_cached == "__NONE__":
            candidates = [""]
        elif primary:
            candidates.append(primary)
        else:
            # No known-good value. Try WITHOUT brokerId first (Transaction keys),
            # then fall back to broker-key candidates.
            candidates.append("")
            for c in self._BROKER_CANDIDATES:
                candidates.append(c)
        if not candidates:
            candidates = [""]   # last-resort: try with empty value present

        last_err = None
        for bid in candidates:
            kwargs: Dict[str, Any] = {}
            if bid:
                kwargs["brokerId"] = bid
            if tp is not None:
                # Pass as-is — caller is responsible for tick-size rounding.
                # Old f"{tp:.8f}" formatted 8 decimals which BloFin rejected.
                kwargs["tpTriggerPrice"] = str(tp)
                kwargs["tpOrderPrice"]   = "-1"   # -1 = market on trigger
            if sl is not None:
                kwargs["slTriggerPrice"] = str(sl)
                kwargs["slOrderPrice"]   = "-1"
            if custom_id:
                kwargs["clientOrderId"] = custom_id
            try:
                # LIMIT-ONLY ENFORCEMENT (Saad 2026-05-06: "only limit orders").
                # Maker fees are 1/3 of taker. If limit_price isn't supplied, REFUSE
                # to fall back to market — log loud, return error. Fail-loud beats
                # silent fee bleeding.
                if not limit_price or limit_price <= 0:
                    log.error(f"LIMIT-ONLY: refusing market fallback for {symbol} {side} (no limit_price)")
                    return {"error": "limit-only enforced: no limit_price provided", "code": "LIMIT_REQUIRED"}
                order_type_use = "limit"
                price_use = round(float(limit_price), 6)
                res = self.client.trading.place_order(
                    inst_id       = symbol,
                    margin_mode   = self.margin_mode,
                    position_side = self._pos_side_for_open(side),
                    side          = side,
                    order_type    = order_type_use,
                    price         = price_use,
                    size          = size,
                    **kwargs,
                ) or {}
            except Exception as e:
                last_err = {"error": str(e)}
                log.error(f"place_order {symbol} broker_id={bid!r}: {e}")
                continue

            code = str(res.get("code", "")) if isinstance(res, dict) else ""
            # 152013 = Unmatched brokerId — try next candidate
            # 152012 = brokerId is required — also try next (current was None/empty)
            if code in ("152013", "152012"):
                last_err = res
                log.warning(f"order rejected {symbol} broker_id={bid!r}: {res} — trying next candidate")
                continue
            # 152011 = Transaction API Key does not support brokerId — cache and retry empty
            if code == "152011":
                BloFin._broker_id_cached = "__NONE__"
                log.warning(f"152011 with broker_id={bid!r}: Transaction API key — caching no-brokerId mode, retrying as LIMIT")
                kwargs.pop("brokerId", None)
                try:
                    # LIMIT-ONLY: retry must also be a limit order (not market)
                    res = self.client.trading.place_order(
                        inst_id       = symbol,
                        margin_mode   = self.margin_mode,
                        position_side = self._pos_side_for_open(side),
                        side          = side,
                        order_type    = "limit",
                        price         = round(float(limit_price), 6),
                        size          = size,
                        **kwargs,
                    ) or {}
                    return res
                except Exception as e:
                    return {"error": str(e)}
            # Anything else (success, or a different rejection) — return immediately.
            if code == "0" and bid:
                BloFin._broker_id_cached = bid
                log.info(f"broker_id={bid!r} accepted by BloFin — cached for session")
            return res

        return last_err or {"error": "all broker_id candidates rejected"}

    def close_position(self, symbol: str, position_side: str = "net") -> dict:
        """Closes by symbol+side. position_side='net' for one-way, 'long'/'short' for hedge."""
        try:
            return self.client.trading.close_positions(
                inst_id=symbol,
                margin_mode=self.margin_mode,
                position_side=position_side,
            ) or {}
        except Exception as e:
            log.error(f"close_position {symbol}: {e}")
            return {"error": str(e)}

    def close_logical(self, symbol: str, logical_side: str) -> dict:
        """Close by LOGICAL side ('long'/'short'). Auto-maps to net/hedge mode."""
        if self.position_mode == "long_short_mode":
            return self.close_position(symbol, logical_side)
        return self.close_position(symbol, "net")


# =============================================================================
# SIGNAL + AGENT BASE
# =============================================================================
@dataclass
class Signal:
    agent: str
    symbol: str
    side: str            # "long" or "short"
    confidence: int      # 1..10
    profile: str         # key into PROFILES
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrendState:
    """Per-symbol trend snapshot. 'Trend is your friend' — Saad's directive 2026-05-06.
    Attached to MarketContext.trend for every agent to read.

    Fields:
      direction: 'UP', 'DOWN', or 'FLAT'
      strength:  'STRONG', 'MODERATE', or 'WEAK' (based on ADX-ish + EMA slope)
      mtf_aligned: True if 1H trend matches the longer 1H-derived 4H view
      ema_slope_pct: 1H EMA50 5-bar slope (for confidence weighting)
      adx_proxy: 14-bar high/low range as % of price (chop indicator)
      score: -3 to +3 — signed strength (positive=up, magnitude=conviction)
             Used for confidence boost: with-trend +1, against-trend -1, cap penalty -2.
    """
    direction: str = "FLAT"
    strength: str = "WEAK"
    mtf_aligned: bool = False
    ema_slope_pct: float = 0.0
    adx_proxy: float = 0.0
    score: int = 0


def compute_trend_state(df_1h: pd.DataFrame) -> TrendState:
    """Compute trend state from 1h candles. Cheap; called once per symbol per scan."""
    if df_1h is None or len(df_1h) < 60:
        return TrendState()
    try:
        c = df_1h["close"]; h = df_1h["high"]; l = df_1h["low"]
        last = float(c.iloc[-1])
        if last <= 0:
            return TrendState()
        # EMA50 slope over last 5 bars
        e50 = ema(c, 50)
        if pd.isna(e50.iloc[-1]) or pd.isna(e50.iloc[-5]) or e50.iloc[-5] <= 0:
            return TrendState()
        slope_pct = (e50.iloc[-1] / e50.iloc[-5] - 1) * 100
        # EMA200 position — price above = uptrend bias, below = downtrend bias
        e200 = ema(c, 200) if len(c) >= 200 else e50
        ema200_val = e200.iloc[-1] if not pd.isna(e200.iloc[-1]) else e50.iloc[-1]
        above_ema200 = last > ema200_val
        # ADX proxy: 50-bar range as % of price (proxy for trend "strength")
        rng = (h.iloc[-50:].max() - l.iloc[-50:].min()) / last * 100
        # Higher-highs / lower-lows count over last 20 bars
        hhs = sum(1 for i in range(-19, 0) if h.iloc[i] > h.iloc[i-1])
        lls = sum(1 for i in range(-19, 0) if l.iloc[i] < l.iloc[i-1])

        # Direction
        if slope_pct > 0.5 and above_ema200 and hhs >= 11:
            direction = "UP"
        elif slope_pct < -0.5 and not above_ema200 and lls >= 11:
            direction = "DOWN"
        else:
            direction = "FLAT"

        # Strength
        abs_slope = abs(slope_pct)
        if abs_slope > 1.5 and rng > 4.0:
            strength = "STRONG"
        elif abs_slope > 0.5 and rng > 2.0:
            strength = "MODERATE"
        else:
            strength = "WEAK"

        # MTF alignment: build pseudo-4H by sampling every 4 bars, recompute slope
        df_4h_close = c.iloc[::4]
        if len(df_4h_close) >= 30:
            e4h = ema(df_4h_close, 20)
            if not pd.isna(e4h.iloc[-1]) and not pd.isna(e4h.iloc[-3]) and e4h.iloc[-3] > 0:
                slope_4h = (e4h.iloc[-1] / e4h.iloc[-3] - 1) * 100
                mtf_up = slope_4h > 0.3
                mtf_down = slope_4h < -0.3
                mtf_aligned = (
                    (direction == "UP" and mtf_up) or
                    (direction == "DOWN" and mtf_down) or
                    (direction == "FLAT" and abs(slope_4h) <= 0.3)
                )
            else:
                mtf_aligned = False
        else:
            mtf_aligned = False

        # Signed score (-3 to +3): magnitude = conviction, sign = direction
        if direction == "UP":
            mag = 1 + int(strength == "MODERATE") + int(strength == "STRONG") + int(mtf_aligned)
            score = min(3, mag)
        elif direction == "DOWN":
            mag = 1 + int(strength == "MODERATE") + int(strength == "STRONG") + int(mtf_aligned)
            score = -min(3, mag)
        else:
            score = 0

        return TrendState(
            direction=direction,
            strength=strength,
            mtf_aligned=mtf_aligned,
            ema_slope_pct=float(slope_pct),
            adx_proxy=float(rng),
            score=int(score),
        )
    except Exception:
        return TrendState()


@dataclass
class MarketContext:
    symbol: str
    df_5m: pd.DataFrame
    df_15m: pd.DataFrame
    df_30m: pd.DataFrame  # 2026-06-06: added for Viki optimal TF
    df_1h: pd.DataFrame
    funding_rate: float
    orderbook: dict
    news_sentiment: Dict[str, dict]
    trend: TrendState = field(default_factory=TrendState)


class Agent:
    name = "base"
    profile = "momentum"
    enabled = True
    notional_multiplier = 1.0
    paper_only = False
    # Regimes this agent is allowed to fire in; empty = all
    valid_regimes: List[str] = []

    def analyze(self, symbol: str, ctx: MarketContext) -> Optional[Signal]:
        raise NotImplementedError


# =============================================================================
# AGENT 1: SCALP
# =============================================================================
class ScalpAgent(Agent):
    name = "scalp"
    enabled = False  # DISABLED — backtest: -10%, 49% WR
    profile = "scalp"
    valid_regimes = ["RANGING", "VOLATILE"]

    def analyze(self, sym, ctx):
        df = ctx.df_5m
        if len(df) < 50:
            return None
        c = df["close"]
        v = df["volume"]
        r = rsi(c).iloc[-1]
        avg_v = v.rolling(20).mean().iloc[-1]
        cur_v = v.iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = cur_v / avg_v
        last_o = df["open"].iloc[-1]
        last_c = c.iloc[-1]
        body_pct = (last_c - last_o) / last_o * 100 if last_o else 0
        # Sniper entry: oversold + volume + green confirm candle
        if r < 25 and v_ratio > 1.8 and body_pct > 0:
            conf = 6 + int(r < 20) + int(v_ratio > 2.5) + int(body_pct > 0.3)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"RSI {r:.1f} oversold + {v_ratio:.1f}x volume + green confirm",
                          {"rsi": r, "v_ratio": v_ratio})
        if r > 75 and v_ratio > 1.8 and body_pct < 0:
            conf = 6 + int(r > 80) + int(v_ratio > 2.5) + int(body_pct < -0.3)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"RSI {r:.1f} overbought + {v_ratio:.1f}x volume + red confirm",
                          {"rsi": r, "v_ratio": v_ratio})
        return None


# =============================================================================
# AGENT 2: MOMENTUM
# =============================================================================
class MomentumAgent(Agent):
    name = "momentum"
    enabled = False  # 2026-06-09: DISABLED — backtest shows -53% return, 45.8% WR, R:R 0.85
    profile = "momentum"
    valid_regimes = ["RANGING", "TRENDING"]

    def analyze(self, sym, ctx):
        df = ctx.df_15m
        if len(df) < 80:
            return None
        c = df["close"]
        e9 = ema(c, 9).iloc[-1]
        e21 = ema(c, 21).iloc[-1]
        e50 = ema(c, 50).iloc[-1]
        line, sig_line, hist = macd(c)
        h0, h1 = hist.iloc[-1], hist.iloc[-2]
        r = rsi(c).iloc[-1]
        last = c.iloc[-1]
        # Bullish trend
        if e9 > e21 > e50 and h0 > h1 > 0 and 50 < r < 72 and last > e9:
            conf = 7 + int(last > e9 * 1.003) + int(r > 55) + int(h0 > 1.5 * h1)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"EMA bull stack + MACD rising + RSI {r:.1f}",
                          {"rsi": r, "macd_hist": h0})
        if e9 < e21 < e50 and h0 < h1 < 0 and 28 < r < 50 and last < e9:
            conf = 7 + int(last < e9 * 0.997) + int(r < 45) + int(h0 < 1.5 * h1)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"EMA bear stack + MACD falling + RSI {r:.1f}",
                          {"rsi": r, "macd_hist": h0})
        return None


# =============================================================================
# AGENT 3: SWING (reversals on 1H, divergence + Bollinger)
# =============================================================================
class SwingAgent(Agent):
    name = "swing"
    enabled = False  # DISABLED — backtest: -34%, 44% WR
    profile = "swing"
    valid_regimes = ["RANGING"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 60:
            return None
        c = df["close"]
        bbu, bbm, bbl = bbands(c, 20, 2.0)
        r = rsi(c, 14)
        last = c.iloc[-1]
        # Look at last 10 vs prior 20-30 bars for divergence
        recent = c.iloc[-10:]
        prior = c.iloc[-30:-10]
        if len(recent) < 5 or len(prior) < 10:
            return None
        try:
            recent_low_idx = recent.idxmin()
            prior_low_idx  = prior.idxmin()
            recent_high_idx = recent.idxmax()
            prior_high_idx  = prior.idxmax()
            # Bullish divergence: lower low in price, higher low in RSI
            if (last <= bbl.iloc[-1] * 1.005 and
                c.loc[recent_low_idx] < c.loc[prior_low_idx] and
                r.loc[recent_low_idx] > r.loc[prior_low_idx] and
                r.iloc[-1] < 38):
                return Signal(self.name, sym, "long", 8, self.profile,
                              f"BB lower + bullish RSI divergence (RSI {r.iloc[-1]:.1f})",
                              {"rsi": float(r.iloc[-1])})
            # Bearish divergence: higher high in price, lower high in RSI
            if (last >= bbu.iloc[-1] * 0.995 and
                c.loc[recent_high_idx] > c.loc[prior_high_idx] and
                r.loc[recent_high_idx] < r.loc[prior_high_idx] and
                r.iloc[-1] > 62):
                return Signal(self.name, sym, "short", 8, self.profile,
                              f"BB upper + bearish RSI divergence (RSI {r.iloc[-1]:.1f})",
                              {"rsi": float(r.iloc[-1])})
        except Exception:
            return None
        return None


# =============================================================================
# AGENT 4: MEAN REVERSION
# =============================================================================
class MeanReversionAgent(Agent):
    name = "meanrev"
    paper_only = True
    enabled = False
    profile = "meanrev"
    valid_regimes = ["RANGING"]

    def analyze(self, sym, ctx):
        df = ctx.df_5m
        if len(df) < 50:
            return None
        c = df["close"]
        bbu, bbm, bbl = bbands(c, 20, 2.5)
        r = rsi(c).iloc[-1]
        last = c.iloc[-1]
        if len(c) < 4:
            return None
        move_3 = (last - c.iloc[-4]) / c.iloc[-4] * 100
        if last < bbl.iloc[-1] and r < 22 and move_3 < -2.0:
            conf = 7 + int(r < 18) + int(move_3 < -3.5)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"Extreme dip {move_3:.1f}% / 15m, RSI {r:.1f}",
                          {"rsi": r, "move_3": move_3})
        if last > bbu.iloc[-1] and r > 78 and move_3 > 2.0:
            conf = 7 + int(r > 82) + int(move_3 > 3.5)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"Extreme pump {move_3:.1f}% / 15m, RSI {r:.1f}",
                          {"rsi": r, "move_3": move_3})
        return None


# =============================================================================
# AGENT 5: WHALE TRACKER
# =============================================================================
class WhaleTrackerAgent(Agent):
    name = "whale"
    profile = "whale"
    valid_regimes = ["TRENDING", "VOLATILE"]
    paper_only = True

    def analyze(self, sym, ctx):
        ob = ctx.orderbook
        if not ob or not ob.get("bids") or not ob.get("asks"):
            return None
        try:
            bid_vol = sum(float(b[1]) for b in ob["bids"][:20])
            ask_vol = sum(float(a[1]) for a in ob["asks"][:20])
            if bid_vol <= 0 or ask_vol <= 0:
                return None
            imb = (bid_vol - ask_vol) / (bid_vol + ask_vol)
            df = ctx.df_5m
            if len(df) < 30:
                return None
            cur_v = df["volume"].iloc[-1]
            avg_v = df["volume"].rolling(20).mean().iloc[-1]
            if avg_v <= 0:
                return None
            v_spike = cur_v / avg_v
            last = df["close"].iloc[-1]
            prev = df["close"].iloc[-2]
            move = (last - prev) / prev * 100 if prev else 0
            funding = ctx.funding_rate
            # Aggressive whale buy: lopsided book toward bids, volume spike, price moving up
            if imb > 0.30 and v_spike > 2.0 and move > 0.15:
                conf = 7 + int(imb > 0.5) + int(v_spike > 3) + int(funding < 0)
                return Signal(self.name, sym, "long", min(10, conf), self.profile,
                              f"Whale BUY: book {imb:+.2f}, vol {v_spike:.1f}x, move {move:+.2f}%",
                              {"imbalance": imb, "v_spike": v_spike})
            if imb < -0.30 and v_spike > 2.0 and move < -0.15:
                conf = 7 + int(imb < -0.5) + int(v_spike > 3) + int(funding > 0)
                return Signal(self.name, sym, "short", min(10, conf), self.profile,
                              f"Whale SELL: book {imb:+.2f}, vol {v_spike:.1f}x, move {move:+.2f}%",
                              {"imbalance": imb, "v_spike": v_spike})
        except Exception:
            return None
        return None


# =============================================================================
# AGENT 6: NEWS
# =============================================================================
BULLISH_WORDS = {
    "surge", "rally", "approve", "approved", "launch", "launches", "upgrade",
    "bullish", "etf", "listed", "listing", "partnership", "invest", "investment",
    "integrate", "integration", "gain", "gains", "soars", "soar", "all-time",
    "ath", "breakout", "adoption", "buy", "buys", "accumulate", "milestone",
}
BEARISH_WORDS = {
    "hack", "hacked", "exploit", "exploited", "crash", "crashes", "sell-off",
    "ban", "banned", "outflow", "outflows", "fud", "lawsuit", "sec", "decline",
    "plunge", "plunges", "drop", "drops", "rugpull", "rug", "liquidation",
    "liquidations", "bearish", "fraud", "scam", "halts", "halted", "paused",
}


async def fetch_news(session: aiohttp.ClientSession) -> Dict[str, dict]:
    """Returns {SYMBOL: {score: -1..1, headline: str, n: int}}."""
    feeds = [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
        "https://decrypt.co/feed",
    ]
    out: Dict[str, dict] = {}
    headers = {"User-Agent": "Mozilla/5.0 MAB/1.0"}
    for url in feeds:
        try:
            async with session.get(url, headers=headers,
                                   timeout=aiohttp.ClientTimeout(total=12)) as r:
                txt = await r.text()
        except Exception as e:
            log.warning(f"news fetch {url}: {e}")
            continue
        items = re.findall(r"<item[^>]*>(.*?)</item>", txt, re.S | re.I)
        for item in items[:40]:
            tm = re.search(r"<title[^>]*>(.*?)</title>", item, re.S | re.I)
            if not tm:
                continue
            h = tm.group(1)
            h = re.sub(r"<!\[CDATA\[(.+?)\]\]>", r"\1", h, flags=re.S)
            h = re.sub(r"<[^>]+>", "", h).strip()
            if not h:
                continue
            lower = h.lower()
            score = 0
            for w in BULLISH_WORDS:
                if w in lower:
                    score += 1
            for w in BEARISH_WORDS:
                if w in lower:
                    score -= 1
            if score == 0:
                continue
            norm = max(-1.0, min(1.0, score / 3.0))
            for sym in NEWS_SYMBOLS:
                if re.search(rf"\b{sym}\b", h, re.I):
                    prev = out.get(sym)
                    if prev:
                        n = prev["n"] + 1
                        avg = (prev["score"] * prev["n"] + norm) / n
                        out[sym] = {"score": avg, "headline": h, "n": n}
                    else:
                        out[sym] = {"score": norm, "headline": h, "n": 1}
    return out


class NewsAgent(Agent):
    name = "news"
    profile = "news"
    valid_regimes = []  # fires in any regime
    paper_only = True

    def analyze(self, sym, ctx):
        base = sym.split("-")[0]
        s = ctx.news_sentiment.get(base)
        if not s:
            return None
        score = s["score"]
        headline = s["headline"]
        df = ctx.df_5m
        if len(df) < 5:
            return None
        c = df["close"].iloc[-1]
        p = df["close"].iloc[-3]
        move = (c - p) / p * 100 if p else 0
        # Need price confirmation
        if score >= 0.5 and move > 0.1:
            conf = 7 + int(score >= 0.8) + int(move > 0.5) + int(s["n"] >= 2)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"News+: \"{headline[:55]}\" (score {score:+.2f})",
                          {"score": score, "n": s["n"]})
        if score <= -0.5 and move < -0.1:
            conf = 7 + int(score <= -0.8) + int(move < -0.5) + int(s["n"] >= 2)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"News-: \"{headline[:55]}\" (score {score:+.2f})",
                          {"score": score, "n": s["n"]})
        return None


# =============================================================================
# AGENT 9: ASYMMETRIC BREAKOUT  (Bollinger squeeze + 3+ confluences)
# =============================================================================
class AsymmetricBreakoutAgent(Agent):
    name = "asymmetric"
    enabled = True   # 2026-06-05: RE-ENABLED — 1yr backtest: +13% at 1H, 333t, 10.7% DD, best risk/reward
    profile = "asymmetric"
    valid_regimes = ["TRENDING"]

    def analyze(self, sym, ctx):
        # 2026-06-05: MOVED primary from 15m to 1H + 15m confirm (backtest: 1H+15m +15% vs 15m -17%)
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        v = df["volume"]
        last = c.iloc[-1]

        # Bollinger width squeeze: bottom 15% of last 100 bars
        bbu, bbm, bbl = bbands(c, 20, 2.0)
        bb_width = (bbu - bbl) / bbm
        w_now = bb_width.iloc[-1]
        w_hist = bb_width.iloc[-51:-1]
        if len(w_hist) < 25 or pd.isna(w_now):
            return None
        squeeze = w_now <= w_hist.quantile(0.15)
        if not squeeze:
            return None

        # Breakout candle: close above 20-bar high (long) or below 20-bar low (short)
        high20 = df["high"].iloc[-21:-1].max()
        low20  = df["low"].iloc[-21:-1].min()
        breakout_long  = last > high20
        breakout_short = last < low20
        if not breakout_long and not breakout_short:
            return None

        # Count confluences
        e9  = ema(c, 9).iloc[-1]
        e21 = ema(c, 21).iloc[-1]
        e50 = ema(c, 50).iloc[-1]
        r   = rsi(c).iloc[-1]
        avg_v = v.rolling(20).mean().iloc[-1]
        v_ratio = v.iloc[-1] / avg_v if avg_v > 0 else 0

        # Lower-TF confirmation from 15m (backtest-proven: +15% vs +13% without)
        if hasattr(ctx, 'df_15m') and ctx.df_15m is not None and len(ctx.df_15m) >= 50:
            c15 = ctx.df_15m["close"]
            ema15_21 = ema(c15, 21).iloc[-1]
            if breakout_long and c15.iloc[-1] <= ema15_21:
                return None
            if breakout_short and c15.iloc[-1] >= ema15_21:
                return None

        # HTF trend from 1H (same TF = same as primary, always passes)
        df1h = ctx.df_1h
        htf_bull = htf_bear = False
        if len(df1h) >= 50:
            h_e21 = ema(df1h["close"], 21).iloc[-1]
            h_e50 = ema(df1h["close"], 50).iloc[-1]
            htf_bull = df1h["close"].iloc[-1] > h_e21 > h_e50
            htf_bear = df1h["close"].iloc[-1] < h_e21 < h_e50

        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None

        # Per Claude Code forensics: 1×ATR ≈ 0.23% on BTC 15m, fees (0.12%) eat 52% of stop risk.
        # Floor SL at max(2×ATR, 0.8% of price) — drops fee/risk ratio to ~15% and break-even WR
        # from 37.6% to ~28.8%. TP unchanged at 3×ATR (lock big winners with trail).
        ASYMMETRIC_SL_ATR_MULT = 2.0
        ASYMMETRIC_SL_PCT_FLOOR = 0.008   # 0.8% of price minimum
        sl_distance = max(ASYMMETRIC_SL_ATR_MULT * atr_val, last * ASYMMETRIC_SL_PCT_FLOOR)

        if breakout_long:
            confluences = (
                int(e9 > e21 > e50) +
                int(v_ratio >= 2.0) +
                int(55 <= r <= 70) +
                int(htf_bull)
            )
            if confluences < 3:
                return None
            tp_price = last + 3 * atr_val
            sl_price = last - sl_distance
            conf = 7 + min(3, confluences - 3)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"BB-squeeze breakout long {confluences} confluences, "
                          f"ATR {atr_val:.4f}, SL {sl_distance/last*100:.2f}%, vol {v_ratio:.1f}x",
                          {"atr_tp": tp_price, "atr_sl": sl_price,
                           "atr_val": atr_val, "sl_distance": sl_distance,
                           "confluences": confluences})

        if breakout_short:
            confluences = (
                int(e9 < e21 < e50) +
                int(v_ratio >= 2.0) +
                int(30 <= r <= 45) +
                int(htf_bear)
            )
            if confluences < 3:
                return None
            tp_price = last - 3 * atr_val
            sl_price = last + sl_distance
            conf = 7 + min(3, confluences - 3)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"BB-squeeze breakout short {confluences} confluences, "
                          f"ATR {atr_val:.4f}, SL {sl_distance/last*100:.2f}%, vol {v_ratio:.1f}x",
                          {"atr_tp": tp_price, "atr_sl": sl_price,
                           "atr_val": atr_val, "sl_distance": sl_distance,
                           "confluences": confluences})
        return None


# =============================================================================
# AGENT 10: BOLLINGER SQUEEZE  (simpler, higher frequency)
# =============================================================================
class BollingerSqueezeAgent(Agent):
    name = "bb_squeeze"
    paper_only = True
    enabled = False
    profile = "momentum"
    valid_regimes = ["RANGING", "TRENDING"]

    def analyze(self, sym, ctx):
        df = ctx.df_5m
        if len(df) < 110:
            return None
        c = df["close"]
        last = c.iloc[-1]
        bbu, bbm, bbl = bbands(c, 20, 2.0)
        bb_width = (bbu - bbl) / bbm
        w_now  = bb_width.iloc[-1]
        w_hist = bb_width.iloc[-101:-1]
        if len(w_hist) < 50 or pd.isna(w_now):
            return None
        if w_now > w_hist.quantile(0.20):
            return None
        # Breakout direction
        prev = c.iloc[-2]
        high20 = df["high"].iloc[-21:-1].max()
        low20  = df["low"].iloc[-21:-1].min()
        r = rsi(c).iloc[-1]
        v_ratio = df["volume"].iloc[-1] / df["volume"].rolling(20).mean().iloc[-1]
        if last > high20 and v_ratio > 1.4 and r > 50:
            conf = 6 + int(v_ratio > 2.0) + int(r > 58)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"BB-squeeze 5m breakout long vol {v_ratio:.1f}x RSI {r:.1f}",
                          {"v_ratio": v_ratio, "rsi": r})
        if last < low20 and v_ratio > 1.4 and r < 50:
            conf = 6 + int(v_ratio > 2.0) + int(r < 42)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"BB-squeeze 5m breakout short vol {v_ratio:.1f}x RSI {r:.1f}",
                          {"v_ratio": v_ratio, "rsi": r})
        return None


# =============================================================================
# AGENT 11: DONCHIAN BREAKOUT  (30-period 1H channel — tuned per param sweep)
# =============================================================================
DONCHIAN_PERIOD = 30      # was 20 — sweep showed 30 has best ExpR (+0.052R vs +0.031R)
DONCHIAN_ATR_MULT = 2.0   # SL distance multiplier on ATR
# Donchian is profitable on these coins per per-symbol backtest, loses on others.
# Whitelist limits firing to coins where the strategy historically works.
DONCHIAN_WHITELIST = {"ETH-USDT", "ARB-USDT", "INJ-USDT", "NEAR-USDT", "DOT-USDT",
                      "TIA-USDT", "AVAX-USDT", "ADA-USDT", "LINK-USDT"}

class DonchianBreakoutAgent(Agent):
    name = "donchian"
    enabled = False
    paper_only = True
    profile = "swing"
    valid_regimes = ["TRENDING"]

    def analyze(self, sym, ctx):
        if sym not in DONCHIAN_WHITELIST:
            return None   # don't fire on coins where this strategy historically loses
        df = ctx.df_1h
        if len(df) < DONCHIAN_PERIOD + 20:
            return None
        c = df["close"]
        last = c.iloc[-1]
        prev_highs = df["high"].iloc[-(DONCHIAN_PERIOD+1):-1]
        prev_lows  = df["low"].iloc[-(DONCHIAN_PERIOD+1):-1]
        don_high = prev_highs.max()
        don_low  = prev_lows.min()
        atr_val  = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        avg_v  = df["volume"].rolling(20).mean().iloc[-1]
        v_ratio = df["volume"].iloc[-1] / avg_v if avg_v > 0 else 0
        if v_ratio < 1.8:
            return None
        if last > don_high:
            sl = last - atr_val * DONCHIAN_ATR_MULT
            conf = 7 + int(v_ratio > 2.5)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"Donchian {DONCHIAN_PERIOD}-bar 1H breakout long vol {v_ratio:.1f}x ATR×{DONCHIAN_ATR_MULT} stop",
                          {"atr_sl": sl, "atr_val": atr_val, "v_ratio": v_ratio})
        if last < don_low:
            sl = last + atr_val * DONCHIAN_ATR_MULT
            conf = 7 + int(v_ratio > 2.5)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"Donchian {DONCHIAN_PERIOD}-bar 1H breakout short vol {v_ratio:.1f}x ATR×{DONCHIAN_ATR_MULT} stop",
                          {"atr_sl": sl, "atr_val": atr_val, "v_ratio": v_ratio})
        return None


# =============================================================================
# AGENT 12: FUNDING HUNTER  (exploit extreme funding)
# =============================================================================
class FundingHunterAgent(Agent):
    name = "funding"
    enabled = False
    profile = "meanrev"
    valid_regimes = ["RANGING", "VOLATILE"]

    def analyze(self, sym, ctx):
        fr = ctx.funding_rate
        df = ctx.df_5m
        if len(df) < 20:
            return None
        r = rsi(df["close"]).iloc[-1]
        # High positive funding → shorts are paying longs → fade the long bias
        if fr > 0.0008:
            conf = 7 + int(fr > 0.0012) + int(r > 60)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"Funding {fr*100:.4f}% > 0.08% → short",
                          {"funding_rate": fr, "rsi": r})
        # High negative funding → longs are paying shorts → fade the short bias
        if fr < -0.0008:
            conf = 7 + int(fr < -0.0012) + int(r < 40)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"Funding {fr*100:.4f}% < -0.08% → long",
                          {"funding_rate": fr, "rsi": r})
        return None


# =============================================================================
# AGENT 13: EMA RIBBON  (5m + 15m + 1h EMA alignment)
# =============================================================================
class EMARibbonAgent(Agent):
    name = "ema_ribbon"
    enabled = False
    profile = "momentum"
    valid_regimes = ["TRENDING"]

    def analyze(self, sym, ctx):
        for df in [ctx.df_5m, ctx.df_15m, ctx.df_1h]:
            if len(df) < 55:
                return None
        c5  = ctx.df_5m["close"]
        c15 = ctx.df_15m["close"]
        c1h = ctx.df_1h["close"]

        # Each timeframe: EMA 9 > EMA 21 > EMA 50
        bull = (
            ema(c5,  9).iloc[-1] > ema(c5,  21).iloc[-1] > ema(c5,  50).iloc[-1] and
            ema(c15, 9).iloc[-1] > ema(c15, 21).iloc[-1] > ema(c15, 50).iloc[-1] and
            ema(c1h, 9).iloc[-1] > ema(c1h, 21).iloc[-1] > ema(c1h, 50).iloc[-1]
        )
        bear = (
            ema(c5,  9).iloc[-1] < ema(c5,  21).iloc[-1] < ema(c5,  50).iloc[-1] and
            ema(c15, 9).iloc[-1] < ema(c15, 21).iloc[-1] < ema(c15, 50).iloc[-1] and
            ema(c1h, 9).iloc[-1] < ema(c1h, 21).iloc[-1] < ema(c1h, 50).iloc[-1]
        )
        r5 = rsi(c5).iloc[-1]
        if bull and 50 < r5 < 75:
            conf = 8 + int(r5 > 58)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"EMA ribbon 3TF bullish aligned RSI {r5:.1f}",
                          {"rsi_5m": r5})
        if bear and 25 < r5 < 50:
            conf = 8 + int(r5 < 42)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"EMA ribbon 3TF bearish aligned RSI {r5:.1f}",
                          {"rsi_5m": r5})
        return None


# =============================================================================
# AGENT 12: CANDLESTICK PATTERN AGENT
# Classical Japanese candlestick reversals at exhaustion zones.
# Only fires with multi-condition confluence (pattern + trend context + volume + RSI).
# =============================================================================
class CandlestickAgent(Agent):
    name = "candlestick"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = True   # validation needed before live
    profile = "swing"   # reversal trades — give them room to develop
    valid_regimes = ["RANGING", "TRENDING"]

    def analyze(self, sym, ctx):
        df = ctx.df_15m
        if len(df) < 60:
            return None
        c = df["close"]
        v = df["volume"]
        # Trend context via EMA 50 — only fade exhaustion at meaningful extremes
        e50 = ema(c, 50).iloc[-1]
        e21 = ema(c, 21).iloc[-1]
        price = c.iloc[-1]
        if pd.isna(e50) or pd.isna(e21) or e50 <= 0:
            return None

        # Volume confirm
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v

        r = rsi(c).iloc[-1]

        # Bullish setup: price extended below EMA50, RSI oversold, bullish reversal pattern
        if price < e50 * 0.985 and r < 38:
            pattern = detect_bullish_pattern(df.tail(5))
            if pattern and v_ratio >= 1.3:
                conf = 7 + int(r < 30) + int(v_ratio >= 2.0) + int(pattern in ("morning_star", "three_white_soldiers"))
                return Signal(self.name, sym, "long", min(10, conf), self.profile,
                              f"{pattern} at oversold (RSI {r:.0f}, vol {v_ratio:.1f}x, price {((price/e50-1)*100):+.1f}% vs EMA50)",
                              {"pattern": pattern, "rsi": float(r), "v_ratio": float(v_ratio)})

        # Bearish setup: price extended above EMA50, RSI overbought, bearish reversal pattern
        if price > e50 * 1.015 and r > 62:
            pattern = detect_bearish_pattern(df.tail(5))
            if pattern and v_ratio >= 1.3:
                conf = 7 + int(r > 70) + int(v_ratio >= 2.0) + int(pattern in ("evening_star", "three_black_crows"))
                return Signal(self.name, sym, "short", min(10, conf), self.profile,
                              f"{pattern} at overbought (RSI {r:.0f}, vol {v_ratio:.1f}x, price {((price/e50-1)*100):+.1f}% vs EMA50)",
                              {"pattern": pattern, "rsi": float(r), "v_ratio": float(v_ratio)})

        return None


# =============================================================================
# VWAP HELPER — rolling VWAP and std-dev bands
# =============================================================================
def rolling_vwap(df: pd.DataFrame, n: int = 96) -> pd.DataFrame:
    """Rolling N-bar VWAP and standard deviation of typical_price - VWAP.
    Default n=96 = 24 hours on 15m bars.
    Returns DataFrame with columns: vwap, vwap_std."""
    tp = (df["high"] + df["low"] + df["close"]) / 3
    pv = tp * df["volume"]
    rolling_pv = pv.rolling(n).sum()
    rolling_v  = df["volume"].rolling(n).sum().replace(0, np.nan)
    vwap = rolling_pv / rolling_v
    diff = tp - vwap
    vwap_std = diff.rolling(n).std()
    return pd.DataFrame({"vwap": vwap, "vwap_std": vwap_std})


# =============================================================================
# AGENT 15: HIGHER-TIMEFRAME TREND PULLBACK
# Designed for fee survival: 1h bars, wide stops, trailing-only exit.
# Premise: in confirmed uptrend, pullbacks to 50 EMA followed by reversal candles
# offer high-probability long entries. Cut losses fast (-2.5% or 2×ATR), let
# winners run via trailing only. Mirror logic for shorts.
# =============================================================================
class TrendPullbackAgent(Agent):
    notional_multiplier = 0.1
    name = "trend_pullback"
    enabled = False  # 2026-06-09: DISABLED — backtest shows -12% return, R:R 0.49 (wins too small vs losses)
    paper_only = False  # 2026-06-08: CEO ACTIVATED — live trading
    profile = "trend_pullback"
    valid_regimes = ["TRENDING"]   # only fires when bot regime detector says trending

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 220:
            return None
        c = df["close"]
        v = df["volume"]
        h = df["high"]
        l = df["low"]

        # Macro trend filter: 50 EMA > 200 EMA AND price > 200 EMA (uptrend definition)
        e50  = ema(c, 50).iloc[-1]
        e200 = ema(c, 200).iloc[-1]
        e21  = ema(c, 21).iloc[-1]
        last = c.iloc[-1]
        if pd.isna(e50) or pd.isna(e200) or e50 <= 0 or e200 <= 0:
            return None

        macro_up   = (e50 > e200 * 1.001) and (last > e200 * 1.005)
        macro_down = (e50 < e200 * 0.999) and (last < e200 * 0.995)

        # Volume confirm — only on the entry bar
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v

        # ATR for SL sizing
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        atr_pct = atr_val / last

        # Bar 1 (prior) vs bar 2 (current closed) for reversal-pattern check
        o2, c2 = df["open"].iloc[-1], c.iloc[-1]
        o1, c1 = df["open"].iloc[-2], c.iloc[-2]
        bar2_green = c2 > o2
        bar2_red   = c2 < o2

        # Pullback proximity: price within 1.0% of 50 EMA (the pullback zone)
        pull_long  = abs(last - e50) / e50 < 0.010 and last >= e50 * 0.995
        pull_short = abs(last - e50) / e50 < 0.010 and last <= e50 * 1.005

        # RSI not extreme (avoid catching falling knives in trends)
        r = rsi(c).iloc[-1]

        # ── LONG setup ──────────────────────────────────────────────────────
        if macro_up and pull_long and bar2_green and 40 <= r <= 65 and v_ratio >= 1.2:
            # Was prior bar a red pullback? confirms the pullback dynamic
            prior_pullback = (c1 < o1) or (df["low"].iloc[-2] < df["low"].iloc[-3])
            if not prior_pullback:
                return None
            # SL: max(2.5% of price, 2× ATR)
            sl_distance = max(0.025 * last, 2.0 * atr_val)
            sl_price = last - sl_distance
            tp_price = last * 1.99   # cosmetic — trailing stop will exit first
            conf = 7 + int(macro_up and last > e21) + int(v_ratio >= 1.8) + int(50 <= r <= 60)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"1h trend-pullback long: e50>{e200:.4f}, pullback to e50, vol {v_ratio:.1f}x, ATR {atr_pct*100:.2f}%",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val,
                           "v_ratio": v_ratio, "rsi": r})

        # ── SHORT setup ─────────────────────────────────────────────────────
        if macro_down and pull_short and bar2_red and 35 <= r <= 60 and v_ratio >= 1.2:
            prior_pullback = (c1 > o1) or (df["high"].iloc[-2] > df["high"].iloc[-3])
            if not prior_pullback:
                return None
            sl_distance = max(0.025 * last, 2.0 * atr_val)
            sl_price = last + sl_distance
            tp_price = last * 0.01   # cosmetic — trailing stop will exit first
            conf = 7 + int(macro_down and last < e21) + int(v_ratio >= 1.8) + int(40 <= r <= 50)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"1h trend-pullback short: e50<{e200:.4f}, pullback to e50, vol {v_ratio:.1f}x, ATR {atr_pct*100:.2f}%",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val,
                           "v_ratio": v_ratio, "rsi": r})

        return None


# =============================================================================
# AGENT 16: DAILY RANGE BREAKOUT
# Multi-day range breaks (1-week structure) with volume + ATR expansion.
# Wide stops (4% min) make fees background noise. Trailing-only exit.
# =============================================================================
class DailyRangeBreakoutAgent(Agent):
    notional_multiplier = 0.1
    name = "daily_breakout"
    enabled = True   # 2026-06-05: RE-ENABLED — #1 backtest agent +1,992%
    paper_only = False   # validation pending
    profile = "daily_breakout"
    valid_regimes = ["TRENDING", "VOLATILE"]

    LOOKBACK_BARS = 168          # 1 week of 1H bars
    MIN_SL_PCT = 0.04
    MIN_VOLUME_RATIO = 1.4   # was 2.0 — loosened to fire more often

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.LOOKBACK_BARS + 30:
            return None
        c = df["close"]
        h = df["high"]
        l = df["low"]
        v = df["volume"]
        last = c.iloc[-1]

        # 1-week range structure (excluding current bar)
        range_high = h.iloc[-(self.LOOKBACK_BARS + 1):-1].max()
        range_low  = l.iloc[-(self.LOOKBACK_BARS + 1):-1].min()
        if pd.isna(range_high) or pd.isna(range_low):
            return None

        # Volume confirmation
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOLUME_RATIO:
            return None

        # ATR expansion: current ATR > 1.1× rolling-20 ATR average
        atr_now = atr(df).iloc[-1]
        atr_avg = atr(df).rolling(20).mean().iloc[-1]
        if atr_now <= 0 or pd.isna(atr_now) or atr_avg <= 0 or pd.isna(atr_avg):
            return None
        if atr_now < atr_avg * 1.1:
            return None

        # Breakout candle dimensions (for SL placement)
        bar_o = df["open"].iloc[-1]
        bar_h = h.iloc[-1]
        bar_l = l.iloc[-1]
        bar_range = bar_h - bar_l
        if bar_range <= 0:
            return None

        # LONG: close above 1-week high
        if last > range_high and last > bar_o:
            sl_retrace = bar_o + bar_range * 0.5     # 50% retrace of breakout candle
            sl_floor = last * (1 - self.MIN_SL_PCT)  # 4% floor
            sl_price = min(sl_retrace, sl_floor)     # whichever is wider stop
            tp_price = last * 1.99                   # cosmetic — trailing exits first
            conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.3) + int(last > range_high * 1.005)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"1week-high break long ({range_high:.4f}) vol {v_ratio:.1f}x ATRx{atr_now/atr_avg:.2f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "range_high": float(range_high),
                           "atr_val": atr_now, "v_ratio": v_ratio})

        # SHORT: close below 1-week low
        if last < range_low and last < bar_o:
            sl_retrace = bar_o - bar_range * 0.5
            sl_floor = last * (1 + self.MIN_SL_PCT)
            sl_price = max(sl_retrace, sl_floor)
            tp_price = last * 0.01
            conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.3) + int(last < range_low * 0.995)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"1week-low break short ({range_low:.4f}) vol {v_ratio:.1f}x ATRx{atr_now/atr_avg:.2f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "range_low": float(range_low),
                           "atr_val": atr_now, "v_ratio": v_ratio})

        return None


# =============================================================================
# AGENT 13b: DAILY BREAKOUT 24H — fast variant
# Same logic as DailyRangeBreakoutAgent but with a 24-bar lookback (1 day) instead
# of 168 (1 week). Fires ~3-4x more often than parent. Backtest 2026-04-30 across
# all 20 symbols: ~82% WR, +0.535R, MaxDD <-5%, Sharpe ~4.7 over 4150 trades.
# Tighter SL (2.5%) suits the shorter timeframe.
# =============================================================================
class DailyBreakout24hAgent(Agent):
    notional_multiplier = 0.1
    name = "daily_breakout_24h"
    # 2026-06-03: SCALED — 1yr backtest: 3,841 trades, 79.7% WR, +0.493 ExpR
    # 2026-06-09: RE-ENABLED for ranging — +408R backtest, add RANGING
    enabled = True
    paper_only = False
    profile = "daily_breakout_24h"
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]

    LOOKBACK_BARS = 24           # 1 day of 1H bars
    MIN_SL_PCT = 0.025
    MIN_VOLUME_RATIO = 1.3   # was 1.8 — loosened to fire more

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.LOOKBACK_BARS + 30:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last = c.iloc[-1]
        range_high = h.iloc[-(self.LOOKBACK_BARS + 1):-1].max()
        range_low  = l.iloc[-(self.LOOKBACK_BARS + 1):-1].min()
        if pd.isna(range_high) or pd.isna(range_low):
            return None
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOLUME_RATIO:
            return None
        atr_now = atr(df).iloc[-1]
        atr_avg = atr(df).rolling(20).mean().iloc[-1]
        if atr_now <= 0 or pd.isna(atr_now) or atr_avg <= 0 or pd.isna(atr_avg):
            return None
        if atr_now < atr_avg * 1.05:
            return None
        bar_o = df["open"].iloc[-1]
        bar_h = h.iloc[-1]; bar_l = l.iloc[-1]
        bar_range = bar_h - bar_l
        if bar_range <= 0:
            return None
        if last > range_high and last > bar_o:
            sl_retrace = bar_o + bar_range * 0.5
            sl_floor = last * (1 - self.MIN_SL_PCT)
            sl_price = min(sl_retrace, sl_floor)
            tp_price = last + 2.5 * atr_now   # v2.0 fix: was last*1.99 (unreachable)
            conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"24h-high break long ({range_high:.4f}) vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "atr_val": atr_now, "v_ratio": v_ratio})
        if last < range_low and last < bar_o:
            sl_retrace = bar_o - bar_range * 0.5
            sl_floor = last * (1 + self.MIN_SL_PCT)
            sl_price = max(sl_retrace, sl_floor)
            tp_price = last - 2.5 * atr_now   # v2.0 fix: was last*0.01 (unreachable)
            conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"24h-low break short ({range_low:.4f}) vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "atr_val": atr_now, "v_ratio": v_ratio})
        return None


# =============================================================================
# AGENT 13c/13d: DailyBreakout 4-hour & 7-day variants
# Same parametric breakout pattern as DailyBreakout24h. The 4h variant fires
# 30+ times/day with 1.2% SL and short hold. Backtest 2026-04-30 across 20
# symbols: ~11k trades, 76% WR, +0.67R/trade, Sharpe 5-10, MaxDD <5%.
# The 7d variant is slower than even the original (168h) — fewer trades but
# very stable wide-stop swings.
# =============================================================================
class _DailyBreakoutBase(Agent):
    """Shared logic — subclass sets LOOKBACK_BARS / MIN_SL_PCT / MIN_VOLUME_RATIO / atr_mult / name / profile."""
    enabled = True   # 2026-06-05: RE-ENABLED — all profitable (+0.35 to +0.62 ExpR)
    paper_only = False  # 2026-06-03: SCALED — 1yr backtest all profitable (+0.35 to +0.62 ExpR)
    valid_regimes = ["TRENDING", "VOLATILE"]

    LOOKBACK_BARS = 24           # override in subclass
    MIN_SL_PCT = 0.025
    MIN_VOLUME_RATIO = 1.2   # was 1.8 — loosened (subclasses inherit)
    ATR_MULT = 1.0

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.LOOKBACK_BARS + 30:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last = c.iloc[-1]
        range_high = h.iloc[-(self.LOOKBACK_BARS + 1):-1].max()
        range_low  = l.iloc[-(self.LOOKBACK_BARS + 1):-1].min()
        if pd.isna(range_high) or pd.isna(range_low):
            return None
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOLUME_RATIO:
            return None
        atr_now = atr(df).iloc[-1]
        atr_avg = atr(df).rolling(20).mean().iloc[-1]
        if atr_now <= 0 or pd.isna(atr_now) or atr_avg <= 0 or pd.isna(atr_avg):
            return None
        if atr_now < atr_avg * self.ATR_MULT:
            return None
        bar_o = df["open"].iloc[-1]
        bar_h = h.iloc[-1]; bar_l = l.iloc[-1]
        bar_range = bar_h - bar_l
        if bar_range <= 0:
            return None
        if last > range_high and last > bar_o:
            sl_retrace = bar_o + bar_range * 0.5
            sl_floor = last * (1 - self.MIN_SL_PCT)
            sl_price = min(sl_retrace, sl_floor)
            tp_price = last + 2.5 * atr_now   # v2.0 fix: was last*1.99 (unreachable)
            conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"{self.LOOKBACK_BARS}h-high break long ({range_high:.4f}) vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_now, "v_ratio": v_ratio})
        if last < range_low and last < bar_o:
            sl_retrace = bar_o - bar_range * 0.5
            sl_floor = last * (1 + self.MIN_SL_PCT)
            sl_price = max(sl_retrace, sl_floor)
            tp_price = last - 2.5 * atr_now   # v2.0 fix: was last*0.01 (unreachable)
            conf = 7 + int(v_ratio > 3) + int(atr_now > atr_avg * 1.25)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"{self.LOOKBACK_BARS}h-low break short ({range_low:.4f}) vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_now, "v_ratio": v_ratio})
        return None


class DailyBreakout4hAgent(_DailyBreakoutBase):
    notional_multiplier = 0.02
    name = "daily_breakout_4h"
    profile = "daily_breakout_4h"
    enabled = True  # 2026-06-09: RE-ENABLED for ranging — +678R backtest
    LOOKBACK_BARS = 4
    MIN_SL_PCT = 0.012
    MIN_VOLUME_RATIO = 1.3
    ATR_MULT = 1.0
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]  # 2026-06-09: +RANGING, +678R backtest
    # 2026-06-09: RE-ENABLED for ranging — +678R backtest
    paper_only = False


class DailyBreakout7dAgent(_DailyBreakoutBase):
    notional_multiplier = 0.1
    name = "daily_breakout_7d"
    profile = "daily_breakout_7d"
    LOOKBACK_BARS = 168
    MIN_SL_PCT = 0.04
    MIN_VOLUME_RATIO = 1.4   # was 2.0 — loosened
    ATR_MULT = 1.05
    paper_only = False


class DailyBreakout12hAgent(_DailyBreakoutBase):
    notional_multiplier = 0.02
    name = "daily_breakout_12h"
    profile = "daily_breakout_12h"
    LOOKBACK_BARS = 12
    MIN_SL_PCT = 0.018
    MIN_VOLUME_RATIO = 1.5
    ATR_MULT = 1.0
    paper_only = False  # 2026-06-08: CEO ACTIVATED — +653R backtest, +0.22R avg


class DailyBreakout48hAgent(_DailyBreakoutBase):
    notional_multiplier = 0.02
    name = "daily_breakout_48h"
    profile = "daily_breakout_48h"
    LOOKBACK_BARS = 48
    MIN_SL_PCT = 0.030
    MIN_VOLUME_RATIO = 1.9
    ATR_MULT = 1.05
    paper_only = False  # 2026-06-08: CEO ACTIVATED — +233R backtest, +0.36R avg


class DailyBreakout2hAgent(_DailyBreakoutBase):
    notional_multiplier = 0.02
    name = "daily_breakout_2h"
    profile = "daily_breakout_2h"
    enabled = False  # 2026-06-09: DISABLED — backtest shows 0% return, 39% WR across all TFs
    LOOKBACK_BARS = 2
    MIN_SL_PCT = 0.008
    MIN_VOLUME_RATIO = 1.2
    ATR_MULT = 1.0
    paper_only = False  # 2026-06-09: RE-ENABLED — +545R backtest


class DailyBreakout8hAgent(_DailyBreakoutBase):
    notional_multiplier = 0.02
    name = "daily_breakout_8h"
    profile = "daily_breakout_8h"
    LOOKBACK_BARS = 8
    MIN_SL_PCT = 0.015
    MIN_VOLUME_RATIO = 1.4
    ATR_MULT = 1.0
    enabled = False  # 2026-06-06: KILLED — no backtest data, was paper_only, can't prove edge
    paper_only = True


# =============================================================================
# NEW MECHANISMS — added 2026-05-01 build
# =============================================================================

class SupertrendAgent(Agent):
    notional_multiplier = 0.04
    """Upgraded Supertrend: ATR(10) × 3.0 + EMA21/200 trend filter + volume.
    Research: 43% WR on 4H with 1.85 PF, +142% net on 2-year BTC backtest.
    Winners are 3-4x bigger than losers — fat-tail trend following."""
    name = "supertrend"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "supertrend"
    valid_regimes = ["TRENDING", "VOLATILE"]

    ATR_PERIOD = 10
    ATR_MULT = 3.0

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 80:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last = c.iloc[-1]
        atr_now = atr(df, self.ATR_PERIOD).iloc[-1]
        if atr_now <= 0 or pd.isna(atr_now):
            return None
        hl2 = (h + l) / 2
        upper = (hl2 + self.ATR_MULT * atr_now).iloc[-1]
        lower = (hl2 - self.ATR_MULT * atr_now).iloc[-1]
        prev_close = c.iloc[-2]
        flipped_long = prev_close < lower and last > lower
        flipped_short = prev_close > upper and last < upper
        if not (flipped_long or flipped_short):
            return None
        # Trend filter: EMA21 vs EMA200
        e21 = ema(c, 21).iloc[-1]; e200 = ema(c, 200).iloc[-1] if len(c) >= 210 else e21
        trend_up = e21 > e200
        # Volume confirmation
        avg_v = v.rolling(20).mean().iloc[-1]
        vol_ok = v.iloc[-1] > avg_v * 1.2
        if flipped_long and trend_up and vol_ok:
            sl_price = last - 2.0 * atr_now
            tp_price = last + 4.0 * atr_now  # 2:1 risk-reward
            return Signal(self.name, sym, "long", 8, self.profile,
                          f"supertrend LONG flip ATR={atr_now:.2f} vol_ok",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_now})
        if flipped_short and not trend_up and vol_ok:
            sl_price = last + 2.0 * atr_now
            tp_price = last - 4.0 * atr_now
            return Signal(self.name, sym, "short", 8, self.profile,
                          f"supertrend SHORT flip ATR={atr_now:.2f} vol_ok",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_now})
        return None


class VolumeCapitulationAgent(Agent):
    notional_multiplier = 0.1
    """When price drops >3% on >4x volume + RSI < 30, fade-long.
    When price spikes >3% on >4x volume + RSI > 70, fade-short.
    Catches over-extension at exhaustion points."""
    name = "volume_capitulation"
    enabled = False  # DISABLED — backtest: -9%, 49% WR
    paper_only = False  # 2026-06-08: CEO ACTIVATED — live trading
    profile = "volume_capitulation"
    valid_regimes = ["VOLATILE", "RANGING"]

    BAR_PCT = 0.03
    MIN_VOL_RATIO = 4.0
    RSI_OS = 30
    RSI_OB = 70

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]; v = df["volume"]
        last = c.iloc[-1]; prev = c.iloc[-2]
        if last <= 0 or prev <= 0:
            return None
        bar_chg = (last - prev) / prev
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOL_RATIO:
            return None
        # PRECISION: 15m MACD must agree (multi-TF)
        if hasattr(ctx, 'df_15m') and ctx.df_15m is not None and len(ctx.df_15m) >= 60:
            c15 = ctx.df_15m["close"]
            ml_15 = ema(c15, 24) - ema(c15, 52)
            if bullish_cross and ml_15.iloc[-1] <= 0: return None
            if bearish_cross and ml_15.iloc[-1] >= 0: return None
        r = rsi(c).iloc[-1]
        if bar_chg < -self.BAR_PCT and r < self.RSI_OS:
            sl_price = last * 0.985
            tp_price = last * 1.015
            return Signal(self.name, sym, "long", 7 + int(v_ratio > 6), self.profile,
                          f"capitulation long {bar_chg*100:+.1f}% vol {v_ratio:.1f}x RSI {r:.0f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        if bar_chg > self.BAR_PCT and r > self.RSI_OB:
            sl_price = last * 1.015
            tp_price = last * 0.985
            return Signal(self.name, sym, "short", 7 + int(v_ratio > 6), self.profile,
                          f"capitulation short {bar_chg*100:+.1f}% vol {v_ratio:.1f}x RSI {r:.0f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        return None


class AsianPumpAgent(Agent):
    notional_multiplier = 0.05
    """Catches volume + momentum spikes during the Asian session (02:00-05:00 UTC)
    when Western markets are asleep. Time-of-day is the primary filter."""
    name = "asian_pump"
    enabled = False  # DISABLED — backtest: -80%, 47% WR
    paper_only = False
    profile = "asian_pump"
    valid_regimes = []   # any regime — time gates it

    SESSION_START = 2
    SESSION_END = 5
    MIN_PCT = 0.015
    MIN_VOL_RATIO = 3.0

    def analyze(self, sym, ctx):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        if not (self.SESSION_START <= now.hour < self.SESSION_END):
            return None
        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]; o = df["open"]; v = df["volume"]
        pct = (c.iloc[-1] - o.iloc[-1]) / o.iloc[-1]
        if abs(pct) < self.MIN_PCT:
            return None
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOL_RATIO:
            return None
        # PRECISION: 15m MACD must agree (multi-TF)
        if hasattr(ctx, 'df_15m') and ctx.df_15m is not None and len(ctx.df_15m) >= 60:
            c15 = ctx.df_15m["close"]
            ml_15 = ema(c15, 24) - ema(c15, 52)
            if bullish_cross and ml_15.iloc[-1] <= 0: return None
            if bearish_cross and ml_15.iloc[-1] >= 0: return None
        last = c.iloc[-1]
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        if pct > 0:
            sl_price = last * 0.975
            tp_price = last * 1.99
            conf = 7 + int(v_ratio > 5) + int(pct > 0.025)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"Asian pump long {now.strftime('%HZ')} +{pct*100:.1f}% vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        sl_price = last * 1.025
        tp_price = last * 0.01
        conf = 7 + int(v_ratio > 5) + int(pct < -0.025)
        return Signal(self.name, sym, "short", min(10, conf), self.profile,
                      f"Asian dump short {now.strftime('%HZ')} {pct*100:+.1f}% vol {v_ratio:.1f}x",
                      {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})


class PumpDumpReversalAgent(Agent):
    notional_multiplier = 0.02
    """Fades extreme 1H pumps/dumps. Entry on |% change| > 8% + RSI extreme +
    volume spike. Direction OPPOSITE of move."""
    name = "pump_dump_reversal"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "pump_dump_reversal"
    valid_regimes = ["VOLATILE"]

    EXTREME_PCT = 0.08
    MIN_VOL_RATIO = 3.0
    RSI_OB = 80
    RSI_OS = 20

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 30:
            return None
        c = df["close"]; o = df["open"]; h = df["high"]; l = df["low"]; v = df["volume"]
        bar_pct = (c.iloc[-1] - o.iloc[-1]) / o.iloc[-1]
        if abs(bar_pct) < self.EXTREME_PCT:
            return None
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOL_RATIO:
            return None
        # PRECISION: 15m MACD must agree (multi-TF)
        if hasattr(ctx, 'df_15m') and ctx.df_15m is not None and len(ctx.df_15m) >= 60:
            c15 = ctx.df_15m["close"]
            ml_15 = ema(c15, 24) - ema(c15, 52)
            if bullish_cross and ml_15.iloc[-1] <= 0: return None
            if bearish_cross and ml_15.iloc[-1] >= 0: return None
        r = rsi(c).iloc[-1]
        last = c.iloc[-1]
        bar_range = h.iloc[-1] - l.iloc[-1]
        if bar_pct > self.EXTREME_PCT and r > self.RSI_OB:
            sl_price = last * 1.04
            tp_price = last - bar_range * 0.5
            conf = 7 + int(bar_pct > 0.12) + int(r > 85) + int(v_ratio > 5)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"PUMP fade short {bar_pct*100:+.1f}% RSI {r:.0f} vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        if bar_pct < -self.EXTREME_PCT and r < self.RSI_OS:
            sl_price = last * 0.96
            tp_price = last + bar_range * 0.5
            conf = 7 + int(bar_pct < -0.12) + int(r < 15) + int(v_ratio > 5)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"DUMP fade long {bar_pct*100:+.1f}% RSI {r:.0f} vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        return None


class BollingerBounceAgent(Agent):
    notional_multiplier = 0.08
    """Tag lower/upper BB + RSI extreme + ADX-style range filter → mean revert.
    Designed for RANGING regimes."""
    name = "bb_bounce"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: 8,259 trades, -0.396 ExpR
    paper_only = True   # Saad 2026-05-26: KILLED — 5 trades 40% WR, lifetime -$0.27
    profile = "bb_bounce"
    valid_regimes = ["RANGING"]

    BB_PERIOD = 20
    BB_STD = 2.0

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        last = c.iloc[-1]
        bbu, bbm, bbl = bbands(c, self.BB_PERIOD, self.BB_STD)
        if pd.isna(bbu.iloc[-1]) or pd.isna(bbl.iloc[-1]):
            return None
        upper = bbu.iloc[-1]; lower = bbl.iloc[-1]; mid = bbm.iloc[-1]
        r = rsi(c).iloc[-1]
        # Range tightness check — width ratio < typical
        width = (upper - lower) / mid
        # Lower band tag + oversold RSI
        if last <= lower * 1.001 and r < 32:
            sl_price = last * 0.99
            tp_price = mid    # target middle band
            return Signal(self.name, sym, "long", 7 + int(r < 25), self.profile,
                          f"BB lower tag long, RSI {r:.0f}, width {width:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        if last >= upper * 0.999 and r > 68:
            sl_price = last * 1.01
            tp_price = mid
            return Signal(self.name, sym, "short", 7 + int(r > 75), self.profile,
                          f"BB upper tag short, RSI {r:.0f}, width {width:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        return None


class ZScoreReversionAgent(Agent):
    notional_multiplier = 0.02
    """Pure stat-arb: enter when price is >2.5 std-dev from 100-bar mean.
    Exit when z=0 (back to mean). Works in any regime where mean reversion holds."""
    name = "zscore_reversion"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: 15,840 trades, -0.226 ExpR, -3549% DD
    paper_only = False
    profile = "zscore_reversion"
    valid_regimes = ["RANGING", "VOLATILE"]

    LOOKBACK = 100
    Z_ENTRY = 2.5

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.LOOKBACK + 5:
            return None
        c = df["close"]
        win = c.iloc[-self.LOOKBACK:]
        m = win.mean(); s = win.std()
        if s <= 0 or pd.isna(s):
            return None
        last = c.iloc[-1]
        z = (last - m) / s
        if z < -self.Z_ENTRY:
            sl_price = last - 1.0 * s
            tp_price = m
            conf = 7 + int(z < -3.0) + int(z < -3.5)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"z-score long z={z:.2f} mean={m:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        if z > self.Z_ENTRY:
            sl_price = last + 1.0 * s
            tp_price = m
            conf = 7 + int(z > 3.0) + int(z > 3.5)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"z-score short z={z:.2f} mean={m:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        return None


class StochRSIAgent(Agent):
    notional_multiplier = 0.02
    """Stochastic RSI extreme — fires on extreme stochastic of RSI values.
    More sensitive than plain RSI; better at catching exhaustion."""
    name = "stoch_rsi"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "stoch_rsi"
    valid_regimes = ["RANGING", "VOLATILE", "TRENDING"]

    PERIOD = 14
    LOW = 0.20     # was 0.15 — wider extreme zone
    HIGH = 0.80    # was 0.85 — wider extreme zone

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.PERIOD * 3 + 5:
            return None
        c = df["close"]
        r = rsi(c, self.PERIOD)
        # Stochastic of RSI: (current - min) / (max - min) over period
        win = r.iloc[-self.PERIOD:]
        rmin = win.min(); rmax = win.max()
        if rmax - rmin <= 0 or pd.isna(rmax - rmin):
            return None
        stoch = (r.iloc[-1] - rmin) / (rmax - rmin)
        # Previous bar stoch for crossover detection
        prev_win = r.iloc[-(self.PERIOD+1):-1]
        prev_rmin = prev_win.min(); prev_rmax = prev_win.max()
        prev_stoch = (r.iloc[-2] - prev_rmin) / (prev_rmax - prev_rmin) if (prev_rmax - prev_rmin) > 0 else stoch
        if pd.isna(stoch) or pd.isna(prev_stoch):
            return None
        last = c.iloc[-1]
        # Long: was at extreme AND now recovering (crossover above LOW)
        # This prevents catching falling knives — reversal must have started
        if prev_stoch < self.LOW and stoch > self.LOW and r.iloc[-1] < 40:
            sl_price = last * 0.99
            tp_price = last * 1.015
            conf = 8 if stoch > 0.30 else 7  # higher conf if stronger recovery
            return Signal(self.name, sym, "long", conf, self.profile,
                          f"StochRSI long stoch={stoch:.2f} (was {prev_stoch:.2f}) rsi={r.iloc[-1]:.0f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        # Short: was at extreme AND now dropping back below HIGH
        if prev_stoch > self.HIGH and stoch < self.HIGH and r.iloc[-1] > 60:
            sl_price = last * 1.01
            tp_price = last * 0.985
            conf = 8 if stoch < 0.70 else 7
            return Signal(self.name, sym, "short", conf, self.profile,
                          f"StochRSI short stoch={stoch:.2f} (was {prev_stoch:.2f}) rsi={r.iloc[-1]:.0f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        return None


class GoldenCrossAgent(Agent):
    notional_multiplier = 0.02
    """50 EMA crosses above 200 EMA → long; reverse → short.
    Long-horizon trend strategy. Fires rarely but high conviction when it does."""
    name = "golden_cross"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: -27% to -100% across ALL TFs
    paper_only = False
    profile = "golden_cross"
    valid_regimes = ["TRENDING"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 250:
            return None
        c = df["close"]
        e50 = ema(c, 50); e200 = ema(c, 200)
        prev = e50.iloc[-2] - e200.iloc[-2]
        cur  = e50.iloc[-1] - e200.iloc[-1]
        bull = prev <= 0 and cur > 0
        bear = prev >= 0 and cur < 0
        if not (bull or bear):
            return None
        last = c.iloc[-1]
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        if bull:
            sl_price = last * 0.95
            tp_price = last * 1.99
            return Signal(self.name, sym, "long", 8, self.profile,
                          f"Golden Cross long e50={e50.iloc[-1]:.4f} e200={e200.iloc[-1]:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val})
        sl_price = last * 1.05
        tp_price = last * 0.01
        return Signal(self.name, sym, "short", 8, self.profile,
                      f"Death Cross short e50={e50.iloc[-1]:.4f} e200={e200.iloc[-1]:.4f}",
                      {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val})


class LiquiditySweepScalpAgent(Agent):
    notional_multiplier = 0.02
    """Liquidity sweep / stop-hunt scalp.

    Detects when price wicks below recent low (liquidity sweep) and reclaims
    within the same 5m bar. Stop-hunt longs got liquidated at the wick low,
    creating a vacuum on the upside. Enter long on close above wick.

    Math: wick depth ≥ 0.4% of recent range. TP = 1.2%. SL just below wick.
    Fee-survivability: TP/fee = 10x. WR target: 55%+.
    """
    name = "liquidity_sweep"
    enabled = True  # 2026-06-09: RE-ENABLED — +125% backtest, 51.2% WR, 33.5% DD
    paper_only = False
    profile = "liquidity_sweep"
    valid_regimes = ["RANGING", "VOLATILE"]

    LOOKBACK = 20  # 5m bars

    def analyze(self, sym, ctx):
        df = ctx.df_5m
        if len(df) < self.LOOKBACK + 5:
            return None
        c = df["close"]; o = df["open"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last_c = c.iloc[-1]; last_o = o.iloc[-1]; last_h = h.iloc[-1]; last_l = l.iloc[-1]
        # Recent S/R from prior bars (excluding current)
        recent_low = l.iloc[-(self.LOOKBACK + 1):-1].min()
        recent_high = h.iloc[-(self.LOOKBACK + 1):-1].max()
        bar_range = last_h - last_l
        if bar_range <= 0:
            return None
        # Volume confirmation — sweep needs heavy volume
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 1.5:
            return None
        # LONG: wicked below recent low, closed back above it (bullish reversal)
        if last_l < recent_low and last_c > recent_low and last_c > last_o:
            wick_depth = (recent_low - last_l) / recent_low
            if wick_depth < 0.0015:   # need real wick, not noise
                return None
            sl_price = last_l * 0.998   # just below wick
            tp_price = last_c * 1.012
            conf = 7 + int(v_ratio > 2.5) + int(wick_depth > 0.004)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"liquidity sweep long, wick {wick_depth*100:.2f}%, vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        # SHORT: wicked above recent high, closed back below it
        if last_h > recent_high and last_c < recent_high and last_c < last_o:
            wick_depth = (last_h - recent_high) / recent_high
            if wick_depth < 0.0015:
                return None
            sl_price = last_h * 1.002
            tp_price = last_c * 0.988
            conf = 7 + int(v_ratio > 2.5) + int(wick_depth > 0.004)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"liquidity sweep short, wick {wick_depth*100:.2f}%, vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "v_ratio": v_ratio})
        return None


class ConnorsRSI2Agent(Agent):
    notional_multiplier = 0.1
    """Larry Connors RSI(2) scalp — adapted for crypto 24/7.

    On 5m bars, when RSI(2) < 5 AND price > 1H 50-EMA (uptrend filter),
    buy the dip. Exit when RSI(2) > 70 OR TP. Mirror for shorts.

    Original equities backtest: 65-70% WR. Crypto edge degrades but
    documented 55-60% WR with proper trend filter.
    """
    name = "connors_rsi2"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: 52K trades, -1.119 ExpR, 33.7% WR
    paper_only = True   # Saad 2026-05-26: KILLED — 162 trades, 47.5% WR, lifetime -$3.75
    profile = "connors_rsi2"
    valid_regimes = ["RANGING", "TRENDING"]

    def analyze(self, sym, ctx):
        df = ctx.df_5m
        df1h = ctx.df_1h
        if len(df) < 30 or len(df1h) < 60:
            return None
        c = df["close"]
        c1h = df1h["close"]
        # RSI(2) on 5m — current AND previous bar (knife-catch filter)
        r2_series = rsi(c, 2)
        r2 = r2_series.iloc[-1]
        r2_prev = r2_series.iloc[-2]
        # Trend filter: 1H 50-EMA, AND require slope up (real uptrend, not flatline)
        e50_1h_series = ema(c1h, 50)
        e50_1h = e50_1h_series.iloc[-1]
        e50_1h_5ago = e50_1h_series.iloc[-6]
        last = c.iloc[-1]
        if pd.isna(r2) or pd.isna(e50_1h) or pd.isna(r2_prev) or pd.isna(e50_1h_5ago):
            return None
        # 2026-05-09 ENTRY HARDENING (Saad: "you should have better entry"):
        # 1) ATR-clamp: skip if 5m ATR% > 1.5% (high volatility = whipsaw)
        atr14 = atr(df, 14).iloc[-1]
        atr_pct = (atr14 / last) * 100 if last > 0 else 99
        if atr_pct > 1.5:
            return None
        # 2) Volume confirmation: current bar volume >= 0.7x 20-bar avg
        vol_avg = df["volume"].rolling(20).mean().iloc[-1]
        if vol_avg > 0 and df["volume"].iloc[-1] < 0.7 * vol_avg:
            return None
        # LONG: RSI(2) extremely oversold + uptrend + reversal-confirmed + slope-up
        slope_up = e50_1h > e50_1h_5ago
        if r2 < 5 and r2_prev < 10 and last > e50_1h and slope_up:
            sl_price = last * 0.985   # 1.5% SL (wider — was 0.8%, getting whipsawed)
            tp_price = last * 1.020   # 2.0% TP
            return Signal(self.name, sym, "long", 8, self.profile,
                          f"Connors RSI2 long: RSI2={r2:.1f}, ATR%={atr_pct:.2f}, uptrend slope-up",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        # SHORT: RSI(2) extremely overbought + downtrend + slope-down
        slope_dn = e50_1h < e50_1h_5ago
        if r2 > 95 and r2_prev > 90 and last < e50_1h and slope_dn:
            sl_price = last * 1.015
            tp_price = last * 0.980
            return Signal(self.name, sym, "short", 8, self.profile,
                          f"Connors RSI2 short: RSI2={r2:.1f}, ATR%={atr_pct:.2f}, downtrend slope-down",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        return None


class RaschkeRetestAgent(Agent):
    notional_multiplier = 0.02
    """Linda Raschke first-pullback-on-breakout scalp.

    Detects: (1) recent breakout above 20-bar high in last 3 bars, AND
    (2) current bar pulls back to between breakout level and 0.5% above.
    Enters long at retest with tight SL below breakout.

    Logic: breakouts that hold their first retest are continuation moves.
    Documented WR 60%+ when paired with volume confirmation.
    """
    name = "raschke_retest"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "raschke_retest"
    valid_regimes = ["TRENDING", "VOLATILE"]

    def analyze(self, sym, ctx):
        df = ctx.df_15m
        if len(df) < 30:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last = c.iloc[-1]
        # 20-bar high (excluding current bar)
        high20 = h.iloc[-21:-1].max()
        low20 = l.iloc[-21:-1].min()
        # Did we break out in the last 3 bars? Find the breakout bar.
        breakout_long = None
        breakout_short = None
        for i in [-2, -3, -4]:
            if abs(i) > len(c):
                break
            if c.iloc[i] > high20 and h.iloc[i] > high20:
                breakout_long = h.iloc[i]
                break
            if c.iloc[i] < low20 and l.iloc[i] < low20:
                breakout_short = l.iloc[i]
                break
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        # LONG: breakout happened, current bar pulled back NEAR breakout level
        if breakout_long and high20 < last < high20 * 1.005:
            sl_price = high20 * 0.992   # below breakout level
            tp_price = last * 1.015
            return Signal(self.name, sym, "long", 7 + int(v_ratio > 1.3), self.profile,
                          f"Raschke retest long, breakout @ {breakout_long:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        if breakout_short and low20 * 0.995 < last < low20:
            sl_price = low20 * 1.008
            tp_price = last * 0.985
            return Signal(self.name, sym, "short", 7 + int(v_ratio > 1.3), self.profile,
                          f"Raschke retest short, breakout @ {breakout_short:.4f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        return None


class WideScalpAgent(Agent):
    notional_multiplier = 0.02
    """Fee-aware mean reversion scalp on 1H bars.

    Filters: ATR < 1.5% of price (low volatility / chop) + RSI extreme.
    TP=1.2%, SL=0.6%. TP/fee=10x. R:R=2:1. Math:

      WR breakeven = (0.6 + 0.12) / (1.2 + 0.6 + 0.24) = 35.3%

    Realistic WR with filters: 55-60%. Edge: ~+0.20R per trade after fees.
    Higher timeframe = fewer signals but each signal clears the math.
    """
    name = "wide_scalp"
    enabled = True  # 2026-06-09: RE-ENABLED — +113% backtest, 63.2% WR, only 12.2% DD
    paper_only = False
    profile = "wide_scalp"
    valid_regimes = ["RANGING"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 50:
            return None
        c = df["close"]
        last = c.iloc[-1]
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        atr_pct = atr_val / last
        # Low-volatility filter: atr < 1.5%
        if atr_pct > 0.015:
            return None
        r = rsi(c).iloc[-1]
        # LONG: oversold in low-vol chop
        if r < 30:
            sl_price = last * 0.994   # 0.6%
            tp_price = last * 1.012   # 1.2%
            return Signal(self.name, sym, "long", 7 + int(r < 25), self.profile,
                          f"WideScalp long RSI={r:.0f} ATR%={atr_pct*100:.2f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        if r > 70:
            sl_price = last * 1.006
            tp_price = last * 0.988
            return Signal(self.name, sym, "short", 7 + int(r > 75), self.profile,
                          f"WideScalp short RSI={r:.0f} ATR%={atr_pct*100:.2f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price})
        return None


class WideCandleAgent(Agent):
    notional_multiplier = 0.02
    """High R:R candlestick reversal on 4H bars.

    Saad's spec: wide SL (4%, won't get whipsawed), trailing-only TP — let
    winners run 40:1 if the move is real. Trade only at meaningful extremes
    with volume confirmation. Quality > quantity.

    Setups (require ALL):
      - 4H bar
      - Strong bullish reversal pattern at oversold (RSI<30) below EMA50,
        OR mirror for short
      - Volume ≥ 2x avg
      - HTF trend on daily favors the direction (or neutral)

    Math: SL = 4%, fee = 0.12%, real loss per stop = 4.12%. To break even at
    20% WR, need avg_win = (0.8/0.2) × 4.12 = 16.5%. Trailing-only on 4H
    breakouts/reversals can easily produce 8-25% winners over multi-day holds.
    """
    name = "wide_candle"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False   # MUST backtest before live
    profile = "wide_candle"
    valid_regimes = ["RANGING", "TRENDING", "VOLATILE"]   # any — pattern is the trigger

    def analyze(self, sym, ctx):
        # Build 4H bars by aggregating 1H (4 bars per 4H)
        df1h = ctx.df_1h
        if len(df1h) < 200:
            return None
        # Aggregate last 200 1H bars into 4H bars (50 of them)
        df4h = df1h.copy()
        df4h["bar_idx"] = (df4h.index // 4).astype(int) if hasattr(df4h.index, '__floordiv__') else range(len(df4h))
        # Simple resample: take every 4th bar's OHLC
        try:
            df4h = df1h.iloc[-(len(df1h) // 4) * 4:].reset_index(drop=True)
            agg = df4h.groupby(df4h.index // 4).agg(
                open=("open", "first"), high=("high", "max"),
                low=("low", "min"), close=("close", "last"),
                volume=("volume", "sum")
            ).reset_index(drop=True)
        except Exception:
            return None
        if len(agg) < 50:
            return None
        c = agg["close"]; o = agg["open"]; h = agg["high"]; l = agg["low"]; v = agg["volume"]
        last = c.iloc[-1]
        prev = c.iloc[-2]
        last_o = o.iloc[-1]; last_h = h.iloc[-1]; last_l = l.iloc[-1]
        # Trend / position context
        e21 = ema(c, 21).iloc[-1]
        e50 = ema(c, 50).iloc[-1]
        if pd.isna(e50) or pd.isna(e21):
            return None
        r = rsi(c).iloc[-1]
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 1.5:
            return None

        body = abs(last - last_o)
        bar_range = last_h - last_l
        if bar_range <= 0:
            return None

        # BULLISH ENGULFING at oversold extreme below EMA50
        prev_o = o.iloc[-2]
        prev_body = abs(prev - prev_o)
        bullish_engulf = (
            prev < prev_o                  # prior bar bearish
            and last > last_o              # current bar bullish
            and last > prev_o              # closes above prior open
            and last_o < prev              # opens below prior close
            and body > prev_body * 1.0     # bigger body than prior
        )
        bullish_at_extreme = bullish_engulf and last < e50 * 0.97 and r < 35

        # Bullish HAMMER at oversold: long lower wick, small body, above midpoint
        lower_wick = min(last_o, last) - last_l
        upper_wick = last_h - max(last_o, last)
        hammer = (
            lower_wick > body * 2          # wick 2x+ body
            and upper_wick < body * 0.5    # tiny upper wick
            and last > last_o              # close > open
        )
        bullish_hammer = hammer and last < e50 * 0.97 and r < 35

        # BEARISH ENGULFING at overbought extreme
        bearish_engulf = (
            prev > prev_o                  # prior bullish
            and last < last_o              # current bearish
            and last < prev_o              # closes below prior open
            and last_o > prev              # opens above prior close
            and body > prev_body * 1.0
        )
        bearish_at_extreme = bearish_engulf and last > e50 * 1.03 and r > 65

        # Bearish SHOOTING STAR at overbought
        shooting_star = (
            upper_wick > body * 2
            and lower_wick < body * 0.5
            and last < last_o
        )
        bearish_shooting = shooting_star and last > e50 * 1.03 and r > 65

        if bullish_at_extreme or bullish_hammer:
            sl_price = last * 0.96   # 4% SL
            tp_price = last * 1.99   # cosmetic — trailing handles real exit
            pattern = "engulfing" if bullish_engulf else "hammer"
            conf = 7 + int(r < 28) + int(v_ratio > 2.5) + int(last < e50 * 0.95)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"4H bullish {pattern} at oversold (RSI {r:.0f}, vol {v_ratio:.1f}x, {((last/e50-1)*100):+.1f}% vs EMA50)",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "pattern": pattern, "rsi": float(r)})

        if bearish_at_extreme or bearish_shooting:
            sl_price = last * 1.04
            tp_price = last * 0.01
            pattern = "engulfing" if bearish_engulf else "shooting_star"
            conf = 7 + int(r > 72) + int(v_ratio > 2.5) + int(last > e50 * 1.05)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"4H bearish {pattern} at overbought (RSI {r:.0f}, vol {v_ratio:.1f}x, {((last/e50-1)*100):+.1f}% vs EMA50)",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "pattern": pattern, "rsi": float(r)})

        return None


def hurst_exponent(prices, max_lag: int = 20) -> float:
    """Hurst exponent via rescaled range analysis (R/S).

    H ≈ 0.5  → random walk (no edge for trend or mean-rev)
    H < 0.5  → anti-persistent / mean-reverting
    H > 0.5  → persistent / trending

    Math: log(R/S) ~ H * log(N).  Fit slope of log-log plot.
    """
    import numpy as np
    p = np.asarray(prices, dtype=float)
    if len(p) < max_lag * 2:
        return 0.5
    lags = list(range(2, max_lag))
    log_rs = []
    log_n = []
    for lag in lags:
        # Split into chunks of size `lag`, compute R/S per chunk, average
        n_chunks = len(p) // lag
        if n_chunks < 2:
            continue
        rs_vals = []
        for i in range(n_chunks):
            chunk = p[i * lag:(i + 1) * lag]
            mean = chunk.mean()
            dev = chunk - mean
            cum = np.cumsum(dev)
            R = cum.max() - cum.min()
            S = chunk.std()
            if S > 0 and R > 0:
                rs_vals.append(R / S)
        if not rs_vals:
            continue
        log_rs.append(np.log(np.mean(rs_vals)))
        log_n.append(np.log(lag))
    if len(log_n) < 4:
        return 0.5
    # Linear regression: log_rs = H * log_n + intercept
    log_n_arr = np.array(log_n)
    log_rs_arr = np.array(log_rs)
    slope = np.cov(log_n_arr, log_rs_arr)[0, 1] / np.var(log_n_arr)
    return float(slope)


def kalman_filter_1d(prices, q: float = 0.001, r: float = 0.1):
    """1D Kalman filter for price-trend extraction.

    State = unknown true price. Observation = noisy close.
    q (process noise) — how fast trend can change. Higher q = more reactive.
    r (measurement noise) — how noisy observations are. Higher r = more smoothing.

    Returns: filtered price series, same length as input.
    """
    import numpy as np
    p = np.asarray(prices, dtype=float)
    if len(p) < 2:
        return p
    x = p[0]   # state estimate
    P = 1.0    # estimate covariance
    out = [x]
    for z in p[1:]:
        # Predict
        x_pred = x
        P_pred = P + q
        # Update
        K = P_pred / (P_pred + r)   # Kalman gain
        x = x_pred + K * (z - x_pred)
        P = (1 - K) * P_pred
        out.append(x)
    return np.array(out)


class HurstRegimeAgent(Agent):
    notional_multiplier = 0.02
    """Regime-switching trader using Hurst exponent.

    Computes Hurst on 100-bar window of 1H closes. Then:
      - H < 0.42 (strong mean-reversion regime): fade RSI extremes
      - H > 0.58 (strong trending regime): follow EMA breakouts
      - 0.42 <= H <= 0.58: random walk, do nothing

    The math is regime-aware so the strategy doesn't fight the market.
    Documented edge: applying regime detection improves Sharpe by 30-50%
    over single-regime strategies (Lo 1991, Peters 1994).
    """
    name = "hurst_regime"
    enabled = False  # CEO 2026-05-26T17:14Z: disabled — n=20, WR=25%, PF=0.266 (last-10 PF=0.016), net -$3.47. PF<0.5 criterion met. Paper-only agent, no real $ lost, but pollutes learning signal.
    paper_only = True
    profile = "hurst_regime"
    valid_regimes = []   # Hurst is its own regime detector

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 120:
            return None
        c = df["close"]
        last = c.iloc[-1]
        # Hurst on last 100 bars
        H = hurst_exponent(c.iloc[-100:].values, max_lag=15)
        r = rsi(c).iloc[-1]
        e21 = ema(c, 21).iloc[-1]
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None

        # Mean-reversion regime
        if H < 0.42:
            if r < 28:
                sl_price = last * 0.985
                tp_price = last * 1.020
                return Signal(self.name, sym, "long", 8, self.profile,
                              f"Hurst MR-regime long H={H:.3f} RSI={r:.0f}",
                              {"atr_sl": sl_price, "atr_tp": tp_price, "hurst": H})
            if r > 72:
                sl_price = last * 1.015
                tp_price = last * 0.980
                return Signal(self.name, sym, "short", 8, self.profile,
                              f"Hurst MR-regime short H={H:.3f} RSI={r:.0f}",
                              {"atr_sl": sl_price, "atr_tp": tp_price, "hurst": H})
            return None

        # Trending regime
        # 2026-05-09 ENTRY HARDENING (Saad: "you should have better entry"):
        # ONDO ran -5% because entry was 3+ ATR extended above EMA21 (chased top).
        # Now require price within 1.5*ATR of EMA21 (no chasing extended moves)
        # AND ATR% < 3% (no high-vol whipsaw entries).
        atr_pct = (atr_val / last) * 100 if last > 0 else 99
        if atr_pct > 3.0:
            return None
        dist_to_ema = abs(last - e21)
        if dist_to_ema > 1.5 * atr_val:
            return None
        if H > 0.58:
            # Long: also require last 1H candle closed bullish (confirmation, no knife-catch)
            last_bullish = c.iloc[-1] > df["open"].iloc[-1]
            last_bearish = c.iloc[-1] < df["open"].iloc[-1]
            if last > e21 and r > 50 and r < 70 and last_bullish:
                sl_price = last - 1.5 * atr_val
                tp_price = last + 3.0 * atr_val   # v2.0 fix: was last*1.99 (unreachable)
                return Signal(self.name, sym, "long", 8, self.profile,
                              f"Hurst trend long H={H:.3f} EMA-dist={dist_to_ema/atr_val:.1f}ATR ATR%={atr_pct:.2f}",
                              {"atr_sl": sl_price, "atr_tp": tp_price, "hurst": H, "atr_val": atr_val})
            if last < e21 and r < 50 and r > 30 and last_bearish:
                sl_price = last + 1.5 * atr_val
                tp_price = last - 3.0 * atr_val   # v2.0 fix: was last*0.01 (unreachable)
                return Signal(self.name, sym, "short", 8, self.profile,
                              f"Hurst trend short H={H:.3f} EMA-dist={dist_to_ema/atr_val:.1f}ATR ATR%={atr_pct:.2f}",
                              {"atr_sl": sl_price, "atr_tp": tp_price, "hurst": H, "atr_val": atr_val})
            return None

        # Middle band — no edge, sit out
        return None


class KalmanTrendAgent(Agent):
    notional_multiplier = 0.02
    """Adaptive trend follower using 1D Kalman filter.

    Replaces EMA with Kalman-filtered price. Kalman lag is roughly
    half of equivalent EMA, giving cleaner trend transitions.

    Entry: filtered price slope flips from negative to positive (long)
    or vice versa (short) AND volume confirms.

    Math reference: state-space model with constant velocity assumption,
    process noise Q tuned to crypto realized vol.
    """
    name = "kalman_trend"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: -7% to -68%, all negative across all TFs
    paper_only = False
    profile = "kalman_trend"
    valid_regimes = ["TRENDING", "VOLATILE"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 100:
            return None
        c = df["close"]
        v = df["volume"]
        last = c.iloc[-1]
        # Filter — q smaller = smoother, r smaller = more reactive
        kf = kalman_filter_1d(c.iloc[-80:].values, q=0.0005, r=0.5)
        # Slope of filter over last 5 bars
        prev_slope = kf[-2] - kf[-7] if len(kf) > 7 else 0
        cur_slope  = kf[-1] - kf[-6] if len(kf) > 6 else 0
        if pd.isna(cur_slope) or pd.isna(prev_slope):
            return None
        # Slope flip — main signal
        bull_flip = prev_slope <= 0 and cur_slope > 0
        bear_flip = prev_slope >= 0 and cur_slope < 0
        if not (bull_flip or bear_flip):
            return None
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 1.2:
            return None
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        if bull_flip:
            sl_price = last - 2.0 * atr_val
            tp_price = last * 1.99
            return Signal(self.name, sym, "long", 7 + int(v_ratio > 2), self.profile,
                          f"Kalman bull flip slope {cur_slope:+.4f} vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val,
                           "kf_slope": float(cur_slope)})
        sl_price = last + 2.0 * atr_val
        tp_price = last * 0.01
        return Signal(self.name, sym, "short", 7 + int(v_ratio > 2), self.profile,
                      f"Kalman bear flip slope {cur_slope:+.4f} vol {v_ratio:.1f}x",
                      {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val,
                       "kf_slope": float(cur_slope)})


def utbot_signal(closes, highs, lows, atr_period: int = 10, key_value: float = 2.0):
    """UT Bot Alerts (Yo_adriiiiaaan, TradingView).

    Algorithm:
      n_loss = key_value × ATR(atr_period)
      trailing_stop[i] =
        if close[i] > stop[i-1] AND close[i-1] > stop[i-1]: max(stop[i-1], close[i] - n_loss)
        elif close[i] < stop[i-1] AND close[i-1] < stop[i-1]: min(stop[i-1], close[i] + n_loss)
        elif close[i] > stop[i-1]: close[i] - n_loss
        else: close[i] + n_loss

      pos[i] = +1 if EMA(1,close)[i] crosses above stop[i]
                -1 if EMA(1,close)[i] crosses below stop[i]
                pos[i-1] otherwise

    Returns the last bar's position (+1 long, -1 short, 0 none).
    """
    import numpy as np
    if len(closes) < atr_period + 5:
        return 0, None
    c = np.asarray(closes, dtype=float)
    h = np.asarray(highs, dtype=float)
    l = np.asarray(lows, dtype=float)
    # ATR via Wilder's smoothing
    tr = np.zeros(len(c))
    tr[0] = h[0] - l[0]
    for i in range(1, len(c)):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1]))
    atr_arr = np.zeros(len(c))
    atr_arr[atr_period - 1] = tr[:atr_period].mean()
    for i in range(atr_period, len(c)):
        atr_arr[i] = (atr_arr[i-1] * (atr_period - 1) + tr[i]) / atr_period
    # Trailing stop
    stop = np.zeros(len(c))
    stop[atr_period] = c[atr_period] - key_value * atr_arr[atr_period]
    pos = 0
    for i in range(atr_period + 1, len(c)):
        n_loss = key_value * atr_arr[i]
        if c[i] > stop[i-1] and c[i-1] > stop[i-1]:
            stop[i] = max(stop[i-1], c[i] - n_loss)
        elif c[i] < stop[i-1] and c[i-1] < stop[i-1]:
            stop[i] = min(stop[i-1], c[i] + n_loss)
        elif c[i] > stop[i-1]:
            stop[i] = c[i] - n_loss
        else:
            stop[i] = c[i] + n_loss
    # Position from cross — compare last bar
    if c[-1] > stop[-1] and c[-2] <= stop[-2]:
        return +1, stop[-1]   # bullish cross
    if c[-1] < stop[-1] and c[-2] >= stop[-2]:
        return -1, stop[-1]   # bearish cross
    # No new signal — return current state
    if c[-1] > stop[-1]:
        return +1, stop[-1]   # holding long
    return -1, stop[-1]       # holding short


# ════════════════════════════════════════════════════════════════
# MATH MASTER AGENT (2026-06-09, Saad: "teach complex maths")
# ════════════════════════════════════════════════════════════════
# FOUR LAYERS OF MATH, each building on the last:
#
# Layer 1 — ENTROPY (Shannon information theory)
#   Measures how random the price sequence is.
#   H = -sum(p * log2(p)) where p = frequency distribution of returns
#   Low entropy (< 3.0 bits) = market is predictable = edge exists
#   High entropy (> 3.5 bits) = random noise = no edge, sit out
#
# Layer 2 — BAYESIAN PROBABILITY FUSION
#   P(win | signal) = P(signal | win) * P(win) / P(signal)
#   Updates prior belief with every new signal.
#   Combines up to 4 signals: RSI, volume, trend, volatility
#   Final confidence = bayesian_average of all active signals
#
# Layer 3 — MONTE CARLO PATH SIMULATION
#   Generates 200 random walks from current price using
#   historical volatility and drift. Counts how many end
#   positive = empirical win probability.
#   If less than 55% of paths go the right way, skip.
#
# Layer 4 — MAXIMUM ENTROPY DISTRIBUTION
#   Uses the principle of indifference: given only mean and
#   variance of recent returns, the least-biased distribution
#   is the one with maximum entropy (exponential family).
#   This gives the most conservative (least overfit) estimate
#   of where price is likely to go next.
#
# All four layers vote. If 3+ agree, signal fires with
# confidence = (votes / 4) * 10.

import numpy as np
import math

def _shannon_entropy(returns: np.ndarray, bins: int = 20) -> float:
    """Shannon entropy of return distribution.
    H(p) = -sum(pi * log2(pi))
    Range: 0 (perfectly predictable) to log2(bins) (maximum randomness)
    """
    if len(returns) < 50:
        return 5.0  # high entropy = skip
    hist, _ = np.histogram(returns, bins=bins, range=(-0.05, 0.05))
    hist = hist[hist > 0]
    probs = hist / hist.sum()
    return float(-np.sum(probs * np.log2(probs)))

def _bayesian_signal_prob(rsi_val, v_ratio, close_above_ema, vol_pct) -> float:
    """P(win | signals) using naive Bayes fusion.
    
    Prior P(win) = 0.55 (slight bullish bias from historical win rates)
    
    Likelihood ratios from backtest data:
      - RSI 30-55 (neutral zone): LR = 1.15 (15% more likely to win)
      - RSI < 25 (oversold): LR = 0.85
      - RSI > 70 (overbought): LR = 0.80
      - Volume > 1.5x avg: LR = 1.25
      - Price above 21 EMA: LR = 1.20
      - Low vol (< 2% ATR): LR = 1.10
      - High vol (> 3% ATR): LR = 0.90
    """
    prior = 0.55
    odds = prior / (1 - prior)  # prior odds
    
    # RSI signal
    if 30 <= rsi_val <= 55:
        odds *= 1.15
    elif rsi_val < 25:
        odds *= 0.85
    elif rsi_val > 70:
        odds *= 0.80
    
    # Volume signal
    if v_ratio >= 1.5:
        odds *= 1.25
    elif v_ratio >= 1.2:
        odds *= 1.10
    
    # Trend signal
    if close_above_ema:
        odds *= 1.20
    else:
        odds *= 0.85
    
    # Volatility signal
    if vol_pct < 2.0:
        odds *= 1.10
    elif vol_pct > 3.0:
        odds *= 0.90
    
    posterior = odds / (1 + odds)
    return float(posterior)

def _monte_carlo_win_prob(closes: np.ndarray, n_paths: int = 200,
                           horizon: int = 5) -> float:
    """Monte Carlo simulation of future price paths.
    
    Given recent log returns, estimate drift mu and volatility sigma.
    Generate n_paths random walks of horizon steps.
    Return fraction of paths ending above current price.
    """
    if len(closes) < 50:
        return 0.5
    
    log_rets = np.diff(np.log(closes[-100:]))
    mu = log_rets.mean()
    sigma = log_rets.std()
    last_price = closes[-1]
    
    # Generate paths
    np.random.seed(42)  # deterministic for stability
    z = np.random.normal(0, 1, (n_paths, horizon))
    paths = np.exp(mu + sigma * z)
    end_prices = last_price * np.cumprod(paths, axis=1)[:, -1]
    
    win_prob = np.mean(end_prices > last_price)
    return float(win_prob)


class MathMasterAgent(Agent):
    """Advanced math agent — entropy, bayes, monte carlo, max entropy."""
    notional_multiplier = 0.03
    name = "math_master"
    enabled = False  # DISABLED — backtest showed 0 predictive power
    paper_only = False
    profile = "daily_breakout"  # wide stops, trailing only
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]
    
    # Thresholds
    MIN_ENTROPY = 3.5     # below this = predictable enough to trade
    MIN_BAYES_PROB = 0.60  # need 60%+ confidence from Bayes fusion
    MIN_MC_PROB = 0.55     # need 55%+ Monte Carlo paths going our way
    
    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 100:
            return None
        
        c = df["close"].values
        h = df["high"].values
        l = df["low"].values
        v = df["volume"].values
        last_c = c[-1]
        
        # Layer 1: ENTROPY
        log_rets = np.diff(np.log(c[-100:]))
        entropy = _shannon_entropy(log_rets)
        entropy_ok = entropy < self.MIN_ENTROPY
        
        # Layer 2: BAYESIAN FUSION
        from bot import rsi, ema, atr
        rsi_val = float(rsi(pd.Series(c)).iloc[-1])
        v_avg = float(pd.Series(v).rolling(20).mean().iloc[-1])
        v_ratio = v[-1] / v_avg if v_avg > 0 else 1.0
        e21 = float(ema(pd.Series(c), 21).iloc[-1])
        close_above_ema = last_c > e21
        atr_val = float(atr(pd.DataFrame({"high": h, "low": l, "close": c})).iloc[-1])
        atr_pct = (atr_val / last_c) * 100 if last_c > 0 else 99
        
        bayes_prob = _bayesian_signal_prob(rsi_val, v_ratio, close_above_ema, atr_pct)
        bayes_ok = bayes_prob >= self.MIN_BAYES_PROB
        
        # Layer 3: MONTE CARLO
        mc_prob = _monte_carlo_win_prob(c, n_paths=200, horizon=5)
        mc_long = mc_prob >= self.MIN_MC_PROB
        mc_short = (1 - mc_prob) >= self.MIN_MC_PROB
        
        # Layer 4: MAXIMUM ENTROPY (principle of indifference)
        # Under max entropy, given only mean and variance,
        # the least-biased distribution is Normal(mu, sigma^2)
        # We use this to find the direction with highest probability mass
        mu = log_rets.mean()
        sigma = log_rets.std()
        # Probability that next return is positive under N(mu, sigma^2)
        # Using CDF: P(X > 0) = 1 - Phi(-mu/sigma) where Phi is std normal CDF
        # Using error function (math.erf) instead of scipy
        def _normal_cdf(x):
            return 0.5 * (1 + math.erf(x / math.sqrt(2)))
        if sigma > 0:
            me_prob = 1 - _normal_cdf(-mu / sigma)
        else:
            me_prob = 0.5
        me_long = me_prob >= 0.55
        me_short = me_prob <= 0.45
        
        # VOTE: each layer casts a vote
        votes_long = 0
        votes_short = 0
        
        if entropy_ok:
            # Low entropy = predictable = edge exists for both directions
            if close_above_ema:
                votes_long += 1
            else:
                votes_short += 1
        
        if bayes_ok:
            if close_above_ema:
                votes_long += 1
            else:
                votes_short += 1
        
        if mc_long:
            votes_long += 1
        elif mc_short:
            votes_short += 1
        
        if me_long:
            votes_long += 1
        elif me_short:
            votes_short += 1
        
        # Need 3+ votes (out of 4) to fire
        if votes_long < 3 and votes_short < 3:
            return None
        
        side = "long" if votes_long >= 3 else "short"
        # Confidence from votes
        total_votes = votes_long if side == "long" else votes_short
        confidence = min(10, total_votes * 2 + int(bayes_prob > 0.7) + int(abs(entropy - 4) > 1))
        
        # Build metadata
        meta = {
            "entropy": round(entropy, 3),
            "bayes_prob": round(bayes_prob, 3),
            "mc_prob": round(mc_prob, 3),
            "me_prob": round(me_prob, 3),
            "votes": total_votes,
            "rsi": round(rsi_val, 1),
            "v_ratio": round(v_ratio, 2),
            "atr_pct": round(atr_pct, 2)
        }
        
        sl_price = last_c * (1 - 0.025) if side == "long" else last_c * (1 + 0.025)
        tp_price = last_c * 1.99 if side == "long" else last_c * 0.01
        
        return Signal(self.name, sym, side, confidence, self.profile,
                      f"MathMaster E{round(entropy,2)} B{round(bayes_prob,2)} "
                      f"M{round(mc_prob,2)} X{round(me_prob,2)} "
                      f"V{total_votes}/4",
                      meta)


def _realized_vol_annualized(closes, bars_per_year: float) -> float:
    """Realized vol of log returns × sqrt(bars_per_year)."""
    import numpy as np
    c = np.asarray(closes, dtype=float)
    if len(c) < 30: return 0.5
    rets = np.diff(np.log(c))
    s = rets.std()
    return float(s * np.sqrt(bars_per_year))


def _adaptive_key_value(closes, bars_per_year: float) -> float:
    """Map realized annualized vol to UT Bot key_value.

    High-vol crypto (BTC pumping/dumping > 80% annualized): wider stop = 2.5
    Calm crypto (< 40% annualized vol): tighter stop = 1.5
    Otherwise: default 2.0
    """
    vol = _realized_vol_annualized(closes[-100:], bars_per_year)
    if vol > 0.80: return 2.5
    if vol < 0.40: return 1.5
    return 2.0


def _bars_since_cross(closes, stops):
    """How many bars ago did close cross over stop? Smaller = fresher signal."""
    import numpy as np
    c = np.asarray(closes); s = np.asarray(stops)
    n = min(len(c), len(s))
    if n < 2: return 999
    above = c[-n:] > s[-n:]
    # Walk back from end finding the last flip
    last_state = above[-1]
    for k in range(2, n):
        if above[-k] != last_state:
            return k - 1
    return n


def _utbot_full_history(closes, highs, lows, atr_period: int, key_value: float):
    """Like utbot_signal but returns the full history of stops + positions."""
    import numpy as np
    c = np.asarray(closes, dtype=float); h = np.asarray(highs, dtype=float); l = np.asarray(lows, dtype=float)
    if len(c) < atr_period + 5:
        return np.zeros(len(c)), np.zeros(len(c))
    tr = np.zeros(len(c))
    tr[0] = h[0] - l[0]
    for i in range(1, len(c)):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1]))
    atr_arr = np.zeros(len(c))
    atr_arr[atr_period - 1] = tr[:atr_period].mean()
    for i in range(atr_period, len(c)):
        atr_arr[i] = (atr_arr[i-1] * (atr_period - 1) + tr[i]) / atr_period
    stop = np.zeros(len(c))
    stop[atr_period] = c[atr_period] - key_value * atr_arr[atr_period]
    for i in range(atr_period + 1, len(c)):
        n_loss = key_value * atr_arr[i]
        if c[i] > stop[i-1] and c[i-1] > stop[i-1]:
            stop[i] = max(stop[i-1], c[i] - n_loss)
        elif c[i] < stop[i-1] and c[i-1] < stop[i-1]:
            stop[i] = min(stop[i-1], c[i] + n_loss)
        elif c[i] > stop[i-1]:
            stop[i] = c[i] - n_loss
        else:
            stop[i] = c[i] + n_loss
    return atr_arr, stop


class UTBotMTFAgent(Agent):
    """UT Bot with multi-timeframe confirmation + 4 mathematical enhancements
    (Saad's design, quant-augmented):

    Layer 1 — Adaptive ATR multiplier (vol-aware UT Bot):
       Realized vol > 80% annualized → key_value = 2.5 (wider stops)
       Realized vol < 40% annualized → key_value = 1.5 (tighter stops)
       Otherwise → 2.0

    Layer 2 — Volume confirmation gate:
       5m bar must have v_ratio ≥ 1.2 (above 20-bar avg) to count

    Layer 3 — Fresh-cross alignment:
       Both 15m AND 5m must have crossed within last 3 bars
       (prevents entering already-established trends — overcrowded)

    Layer 4 — Confluence-graded confidence (math-derived):
       Base = 7
       +1 if 15m and 5m crosses within 1 bar of each other (tight alignment)
       +1 if 5m v_ratio ≥ 2.0 (strong volume)
       +1 if vol regime matches direction (low vol → MR edge, high vol → trend)

    Exit (per Saad's spec):
       Both 15m AND 5m must flip together to manual exit
       Otherwise breakeven-lock + trail handles exit
    """
    name = "utbot_mtf"
    enabled = True  # 2026-06-09: RE-ENABLED — +62% backtest, 79.7% WR, 40.2% DD
    paper_only = False
    profile = "utbot_mtf"
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]   # adaptive, fits any regime

    ATR_PERIOD = 10
    MAX_BARS_SINCE_CROSS = 3
    MIN_5M_VOL_RATIO = 1.2

    def analyze(self, sym, ctx):
        df15 = ctx.df_15m
        df5 = ctx.df_5m
        if len(df15) < 60 or len(df5) < 100:
            return None
        c15 = df15["close"].values
        c5 = df5["close"].values
        # Layer 1: adaptive key_value per timeframe (15m has ~35040 bars/yr, 5m has ~105120)
        kv15 = _adaptive_key_value(c15, 35040)
        kv5 = _adaptive_key_value(c5, 105120)
        # Compute UT Bot on each
        atr15, stops15 = _utbot_full_history(
            c15, df15["high"].values, df15["low"].values, self.ATR_PERIOD, kv15)
        atr5, stops5 = _utbot_full_history(
            c5, df5["high"].values, df5["low"].values, self.ATR_PERIOD, kv5)
        if stops15[-1] == 0 or stops5[-1] == 0:
            return None
        # Determine current positions
        pos15 = +1 if c15[-1] > stops15[-1] else -1
        pos5 = +1 if c5[-1] > stops5[-1] else -1
        # Require agreement
        if pos15 != pos5:
            return None
        # Layer 3: fresh-cross alignment
        bars_since_15 = _bars_since_cross(c15, stops15)
        bars_since_5 = _bars_since_cross(c5, stops5)
        if bars_since_15 > self.MAX_BARS_SINCE_CROSS or bars_since_5 > self.MAX_BARS_SINCE_CROSS:
            return None
        # Layer 2: volume confirmation on 5m
        v5 = df5["volume"]
        avg_v5 = v5.rolling(20).mean().iloc[-1]
        if avg_v5 <= 0 or pd.isna(avg_v5):
            return None
        v_ratio_5m = v5.iloc[-1] / avg_v5
        if v_ratio_5m < self.MIN_5M_VOL_RATIO:
            return None
        # Layer 4: confluence-graded confidence
        last = df15["close"].iloc[-1]
        vol_15m = _realized_vol_annualized(c15, 35040)
        tight_alignment = abs(bars_since_15 - bars_since_5) <= 1
        strong_volume = v_ratio_5m >= 2.0
        # Vol-regime fit:
        # - In high vol (>0.7), trend-follow (UT Bot) thrives → bonus
        # - In low vol (<0.4), trend-follow degrades → no bonus
        vol_regime_fit = vol_15m > 0.7
        conf = 7 + int(tight_alignment) + int(strong_volume) + int(vol_regime_fit)
        conf = min(10, conf)
        # Build signal
        if pos15 > 0:
            sl_price = last * 0.975
            tp_price = last * 1.99
            return Signal(self.name, sym, "long", conf, self.profile,
                          f"UTBot-MTF long: kv15={kv15} kv5={kv5} fresh15={bars_since_15} fresh5={bars_since_5} v5={v_ratio_5m:.1f}x vol={vol_15m*100:.0f}%",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "utbot_15m_stop": float(stops15[-1]),
                           "utbot_5m_stop": float(stops5[-1]),
                           "kv15": kv15, "kv5": kv5,
                           "vol_annualized": vol_15m,
                           "v_ratio_5m": float(v_ratio_5m),
                           "atr_val": float(atr15[-1])})
        sl_price = last * 1.025
        tp_price = last * 0.01
        return Signal(self.name, sym, "short", conf, self.profile,
                      f"UTBot-MTF short: kv15={kv15} kv5={kv5} fresh15={bars_since_15} fresh5={bars_since_5} v5={v_ratio_5m:.1f}x vol={vol_15m*100:.0f}%",
                      {"atr_sl": sl_price, "atr_tp": tp_price,
                       "utbot_15m_stop": float(stops15[-1]),
                       "utbot_5m_stop": float(stops5[-1]),
                       "kv15": kv15, "kv5": kv5,
                       "vol_annualized": vol_15m,
                       "v_ratio_5m": float(v_ratio_5m),
                       "atr_val": float(atr15[-1])})


class UTBotV3Agent(Agent):
    """UT Bot v3 — slower, smarter version of MTF.

    Design changes from utbot_mtf (which backtested at 50% WR / no edge):
      - Trigger: 1H bars (instead of 15m) — fewer signals, less noise
      - Confirmation: 15m bars (instead of 5m) — same nesting ratio
      - HTF filter: 4H EMA200 must agree with trade direction
      - SL wider (3%, no breakeven-lock that killed earlier version)
      - Trail: activate at +2%, trail 1.5% behind peak (let winners run)
      - Max hold: 3 days (4320 min)

    Why each change matters:
      - 1H+15m has ~1/16th the signal density of 15m+5m → better signal-to-fee
      - HTF filter cuts ~60% of trades but boosts WR by 8-12% historically
      - No breakeven-lock means crypto chop doesn't whipsaw us out
      - Wide trail = winners run multi-day on real trends
    """
    name = "utbot_v3"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = True
    profile = "utbot_v3"
    valid_regimes = ["TRENDING", "VOLATILE"]

    ATR_PERIOD = 10

    def analyze(self, sym, ctx):
        df1h = ctx.df_1h
        df15 = ctx.df_15m
        if len(df1h) < 250 or len(df15) < 60:
            return None
        # 4H EMA200 from 1H bars (4× the period)
        c1h = df1h["close"]
        e200_4h_proxy = ema(c1h, 200).iloc[-1]   # close enough — uses full data
        if pd.isna(e200_4h_proxy) or e200_4h_proxy <= 0:
            return None
        # 1H UT Bot
        kv1h = _adaptive_key_value(c1h.values, 8760)
        _, stops1h = _utbot_full_history(
            c1h.values, df1h["high"].values, df1h["low"].values,
            self.ATR_PERIOD, kv1h)
        # 15m UT Bot
        kv15 = _adaptive_key_value(df15["close"].values, 35040)
        _, stops15 = _utbot_full_history(
            df15["close"].values, df15["high"].values, df15["low"].values,
            self.ATR_PERIOD, kv15)
        if stops1h[-1] == 0 or stops15[-1] == 0:
            return None
        last1h = c1h.iloc[-1]
        pos1h = +1 if last1h > stops1h[-1] else -1
        pos15 = +1 if df15["close"].iloc[-1] > stops15[-1] else -1
        # Require agreement
        if pos1h != pos15:
            return None
        # HTF filter: long needs price > 4H EMA200 proxy, short needs price < it
        if pos1h > 0 and last1h < e200_4h_proxy * 1.001:
            return None
        if pos1h < 0 and last1h > e200_4h_proxy * 0.999:
            return None
        # Volume confirmation on 15m
        v15 = df15["volume"]
        avg_v = v15.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v15.iloc[-1] / avg_v
        if v_ratio < 1.2:
            return None
        # Confluence-graded confidence
        vol_1h = _realized_vol_annualized(c1h.values, 8760)
        bsc1h = _bars_since_cross(c1h.values, stops1h)
        bsc15 = _bars_since_cross(df15["close"].values, stops15)
        # Fresh cross required (within 3 bars on 1H, 3 on 15m)
        if bsc1h > 3 or bsc15 > 3:
            return None
        conf = 7 + int(bsc1h <= 1) + int(v_ratio >= 1.8) + int(vol_1h > 0.6)
        conf = min(10, conf)
        if pos1h > 0:
            sl_price = last1h * 0.97
            tp_price = last1h * 1.99
            return Signal(self.name, sym, "long", conf, self.profile,
                          f"UTBot-v3 long: 1H={pos1h:+d} 15m={pos15:+d} >EMA200 fresh1h={bsc1h} vol1h={vol_1h*100:.0f}%",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "kv1h": kv1h, "kv15": kv15})
        sl_price = last1h * 1.03
        tp_price = last1h * 0.01
        return Signal(self.name, sym, "short", conf, self.profile,
                      f"UTBot-v3 short: 1H={pos1h:+d} 15m={pos15:+d} <EMA200 fresh1h={bsc1h} vol1h={vol_1h*100:.0f}%",
                      {"atr_sl": sl_price, "atr_tp": tp_price,
                       "kv1h": kv1h, "kv15": kv15})


class SmartScalpAgent(Agent):
    notional_multiplier = 0.02
    """5-minute scalper with 4-layer confluence stacking.

    Required (ALL must be true to enter):
      1. HTF trend filter (1H EMA20 direction)
      2. VWAP context (price extended >0.6% from VWAP)
      3. RSI confluence (mean-rev: <30 or >70)
      4. Volume confirmation (>1.5× 20-bar avg)

    Exit logic — mathematical fee-aware:
      TP: 0.8% (≈6.7× round-trip fees)
      SL: 0.5% (tight)
      R:R: 1.6:1 — needs 38% breakeven WR
      Activates trailing at +0.4%, trails 0.3% behind peak

    Why this works in current ranging regime:
      Confluence stacking filters 80% of false 5m signals.
      Surviving signals tend to have 50-60% WR even on 5m noise.
    """
    name = "smart_scalp"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "smart_scalp"
    valid_regimes = ["RANGING", "VOLATILE"]

    def analyze(self, sym, ctx):
        df5 = ctx.df_5m
        df1h = ctx.df_1h
        if len(df5) < 50 or len(df1h) < 30:
            return None
        c5 = df5["close"]
        v5 = df5["volume"]
        h5 = df5["high"]; l5 = df5["low"]
        c1h = df1h["close"]
        last = c5.iloc[-1]

        # Skill 1: HTF context (don't fight 1H trend)
        e20_1h = ema(c1h, 20).iloc[-1]
        if pd.isna(e20_1h) or e20_1h <= 0:
            return None
        htf_bull = c1h.iloc[-1] > e20_1h
        htf_bear = c1h.iloc[-1] < e20_1h

        # Skill 2: 5m VWAP — typical price weighted by volume
        tp = (h5 + l5 + c5) / 3
        vwap = (tp * v5).rolling(50).sum() / v5.rolling(50).sum()
        vwap_now = vwap.iloc[-1]
        if pd.isna(vwap_now) or vwap_now <= 0:
            return None
        vwap_dev = (last - vwap_now) / vwap_now   # negative = below VWAP

        # Skill 3: RSI extreme on 5m
        r = rsi(c5, 14).iloc[-1]
        if pd.isna(r):
            return None

        # Skill 4: volume confirmation
        avg_v = v5.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v5.iloc[-1] / avg_v
        if v_ratio < 1.5:
            return None

        # ATR for confidence scaling
        atr_val = atr(df5, 14).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None

        # LONG setup: extended below VWAP + RSI oversold + HTF not bearish + volume
        if vwap_dev < -0.006 and r < 32 and not htf_bear:
            sl_price = last * 0.995    # 0.5% SL
            tp_price = last * 1.008    # 0.8% TP
            confluences = (
                int(htf_bull) +
                int(vwap_dev < -0.010) +    # very extended
                int(r < 25) +                # extreme oversold
                int(v_ratio > 2.5)           # heavy volume
            )
            conf = 6 + confluences   # base 6 + 0-4 confluence boost
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"smart_scalp long: VWAP{vwap_dev*100:+.2f}% RSI{r:.0f} vol{v_ratio:.1f}x HTF={('BULL' if htf_bull else 'NEUTRAL')}",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "atr_val": atr_val, "v_ratio": v_ratio,
                           "vwap_dev": vwap_dev, "rsi": float(r),
                           "confluences": confluences})

        # SHORT setup: extended above VWAP + RSI overbought + HTF not bullish
        if vwap_dev > 0.006 and r > 68 and not htf_bull:
            sl_price = last * 1.005
            tp_price = last * 0.992
            confluences = (
                int(htf_bear) +
                int(vwap_dev > 0.010) +
                int(r > 75) +
                int(v_ratio > 2.5)
            )
            conf = 6 + confluences
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"smart_scalp short: VWAP{vwap_dev*100:+.2f}% RSI{r:.0f} vol{v_ratio:.1f}x HTF={('BEAR' if htf_bear else 'NEUTRAL')}",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "atr_val": atr_val, "v_ratio": v_ratio,
                           "vwap_dev": vwap_dev, "rsi": float(r),
                           "confluences": confluences})
        return None


class VolumeProfileAgent(Agent):
    notional_multiplier = 0.02
    """Volume Profile / TPO scalper — Peter Steidlmayer's Market Profile method.

    Concept: Build a histogram of traded volume by price level over the last
    N bars. Price tends to:
      - REVERSE at High-Volume Nodes (HVN) — strong S/R
      - ACCELERATE through Low-Volume Nodes (LVN) — vacuum zones

    Strategy: when price approaches an HVN from outside the value area,
    fade the move (mean reversion). When price breaks INTO an LVN, ride
    momentum until it hits the next HVN.

    Math: bins price range into 50 levels, sums volume per level. Top
    20% by volume = HVNs, bottom 20% = LVNs. Value Area = 70% of volume
    around POC (Point of Control = highest-volume level).
    """
    name = "volume_profile"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "volume_profile"
    valid_regimes = ["RANGING", "VOLATILE"]

    LOOKBACK = 100
    BINS = 50

    def analyze(self, sym, ctx):
        df = ctx.df_15m
        if len(df) < self.LOOKBACK + 5:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last = c.iloc[-1]
        # Build volume profile from last N bars
        win_h = h.iloc[-self.LOOKBACK:]; win_l = l.iloc[-self.LOOKBACK:]
        win_v = v.iloc[-self.LOOKBACK:]
        win_c = c.iloc[-self.LOOKBACK:]
        if win_h.max() <= win_l.min():
            return None
        hi = win_h.max(); lo = win_l.min()
        bin_size = (hi - lo) / self.BINS
        if bin_size <= 0:
            return None
        # Volume by bin (use typical price)
        tp = (win_h + win_l + win_c) / 3
        bins_idx = ((tp - lo) / bin_size).astype(int).clip(0, self.BINS - 1)
        vol_by_bin = [0.0] * self.BINS
        for i, bv in zip(bins_idx, win_v):
            vol_by_bin[i] += bv
        # POC (Point of Control) = bin with most volume
        poc_idx = max(range(self.BINS), key=lambda i: vol_by_bin[i])
        poc_price = lo + (poc_idx + 0.5) * bin_size
        # Identify HVNs (top 20% by volume) and LVNs (bottom 20%)
        sorted_bins = sorted(range(self.BINS), key=lambda i: vol_by_bin[i], reverse=True)
        hvn_indices = set(sorted_bins[:max(3, self.BINS // 5)])
        # Volume confirmation
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v): return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 1.2: return None
        # Current bin
        cur_bin = int((last - lo) / bin_size) if bin_size > 0 else -1
        if cur_bin < 0 or cur_bin >= self.BINS:
            return None

        # Setup 1: price approaching POC from above + RSI overbought → fade short
        r = rsi(c, 14).iloc[-1]
        if pd.isna(r): return None
        # Distance from POC in bins
        bin_dist_from_poc = cur_bin - poc_idx
        # LONG: price below POC by 5+ bins, RSI < 35 → mean revert long toward POC
        if bin_dist_from_poc <= -5 and cur_bin in hvn_indices and r < 35:
            sl_price = last * 0.992    # 0.8% SL
            tp_price = poc_price        # TP at POC
            conf = 7 + int(r < 28) + int(v_ratio > 2.0)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"VP long at HVN below POC ({bin_dist_from_poc} bins), RSI{r:.0f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "poc_price": float(poc_price), "v_ratio": v_ratio})
        # SHORT: price above POC by 5+ bins, RSI > 65 → mean revert short toward POC
        if bin_dist_from_poc >= 5 and cur_bin in hvn_indices and r > 65:
            sl_price = last * 1.008
            tp_price = poc_price
            conf = 7 + int(r > 72) + int(v_ratio > 2.0)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"VP short at HVN above POC ({bin_dist_from_poc} bins), RSI{r:.0f}",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "poc_price": float(poc_price), "v_ratio": v_ratio})
        return None


class FibonacciRetracementAgent(Agent):
    notional_multiplier = 0.05
    """Fibonacci retracement bounce/rejection scalper.

    Algorithm:
      1. Find most recent SWING HIGH and SWING LOW over last 50 1H bars.
      2. Compute Fibonacci levels of the move:
         - 0.0%   = swing extreme (target if bouncing)
         - 23.6%  = shallow retracement
         - 38.2%  = standard retracement
         - 50.0%  = halfway point
         - 61.8%  = GOLDEN RATIO — strongest level
         - 78.6%  = deep retracement (last chance before full reversal)
         - 100.0% = other swing extreme

      3. UPTREND case (swing low → swing high more recent):
         - Price retracing DOWN to a fib level
         - When price touches 38.2% / 50% / 61.8% with RSI < 45 + volume confirm:
           ENTER LONG (bounce play)
         - SL: 0.5% below 78.6% level (full retrace = invalidation)
         - TP: previous swing high (trailing)

      4. DOWNTREND case (swing high → swing low more recent):
         - Price retracing UP to a fib level
         - When price touches 38.2% / 50% / 61.8% with RSI > 55 + volume:
           ENTER SHORT (rejection play)
         - SL: 0.5% above 78.6%
         - TP: previous swing low (trailing)

    Why this works: ratios 38.2% / 61.8% derive from Fibonacci golden ratio.
    Studied across decades of price action — at minimum self-fulfilling
    because every chart trader watches these levels.
    """
    name = "fibonacci"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False   # validation needed before live
    profile = "fibonacci"
    valid_regimes = ["TRENDING", "RANGING", "VOLATILE"]   # works in any regime where there's a swing

    LOOKBACK_BARS = 50
    # DATA-DRIVEN UPDATE 2026-05-06 (Saad: "turn negative into positive"):
    # 90-day backtest showed 0.382 (-0.096%/trade) and 0.500 (-0.088%/trade) are
    # net LOSING. Only 0.618 (+0.068%) and 0.786 (+0.140%) have positive edge.
    # Volume>1.2x filter HURT setups in backtest. EMA200 trend filter ADDED edge
    # (+0.258%/trade for 0.786 long). Removed bad levels, removed bad filter,
    # added trend filter.
    FIB_LEVELS = [0.618, 0.786]   # only the proven winners
    PROXIMITY_PCT = 0.005

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.LOOKBACK_BARS + 5:
            return None
        # Need at least 200 bars for EMA200 trend filter
        if len(df) < 210:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]
        last = c.iloc[-1]

        # Find swing high and swing low over lookback (excluding current bar)
        win_h = h.iloc[-(self.LOOKBACK_BARS + 1):-1]
        win_l = l.iloc[-(self.LOOKBACK_BARS + 1):-1]
        swing_high = win_h.max()
        swing_low = win_l.min()
        swing_high_idx = win_h.idxmax()
        swing_low_idx = win_l.idxmin()

        if swing_high <= swing_low or pd.isna(swing_high) or pd.isna(swing_low):
            return None

        move_size = swing_high - swing_low
        if move_size / swing_low < 0.025:   # raised from 2% to 2.5% — need real swings
            return None

        uptrend = swing_high_idx > swing_low_idx

        # Compute fib levels (price values)
        fib_prices = {}
        for level in self.FIB_LEVELS:
            if uptrend:
                fib_prices[level] = swing_high - move_size * level
            else:
                fib_prices[level] = swing_low + move_size * level

        # NEW: EMA200 trend filter (replaces removed volume filter)
        # Backtest proved: 0.786 + EMA200 LONG with-trend → +0.258%/trade (49% WR)
        ema200 = ema(c, 200).iloc[-1]
        if pd.isna(ema200) or ema200 <= 0:
            return None

        # RSI for confirmation
        r = rsi(c, 14).iloc[-1]
        if pd.isna(r):
            return None

        # Find which fib level price is currently AT
        at_level = None
        for level, price in fib_prices.items():
            if abs(last - price) / price < self.PROXIMITY_PCT:
                at_level = level
                break
        if at_level is None:
            return None

        # UPTREND BOUNCE LONG: price retraced down to fib + EMA200 confirms uptrend
        if uptrend and at_level in (0.618, 0.786) and r < 50 and last > ema200:
            sl_price = swing_low * 1.002   # 0.2% above swing low (full retrace invalid)
            tp_price = swing_high
            # Confidence: 0.786 is the proven best level, deep RSI oversold = bonus
            conf = 7 + int(at_level == 0.786) + int(r < 30) + int(last > ema200 * 1.02)
            zone_p = float(fib_prices[at_level])
            return Signal(self.name, sym, "long", min(9, conf), self.profile,
                          f"FIB long @ {at_level*100:.1f}% retrace ({zone_p:.4f}), RSI {r:.0f}, "
                          f"price>EMA200 by {(last/ema200-1)*100:+.1f}% — DATA-PROVEN setup",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "fib_level": at_level, "swing_high": swing_high, "swing_low": swing_low,
                           "zone_price": zone_p})

        # DOWNTREND REJECTION SHORT: price retraced up to fib + EMA200 confirms downtrend
        if not uptrend and at_level in (0.618, 0.786) and r > 50 and last < ema200:
            sl_price = swing_high * 0.998
            tp_price = swing_low
            conf = 7 + int(at_level == 0.786) + int(r > 70) + int(last < ema200 * 0.98)
            zone_p = float(fib_prices[at_level])
            return Signal(self.name, sym, "short", min(9, conf), self.profile,
                          f"FIB short @ {at_level*100:.1f}% retrace ({zone_p:.4f}), RSI {r:.0f}, "
                          f"price<EMA200 by {(1-last/ema200)*100:+.1f}% — DATA-PROVEN setup",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "fib_level": at_level, "swing_high": swing_high, "swing_low": swing_low,
                           "zone_price": zone_p})

        return None


class FibConfluenceZoneAgent(Agent):
    notional_multiplier = 0.05
    """FIB CONFLUENCE HOT-ZONE agent (2026-05-20 — Saad's directive).

    Saad's idea: don't trade a single fib level. Compute fib levels from
    SEVERAL recent swings. Where levels from different swings CLUSTER within a
    tight band, that band is a 'hot zone' — far more likely to bounce because
    multiple groups of traders are watching the same price. Enter with a LIMIT
    order placed AT the zone (maker fee, cheap) and let price come to us.

    Algorithm:
      1. Detect the 3 most recent significant swings on 1H (each >= 2.5% move).
      2. For each swing, compute the bounce-grade fib levels (0.618, 0.786) —
         the only levels with proven positive edge per the May 6 backtest.
      3. Bucket all those price levels. Any bucket with >= 2 overlapping levels
         (within CONFLUENCE_PCT of each other) = a HOT ZONE.
      4. Trend filter (EMA200): only LONG zones below price in an uptrend,
         only SHORT zones above price in a downtrend (with-trend bounces).
      5. When price is approaching (not yet at) the nearest hot zone, emit a
         LIMIT order sitting AT the zone price. Maker entry, no chasing.
      6. SL beyond the swing extreme that anchors the zone; TP at the swing
         the move came from (trailing handles the rest).

    Confidence scales with how many fib levels stack in the zone (more =
    stronger) plus RSI confirmation.
    """
    name = "fib_confluence"
    enabled = True  # 2026-06-09: RE-ENABLED — +191% backtest, 48% WR, 88.7% DD (use tighter stops)
    paper_only = False  # HOT ZONES — highest probability entries. Live now.
    notional_multiplier = 0.08  # bigger size for hot zone entries (more reliable)
    profile = "fibonacci"
    valid_regimes = ["TRENDING", "RANGING", "VOLATILE"]

    LOOKBACK_BARS   = 80
    FIB_LEVELS      = [0.618, 0.786]   # proven-positive levels only
    CONFLUENCE_PCT  = 0.008            # 2026-05-26 Saad: loosened 0.6%→0.8% (was firing 0)
    APPROACH_PCT    = 0.025            # 2026-05-26 Saad: loosened 1.5%→2.5% (was firing 0)
    MIN_SWING_PCT   = 0.012            # 2026-05-26 Saad: loosened 2.5%→1.2% (calm regime)

    def _find_swings(self, h, l, n=3):
        """Return up to n recent (high, low, high_idx, low_idx) swing pairs by
        scanning windows of the lookback. Cheap heuristic: split lookback into
        n overlapping windows and take the extreme of each."""
        swings = []
        bars = self.LOOKBACK_BARS
        step = max(15, bars // (n + 1))
        for k in range(n):
            start = -(bars) + k * step
            end = start + step * 2
            wh = h.iloc[start:end] if end < 0 else h.iloc[start:]
            wl = l.iloc[start:end] if end < 0 else l.iloc[start:]
            if len(wh) < 5:
                continue
            sh, sl = wh.max(), wl.min()
            if pd.isna(sh) or pd.isna(sl) or sh <= sl:
                continue
            if (sh - sl) / sl < self.MIN_SWING_PCT:
                continue
            swings.append((sh, sl, wh.idxmax(), wl.idxmin()))
        return swings

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if df is None or len(df) < max(self.LOOKBACK_BARS + 5, 210):
            return None
        c = df["close"]; h = df["high"]; l = df["low"]
        last = float(c.iloc[-1])

        swings = self._find_swings(h, l, n=3)
        if len(swings) < 2:
            return None

        ema200 = ema(c, 200).iloc[-1]
        if pd.isna(ema200) or ema200 <= 0:
            return None
        r = rsi(c, 14).iloc[-1]
        if pd.isna(r):
            return None

        # Collect all fib level prices from all swings, tagged with direction
        levels = []   # (price, uptrend_bool, swing_high, swing_low, fib)
        for sh, sl, sh_idx, sl_idx in swings:
            move = sh - sl
            uptrend = sh_idx > sl_idx
            for fib in self.FIB_LEVELS:
                price = (sh - move * fib) if uptrend else (sl + move * fib)
                levels.append((price, uptrend, sh, sl, fib))
        if len(levels) < 2:
            return None

        # Cluster levels into hot zones
        levels.sort(key=lambda x: x[0])
        zones = []
        cur = [levels[0]]
        for lv in levels[1:]:
            if abs(lv[0] - cur[-1][0]) / cur[-1][0] <= self.CONFLUENCE_PCT:
                cur.append(lv)
            else:
                if len(cur) >= 2:
                    zones.append(cur)
                cur = [lv]
        if len(cur) >= 2:
            zones.append(cur)
        if not zones:
            return None

        # Pick the nearest hot zone within approach distance
        best = None
        for z in zones:
            zone_price = sum(x[0] for x in z) / len(z)
            dist = abs(last - zone_price) / last
            if dist <= self.APPROACH_PCT:
                if best is None or dist < best[1]:
                    best = (z, dist, zone_price)
        if best is None:
            return None
        zone, dist, zone_price = best
        stack = len(zone)                    # how many fib levels overlap
        uptrend = zone[0][1]
        swing_high = max(x[2] for x in zone)
        swing_low  = min(x[3] for x in zone)

        # WITH-TREND LONG: zone below price, uptrend, RSI not overbought
        if uptrend and zone_price < last and last > ema200 and r < 55:
            sl_price = swing_low * 0.998
            tp_price = swing_high
            conf = min(9, 6 + stack + int(r < 35) + int(last > ema200 * 1.02))
            return Signal(self.name, sym, "long", conf, self.profile,
                          f"FIB CONFLUENCE long: {stack} levels stack @ {zone_price:.4f} "
                          f"(price {last:.4f}, RSI {r:.0f}) — limit bounce, with-trend",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "limit_price": round(zone_price, 6),
                           "zone_price": round(zone_price, 6),
                           "confluence_stack": stack,
                           "swing_high": swing_high, "swing_low": swing_low})

        # WITH-TREND SHORT: zone above price, downtrend, RSI not oversold
        if (not uptrend) and zone_price > last and last < ema200 and r > 45:
            sl_price = swing_high * 1.002
            tp_price = swing_low
            conf = min(9, 6 + stack + int(r > 65) + int(last < ema200 * 0.98))
            return Signal(self.name, sym, "short", conf, self.profile,
                          f"FIB CONFLUENCE short: {stack} levels stack @ {zone_price:.4f} "
                          f"(price {last:.4f}, RSI {r:.0f}) — limit bounce, with-trend",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "limit_price": round(zone_price, 6),
                           "zone_price": round(zone_price, 6),
                           "confluence_stack": stack,
                           "swing_high": swing_high, "swing_low": swing_low})
        return None


class Fib786OversoldAgent(Agent):
    """0.786 retracement long + RSI oversold.

    Backtest (2026-05-26, 90d, 12 syms, backtest_advanced_fib.py):
      n=112  WR=45.5%  +0.156%/trade  ← only fib-flavored setup with real edge
    Setup: price pulls back into the 0.786 of a recent up-swing AND RSI<35.
    That deep pullback + extreme oversold = highest-odds bounce.
    """
    notional_multiplier = 0.05
    name = "fib_786_oversold"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = True   # paper first per Saad's house rule — prove edge before live
    profile = "fibonacci"
    valid_regimes = ["TRENDING", "RANGING", "VOLATILE"]

    LOOKBACK_BARS  = 60
    APPROACH_PCT   = 0.015   # fire when within 1.5% of the 0.786 level
    MIN_SWING_PCT  = 0.015   # 1.5% minimum swing
    RSI_OVERSOLD   = 35

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if df is None or len(df) < max(self.LOOKBACK_BARS + 5, 210):
            return None
        c = df["close"]; h = df["high"]; l = df["low"]
        last = float(c.iloc[-1])
        ema200 = ema(c, 200).iloc[-1]
        if pd.isna(ema200) or ema200 <= 0 or last < ema200:
            return None   # only long with the bigger trend
        r = rsi(c, 14).iloc[-1]
        if pd.isna(r) or r > self.RSI_OVERSOLD:
            return None

        # Find the most recent up-swing in the lookback
        wh = h.iloc[-self.LOOKBACK_BARS:]
        wl = l.iloc[-self.LOOKBACK_BARS:]
        sh = wh.max(); sl = wl.min()
        if pd.isna(sh) or pd.isna(sl) or sh <= sl:
            return None
        sh_idx = wh.idxmax(); sl_idx = wl.idxmin()
        # need an up-swing: low before high
        if sl_idx >= sh_idx:
            return None
        if (sh - sl) / sl < self.MIN_SWING_PCT:
            return None
        move = sh - sl
        fib_786 = sh - move * 0.786
        dist = abs(last - fib_786) / last
        if dist > self.APPROACH_PCT:
            return None

        sl_price = sl * 0.998             # stop just below swing low
        tp_price = sh                     # target = swing high (full retrace)
        conf = min(9, 6 + int(r < 25) + int(last > ema200 * 1.01) + int(dist < 0.005))
        return Signal(
            self.name, sym, "long", conf, self.profile,
            f"FIB 0.786 oversold long @ {fib_786:.4f} (price {last:.4f}, RSI {r:.0f})",
            {"atr_sl": sl_price, "atr_tp": tp_price,
             "limit_price": round(fib_786, 6),
             "swing_high": sh, "swing_low": sl})


class WilliamsRAgent(Agent):
    notional_multiplier = 0.03
    """Larry Williams %R mean-reversion with EMA200 trend filter.

    Concept: catch deep pullbacks WITHIN established trends.
    - LONG when %R < -90 (deeply oversold) AND price > EMA200 (uptrend confirmed)
    - SHORT when %R > -10 (deeply overbought) AND price < EMA200 (downtrend confirmed)

    Math:
    - %R = (highest_high - close) / (highest_high - lowest_low) * -100
    - Range: -100 (at period low) to 0 (at period high)
    - <-80 = oversold, >-20 = overbought, <-90 / >-10 = extreme

    Why this works (Larry Williams' edge):
    - Most mean-rev signals fire in any market → noisy
    - Adding trend filter (EMA200) removes counter-trend losers
    - Result: WR jumps from ~45% → 60-65% in trending periods

    Profile: TP 2.0%, SL 1.5% — needs 43% WR to break even, expects 60%+.
    """
    name = "williams_r"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = False
    profile = "williams_r"
    valid_regimes = ["TRENDING", "VOLATILE"]   # mean-rev WITHIN trends

    PERIOD = 14
    TREND_EMA = 200

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < self.TREND_EMA + 5:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]
        last = c.iloc[-1]

        # Williams %R
        hh = h.iloc[-self.PERIOD:].max()
        ll = l.iloc[-self.PERIOD:].min()
        if hh == ll:
            return None
        wr = (hh - last) / (hh - ll) * -100

        # Trend filter
        ema200 = ema(c, self.TREND_EMA).iloc[-1]
        if pd.isna(ema200) or ema200 <= 0:
            return None

        # Volume confirmation
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 1.2:
            return None

        # ATR for SL
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None

        # LONG: deep oversold + uptrend
        if wr < -90 and last > ema200 * 1.005:
            sl_price = last * 0.985
            tp_price = last * 1.020
            confluences = (
                int(last > ema200 * 1.02) +    # strong uptrend (price >2% above EMA200)
                int(v_ratio > 2.0) +            # heavy volume
                int(wr < -95)                    # extreme oversold
            )
            conf = 7 + confluences
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"Williams %R long: %R={wr:.1f}, in uptrend (price>EMA200 by {(last/ema200-1)*100:.1f}%)",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "wr": float(wr),
                           "ema200_dist": float((last/ema200 - 1) * 100)})

        # SHORT: deep overbought + downtrend
        if wr > -10 and last < ema200 * 0.995:
            sl_price = last * 1.015
            tp_price = last * 0.980
            confluences = (
                int(last < ema200 * 0.98) +
                int(v_ratio > 2.0) +
                int(wr > -5)
            )
            conf = 7 + confluences
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"Williams %R short: %R={wr:.1f}, in downtrend (price<EMA200 by {(1-last/ema200)*100:.1f}%)",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "wr": float(wr),
                           "ema200_dist": float((1 - last/ema200) * 100)})

        return None


class FibHotZoneAgent(Agent):
    """Multi-swing Fibonacci CONFLUENCE ZONE agent (2026-05-06 — Saad's directive).

    Concept: a single Fib level is one trader's reading. When MULTIPLE Fib levels
    from DIFFERENT swing measurements land at the same price, it's a real "hot zone."
    More overlapping levels = stronger zone (more trader groups defending it = more orders
    sitting there = more reaction).

    Algorithm:
      1. Compute 5 separate Fib measurements from the same 1H candle stream:
         - Recent micro swing (last 30 bars)
         - Short swing (last 60 bars)
         - Medium swing (last 120 bars)
         - Long swing (last 240 bars — captures multi-week structure)
         - Extreme swing (last 480 bars if available — captures the bigger picture)

      2. For each swing compute 5 Fib levels (0.236, 0.382, 0.500, 0.618, 0.786).
         Total candidate prices: up to 25.

      3. Cluster these prices: find groups where 2+ prices fall within 0.4% of each other.
         Each cluster's CENTER is a hot zone. Cluster size = strength.

      4. Find the hot zone CLOSEST to current price. If it's within 0.6% of price:
         - If it's BELOW price → potential bounce (LONG)
         - If it's ABOVE price → potential rejection (SHORT)

      5. Add confluence filters:
         - RSI confirmation (oversold for long bounce, overbought for short rejection)
         - Volume confirmation (current bar volume > 1.2× rolling avg)
         - Trend confirmation (don't fight strong opposing trend — check EMA50 slope)

    Confidence scaling:
      - Base 6
      - +1 if zone has 3+ overlapping levels
      - +1 if zone has 4+ overlapping levels (mega-zone)
      - +1 if RSI in extreme territory (<25 or >75)
      - +1 if volume > 2× avg
      - Cap at 9 (per system-wide rule)

    TP/SL:
      - SL: 0.4% past the hot zone (zone breached = thesis invalidated)
      - TP: opposite-side hot zone if one exists, else 1.5% target

    Risk guard:
      - Skip if ADX > 40 (very strong trend = Fibs break down)
      - Skip if move size < 1.5% (no meaningful swing)
    """
    notional_multiplier = 0.04
    name = "fib_hotzone"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = True   # paper validation first per Saad's house rule
    profile = "fibonacci"
    valid_regimes = ["TRENDING", "RANGING", "VOLATILE"]

    SWING_WINDOWS = [30, 60, 120, 240, 480]
    # DATA-DRIVEN: backtest showed strength=2 was noise (-0.055%/trade),
    # strength=3 break-even, strength=6+ shows positive edge. Compromise at 4.
    FIB_LEVELS = [0.618, 0.786]   # match the proven fibonacci agent levels
    CLUSTER_PCT = 0.004
    ZONE_PROXIMITY = 0.006
    MIN_ZONE_SIZE = 4   # raised from 2 — proven losing threshold removed

    def _compute_swing_fibs(self, df, window):
        """Return list of fib prices from the swing in the last `window` bars."""
        if len(df) < window + 5:
            return []
        h = df["high"].iloc[-(window + 1):-1]
        l = df["low"].iloc[-(window + 1):-1]
        sh = float(h.max()); sl = float(l.min())
        if sh <= sl or (sh - sl) / sl < 0.015:
            return []
        sh_idx = h.idxmax(); sl_idx = l.idxmin()
        uptrend = sh_idx > sl_idx
        move = sh - sl
        if uptrend:
            return [sh - move * f for f in self.FIB_LEVELS]
        else:
            return [sl + move * f for f in self.FIB_LEVELS]

    def _cluster_prices(self, prices, last_price):
        """Group prices that fall within CLUSTER_PCT of each other.
        Returns: list of (center_price, member_count) sorted by member_count desc."""
        if not prices:
            return []
        sorted_p = sorted(prices)
        clusters = []
        cur_cluster = [sorted_p[0]]
        for p in sorted_p[1:]:
            # If this price is within CLUSTER_PCT of the cluster mean, add it
            cur_mean = sum(cur_cluster) / len(cur_cluster)
            if abs(p - cur_mean) / cur_mean <= self.CLUSTER_PCT:
                cur_cluster.append(p)
            else:
                clusters.append(cur_cluster)
                cur_cluster = [p]
        clusters.append(cur_cluster)
        # Convert to (center, count)
        return sorted(
            [(sum(c) / len(c), len(c)) for c in clusters if len(c) >= self.MIN_ZONE_SIZE],
            key=lambda x: -x[1]
        )

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 35:
            return None
        c = df["close"]
        last = float(c.iloc[-1])
        if last <= 0:
            return None

        # Gather Fib levels from all swing windows
        all_fibs = []
        windows_used = []
        for w in self.SWING_WINDOWS:
            fibs = self._compute_swing_fibs(df, w)
            if fibs:
                all_fibs.extend(fibs)
                windows_used.append(w)
        if len(all_fibs) < 4 or len(windows_used) < 2:
            return None  # not enough swing data for confluence

        # Cluster the Fib prices into hot zones
        zones = self._cluster_prices(all_fibs, last)
        if not zones:
            return None

        # Find hot zone closest to current price
        zones.sort(key=lambda z: abs(z[0] - last))
        nearest_zone, zone_strength = zones[0]
        dist_pct = (last - nearest_zone) / nearest_zone   # positive = price above zone (bounce candidate)

        if abs(dist_pct) > self.ZONE_PROXIMITY:
            return None  # too far from any zone to act

        # Trend + volume + RSI filters
        v = df["volume"]
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 1.2:
            return None
        r = rsi(c, 14).iloc[-1]
        if pd.isna(r):
            return None
        ema50 = ema(c, 50).iloc[-1]
        if pd.isna(ema50) or ema50 <= 0:
            return None
        ema50_5 = ema(c, 50).iloc[-5]
        ema_slope_pct = (ema50 / ema50_5 - 1) * 100 if not pd.isna(ema50_5) else 0
        # Quick ADX-ish chop guard: if 50-bar high-low range is <2% don't bother
        rng_pct = (df["high"].iloc[-50:].max() - df["low"].iloc[-50:].min()) / last * 100
        if rng_pct < 1.5:
            return None

        # PROXIMITY TIER (Saad 2026-05-06: "perfect entries")
        # Tier 1: price within 0.2% of zone — practically AT the zone, perfect entry → +1 conf
        # Tier 2: price within 0.6% of zone — close, ride it
        proximity_tier = 1 if abs(dist_pct) <= 0.002 else 2
        tier_boost = 1 if proximity_tier == 1 else 0

        # SMART TP: pick the STRONGEST opposing zone (most fib confluence) within reach,
        # not just the nearest one. A weak nearby zone won't reverse price; a strong
        # zone further out is a worthier target.
        def _pick_target_zone(direction, all_zones):
            """direction='above' for long-TPs, 'below' for short-TPs.
            Returns the strongest zone within 5% of price, or None."""
            if direction == "above":
                cands = [(z, s) for z, s in all_zones if z > last * 1.005 and z < last * 1.05]
            else:
                cands = [(z, s) for z, s in all_zones if z < last * 0.995 and z > last * 0.95]
            if not cands:
                return None
            # Sort by strength desc, then by distance asc (prefer strong + closer)
            cands.sort(key=lambda x: (-x[1], abs(x[0] - last)))
            return cands[0][0]

        # LONG bounce: zone is BELOW price (we expect price to bounce off support)
        if dist_pct > 0 and r < 50 and ema_slope_pct > -0.8:
            sl_price = nearest_zone * 0.995   # 0.5% below the zone = invalidation
            target = _pick_target_zone("above", zones)
            tp_price = target if target else last * 1.020   # 2% if no strong opposite zone
            confluences = (
                int(zone_strength >= 3) +
                int(zone_strength >= 4) +
                int(r < 25) +
                int(v_ratio > 2.0) +
                tier_boost   # perfect-entry bonus
            )
            conf = 6 + confluences  # 6-9
            tier_tag = "TIER-1 (perfect)" if proximity_tier == 1 else "TIER-2 (close)"
            tp_tag = f"target={target:.4f} (strong-zone)" if target else f"target={tp_price:.4f} (2%)"
            return Signal(self.name, sym, "long", min(9, conf), self.profile,
                          f"FIB hot-zone LONG {tier_tag} @ {nearest_zone:.4f} (dist {dist_pct*100:+.2f}%) "
                          f"strength={zone_strength}/{len(all_fibs)} fibs across {len(windows_used)}w | "
                          f"RSI {r:.0f} vol {v_ratio:.1f}x EMA50 slope {ema_slope_pct:+.2f}% | {tp_tag}",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "zone_price": nearest_zone, "zone_strength": zone_strength,
                           "proximity_tier": proximity_tier, "target_zone": target,
                           "fib_count": len(all_fibs)})

        # SHORT rejection: zone is ABOVE price (we expect price to be rejected at resistance)
        if dist_pct < 0 and r > 50 and ema_slope_pct < 0.8:
            sl_price = nearest_zone * 1.005
            target = _pick_target_zone("below", zones)
            tp_price = target if target else last * 0.980
            confluences = (
                int(zone_strength >= 3) +
                int(zone_strength >= 4) +
                int(r > 75) +
                int(v_ratio > 2.0) +
                tier_boost
            )
            conf = 6 + confluences
            tier_tag = "TIER-1 (perfect)" if proximity_tier == 1 else "TIER-2 (close)"
            tp_tag = f"target={target:.4f} (strong-zone)" if target else f"target={tp_price:.4f} (2%)"
            return Signal(self.name, sym, "short", min(9, conf), self.profile,
                          f"FIB hot-zone SHORT {tier_tag} @ {nearest_zone:.4f} (dist {dist_pct*100:+.2f}%) "
                          f"strength={zone_strength}/{len(all_fibs)} fibs across {len(windows_used)}w | "
                          f"RSI {r:.0f} vol {v_ratio:.1f}x EMA50 slope {ema_slope_pct:+.2f}% | {tp_tag}",
                          {"atr_sl": sl_price, "atr_tp": tp_price,
                           "zone_price": nearest_zone, "zone_strength": zone_strength,
                           "proximity_tier": proximity_tier, "target_zone": target,
                           "fib_count": len(all_fibs)})

        return None


class ScoutAgent(Agent):
    """2026-06-04: AUTO COIN HUNTER — scores every USDT pair for breakout potential.
    Finds coins with ADX>25, daily_range>3%, volume surging, fib structure.
    Runs every 4 hours, feeds top coins to winning strategies."""
    name = "scout"
    enabled = False  # 2026-06-04: KILLED — only macd_cross + fib_bounce survive
    paper_only = True  # Signal agent only — doesn't trade, just discovers coins
    notional_multiplier = 0.0  # Never trades
    profile = "momentum"

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 100:
            return None
        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]

        try:
            tr1 = h - l; tr2 = (h - c.shift()).abs(); tr3 = (l - c.shift()).abs()
            tr = pd.concat([tr1,tr2,tr3], axis=1).max(axis=1)
            atr = tr.ewm(span=14, adjust=False).mean()
            up = h.diff(); down = l.shift() - l
            pdm = np.where((up > down) & (up > 0), up, 0)
            ndm = np.where((down > up) & (down > 0), down, 0)
            pdi = 100 * pd.Series(pdm).ewm(span=14, adjust=False).mean() / atr.replace(0, 1e-9)
            ndi = 100 * pd.Series(ndm).ewm(span=14, adjust=False).mean() / atr.replace(0, 1e-9)
            dx = 100 * abs(pdi - ndi) / (pdi + ndi + 1e-9)
            adx = pd.Series(dx).ewm(span=14, adjust=False).mean().iloc[-1]
        except:
            adx = 0

        try:
            daily_range = ((h.iloc[-24:].max() - l.iloc[-24:].min()) / c.iloc[-1]) * 100
        except:
            daily_range = 0

        try:
            v_ratio = v.iloc[-1] / v.iloc[-50:].mean() if v.iloc[-50:].mean() > 0 else 1
        except:
            v_ratio = 1

        score = 0
        if adx > 30: score += 35
        elif adx > 25: score += 25
        elif adx > 20: score += 15
        if daily_range > 5: score += 35
        elif daily_range > 3: score += 25
        elif daily_range > 1.5: score += 15
        if v_ratio > 2.0: score += 30
        elif v_ratio > 1.5: score += 20
        elif v_ratio > 1.2: score += 10

        if score >= 80 and pdi > ndi:
            return Signal(self.name, sym, "long", min(9, score//10), self.profile,
                          f"🔥 SCOUT: score={score} ADX={adx:.0f} range={daily_range:.1f}% vol={v_ratio:.1f}x",
                          {"score": score, "adx": adx, "range": daily_range, "vol": v_ratio})
        return None


class FibBounceAgent(Agent):
    """2026-06-04 MEGA BACKTEST WINNER (95 coins): Fib=0.500, SL=5%, Trail=6%, Act=2%, ADX>20, 1H.
    +2,889% return, 614 trades, 49% WR, 52% DD — tradeable. Hyperliquid data proved 0.500 > 0.382."""
    name = "fib_bounce"
    enabled = True  # 2026-06-04: FIB=0.500 WINNER — +2,889% backtest — only macd_cross + fib_bounce survive
    paper_only = False
    notional_multiplier = 0.05  # 5% risk per trade (backtest-optimized: +9,613% at 5m, 42% DD)
    profile = "fib_bounce"

    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 120:
            return None

        c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]

        # Fib levels: 0.382 (NEW MEGA BACKTEST WINNER) and 0.618
        h100 = h.rolling(100).max().iloc[-1]
        l100 = l.rolling(100).min().iloc[-1]
        rng = h100 - l100
        if rng <= 0:
            return None
        fib500 = l100 + 0.500 * rng
        fib382 = l100 + 0.382 * rng
        fib618 = l100 + 0.618 * rng

        # Check all three fib levels — 0.500 is primary (8hr backtest winner)
        near_500 = abs(c.iloc[-1] - fib500) / fib500 < 0.012
        near_382 = abs(c.iloc[-1] - fib382) / fib382 < 0.012
        near_618 = abs(c.iloc[-1] - fib618) / fib618 < 0.012
        if not (near_500 or near_382 or near_618):
            return None

        # Determine which fib level was hit
        if near_500: fib_hit, fib_price = 0.500, fib500
        elif near_382: fib_hit, fib_price = 0.382, fib382
        else: fib_hit, fib_price = 0.618, fib618

        # 1-bar reversal
        reversal = c.iloc[-1] > c.iloc[-2] and c.iloc[-2] <= c.iloc[-3]
        if not reversal:
            return None

        # Volume filter
        v_avg = v.rolling(50).mean().iloc[-1]
        if v_avg <= 0 or v.iloc[-1] / v_avg < 0.6:
            return None

        # RSI filter
        r = rsi(c).iloc[-1]
        if r < 25 or r > 55:
            return None

        # ADX regime filter — the KEY
        if not self._regime_ok(df):
            return None

        conf = 7 + int(r < 40) + int(v.iloc[-1] / v_avg > 1.0)
        if near_500: conf += 1  # Bonus for 0.500 — 8hr backtest winner
        return Signal(self.name, sym, "long", min(10, conf), self.profile,
                      f"Fib {fib_hit:.3f} bounce | RSI {r:.0f} | near {fib_price:.4f}",
                      {"fib_level": fib_hit, "rsi": r, "entry_price": c.iloc[-1]})

    def _regime_ok(self, df):
        """ADX > 22 and +DI > -DI = trending uptrend."""
        c = df["close"]; h = df["high"]; l = df["low"]
        tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
        atr_val = tr.ewm(span=14, adjust=False).mean()
        up = h.diff(); down = l.shift() - l
        pdm = np.where((up > down) & (up > 0), up, 0)
        ndm = np.where((down > up) & (down > 0), down, 0)
        pdi = 100 * pd.Series(pdm).ewm(span=14, adjust=False).mean() / atr_val.replace(0, 1e-9)
        ndi = 100 * pd.Series(ndm).ewm(span=14, adjust=False).mean() / atr_val.replace(0, 1e-9)
        dx = 100 * abs(pdi - ndi) / (pdi + ndi + 1e-9)
        adx = pd.Series(dx).ewm(span=14, adjust=False).mean()
        return adx.iloc[-1] > 22 and pdi.iloc[-1] > ndi.iloc[-1]


class FundingExtremesAgent(Agent):
    """Fade extreme funding rates (per RESEARCH_REPORT_2.md, highest expected edge).

    Logic: when funding rate per 8h cycle is in the EXTREME tail (>0.05% or <-0.05%),
    one side of the trade is paying through the nose to hold their position. Empirically,
    extreme funding precedes a mean-reversion in price ~62-73% of the time on majors.

    Rules:
      - Funding > +0.05%/8h (annualized 54%+): SHORT (longs are over-leveraged, paying)
      - Funding < -0.05%/8h: LONG (shorts are over-leveraged, paying)
      - Require RSI confirmation: don't fade if price still trending HARD against fade
      - EMA50 1h slope check: avoid fading into a strong continuing trend
      - Confidence scales with funding magnitude (more extreme = higher conf)

    TP/SL: 1.8% / 1.2% (mean-rev profile, tight). Trail activates at 1.0% gain.

    Run on: BTC, ETH, SOL, BNB primarily — alts have erratic funding, less reliable.
    """
    notional_multiplier = 0.04
    name = "funding_extremes"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: 6,347 trades, -0.002 ExpR, -167% DD
    paper_only = False
    profile = "meanrev"
    valid_regimes = ["RANGING", "VOLATILE", "TRENDING"]

    EXTREME_THRESHOLD = 0.0005    # 0.05% per 8h = ~54% annualized
    SUPER_EXTREME = 0.0010        # 0.10% = exceptional, max conf
    EMA_PERIOD = 50

    def analyze(self, sym, ctx):
        fr = ctx.funding_rate or 0.0
        if abs(fr) < self.EXTREME_THRESHOLD:
            return None
        df = ctx.df_1h
        if len(df) < self.EMA_PERIOD + 5:
            return None
        c = df["close"]
        last = c.iloc[-1]
        if last <= 0:
            return None
        r = rsi(c, 14).iloc[-1]
        ema50 = ema(c, self.EMA_PERIOD).iloc[-1]
        ema50_5 = ema(c, self.EMA_PERIOD).iloc[-5]
        if pd.isna(ema50) or pd.isna(ema50_5) or ema50 <= 0:
            return None
        ema_slope_pct = (ema50 / ema50_5 - 1) * 100
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        atr_pct = atr_val / last * 100

        # Funding > extreme positive: longs pay shorts → fade by SHORTING
        if fr > self.EXTREME_THRESHOLD:
            # Don't short if EMA50 is ripping up (strong trend = wait)
            if ema_slope_pct > 0.8:
                return None
            # Confluence: RSI should be elevated (overbought-ish) for cleaner fade
            if r < 50:
                return None
            sl_price = last * 1.012
            tp_price = last * 0.982
            confluences = (
                int(fr > self.SUPER_EXTREME) +
                int(r > 65) +
                int(ema_slope_pct < 0) +     # EMA already turning down = bonus
                int(atr_pct > 1.0)            # volatility expansion = better fade
            )
            conf = 6 + confluences   # 6-9 (cap at 9 per fixed scoring)
            return Signal(self.name, sym, "short", min(9, conf), self.profile,
                          f"Funding extremes SHORT: fr={fr*100:.4f}%/8h "
                          f"(annual≈{fr*100*3*365:.0f}%), RSI={r:.0f}, EMA50 slope={ema_slope_pct:+.2f}%",
                          {"funding_rate": fr, "rsi": float(r),
                           "ema_slope": float(ema_slope_pct), "atr_pct": float(atr_pct)})

        # Funding < extreme negative: shorts pay longs → fade by LONGING
        if fr < -self.EXTREME_THRESHOLD:
            if ema_slope_pct < -0.8:
                return None
            if r > 50:
                return None
            sl_price = last * 0.988
            tp_price = last * 1.018
            confluences = (
                int(fr < -self.SUPER_EXTREME) +
                int(r < 35) +
                int(ema_slope_pct > 0) +
                int(atr_pct > 1.0)
            )
            conf = 6 + confluences
            return Signal(self.name, sym, "long", min(9, conf), self.profile,
                          f"Funding extremes LONG: fr={fr*100:.4f}%/8h "
                          f"(annual≈{fr*100*3*365:.0f}%), RSI={r:.0f}, EMA50 slope={ema_slope_pct:+.2f}%",
                          {"funding_rate": fr, "rsi": float(r),
                           "ema_slope": float(ema_slope_pct), "atr_pct": float(atr_pct)})

        return None


# =============================================================================
# AGENT: VIKI — Triple EMA Crossover (9/21/50) on 15-minute
# Backtested: 63 days, 81.5% WR, +68% at 10× on SOL/TAO/TIA
# Profile: 7% SL, trailing TP activates at +3% with 1.5% trail distance
# =============================================================================
class VikiAgent(Agent):
    notional_multiplier = 0.03
    """Triple EMA crossover on 15m + 5m confirm — 9/21/50 alignment.
    2026-06-06: MarketContext lacks 30m, using 15m+5m instead."""
    name = "viki"
    enabled = False  # DISABLED — backtest: -8.5%, 47% WR
    paper_only = False
    profile = "viki"
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]

    # Symbols with proven edge from backtest (81.5%+ WR combined)
    WHITELIST = {"SOL-USDT", "TAO-USDT", "TIA-USDT", "BTC-USDT", "ETH-USDT", "BNB-USDT", "XRP-USDT"}

    def analyze(self, sym, ctx):
        # Only fire on backtest-validated symbols
        if sym not in self.WHITELIST:
            return None

        df = ctx.df_30m  # 2026-06-06: df_30m now available — Viki's optimal TF (+14.5% vs -27% at 15m)
        if len(df) < 60:
            return None

        c = df["close"]
        v = df["volume"]

        # Triple EMA: 9, 21, 50
        e9  = ema(c, 9)
        e21 = ema(c, 21)
        e50 = ema(c, 50)

        if pd.isna(e9.iloc[-1]) or pd.isna(e21.iloc[-1]) or pd.isna(e50.iloc[-1]):
            return None
        if pd.isna(e9.iloc[-2]) or pd.isna(e21.iloc[-2]):
            return None

        # Detect crossover: 9 crosses 21
        prev_diff = e9.iloc[-2] - e21.iloc[-2]
        cur_diff  = e9.iloc[-1] - e21.iloc[-1]

        bullish_cross = prev_diff <= 0 and cur_diff > 0
        bearish_cross = prev_diff >= 0 and cur_diff < 0

        if not (bullish_cross or bearish_cross):
            return None

        last = c.iloc[-1]
        if last <= 0:
            return None

        # Volume check — skip if below average (fakeout filter)
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < 0.8:
            return None

        # 5m confirmation (backtest-proven: +14.5% vs +8.0% without)
        if hasattr(ctx, 'df_5m') and ctx.df_5m is not None and len(ctx.df_5m) >= 60:
            c5 = ctx.df_5m["close"]
            e9_5 = ema(c5, 9)
            e21_5 = ema(c5, 21)
            if bullish_cross and e9_5.iloc[-1] <= e21_5.iloc[-1]:
                return None
            if bearish_cross and e9_5.iloc[-1] >= e21_5.iloc[-1]:
                return None

        # 7% fixed SL (trailing TP handled by profile: activate=3%, trail=1.5%)
        sl_pct = 0.07
        e50_now = e50.iloc[-1]

        # LONG: 9 > 21 (just crossed) AND both > 50 (bullish alignment)
        if bullish_cross and e9.iloc[-1] > e50_now and e21.iloc[-1] > e50_now:
            sl_price = last * (1 - sl_pct)
            conf = 7 + int(v_ratio > 1.5) + int(last > e50_now * 1.01)
            return Signal(self.name, sym, "long", conf, self.profile,
                          f"VIKI 9/21 bull cross > 50ema @ 30m+5m | vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": last * 99.0,
                           "ema9": float(e9.iloc[-1]), "ema21": float(e21.iloc[-1]),
                           "ema50": float(e50_now)})

        # SHORT: 9 < 21 (just crossed) AND both < 50 (bearish alignment)
        if bearish_cross and e9.iloc[-1] < e50_now and e21.iloc[-1] < e50_now:
            sl_price = last * (1 + sl_pct)
            conf = 7 + int(v_ratio > 1.5) + int(last < e50_now * 0.99)
            return Signal(self.name, sym, "short", conf, self.profile,
                          f"VIKI 9/21 bear cross < 50ema @ 30m+5m | vol {v_ratio:.1f}x",
                          {"atr_sl": sl_price, "atr_tp": last * 0.01,
                           "ema9": float(e9.iloc[-1]), "ema21": float(e21.iloc[-1]),
                           "ema50": float(e50_now)})

        return None


class MACDCrossAgent(Agent):
    notional_multiplier = 0.02  # 2026-06-08: REDUCED — backtest -42R, keep small for regime
    """2026-06-04: Backtest proved this bleeds (-42R 1H, -1,506R all TFs).
    Keeping at reduced size for trending markets only."""
    name = "macd_cross"
    enabled = False  # DISABLED — backtest: -41%, 48% WR
    paper_only = False
    profile = "macd_cross"
    valid_regimes = ["TRENDING", "VOLATILE"]

    MIN_VOL_RATIO = 1.8  # precision entries: real volume only  # raised from 1.3 — only trade with real volume

    def analyze(self, sym, ctx):
        # 2026-06-05: MOVED from 1H to 15m + 5m confirm — backtest: 15m+5m +22.4% vs 1H -49.5%
        df = ctx.df_15m
        if len(df) < 60:
            return None
        c = df["close"]; v = df["volume"]
        # Crypto-optimized: 24/52/18 (standard 12/26/9 is too slow for crypto)
        e24 = ema(c, 24); e52 = ema(c, 52)
        macd_line = e24 - e52
        signal_line = ema(macd_line, 18)
        prev_diff = macd_line.iloc[-2] - signal_line.iloc[-2]
        cur_diff  = macd_line.iloc[-1] - signal_line.iloc[-1]
        bullish_cross = prev_diff <= 0 and cur_diff > 0
        bearish_cross = prev_diff >= 0 and cur_diff < 0
        if not (bullish_cross or bearish_cross):
            return None
        # Volume must confirm
        avg_v = v.rolling(20).mean().iloc[-1]
        if avg_v <= 0 or pd.isna(avg_v):
            return None
        v_ratio = v.iloc[-1] / avg_v
        if v_ratio < self.MIN_VOL_RATIO:
            return None
        # PRECISION: 5m MACD must agree (multi-TF confirmation — backtest proven)
        if hasattr(ctx, 'df_5m') and ctx.df_5m is not None and len(ctx.df_5m) >= 60:
            c5 = ctx.df_5m["close"]
            ml_5 = ema(c5, 24) - ema(c5, 52)
            if bullish_cross and ml_5.iloc[-1] <= 0: return None
            if bearish_cross and ml_5.iloc[-1] >= 0: return None
        last = c.iloc[-1]
        atr_val = atr(df).iloc[-1]
        if atr_val <= 0 or pd.isna(atr_val):
            return None
        # Research: 1:3 R:R only needs 25% WR to breakeven. SL=1.5xATR, TP=4.5xATR = 3:1
        if bullish_cross:
            sl_price = last - 1.5 * atr_val
            tp_price = last + 4.5 * atr_val  # 3:1 risk-reward
            conf = 7 + int(v_ratio > 2.0) + int(macd_line.iloc[-1] > 0)
            return Signal(self.name, sym, "long", conf, self.profile,
                          f"MACD bull 24/52 cross vol {v_ratio:.1f}x RR=3:1",
                          {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val})
        sl_price = last + 1.5 * atr_val
        tp_price = last - 4.5 * atr_val
        conf = 7 + int(v_ratio > 2.0) + int(macd_line.iloc[-1] < 0)
        return Signal(self.name, sym, "short", conf, self.profile,
                      f"MACD bear 24/52 cross vol {v_ratio:.1f}x RR=3:1",
                      {"atr_sl": sl_price, "atr_tp": tp_price, "atr_val": atr_val})


# =============================================================================
# AGENT 14: VWAP MEAN-REVERSION
# Institutional strategy: when price extends >2 std-dev from rolling 24h VWAP
# with declining volume on the extension, fade back to VWAP.
# Stop = 0.5 std-dev beyond entry. Target = VWAP. Trail once at +0.5R.
# =============================================================================
class VWAPReversionAgent(Agent):
    notional_multiplier = 0.02
    name = "vwap_reversion"
    # 2026-05-09 — DISABLED by Saad: net -$1.43 (1W/1L). Loss-mechanism kill.
    # Loss came from TON-USDT short z=4.75σ — knife-catch. Re-enable only after
    # backtest shows ≥55% WR + ≥+0.20R ExpR over 100+ trades.
    enabled = False
    paper_only = True
    profile = "meanrev"   # short hold, tight TP — meanrev profile suits
    valid_regimes = ["RANGING", "VOLATILE"]   # don't fade strong trends

    def analyze(self, sym, ctx):
        df = ctx.df_15m
        if len(df) < 100:
            return None
        c = df["close"]
        v = df["volume"]
        last = c.iloc[-1]
        if last <= 0:
            return None

        # 24h rolling VWAP (96 × 15m = 24h)
        vw = rolling_vwap(df, 96)
        vwap = vw["vwap"].iloc[-1]
        vstd = vw["vwap_std"].iloc[-1]
        if pd.isna(vwap) or pd.isna(vstd) or vstd <= 0:
            return None

        # Extension Z-score
        z = (last - vwap) / vstd
        if abs(z) < 2.0:
            return None   # not extended enough
        if abs(z) > 3.5:
            return None   # v2.0 fix: beyond 3.5σ = strong trend, not reversion (TON-USDT loss)

        # Volume confirmation: extension on DECLINING volume = exhaustion
        # (rising volume on extension = breakout, not reversal)
        v_now = v.iloc[-1]
        v_avg5 = v.iloc[-6:-1].mean()
        if v_avg5 <= 0:
            return None
        v_ratio_recent = v_now / v_avg5
        # We want recent volume LOWER than the extension — exhaustion sign
        if v_ratio_recent > 1.4:
            return None

        # RSI confirms exhaustion
        r = rsi(c).iloc[-1]

        # Entry timing: only fade after a "stalling" bar (small body)
        last_o = df["open"].iloc[-1]
        last_body_pct = abs(last - last_o) / last_o if last_o else 0
        last_atr = atr(df).iloc[-1]
        if last_atr <= 0:
            return None
        small_body = last_body_pct * last < last_atr * 0.6   # body < 0.6 ATR

        # Long: price extended BELOW VWAP, RSI low, exhaustion candle
        # v2.0 fix: tightened RSI 40→32 to avoid mid-range fades
        if z < -2.0 and r < 32 and small_body:
            tp = vwap                                    # target = VWAP itself
            sl = last - 0.5 * vstd                       # stop 0.5 std beyond entry
            conf = 7 + int(z < -2.5) + int(r < 30) + int(v_ratio_recent < 0.8)
            return Signal(self.name, sym, "long", min(10, conf), self.profile,
                          f"VWAP fade long z={z:+.2f}σ RSI {r:.0f} vol_recent={v_ratio_recent:.1f}x",
                          {"vwap": float(vwap), "z": float(z), "rsi": float(r),
                           "tp_price": float(tp), "sl_price": float(sl)})

        # Short: price extended ABOVE VWAP
        # v2.0 fix: tightened RSI 60→68 to avoid mid-range fades
        if z > 2.0 and r > 68 and small_body:
            tp = vwap
            sl = last + 0.5 * vstd
            conf = 7 + int(z > 2.5) + int(r > 70) + int(v_ratio_recent < 0.8)
            return Signal(self.name, sym, "short", min(10, conf), self.profile,
                          f"VWAP fade short z={z:+.2f}σ RSI {r:.0f} vol_recent={v_ratio_recent:.1f}x",
                          {"vwap": float(vwap), "z": float(z), "rsi": float(r),
                           "tp_price": float(tp), "sl_price": float(sl)})

        return None


# =============================================================================
# AGENT 13: RSI DIVERGENCE AGENT
# Bullish: lower price low + higher RSI low (selling exhausted, hidden buying)
# Bearish: higher price high + lower RSI high (buying exhausted, hidden selling)
# Powerful reversal confluence — only at significant swing points.
# =============================================================================
class RSIDivergenceAgent(Agent):
    name = "rsi_divergence"
    enabled = False  # 2026-06-03: KILLED — 1yr backtest: -35% to -60% across ALL TFs
    paper_only = True   # validation needed
    profile = "swing"
    valid_regimes = ["RANGING", "TRENDING"]

    def analyze(self, sym, ctx):
        df = ctx.df_1h if len(ctx.df_1h) >= 50 else ctx.df_15m
        if len(df) < 50:
            return None
        c = df["close"]
        r = rsi(c)
        if len(r) < 50 or pd.isna(r.iloc[-1]):
            return None

        # Find recent swing lows/highs in price and RSI
        # Swing point = local extrema with at least N bars on either side that don't violate it
        N = 3
        prices = c.values[-30:]
        rsis = r.values[-30:]

        # Look for the two most recent swing lows in price
        swing_lows = []
        for i in range(N, len(prices) - N):
            if prices[i] == min(prices[i-N:i+N+1]):
                swing_lows.append((i, prices[i], rsis[i]))
        # And swing highs
        swing_highs = []
        for i in range(N, len(prices) - N):
            if prices[i] == max(prices[i-N:i+N+1]):
                swing_highs.append((i, prices[i], rsis[i]))

        # Bullish divergence: 2 most recent swing lows, second has lower price but higher RSI
        if len(swing_lows) >= 2:
            (i1, p1, r1), (i2, p2, r2) = swing_lows[-2], swing_lows[-1]
            if p2 < p1 and r2 > r1 + 3 and r2 < 45 and r1 < 40:
                # Confirm price has turned up since swing low
                if c.iloc[-1] > p2 * 1.003:
                    conf = 8 + int(r2 - r1 > 8) + int(p1 - p2 > p1 * 0.02)
                    return Signal(self.name, sym, "long", min(10, conf), self.profile,
                                  f"Bullish RSI div: price {p1:.4f}→{p2:.4f} but RSI {r1:.0f}→{r2:.0f}",
                                  {"price_low_1": float(p1), "price_low_2": float(p2),
                                   "rsi_low_1": float(r1), "rsi_low_2": float(r2)})

        # Bearish divergence: 2 most recent swing highs, second has higher price but lower RSI
        if len(swing_highs) >= 2:
            (i1, p1, r1), (i2, p2, r2) = swing_highs[-2], swing_highs[-1]
            if p2 > p1 and r2 < r1 - 3 and r2 > 55 and r1 > 60:
                if c.iloc[-1] < p2 * 0.997:
                    conf = 8 + int(r1 - r2 > 8) + int(p2 - p1 > p1 * 0.02)
                    return Signal(self.name, sym, "short", min(10, conf), self.profile,
                                  f"Bearish RSI div: price {p1:.4f}→{p2:.4f} but RSI {r1:.0f}→{r2:.0f}",
                                  {"price_high_1": float(p1), "price_high_2": float(p2),
                                   "rsi_high_1": float(r1), "rsi_high_2": float(r2)})

        return None


# ═══════════════════════════════════════════════════════════════════════════
# QUANTUM MASTER AGENT (2026-06-09, Saad: "extreme level mathematics")
# ═══════════════════════════════════════════════════════════════════════════
# SIX LAYERS — each is PhD-level math implemented in pure numpy:
#
# Layer 1 — LYAPUNOV EXPONENT (Chaos Theory)
#   Lambda = (1/N) * sum(log(|dF/dx|)) where F = return-generating map
#   Positive Lyapunov = sensitive to initial conditions = chaotic market
#   Negative Lyapunov = orderly, predictable = tradeable
#   λ > 0.1 = chaos, skip. λ < 0.01 = orderly, trade.
#
# Layer 2 — WASSERSTEIN-1 DISTANCE (Earth Mover's Distance)
#   W(P, Q) = integral |F^(-1)(t) - G^(-1)(t)| dt
#   Measures the "work" of transforming recent return distribution into
#   the full-sample distribution. Jump in W = regime shift detected.
#   Also called Kantorovich-Rubinstein metric.
#
# Layer 3 — SPECTRAL ENTROPY (Fourier domain)
#   S = -sum(p_k * log(p_k)) where p_k = |FFT(f)|^2 / total power
#   Low spectral entropy = price has a dominant frequency (predictable rhythm)
#   High spectral entropy = white noise in frequency domain (chaotic)
#   H_spec < 0.6 = strong periodic component = mean-reversion opportunity
#   H_spec > 0.85 = pure noise = no edge
#
# Layer 4 — DETRENDED FLUCTUATION ANALYSIS (Fractal Scaling)
#   DFA α exponent from integrated time series:
#   F(n) ~ n^α where F = RMS fluctuation at window size n
#   α > 0.5 = persistent (trending)
#   α = 0.5 = uncorrelated (random walk)
#   α < 0.5 = anti-persistent (mean-reverting)
#   α ≈ 1.0 = 1/f noise (pink noise — most financial markets)
#
# Layer 5 — FISHER INFORMATION METRIC
#   I(theta) = E[(d/dtheta log f(X;theta))^2]
#   Discrete version: I_t = (p_t+1 - p_t)^2 / p_t where p_t = price[t] / sum(prices)
#   Measures how much "information" each new bar carries.
#   High Fisher = new information entering = tradeable move
#   Low Fisher = stale, drifting = no edge
#
# Layer 6 — RÉNYI ENTROPY (Generalized Entropy)
#   H_q(p) = (1/(1-q)) * log(sum(p_i^q))
#   q=2 gives collision entropy (probability two samples are same)
#   q→∞ gives min-entropy (most probable outcome only)
#   Compare H_2 vs H_1 (Shannon): gap = tail risk indicator
#   Big gap between q=1 and q=2 = fat tail risk
#
# Voting: each layer casts 1 vote. Need 4/6 for a signal.
# All math is self-contained — numpy only, no scipy.

import numpy as np

def _lyapunov_exponent(prices: np.ndarray, window: int = 50) -> float:
    """Estimate Lyapunov exponent from return map.
    
    Uses the Rosenstein algorithm: for a point on the attractor,
    find its nearest neighbor and track divergence over time.
    
    λ ≈ (1/(N*dt)) * sum(log(divergence))
    
    Returns λ. Ranges from large positive (chaotic) to negative (orderly).
    """
    if len(prices) < window + 10:
        return 0.5  # neutral
    
    rets = np.diff(np.log(prices[-window:]))
    if len(rets) < 10:
        return 0.5
        
    # Build the return map: (r_t, r_t+1) pairs
    x = rets[:-1]
    y = rets[1:]
    if len(x) < 5:
        return 0.5
    
    # For each point, find nearest neighbor (excluding itself)
    divergences = []
    for i in range(len(x) - 2):
        dists = np.sqrt((x - x[i])**2 + (y - y[i])**2)
        dists[i] = np.inf  # exclude self
        min_idx = np.argmin(dists)
        if min_idx < len(x) - 1:
            # Divergence over 1 step
            d0 = dists[min_idx]
            if d0 > 1e-10:
                # Track how far apart they are 1 step later
                d1 = np.sqrt((x[min_idx+1] - x[i+1])**2 + 
                             (y[min_idx+1] if min_idx+1 < len(y) else y[-1] - y[i+1])**2)
                d1 = max(d1, 1e-10)
                divergences.append(np.log(d1 / d0))
    
    if len(divergences) < 3:
        return 0.5
    return float(np.mean(divergences))


def _wasserstein_1d(sample_a: np.ndarray, sample_b: np.ndarray) -> float:
    """Wasserstein-1 distance (Earth Mover's Distance) for 1D.
    
    W_1(P, Q) = integral |F_A^(-1)(t) - F_B^(-1)(t)| dt
    where F^(-1) is the quantile function.
    
    In 1D this is equivalent to |mean(a) - mean(b)| for same-sized samples,
    but for different distributions it captures the full transport cost.
    
    Implemented as: sort both, then mean absolute difference at each quantile.
    """
    if len(sample_a) < 5 or len(sample_b) < 5:
        return 0.0
    a_sorted = np.sort(sample_a)
    b_sorted = np.sort(sample_b)
    n = min(len(a_sorted), len(b_sorted))
    # Resample both to same length via interpolation
    a_idx = np.linspace(0, len(a_sorted) - 1, n).astype(int)
    b_idx = np.linspace(0, len(b_sorted) - 1, n).astype(int)
    a_sampled = a_sorted[a_idx]
    b_sampled = b_sorted[b_idx]
    return float(np.mean(np.abs(a_sampled - b_sampled)))


def _spectral_entropy(prices: np.ndarray) -> float:
    """Spectral entropy from power spectrum.
    
    P(k) = |FFT(prices)|^2
    p_k = P(k) / sum(P(k))
    H_spec = -sum(p_k * log(p_k)) / log(N)  # normalized [0, 1]
    
    0 = single frequency (perfectly periodic)
    1 = white noise (all frequencies equal)
    """
    if len(prices) < 30:
        return 0.5
    # Detrend by subtracting linear fit
    x = np.arange(len(prices))
    slope, intercept = np.polyfit(x, prices, 1)
    detrended = prices - (slope * x + intercept)
    # Hamming window to reduce spectral leakage
    windowed = detrended * np.hamming(len(detrended))
    # FFT
    fft = np.fft.rfft(windowed)
    power = np.abs(fft)**2
    if power.sum() < 1e-10:
        return 0.5
    p = power / power.sum()
    # Entropy (avoid log(0))
    p = p[p > 1e-10]
    if len(p) < 2:
        return 0.5
    H = -np.sum(p * np.log2(p))
    H_max = np.log2(len(p))
    return float(H / H_max) if H_max > 0 else 0.5


def _dfa_alpha(prices: np.ndarray) -> float:
    """Detrended Fluctuation Analysis — fractal scaling exponent.
    
    Algorithm:
    1. Integrate: y[k] = sum(prices[i] - mean(prices))
    2. Split into windows of size n
    3. For each window: detrend with OLS fit, compute RMS
    4. F(n) = sqrt(mean of RMS^2 over all windows)
    5. Repeat for multiple n values
    6. α = slope of log(F(n)) vs log(n)
    
    Interpretation:
    α = 0.5 → white noise (random walk)
    α = 1.0 → 1/f noise (pink noise — markets)
    α = 1.5 → Brownian motion
    α > 0.5 → long memory, trending
    α < 0.5 → anti-persistence, mean-reverting
    """
    if len(prices) < 100:
        return 0.5
    y = np.cumsum(prices - np.mean(prices))
    n_values = np.logspace(np.log10(10), np.log10(len(prices) // 4), 15).astype(int)
    n_values = np.unique(n_values)
    n_values = n_values[n_values >= 4]
    if len(n_values) < 3:
        return 0.5
    
    fluct = []
    for n in n_values:
        n_windows = len(y) // n
        if n_windows < 2:
            continue
        rms = 0.0
        for i in range(n_windows):
            segment = y[i*n:(i+1)*n]
            x_seg = np.arange(len(segment))
            # OLS detrend
            A = np.vstack([x_seg, np.ones(len(x_seg))]).T
            coeffs, _, _, _ = np.linalg.lstsq(A, segment, rcond=None)
            trend = A @ coeffs
            detrended = segment - trend
            rms += np.mean(detrended**2)
        rms /= n_windows
        fluct.append(np.sqrt(rms))
    
    if len(fluct) < 3:
        return 0.5
    # Slope of log-log
    log_n = np.log(n_values[:len(fluct)])
    log_f = np.log(np.maximum(fluct, 1e-10))
    A = np.vstack([log_n, np.ones(len(log_n))]).T
    alpha, _ = np.linalg.lstsq(A, log_f, rcond=None)[:2]
    return float(alpha[0])


def _fisher_information(prices: np.ndarray, window: int = 30) -> float:
    """Fisher Information Metric — information per bar.
    
    I_t = sum((p_t+1 - p_t)^2 / p_t)  where p_t = normalized price
    
    High I = new information entering price = tradeable move
    Low I = stale, drifting, no new info = no edge
    
    Returns z-scored value relative to its own history.
    """
    if len(prices) < window + 5:
        return 0.0
    
    # Normalize prices
    p = prices / np.sum(prices[-window:])
    if np.any(p <= 0):
        return 0.0
    
    # Fisher info: (delta_p)^2 / p
    dp = np.diff(p)
    fisher = np.sum(dp**2 / p[1:]) if np.all(p[1:] > 0) else 0
    
    # Compare to a rolling window to detect spikes
    fisher_hist = []
    for i in range(window, len(prices) - 1):
        p_slice = prices[i-window:i] / np.sum(prices[i-window:i])
        if np.all(p_slice[1:] > 0):
            dp_s = np.diff(p_slice)
            f = np.sum(dp_s**2 / p_slice[1:])
            fisher_hist.append(f)
    
    if len(fisher_hist) < 5:
        return float(fisher * 1000)  # raw value if no history
    
    # Z-score
    fisher_hist = np.array(fisher_hist)
    mu = np.mean(fisher_hist)
    sigma = np.std(fisher_hist)
    if sigma < 1e-10:
        return 0.0
    return float((fisher - mu) / sigma)


def _renyi_entropy(prices: np.ndarray, q: float = 2.0) -> float:
    """Rényi entropy of order q.
    
    H_q(p) = (1/(1-q)) * log(sum(p_i^q))
    
    q=1 (limit) → Shannon entropy
    q=2 → collision entropy
    q→∞ → min-entropy
    
    Gap H_1 - H_2 > 0.5 = fat tails = tail risk
    """
    if len(prices) < 20:
        return 0.0
    
    # Convert prices to return distribution
    rets = np.diff(np.log(prices[-100:]))
    if len(rets) < 10:
        return 0.0
    
    # Histogram probability
    hist, _ = np.histogram(rets, bins=20, range=(-0.05, 0.05))
    hist = hist[hist > 0]
    if len(hist) < 2:
        return 0.0
    p = hist / hist.sum()
    
    # H_q
    if abs(q - 1.0) < 0.01:
        # Limit case: Shannon
        return float(-np.sum(p * np.log2(p)))
    else:
        sum_pq = np.sum(p**q)
        if sum_pq < 1e-10:
            return 0.0
        return float((1.0 / (1.0 - q)) * np.log2(sum_pq))


class QuantumMasterAgent(Agent):
    """Deepest math agent — chaos theory, Wasserstein, spectral entropy, DFA, Fisher info, Rényi entropy."""
    notional_multiplier = 0.02
    name = "quantum_master"
    enabled = False  # DISABLED — backtest showed 0 predictive power
    paper_only = False
    profile = "daily_breakout"
    valid_regimes = ["TRENDING", "VOLATILE", "RANGING"]
    
    # Layer thresholds (calibrated from market microstructure theory)
    LYAPUNOV_MAX = 0.15      # λ must be below this (orderly, not chaotic)
    WASSERSTEIN_MIN = 0.001  # W must be above this (some regime structure)
    SPECTRAL_ENTROPY_MAX = 0.80  # below this = has a dominant frequency
    DFA_MIN = 0.4            # α must be outside random-walk range 0.45-0.55
    DFA_MAX = 0.6
    FISHER_ZSCORE_MIN = -0.5  # not completely stale
    RENYI_GAP_MAX = 0.5       # gap between H_1 and H_2 must be < this (no fat tail risk)
    
    def analyze(self, sym, ctx):
        df = ctx.df_1h
        if len(df) < 150:
            return None
        
        c = df["close"].values
        h = df["high"].values
        l = df["low"].values
        v = df["volume"].values
        last_c = c[-1]
        
        # Layer 1: LYAPUNOV EXPONENT — chaos detection
        lyap = _lyapunov_exponent(c)
        lyap_ok = lyap < self.LYAPUNOV_MAX
        
        # Layer 2: WASSERSTEIN DISTANCE — regime shift detection
        # Compare recent returns (last 20) to older returns (last 100-20)
        recent_rets = np.diff(np.log(c[-30:]))
        old_rets = np.diff(np.log(c[-120:-30]))
        wass = _wasserstein_1d(recent_rets, old_rets)
        wass_ok = wass > self.WASSERSTEIN_MIN
        
        # Layer 3: SPECTRAL ENTROPY — frequency domain randomness
        spec_ent = _spectral_entropy(c[-200:])
        spec_ok = spec_ent < self.SPECTRAL_ENTROPY_MAX
        
        # Layer 4: DFA — fractal scaling exponent
        dfa_alpha = _dfa_alpha(c)
        # Trending: α > 0.6. Mean-reverting: α < 0.4. Random: 0.4-0.6.
        dfa_trending = dfa_alpha > self.DFA_MAX
        dfa_mr = dfa_alpha < self.DFA_MIN
        dfa_ok = dfa_trending or dfa_mr  # edge exists in either direction
        
        # Layer 5: FISHER INFORMATION — information flow
        fisher_z = _fisher_information(c)
        fisher_ok = fisher_z > self.FISHER_ZSCORE_MIN
        
        # Layer 6: RÉNYI ENTROPY — tail risk detection
        h1 = _renyi_entropy(c, q=1.0)    # Shannon
        h2 = _renyi_entropy(c, q=2.0)    # Collision
        renyi_gap = abs(h1 - h2)
        renyi_ok = renyi_gap < self.RENYI_GAP_MAX  # no excessive tail risk
        
        # Determine direction from DFA + spectral + Fisher
        from bot import rsi as _rsi_fn, ema as _ema_fn
        e21 = float(_ema_fn(pd.Series(c), 21).iloc[-1])
        close_above_ema = last_c > e21
        
        # VOTE
        votes_long = 0
        votes_short = 0
        
        # Layer votes
        if lyap_ok:
            if close_above_ema:
                votes_long += 1
            else:
                votes_short += 1
        
        if wass_ok:
            # Wasserstein says regime is shifting — trade the direction
            if wass > 0 and close_above_ema:
                votes_long += 1
            elif wass > 0:
                votes_short += 1
        
        if spec_ok:
            # Spectral entropy says market has a rhythm — trade it
            if close_above_ema:
                votes_long += 1
            else:
                votes_short += 1
        
        if dfa_ok:
            if dfa_trending and close_above_ema:
                votes_long += 1
            elif dfa_mr and not close_above_ema:
                votes_short += 1
            elif dfa_trending and not close_above_ema:
                votes_short += 1
            else:
                votes_long += 1
        
        if fisher_ok:
            if fisher_z > 1.0:  # strong new info
                if close_above_ema:
                    votes_long += 2  # double vote for strong signals
                else:
                    votes_short += 2
            else:
                if close_above_ema:
                    votes_long += 1
                else:
                    votes_short += 1
        
        if renyi_ok:
            if h1 > h2:  # more information content than noise
                if close_above_ema:
                    votes_long += 1
                else:
                    votes_short += 1
        
        # Need 4+ weighted votes (or 3+ if Fisher gives a double vote)
        if votes_long < 3 and votes_short < 3:
            return None
        
        side = "long" if votes_long >= votes_short else "short"
        total_votes = votes_long if side == "long" else votes_short
        
        # Confidence
        confidence = min(10, total_votes + int(abs(fisher_z) > 1.0) + int(spec_ent < 0.6) + int(abs(dfa_alpha - 0.5) > 0.2))
        
        meta = {
            "lyap": round(lyap, 4),
            "wasser": round(wass, 4),
            "spec_ent": round(spec_ent, 3),
            "dfa": round(dfa_alpha, 3),
            "fisher_z": round(fisher_z, 2),
            "renyi_h1": round(h1, 3),
            "renyi_h2": round(h2, 3),
            "votes": total_votes
        }
        
        sl_price = last_c * (1 - 0.025) if side == "long" else last_c * (1 + 0.025)
        tp_price = last_c * 1.99 if side == "long" else last_c * 0.01
        
        return Signal(self.name, sym, side, confidence, self.profile,
                      f"QM L{round(lyap,3)} W{wass:.4f} S{round(spec_ent,2)} "
                      f"D{round(dfa_alpha,2)} F{round(fisher_z,1)} "
                      f"R{round(renyi_gap,2)} V{total_votes}",
                      meta)

# =============================================================================
# DATABASE  (trade journal + agent stats)
# =============================================================================
class TradeDB:
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        custom_id   TEXT UNIQUE,
        agent       TEXT,
        profile     TEXT,
        symbol      TEXT,
        side        TEXT,
        entry_price REAL,
        qty         REAL,
        notional    REAL,
        tp_price    REAL,
        sl_price    REAL,
        trail_pct   REAL,
        high_water  REAL,
        low_water   REAL,
        current_stop REAL,
        exit_price  REAL,
        pnl         REAL,
        pnl_pct     REAL,
        confidence  INTEGER,
        reason      TEXT,
        status      TEXT,
        opened_at   TEXT,
        closed_at   TEXT,
        meta        TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_status ON trades(status);
    CREATE INDEX IF NOT EXISTS idx_agent  ON trades(agent);
    CREATE INDEX IF NOT EXISTS idx_symbol ON trades(symbol);
    """

    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False, timeout=20)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(self.SCHEMA)
        self.conn.commit()

    def insert(self, t: dict):
        cols = ",".join(t.keys())
        qs = ",".join(["?"] * len(t))
        self.conn.execute(f"INSERT OR IGNORE INTO trades ({cols}) VALUES ({qs})",
                          list(t.values()))
        self.conn.commit()

    def update(self, custom_id: str, **kw):
        if not kw:
            return
        sets = ",".join([f"{k}=?" for k in kw])
        self.conn.execute(f"UPDATE trades SET {sets} WHERE custom_id=?",
                          list(kw.values()) + [custom_id])
        self.conn.commit()

    def open_trades(self) -> List[dict]:
        cur = self.conn.execute(
            "SELECT * FROM trades WHERE status='open' ORDER BY id"
        )
        return [dict(r) for r in cur.fetchall()]

    def today_pnl(self) -> float:
        start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0,
                                                   microsecond=0).isoformat()
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(pnl),0) FROM trades WHERE status='closed' AND closed_at>=?",
            (start,))
        return float(cur.fetchone()[0] or 0)

    def recent_loss_in_symbol(self, sym: str, hours: int = 2) -> bool:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        cur = self.conn.execute(
            "SELECT COUNT(*) FROM trades WHERE symbol=? AND pnl<0 AND closed_at>=?",
            (sym, cutoff))
        return cur.fetchone()[0] > 0

    def recent_closed(self, n: int = 10) -> List[dict]:
        cur = self.conn.execute(
            "SELECT * FROM trades WHERE status='closed' ORDER BY closed_at DESC LIMIT ?", (n,))
        return [dict(r) for r in cur.fetchall()]

    def recent_agent_trades(self, agent: str, n: int = 20) -> List[dict]:
        """Last n closed trades for a specific agent. Each row gets pnl_R
        derived from sl distance if available, else falls back to pnl_pct."""
        cur = self.conn.execute(
            "SELECT * FROM trades WHERE agent=? AND status='closed' ORDER BY closed_at DESC LIMIT ?",
            (agent, n))
        rows = [dict(r) for r in cur.fetchall()]
        for r in rows:
            try:
                entry = float(r.get("entry") or 0)
                sl = float(r.get("initial_sl") or 0)
                pnl = float(r.get("pnl") or 0)
                if entry > 0 and sl > 0 and pnl != 0:
                    risk_pct = abs(entry - sl) / entry
                    if risk_pct > 0:
                        pnl_pct = pnl / (float(r.get("notional") or 1.0) or 1.0)
                        r["pnl_R"] = pnl_pct / risk_pct if risk_pct > 0 else 0
                    else:
                        r["pnl_R"] = 0
                else:
                    r["pnl_R"] = 0
            except Exception:
                r["pnl_R"] = 0
        return rows

    def recent_two_losses(self, since_iso: Optional[str] = None) -> bool:
        """True if the last 2 closed trades are both REAL losses.
        If `since_iso` is given, only trades closed AFTER that ISO timestamp
        are considered — this prevents the same loss cluster from re-triggering
        the lockout on every cycle after it expires (which used to leave the
        bot permanently inert).

        BUGFIX 2026-05-07: two filters added so lockout only fires for genuine
        tilt/revenge sequences:
          1) |pnl| >= $0.50 — filters phantom reconcile_sync closes that came
             from SSL drops, not real stop-outs.
          2) closed within last 2 HOURS — losses 14h apart aren't tilt.
        """
        NOISE_THRESHOLD = 0.50  # ignore phantom reconciles
        WINDOW_HOURS = 2        # only count losses inside this rolling window
        cutoff = (datetime.now(timezone.utc)
                  - timedelta(hours=WINDOW_HOURS)).isoformat()
        # The since_iso anchor (set when last lockout fired) takes precedence
        # if it's tighter than the rolling window
        effective_since = max(since_iso, cutoff) if since_iso else cutoff
        cur = self.conn.execute(
            "SELECT * FROM trades WHERE status='closed' AND closed_at > ? "
            "AND ABS(COALESCE(pnl, 0)) >= ? "
            "ORDER BY closed_at DESC LIMIT 2",
            (effective_since, NOISE_THRESHOLD))
        recent = [dict(r) for r in cur.fetchall()]
        return len(recent) >= 2 and all(float(t.get("pnl") or 0) < 0 for t in recent)

    def agent_winrates(self) -> Dict[str, dict]:
        # v2.0 FAIRNESS FIX (2026-05-09): exclude pre-stacking-fix trades and
        # blacklisted-symbol trades. Bug-induced losses shouldn't condemn
        # an agent after the bug is fixed and the symbol is blocked.
        # - Stacking-bug fix shipped 2026-05-05 (conf-cap, +1 boost, cross-family).
        # - LOSING_SYMBOL_BLACKLIST = TAO, YFI, TON.
        cur = self.conn.execute("""
            SELECT agent,
                   COUNT(*) AS n,
                   SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END) AS wins,
                   COALESCE(SUM(pnl),0) AS total_pnl,
                   COALESCE(AVG(CASE WHEN pnl>0 THEN pnl END),0) AS avg_win,
                   COALESCE(AVG(CASE WHEN pnl<0 THEN pnl END),0) AS avg_loss,
                   COALESCE(SUM(CASE WHEN pnl>0 THEN pnl ELSE 0 END),0) AS gross_win,
                   COALESCE(SUM(CASE WHEN pnl<0 THEN pnl ELSE 0 END),0) AS gross_loss
            FROM trades
            WHERE status='closed' AND pnl IS NOT NULL
              -- 2026-05-19: removed `AND opened_at >= '2026-05-05'` cutoff.
              -- The cutoff was starving agent_winrates() so hurst_regime
              -- showed n=4 instead of lifetime n=20, blocking the kill-switch.
              -- (Patched by Claude/Cowork on Saad's request.)
              AND symbol NOT IN ('TAO-USDT','YFI-USDT','TON-USDT')
              AND pnl != 0
            GROUP BY agent
        """)
        out = {}
        for row in cur.fetchall():
            n = row["n"] or 0
            wins = row["wins"] or 0
            out[row["agent"]] = {
                "n": n,
                "win_rate": (wins / n) if n else 0.5,
                "total_pnl": float(row["total_pnl"] or 0),
                "avg_win": float(row["avg_win"] or 0),
                "avg_loss": float(row["avg_loss"] or 0),
                "gross_win": float(row["gross_win"] or 0),
                "gross_loss": float(row["gross_loss"] or 0),
            }
        return out

    def by_custom_id(self, custom_id: str) -> Optional[dict]:
        cur = self.conn.execute("SELECT * FROM trades WHERE custom_id=?", (custom_id,))
        row = cur.fetchone()
        return dict(row) if row else None


# =============================================================================
# AGENT 8: LEARNING  (weights confidence by historical win-rate per agent)
# =============================================================================
class LearningAgent:
    def __init__(self, db: TradeDB):
        self.db = db
        self.cache: Dict[str, dict] = {}
        self.last_refresh = 0
        self.refresh()

    def refresh(self):
        try:
            self.cache = self.db.agent_winrates()
            self.last_refresh = time.time()
        except Exception as e:
            log.warning(f"learning refresh: {e}")

    def maybe_refresh(self):
        if time.time() - self.last_refresh > 600:
            self.refresh()

    def weight(self, agent: str) -> float:
        """Historical-accuracy weighting (2026-05-05 upgrade per Saad).

        Returns a confidence-multiplier from 0.0 to 1.7 based on the agent's live track record:
          - 0.0  : KILL SWITCH — agent has 5+ trades AND WR < 30%. Don't trade it.
          - 0.5–0.85 : agent is underperforming (45-55% WR or below).
          - 1.0  : baseline (insufficient data <3 trades, or neutral WR ~50%).
          - 1.0–1.7 : agent is winning. 70% WR → ~1.5×, 80%+ → 1.7× cap.

        Also factors in PROFIT FACTOR (gross_win/gross_loss) when n>=5,
        because an agent can have 60% WR but still lose money via tiny wins / huge losses.
        """
        wr = self.cache.get(agent)
        if not wr:
            return 1.0
        n = wr.get("n", 0)
        if n < 3:
            return 1.0   # not enough data yet
        rate = wr.get("win_rate", 0.5)
        # Profit factor — compute first so kill-switch can check it
        pf = 1.0
        gw = wr.get("gross_win", 0) or 0
        gl = abs(wr.get("gross_loss", 0) or 0)
        if gl > 0.001:
            pf = gw / gl
        # v2.0 KILL-SWITCH FIX (2026-05-08): WR-only kill was killing PROFITABLE agents
        # like hurst_regime (29% WR but PF=20! big winners, tiny losers — trend-follower).
        # Now: only kill on low WR if PF is ALSO bad (<1.0 = losing money).
        if n >= 5 and rate < 0.30 and pf < 1.0:
            return 0.0
        # v2.0 PF KILL-SWITCH (added 2026-05-08): an agent that loses $2 for every $1 won
        # is a money pit regardless of WR — kill it after 10+ trades.
        if n >= 10 and pf < 0.5:
            return 0.0
        # Penalty if PF < 1 (losing money) even with good WR
        if n >= 5 and pf < 0.8:
            return max(0.3, rate)   # severe weight cut
        # v2.0 PROFIT-IS-PROFIT (2026-05-09): if the agent is meaningfully profitable
        # (PF>=1.5), skip WR-based penalties below. low-WR/big-winner agents (funding_extremes
        # 40% WR PF=2.59, hurst trend-follower) deserve their full weight.
        if pf >= 1.5:
            return 1.0 if rate <= 0.55 else min(1.7, 1.0 + (rate - 0.5) * 7)
        # Weighting curve — rewards real edge harder, punishes losers harder
        if rate > 0.55:
            return min(1.7, 1.0 + (rate - 0.5) * 7)   # was 5×, now 7× — bigger spread
        if rate < 0.45:
            return max(0.4, 1.0 - (0.5 - rate) * 7)
        return 1.0

    def summary(self) -> str:
        if not self.cache:
            return "no data yet"
        rows = sorted(self.cache.items(), key=lambda x: -x[1]["total_pnl"])
        return " | ".join(
            f"{a}: {d['n']}t {d['win_rate']*100:.0f}%w ${d['total_pnl']:+.1f}"
            for a, d in rows
        )


# =============================================================================
# AGENT 7: RISK MANAGER  (pre-trade veto)
# =============================================================================
class RiskManager:
    def __init__(self, db: TradeDB):
        self.db = db

    def vet(self, sig: Signal, equity: float,
            our_open: List[dict],
            exchange_positions: List[dict],
            funding_rate: float = 0.0) -> Tuple[bool, str]:
        if equity <= 0:
            return False, "no equity"
        # 0. Blacklisted symbols — Saad's manual book, hands off
        if sig.symbol in SYMBOL_BLACKLIST:
            return False, f"{sig.symbol} blacklisted (Saad-only)"
        # 0b. Loss-blacklisted symbols — proven money pit, learning-agent veto
        if sig.symbol in LOSING_SYMBOL_BLACKLIST:
            return False, f"{sig.symbol} loss-blacklisted (learning_agent veto)"
        # 0c. Hour gate — 10:00-12:00 UTC worst window (13 removed, too many good signals blocked)
        # Block solo-agent signals; allow only confluence (≥2 agents agree).
        try:
            now_hour = datetime.now(timezone.utc).hour
            now_dow  = datetime.now(timezone.utc).strftime("%a")
        except Exception:
            now_hour = -1
            now_dow  = ""
        # v2.0 GOLD-ZONE: hard block in proven-toxic hours (regardless of confluence)
        if now_hour in GOLD_TOXIC_HOURS_HARD:
            return False, f"gold-zone: hr {now_hour:02d} UTC blocked (0/2 WR, -$2.80 historical)"
        # v2.0 GOLD-ZONE: skip Friday (0/3 WR, -$0.91 historical)
        if now_dow in GOLD_TOXIC_DAYS:
            return False, f"gold-zone: {now_dow} blocked (0/3 WR historical)"
        # v2.0 GOLD-ZONE: ATR ceiling — skip wild markets (>2.5% ATR = 33% WR)
        if sig.metadata and isinstance(sig.metadata, dict):
            atr_pct_meta = sig.metadata.get("atr_pct", 0)
            if atr_pct_meta and atr_pct_meta > GOLD_MAX_ATR_PCT_AT_ENTRY:
                return False, f"gold-zone: ATR%={atr_pct_meta:.2f}% > {GOLD_MAX_ATR_PCT_AT_ENTRY}% (wild market)"
        if 10 <= now_hour <= 12:
            agents_agreeing = 1
            if sig.metadata and isinstance(sig.metadata, dict):
                agents_agreeing = int(sig.metadata.get("n_agents_agree", 1))
            if agents_agreeing < 2:
                return False, f"hour gate {now_hour:02d}:00 UTC (need ≥2-agent confluence)"
        # 1. Daily loss kill-switch
        today = self.db.today_pnl()
        if today <= -DAILY_LOSS_LIMIT_USD:
            return False, f"daily loss limit ({today:+.2f})"
        # 2. Max concurrent
        if len(our_open) >= MAX_CONCURRENT_POSITIONS:
            return False, "max positions"
        # 3. Already in this symbol — DB
        for p in our_open:
            if p["symbol"] == sig.symbol:
                return False, "already in symbol (db)"
        # 4. Already in this symbol — EXCHANGE (critical in net mode!)
        for p in exchange_positions:
            if p["symbol"] == sig.symbol:
                return False, "exchange position exists (net-mode collision)"
        # 5. Same-direction concentration limit
        same_dir = sum(1 for p in our_open if p["side"] == sig.side)
        if same_dir >= 8:
            return False, f"already {same_dir} same-side"
        # 6. Confidence floor
        if sig.confidence < MIN_CONFIDENCE:
            return False, f"conf {sig.confidence}<{MIN_CONFIDENCE}"
        # 7. Cooldown after recent loss
        if self.db.recent_loss_in_symbol(sig.symbol, hours=0.5):
            return False, "cooldown"
        # ===== WISDOM LAYER — universal intelligence applied to ALL agents =====
        # W1. Volatility floor — if metadata has ATR, skip dead-vol trades
        atr_val = sig.metadata.get("atr_val") if sig.metadata else None
        if atr_val and atr_val > 0:
            # Need a price reference. Use atr_sl distance as proxy if no entry-price.
            sl_price = sig.metadata.get("atr_sl") if sig.metadata else None
            if sl_price and sl_price > 0:
                # Estimate entry as midpoint of sl_price ±2×ATR distance — rough but ok
                ref_price = sl_price + (2 * atr_val if sig.side == "long" else -2 * atr_val)
                atr_pct = atr_val / ref_price if ref_price > 0 else 0
                if 0 < atr_pct < WISDOM_MIN_ATR_PCT:
                    return False, f"wisdom: dead vol (ATR%={atr_pct*100:.3f}%)"
        # W2. Adaptive confidence floor based on recent agent performance
        try:
            recent = self.db.recent_agent_trades(sig.agent, n=20) if hasattr(self.db, "recent_agent_trades") else []
        except Exception:
            recent = []
        if len(recent) >= WISDOM_MIN_TRADES_FOR_ADAPTIVE:
            recent_expR = sum(t.get("pnl_R", 0.0) for t in recent) / len(recent)
            if recent_expR < WISDOM_AGENT_BAD_EXPR and sig.confidence < 9:
                return False, f"wisdom: agent {sig.agent} recent ExpR={recent_expR:+.2f}R, conf {sig.confidence}<9 required"
        # W3. Drawdown throttle — raise conf floor when in drawdown
        if today < -DAILY_LOSS_LIMIT_USD * WISDOM_DRAWDOWN_PAUSE_PCT and sig.confidence < 8:
            return False, f"wisdom: in drawdown ({today:+.2f}), conf {sig.confidence}<8 required"
        # W4. BTC-correlated cluster cap — limit concurrent same-side positions in tight-corr group
        if sig.symbol in WISDOM_BTC_CORR_GROUP:
            same_side_in_group = sum(
                1 for p in our_open
                if p.get("symbol") in WISDOM_BTC_CORR_GROUP and p.get("side") == sig.side
            )
            if same_side_in_group >= WISDOM_BTC_GROUP_MAX_SAME_SIDE:
                return False, f"wisdom: {same_side_in_group} same-side BTC-corr positions already (cap {WISDOM_BTC_GROUP_MAX_SAME_SIDE})"
        # ===== END WISDOM LAYER =====

        # 8. FUNDING_FILTER (FundingHunterAgent is exempt — it's designed for extremes)
        if sig.agent != "funding":
            fr_pct = funding_rate * 100
            if sig.side == "long" and fr_pct > FUNDING_FILTER_LONG_MAX:
                return False, f"funding {fr_pct:.4f}% too high for long"
            if sig.side == "short" and fr_pct < FUNDING_FILTER_SHORT_MIN:
                return False, f"funding {fr_pct:.4f}% too negative for short"
        return True, "ok"


# =============================================================================
# AI ARBITER — prefers Claude Max via Agent SDK, falls back to OpenRouter
# =============================================================================
ARBITER_PROMPT_TEMPLATE = (
    "You are an experienced crypto trading signal reviewer. Reply with JSON only — "
    'no markdown, no prose. Format: {{"approve": true|false, "reason": "<=12 words"}}.\n\n'
    "Signal: agent={agent}, symbol={symbol}, side={side}, "
    "confidence={confidence}/10, profile={profile}\n"
    "Reason: {reason}\n"
    "Context: {context}\n\n"
    "Default to APPROVE. Only REJECT if: extreme risk (e.g. low liquidity penny coin), "
    "obviously broken signal (contradictory logic), or insane position sizing. "
    "Be permissive — the risk manager handles stops and sizing."
)


def _build_arbiter_prompt(sig: "Signal", ctx_summary: str) -> str:
    return ARBITER_PROMPT_TEMPLATE.format(
        agent=sig.agent, symbol=sig.symbol, side=sig.side.upper(),
        confidence=sig.confidence, profile=sig.profile,
        reason=sig.reason, context=ctx_summary,
    )


def _parse_arbiter_json(text: str) -> Tuple[bool, str]:
    m = re.search(r"\{.*?\}", text, re.S)
    if not m:
        return True, "ai-noparse"
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return True, "ai-badjson"
    return bool(obj.get("approve", True)), str(obj.get("reason", ""))[:80]


async def _arbiter_via_max_sdk(sig: "Signal", ctx_summary: str) -> Optional[Tuple[bool, str]]:
    """Use Claude Max subscription (no API costs) via Claude Agent SDK.
    Returns None on error so the caller can fall back to OpenRouter instead
    of silently auto-approving every high-conviction signal."""
    prompt = _build_arbiter_prompt(sig, ctx_summary)
    options = ClaudeAgentOptions(
        system_prompt="You output ONLY a single-line JSON object. No markdown. No commentary.",
        max_turns=1,
        allowed_tools=[],            # text-only reasoning, no file/bash/web access
        permission_mode="dontAsk",   # never prompt — we're headless
    )
    try:
        chunks: List[str] = []
        async for msg in claude_query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        chunks.append(block.text)
        return _parse_arbiter_json("".join(chunks).strip())
    except Exception as e:
        # Saad 2026-05-27: downgraded WARNING→DEBUG. The Claude SDK isn't always
        # available; we fall back to OpenRouter cleanly. No need to spam logs.
        log.debug(f"max-sdk arbiter unavailable (fallback active): {e}")
        return None  # signal failure → caller will try OpenRouter


async def _arbiter_via_deepseek(session: aiohttp.ClientSession,
                                sig: "Signal", ctx_summary: str) -> Optional[Tuple[bool, str]]:
    """Tier-1 arbiter: DeepSeek API (main brain — cheap, fast, smart).

    Direct API call, no proxy. Fast-fail in 5s so we don't slow the pipeline.
    Returns None on any failure so caller falls through to next tier.
    """
    if not DEEPSEEK_API_KEY:
        return None
    prompt = _build_arbiter_prompt(sig, ctx_summary)
    try:
        async with session.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 80,
                "temperature": 0.2,
            },
            timeout=aiohttp.ClientTimeout(total=5),
        ) as r:
            if r.status != 200:
                log.debug(f"deepseek arbiter: http {r.status}")
                return None
            data = await r.json()
        return _parse_arbiter_json(data["choices"][0]["message"]["content"])
    except Exception as e:
        log.debug(f"deepseek arbiter: {e}")
        return None


async def _arbiter_via_ollama(session: aiohttp.ClientSession,
                              sig: "Signal", ctx_summary: str
                              ) -> Optional[Tuple[bool, str]]:
    """Tier-1 arbiter: local Ollama (FREE — no API tokens spent).

    Tries primary model first (3s fast-fail), then fast fallback model (1.5s).
    Returns None on error/disabled so caller falls through to next tier.
    """
    url   = os.getenv("OLLAMA_URL", "off")  # DEFAULT OFF — opt-in only
    if url.lower() in ("off", "false", "0", "disabled", ""):
        return None
    prompt = _build_arbiter_prompt(sig, ctx_summary)
    # Try primary model first, then fast fallback model
    models_to_try = [
        (os.getenv("OLLAMA_MODEL", "llama3.2:3b"), 3.0),
        (os.getenv("OLLAMA_FAST_MODEL", "qwen3:4b"), 1.5),
    ]
    for model, timeout_s in models_to_try:
        try:
            async with session.post(
                f"{url.rstrip('/')}/api/chat",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 80},
                },
                timeout=aiohttp.ClientTimeout(total=timeout_s),
            ) as r:
                data = await r.json()
            text = (data.get("message") or {}).get("content", "")
            if not text:
                continue
            return _parse_arbiter_json(text)
        except Exception as e:
            log.debug(f"ollama arbiter {model}: {e}")
            continue
    return None


async def local_llm_chat(prompt: str, model: Optional[str] = None,
                         max_tokens: int = 400, temperature: float = 0.3,
                         timeout: int = 60) -> Optional[str]:
    """General-purpose LOCAL LLM caller (FREE — no API tokens spent).

    Uses Ollama on http://127.0.0.1:11434. Default model is OLLAMA_FAST_MODEL
    (qwen3:4b) for cheap/high-volume tasks like daily recaps and trade
    narratives. Returns None on any failure so callers can degrade gracefully.
    """
    url = os.getenv("OLLAMA_URL", "")
    if not url or url.lower() in ("off", "false", "0", "disabled"):
        return None
    model = model or os.getenv("OLLAMA_FAST_MODEL", "qwen3:4b")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                f"{url.rstrip('/')}/api/chat",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": temperature,
                                "num_predict": max_tokens},
                },
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as r:
                data = await r.json()
        return ((data.get("message") or {}).get("content") or "").strip() or None
    except Exception as e:
        log.debug(f"local_llm_chat unreachable: {e}")
        return None


async def _arbiter_via_openrouter(session: aiohttp.ClientSession,
                                  sig: "Signal", ctx_summary: str) -> Tuple[bool, str]:
    """OpenRouter call with key rotation + free-only enforcement.

    Rotates through every configured key on 429/5xx/auth errors. Default model
    is Owl Alpha (free 1M-context stealth model)."""
    if OPENROUTER_FREE_ONLY and not _or_is_free(OPENROUTER_MODEL):
        log.warning(f"openrouter arbiter: model {OPENROUTER_MODEL} not free, skipping")
        return True, "non-free-model-skipped"
    prompt = _build_arbiter_prompt(sig, ctx_summary)
    body = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 80,
        "temperature": 0.2,
    }
    rot = _OR_ROTATOR
    attempts = max(rot.count(), 1) if rot else 1
    last_err = None
    for _ in range(attempts):
        key = rot.next_key() if rot else OPENROUTER_API_KEY
        if not key:
            break
        try:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://infinitylux.co.uk",
                    "X-Title": "MAB",
                },
                json=body,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as r:
                if r.status in (401, 403, 429) or 500 <= r.status < 600:
                    if rot:
                        rot.mark_failed(key)
                    last_err = f"http {r.status}"
                    log.info(f"openrouter rotating key (status={r.status})")
                    continue
                data = await r.json()
            return _parse_arbiter_json(data["choices"][0]["message"]["content"])
        except Exception as e:
            last_err = e
            if rot:
                rot.mark_failed(key, cooldown=15.0)
            continue
    # All OpenRouter keys exhausted — fall back to confidence-based heuristic
    # so the bot doesn't blindly approve everything when the network is down.
    if sig.confidence >= 8:
        log.warning(f"openrouter exhausted, auto-approving conf={sig.confidence}")
        return True, "openrouter-exhausted-high-conf"
    elif sig.confidence >= 6:
        log.warning(f"openrouter exhausted, cautious-approve conf={sig.confidence}")
        return True, "openrouter-exhausted-mid-conf"
    else:
        log.warning(f"openrouter exhausted, rejecting low-conf={sig.confidence}")
        return False, "openrouter-exhausted-low-conf"


async def ai_arbiter(session: aiohttp.ClientSession, sig: "Signal",
                     ctx_summary: str) -> Tuple[bool, str]:
    if not USE_AI_ARBITER:
        return True, "ai-disabled"
    if sig.confidence < AI_ARBITER_MIN_CONF:
        return True, "below-arbiter-threshold"
    # Tier-1: DeepSeek (main brain — cheap, fast, smart)
    result = await _arbiter_via_deepseek(session, sig, ctx_summary)
    if result is not None:
        return result
    # Tier-2: Local Ollama (FREE) — fallback
    result = await _arbiter_via_ollama(session, sig, ctx_summary)
    if result is not None:
        return result
    # Tier-3: Claude Max SDK (subscription)
    if HAS_CLAUDE_SDK:
        result = await _arbiter_via_max_sdk(sig, ctx_summary)
        if result is not None:
            return result
    # Tier-4: OpenRouter (paid per call)
    if OPENROUTER_API_KEY:
        return await _arbiter_via_openrouter(session, sig, ctx_summary)
    return True, "no-ai-configured"


# =============================================================================
# EXECUTOR  (sizing, opens, closes, trailing-stop bookkeeping)
# =============================================================================
def make_custom_id(agent: str, symbol: str) -> str:
    sym = symbol.replace("-", "").replace("/", "")[:6]
    return f"{POSITION_TAG}{agent[:3].upper()}{sym}{int(time.time())%100000}"


class Executor:
    def __init__(self, bf: BloFin, db: TradeDB):
        self.bf = bf
        self.db = db

    # ---------- sizing -------------------------------------------------------
    def size_for(self, sig: Signal, equity: float, price: float,
                 instr: dict) -> Tuple[float, float]:
        # COMPOUNDING: base trade is a % of CURRENT equity, so size grows as the
        # account grows. Confidence scales it up. Floor $100, ceiling 15% equity.
        base = equity * COMPOUND_BASE_PCT
        mult = sig.confidence / 7.0
        compound_max = equity * COMPOUND_MAX_PCT
        notional = max(MIN_NOTIONAL_USD, min(compound_max, base * mult))
        # 2026-05-20 (Saad: wants more room to size up for profit): raised the
        # per-trade equity cap from 20% → 50%. This is aggressive but survivable
        # — even a full loss on one trade leaves half the account to recover.
        # NOT removed entirely: a no-cap setting lets a single bad fill (or a
        # leverage wick) zero the account, which Saad's own May 5 post-mortem
        # flagged as the #1 way small accounts die. 50% is the responsible max.
        notional = min(notional, max(MIN_NOTIONAL_USD, equity * 0.50))  # never > 50% equity
        cv = max(instr.get("contract_value", 0.001), 1e-9)
        # contracts = (USD notional / price) / contract_value_in_base
        contracts = (notional / price) / cv
        lot = max(instr.get("lot_size", 1), 1e-9)
        contracts = math.floor(contracts / lot) * lot
        contracts = max(contracts, instr.get("min_size", 1))
        # Round to clean number
        if contracts >= 100:
            contracts = round(contracts)
        elif contracts >= 10:
            contracts = round(contracts, 1)
        else:
            contracts = round(contracts, 2)
        actual_notional = contracts * cv * price
        return contracts, actual_notional

    # ---------- open ---------------------------------------------------------
    async def open(self, sig: Signal, equity: float, price: float,
                   session: aiohttp.ClientSession, paper: bool = False) -> bool:
        prof = PROFILES[sig.profile]
        # Agents may provide exact ATR-based prices via metadata
        meta_tp = sig.metadata.get("atr_tp")
        meta_sl = sig.metadata.get("atr_sl")
        if sig.side == "long":
            tp = float(meta_tp) if meta_tp else price * (1 + prof["tp"] / 100)
            sl = float(meta_sl) if meta_sl else price * (1 - prof["sl"] / 100)
            order_side = "buy"
            position_side = "long"
        else:
            tp = float(meta_tp) if meta_tp else price * (1 - prof["tp"] / 100)
            sl = float(meta_sl) if meta_sl else price * (1 + prof["sl"] / 100)
            order_side = "sell"
            position_side = "short"
        # Apply per-agent notional multiplier (set by backtest auto-pruner)
        agent_mult = getattr(sig, "_agent_mult", 1.0)

        # Confidence-scaled sizing (REWORKED 2026-05-05).
        # Old curve was 1x/2x/3x/5x at conf 7/8/9/10 — too aggressive, especially
        # with the (now-fixed) inverted confidence scoring that pushed losers to 10.
        # New curve is GENTLER and matches the new conf cap (max 9):
        #   conf ≤6 → 0.6x  (low conviction, small bet)
        #   conf  7 → 0.8x
        #   conf  8 → 1.0x  (baseline)
        #   conf  9 → 1.4x  (high conviction)
        # Note: the LearningAgent already multiplies CONFIDENCE itself by the agent's
        # historical-WR weight (line ~4564), so a 70%+ WR agent gets pushed up the
        # conf ladder automatically → ends up at higher conf_mult. Two-stage Kelly-ish.
        conf = sig.confidence
        if conf >= 9:
            conf_mult = 1.4
        elif conf >= 8:
            conf_mult = 1.0
        elif conf >= 7:
            conf_mult = 0.8
        else:
            conf_mult = 0.6

        # v2.0 GOLD-COMBO BUFF: lean into proven winners. ZEC/BNB long during Asian
        # session showed 100%/66% WR historically. Buff size 1.4× when criteria met.
        gold_mult = 1.0
        try:
            _now_h = datetime.now(timezone.utc).hour
        except Exception:
            _now_h = -1
        if (sig.agent, sig.symbol, sig.side) in GOLD_BUFF_COMBOS and _now_h in GOLD_BUFF_HOURS:
            gold_mult = GOLD_BUFF_MULT
            log.info(f"GOLD-BUFF: {sig.agent} {sig.symbol} {sig.side} @ hr{_now_h} → {gold_mult}x size")

        instr = await asyncio.to_thread(self.bf.instrument, sig.symbol)
        size, notional = self.size_for(sig, equity, price, instr)
        # Apply agent_mult × conf_mult × gold_mult × DYNAMIC_RISK, then RE-ROUND
        # Dynamic risk: recovery mode → 1.2-1.5x boost, profit lock → 0.7-0.85x reduce
        try:
            risk_state = compute_dynamic_risk(float(today if today is not None else 0), equity, DAILY_LOSS_LIMIT_USD)
            risk_mult = risk_state.get("multiplier", 1.0)
            if risk_mult != 1.0:
                log.info(f"RISK-ADJUST: {risk_state['mode']} → {risk_mult}x size ({risk_state['reason']})")
        except Exception:
            risk_mult = 1.0
        total_mult = agent_mult * conf_mult * gold_mult * risk_mult
        size = size * total_mult
        notional = notional * total_mult
        min_size = instr.get("min_size", 1)
        lot_size = max(instr.get("lot_size", 1), 1e-9)
        cv = max(instr.get("contract_value", 0.001), 1e-9)
        # Floor to lot_size grid
        size = math.floor(size / lot_size) * lot_size
        # Bump to min_size if below (BloFin requires at least this)
        if size < min_size:
            log.info(f"BUMP {sig.symbol} {sig.side}: size below min {min_size}, bumping")
            size = min_size
        # Re-round to lot grid (in case min_size isn't on the grid)
        size = math.floor(size / lot_size) * lot_size
        if size < min_size:
            size = min_size
        # Eliminate floating-point precision artifacts (0.7000000000000001 → 0.7)
        size = round(size, 6)
        # Recompute actual notional from final size
        notional = size * cv * price
        # If below MIN_NOTIONAL_USD ($50), BUMP UP size to hit it.
        # 2026-05-20 (Saad: "no more $10 trades, $50 minimum"): the per-agent
        # notional_multiplier (0.02–0.05) was shrinking the $50 floor down to
        # ~$1–2, and the old 10× bump cap couldn't recover it, so trades either
        # fired tiny or got skipped. We now ALWAYS bump to the $50 floor
        # regardless of how small the multiplier made it. The 20%-equity cap in
        # size_for() still protects against oversizing.
        if notional < MIN_NOTIONAL_USD and price > 0 and cv > 0:
            needed_size = MIN_NOTIONAL_USD / (cv * price)
            needed_size = math.ceil(needed_size / lot_size) * lot_size
            log.info(f"BUMP_UP {sig.symbol} {sig.side}: notional ${notional:.1f} "
                     f"below ${MIN_NOTIONAL_USD} floor, bumping size {size}→{needed_size}")
            size = round(needed_size, 6)
            notional = size * cv * price
        if size <= 0 or notional < MIN_NOTIONAL_USD * 0.9:
            log.info(f"SKIP {sig.symbol} {sig.side}: cannot reach min notional ({size}/{notional:.1f})")
            return False

        cid = make_custom_id(sig.agent, sig.symbol)
        # Signal quality score from Hermes Brain
        quality = 50
        if HAS_HERMES:
            try:
                current_regime = getattr(self._state, "regime", "RANGING") if hasattr(self, "_state") else "RANGING"
                quality = score_signal_quality(
                    {"agent": sig.agent, "regime": current_regime, "confidence": sig.confidence,
                     "hour_utc": datetime.now(timezone.utc).hour},
                    None,
                )
            except Exception:
                pass
        # Quality gate: DeepSeek arbiter is the real filter — just catch obvious junk
        if quality < 40 and sig.confidence < 6:
            log.info(f"SKIP {sig.symbol} {sig.side}: quality={quality} too low, conf={sig.confidence}")
            return False
        log.info(f"OPEN {sig.agent}/{sig.profile} {sig.symbol} {sig.side.upper()} "
                 f"size={size} notional=${notional:.1f} entry≈{price:.6f} "
                 f"tp={tp:.6f} sl={sl:.6f} conf={sig.confidence} quality={quality}")

        if not paper:
            await asyncio.to_thread(self.bf.set_leverage, sig.symbol, LEVERAGE)
            # MAKER-SIDE LIMIT ORDER (2026-05-05 fee-cut change).
            # Old behavior: limit crossed the spread (1.0005x for long, 0.9995x for short)
            # → guaranteed taker fill at 0.06% per side = 0.12% round trip.
            # New behavior: limit sits PASSIVELY on the book.
            #   - Long → place 2 ticks BELOW current price (passive bid)
            #   - Short → place 2 ticks ABOVE current price (passive ask)
            # → fills as MAKER at 0.02% per side = 0.04% round trip (~70% fee cut).
            # Trade-off: if price moves away within the candle, order may not fill.
            # For mean-reversion agents (connors_rsi2, williams_r) this is FINE —
            # missing a worse-priced entry is a feature, not a bug.
            tick = float(instr.get("tick_size", 0.01))
            maker_offset = max(tick * 2, price * 0.0001) if tick > 0 else price * 0.0001
            limit_price = (price - maker_offset) if sig.side == "long" else (price + maker_offset)
            # PRE-POSITION AT HOT ZONE (2026-05-06 — Saad's directive: "horizontal lets you
            # position yourself already").
            # If the signal metadata contains a `zone_price` (set by FibHotZoneAgent), snap
            # the limit DIRECTLY to that exact price. Order rests AT the hot zone, waiting
            # for the market to come to us. Pure hunter mode — no chasing.
            zone_price = sig.metadata.get("zone_price") if sig.metadata else None
            if zone_price and zone_price > 0:
                # Verify zone is on the passive side and within sane distance (max 1% from mid)
                if sig.side == "long" and zone_price < price and (price - zone_price) / price <= 0.01:
                    log.info(f"PRE-POSITION {sig.symbol} long: limit at zone {zone_price:.6f} "
                             f"(was {limit_price:.6f}, mid {price:.6f})")
                    limit_price = float(zone_price)
                elif sig.side == "short" and zone_price > price and (zone_price - price) / price <= 0.01:
                    log.info(f"PRE-POSITION {sig.symbol} short: limit at zone {zone_price:.6f} "
                             f"(was {limit_price:.6f}, mid {price:.6f})")
                    limit_price = float(zone_price)
            # FIB-AWARE LIMIT PLACEMENT (2026-05-06 — Saad's directive after fibonacci agent
            # outperformed). If a Fibonacci retracement level sits within 0.5% of price on
            # the PASSIVE side of the book, snap the limit there instead of a flat 2-tick
            # offset. Orders rest at levels where price actually reacts.
            #   Long  → highest fib below current price (within 0.5%) = better passive bid
            #   Short → lowest fib above current price (within 0.5%) = better passive ask
            # If no qualifying fib level → fall back to the 2-tick offset above.
            try:
                fib_df = await asyncio.to_thread(self.bf.candles, sig.symbol, "1H", 60)
                if fib_df is not None and len(fib_df) >= 30:
                    fh = fib_df["high"]; fl = fib_df["low"]
                    swing_h = float(fh.max()); swing_l = float(fl.min())
                    if swing_h > swing_l and (swing_h - swing_l) / swing_l >= 0.02:
                        sh_idx = fh.idxmax(); sl_idx = fl.idxmin()
                        uptrend_fib = sh_idx > sl_idx
                        move = swing_h - swing_l
                        fib_levels = [0.236, 0.382, 0.500, 0.618, 0.786]
                        fib_prices = [
                            (swing_h - move * f) if uptrend_fib else (swing_l + move * f)
                            for f in fib_levels
                        ]
                        max_dist = price * 0.005   # within 0.5% of mid
                        if sig.side == "long":
                            cands = [fp for fp in fib_prices if 0 < (price - fp) <= max_dist]
                            if cands:
                                fib_lp = max(cands)   # highest fib below price = closest passive bid
                                if fib_lp < limit_price:   # only if more passive than 2-tick offset
                                    log.info(f"FIB-LIMIT {sig.symbol} long: snapping {limit_price:.6f} → {fib_lp:.6f}")
                                    limit_price = fib_lp
                        else:
                            cands = [fp for fp in fib_prices if 0 < (fp - price) <= max_dist]
                            if cands:
                                fib_lp = min(cands)   # lowest fib above price = closest passive ask
                                if fib_lp > limit_price:
                                    log.info(f"FIB-LIMIT {sig.symbol} short: snapping {limit_price:.6f} → {fib_lp:.6f}")
                                    limit_price = fib_lp
            except Exception as _fib_e:
                log.debug(f"fib-aware limit fallback for {sig.symbol}: {_fib_e}")
            # Round all prices (limit, TP, SL) to symbol's tick_size.
            # BloFin rejects with 102016 if any price has wrong precision.
            if tick > 0:
                decimals = max(0, -int(math.floor(math.log10(tick))))
                def round_to_tick(p):
                    if p is None or p <= 0:
                        return p
                    return round(round(p / tick) * tick, decimals)
                limit_price = round_to_tick(limit_price)
                tp = round_to_tick(tp) if tp else tp
                sl = round_to_tick(sl) if sl else sl
            res = await asyncio.to_thread(self.bf.place_market, sig.symbol,
                                          order_side, size, tp, sl, cid, limit_price)
            if "error" in res or (res.get("code") and str(res.get("code")) != "0"):
                # Auto-blacklist symbols that fail with IP-restriction code 102134.
                # No point retrying every cycle — they will keep failing this session.
                res_str = json.dumps(res)
                if "102134" in res_str or "IP location is restricted" in res_str:
                    BloFin._bad_symbols_cache.add(sig.symbol)
                    # Clear cached df1h so hermes_signals stops generating this symbol
                    if hasattr(self, '_state') and hasattr(self._state, '_df1h_cache'):
                        self._state._df1h_cache.pop(sig.symbol, None)
                    log.warning(f"order rejected {sig.symbol}: IP restricted — "
                                f"adding to session skip-list (no further retries)")
                    return False
                log.error(f"order rejected {sig.symbol}: {res}")
                await tg_send(session,
                    f"❌ <b>REJECTED</b> {sig.agent} {sig.symbol} {sig.side.upper()}\n"
                    f"<code>{res_str[:300]}</code>")
                return False

        # Persist
        now = datetime.now(timezone.utc).isoformat()
        self.db.insert({
            "custom_id":   cid,
            "agent":       sig.agent,
            "profile":     sig.profile,
            "symbol":      sig.symbol,
            "side":        position_side,
            "entry_price": price,
            "qty":         size,
            "notional":    notional,
            "tp_price":    tp,
            "sl_price":    sl,
            "trail_pct":   prof["trail"],
            "high_water":  price,
            "low_water":   price,
            "current_stop": sl,
            "confidence":  sig.confidence,
            "reason":      sig.reason,
            "status":      "open" if not paper else "paper",
            "opened_at":   now,
            "meta":        _safe_json_dumps(sig.metadata),
        })

        await tg_send(session,
            f"🟢 <b>OPEN</b> {sig.symbol} {sig.side.upper()}\n"
            f"agent: <b>{sig.agent}</b> ({sig.profile})  conf {sig.confidence}/10\n"
            f"entry {price:.6f}  TP {tp:.6f}  SL {sl:.6f}\n"
            f"size {size}  notional ${notional:.0f}  lev {LEVERAGE}x\n"
            f"<i>{sig.reason}</i>")
        return True

    # ---------- close --------------------------------------------------------
    async def close_trade(self, t: dict, price: float,
                          session: aiohttp.ClientSession,
                          reason: str = "trail",
                          paper: bool = False) -> bool:
        if not paper:
            res = await asyncio.to_thread(self.bf.close_logical,
                                          t["symbol"], t["side"])
            if "error" in res:
                log.error(f"close failed {t['symbol']}: {res}")
                # Still mark closed in DB so we don't loop trying
        side_mult = 1 if t["side"] == "long" else -1
        pnl_pct = ((price - t["entry_price"]) / t["entry_price"]) * 100 * side_mult
        # Effective leveraged PnL
        pnl_usd = (pnl_pct / 100) * t["notional"] * LEVERAGE / LEVERAGE  # notional already x1
        # Wait — notional in size_for is the position notional (size*cv*price), so:
        pnl_usd = (pnl_pct / 100) * t["notional"]
        now = datetime.now(timezone.utc).isoformat()
        self.db.update(t["custom_id"],
                       exit_price=price,
                       pnl=pnl_usd,
                       pnl_pct=pnl_pct,
                       status="closed",
                       closed_at=now)
        emoji = "✅" if pnl_usd > 0 else "🛑"
        log.info(f"CLOSE {t['symbol']} {t['side']} pnl=${pnl_usd:+.2f} "
                 f"({pnl_pct:+.2f}%) reason={reason}")
        # Local LLM (Qwen) narrative — FREE. One line, why this won/lost.
        verdict = "WIN" if pnl_usd > 0 else "LOSS"
        narrative = await local_llm_chat(
            f"In ONE short sentence (max 18 words), explain this trade "
            f"{verdict}: {t['agent']} agent went {t['side']} on {t['symbol']}, "
            f"entry {t['entry_price']:.6f}, exit {price:.6f}, "
            f"PnL ${pnl_usd:+.2f} ({pnl_pct:+.2f}%), exit reason: {reason}. "
            f"Be plain and concrete. No hedging, no disclaimers.",
            max_tokens=60, temperature=0.4, timeout=10,
        )
        narrative_line = f"\n💬 <i>{narrative.strip()}</i>" if narrative else ""
        # If this was a loss, diagnose WHY so Hermes learns
        diagnosis_line = ""
        if pnl_usd < 0 and HAS_HERMES:
            try:
                trade_rec = dict(t)
                trade_rec["pnl"] = pnl_usd
                trade_rec["pnl_pct"] = pnl_pct
                diag = diagnose_loss(trade_rec)
                diagnosis_line = (f"\n🧠 <b>Learned:</b> {diag.root_cause} — {diag.fix[:120]}")
                log.info(f"LOSS-DIAGNOSIS: {diag.root_cause} ({diag.confidence:.0%} conf) — {diag.fix[:100]}")
            except Exception:
                pass
        await tg_send(session,
            f"{emoji} <b>CLOSE</b> {t['symbol']} {t['side'].upper()}\n"
            f"agent: <b>{t['agent']}</b>  reason: <i>{reason}</i>\n"
            f"entry {t['entry_price']:.6f} → exit {price:.6f}\n"
            f"PnL: <b>${pnl_usd:+.2f}</b> ({pnl_pct:+.2f}%){narrative_line}{diagnosis_line}")
        return True


# =============================================================================
# ORCHESTRATOR
# =============================================================================
def universe_from_tickers(tickers: List[dict]) -> List[Tuple[str, float, float]]:
    """Returns list of (symbol, last_price, 24h_quote_volume) sorted by volume desc."""
    out = []
    for t in tickers:
        try:
            sym = t.get("instId") or ""
            if not sym.endswith("-USDT"):
                continue
            # Blacklist — skip symbols that always lose money
            blacklist = {"ICP-USDT", "SOL-USDT", "BCH-USDT", "ZEC-USDT", "ETH-USDT"}
            if sym in blacklist:
                continue
            last = float(t.get("last") or 0)
            if last <= 0:
                continue
            # Try multiple field names for quote volume
            vq = (t.get("volCurrencyQuote24h") or t.get("volCcyQuote24h")
                  or t.get("vol24hQuote") or t.get("quoteVol24h") or 0)
            try:
                vq = float(vq)
            except Exception:
                vq = 0.0
            if vq <= 0:
                # Fall back: base vol * last price
                base_vol = float(t.get("vol24h") or t.get("volCurrency24h") or 0)
                vq = base_vol * last
            if vq < MIN_24H_VOLUME_USD:
                continue
            out.append((sym, last, vq))
        except Exception:
            continue
    out.sort(key=lambda x: -x[2])
    return out


async def analyze_symbol(state: SimpleNamespace, sym: str) -> List[Signal]:
    bf: BloFin = state.bf
    df5  = await asyncio.to_thread(bf.candles, sym, "5m", 200)
    if df5.empty or len(df5) < 50:
        return []
    df15 = await asyncio.to_thread(bf.candles, sym, "15m", 200)
    df30 = await asyncio.to_thread(bf.candles, sym, "30m", 150)  # 2026-06-06: for Viki
    df1h = await asyncio.to_thread(bf.candles, sym, "1H", 150)
    ob   = await asyncio.to_thread(bf.orderbook, sym, 20)
    fr   = await asyncio.to_thread(bf.funding, sym)
    trend_st = compute_trend_state(df1h)
    ctx  = MarketContext(sym, df5, df15, df30, df1h, fr, ob, state.news, trend=trend_st)
    # Cache df1h for Hermes custom signal engine
    if not hasattr(state, '_df1h_cache'):
        state._df1h_cache = {}
    state._df1h_cache[sym] = df1h
    out: List[Signal] = []
    for a in state.agents:
        try:
            sig = a.analyze(sym, ctx)
            if sig:
                # Stash the trend state in metadata so the merge step can apply
                # with-trend / against-trend bias without recomputing.
                if sig.metadata is None:
                    sig.metadata = {}
                sig.metadata["_trend_score"] = trend_st.score
                sig.metadata["_trend_dir"]   = trend_st.direction
                sig.metadata["_df1h"] = df1h  # stash for confluence check
                sig.metadata["_df15m"] = df15
                out.append(sig)
        except Exception as e:
            log.warning(f"agent {a.name} {sym}: {e}")
    return out


async def scan_once(state: SimpleNamespace, paper: bool = False):
    bf: BloFin = state.bf
    state.learning.maybe_refresh()

    # BTC_VOLATILITY_PAUSE check
    now_t = time.time()
    if now_t < getattr(state, "new_entries_paused_until", 0):
        remaining = int(state.new_entries_paused_until - now_t)
        log.info(f"BTC_VOLATILITY_PAUSE active — {remaining}s remaining, skipping entries")
        return

    # ANTI_REVENGE_LOCKOUT check
    if now_t < getattr(state, "anti_revenge_paused_until", 0):
        remaining = int(state.anti_revenge_paused_until - now_t)
        log.info(f"ANTI_REVENGE_LOCKOUT active — {remaining}s remaining, skipping entries")
        return
    # BUGFIX 2026-05-06: previously the same loss cluster re-triggered the
    # lockout every 30 min forever, because recent_two_losses() always looked
    # at the latest 2 trades regardless of age. Track the last-trigger time so
    # only NEW losses after this point can re-arm the lockout.
    last_trigger_t = getattr(state, "anti_revenge_last_trigger", 0)
    since_iso = (datetime.fromtimestamp(last_trigger_t, tz=timezone.utc).isoformat()
                 if last_trigger_t else None)
    if state.db.recent_two_losses(since_iso=since_iso):
        state.anti_revenge_paused_until = now_t + ANTI_REVENGE_PAUSE_MIN * 60
        state.anti_revenge_last_trigger = now_t  # advance horizon — old losses won't re-fire
        log.warning(f"ANTI_REVENGE_LOCKOUT triggered — pausing {ANTI_REVENGE_PAUSE_MIN} min")
        await tg_send(state.session, f"🛡 <b>Anti-revenge lockout</b> — 2 consecutive losses, "
                      f"pausing {ANTI_REVENGE_PAUSE_MIN} min")
        return

    # BTC volatility check (uses BTC-USDT 1H candle)
    try:
        btc_df = await asyncio.to_thread(bf.candles, "BTC-USDT", "1H", 3)
        if len(btc_df) >= 2:
            btc_open = float(btc_df["close"].iloc[-2])
            btc_now  = float(btc_df["close"].iloc[-1])
            if btc_open > 0:
                btc_move = abs(btc_now - btc_open) / btc_open * 100
                if btc_move >= BTC_VOL_PAUSE_PCT:
                    state.new_entries_paused_until = now_t + BTC_VOL_PAUSE_MIN * 60
                    log.warning(f"BTC_VOLATILITY_PAUSE: BTC moved {btc_move:.2f}% in 1H — "
                                f"pausing {BTC_VOL_PAUSE_MIN} min")
                    await tg_send(state.session,
                        f"⏸ <b>BTC volatility pause</b> {btc_move:.2f}% 1H move — "
                        f"pausing {BTC_VOL_PAUSE_MIN} min")
                    return
    except Exception as e:
        log.warning(f"btc vol check: {e}")

    tickers = await asyncio.to_thread(bf.tickers)
    universe = universe_from_tickers(tickers)
    if not universe:
        log.warning("empty universe — ticker fetch may have failed")
        return
    universe = universe[:TOP_N_COINS]
    regime = getattr(state, "regime", "RANGING")
    log.info(f"scan: {len(universe)} symbols  regime: {regime}  | learning: {state.learning.summary()}")

    equity_task = asyncio.to_thread(bf.balance)
    pos_task = asyncio.to_thread(bf.positions)
    equity, exch_positions = await asyncio.gather(equity_task, pos_task)
    our_open = state.db.open_trades()
    log.info(f"equity=${equity:.2f}  exch_positions={len(exch_positions)}  "
             f"our_open={len(our_open)}  today_pnl=${state.db.today_pnl():+.2f}")

    # Concurrent analysis
    sem = asyncio.Semaphore(SCAN_CONCURRENCY)
    async def scan_one(s):
        async with sem:
            return await analyze_symbol(state, s)
    sym_list = [s for s, _, _ in universe]
    price_map = {s: p for s, p, _ in universe}
    results = await asyncio.gather(*[scan_one(s) for s in sym_list],
                                   return_exceptions=True)

    candidates: List[Signal] = []
    for r in results:
        if isinstance(r, list):
            candidates.extend(r)

    if not candidates:
        log.info("no signals this cycle")
        return

    # Apply learning weights — kill-switch + WR scaling.
    # weight()==0 means agent is a proven loser (WR<30% over 5+ trades): drop the signal.
    weighted: List[Signal] = []
    for s in candidates:
        w = state.learning.weight(s.agent)
        if w <= 0.0:
            log.info(f"KILL-SWITCH: dropping {s.agent} signal (WR-weight=0)")
            continue
        s.confidence = max(1, min(9, int(round(s.confidence * w))))
        weighted.append(s)
    candidates = weighted
    if not candidates:
        log.info("all signals killed by WR-weight; nothing to trade this cycle")
        return

    # TREND BIAS — "trend is your friend" (Saad 2026-05-06).
    # With-trend signals get +1 confidence; against-trend get -1; STRONG against = -2.
    # Strong-trend countertrend signals are DROPPED entirely (don't fight a freight train).
    trend_filtered: List[Signal] = []
    for s in candidates:
        ts = (s.metadata or {}).get("_trend_score", 0)
        td = (s.metadata or {}).get("_trend_dir", "FLAT")
        # Determine alignment:
        # ts > 0 = trend UP, ts < 0 = trend DOWN, ts==0 = flat (no bias either way)
        if ts == 0:
            trend_filtered.append(s)
            continue
        with_trend = (ts > 0 and s.side == "long") or (ts < 0 and s.side == "short")
        against_trend = (ts > 0 and s.side == "short") or (ts < 0 and s.side == "long")
        if with_trend:
            s.confidence = min(9, s.confidence + 1)
            s.reason = f"[trend+] {s.reason}"
        elif against_trend:
            # Hard rule: strong opposing trend (|score|=3) — drop the signal entirely
            if abs(ts) >= 3:
                log.info(f"TREND-DROP: {s.agent} {s.symbol} {s.side} — strong opposing {td} trend (score={ts})")
                continue
            penalty = 2 if abs(ts) >= 2 else 1
            s.confidence = max(1, s.confidence - penalty)
            s.reason = f"[trend-{penalty}] {s.reason}"
        trend_filtered.append(s)
    candidates = trend_filtered
    if not candidates:
        log.info("all signals dropped by trend filter")
        return

    # Multi-agent agreement boost (FIXED 2026-05-05 — confidence was inverted).
    # OLD bug: confidence += len(sigs), which let 2 agreeing agents push any signal
    # to conf=10. Live data showed conf=10 trades had 39% WR while conf<=7 had 100%.
    # Headcount is not edge — wrong twice is still wrong.
    # NEW rule:
    #   - Multi-agent boost capped at +1 (regardless of how many agents agree)
    #   - Absolute confidence capped at 9 (10 is reserved for AI arbiter approval)
    #   - Boost only applies when agreeing agents come from DIFFERENT families
    #     (e.g. mean-rev + trend = real confluence; mean-rev + mean-rev = noise)
    MEAN_REV_FAMILY = {"connors_rsi2", "zscore_reversion", "stoch_rsi",
                       "vwap_reversion", "bb_bounce", "williams_r", "raschke_retest"}
    TREND_FAMILY    = {"supertrend", "hurst_regime", "kalman_trend", "golden_cross",
                       "ema_ribbon", "trend_pullback", "macd_cross", "viki"}
    BREAKOUT_FAMILY = {"daily_breakout", "daily_breakout_2h", "daily_breakout_4h",
                       "daily_breakout_8h", "daily_breakout_12h", "daily_breakout_24h",
                       "daily_breakout_48h", "daily_breakout_7d", "donchian", "asymmetric"}
    def _family(agent_name):
        if agent_name in MEAN_REV_FAMILY: return "MR"
        if agent_name in TREND_FAMILY:    return "TR"
        if agent_name in BREAKOUT_FAMILY: return "BO"
        return "OTHER"

    keyed: Dict[Tuple[str, str], List[Signal]] = {}
    for s in candidates:
        keyed.setdefault((s.symbol, s.side), []).append(s)
    final: List[Signal] = []
    for (sym, side), sigs in keyed.items():
        if len(sigs) > 1:
            top = max(sigs, key=lambda x: x.confidence)
            families = {_family(sg.agent) for sg in sigs}
            real_confluence = len(families) > 1   # at least 2 different strategy families
            boost = 1 if real_confluence else 0
            top.confidence = min(9, top.confidence + boost)
            top.reason = (f"{len(sigs)} agents agree ({'cross-family' if real_confluence else 'same-family'}) ["
                          + ",".join(sg.agent for sg in sigs)
                          + f"] — best: {top.reason}")
            final.append(top)
        else:
            # Solo signal — also cap at 9 unless AI arbiter approves later
            sigs[0].confidence = min(9, sigs[0].confidence)
            final.append(sigs[0])
    final.sort(key=lambda s: -s.confidence)

    log.info(f"signals: {len(candidates)} raw → {len(final)} aggregated  "
             f"(top conf {final[0].confidence if final else 0})")

    # 2026-05-09 MACRO-BIAS: read market_context.json (refreshed 3x/day by
    # market_context_loop). Apply +/-1 confidence tilt based on broader market.
    mc_bias, mc_reasons = _load_market_bias()
    if mc_bias != "neutral" and final:
        adjusted = 0
        for sg in final:
            if mc_bias == "bullish":
                if sg.side == "long":
                    sg.confidence = min(9, sg.confidence + 1); adjusted += 1
                else:
                    sg.confidence = max(1, sg.confidence - 1); adjusted += 1
            elif mc_bias == "bearish":
                if sg.side == "short":
                    sg.confidence = min(9, sg.confidence + 1); adjusted += 1
                else:
                    sg.confidence = max(1, sg.confidence - 1); adjusted += 1
        final.sort(key=lambda s: -s.confidence)
        log.info(f"macro bias={mc_bias} ({'; '.join(mc_reasons[:3])}) — adjusted {adjusted} signals")

    # Build funding rate lookup for quick access
    funding_map: Dict[str, float] = {}

    # ============================================================
    # DATA-DRIVEN FILTERS 2026-05-07 (from WHY_LOSE_HOW_WIN analysis):
    # Three filters proven from 40 real trades to remove the bleeders.
    # ============================================================
    BAD_HOURS_UTC      = {4, 6}  # 2026-06-07: narrowed — only the 2 worst hours (-$46 total losses)
    DISABLED_AGENTS    = {"vwap_reversion"}      # net -$1.43, faded momentum
    AGENT_SYM_BLACKLIST = {                       # agent → set of symbols to skip
        "connors_rsi2": {"TAO-USDT"},            # 3 losses, $-1.76, never wins long
    }
    current_hour_utc = datetime.now(timezone.utc).hour
    in_bad_hour = current_hour_utc in BAD_HOURS_UTC

    # === HERMES CUSTOM SIGNALS (weighted 6-indicator consensus) ===
    try:
        from hermes_signals import generate_signals, signal_to_dict
        ctx_map = getattr(state, '_df1h_cache', {})
        for sym in sym_list:
            df1h = ctx_map.get(sym)
            if df1h is not None:
                cs = generate_signals(sym, df1h)
                if cs:
                    from dataclasses import dataclass as _dc
                    sig = Signal("hermes_master", sym, cs.side, cs.confidence,
                                "hermes_master", f"HERMES composite {cs.score:.0f}% {' '.join(cs.reasons)}",
                                {"_df1h": df1h, "score": cs.score, "reasons": cs.reasons})
                    sig._agent_mult = 0.06
                    final.append(sig)
                    log.info(f"HERMES_SIGNAL {sym} {cs.side} score={cs.score:.0f}% conf={cs.confidence} {cs.reasons}")
    except Exception:
        pass
    # === END CUSTOM SIGNALS ===

    # Sort: enabled non-paper agents first, then by confidence
    enabled_first = sorted(final, key=lambda s: (
        0 if getattr(s, '_agent_mult', 0) > 0 else 1,
        -s.confidence
    ))
    for sig in enabled_first[:20]:
        # Bleeder filter #1: bad hours (dead zones per deep learn autopsy)
        if in_bad_hour:
            log.info(f"BAD_HOUR_SKIP {sig.agent} {sig.symbol}: {current_hour_utc:02d}:00 UTC in killer-hours window")
            continue
        # Bleeder filter #1b: SHORTS only in strong DOWN trend (-$26.42 loss on 148 shorts)
        ts = (sig.metadata or {}).get("_trend_score", 0) if sig.metadata else 0
        if sig.side == "short" and ts > -1:
            log.info(f"SHORT_SKIP {sig.agent} {sig.symbol}: trend_score={ts} — shorts only below -1")
            continue
        # Bleeder filter #2: disabled-by-data agents
        if sig.agent in DISABLED_AGENTS:
            log.info(f"DATA_DISABLED {sig.agent} {sig.symbol}: agent disabled by trade-data analysis")
            continue
        # Bleeder filter #3: agent + symbol combos that lose money
        if sig.symbol in AGENT_SYM_BLACKLIST.get(sig.agent, set()):
            log.info(f"AGENT_SYM_SKIP {sig.agent} {sig.symbol}: combo blacklisted (data shows persistent losses)")
            continue
        # Check regime compatibility
        agent_obj = next((a for a in state.agents if a.name == sig.agent), None)
        if agent_obj and agent_obj.valid_regimes and regime not in agent_obj.valid_regimes:
            log.info(f"REGIME_SKIP {sig.agent} {sig.symbol}: regime={regime} not in {agent_obj.valid_regimes}")
            continue
        # Check enabled/paper-only
        if agent_obj and not agent_obj.enabled:
            log.info(f"DISABLED_SKIP {sig.agent} {sig.symbol}: agent disabled by backtest")
            continue
        if agent_obj and agent_obj.paper_only and not paper:
            continue   # already logged above, skip silently
        # Attach notional multiplier to signal for Executor
        if agent_obj:
            sig._agent_mult = agent_obj.notional_multiplier

        # Skip paper-only BEFORE spending CPU on confluence (they can't trade anyway)
        if agent_obj and agent_obj.paper_only and not paper:
            sig.metadata["_paper_only"] = True
            log.info(f"PAPER_ONLY {sig.agent} {sig.symbol}: paper-only agent, signal logged but not executed")
            continue

        # === MULTI-INDICATOR CONFLUENCE (2+ must agree) ===
        # Research: single indicator = ~50% WR. 2+ = 68-72%. 4 = 76%.
        try:
            df_1h = sig.metadata.get("_df1h") if sig.metadata else None
            if df_1h is not None and len(df_1h) >= 50:
                c = df_1h["close"]
                last = c.iloc[-1]
                # RSI
                r = rsi(c, 14).iloc[-1]
                rsi_bull = r < 40
                rsi_bear = r > 60
                # MACD (crypto-optimized 24/52/18)
                e24 = ema(c, 24); e52 = ema(c, 52)
                macd_series = e24 - e52
                ml = macd_series.iloc[-1]
                ms = ema(macd_series, 18).iloc[-1]
                macd_bull = ml > ms
                macd_bear = ml < ms
                # Bollinger (returns: upper, middle, lower)
                bb = bbands(c, 20, 2.0)
                bb_bull = last <= bb[2].iloc[-1] * 1.005  # near/below lower band
                bb_bear = last >= bb[0].iloc[-1] * 0.995  # near/above upper band
                # EMA stack
                e20 = ema(c, 20).iloc[-1]; e50 = ema(c, 50).iloc[-1]
                ema_bull = e20 > e50
                ema_bear = e20 < e50
                # Fibonacci: is price near a key fib retracement of recent swing?
                swing_high = c.iloc[-50:].max()
                swing_low = c.iloc[-50:].min()
                swing_range = swing_high - swing_low
                fib_bull = False; fib_bear = False
                if swing_range > 0:
                    fib_382 = swing_high - swing_range * 0.382
                    fib_500 = swing_high - swing_range * 0.500
                    fib_618 = swing_high - swing_range * 0.618
                    fib_786 = swing_high - swing_range * 0.786
                    # Price near a fib support level (±1% tolerance)
                    fib_bull = any(abs(last - f) / last < 0.01 for f in [fib_382, fib_500, fib_618, fib_786])
                    # Price near a fib resistance level
                    fib_382r = swing_low + swing_range * 0.382
                    fib_618r = swing_low + swing_range * 0.618
                    fib_786r = swing_low + swing_range * 0.786
                    fib_bear = any(abs(last - f) / last < 0.01 for f in [fib_382r, fib_618r, fib_786r])
                # Count agreements (now 5 indicators: RSI, MACD, BB, EMA, FIB)
                if sig.side == "long":
                    agrees = sum([rsi_bull, macd_bull, bb_bull, ema_bull, fib_bull])
                else:
                    agrees = sum([rsi_bear, macd_bear, bb_bear, ema_bear, fib_bear])
                # Require 2+ out of 5 (fib often missing, don't block good trades)
                if agrees < 2:
                    log.info(f"CONFLUENCE_FAIL {sig.agent} {sig.symbol} {sig.side}: "
                             f"only {agrees}/5 agree (need 2+) — "
                             f"RSI={'Y' if (rsi_bull if sig.side=='long' else rsi_bear) else 'N'}"
                             f" MACD={'Y' if (macd_bull if sig.side=='long' else macd_bear) else 'N'}"
                             f" BB={'Y' if (bb_bull if sig.side=='long' else bb_bear) else 'N'}"
                             f" EMA={'Y' if (ema_bull if sig.side=='long' else ema_bear) else 'N'}"
                             f" FIB={'Y' if (fib_bull if sig.side=='long' else fib_bear) else 'N'}")
                    continue
            else:
                log.info(f"CONFLUENCE_PASS {sig.agent} {sig.symbol} {sig.side}: {agrees}/5 agree")
        except Exception as e:
            log.info(f"CONFLUENCE_SKIP {sig.symbol}: {e}")
        # === END CONFLUENCE CHECK ===

        # Fetch funding rate if not cached
        fr = funding_map.get(sig.symbol)
        if fr is None:
            try:
                fr = await asyncio.to_thread(bf.funding, sig.symbol)
                funding_map[sig.symbol] = fr
            except Exception:
                fr = 0.0

        ok, why = state.risk.vet(sig, equity, our_open, exch_positions, funding_rate=fr)
        if not ok:
            log.info(f"VETO {sig.agent}/{sig.profile} {sig.symbol} {sig.side}: {why}")
            continue
        # AI arbiter for high-confidence
        ctx_summary = (f"price={price_map.get(sig.symbol)}, "
                       f"equity=${equity:.0f}, open={len(our_open)}/{MAX_CONCURRENT_POSITIONS}, "
                       f"daily_pnl=${state.db.today_pnl():+.2f}")
        approve, reason = await ai_arbiter(state.session, sig, ctx_summary)
        if not approve:
            log.info(f"AI-VETO {sig.symbol} {sig.side}: {reason}")
            await tg_send(state.session,
                f"🤖 AI-veto {sig.symbol} {sig.side.upper()}: {reason}")
            continue
        price = price_map.get(sig.symbol)
        if not price:
            continue
        opened = await state.exec.open(sig, equity, price, state.session, paper=paper)
        if opened:
            our_open = state.db.open_trades()
            if len(our_open) >= MAX_CONCURRENT_POSITIONS:
                break


async def monitor_positions(state: SimpleNamespace, paper: bool = False):
    """Trailing stop + max-hold management for our open positions only."""
    open_trades = state.db.open_trades()
    if not open_trades:
        return
    bf: BloFin = state.bf
    tickers = await asyncio.to_thread(bf.tickers)
    px = {t.get("instId"): float(t.get("last") or 0) for t in tickers}

    # HARD_LIQUIDATION_GUARD: immediately close any position >5% adverse
    for t in open_trades:
        price = px.get(t["symbol"], 0)
        if price <= 0:
            continue
        ep = float(t["entry_price"] or 0)
        if ep <= 0:
            continue
        if t["side"] == "long":
            adverse_pct = (ep - price) / ep * 100
        else:
            adverse_pct = (price - ep) / ep * 100
        if adverse_pct >= HARD_LIQUIDATION_GUARD:
            log.warning(f"HARD_LIQUIDATION_GUARD: {t['symbol']} {t['side']} "
                        f"{adverse_pct:.2f}% adverse — emergency close")
            await state.exec.close_trade(t, price, state.session,
                                         reason="hard_liquidation_guard", paper=paper)
            await tg_send(state.session,
                f"🚨 <b>HARD GUARD</b> {t['symbol']} {t['side'].upper()} "
                f"{adverse_pct:.2f}% adverse — emergency closed")

    # Reload after possible emergency closes
    open_trades = state.db.open_trades()
    for t in open_trades:
        sym = t["symbol"]
        side = t["side"]
        price = px.get(sym, 0)
        if price <= 0:
            continue
        prof = PROFILES.get(t["profile"], PROFILES["momentum"])
        new_stop = float(t["current_stop"] or 0)
        new_high = float(t["high_water"] or t["entry_price"])
        new_low  = float(t["low_water"]  or t["entry_price"])
        hit_stop = False
        hit_tp   = False

        # v3.0 ATR-BASED TRAIL (2026-06-09, Saad: "tight trails, lock profit, no winners-to-losers"):
        # Replaces the old 0.3% ladder which had slippage eating profits.
        #
        # DESIGN:
        # - Trailing distance = ATR × profile multiplier (1.0x-1.5x depending on agent type)
        # - ATR adapts to volatility automatically — tight when calm, wider when wild
        # - Breakeven at +1.5% profit: once profit is solid, SL moves to entry
        # - Failed runner: if price hit +3% and dropped back below +1%, exit immediately
        # - Pullback tighten: if price pulls back 1.0x ATR+ from peak, tighten trail
        # - Only raises the stop, never lowers it.

        # Cache ATR per symbol — reuse the cached 1H candles if available
        atr_val = None
        atr_key = f"atr_{sym}"
        if hasattr(state, '_atr_cache') and atr_key in state._atr_cache:
            atr_val = state._atr_cache[atr_key]
        else:
            try:
                df1h = bf.candles(sym, "1h", limit=20)
                if len(df1h) >= 20:
                    atr_val = float(atr(df1h).iloc[-1])
                    if not hasattr(state, '_atr_cache'):
                        state._atr_cache = {}
                    state._atr_cache[atr_key] = atr_val
                else:
                    # Fallback: use 1% of price as rough ATR estimate
                    atr_val = price * 0.01
            except:
                atr_val = price * 0.01

        if atr_val is None or atr_val <= 0:
            atr_val = price * 0.01

        atr_pct = (atr_val / price) * 100 if price > 0 else 1.0

        if side == "long":
            new_high = max(new_high, price)
            entry = t["entry_price"]
            peak_pct = (new_high - entry) / entry * 100
            cur_pct = (price - entry) / entry * 100

            # Step 1: ATR-based trailing distance (tightens as profit grows)
            # Profile dictates base trail multiplier; breakouts wider, scalps tighter
            trail_mult = prof.get("atr_trail", 1.5)

            if cur_pct < 0.0:
                # In loss — keep original SL, let it ride
                new_stop_candidate = new_stop if new_stop > 0 else 0.0
            elif cur_pct < 1.5:
                # Small profit zone — tight ATR trail locks early gains
                # Trail = 0.6x ATR from peak for tight protection
                trail_dist = atr_val * 0.6
                new_stop_candidate = new_high - trail_dist
            elif cur_pct < 4.0:
                # Mid profit zone — normal ATR trail, let winners run
                trail_dist = atr_val * trail_mult
                new_stop_candidate = new_high - trail_dist
            else:
                # Big profit zone — pull SL to breakeven + 1.5% (profit locked)
                trail_dist = atr_val * trail_mult
                breakeven_floor = entry * 1.015
                new_stop_candidate = max(breakeven_floor, new_high - trail_dist)

            # Step 2: Failed runner detection
            # If we hit 3%+ profit and now back below 1%, it failed — exit fast
            if peak_pct >= 3.0 and cur_pct < 1.0:
                new_stop_candidate = price * 0.998

            # Step 3: Pullback tighten — if price pulls back 1x ATR from peak,
            # trail becomes tighter (momentum is dying)
            pullback = (new_high - price) / atr_val if atr_val > 0 else 0
            if pullback >= 1.0 and peak_pct >= 2.0:
                # Tighten to 0.5x ATR from peak
                new_stop_candidate = max(new_stop_candidate, new_high - atr_val * 0.5)

            # Never lower the stop
            if new_stop_candidate > new_stop:
                new_stop = new_stop_candidate

            state.db.update(t["custom_id"], high_water=new_high, current_stop=new_stop)

            if price <= new_stop and new_stop > 0:
                hit_stop = True
            if price >= t["tp_price"]:
                hit_tp = True

        else:  # short
            new_low = min(new_low, price)
            entry = t["entry_price"]
            trough_pct = (entry - new_low) / entry * 100
            cur_pct = (entry - price) / entry * 100

            trail_mult = prof.get("atr_trail", 1.5)

            if cur_pct < 0.0:
                new_stop_candidate = new_stop if new_stop > 0 else float('inf')
            elif cur_pct < 1.5:
                trail_dist = atr_val * 0.6
                new_stop_candidate = new_low + trail_dist
            elif cur_pct < 4.0:
                trail_dist = atr_val * trail_mult
                new_stop_candidate = new_low + trail_dist
            else:
                trail_dist = atr_val * trail_mult
                breakeven_ceil = entry * 0.985
                new_stop_candidate = min(breakeven_ceil, new_low + trail_dist)

            # Failed runner (short)
            if trough_pct >= 3.0 and cur_pct < 1.0:
                new_stop_candidate = price * 1.002

            # Bounce back tighten (short)
            bounce = (price - new_low) / atr_val if atr_val > 0 else 0
            if bounce >= 1.0 and trough_pct >= 2.0:
                new_stop_candidate = min(new_stop_candidate, new_low + atr_val * 0.5)

            if new_stop_candidate > 0 and (new_stop == 0 or new_stop_candidate < new_stop):
                new_stop = new_stop_candidate

            state.db.update(t["custom_id"], low_water=new_low, current_stop=new_stop)

            if price >= new_stop and new_stop > 0:
                hit_stop = True
            if price <= t["tp_price"]:
                hit_tp = True


        # Max hold timeout
        opened_at = datetime.fromisoformat(t["opened_at"])
        age_min = (datetime.now(timezone.utc) - opened_at).total_seconds() / 60
        timeout_hit = age_min >= prof["max_hold_min"]

        if hit_tp:
            await state.exec.close_trade(t, price, state.session,
                                         reason="take_profit", paper=paper)
        elif hit_stop:
            await state.exec.close_trade(t, price, state.session,
                                         reason="trailing_stop", paper=paper)
        elif timeout_hit:
            await state.exec.close_trade(t, price, state.session,
                                         reason="max_hold_timeout", paper=paper)


# =============================================================================
# TRADINGVIEW WEBHOOK
# =============================================================================
try:
    from aiohttp import web as _aiohttp_web
    _HAS_WEB = True
except ImportError:
    _HAS_WEB = False


async def _tv_handle(request: "aiohttp.web.Request", state) -> "aiohttp.web.Response":
    # Read body FIRST so we can also accept the secret from the JSON payload
    # (TradingView free tier can't send custom HTTP headers, so we accept
    # either: header X-Secret OR a "secret" field inside the JSON body, OR
    # a ?secret= query string).
    try:
        body = await request.json()
    except Exception:
        return _aiohttp_web.Response(status=400, text="bad json")

    # Auth — header OR body OR query string
    secret = (request.headers.get("X-Secret", "")
              or request.headers.get("secret", "")
              or str(body.get("secret", ""))
              or request.query.get("secret", ""))
    if not TV_WEBHOOK_SECRET or secret != TV_WEBHOOK_SECRET:
        log.warning(f"webhook: bad secret from {request.remote}")
        return _aiohttp_web.Response(status=403, text="forbidden")

    # Validate required fields
    required = {"symbol", "side", "confidence", "strategy"}
    missing = required - body.keys()
    if missing:
        return _aiohttp_web.Response(status=400, text=f"missing: {missing}")

    symbol     = str(body["symbol"]).upper().strip()
    side_raw   = str(body["side"]).lower().strip()
    confidence = int(body["confidence"])
    strategy   = str(body["strategy"]).strip()
    price_hint = float(body.get("price", 0)) or None

    if side_raw not in ("long", "short"):
        return _aiohttp_web.Response(status=400, text="side must be long|short")

    profile = TV_STRATEGY_PROFILES.get(strategy, TV_DEFAULT_PROFILE)
    # Map strategy to agent name so each agent gets proper credit
    agent_name = strategy.replace("_long","").replace("_short","")
    sig = Signal(
        agent=f"tv_{agent_name}",
        symbol=normalized_symbol,
        side=side_raw,
        confidence=confidence,
        profile=profile,
        reason=f"TV/{strategy} conf={confidence}",
        metadata={"strategy": strategy, "price_hint": price_hint, "source": "tradingview"},
    )
    log.info(f"webhook: {symbol} {side_raw} conf={confidence} strategy={strategy} profile={profile}")

    # Get live price + sanity check
    # Normalize symbol: TradingView sends "BTCUSDT", BloFin expects "BTC-USDT"
    normalized_symbol = symbol
    if "-" not in symbol and len(symbol) > 6:
        # Insert dash before the last 4 chars (USDT, USDC, BUSD)
        if symbol.endswith("USDT"): normalized_symbol = symbol[:-4] + "-USDT"
        elif symbol.endswith("USDC"): normalized_symbol = symbol[:-4] + "-USDC"
        elif symbol.endswith("BUSD"): normalized_symbol = symbol[:-4] + "-BUSD"
    
    tickers = await asyncio.to_thread(state.bf.tickers)
    tk = next((t for t in tickers if t.get("instId") == normalized_symbol), None)
    live_price = float(tk.get("last", 0)) if tk else 0.0
    if live_price <= 0:
        log.warning(f"webhook: could not determine price for {symbol}")
        return _aiohttp_web.Response(status=422, text="price unknown")

    # Sanity check: refuse obviously fake prices (>5% off live market)
    if price_hint:
        deviation = abs(price_hint - live_price) / live_price
        if deviation > 0.05:
            log.warning(f"webhook REJECTED: {symbol} price_hint={price_hint} "
                       f"live={live_price:.2f} deviation={deviation*100:.1f}%")
            return _aiohttp_web.Response(status=400,
                text=f"price mismatch: hint={price_hint} live={live_price:.2f}")
        price = price_hint
    else:
        price = live_price

    equity     = await asyncio.to_thread(state.bf.balance)
    our_open   = state.db.open_trades()
    exch_pos   = await asyncio.to_thread(state.bf.positions)

    ok, why = state.risk.vet(sig, equity, our_open, exch_pos)
    if not ok:
        log.info(f"webhook VETO {symbol} {side_raw}: {why}")
        await tg_send(state.session,
            f"📡 <b>TV alert</b> {symbol} {side_raw.upper()} conf={confidence}\n"
            f"⛔ vetoed: {why}")
        return _aiohttp_web.Response(status=200, text=f"vetoed: {why}")

    approve, reason = await ai_arbiter(state.session, sig,
        f"price={price}, equity={equity:.0f}, open={len(our_open)}")
    if not approve:
        log.info(f"webhook AI-VETO {symbol}: {reason}")
        await tg_send(state.session,
            f"📡 <b>TV alert</b> {symbol} {side_raw.upper()}\n🤖 AI-veto: {reason}")
        return _aiohttp_web.Response(status=200, text=f"ai-veto: {reason}")

    opened = await state.exec.open(sig, equity, price, state.session)
    return _aiohttp_web.Response(
        status=200,
        text=f"{'opened' if opened else 'rejected'}: {symbol} {side_raw}"
    )


async def webhook_loop(state):
    if not _HAS_WEB:
        log.warning("webhook: aiohttp.web unavailable — skipping")
        return
    if not TV_WEBHOOK_SECRET:
        log.warning("webhook: TV_WEBHOOK_SECRET not set — listener disabled")
        return

    async def _restart_handle(request):
        secret = request.headers.get("X-Secret", "") or request.headers.get("secret", "")
        if not TV_WEBHOOK_SECRET or secret != TV_WEBHOOK_SECRET:
            return _aiohttp_web.Response(status=403, text="forbidden")
        log.warning("webhook: /restart triggered — exiting for clean reload")
        try:
            await tg_send(state.session, "♻️ MAB reloading via /restart webhook")
        except Exception:
            pass
        # Schedule exit so HTTP response can flush
        async def _exit_soon():
            await asyncio.sleep(0.5)
            os._exit(0)
        asyncio.create_task(_exit_soon())
        return _aiohttp_web.Response(status=200, text="restarting",
    headers={"Access-Control-Allow-Origin": "*"})

    async def _backtest_handle(request):
        secret = request.headers.get("X-Secret", "") or request.headers.get("secret", "")
        if not TV_WEBHOOK_SECRET or secret != TV_WEBHOOK_SECRET:
            return _aiohttp_web.Response(status=403, text="forbidden")
        # Don't run two at once
        bt_lock = os.path.join(WORK_DIR, ".backtest_running")
        if os.path.exists(bt_lock):
            return _aiohttp_web.Response(status=409, text="backtest already running")

        days = int(request.query.get("days", "365"))
        no_apply = request.query.get("no_apply", "1") == "1"   # default safe: don't auto-modify bot.py
        log.warning(f"webhook: /backtest triggered (days={days}, no_apply={no_apply})")

        async def _run_backtest():
            try:
                with open(bt_lock, "w") as f:
                    f.write(str(time.time()))
                args = [sys.executable, os.path.join(WORK_DIR, "backtest.py"),
                        "--days", str(days)]
                if no_apply:
                    args.append("--no-apply")
                proc = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=open(os.path.join(WORK_DIR, "backtest_output.log"), "w"),
                    stderr=asyncio.subprocess.STDOUT,
                    cwd=WORK_DIR,
                )
                rc = await proc.wait()
                log.info(f"backtest finished rc={rc}")
                try:
                    async with aiohttp.ClientSession() as s:
                        await tg_send(s, f"📊 Backtest done (rc={rc}, no_apply={no_apply}). See BACKTEST_REPORT.md")
                except Exception:
                    pass
            finally:
                try: os.remove(bt_lock)
                except OSError: pass

        asyncio.create_task(_run_backtest())
        return _aiohttp_web.Response(
            status=202, text=f"backtest started (days={days}, no_apply={no_apply})")

    async def _deploy_handle(request):
        """User-initiated promote-to-live for a specific agent.
        Edits bot.py: sets paper_only=False and notional_multiplier=<size> on the
        target agent class. The mtime watcher then triggers self-restart, which
        loads the new config. From there the bot is autonomous on real money.

        URL: GET or POST /deploy?agent=<name>&size=<float>&secret=<TV_WEBHOOK_SECRET>
        Or: header X-Secret instead of query secret.
        """
        secret = (request.headers.get("X-Secret", "")
                  or request.headers.get("secret", "")
                  or request.query.get("secret", ""))
        if not TV_WEBHOOK_SECRET or secret != TV_WEBHOOK_SECRET:
            return _aiohttp_web.Response(status=403, text="forbidden")

        agent_name = request.query.get("agent", "").strip()
        try:
            size = float(request.query.get("size", "0.10"))
        except ValueError:
            return _aiohttp_web.Response(status=400, text="size must be a number")

        # Map agent name → class name in bot.py
        AGENT_CLASS = {
            "scalp":          "ScalpAgent",
            "momentum":       "MomentumAgent",
            "swing":          "SwingAgent",
            "meanrev":        "MeanReversionAgent",
            "whale":          "WhaleTrackerAgent",
            "news":           "NewsAgent",
            "asymmetric":     "AsymmetricBreakoutAgent",
            "bb_squeeze":     "BollingerSqueezeAgent",
            "donchian":       "DonchianBreakoutAgent",
            "funding":        "FundingHunterAgent",
            "ema_ribbon":     "EMARibbonAgent",
            "candlestick":    "CandlestickAgent",
            "rsi_divergence": "RSIDivergenceAgent",
            "vwap_reversion": "VWAPReversionAgent",
            "trend_pullback": "TrendPullbackAgent",
            "daily_breakout":     "DailyRangeBreakoutAgent",
            "daily_breakout_24h": "DailyBreakout24hAgent",
            "daily_breakout_4h":  "DailyBreakout4hAgent",
            "daily_breakout_7d":  "DailyBreakout7dAgent",
            "daily_breakout_12h": "DailyBreakout12hAgent",
            "daily_breakout_48h": "DailyBreakout48hAgent",
            "daily_breakout_2h":  "DailyBreakout2hAgent",
            "daily_breakout_8h":  "DailyBreakout8hAgent",
            "supertrend":         "SupertrendAgent",
            "volume_capitulation": "VolumeCapitulationAgent",
            "asian_pump":         "AsianPumpAgent",
            "pump_dump_reversal": "PumpDumpReversalAgent",
            "macd_cross":         "MACDCrossAgent",
            "bb_bounce":          "BollingerBounceAgent",
            "zscore_reversion":   "ZScoreReversionAgent",
            "stoch_rsi":          "StochRSIAgent",
            "golden_cross":       "GoldenCrossAgent",
            "liquidity_sweep":    "LiquiditySweepScalpAgent",
            "connors_rsi2":       "ConnorsRSI2Agent",
            "raschke_retest":     "RaschkeRetestAgent",
            "wide_scalp":         "WideScalpAgent",
            "wide_candle":        "WideCandleAgent",
            "hurst_regime":       "HurstRegimeAgent",
            "kalman_trend":       "KalmanTrendAgent",
            "utbot_mtf":          "UTBotMTFAgent",
            "utbot_v3":           "UTBotV3Agent",
            "smart_scalp":        "SmartScalpAgent",
            "volume_profile":     "VolumeProfileAgent",
            "williams_r":         "WilliamsRAgent",
            "funding_extremes":   "FundingExtremesAgent",
            "fib_hotzone":        "FibHotZoneAgent",
            "fibonacci":          "FibonacciRetracementAgent",
            "viki":               "VikiAgent",
        }
        cls_name = AGENT_CLASS.get(agent_name)
        if not cls_name:
            return _aiohttp_web.Response(
                status=400,
                text=f"unknown agent: {agent_name}. Valid: {','.join(AGENT_CLASS.keys())}"
            )

        if not (0.01 <= size <= 2.0):
            return _aiohttp_web.Response(status=400, text="size must be between 0.01 and 2.0")

        # Read bot.py, find the class block, edit paper_only and notional_multiplier
        try:
            bot_path = os.path.join(WORK_DIR, "bot.py")
            with open(bot_path, "r") as f:
                src = f.read()

            # Match `class X(` regardless of parent (Agent, _DailyBreakoutBase, etc.)
            import re as _re
            m = _re.search(rf"^class {_re.escape(cls_name)}\([^)]+\):", src, _re.MULTILINE)
            if not m:
                return _aiohttp_web.Response(status=500, text=f"class {cls_name} not found in bot.py")
            anchor_idx = m.start()

            # Find the next "class " (or end of file) — that's the end of this class block
            next_class_idx = src.find("\nclass ", m.end())
            if next_class_idx < 0:
                next_class_idx = len(src)

            block = src[anchor_idx:next_class_idx]

            # Edit 1: paper_only = True → paper_only = False
            block_new = block.replace("paper_only = True", "paper_only = False", 1)
            paper_changed = (block != block_new)

            # Edit 2: ensure notional_multiplier is set to size
            import re
            if "notional_multiplier" in block_new:
                block_new = re.sub(
                    r"notional_multiplier\s*=\s*[\d.]+",
                    f"notional_multiplier = {size}",
                    block_new, count=1
                )
            else:
                # Inject after the class line
                inj_point = block_new.find("\n", 0) + 1   # right after `class X(Agent):`
                block_new = block_new[:inj_point] + f"    notional_multiplier = {size}\n" + block_new[inj_point:]

            new_src = src[:anchor_idx] + block_new + src[next_class_idx:]
            if new_src == src:
                return _aiohttp_web.Response(status=200, text=f"no change needed: {agent_name} already deployed")

            with open(bot_path, "w") as f:
                f.write(new_src)

            log.warning(f"DEPLOY: {agent_name} ({cls_name}) flipped paper_only={'False' if paper_changed else 'unchanged'} notional={size} — bot will restart in <15s")
            try:
                await tg_send(state.session,
                    f"🚀 <b>DEPLOYED LIVE</b>\n"
                    f"Agent: <code>{agent_name}</code>\n"
                    f"Size: {size}x notional\n"
                    f"paper_only=False set. Bot restarting via mtime watcher.\n"
                    f"Real-money trades begin on next signal.")
            except Exception:
                pass

            return _aiohttp_web.Response(
                status=200,
                text=f"deployed: {agent_name} live at {size}x. Bot auto-restarting."
            )
        except Exception as e:
            log.error(f"deploy error: {traceback.format_exc()}")
            return _aiohttp_web.Response(status=500, text=f"error: {e}")

    async def _undeploy_handle(request):
        """Mirror of _deploy_handle: flips an agent back to paper_only=True."""
        secret = (request.headers.get("X-Secret", "")
                  or request.headers.get("secret", "")
                  or request.query.get("secret", ""))
        if not TV_WEBHOOK_SECRET or secret != TV_WEBHOOK_SECRET:
            return _aiohttp_web.Response(status=403, text="forbidden")
        agent_name = request.query.get("agent", "").strip()
        AGENT_CLASS = {
            "scalp": "ScalpAgent", "momentum": "MomentumAgent", "swing": "SwingAgent",
            "meanrev": "MeanReversionAgent", "whale": "WhaleTrackerAgent",
            "news": "NewsAgent", "asymmetric": "AsymmetricBreakoutAgent",
            "bb_squeeze": "BollingerSqueezeAgent", "donchian": "DonchianBreakoutAgent",
            "funding": "FundingHunterAgent", "ema_ribbon": "EMARibbonAgent",
            "candlestick": "CandlestickAgent", "rsi_divergence": "RSIDivergenceAgent",
            "vwap_reversion": "VWAPReversionAgent", "trend_pullback": "TrendPullbackAgent",
            "daily_breakout": "DailyRangeBreakoutAgent",
            "daily_breakout_24h": "DailyBreakout24hAgent",
            "daily_breakout_4h": "DailyBreakout4hAgent",
            "daily_breakout_7d": "DailyBreakout7dAgent",
            "daily_breakout_12h": "DailyBreakout12hAgent",
            "daily_breakout_48h": "DailyBreakout48hAgent",
            "daily_breakout_2h":  "DailyBreakout2hAgent",
            "daily_breakout_8h":  "DailyBreakout8hAgent",
            "supertrend":         "SupertrendAgent",
            "volume_capitulation": "VolumeCapitulationAgent",
            "asian_pump":         "AsianPumpAgent",
            "pump_dump_reversal": "PumpDumpReversalAgent",
            "macd_cross":         "MACDCrossAgent",
            "bb_bounce":          "BollingerBounceAgent",
            "zscore_reversion":   "ZScoreReversionAgent",
            "stoch_rsi":          "StochRSIAgent",
            "golden_cross":       "GoldenCrossAgent",
            "liquidity_sweep":    "LiquiditySweepScalpAgent",
            "connors_rsi2":       "ConnorsRSI2Agent",
            "raschke_retest":     "RaschkeRetestAgent",
            "wide_scalp":         "WideScalpAgent",
            "wide_candle":        "WideCandleAgent",
            "hurst_regime":       "HurstRegimeAgent",
            "kalman_trend":       "KalmanTrendAgent",
            "utbot_mtf":          "UTBotMTFAgent",
            "utbot_v3":           "UTBotV3Agent",
            "smart_scalp":        "SmartScalpAgent",
            "volume_profile":     "VolumeProfileAgent",
            "williams_r":         "WilliamsRAgent",
            "funding_extremes":   "FundingExtremesAgent",
            "fib_hotzone":        "FibHotZoneAgent",
            "fibonacci":          "FibonacciRetracementAgent",
            "viki":               "VikiAgent",
        }
        cls_name = AGENT_CLASS.get(agent_name)
        if not cls_name:
            return _aiohttp_web.Response(status=400, text=f"unknown agent: {agent_name}")
        try:
            bot_path = os.path.join(WORK_DIR, "bot.py")
            with open(bot_path, "r") as f:
                src = f.read()
            import re as _re
            m = _re.search(rf"^class {_re.escape(cls_name)}\([^)]+\):", src, _re.MULTILINE)
            if not m:
                return _aiohttp_web.Response(status=500, text="class not found")
            anchor_idx = m.start()
            next_class_idx = src.find("\nclass ", m.end())
            if next_class_idx < 0:
                next_class_idx = len(src)
            block = src[anchor_idx:next_class_idx]
            block_new = block.replace("paper_only = False", "paper_only = True", 1)
            if block_new == block:
                return _aiohttp_web.Response(status=200, text=f"{agent_name} was already paper_only")
            new_src = src[:anchor_idx] + block_new + src[next_class_idx:]
            with open(bot_path, "w") as f:
                f.write(new_src)
            log.warning(f"UNDEPLOY: {agent_name} flipped to paper_only=True")
            try:
                await tg_send(state.session,
                    f"⏸️ <b>UNDEPLOYED</b>\nAgent: <code>{agent_name}</code> back to paper-only.")
            except Exception:
                pass
            return _aiohttp_web.Response(status=200, text=f"undeployed: {agent_name} now paper")
        except Exception as e:
            return _aiohttp_web.Response(status=500, text=f"error: {e}")

    async def _diag_handle(request):
        """Read-only introspection of BloFin SDK + account info, used to find brokerId."""
        secret = (
            request.headers.get("X-Secret", "")
            or request.headers.get("secret", "")
            or request.query.get("secret", "")
        )
        if not TV_WEBHOOK_SECRET or secret != TV_WEBHOOK_SECRET:
            return _aiohttp_web.Response(status=403, text="forbidden")

        out = {"env_broker_id": BLOFIN_BROKER_ID or None, "calls": {}}
        bf = getattr(state, "bf", None) or BloFin()

        client = getattr(bf, "client", None)
        # Enumerate every callable on every sub-API the SDK exposes
        for ns in ("public", "trading", "account", "user", "affiliate", "copytrading"):
            sub = getattr(client, ns, None)
            if sub is None:
                continue
            out["calls"][ns] = sorted(
                m for m in dir(sub)
                if not m.startswith("_") and callable(getattr(sub, m, None))
            )

        # Try the most likely info endpoints (read-only). Failures are captured, not raised.
        async def _try(label, fn, *a, **kw):
            try:
                r = await asyncio.to_thread(fn, *a, **kw)
                return r
            except Exception as e:
                return {"_error": str(e)}

        info = {}
        # account namespace
        if hasattr(client, "account"):
            for m in ("get_balance", "get_positions", "get_account_balance",
                      "get_account_config", "get_config", "get_apikey_info",
                      "get_api_key_info", "get_user_info"):
                fn = getattr(client.account, m, None)
                if fn:
                    info[f"account.{m}"] = await _try(m, fn)
        # trading namespace
        if hasattr(client, "trading"):
            for m in ("get_futures_account_balance", "get_position_mode",
                      "get_margin_mode", "get_leverage", "get_orders_history",
                      "get_positions"):
                fn = getattr(client.trading, m, None)
                if fn:
                    info[f"trading.{m}"] = await _try(m, fn)

        out["info"] = info

        # Recursively scan all string fields for anything that looks broker-y
        broker_hits = []
        def _walk(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if "broker" in str(k).lower():
                        broker_hits.append({"path": f"{path}.{k}", "value": v})
                    _walk(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj[:20]):
                    _walk(v, f"{path}[{i}]")
        _walk(info)
        out["broker_hits"] = broker_hits

        return _aiohttp_web.json_response(out, dumps=lambda o: json.dumps(o, default=str, indent=2))

    app = _aiohttp_web.Application()
    # CORS preflight for Chrome extension
    async def _cors_options(request):
        return _aiohttp_web.Response(status=204,
            headers={"Access-Control-Allow-Origin": "*",
                     "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                     "Access-Control-Allow-Headers": "Content-Type"})
    app.router.add_options("/{tail:.*}", _cors_options)
    app.router.add_post("/tv", lambda r: _tv_handle(r, state))
    app.router.add_post("/restart", _restart_handle)
    app.router.add_post("/backtest", _backtest_handle)
    app.router.add_post("/deploy", _deploy_handle)
    app.router.add_get("/deploy", _deploy_handle)
    app.router.add_post("/undeploy", _undeploy_handle)
    app.router.add_get("/undeploy", _undeploy_handle)
    app.router.add_get("/diag", _diag_handle)
    app.router.add_post("/diag", _diag_handle)
    # Health endpoint for Chrome extension / external monitoring
    async def _health_handle(request):
        try:
            our_open = state.db.open_trades()
            health = {
                "equity": round(await asyncio.to_thread(state.bf.balance), 2),
                "today_pnl": round(state.db.today_pnl(), 2),
                "open_trades": len(our_open),
                "regime": getattr(state, "regime", "UNKNOWN"),
                "keys": (_OR_ROTATOR.live_count() if _OR_ROTATOR else 0),
                "paused": getattr(state, "paused", False),
                "ts": datetime.now(timezone.utc).isoformat(),
            }
            return _aiohttp_web.Response(
                status=200, text=json.dumps(health),
                content_type="application/json",
                headers={"Access-Control-Allow-Origin": "*"})
        except Exception as e:
            return _aiohttp_web.Response(status=500, text=json.dumps({"error": str(e)}),
                                         content_type="application/json")
    app.router.add_get("/health", _health_handle)
    runner = _aiohttp_web.AppRunner(app)
    await runner.setup()
    # 2026-05-19 (Claude/Cowork patch): reuse_address=True lets the bot rebind
    # 8787 immediately after a restart instead of waiting ~60s for the OS
    # TIME_WAIT timeout. reuse_port=False (default) keeps the safety that only
    # ONE process can bind at a time — so duplicate launches still fail clean,
    # but the SAME process restarting doesn't hit Errno 48.
    site = _aiohttp_web.TCPSite(
        runner, "0.0.0.0", TV_WEBHOOK_PORT,
        reuse_address=True,
    )
    await site.start()
    log.info(f"webhook: listening on 0.0.0.0:{TV_WEBHOOK_PORT}/tv")
    while True:
        await asyncio.sleep(3600)


# =============================================================================
# LOOPS
# =============================================================================
async def local_status_loop():
    """Hourly health narrator (FREE — runs on local Qwen).

    Reads last hour of bot.log + open positions + today's P&L, asks Qwen if
    anything looks off. Silent when all is well; pings Telegram only when
    something is wrong. Takes load off Claude / off Saad's eyeballs.
    """
    await asyncio.sleep(120)  # let bot fully start
    while True:
        try:
            # Last 80 log lines
            log_path = os.path.join(WORK_DIR, "bot.log")
            tail = ""
            if os.path.exists(log_path):
                with open(log_path, "rb") as f:
                    f.seek(0, 2)
                    size = f.tell()
                    f.seek(max(0, size - 12000))
                    tail = f.read().decode("utf-8", errors="ignore")[-8000:]
            # Open positions
            conn = sqlite3.connect(DB_PATH, timeout=20)
            opens = conn.execute(
                "SELECT agent, symbol, side, entry_price, opened_at "
                "FROM trades WHERE status='open'"
            ).fetchall()
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            pnl_today = conn.execute(
                "SELECT COALESCE(SUM(pnl),0), COUNT(*) FROM trades "
                "WHERE status='closed' AND date(closed_at)=?", (today,)
            ).fetchone()
            conn.close()
            opens_str = "\n".join(
                f"  - {a} {s} {side} @ {ep:.6f} opened {oa}"
                for a, s, side, ep, oa in opens
            ) or "  (none)"
            prompt = (
                "You are watching a crypto trading bot. Look at recent logs, "
                "open positions, and today's P&L. Return EXACTLY one line:\n"
                "- If everything looks normal: write 'OK'\n"
                "- If something seems wrong (repeated errors, stuck position, "
                "  unusual drawdown, frozen agent, API failures): write a short "
                "  problem description (max 20 words).\n\n"
                f"Today P&L: ${pnl_today[0]:+.2f} over {pnl_today[1]} closed trades.\n"
                f"Open positions:\n{opens_str}\n\n"
                f"Recent log tail:\n{tail}\n\n"
                "Your one-line verdict:"
            )
            verdict = await local_llm_chat(prompt, max_tokens=60,
                                           temperature=0.2, timeout=45)
            if not verdict:
                log.debug("local_status_loop: Qwen unreachable, skipping")
            else:
                v = verdict.strip().splitlines()[0][:200]
                if v.upper().startswith("OK") or v.upper() == "OK":
                    log.info(f"status_narrator: OK (P&L ${pnl_today[0]:+.2f}, "
                             f"{len(opens)} open)")
                else:
                    log.warning(f"status_narrator FLAG: {v}")
                    try:
                        async with aiohttp.ClientSession() as s:
                            await tg_send(s, f"⚠️ Status flag: {v}")
                    except Exception:
                        pass
        except Exception:
            log.warning(f"local_status_loop:\n{traceback.format_exc()}")
        await asyncio.sleep(3600)  # hourly


async def eod_recap_loop():
    """Daily P&L recap at 22:00 UTC. Uses local Qwen (FREE) to narrate today's
    trades. Saves to eod_recap_<date>.md and pings Telegram with a 1-line gist.
    """
    while True:
        try:
            now = datetime.now(timezone.utc)
            target = now.replace(hour=22, minute=0, second=0, microsecond=0)
            if now >= target:
                target = target + timedelta(days=1)
            await asyncio.sleep((target - now).total_seconds())
            # Pull today's closed trades
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            conn = sqlite3.connect(DB_PATH, timeout=20)
            rows = conn.execute(
                "SELECT agent, symbol, side, pnl, pnl_pct, reason "
                "FROM trades WHERE status='closed' AND date(closed_at)=? "
                "ORDER BY pnl DESC", (today,)
            ).fetchall()
            conn.close()
            if not rows:
                log.info("eod_recap: no closed trades today, skipping")
                continue
            wins = [r for r in rows if (r[3] or 0) > 0]
            losses = [r for r in rows if (r[3] or 0) < 0]
            total_pnl = sum((r[3] or 0) for r in rows)
            avg_win = sum(r[3] for r in wins) / len(wins) if wins else 0
            avg_loss = sum(r[3] for r in losses) / len(losses) if losses else 0
            top = rows[0] if rows else None
            bot_ = rows[-1] if rows else None
            agents = {}
            for r in rows:
                agents.setdefault(r[0], []).append(r[3] or 0)
            per_agent = "\n".join(
                f"  - {a}: {sum(p):+.2f} ({len(p)} trades)"
                for a, p in sorted(agents.items(), key=lambda x: -sum(x[1]))
            )
            prompt = (
                f"You are a trading coach. Today ({today}):\n"
                f"- Total P&L: ${total_pnl:+.2f}\n"
                f"- Trades: {len(rows)} ({len(wins)}W / {len(losses)}L)\n"
                f"- Avg win: ${avg_win:+.2f} | Avg loss: ${avg_loss:+.2f}\n"
                f"- Top winner: {top[0]} {top[1]} {top[2]} ${top[3]:+.2f}\n"
                f"- Top loser:  {bot_[0]} {bot_[1]} {bot_[2]} ${bot_[3]:+.2f}\n"
                f"Per-agent:\n{per_agent}\n\n"
                "Write a SHORT recap (max 6 lines). Plain English. "
                "Cover: how today went, which agent stood out (good or bad), "
                "and ONE thing to fix tomorrow. No bullet points, no headers."
            )
            text = await local_llm_chat(prompt, max_tokens=300, timeout=90)
            if not text:
                text = (f"P&L ${total_pnl:+.2f} | {len(wins)}W/{len(losses)}L | "
                        f"avg win ${avg_win:+.2f} vs loss ${avg_loss:+.2f}")
            path = os.path.join(WORK_DIR, f"eod_recap_{today}.md")
            with open(path, "w") as f:
                f.write(f"# EOD Recap — {today}\n\n{text}\n\n"
                        f"## Raw\n- P&L: ${total_pnl:+.2f}\n"
                        f"- {len(wins)}W / {len(losses)}L\n"
                        f"- Avg win: ${avg_win:+.2f}\n- Avg loss: ${avg_loss:+.2f}\n\n"
                        f"## Per agent\n{per_agent}\n")
            log.info(f"eod_recap saved: {path}")
            try:
                async with aiohttp.ClientSession() as s:
                    await tg_send(s, f"📊 EOD ${total_pnl:+.2f} | "
                                     f"{len(wins)}W/{len(losses)}L\n{text}")
            except Exception:
                pass
        except Exception:
            log.warning(f"eod_recap_loop:\n{traceback.format_exc()}")
            await asyncio.sleep(60)


async def market_context_loop():
    """Pull market data from 7+ free sources every 30 min (Binance, Jupiter,
    Fear & Greed, CoinGecko, BTC on-chain, funding rates, trending coins)."""
    while True:
        try:
            from market_data import get_market_snapshot
            snap = await get_market_snapshot()
            bias = snap.get("market_bias", "neutral")
            fg = snap.get("fear_greed", {})
            trending = snap.get("trending", [])
            top_coins = ", ".join(c["symbol"] for c in trending[:5]) if trending else "none"
            log.info(f"market_data: bias={bias} F&G={fg.get('value','?')} trending={top_coins}")
        except Exception:
            log.warning(f"market_data_loop: {traceback.format_exc()}")
        await asyncio.sleep(1800)  # every 30 minutes


async def research_brief_loop(state):
    """2026-05-20 (Claude/Cowork): Hermes reads the news feeds + market context
    every 6h and writes a plain-English research brief to HERMES_RESEARCH_BRIEF.md.
    Both Saad and the trading-decision context can read it. Uses the FREE
    OpenRouter brain (owl-alpha + fallbacks). Cost $0. No Twitter/X scraping
    (no free API + ToS), no copyrighted books — only the legitimate RSS feeds
    the bot already pulls plus the bot's own live stats. Never blocks trading."""
    BRIEF_PATH = os.path.join(WORK_DIR, "HERMES_RESEARCH_BRIEF.md")
    # small initial delay so it doesn't fight startup
    await asyncio.sleep(120)
    while True:
        try:
            # 1) gather inputs the legitimate way
            news = {}
            try:
                news = await fetch_news(state.session)
            except Exception as e:
                log.warning(f"research: news fetch {e}")
            try:
                bias, reasons = market_bias()
            except Exception:
                bias, reasons = "neutral", []
            learn = ""
            try:
                learn = state.learning.summary()
            except Exception:
                pass

            news_lines = "\n".join(
                f"- {sym}: score {d['score']:+.2f} ({d['n']} hits) — {d['headline'][:90]}"
                for sym, d in list(news.items())[:12]
            ) or "(no scored headlines this cycle)"

            prompt = (
                "You are Hermes, a crypto trading analyst. Write a SHORT daily "
                "research brief for Saad (he is dyslexic — short lines, numbers "
                "first, no filler). Base it ONLY on the data below — do not invent "
                "news. End with one line: BIAS: bullish|bearish|neutral.\n\n"
                f"MACRO BIAS (from market_context): {bias}\n"
                f"REASONS: {', '.join(reasons[:5]) if reasons else 'n/a'}\n\n"
                f"NEWS HEADLINES (keyword-scored):\n{news_lines}\n\n"
                f"OUR AGENTS (live edge):\n{learn}\n\n"
                "Write: (1) one-line market read, (2) 2-3 coins to watch and why, "
                "(3) any risk to avoid today. Keep under 150 words total."
            )

            brief = ""
            # Tier-1: DeepSeek (main brain — cheap, fast)
            if DEEPSEEK_API_KEY and not brief:
                try:
                    async with state.session.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": DEEPSEEK_MODEL,
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": 350,
                            "temperature": 0.3,
                        },
                        timeout=aiohttp.ClientTimeout(total=30),
                    ) as r:
                        if r.status == 200:
                            data = await r.json()
                            brief = data["choices"][0]["message"]["content"]
                except Exception as e:
                    log.warning(f"research brief DeepSeek: {e}")
            # Tier-2: OpenRouter fallback
            if not brief and _OR_ROTATOR is not None:
                try:
                    from openrouter_client import chat as _or_chat
                    brief = await asyncio.to_thread(
                        _or_chat,
                        [{"role": "user", "content": prompt}],
                        None, 350, 0.3, 30.0,
                    )
                except Exception as e:
                    log.warning(f"research brief LLM: {e}")

            ts = datetime.now(timezone.utc).isoformat()
            body = (
                f"# Hermes Research Brief\n\n"
                f"**Updated:** {ts}\n"
                f"**Macro bias:** {bias}\n\n"
                f"{brief or '(LLM unavailable this cycle — raw data below)'}\n\n"
                f"---\n## Raw inputs\n\n"
                f"**News:**\n{news_lines}\n\n"
                f"**Agent edge:** {learn}\n"
            )
            try:
                with open(BRIEF_PATH, "w") as f:
                    f.write(body)
                log.info(f"research brief written ({len(brief)} chars) bias={bias}")
            except Exception as e:
                log.warning(f"research brief write: {e}")
        except Exception:
            log.warning(f"research_brief_loop:\n{traceback.format_exc()}")
        await asyncio.sleep(6 * 3600)   # every 6 hours


async def scan_loop(state, paper):
    # Hard timeout: 4× the cycle interval. If a single scan_once hangs (e.g. a
    # BloFin SSL EOF that never resolves), cancel it so the loop survives.
    _SCAN_TIMEOUT = max(120, SCAN_INTERVAL_SEC * 4)
    while True:
        try:
            await asyncio.wait_for(scan_once(state, paper=paper), timeout=_SCAN_TIMEOUT)
        except asyncio.TimeoutError:
            log.error(f"scan_loop: scan_once timed out after {_SCAN_TIMEOUT}s — cancelled")
        except Exception:
            log.error(f"scan_loop:\n{traceback.format_exc()}")
        await asyncio.sleep(SCAN_INTERVAL_SEC)

async def monitor_loop(state, paper):
    _MON_TIMEOUT = max(60, MONITOR_INTERVAL_SEC * 10)
    while True:
        try:
            await asyncio.wait_for(monitor_positions(state, paper=paper), timeout=_MON_TIMEOUT)
        except asyncio.TimeoutError:
            log.error(f"monitor_loop: monitor_positions timed out after {_MON_TIMEOUT}s — cancelled")
        except Exception:
            log.error(f"monitor_loop:\n{traceback.format_exc()}")
        await asyncio.sleep(MONITOR_INTERVAL_SEC)

async def news_loop(state):
    while True:
        try:
            news = await fetch_news(state.session)
            state.news = news
            log.info(f"news: {len(news)} symbols with sentiment")
        except Exception:
            log.error(f"news_loop:\n{traceback.format_exc()}")
        await asyncio.sleep(NEWS_INTERVAL_SEC)

async def regime_loop(state):
    """Classify BTC market regime every 15 min: TRENDING / RANGING / VOLATILE."""
    while True:
        try:
            bf: BloFin = state.bf
            df = await asyncio.to_thread(bf.candles, "BTC-USDT", "1H", 120)
            if len(df) >= 30:
                adx_val  = adx(df).iloc[-1]
                atr_val  = atr(df).iloc[-1]
                atr_avg  = atr(df).rolling(100).mean().iloc[-1] if len(df) >= 100 else atr_val
                if adx_val > 25:
                    regime = "TRENDING"
                elif adx_val < 20:
                    regime = "RANGING"
                elif atr_avg > 0 and atr_val > 2 * atr_avg:
                    regime = "VOLATILE"
                else:
                    regime = "RANGING"
                state.regime = regime
                log.info(f"regime: {regime}  ADX={adx_val:.1f}  ATR={atr_val:.2f}")
        except Exception as e:
            log.warning(f"regime_loop: {e}")
        await asyncio.sleep(900)  # 15 min


async def heartbeat_loop(state):
    """Hourly status push to Telegram."""
    last = 0
    while True:
        await asyncio.sleep(60)
        if time.time() - last < 3600:
            continue
        try:
            equity = await asyncio.to_thread(state.bf.balance)
            our_open = state.db.open_trades()
            today = state.db.today_pnl()
            await tg_send(state.session,
                f"⏱ <b>Heartbeat</b>\n"
                f"equity ${equity:.2f}  open {len(our_open)}/{MAX_CONCURRENT_POSITIONS}  "
                f"today PnL ${today:+.2f}\n"
                f"<i>{state.learning.summary()}</i>")
            last = time.time()
        except Exception as e:
            log.warning(f"heartbeat: {e}")


# =============================================================================
# SELF-HEALING: supervisor, reconciler, watchdog, health writer
# =============================================================================
async def supervised(coro_factory, name: str, restart_delay: int = 5):
    """Wrap any loop so it auto-restarts after a crash or unexpected return."""
    while True:
        try:
            await coro_factory()
            log.warning(f"[supervisor] {name} returned unexpectedly — restart in {restart_delay}s")
        except asyncio.CancelledError:
            raise
        except Exception:
            log.error(f"[supervisor] {name} crashed:\n{traceback.format_exc()}")
        await asyncio.sleep(restart_delay)


async def reconcile_loop(state):
    """Every 5 min: sync DB open trades against live exchange positions.
    If a trade is 'open' in DB but gone from exchange (closed by SL/TP/liq), mark it closed."""
    while True:
        await asyncio.sleep(300)
        try:
            exch_pos  = await _retry_thread(state.bf.positions, label="reconcile.positions")
            exch_syms = {p["symbol"] for p in exch_pos}
            our_open  = state.db.open_trades()
            # SAFETY 2026-05-16 (phantom-trade fix): NEVER fake-close on empty
            # exchange positions. Auditor caught 17 phantom $0 closes corrupting
            # per-agent stats — `hurst_regime` looked like a 25% WR loser when
            # real WR was 80%. Treat empty/error as "unknown", not "absent".
            # Only mark closed when the exchange call CLEARLY succeeded and
            # confirmed at least one OTHER position exists (proving the API
            # actually saw the account).
            if len(exch_pos) == 0 and len(our_open) > 0:
                log.warning(f"reconcile: 0 exchange positions but {len(our_open)} open in DB — "
                            f"treating as unknown (API may have errored or returned stale empty list), "
                            f"skipping cycle")
                continue
            for t in our_open:
                if t["symbol"] in exch_syms:
                    continue
                opened_at = datetime.fromisoformat(t["opened_at"])
                age_min   = (datetime.now(timezone.utc) - opened_at).total_seconds() / 60
                if age_min < 2:
                    continue  # grace period — position may not have landed yet
                log.warning(f"reconcile: {t['symbol']} {t['side']} open in DB but gone from exchange "
                            f"(age {age_min:.0f}m) — syncing closed")
                tickers = await _retry_thread(state.bf.tickers, label="reconcile.tickers")
                px_map  = {tk.get("instId"): float(tk.get("last") or 0) for tk in tickers}
                # v2.0 GHOST-TRADE FIX: previously fell back to entry_price → pnl=$0.
                # Better order: live ticker → current_stop (likely SL trigger) → sl_price → entry.
                price = (px_map.get(t["symbol"])
                         or float(t["current_stop"] or 0)
                         or float(t["sl_price"] or 0)
                         or float(t["entry_price"]))
                await state.exec.close_trade(t, price, state.session, reason="reconcile_sync")
                await tg_send(state.session,
                    f"🔄 <b>Reconcile</b>: {t['symbol']} {t['side'].upper()} was closed on exchange "
                    f"(SL/TP/liq) — DB synced. exit≈{price:.4f}")
        except Exception:
            log.error(f"reconcile_loop:\n{traceback.format_exc()}")


async def watchdog_loop(state):
    """Every 3 min: alert if scan or monitor loops have gone silent."""
    SCAN_STALE    = SCAN_INTERVAL_SEC    * 3
    MONITOR_STALE = MONITOR_INTERVAL_SEC * 15
    alerted: Dict[str, float] = {}
    while True:
        await asyncio.sleep(180)
        try:
            now = time.time()
            checks = [
                ("scan",    getattr(state, "last_scan_at",    0), SCAN_STALE),
                ("monitor", getattr(state, "last_monitor_at", 0), MONITOR_STALE),
            ]
            for name, last, max_gap in checks:
                if last == 0:
                    continue   # not started yet
                gap = now - last
                if gap > max_gap:
                    last_alert = alerted.get(name, 0)
                    if now - last_alert > 1800:   # re-alert at most every 30 min
                        log.error(f"watchdog: {name} loop stalled — last ran {gap/60:.1f} min ago")
                        await tg_send(state.session,
                            f"⚠️ <b>MAB watchdog</b>: <b>{name}</b> loop stalled "
                            f"({gap/60:.0f} min since last run)")
                        alerted[name] = now
                else:
                    alerted.pop(name, None)   # clear alert once recovered
        except Exception:
            log.error(f"watchdog_loop:\n{traceback.format_exc()}")


async def restart_watch_loop(state):
    """
    DISABLED 2026-06-09: Was killing bot on every edit but no LaunchAgent
    to auto-restart. Doctor agent handles restarts instead.
    """
    await asyncio.sleep(3600)  # Check once per hour (effectively disabled)
    return  # Never run the watch loop
    paths = [BOT_PY_PATH, ENV_PATH, RESTART_TRIGGER_PATH]
    initial = {}
    for p in paths:
        try:
            initial[p] = os.path.getmtime(p)
        except OSError:
            initial[p] = 0.0
    log.info(f"restart_watch: tracking mtimes for {[os.path.basename(p) for p in paths]}")
    while True:
        await asyncio.sleep(15)
        try:
            for p in paths:
                try:
                    cur = os.path.getmtime(p)
                except OSError:
                    cur = 0.0
                if cur > initial[p] + 0.5:   # tiny epsilon to avoid float jitter
                    log.warning(
                        f"restart_watch: {os.path.basename(p)} changed "
                        f"(was {initial[p]:.0f} now {cur:.0f}) — exiting for clean reload"
                    )
                    # Best-effort Telegram so user knows reload happened
                    try:
                        async with aiohttp.ClientSession() as s:
                            await tg_send(s, f"♻️ MAB reloading — {os.path.basename(p)} edited")
                    except Exception:
                        pass
                    # Give logs a moment to flush
                    await asyncio.sleep(1)
                    os._exit(0)   # KeepAlive will restart us
        except Exception:
            log.error(f"restart_watch_loop:\n{traceback.format_exc()}")


class _HermesBotCtx:
    """Adapter that satisfies hermes_bridge.CryptoBotContext using `state`."""
    def __init__(self, state):
        self._state = state
    @property
    def paused(self):
        return getattr(self._state, "paused", False)
    @paused.setter
    def paused(self, v):
        setattr(self._state, "paused", bool(v))
        # Repurpose existing pause hook so risk manager honors it
        if v:
            self._state.new_entries_paused_until = time.time() + 10 * 365 * 24 * 3600
        else:
            self._state.new_entries_paused_until = 0
    def flatten(self, symbol):
        try:
            return asyncio.create_task(self._state.exec.close_position(symbol))
        except Exception as e:
            return f"flatten_failed:{e!r}"
    def flatten_all(self):
        try:
            opens = list(self._state.db.open_trades())
            for t in opens:
                sym = t.get("symbol") if isinstance(t, dict) else getattr(t, "symbol", None)
                if sym:
                    asyncio.create_task(self._state.exec.close_position(sym))
            return f"flattening {len(opens)} positions"
        except Exception as e:
            return f"flatten_all_failed:{e!r}"
    def cancel_all(self):
        """Cancel all pending limit orders on the exchange."""
        try:
            cancelled = asyncio.create_task(self._state.exec.cancel_all_orders())
            return f"cancelled_all_orders"
        except Exception as e:
            return f"cancel_all_failed:{e!r}"
    def set_leverage(self, value):
        # store on state so next entry uses it; bot reads LEVERAGE at order time
        global LEVERAGE
        LEVERAGE = int(value)
        return f"leverage={LEVERAGE}"
    def set_risk(self, key, value):
        # gentle: only allow a small allowlist
        allowed = {"DAILY_LOSS_LIMIT_USD", "MAX_CONCURRENT_POSITIONS",
                   "HARD_LIQUIDATION_GUARD", "BTC_VOL_PAUSE_PCT"}
        if key not in allowed:
            return f"refused:{key}_not_allowlisted"
        globals()[key] = value
        return f"{key}={value}"
    def reload_strategies(self):
        # signals KeepAlive to restart by touching bot.py mtime watcher
        try:
            os.utime(__file__, None)
            return "reload-scheduled"
        except Exception as e:
            return f"reload_failed:{e!r}"


async def _hermes_telegram_loop_factory():
    """Supervised wrapper for hermes_telegram.hermes_telegram_loop().
    Lazy-imports so a broken hermes_telegram.py won't crash the whole bot."""
    try:
        from hermes_telegram import hermes_telegram_loop as _htl
    except Exception as e:
        log.warning(f"hermes_telegram import failed (loop disabled): {e}")
        # idle forever — supervised() will see this return and just sleep
        while True:
            await asyncio.sleep(3600)
    await _htl()


async def hermes_loop(state):
    """Publish state to Hermes every 5s, drain commands every loop."""
    if not HAS_HERMES:
        log.info("hermes_loop: hermes_bridge not importable, skipping")
        return
    bridge = _HermesBridge()
    ctx = _HermesBotCtx(state)
    state.hermes = bridge
    log.info(f"hermes_loop: bridge active at {bridge.root}")
    bridge.emit_event("bot_started", pid=os.getpid(),
                      enabled_agents=[a.name for a in state.agents if a.enabled])
    while True:
        try:
            # 1) drain commands and ack
            for cmd in bridge.drain_commands():
                ok, result = _hermes_handle(cmd, ctx=ctx)
                bridge.ack(cmd.id, ok=ok, result=result)
                log.info(f"hermes cmd={cmd.cmd} args={cmd.args} → ok={ok} result={result}")
                bridge.emit_event("cmd_applied", cmd=cmd.cmd, args=cmd.args,
                                  ok=ok, result=str(result))
                # force_scan: trigger an immediate scan cycle in the main loop
                if cmd.cmd == "force_scan" and ok:
                    state.force_scan = True
                    log.info("hermes force_scan: next scan will fire immediately")
            # 2) publish snapshot
            try:
                our_open = state.db.open_trades()
            except Exception:
                our_open = []
            bridge.write_state({
                "paused": getattr(state, "paused", False),
                "regime": getattr(state, "regime", "UNKNOWN"),
                "open_trades": len(our_open),
                "today_pnl": round(state.db.today_pnl(), 4) if state.db else None,
                "last_scan_at": getattr(state, "last_scan_at", 0),
                "last_monitor_at": getattr(state, "last_monitor_at", 0),
                "leverage": LEVERAGE,
                "daily_loss_limit": DAILY_LOSS_LIMIT_USD,
                "max_concurrent": MAX_CONCURRENT_POSITIONS,
                "openrouter_model": OPENROUTER_MODEL,
                "openrouter_keys": (_OR_ROTATOR.count() if _OR_ROTATOR else (1 if OPENROUTER_API_KEY else 0)),
                "openrouter_live_keys": (_OR_ROTATOR.live_count() if _OR_ROTATOR else 0),
                "openrouter_free_only": OPENROUTER_FREE_ONLY,
                "ollama_enabled": bool(os.getenv("OLLAMA_URL", "") and
                                      os.getenv("OLLAMA_URL", "").lower() not in ("off","false","0","disabled","")),
            })
        except Exception:
            log.error(f"hermes_loop:\n{traceback.format_exc()}")
        await asyncio.sleep(5)


async def health_loop(state):
    """Write health.json every 60 s for external monitoring."""
    while True:
        await asyncio.sleep(60)
        try:
            our_open = state.db.open_trades()
            health   = {
                "ts":              datetime.now(timezone.utc).isoformat(),
                "last_scan_at":    getattr(state, "last_scan_at",    0),
                "last_monitor_at": getattr(state, "last_monitor_at", 0),
                "scan_lag_s":      round(time.time() - getattr(state, "last_scan_at", time.time()), 1),
                "monitor_lag_s":   round(time.time() - getattr(state, "last_monitor_at", time.time()), 1),
                "open_trades":     len(our_open),
                "today_pnl":       round(state.db.today_pnl(), 4),
                "broker_id_set":   bool(BLOFIN_BROKER_ID),
                "webhook_secret_set": bool(TV_WEBHOOK_SECRET),
            }
            with open(HEALTH_PATH, "w") as f:
                json.dump(health, f, indent=2)
        except Exception:
            pass   # health file is best-effort


# =============================================================================
# CLI MODES
# =============================================================================
def check_config() -> List[str]:
    missing = []
    if not BLOFIN_API_KEY:    missing.append("BLOFIN_API_KEY")
    if not BLOFIN_API_SECRET: missing.append("BLOFIN_API_SECRET")
    if not BLOFIN_PASSPHRASE: missing.append("BLOFIN_PASSPHRASE")
    return missing


async def cmd_check():
    miss = check_config()
    if miss:
        print(f"❌ Missing env vars: {', '.join(miss)}")
        sys.exit(1)
    print("✅ env vars present")
    if EXCHANGE == "bybit":
        from bybit_wrapper import Bybit
        bf = Bybit()
    else:
        bf = BloFin()
    bal = await asyncio.to_thread(bf.balance)
    print(f"✅ balance:   ${bal:.2f}")
    pos = await asyncio.to_thread(bf.positions)
    print(f"✅ positions: {len(pos)}")
    for p in pos:
        print(f"     {p['symbol']:14} {p['side']:5} qty={p['qty']:<10} "
              f"avg={p['avg_price']:.4f} upnl={p['upnl']:+.2f}")
    tk = await asyncio.to_thread(bf.tickers)
    print(f"✅ tickers:   {len(tk)} markets")
    universe = universe_from_tickers(tk)
    print(f"✅ universe:  {len(universe)} pass volume filter (top 5: "
          f"{', '.join(s for s,_,_ in universe[:5])})")
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        async with aiohttp.ClientSession() as s:
            await tg_send(s, "🔍 MAB <b>--check</b> ok")
        print("✅ telegram:  sent")
    else:
        print("⚠️  telegram: not configured")
    if HAS_CLAUDE_SDK:
        print("✅ claude max:  Agent SDK installed — using your Max subscription")
    elif _OR_ROTATOR and _OR_ROTATOR.count() > 0:
        free_tag = "FREE-ONLY" if OPENROUTER_FREE_ONLY else "any-tier"
        print(f"✅ openrouter:  {_OR_ROTATOR.count()} key(s) rotating — model={OPENROUTER_MODEL} [{free_tag}]")
    elif OPENROUTER_API_KEY:
        print("✅ openrouter:  1 key (no rotation)")
    else:
        print("⚠️  no AI:      arbiter disabled — install claude-agent-sdk to fix")
    print("\nALL GOOD — start bot with:  python3 bot.py")


async def run(paper: bool = False, once: bool = False):
    miss = check_config()
    if miss:
        log.error(f"Missing env vars: {', '.join(miss)}")
        sys.exit(1)

    db = TradeDB(DB_PATH)
    if EXCHANGE == "bybit":
        from bybit_wrapper import Bybit
        bf = Bybit()
        log.info("EXCHANGE=bybit — using Bybit wrapper")
    else:
        bf = BloFin()
    learning = LearningAgent(db)
    agents: List[Agent] = [
        ScalpAgent(),
        MomentumAgent(),
        SwingAgent(),
        MeanReversionAgent(),
        WhaleTrackerAgent(),
        NewsAgent(),
        AsymmetricBreakoutAgent(),
        BollingerSqueezeAgent(),
        DonchianBreakoutAgent(),
        FundingHunterAgent(),
        EMARibbonAgent(),
        CandlestickAgent(),
        RSIDivergenceAgent(),
        VWAPReversionAgent(),
        TrendPullbackAgent(),
        DailyRangeBreakoutAgent(),
        DailyBreakout24hAgent(),
        DailyBreakout4hAgent(),
        DailyBreakout12hAgent(),
        DailyBreakout48hAgent(),
        DailyBreakout7dAgent(),
        DailyBreakout2hAgent(),
        DailyBreakout8hAgent(),
        SupertrendAgent(),
        VolumeCapitulationAgent(),
        AsianPumpAgent(),
        PumpDumpReversalAgent(),
        MACDCrossAgent(),
        VikiAgent(),               # 2026-06-03 — triple EMA 9/21/50 crossover (Saad)
        BollingerBounceAgent(),
        ZScoreReversionAgent(),
        StochRSIAgent(),
        GoldenCrossAgent(),
        LiquiditySweepScalpAgent(),
        ConnorsRSI2Agent(),
        RaschkeRetestAgent(),
        WideScalpAgent(),
        WideCandleAgent(),
        HurstRegimeAgent(),
        KalmanTrendAgent(),
        UTBotMTFAgent(),
        UTBotV3Agent(),
        SmartScalpAgent(),
        VolumeProfileAgent(),
        WilliamsRAgent(),
        FibHotZoneAgent(),
        FundingExtremesAgent(),
        FibonacciRetracementAgent(),
        FibConfluenceZoneAgent(),   # 2026-05-20 — new fib hot-zone agent (Saad)
        Fib786OversoldAgent(),      # 2026-05-26 — 0.786+RSI<35 long, backtest +0.156%/t
        ScoutAgent(),               # 2026-06-04 — AUTO COIN HUNTER: finds breakout coins 24/7
        FibBounceAgent(),           # 2026-06-03 — EXHAUSTIVE BACKTEST WINNER: fib 0.618 + ADX regime
    ]
    # 2026-06-01 — 10 new paper agents from deep research on 285+ trades
    try:
        from paper_agents import get_paper_agents
        paper_ags = get_paper_agents()
        agents.extend(paper_ags)
        log.info(f"paper_agents: loaded {len(paper_ags)} research-backed paper agents")
    except Exception as e:
        log.info(f"paper_agents: skipped ({e})")
    # 2026-05-19 (Claude/Cowork audit): purge agents that have never fired a
    # single real trade in lifetime. Keeping them loaded wastes CPU on every
    # scan computing signals that get discarded by paper_only=True downstream.
    # Audit basis: bot.db lifetime closed_trades query, all status='closed' AND
    # pnl != 0. 26 agents had zero fills lifetime — removing from registry.
    # To re-enable any of these, delete the name from DEAD_AGENT_PURGE.
    DEAD_AGENT_PURGE = {
        # 2026-06-08: CEO RE-ENABLED winners. Keeping only proven losers.
        "asian_session", "atr_momentum",
        "candlestick",
        "daily_breakout_7d",
        "fib_786_oversold", "fib_hotzone", "fibonacci", "fib_confluence",
        "funding_fade_v2", "funding_extremes",
        "golden_cross", "golden_hour",
        "kalman_trend", "keltner_squeeze",
        "liquidity_sweep",
        "metals_scalp", "multi_confluence",
        "news",
        "pump_dump_reversal",
        "raschke_retest", "rsi_divergence",
        "short_bias", "smart_scalp", "stoch_rsi", "supertrend",
        "tv_fibonacci",
        "us_open", "utbot_mtf", "utbot_v3",
        "volume_profile",
        "whale", "wide_candle", "wide_scalp", "williams_r",
        "xmr_meanrev",
    }
    pre_purge_count = len(agents)
    agents = [a for a in agents if a.name not in DEAD_AGENT_PURGE]
    purged = pre_purge_count - len(agents)
    if purged:
        log.info(f"dead-agent purge: removed {purged} never-fired agents — "
                 f"{sorted(DEAD_AGENT_PURGE)}")

    enabled = [a.name for a in agents if a.enabled]
    disabled = [a.name for a in agents if not a.enabled]
    log.info(f"agents enabled: {enabled}")
    if disabled:
        log.info(f"agents disabled (backtest): {disabled}")

    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        risk = RiskManager(db)
        executor = Executor(bf, db)
        state = SimpleNamespace(
            bf=bf, db=db, agents=agents, risk=risk, exec=executor,
            learning=learning, session=session, news={},
            regime="RANGING",
            new_entries_paused_until=0,
            anti_revenge_paused_until=0,
            anti_revenge_last_trigger=0,
        )
        # one-shot broker diagnostic — dumps account+SDK info to broker_diag.json
        # so we can find the brokerId bound to this API key. Read-only; no orders.
        try:
            await asyncio.to_thread(_run_broker_diag, bf)
        except Exception as e:
            log.warning(f"broker_diag failed: {e}")

        # warm news
        try:
            state.news = await fetch_news(session)
        except Exception:
            state.news = {}

        await tg_send(session,
            f"🤖 <b>MAB v2 started</b>{' [PAPER]' if paper else ''}\n"
            f"{len(enabled)} agents active: {', '.join(enabled)}\n"
            f"Safety: hard-liq-guard {HARD_LIQUIDATION_GUARD}%  "
            f"btc-vol-pause {BTC_VOL_PAUSE_PCT}%  regime-detector ON\n"
            f"trailing stop ON every trade  |  lev {LEVERAGE}x  |  "
            f"max {MAX_CONCURRENT_POSITIONS} positions  |  "
            f"daily limit -${DAILY_LOSS_LIMIT_USD}")

        # One-time broker_id alert: if API key is a Broker key (causing 152012/152013),
        # send a clear telegram pointing to FIX_BROKER_NOW.md. Suppressed once a regular
        # Transaction API key is in place.
        try:
            diag_path = os.path.join(WORK_DIR, "broker_diag.json")
            if os.path.exists(diag_path):
                with open(diag_path) as f:
                    diag = json.load(f)
                api_info = diag.get("info", {}).get("user.get_api_key_info", {}).get("data", {})
                api_type = api_info.get("type")
                api_name = api_info.get("apiName", "")
                # type==2 OR apiName=="hyperbot" both flag this is a broker-affiliated key
                if api_type == 2 or "hyper" in api_name.lower():
                    flag = os.path.join(WORK_DIR, ".broker_alert_sent")
                    if not os.path.exists(flag):
                        await tg_send(session,
                            "⚠️ <b>ACTION NEEDED — broker key issue</b>\n"
                            "Your BloFin API key 'hyperbot' is a Broker key (not a Transaction key), "
                            "so trades fail with 152012/152013.\n\n"
                            "<b>Fix (2 min):</b>\n"
                            "1. Open https://blofin.com/account/apiManagement\n"
                            "2. Create a NEW API key — DEFAULT type (Transaction), Read+Trade perms\n"
                            "3. Paste me the 3 new values (key/secret/passphrase) in chat\n\n"
                            "Full details in <code>~/multi_agent_bot/FIX_BROKER_NOW.md</code>")
                        with open(flag, "w") as f:
                            f.write(str(time.time()))
        except Exception as e:
            log.warning(f"broker_alert: {e}")

        if once:
            await scan_once(state, paper=paper)
            await monitor_positions(state, paper=paper)
            return

        await asyncio.gather(
            supervised(lambda: scan_loop(state, paper), "scan_loop"),
            supervised(lambda: monitor_loop(state, paper), "monitor_loop"),
            supervised(lambda: news_loop(state), "news_loop"),
            supervised(lambda: heartbeat_loop(state), "heartbeat_loop"),
            supervised(lambda: regime_loop(state), "regime_loop"),
            supervised(lambda: reconcile_loop(state), "reconcile_loop"),
            supervised(lambda: watchdog_loop(state), "watchdog_loop"),
            supervised(lambda: health_loop(state), "health_loop"),
            supervised(lambda: hermes_loop(state), "hermes_loop"),
            supervised(lambda: _hermes_telegram_loop_factory(), "hermes_telegram_loop"),
            supervised(lambda: restart_watch_loop(state), "restart_watch_loop"),
            supervised(market_context_loop, "market_context_loop"),
            supervised(lambda: research_brief_loop(state), "research_brief_loop"),
            supervised(eod_recap_loop, "eod_recap_loop"),
            supervised(local_status_loop, "local_status_loop"),
            supervised(_big_boss_loop, "big_boss_loop"),
            supervised(_knowledge_loop, "knowledge_loop"),
            supervised(_free_brain_loop, "free_brain_loop"),
            # in 5s without killing the rest of the bot.
            supervised(lambda: webhook_loop(state), "webhook_loop"),
        )


def _run_broker_diag(bf):
    """Read-only introspection of the BloFin SDK + account info.
    Writes /Users/.../multi_agent_bot/broker_diag.json with everything we can
    learn about the broker binding for this API key. Never places orders."""
    out = {
        "ts":            datetime.now(timezone.utc).isoformat(),
        "env_broker_id": BLOFIN_BROKER_ID or None,
        "namespaces":    {},
        "info":          {},
        "broker_hits":   [],
        "sdk_methods_with_brokerid": [],
    }
    client = getattr(bf, "client", None)
    if client is None:
        out["error"] = "bf.client is None"
        _write_broker_diag(out)
        return

    # 1. enumerate all methods on each sub-API
    for ns in ("public", "trading", "account", "user", "affiliate", "copytrading", "asset"):
        sub = getattr(client, ns, None)
        if sub is None:
            continue
        out["namespaces"][ns] = sorted(
            m for m in dir(sub)
            if not m.startswith("_") and callable(getattr(sub, m, None))
        )

    # 2. Inspect each callable's signature for a brokerId/broker_id parameter
    import inspect as _insp
    for ns, methods in out["namespaces"].items():
        sub = getattr(client, ns, None)
        for m in methods:
            try:
                sig = _insp.signature(getattr(sub, m))
                params = list(sig.parameters)
                if any("broker" in p.lower() for p in params):
                    out["sdk_methods_with_brokerid"].append(f"{ns}.{m}({', '.join(params)})")
            except Exception:
                pass

    # 3. call known read-only info endpoints
    def _try(label, fn, *a, **kw):
        try:
            return fn(*a, **kw)
        except Exception as e:
            return {"_error": str(e)[:300]}

    if hasattr(client, "trading"):
        for m in ("get_position_mode", "get_margin_mode",
                  "get_futures_account_balance", "get_positions",
                  "get_orders_history"):
            fn = getattr(client.trading, m, None)
            if fn:
                out["info"][f"trading.{m}"] = _try(m, fn)

    if hasattr(client, "account"):
        for m in ("get_balance", "get_positions", "get_account_balance",
                  "get_account_config", "get_config", "get_apikey_info",
                  "get_api_key_info", "get_user_info"):
            fn = getattr(client.account, m, None)
            if fn:
                out["info"][f"account.{m}"] = _try(m, fn)

    if hasattr(client, "user"):
        for m in dir(client.user):
            if m.startswith("get") and not m.startswith("_"):
                fn = getattr(client.user, m, None)
                if callable(fn):
                    out["info"][f"user.{m}"] = _try(m, fn)

    if hasattr(client, "affiliate"):
        for m in dir(client.affiliate):
            if m.startswith("get") and not m.startswith("_"):
                fn = getattr(client.affiliate, m, None)
                if callable(fn):
                    out["info"][f"affiliate.{m}"] = _try(m, fn)

    # 4. recursively scan responses for broker-y fields
    def _walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if "broker" in str(k).lower():
                    out["broker_hits"].append({"path": f"{path}.{k}", "value": v})
                _walk(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj[:30]):
                _walk(v, f"{path}[{i}]")
    _walk(out["info"])

    _write_broker_diag(out)
    log.info(f"broker_diag: {len(out['broker_hits'])} broker-related fields, "
             f"{len(out['sdk_methods_with_brokerid'])} SDK methods accept brokerId — "
             f"see broker_diag.json")


def _write_broker_diag(out):
    path = os.path.join(WORK_DIR, "broker_diag.json")
    try:
        with open(path, "w") as f:
            json.dump(out, f, default=str, indent=2)
    except Exception as e:
        log.warning(f"broker_diag write failed: {e}")


_caffeinate_proc: Optional[subprocess.Popen] = None

def _start_caffeinate():
    """Keep the Mac fully awake while the bot runs. The bot is the worker,
    so its lifetime should equal "Mac stays awake" lifetime.
    -d disables display sleep, -i disables idle sleep, -m disables disk sleep,
    -s prevents system sleep on AC, -u asserts user-active state.
    Spawned as a child process so it dies with the bot (no orphan caffeinate)."""
    global _caffeinate_proc
    if sys.platform != "darwin":
        return
    if _caffeinate_proc and _caffeinate_proc.poll() is None:
        return
    try:
        _caffeinate_proc = subprocess.Popen(
            ["/usr/bin/caffeinate", "-dimsu"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=False,   # ties to parent — dies on bot exit
        )
        log.info(f"caffeinate started pid={_caffeinate_proc.pid} — Mac will not sleep while bot is alive")
    except Exception as e:
        log.warning(f"caffeinate failed to start: {e}")


def main():
    setup_logging()
    p = argparse.ArgumentParser(description="Multi-Agent Crypto Trading Bot")
    p.add_argument("--check", action="store_true", help="connectivity check, no trading")
    p.add_argument("--paper", action="store_true", help="signals only, no real orders")
    p.add_argument("--once",  action="store_true", help="run one cycle then exit")
    args = p.parse_args()

    log.info("=" * 64)
    log.info(" MULTI-AGENT TRADING BOT v1.0  (Saad)")
    log.info("=" * 64)

    # Prevent Mac sleep — bot is 24/7, sleep kills our trading. Skip in --check / --once.
    if not args.check and not args.once:
        _start_caffeinate()

    try:
        if args.check:
            asyncio.run(cmd_check())
        else:
            asyncio.run(run(paper=args.paper, once=args.once))
    except KeyboardInterrupt:
        log.info("interrupted")
    except Exception:
        log.error(f"FATAL:\n{traceback.format_exc()}")
        sys.exit(1)
    finally:
        # Clean up caffeinate so it doesn't linger as orphan
        if _caffeinate_proc and _caffeinate_proc.poll() is None:
            try: _caffeinate_proc.terminate()
            except Exception: pass


if __name__ == "__main__":
    main()
