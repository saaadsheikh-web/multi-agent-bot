#!/usr/bin/env python3
"""market_context.py — pull macro market data 2-3x/day for bot decisions.

Sources:
  1. CoinGecko (free, no auth)        — global market cap, BTC dominance, top movers
  2. Fear & Greed Index (free)        — alternative.me, sentiment proxy
  3. Crypto.com (free, public ticker) — BTC/ETH/SOL price + 24h change cross-check
  4. CoinGlass (optional, COINGLASS_KEY env) — funding rates, liquidations
  5. CryptoQuant (optional, CRYPTOQUANT_KEY env) — on-chain flows
  6. TradingView lite (optional)       — sentiment scrape

Output: /Users/saad/multi_agent_bot/market_context.json
        plus a 'bias' field: 'bullish' / 'bearish' / 'neutral'

Bot reads this JSON each scan and applies a global tilt to confidence:
  - bullish bias  → +1 conf on longs, -1 on shorts
  - bearish bias  → -1 conf on longs, +1 on shorts
  - neutral       → no change

Schedule: run 3x/day (08:00, 16:00, 00:00 UTC) via cron or bot.py sidecar.
"""

from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

OUT_PATH = Path(__file__).parent / "market_context.json"
LOG_PATH = Path(__file__).parent / "market_context.log"

UA = "multi-agent-bot/1.0 (+market-context-fetcher)"


def _http_get(url: str, headers: dict | None = None, timeout: int = 15) -> dict | list | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        _log(f"GET {url} failed: {e}")
        return None


def _log(msg: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat()}  {msg}\n"
    try:
        LOG_PATH.write_text((LOG_PATH.read_text() if LOG_PATH.exists() else "") + line)
    except Exception:
        pass
    print(line.rstrip(), file=sys.stderr)


# ----- 1. CoinGecko global ---------------------------------------------------
def fetch_coingecko_global() -> dict:
    d = _http_get("https://api.coingecko.com/api/v3/global")
    if not d or "data" not in d:
        return {}
    g = d["data"]
    return {
        "total_mcap_usd":          g.get("total_market_cap", {}).get("usd"),
        "total_volume_24h_usd":    g.get("total_volume", {}).get("usd"),
        "btc_dominance":           g.get("market_cap_percentage", {}).get("btc"),
        "eth_dominance":           g.get("market_cap_percentage", {}).get("eth"),
        "mcap_change_24h_pct":     g.get("market_cap_change_percentage_24h_usd"),
        "active_cryptocurrencies": g.get("active_cryptocurrencies"),
    }


# ----- 2. CoinGecko top movers (top 100 by mcap, sorted by 24h change) -------
def fetch_coingecko_movers() -> list:
    d = _http_get(
        "https://api.coingecko.com/api/v3/coins/markets"
        "?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"
        "&price_change_percentage=24h,7d"
    )
    if not isinstance(d, list):
        return []
    rows = []
    for c in d:
        rows.append({
            "symbol":     c.get("symbol", "").upper(),
            "name":       c.get("name"),
            "price_usd":  c.get("current_price"),
            "change_24h": c.get("price_change_percentage_24h"),
            "change_7d":  c.get("price_change_percentage_7d_in_currency"),
            "vol_24h":    c.get("total_volume"),
            "mcap":       c.get("market_cap"),
        })
    rows.sort(key=lambda r: (r["change_24h"] or 0), reverse=True)
    return rows


# ----- 2b. Money-flow analysis (where the $ is going) -----------------------
def derive_money_flow(movers: list) -> dict:
    """Top-volume coins, rotation signals, real up-moves with high volume."""
    if not movers:
        return {}
    by_vol = sorted(movers, key=lambda c: c.get("vol_24h", 0) or 0, reverse=True)[:10]
    rotations = []
    for c in movers:
        mc = c.get("mcap") or 0
        vol = c.get("vol_24h") or 0
        if mc > 1e8 and vol > 0 and vol / mc > 0.20:
            rotations.append({
                **c,
                "vol_to_mcap_pct": round(vol / mc * 100, 1),
                "direction": "INFLOW" if (c.get("change_24h") or 0) > 0 else "OUTFLOW",
            })
    rotations.sort(key=lambda r: -r["vol_to_mcap_pct"])
    real_pumps = [c for c in movers
                  if (c.get("change_24h") or 0) > 3
                  and (c.get("vol_24h") or 0) > 200e6]
    real_pumps.sort(key=lambda c: -(c.get("change_24h") or 0))
    return {
        "top_10_by_volume": by_vol,
        "rotation_signals": rotations[:10],   # >20% of mcap traded
        "real_up_moves":    real_pumps[:10],  # >3% gain on >$200M vol
    }


# ----- 3. Fear & Greed Index --------------------------------------------------
def fetch_fear_greed() -> dict:
    d = _http_get("https://api.alternative.me/fng/?limit=2")
    if not d or "data" not in d:
        return {}
    rows = d["data"]
    if not rows:
        return {}
    cur = rows[0]
    prev = rows[1] if len(rows) > 1 else cur
    return {
        "value":            int(cur["value"]),
        "label":            cur["value_classification"],
        "delta_24h":        int(cur["value"]) - int(prev["value"]),
        "timestamp_unix":   int(cur["timestamp"]),
    }


