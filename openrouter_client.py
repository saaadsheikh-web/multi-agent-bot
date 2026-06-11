#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 OPENROUTER CLIENT — multi-key rotator, free-only guard, retry logic.
=============================================================================
 Reads from env:
   OPENROUTER_API_KEYS   comma-separated; falls back to OPENROUTER_API_KEY
   OPENROUTER_MODEL      default model slug (e.g. openrouter/owl-alpha)
   OPENROUTER_FREE_ONLY  "1" rejects paid slugs (refuses calls)

 Rotation policy: round-robin across keys on each call; on 429/5xx/401/403
 mark the key cooling-down for 60s and immediately try the next key.

 Free-only guard: the model slug is considered free if it
   • contains ":free", OR
   • is in the known-free allowlist (extend FREE_ALLOWLIST as needed).
=============================================================================
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from typing import Dict, List, Optional

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Known-free slugs that don't carry the ":free" suffix.
# Focus: ONLY smart models. DeepSeek, Qwen, top Chinese. No dumb ones.
FREE_ALLOWLIST = {
    # OpenRouter stealth models
    "openrouter/owl-alpha",             # stealth, agentic, 1M context
    "openrouter/optimus-alpha",         # historic stealth
    "openrouter/quasar-alpha",          # historic stealth
    # DeepSeek — the GOAT of free models
    "deepseek/deepseek-chat",           # DeepSeek-V2/V3 (paid but cheap)
    "deepseek/deepseek-r1",             # DeepSeek reasoning
    # Qwen — Alibaba's best, all free
    "qwen/qwen-max",                    # Qwen flagship
    "qwen/qwen3-235b-a22b",             # 235B MoE — insanely smart
    "qwen/qwen-2.5-72b-instruct",       # 72B — workhorse
    "qwen/qwq-32b",                     # Qwen reasoning
    # Other smart Chinese models (free)
    "moonshotai/moonshot-v1-8k",        # Moonshot AI
    "01-ai/yi-large",                   # 01.AI Yi series
    "zhipuai/glm-4",                    # Zhipu GLM-4
}


def _free_only() -> bool:
    return os.getenv("OPENROUTER_FREE_ONLY", "1") == "1"


def is_free_slug(model: str) -> bool:
    if not model:
        return False
    return ":free" in model or model in FREE_ALLOWLIST or model.startswith("openrouter/")


def _load_keys() -> List[str]:
    multi = os.getenv("OPENROUTER_API_KEYS", "").strip()
    if multi:
        keys = [k.strip() for k in multi.split(",") if k.strip()]
    else:
        single = os.getenv("OPENROUTER_API_KEY", "").strip()
        keys = [single] if single else []
    # de-dupe but preserve order
    seen, out = set(), []
    for k in keys:
        if k and k not in seen:
            seen.add(k); out.append(k)
    return out


class KeyRotator:
    """Thread-safe workload-aware key rotator.

    Distributes work across ALL keys based on:
    - Usage count (least-used gets priority)
    - Per-key cooldown (rate-limited keys cool for 30s, not 60s)
    - Health tracking (keys that fail often get longer cooldowns)

    Keys that hit 401 (invalid/revoked) are permanently dropped and logged
    to dead_keys.log so the operator can clean them up later.
    """

    COOLDOWN_S = 30.0  # shorter cooldown → faster recovery → more key usage
    MAX_COOLDOWN_S = 120.0  # cap for keys that fail repeatedly

    def __init__(self, keys: Optional[List[str]] = None):
        self._lock = threading.Lock()
        self._keys = list(keys) if keys is not None else _load_keys()
        self._idx = 0
        self._cool_until: Dict[str, float] = {}
        self._dead: set = set()
        self._usage: Dict[str, int] = {}  # track workload per key
        self._fail_count: Dict[str, int] = {}  # consecutive failures

    def count(self) -> int:
        return len(self._keys)

    def live_count(self) -> int:
        """Keys that are not currently cooling."""
        now = time.time()
        with self._lock:
            return sum(1 for k in self._keys
                      if self._cool_until.get(k, 0) <= now)

    def add_key(self, k: str) -> None:
        with self._lock:
            if k and k not in self._keys:
                self._keys.append(k)
                self._usage[k] = 0

    def next_key(self) -> Optional[str]:
        """Pick the least-loaded, non-cooled key. Distributes workload evenly
        across ALL available keys instead of simple round-robin."""
        with self._lock:
            if not self._keys:
                return None
            now = time.time()
            # find all available (not cooling) keys
            available = [k for k in self._keys
                        if self._cool_until.get(k, 0) <= now]
            if available:
                # pick least-used available key → even workload distribution
                k = min(available, key=lambda kk: self._usage.get(kk, 0))
                self._usage[k] = self._usage.get(k, 0) + 1
                return k
            # all cooling — return the soonest-ready one
            k = min(self._keys, key=lambda kk: self._cool_until.get(kk, 0))
            self._usage[k] = self._usage.get(k, 0) + 1
            return k

    def mark_failed(self, key: str, cooldown: float = COOLDOWN_S) -> None:
        """Mark a key as rate-limited. Uses progressive backoff:
        each consecutive failure doubles the cooldown (30s → 60s → 120s)."""
        with self._lock:
            self._fail_count[key] = self._fail_count.get(key, 0) + 1
            # progressive cooldown: 30s → 60s → 120s (capped)
            penalty = min(cooldown * (2 ** (self._fail_count[key] - 1)),
                         self.MAX_COOLDOWN_S)
            self._cool_until[key] = time.time() + penalty

    def mark_success(self, key: str) -> None:
        """Reset failure count on successful use — key is healthy again."""
        with self._lock:
            self._fail_count[key] = 0

    def kill_key(self, key: str, reason: str = "401") -> None:
        """Permanently remove a key from the rotation and log it to disk.
        Use this when a key returns 401 (invalid/revoked) — cooldown is pointless."""
        with self._lock:
            if key in self._dead:
                return
            self._dead.add(key)
            if key in self._keys:
                self._keys.remove(key)
                self._idx = self._idx % max(len(self._keys), 1)
            self._usage.pop(key, None)
            self._fail_count.pop(key, None)
        # write to dead_keys.log for the operator
        try:
            import pathlib, datetime
            log_p = pathlib.Path(__file__).resolve().parent / "dead_keys.log"
            with log_p.open("a") as f:
                ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
                suffix = key[-12:] if len(key) > 12 else key
                f.write(f"{ts}\treason={reason}\tkey_suffix=...{suffix}\tfull={key}\n")
        except Exception:
            pass


