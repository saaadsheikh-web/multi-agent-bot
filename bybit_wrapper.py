#!/usr/bin/env python3
"""
Bybit wrapper — mirrors the BloFin class interface so bot.py can swap
exchanges by changing one import line. All methods use exactly the same
signatures and return shapes as bot.py's BloFin class.

Symbol convention: bot.py uses "BTC-USDT". Bybit uses "BTCUSDT" internally.
This wrapper normalizes both directions so callers always see "BTC-USDT".

Setup:
  pip install pybit --break-system-packages
  Set in .env:
    BYBIT_API_KEY=<your key>
    BYBIT_API_SECRET=<your secret>
    BYBIT_DEMO=0   # 1 for testnet
"""
import os
import time
import logging
from typing import Optional, List, Dict, Any
import pandas as pd

try:
    from pybit.unified_trading import HTTP
except ImportError:
    raise ImportError("pip install pybit --break-system-packages")

log = logging.getLogger("BYBIT")


def _to_bybit(sym: str) -> str:
    """BTC-USDT → BTCUSDT"""
    return sym.replace("-", "")


def _to_bot(sym: str) -> str:
    """BTCUSDT → BTC-USDT (assumes USDT pair)"""
    if sym.endswith("USDT") and "-" not in sym:
        return sym[:-4] + "-USDT"
    return sym


def _bar_to_interval(bar: str) -> str:
    """bot.py bar codes → Bybit interval codes."""
    m = {"1m": "1", "3m": "3", "5m": "5", "15m": "15",
         "30m": "30", "1H": "60", "4H": "240", "1D": "D"}
    return m.get(bar, "60")


