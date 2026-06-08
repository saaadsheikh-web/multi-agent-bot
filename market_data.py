#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 MARKET DATA ENGINE — free crypto data, predictions, on-chain intelligence
=============================================================================
 Uses FREE public APIs (no paid keys needed for most) + your Jupiter/Helios keys.

 Data sources:
   - Binance public API (klines, order book, funding rate) — FREE
   - Jupiter DEX API (Solana swaps, liquidity, token prices) — FREE (key optional)
   - Helios API (crypto predictions, sentiment) — your key
   - CoinGecko free API (sentiment, trends, global data)
   - Fear & Greed Index (alternative.me) — FREE
   - Blockchain.info (BTC on-chain) — FREE

 Feeds Hermes with real-time market intelligence for better trading decisions.
=============================================================================
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import aiohttp

HERE = Path(__file__).resolve().parent
log = logging.getLogger("market_data")

# Load .env
env_path = HERE / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

JUPITER_API_KEY = os.getenv("JUPITER_API_KEY", "")
JUPITER_API_SECRET = os.getenv("JUPITER_API_SECRET", "")
HELIOS_API_KEY = os.getenv("HELIOS_API_KEY", "")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")

# Cache to avoid rate limits
_cache: Dict[str, Tuple[float, Any]] = {}
CACHE_TTL = 60  # seconds


def _cached(key: str, ttl: int = CACHE_TTL):
    """Simple in-memory cache decorator."""
    def decorator(fn):
        async def wrapper(*args, **kwargs):
            now = time.time()
            if key in _cache:
                ts, val = _cache[key]
                if now - ts < ttl:
                    return val
            result = await fn(*args, **kwargs)
            _cache[key] = (now, result)
            return result
        return wrapper
    return decorator


# =============================================================================
# BINANCE PUBLIC API (FREE — no key needed)
# =============================================================================

@_cached("bn_btc_klines", ttl=60)
async def get_btc_klines(interval: str = "1h", limit: int = 50) -> List[Dict]:
    """Get BTC/USDT klines from Binance public API."""
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={interval}&limit={limit}"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                data = await r.json()
        return [{
            "open": float(k[1]), "high": float(k[2]), "low": float(k[3]),
            "close": float(k[4]), "volume": float(k[5]),
            "close_time": k[6]
        } for k in data]
    except Exception as e:
        log.debug(f"binance klines: {e}")
        return []


@_cached("bn_funding", ttl=120)
async def get_funding_rates() -> Dict[str, float]:
    """Get funding rates for top USDT perpetuals."""
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://fapi.binance.com/fapi/v1/premiumIndex",
                            timeout=aiohttp.ClientTimeout(total=10)) as r:
                data = await r.json()
        return {item["symbol"]: float(item["lastFundingRate"])
                for item in data if item["symbol"].endswith("USDT")}
    except Exception as e:
        log.debug(f"funding rates: {e}")
        return {}


@_cached("bn_orderbook", ttl=30)
async def get_order_book(symbol: str = "BTCUSDT", depth: int = 20) -> Dict:
    """Get order book depth for a symbol."""
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={depth}"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
                data = await r.json()
        bids = [(float(b[0]), float(b[1])) for b in data.get("bids", [])]
        asks = [(float(a[0]), float(a[1])) for a in data.get("asks", [])]
        bid_vol = sum(b[1] for b in bids)
        ask_vol = sum(a[1] for a in asks)
        imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol) if (bid_vol + ask_vol) > 0 else 0
        return {
            "bids": bids[:5], "asks": asks[:5],
            "bid_volume": bid_vol, "ask_volume": ask_vol,
            "imbalance": round(imbalance, 4),
            "spread_pct": round((asks[0][0] - bids[0][0]) / bids[0][0] * 100, 4) if bids and asks else 0,
        }
    except Exception as e:
        log.debug(f"orderbook: {e}")
        return {}


# =============================================================================
# JUPITER DEX API (Solana — key optional, works without for public endpoints)
# =============================================================================