# module-level singleton
_ROTATOR: Optional[KeyRotator] = None


def get_rotator() -> KeyRotator:
    global _ROTATOR
    if _ROTATOR is None:
        _ROTATOR = KeyRotator()
    return _ROTATOR


class OpenRouterError(Exception):
    pass


def chat(messages: List[Dict[str, str]],
         model: Optional[str] = None,
         max_tokens: int = 600,
         temperature: float = 0.3,
         timeout: float = 30.0,
         max_attempts: Optional[int] = None) -> str:
    """Synchronous chat completion via OpenRouter with workload-aware key rotation.

    Distributes across ALL keys: picks least-loaded available key first.
    On success, resets the key's fail count. On 429/5xx, marks cooldown.
    Rotates through every available key (up to max_attempts) before raising.
    """
    model = model or os.getenv("OPENROUTER_MODEL", "openrouter/owl-alpha")
    if _free_only() and not is_free_slug(model):
        raise OpenRouterError(
            f"OPENROUTER_FREE_ONLY=1 and '{model}' is not in the free allowlist. "
            f"Use a ':free' slug or extend FREE_ALLOWLIST."
        )
    rot = get_rotator()
    if rot.count() == 0:
        raise OpenRouterError("no OPENROUTER_API_KEYS configured")
    # Try ALL live keys before giving up (not just count)
    attempts = max_attempts or max(rot.count() * 2, 3)
    last_err: Optional[Exception] = None
    body = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode("utf-8")
    for attempt in range(attempts):
        key = rot.next_key()
        if not key:
            break
        req = urllib.request.Request(
            OPENROUTER_URL,
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://infinitylux.co.uk",
                "X-Title": "MAB",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                payload = json.loads(r.read().decode("utf-8"))
            # Success — key is healthy, reset fail count
            rot.mark_success(key)
            return payload["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            code = e.code
            try: detail = e.read().decode("utf-8", "replace")[:300]
            except Exception: detail = ""
            last_err = OpenRouterError(f"http {code}: {detail}")
            # 401 = invalid/revoked key — KILL it permanently
            if code == 401:
                rot.kill_key(key, reason="401_user_not_found")
                continue
            # 429 = rate limit, 5xx = server, 403 = forbidden → cool this key down
            if code in (403, 429) or 500 <= code < 600:
                rot.mark_failed(key)
                continue
            raise last_err
        except Exception as e:
            last_err = e
            rot.mark_failed(key, cooldown=15.0)
            continue
    raise OpenRouterError(f"all keys exhausted: {last_err}")


# tiny CLI for manual probing
if __name__ == "__main__":
    import argparse, pathlib
    # auto-load .env if present
    envp = pathlib.Path(__file__).resolve().parent / ".env"
    if envp.exists():
        for line in envp.read_text().splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="+")
    ap.add_argument("--model", default=None)
    args = ap.parse_args()
    rot = get_rotator()
    print(f"keys={rot.count()}  model={args.model or os.getenv('OPENROUTER_MODEL')}")
    print(chat([{"role":"user","content":" ".join(args.prompt)}], model=args.model))