class Bybit:
    """Drop-in replacement for bot.py's BloFin class."""

    def __init__(self):
        self.api_key    = os.environ.get("BYBIT_API_KEY", "")
        self.api_secret = os.environ.get("BYBIT_API_SECRET", "")
        self.demo       = os.environ.get("BYBIT_DEMO", "0") == "1"
        self.client = HTTP(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=self.demo,
        )
        # Bybit Unified perp uses one-way mode + isolated margin by default
        self.position_mode = "net_mode"
        self.margin_mode = "isolated"
        self._contract_cache: Dict[str, dict] = {}
        log.info(f"Bybit init  demo={self.demo}")

    # --- balance/positions ----------------------------------------------------
    def balance(self) -> float:
        try:
            r = self.client.get_wallet_balance(
                accountType="UNIFIED", coin="USDT")
            data = (r or {}).get("result", {}).get("list", [{}])[0]
            return float(data.get("totalEquity") or 0)
        except Exception as e:
            log.error(f"balance: {e}")
            return 0.0

    def positions(self) -> List[dict]:
        try:
            r = self.client.get_positions(category="linear", settleCoin="USDT")
            items = (r or {}).get("result", {}).get("list", []) or []
            out = []
            for p in items:
                size = float(p.get("size") or 0)
                if size == 0:
                    continue
                out.append({
                    "symbol":     _to_bot(p.get("symbol", "")),
                    "side":       p.get("side", "").lower(),
                    "qty":        size,
                    "avg_price":  float(p.get("avgPrice") or 0),
                    "upnl":       float(p.get("unrealisedPnl") or 0),
                    "leverage":   float(p.get("leverage") or 0),
                })
            return out
        except Exception as e:
            log.error(f"positions: {e}")
            return []

    # --- market data ---------------------------------------------------------
    def tickers(self) -> List[dict]:
        try:
            r = self.client.get_tickers(category="linear")
            items = (r or {}).get("result", {}).get("list", []) or []
            return [
                {"instId": _to_bot(t.get("symbol", "")),
                 "last":   t.get("lastPrice"),
                 "vol24h": t.get("volume24h"),
                 "volCcy24h": t.get("turnover24h")}
                for t in items
                if (t.get("symbol") or "").endswith("USDT")
            ]
        except Exception as e:
            log.error(f"tickers: {e}")
            return []

    def candles(self, symbol: str, bar: str = "5m", limit: int = 200) -> pd.DataFrame:
        try:
            r = self.client.get_kline(
                category="linear",
                symbol=_to_bybit(symbol),
                interval=_bar_to_interval(bar),
                limit=min(limit, 1000),
            )
            rows = (r or {}).get("result", {}).get("list", []) or []
            if not rows:
                return pd.DataFrame()
            # Bybit klines: [start, open, high, low, close, volume, turnover]
            df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume", "turnover"])
            for c in ["ts", "open", "high", "low", "close", "volume"]:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            df = df.sort_values("ts").reset_index(drop=True)
            return df.dropna(subset=["close"])
        except Exception as e:
            log.warning(f"candles {symbol} {bar}: {e}")
            return pd.DataFrame()

    def orderbook(self, symbol: str, depth: int = 20) -> dict:
        try:
            r = self.client.get_orderbook(category="linear",
                                          symbol=_to_bybit(symbol),
                                          limit=min(depth, 50))
            d = (r or {}).get("result", {}) or {}
            return {"bids": d.get("b", []) or [],
                    "asks": d.get("a", []) or []}
        except Exception:
            return {"bids": [], "asks": []}

    def funding(self, symbol: str) -> float:
        try:
            r = self.client.get_tickers(category="linear", symbol=_to_bybit(symbol))
            items = (r or {}).get("result", {}).get("list", []) or []
            if not items:
                return 0.0
            return float(items[0].get("fundingRate") or 0) * 100  # → percent
        except Exception:
            return 0.0

    def instrument(self, symbol: str) -> dict:
        if symbol in self._contract_cache:
            return self._contract_cache[symbol]
        try:
            r = self.client.get_instruments_info(
                category="linear", symbol=_to_bybit(symbol))
            items = (r or {}).get("result", {}).get("list", []) or []
            if not items:
                return {}
            d = items[0]
            lf = d.get("lotSizeFilter", {})
            pf = d.get("priceFilter", {})
            info = {
                "instId":      _to_bot(d.get("symbol", "")),
                "minSize":     float(lf.get("minOrderQty") or 0),
                "lotSize":     float(lf.get("qtyStep") or 0.001),
                "tickSize":    float(pf.get("tickSize") or 0.01),
                "ctVal":       float(d.get("contractSize") or 1),
            }
            self._contract_cache[symbol] = info
            return info
        except Exception as e:
            log.warning(f"instrument {symbol}: {e}")
            return {}

    # --- trading -------------------------------------------------------------
    def set_leverage(self, symbol: str, lev: int = 5):
        try:
            self.client.set_leverage(
                category="linear", symbol=_to_bybit(symbol),
                buyLeverage=str(lev), sellLeverage=str(lev))
        except Exception as e:
            # Bybit returns an error if leverage is unchanged; that's not fatal.
            if "110043" not in str(e) and "leverage not modified" not in str(e).lower():
                log.warning(f"set_leverage {symbol}: {e}")

    def place_market(self, symbol: str, side: str, size: float,
                     tp: Optional[float] = None, sl: Optional[float] = None,
                     custom_id: Optional[str] = None) -> dict:
        # bot.py uses side='buy'/'sell'; Bybit wants 'Buy'/'Sell'.
        side_b = "Buy" if side.lower() in ("buy", "long") else "Sell"
        kwargs = dict(
            category="linear",
            symbol=_to_bybit(symbol),
            side=side_b,
            orderType="Market",
            qty=str(size),
        )
        if tp is not None:
            kwargs["takeProfit"] = f"{tp:.8f}"
            kwargs["tpTriggerBy"] = "MarkPrice"
        if sl is not None:
            kwargs["stopLoss"] = f"{sl:.8f}"
            kwargs["slTriggerBy"] = "MarkPrice"
        if custom_id:
            kwargs["orderLinkId"] = custom_id
        try:
            r = self.client.place_order(**kwargs)
            # Normalize response shape to match BloFin's
            return {"code": str(r.get("retCode", "")), "data": r.get("result", {}),
                    "msg": r.get("retMsg", "")}
        except Exception as e:
            log.error(f"place_order {symbol}: {e}")
            return {"error": str(e)}

    def close_position(self, symbol: str, position_side: str = "net") -> dict:
        try:
            # Bybit close is just a reduceOnly order in opposite direction
            poslist = self.client.get_positions(
                category="linear", symbol=_to_bybit(symbol))
            items = (poslist or {}).get("result", {}).get("list", []) or []
            if not items:
                return {"msg": "no position"}
            pos = items[0]
            size = float(pos.get("size") or 0)
            if size == 0:
                return {"msg": "no position"}
            cur_side = pos.get("side", "").lower()  # buy / sell
            close_side = "Sell" if cur_side == "buy" else "Buy"
            r = self.client.place_order(
                category="linear",
                symbol=_to_bybit(symbol),
                side=close_side,
                orderType="Market",
                qty=str(size),
                reduceOnly=True,
            )
            return {"code": str(r.get("retCode", "")), "msg": r.get("retMsg", "")}
        except Exception as e:
            log.error(f"close_position {symbol}: {e}")
            return {"error": str(e)}

    def close_logical(self, symbol: str, logical_side: str) -> dict:
        return self.close_position(symbol, "net")
