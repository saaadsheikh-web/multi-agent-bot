---
name: data-sources
description: "Permanent connections to all market data sources — Hyperliquid (230 coins), CoinGecko (trending/gainers), CryptoCompare (candles/news)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

Permanent market data connections configured in `data_sources.py`.

**Hyperliquid**: 
- 230 perpetual markets
- Candle data (1H, 15m, 5m, etc.) with auto-caching
- Files: `market_data_cache/HL_*.parquet`
- Connection: REST API `api.hyperliquid.xyz/info`

**CoinGecko**:
- Trending coins, top gainers, top losers, new listings
- Used for: coin discovery, finding explosive setups
- Rate limit: 10-30 calls/min (free tier)
- Connection: `api.coingecko.com/api/v3`

**CryptoCompare**:
- OHLCV candles for any coin
- News feed
- Rate limit: 100K calls/month (free tier)
- Connection: `min-api.cryptocompare.com/data`

**Usage**:
```python
from data_sources import CoinGecko, Hyperliquid, CryptoCompare, MarketHunter

# Find hot coins
MarketHunter.print_report()
setups = MarketHunter.find_explosive_setups(min_change=5.0)

# Get Hyperliquid data
hl_markets = Hyperliquid.get_markets()
df = Hyperliquid.get_candles("BTC", "1h")

# Get CoinGecko data
trending = CoinGecko.trending()
gainers = CoinGecko.top_gainers(50)
```

**Auto-refresh**: Hyperliquid candles cached for 1 hour. CoinGecko data is live each call.

**Why**: Unlimited data for backtesting and live trading. More coins = more opportunities.
**How to apply**: Import in bot.py, Hermes, or any script. All data flows through unified layer.