@_cached("jup_quote", ttl=30)
async def get_jupiter_quote(input_mint: str = "So11111111111111111111111111111111111111112",
                            output_mint: str = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                            amount: int = 1_000_000_000) -> Dict:
    """Get a swap quote from Jupiter (Solana DEX aggregator). 1 SOL → USDC by default.
    Uses API key + secret for higher rate limits and authenticated access."""
    url = "https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(amount),
        "slippageBps": "50",
    }
    headers = {}
    if JUPITER_API_KEY:
        headers["x-api-key"] = JUPITER_API_KEY
        if JUPITER_API_SECRET:
            headers["x-api-secret"] = JUPITER_API_SECRET
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, params=params, headers=headers,
                           timeout=aiohttp.ClientTimeout(total=8)) as r:
                if r.status == 200:
                    return await r.json()
        return {}
    except Exception as e:
        log.debug(f"jupiter: {e}")
        return {}


async def get_jupiter_price(token_mint: str) -> Optional[float]:
    """Get any Solana token price in USDC via Jupiter."""
    try:
        quote = await get_jupiter_quote(
            input_mint=token_mint,
            output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            amount=1_000_000_000,
        )
        out = quote.get("outAmount")
        if out:
            return int(out) / 1_000_000
    except Exception:
        pass
    return None


async def get_sol_price_usdc() -> Optional[float]:
    """Quick SOL → USDC price via Jupiter."""
    quote = await get_jupiter_quote()
    out = quote.get("outAmount")
    if out:
        return int(out) / 1_000_000
    return None


# =============================================================================
# HELIOS API — crypto predictions & sentiment
# =============================================================================

@_cached("helios_sentiment", ttl=300)
async def get_helios_sentiment() -> Dict:
    """Get market sentiment/predictions from Helios API."""
    if not HELIOS_API_KEY:
        return {"available": False, "reason": "no HELIOS_API_KEY in .env"}
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                "https://api.helios.finance/v1/sentiment",
                headers={"Authorization": f"Bearer {HELIOS_API_KEY}"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status == 200:
                    return await r.json()
        return {"available": False, "reason": f"http {r.status}"}
    except Exception as e:
        return {"available": False, "reason": str(e)}


# =============================================================================
# FEAR & GREED INDEX (FREE)
# =============================================================================

@_cached("fear_greed", ttl=3600)
async def get_fear_greed() -> Dict:
    """Fear & Greed Index from alternative.me."""
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.alternative.me/fng/?limit=1",
                           timeout=aiohttp.ClientTimeout(total=10)) as r:
                data = await r.json()
        item = data["data"][0]
        return {
            "value": int(item["value"]),
            "classification": item["value_classification"],
            "timestamp": item["timestamp"],
        }
    except Exception as e:
        log.debug(f"fear_greed: {e}")
        return {"value": 50, "classification": "Neutral"}


# =============================================================================
# COINGECKO FREE API — global market data
# =============================================================================

@_cached("coingecko_global", ttl=600)
async def get_global_market_data() -> Dict:
    """Global crypto market data from CoinGecko."""
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                "https://api.coingecko.com/api/v3/global",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status == 200:
                    return await r.json()
        return {}
    except Exception as e:
        log.debug(f"coingecko: {e}")
        return {}


@_cached("coingecko_trending", ttl=600)
async def get_trending_coins() -> List[Dict]:
    """Trending coins from CoinGecko."""
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                "https://api.coingecko.com/api/v3/search/trending",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    return [
                        {"name": c["item"]["name"], "symbol": c["item"]["symbol"],
                         "market_cap_rank": c["item"].get("market_cap_rank"),
                         "score": c["item"].get("score")}
                        for c in data.get("coins", [])[:10]
                    ]
        return []
    except Exception as e:
        log.debug(f"coingecko trending: {e}")
        return []


# =============================================================================
# BIRDEYE API (Solana on-chain data, token trends, wallet tracking)
# =============================================================================

