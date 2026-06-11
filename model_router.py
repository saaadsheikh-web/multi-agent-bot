#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 SMART MODEL ROUTER — tiered intelligence, free-model maximization
=============================================================================
 Strategy:
   TIER 0 (Free, fast) — grammar, spelling, "India" corrections, basic stuff
     Models: qwen/qwen-2.5-72b-instruct:free, meta-llama/llama-3.3-70b-instruct:free,
             google/gemini-2.0-flash-exp:free

   TIER 1 (Free, smart) — daily recaps, trade narratives, agent decisions
     Models: deepseek/deepseek-chat-v3.1:free, deepseek/deepseek-r1:free,
             openrouter/owl-alpha, qwen/qwen-max:free, qwen/qwen3-235b-a22b:free

   TIER 2 (DeepSeek-V2 heavy lifting) — complex trading decisions, strategy design
     Model: deepseek/deepseek-chat (paid but cheap), deepseek/deepseek-r1

   TIER 3 (Fallback) — when all free models are exhausted, use local Ollama
     Models: gemma4:e4b, qwen3:4b

 Chinese free models to rotate through (they're smart and free right now):
   - qwen/qwen-2.5-72b-instruct:free     (Alibaba, 72B, very capable)
   - qwen/qwen-max:free                   (Alibaba, flagship)
   - qwen/qwen3-235b-a22b:free            (Alibaba, 235B MoE)
   - deepseek/deepseek-chat-v3.1:free     (DeepSeek, 685B)
   - deepseek/deepseek-r1:free            (DeepSeek, reasoning)
   - moonshotai/moonshot-v1-8k:free       (Moonshot, Chinese)
   - zhipuai/glm-4-9b:free                (Zhipu, Chinese)
   - 01-ai/yi-large:free                  (01.AI, Chinese)
   - baichuan/baichuan-4:free             (Baichuan, Chinese)
=============================================================================
"""

from __future__ import annotations

import os
import time
import threading
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict


# =============================================================================
# TIER DEFINITIONS
# =============================================================================

@dataclass
class ModelTier:
    name: str
    models: List[str]
    max_tokens: int
    temperature: float
    timeout: float
    description: str


# Tier 0 — Basic tasks (grammar, spelling) — only the best free models
# NO stupid models. NO llama-3.3 (dumb). NO gemini-flash (dumb).
# Only Qwen 72B — smart, Chinese, fast, free.
TIER_0_BASIC = ModelTier(
    name="basic",
    models=[
        "qwen/qwen-2.5-72b-instruct:free",     # Alibaba 72B — smart & free
        "qwen/qwen3-235b-a22b:free",            # Alibaba 235B MoE — very smart
        "deepseek/deepseek-chat-v3.1:free",     # DeepSeek 685B — insanely smart
    ],
    max_tokens=150,
    temperature=0.1,
    timeout=10.0,
    description="Grammar, spelling — only smart free models",
)

# Tier 1 — Smart trading tasks (recaps, agents, decisions)
# Only the SMARTEST free models. DeepSeek + Qwen + top Chinese models.
TIER_1_SMART = ModelTier(
    name="smart",
    models=[
        "deepseek/deepseek-chat-v3.1:free",     # DeepSeek V3.1 685B — #1 pick
        "deepseek/deepseek-r1:free",             # DeepSeek R1 reasoning — #2
        "qwen/qwen3-235b-a22b:free",             # Qwen 235B MoE — #3
        "qwen/qwen-max:free",                    # Qwen flagship — #4
        "openrouter/owl-alpha",                   # Stealth agentic 1M ctx — #5
        "qwen/qwen-2.5-72b-instruct:free",       # Qwen 72B — #6
    ],
    max_tokens=500,
    temperature=0.3,
    timeout=30.0,
    description="Trading decisions — only DeepSeek + Qwen + Owl (the smartest free models)",
)

# Tier 2 — Heavy lifting (DeepSeek-V2 primary, Qwen 235B fallback)
TIER_2_HEAVY = ModelTier(
    name="heavy",
    models=[
        "deepseek/deepseek-chat",                # DeepSeek-V2/V3 — the boss
        "deepseek/deepseek-r1",                   # DeepSeek reasoning — second boss
        "deepseek/deepseek-chat-v3.1:free",       # fallback free
        "qwen/qwen3-235b-a22b:free",              # Qwen 235B — very smart free fallback
    ],
    max_tokens=800,
    temperature=0.2,
    timeout=45.0,
    description="Heavy trading analysis — DeepSeek-V2 + Qwen 235B only",
)


def get_tier(task_type: str) -> ModelTier:
    """Smart router: pick the right tier based on the task."""
    task_lower = task_type.lower() if task_type else ""

    # Small tasks → Tier 0
    small_keywords = ["grammar", "spell", "correct", "typo", "punctuation",
                      "capitalize", "format", "basic", "simple", "translate",
                      "india", "fix text", "proofread", "edit this"]
    if any(kw in task_lower for kw in small_keywords):
        return TIER_0_BASIC

    # Heavy tasks → Tier 2
    heavy_keywords = ["strategy", "analysis", "deep", "complex", "research",
                      "prediction", "forecast", "arbitrage", "portfolio",
                      "risk assessment", "backtest design", "architecture",
                      "heavy", "trading decision", "market analysis"]
    if any(kw in task_lower for kw in heavy_keywords):
        return TIER_2_HEAVY

    # Default → Tier 1
    return TIER_1_SMART


# =============================================================================
# MODEL ROTATOR (tier-aware, rotates through Chinese free models)
# =============================================================================

class ModelRotator:
    """Rotates through models within a tier, tracks per-model rate limits."""

    def __init__(self):
        self._lock = threading.Lock()
        self._usage: Dict[str, int] = defaultdict(int)
        self._cool_until: Dict[str, float] = {}
        self._dead: set = set()  # models that consistently fail

    def pick(self, tier: ModelTier) -> str:
        """Pick the least-used, non-cooled model from the tier."""
        with self._lock:
            now = time.time()
            available = [m for m in tier.models
                        if m not in self._dead
                        and self._cool_until.get(m, 0) <= now]
            if not available:
                # All cooling — return soonest-ready
                return min(tier.models, key=lambda m: self._cool_until.get(m, 0))
            # Pick least-used
            return min(available, key=lambda m: self._usage.get(m, 0))

    def mark_used(self, model: str):
        with self._lock:
            self._usage[model] += 1

    def mark_cool(self, model: str, seconds: float = 60.0):
        with self._lock:
            self._cool_until[model] = time.time() + seconds

    def mark_dead(self, model: str):
        with self._lock:
            self._dead.add(model)

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "usage": dict(self._usage),
                "cooling": {m: max(0, self._cool_until.get(m, 0) - time.time())
                           for m in self._cool_until},
                "dead": list(self._dead),
            }


# Module-level singleton
_MODEL_ROTATOR = ModelRotator()


def get_model_rotator() -> ModelRotator:
    return _MODEL_ROTATOR


# =============================================================================
# SMART CHAT — tiered routing with fallback
# =============================================================================

def smart_chat(messages: List[Dict[str, str]],
               task_type: str = "general",
               max_tokens: Optional[int] = None,
               temperature: Optional[float] = None,
               timeout: Optional[float] = None) -> Tuple[str, str]:
    """Route to the right tier, rotate through free models, fall back gracefully.

    Returns (response_text, model_used).
    """
    import json
    import urllib.request
    import urllib.error

    tier = get_tier(task_type)
    rot = get_model_rotator()

    effective_max_tokens = max_tokens or tier.max_tokens
    effective_temp = temperature or tier.temperature
    effective_timeout = timeout or tier.timeout

    body = json.dumps({
        "model": "",  # filled per-attempt
        "messages": messages,
        "max_tokens": effective_max_tokens,
        "temperature": effective_temp,
    }).encode("utf-8")

    last_err = None
    attempts = min(len(tier.models) * 2, 10)

    for _ in range(attempts):
        model = rot.pick(tier)
        if model in rot._dead:
            continue

        try:
            data = body.decode()
            # Replace model in body
            payload = json.dumps({
                "model": model,
                "messages": messages,
                "max_tokens": effective_max_tokens,
                "temperature": effective_temp,
            }).encode("utf-8")

            # Use any available OpenRouter key
            from openrouter_client import get_rotator as _get_or_rotator
            or_rot = _get_or_rotator()
            key = or_rot.next_key()
            if not key:
                continue

            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=payload,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://infinitylux.co.uk",
                    "X-Title": f"MAB-{tier.name}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=effective_timeout) as r:
                resp = json.loads(r.read().decode("utf-8"))

            text = resp["choices"][0]["message"]["content"].strip()
            rot.mark_used(model)
            or_rot.mark_success(key)
            return text, model

        except urllib.error.HTTPError as e:
            if e.code in (429, 503, 502):
                rot.mark_cool(model, seconds=120)
            elif e.code in (401, 403):
                rot.mark_dead(model)
            last_err = f"HTTP {e.code}"
        except Exception as e:
            rot.mark_cool(model)
            last_err = str(e)

    # All models exhausted — try local Ollama
    try:
        from hermes import _local_chat
        local = _local_chat(messages, max_tokens=effective_max_tokens,
                            temperature=effective_temp, timeout=15)
        if local:
            return local, "ollama-local"
    except Exception:
        pass

    raise Exception(f"All models exhausted (tier={tier.name}): {last_err}")


# =============================================================================
# SIMPLE TASK HELPERS
# =============================================================================

def fix_grammar(text: str) -> str:
    """Quick grammar/spelling fix using Tier 0 (free, fast)."""
    try:
        result, model = smart_chat(
            [{"role": "user", "content":
              f"Fix grammar, spelling, and capitalization in this text. "
              f"Return ONLY the corrected text, no explanation:\n\n{text}"}],
            task_type="grammar",
            max_tokens=len(text) + 100,
            temperature=0.0,
        )
        return result
    except Exception:
        return text  # graceful degradation


def quick_answer(question: str) -> str:
    """Fast answer to a simple question using Tier 1 (free, smart)."""
    result, model = smart_chat(
        [{"role": "user", "content": question}],
        task_type="general",
        max_tokens=300,
    )
    return result


def heavy_analysis(prompt: str, context: str = "") -> str:
    """Deep analysis using DeepSeek-V2 heavy lifting (Tier 2)."""
    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": prompt})

    result, model = smart_chat(
        messages,
        task_type="deep complex trading analysis",
        max_tokens=800,
        temperature=0.2,
        timeout=60,
    )
    return result


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 model_router.py <tier> <prompt>")
        print("  tier: basic | smart | heavy")
        print("  OR: python3 model_router.py grammar 'text to fix'")
        sys.exit(1)

    cmd = sys.argv[1]
    text = " ".join(sys.argv[2:])

    if cmd == "grammar":
        print(fix_grammar(text))
    elif cmd in ("basic", "smart", "heavy"):
        task_map = {"basic": "grammar spelling", "smart": "general", "heavy": "deep complex trading analysis"}
        result, model = smart_chat(
            [{"role": "user", "content": text}],
            task_type=task_map[cmd],
        )
        print(f"[{model}] {result}")
    else:
        print(f"Unknown command: {cmd}")
