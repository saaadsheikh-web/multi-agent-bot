"""One-shot: where is the money going right now?
Outputs: top volume, biggest vol/mcap ratio (smart-money rotations), gainers with high $ volume."""
import json, urllib.request, urllib.error

UA = "multi-agent-bot/money-flow"

def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return None

# Top 100 by mcap, full data
data = get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&price_change_percentage=24h,7d")
if not data:
    print("fetch failed"); exit()

print("="*72)
print(" WHERE THE MONEY IS — top 100 by mcap, snapshot")
print("="*72)
print()

# 1. TOP 10 BY $ VOLUME (where most $ is changing hands)
print(">>> TOP 10 BY 24H VOLUME (raw money flow)")
by_vol = sorted(data, key=lambda c: c.get("total_volume", 0) or 0, reverse=True)[:10]
print(f"{'#':>2} {'Sym':<6} {'Price':>10} {'24h%':>7} {'7d%':>7} {'Vol $24h':>13} {'MCap':>13}")
for i, c in enumerate(by_vol, 1):
    sym = (c.get("symbol") or "").upper()
    p = c.get("current_price") or 0
    chg24 = c.get("price_change_percentage_24h") or 0
    chg7 = c.get("price_change_percentage_7d_in_currency") or 0
    vol = c.get("total_volume") or 0
    mc = c.get("market_cap") or 0
    print(f"{i:>2} {sym:<6} ${p:>9.4f} {chg24:>+6.2f}% {chg7:>+6.2f}% ${vol/1e9:>11.2f}B ${mc/1e9:>11.2f}B")
print()

# 2. SMART MONEY ROTATIONS (vol/mcap > 0.20 = >20% of mcap traded today, unusual)
print(">>> ROTATION SIGNALS (vol/mcap > 0.20 = heavy turnover)")
rot = []
for c in data:
    mc = c.get("market_cap") or 0
    vol = c.get("total_volume") or 0
    if mc > 1e8 and vol/mc > 0.20:
        rot.append((c, vol/mc))
rot.sort(key=lambda x: -x[1])
for c, ratio in rot[:10]:
    sym = (c.get("symbol") or "").upper()
    chg24 = c.get("price_change_percentage_24h") or 0
    direction = "🟢 INFLOW" if chg24 > 0 else "🔴 OUTFLOW"
    print(f"  {sym:<6} ratio={ratio*100:>5.1f}%  24h={chg24:+.2f}%  {direction}")
print()

# 3. GAINERS WITH HIGH VOLUME (real moves, not thin pumps)
print(">>> REAL UP-MOVES (gainers with >$200M 24h vol)")
real = [c for c in data
        if (c.get("price_change_percentage_24h") or 0) > 3
        and (c.get("total_volume") or 0) > 200e6]
real.sort(key=lambda c: -(c.get("price_change_percentage_24h") or 0))
for c in real[:10]:
    sym = (c.get("symbol") or "").upper()
    chg24 = c.get("price_change_percentage_24h") or 0
    chg7 = c.get("price_change_percentage_7d_in_currency") or 0
    vol = c.get("total_volume") or 0
    print(f"  {sym:<6} 24h={chg24:+.2f}%  7d={chg7:+.2f}%  vol=${vol/1e6:.0f}M")
print()

# 4. SECTOR ROTATION HINT — alts vs BTC
btc = next((c for c in data if c.get("symbol") == "btc"), None)
eth = next((c for c in data if c.get("symbol") == "eth"), None)
btc_chg = btc.get("price_change_percentage_24h", 0) if btc else 0
print(">>> SECTOR ROTATION")
print(f"  BTC 24h: {btc_chg:+.2f}%")
print(f"  ETH 24h: {eth.get('price_change_percentage_24h', 0) if eth else 0:+.2f}%")
green_alts = sum(1 for c in data if c.get("symbol")!="btc" and (c.get("price_change_percentage_24h") or 0) > 0)
print(f"  Alts beating BTC: {green_alts}/99")