@_cached("birdeye_trending", ttl=300)
async def get_birdeye_trending() -> List[Dict]:
    """Trending Solana tokens from Birdeye."""
    if not BIRDEYE_API_KEY:
        return []
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                "https://public-api.birdeye.so/defi/token_trending?sort_by=rank&sort_type=asc&limit=10",
                headers={"X-API-KEY": BIRDEYE_API_KEY, "accept": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    return data.get("data", {}).get("tokens", []) if "data" in data else []
        return []
    except Exception as e:
        log.debug(f"birdeye: {e}")
        return []


@_cached("birdeye_sol_price", ttl=30)
async def get_birdeye_sol_price() -> Optional[float]:
    """SOL price from Birdeye."""
    if not BIRDEYE_API_KEY:
        return None
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                "https://public-api.birdeye.so/public/price?address=So11111111111111111111111111111111111111112",
                headers={"X-API-KEY": BIRDEYE_API_KEY},
                timeout=aiohttp.ClientTimeout(total=5),
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    return data.get("data", {}).get("value")
        return None
    except Exception as e:
        log.debug(f"birdeye sol: {e}")
        return None


# =============================================================================
# BITCOIN ON-CHAIN (blockchain.info — FREE)
# =============================================================================

@_cached("btc_onchain", ttl=600)
async def get_btc_onchain() -> Dict:
    """BTC on-chain stats from blockchain.info."""
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                "https://api.blockchain.info/stats",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    return {
                        "hash_rate": data.get("hash_rate", 0),
                        "total_btc_sent": data.get("total_btc_sent", 0),
                        "total_fees_btc": data.get("total_fees_btc", 0),
                        "n_transactions": data.get("n_transactions", 0),
                        "estimated_btc_sent": data.get("estimated_btc_sent", 0),
                    }
        return {}
    except Exception as e:
        log.debug(f"btc onchain: {e}")
        return {}


# =============================================================================
# COMPREHENSIVE MARKET SNAPSHOT
# =============================================================================

async def get_market_snapshot() -> Dict[str, Any]:
    """Pull ALL market data in parallel for a complete intelligence snapshot."""
    results = {}

    async def safe_fetch(name, coro):
        try:
            results[name] = await coro
        except Exception as e:
            results[name] = {"error": str(e)}

    await asyncio.gather(
        safe_fetch("btc_klines", get_btc_klines("1h", 24)),
        safe_fetch("funding_rates", get_funding_rates()),
        safe_fetch("fear_greed", get_fear_greed()),
        safe_fetch("trending", get_trending_coins()),
        safe_fetch("btc_onchain", get_btc_onchain()),
        safe_fetch("jupiter_sol", get_sol_price_usdc()),
        safe_fetch("birdeye_sol", get_birdeye_sol_price()),
        safe_fetch("birdeye_trending", get_birdeye_trending()),
        safe_fetch("global", get_global_market_data()),
    )

    if HELIOS_API_KEY:
        results["helios"] = await get_helios_sentiment()

    # Compute market bias
    fg = results.get("fear_greed", {})
    fg_value = fg.get("value", 50)

    if fg_value <= 25:
        bias = "bearish_extreme"
    elif fg_value <= 40:
        bias = "bearish"
    elif fg_value <= 60:
        bias = "neutral"
    elif fg_value <= 80:
        bias = "bullish"
    else:
        bias = "bullish_extreme"

    results["market_bias"] = bias
    results["timestamp"] = datetime.now(timezone.utc).isoformat()

    # Save to disk for Hermes
    snapshot_path = HERE / "market_context.json"
    snapshot_path.write_text(json.dumps(results, indent=2, default=str))

    return results


# =============================================================================
# STANDALONE CLI
# =============================================================================

if __name__ == "__main__":
    async def main():
        print("📊 Pulling market data from 7+ free sources...\n")
        snap = await get_market_snapshot()
        print(json.dumps(snap, indent=2, default=str, ensure_ascii=False))

    asyncio.run(main())