# ----- 3b. Crypto.com public tickers (free, no auth) ------------------------
def fetch_crypto_com() -> dict:
    """Crypto.com Exchange public ticker — cross-check our key symbols."""
    syms = ["BTC_USDT", "ETH_USDT", "SOL_USDT", "XRP_USDT", "ZEC_USDT"]
    out = {}
    for s in syms:
        d = _http_get(f"https://api.crypto.com/exchange/v1/public/get-tickers?instrument_name={s}")
        if not d or "result" not in d:
            continue
        rows = d.get("result", {}).get("data", [])
        if not rows:
            continue
        t = rows[0]
        # crypto.com fields: a=ask, b=bid, k=24h-high, l=24h-low, c=24h-change-pct, v=24h-vol
        try:
            last = float(t.get("a") or t.get("b") or 0)
            chg = float(t.get("c") or 0) * 100   # convert fraction → pct
            out[s.replace("_", "-")] = {
                "last": last,
                "change_24h_pct": round(chg, 3),
                "high_24h": float(t.get("k") or 0),
                "low_24h":  float(t.get("l") or 0),
                "vol_24h":  float(t.get("v") or 0),
            }
        except (TypeError, ValueError):
            continue
    return out


# ----- 4. CoinGlass funding rates (requires COINGLASS_KEY) -------------------
def fetch_coinglass_funding() -> dict:
    key = os.getenv("COINGLASS_KEY")
    if not key:
        return {"_skipped": "no COINGLASS_KEY env"}
    d = _http_get(
        "https://open-api-v4.coinglass.com/api/futures/fundingRate/exchangeList?symbol=BTC",
        headers={"CG-API-KEY": key},
    )
    return d or {"_error": "no data"}


# ----- 5. CryptoQuant (requires CRYPTOQUANT_KEY) -----------------------------
def fetch_cryptoquant_flows() -> dict:
    key = os.getenv("CRYPTOQUANT_KEY")
    if not key:
        return {"_skipped": "no CRYPTOQUANT_KEY env"}
    d = _http_get(
        "https://api.cryptoquant.com/v1/btc/exchange-flows/netflow?window=hour&limit=1",
        headers={"Authorization": f"Bearer {key}"},
    )
    return d or {"_error": "no data"}


# ----- BIAS DECISION ---------------------------------------------------------
def derive_bias(g: dict, fg: dict, movers: list) -> tuple[str, list[str]]:
    """Compute bullish/bearish/neutral bias from inputs. Returns (bias, reasons)."""
    score = 0
    reasons = []

    # Total market cap 24h change
    mcap_chg = g.get("mcap_change_24h_pct") or 0
    if mcap_chg > 1.5:
        score += 1; reasons.append(f"mcap +{mcap_chg:.1f}%/24h")
    elif mcap_chg < -1.5:
        score -= 1; reasons.append(f"mcap {mcap_chg:.1f}%/24h")

    # Fear & Greed
    fgv = fg.get("value", 50)
    if fgv >= 70:
        score += 1; reasons.append(f"F&G {fgv} ({fg.get('label')})")
    elif fgv <= 30:
        score -= 1; reasons.append(f"F&G {fgv} ({fg.get('label')})")
    if abs(fg.get("delta_24h", 0)) >= 10:
        # Big sentiment swing — momentum signal
        if fg.get("delta_24h", 0) > 0:
            score += 1; reasons.append(f"F&G +{fg['delta_24h']} swing")
        else:
            score -= 1; reasons.append(f"F&G {fg['delta_24h']} swing")

    # Breadth: how many of top 50 are green vs red?
    if movers:
        green = sum(1 for m in movers if (m.get("change_24h") or 0) > 0)
        red   = sum(1 for m in movers if (m.get("change_24h") or 0) < 0)
        if green >= 35:
            score += 1; reasons.append(f"breadth {green}/50 green")
        elif red >= 35:
            score -= 1; reasons.append(f"breadth {red}/50 red")

    if score >= 2:   return "bullish", reasons
    if score <= -2:  return "bearish", reasons
    return "neutral", reasons


# ----- ENTRY POINT -----------------------------------------------------------
def main():
    _log("=== market_context.py START ===")
    g       = fetch_coingecko_global()
    movers  = fetch_coingecko_movers()
    fg      = fetch_fear_greed()
    cdc     = fetch_crypto_com()
    funding = fetch_coinglass_funding()
    onchain = fetch_cryptoquant_flows()
    bias, reasons = derive_bias(g, fg, movers)

    out = {
        "fetched_at":       datetime.now(timezone.utc).isoformat(),
        "bias":             bias,
        "bias_reasons":     reasons,
        "global":           g,
        "fear_greed":       fg,
        "top_5_gainers":    movers[:5],
        "top_5_losers":     movers[-5:][::-1],
        "movers_breadth":   {
            "green": sum(1 for m in movers if (m.get("change_24h") or 0) > 0),
            "red":   sum(1 for m in movers if (m.get("change_24h") or 0) < 0),
            "total": len(movers),
        },
        "money_flow":        derive_money_flow(movers),
        "crypto_com_tickers": cdc,
        "coinglass_funding": funding,
        "cryptoquant_flows": onchain,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2))
    _log(f"=== bias={bias}  reasons={reasons}  written to {OUT_PATH} ===")
    print(f"bias: {bias} | {' | '.join(reasons) if reasons else 'no signals'}")


if __name__ == "__main__":
    main()
