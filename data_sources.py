#!/usr/bin/env python3
"""
UNIFIED DATA LAYER — Permanent connections to all market data sources.
Hyperliquid, CoinGecko, CryptoCompare — auto-fetch, cache, normalize.

Used by: bot.py, Hermes, Claude Code, backtests
"""

import os, sys, json, time, hashlib
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests
import pandas as pd
import numpy as np

WORK = os.path.expanduser("~/multi_agent_bot")
CACHE_DIR = os.path.join(WORK, "market_data_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# COINGECKO — Coin discovery, metadata, trending
# ═══════════════════════════════════════════════════════════
class CoinGecko:
    """Free API — 10-30 calls/min. Coin discovery, trending, metadata."""
    BASE = "https://api.coingecko.com/api/v3"

    @staticmethod
    def trending() -> List[dict]:
        """Coins trending on CoinGecko right now."""
        r = requests.get(f"{CoinGecko.BASE}/search/trending", timeout=10)
        if r.status_code == 200:
            coins = r.json().get("coins", [])
            return [{
                "id": c["item"]["id"],
                "symbol": c["item"]["symbol"].upper(),
                "name": c["item"]["name"],
                "market_cap_rank": c["item"].get("market_cap_rank"),
                "score": c["item"].get("score"),
                "price_btc": c["item"].get("price_btc"),
            } for c in coins]
        return []

    @staticmethod
    def top_gainers(top_n: int = 50) -> List[dict]:
        """Top gainers in 24h — find explosive coins."""
        r = requests.get(
            f"{CoinGecko.BASE}/coins/markets",
            params={"vs_currency": "usd", "order": "percent_change_24h_desc",
                    "per_page": top_n, "page": 1, "sparkline": "false"},
            timeout=10
        )
        if r.status_code == 200:
            return [{
                "symbol": c["symbol"].upper(),
                "name": c["name"],
                "price": c["current_price"],
                "change_24h": c.get("price_change_percentage_24h"),
                "change_7d": c.get("price_change_percentage_7d"),
                "volume_24h": c.get("total_volume"),
                "market_cap": c.get("market_cap"),
            } for c in r.json()]
        return []

    @staticmethod
    def top_losers(top_n: int = 50) -> List[dict]:
        """Top losers in 24h — find crash candidates."""
        r = requests.get(
            f"{CoinGecko.BASE}/coins/markets",
            params={"vs_currency": "usd", "order": "percent_change_24h_asc",
                    "per_page": top_n, "page": 1, "sparkline": "false"},
            timeout=10
        )
        if r.status_code == 200:
            return [{
                "symbol": c["symbol"].upper(),
                "name": c["name"],
                "price": c["current_price"],
                "change_24h": c.get("price_change_percentage_24h"),
                "volume_24h": c.get("total_volume"),
            } for c in r.json()]
        return []

    @staticmethod
    def new_listings(days: int = 30) -> List[dict]:
        """Recently added coins — find fresh opportunities."""
        r = requests.get(
            f"{CoinGecko.BASE}/coins/markets",
            params={"vs_currency": "usd", "order": "created_at_desc",
                    "per_page": 100, "page": 1, "sparkline": "false"},
            timeout=10
        )
        if r.status_code == 200:
            return [{
                "symbol": c["symbol"].upper(),
                "name": c["name"],
                "price": c["current_price"],
                "volume_24h": c.get("total_volume"),
                "market_cap": c.get("market_cap"),
            } for c in r.json() if c.get("market_cap", 0) > 100000]
        return []

    @staticmethod
    def high_volume_gainers(min_vol: int = 10_000_000) -> List[dict]:
        """High volume coins that are moving — quality over noise."""
        r = requests.get(
            f"{CoinGecko.BASE}/coins/markets",
            params={"vs_currency": "usd", "order": "volume_desc",
                    "per_page": 100, "page": 1, "sparkline": "false"},
            timeout=10
        )
        if r.status_code == 200:
            return [{
                "symbol": c["symbol"].upper(),
                "name": c["name"],
                "price": c["current_price"],
                "change_24h": c.get("price_change_percentage_24h"),
                "volume_24h": c.get("total_volume"),
                "market_cap": c.get("market_cap"),
            } for c in r.json() if c.get("total_volume", 0) > min_vol]
        return []


# ═══════════════════════════════════════════════════════════
# HYPERLIQUID — Perpetual data, 230+ coins
# ═══════════════════════════════════════════════════════════
class Hyperliquid:
    """Decentralized perps exchange — 230+ coins, fast data."""
    API = "https://api.hyperliquid.xyz/info"

    @staticmethod
    def get_markets() -> List[str]:
        """All available perpetual markets."""
        r = requests.post(Hyperliquid.API, json={"type": "meta"}, timeout=10)
        if r.status_code == 200:
            return [u["name"] for u in r.json().get("universe", []) if "name" in u]
        return []

    @staticmethod
    def get_candles(coin: str, interval: str = "1h", days: int = 365) -> Optional[pd.DataFrame]:
        """Fetch candles for a Hyperliquid coin. Cached to parquet."""
        cache_key = f"HL_{coin}_{interval}_{days}d"
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.parquet")

        # Return cached if fresh (< 1 hour old)
        if os.path.exists(cache_file):
            age = time.time() - os.path.getmtime(cache_file)
            if age < 3600:
                return pd.read_parquet(cache_file)

        end = int(time.time() * 1000)
        start = end - (days * 24 * 3600 * 1000)

        r = requests.post(Hyperliquid.API, json={
            "type": "candleSnapshot",
            "req": {"coin": coin, "interval": interval, "startTime": start, "endTime": end}
        }, timeout=30)

        if r.status_code != 200:
            return None

        data = r.json()
        if not isinstance(data, list) or len(data) < 50:
            return None

        df = pd.DataFrame([{
            "ts": c["t"], "open": float(c["o"]), "high": float(c["h"]),
            "low": float(c["l"]), "close": float(c["c"]), "volume": float(c["v"]),
        } for c in data]).sort_values("ts").reset_index(drop=True)

        df.to_parquet(cache_file, index=False)
        return df

    @staticmethod
    def get_all_candles(interval: str = "1h", coins: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Fetch 1H candles for multiple coins. Returns {coin: df}."""
        if coins is None:
            coins = Hyperliquid.get_markets()[:50]  # top 50

        results = {}
        for i, coin in enumerate(coins):
            df = Hyperliquid.get_candles(coin, interval)
            if df is not None:
                results[coin] = df
            if i > 0 and i % 10 == 0:
                time.sleep(0.5)  # rate limit
        return results


# ═══════════════════════════════════════════════════════════
# CRYPTOCOMPARE — Free OHLCV for any coin
# ═══════════════════════════════════════════════════════════
class CryptoCompare:
    """Free tier — 100K calls/month. OHLCV, news, social."""
    BASE = "https://min-api.cryptocompare.com/data"

    @staticmethod
    def get_candles(symbol: str, tf: str = "1H", limit: int = 2000) -> Optional[pd.DataFrame]:
        """Get candles. symbol='BTC', tf='1H'/'15m'/'5m'."""
        tf_map = {"5m": "histominute", "15m": "histominute", "30m": "histominute",
                   "1H": "histohour", "4H": "histohour"}
        endpoint = tf_map.get(tf, "histohour")
        agg = {"5m": 5, "15m": 15, "30m": 30, "1H": 1, "4H": 4}.get(tf, 1)

        r = requests.get(f"{CryptoCompare.BASE}/v2/{endpoint}", params={
            "fsym": symbol, "tsym": "USD", "limit": limit, "aggregate": agg,
        }, timeout=15)

        if r.status_code != 200:
            return None

        data = r.json().get("Data", {}).get("Data", [])
        if not data:
            return None

        return pd.DataFrame([{
            "ts": d["time"] * 1000,
            "open": d["open"], "high": d["high"],
            "low": d["low"], "close": d["close"],
            "volume": d.get("volumefrom", d.get("volume", 0)),
        } for d in data]).sort_values("ts").reset_index(drop=True)

    @staticmethod
    def get_news(symbol: str = "", categories: List[str] = None) -> List[dict]:
        """Latest crypto news. Filter by symbol or category."""
        params = {"lang": "EN"}
        if symbol:
            params["categories"] = symbol
        r = requests.get(f"{CryptoCompare.BASE}/v2/news/", params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("Data", [])[:20]
        return []


# ═══════════════════════════════════════════════════════════
# UNIFIED HUNTER — Combines all sources to find opportunities
# ═══════════════════════════════════════════════════════════
class MarketHunter:
    """Combines CoinGecko + Hyperliquid + CryptoCompare to find the best coins."""

    @staticmethod
    def hunt_hot_coins() -> dict:
        """Find coins trending, pumping, or about to explode."""
        results = {"trending": [], "gainers": [], "losers": [], "new": []}

        try:
            results["trending"] = CoinGecko.trending()[:10]
        except: pass

        try:
            results["gainers"] = CoinGecko.top_gainers(20)
        except: pass

        try:
            results["losers"] = CoinGecko.top_losers(20)
        except: pass

        try:
            results["new"] = CoinGecko.new_listings(30)[:10]
        except: pass

        return results

    @staticmethod
    def find_explosive_setups(min_change: float = 5.0) -> List[dict]:
        """Find coins that are moving hard — ready for breakout or crash."""
        setups = []

        # High volume gainers (breakout candidates)
        gainers = CoinGecko.top_gainers(50)
        for g in gainers:
            change = g.get("change_24h") or 0
            volume = g.get("volume_24h") or 0
            if abs(change) > min_change and volume > 5_000_000:
                setups.append({
                    "symbol": g["symbol"],
                    "name": g["name"],
                    "change_24h": change,
                    "direction": "LONG" if change > 0 else "SHORT",
                    "volume": volume,
                    "price": g["price"],
                    "source": "coingecko",
                    "reason": f"{'Pumping' if change>0 else 'Dumping'} {abs(change):.1f}% in 24h on ${volume:,.0f} volume",
                })

        setups.sort(key=lambda x: abs(x["change_24h"]), reverse=True)
        return setups[:20]

    @staticmethod
    def print_report():
        """Print a clean market hunting report."""
        print("=" * 80)
        print("MARKET HUNTER — Multi-Source Coin Discovery")
        print(f"Sources: CoinGecko, Hyperliquid, CryptoCompare")
        print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        print("=" * 80)

        # Trending
        try:
            trending = CoinGecko.trending()[:7]
            print(f"\n🔥 TRENDING NOW (CoinGecko)")
            for c in trending:
                print(f"  {c['symbol']:<12s} {c['name'][:20]:<22s} rank=#{c.get('market_cap_rank','?')}")
        except Exception as e:
            print(f"  Trending: {e}")

        # Explosive setups
        try:
            setups = MarketHunter.find_explosive_setups(8)[:10]
            print(f"\n⚡ EXPLOSIVE SETUPS (Volume > $5M, Move > 5%)")
            for s in setups:
                arrow = "🚀" if s["direction"] == "LONG" else "💥"
                print(f"  {arrow} {s['symbol']:<12s} {s['change_24h']:+.1f}% | ${s['volume']:,.0f} vol | {s['reason']}")
        except Exception as e:
            print(f"  Setups: {e}")

        # Hyperliquid markets
        try:
            hl_markets = Hyperliquid.get_markets()
            print(f"\n📡 HYPERLIQUID: {len(hl_markets)} markets available")
            print(f"  Top: {', '.join(hl_markets[:15])}")
        except Exception as e:
            print(f"  Hyperliquid: {e}")

        print(f"\n{'='*80}")


if __name__ == "__main__":
    MarketHunter.print_report()
