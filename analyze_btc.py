#!/usr/bin/env python3
"""Quick BTC technical analysis using the bot's BloFin client.
Run from /Users/saad/multi_agent_bot:  python3 analyze_btc.py
"""
import os, sys, math, datetime as dt
from statistics import mean, stdev

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reuse the bot's client setup — same .env, same SDK
from dotenv import load_dotenv
load_dotenv()

from blofin import BloFinClient
client = BloFinClient(
    api_key=os.environ["BLOFIN_API_KEY"],
    api_secret=os.environ["BLOFIN_API_SECRET"],
    passphrase=os.environ["BLOFIN_PASSPHRASE"],
)

def get_candles(bar="1H", limit=200):
    res = client.public.get_candlesticks(inst_id="BTC-USDT", bar=bar, limit=limit)
    rows = res["data"]  # newest first
    rows = list(reversed(rows))
    # row format: [ts, o, h, l, c, vol_base, vol_quote, ...]
    return [(int(x[0])/1000, float(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5])) for x in rows]

def ema(vals, n):
    k = 2/(n+1); out = [vals[0]]
    for v in vals[1:]: out.append(v*k + out[-1]*(1-k))
    return out

def rsi(closes, n=14):
    g, l = [], []
    for i in range(1, len(closes)):
        ch = closes[i]-closes[i-1]
        g.append(max(ch,0)); l.append(max(-ch,0))
    if len(g) < n: return 50
    ag = mean(g[:n]); al = mean(l[:n])
    for i in range(n, len(g)):
        ag = (ag*(n-1)+g[i])/n
        al = (al*(n-1)+l[i])/n
    return 100 if al == 0 else 100 - 100/(1 + ag/al)

def atr(h, l, c, n=14):
    trs = [h[0]-l[0]]
    for i in range(1, len(c)):
        trs.append(max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1])))
    return mean(trs[-n:])

def macd(closes):
    e12 = ema(closes, 12); e26 = ema(closes, 26)
    line = [a-b for a,b in zip(e12, e26)]
    sig  = ema(line, 9)
    return line[-1], sig[-1], line[-1]-sig[-1]

def analyze(bar):
    c = get_candles(bar, 200)
    closes = [r[4] for r in c]; highs = [r[2] for r in c]; lows = [r[3] for r in c]; vols = [r[5] for r in c]
    last = closes[-1]
    e20 = ema(closes, 20)[-1]; e50 = ema(closes, 50)[-1]; e200 = ema(closes, min(200, len(closes)))[-1]
    r = rsi(closes, 14); a = atr(highs, lows, closes, 14)
    mline, msig, mhist = macd(closes)
    win = closes[-50:]; whigh = highs[-50:]; wlow = lows[-50:]
    res = max(whigh); sup = min(wlow)
    rets = [(closes[i]/closes[i-1]-1) for i in range(1, len(closes))][-20:]
    vol_pct = stdev(rets)*100
    avg_vol = mean(vols[-20:]); cur_vol = vols[-1]
    return dict(bar=bar, last=last, ema20=e20, ema50=e50, ema200=e200,
                rsi=r, atr=a, sup=sup, res=res, vol_pct=vol_pct,
                vs20=(last/e20-1)*100, vs50=(last/e50-1)*100, vs200=(last/e200-1)*100,
                macd=mline, macd_sig=msig, macd_hist=mhist,
                vol_ratio=cur_vol/avg_vol if avg_vol else 1.0)

ENTRY = 76248.7
TP = 78536.16
SL = 75333.72
SIZE = 0.0033

print("=" * 64)
print(f"  BTC TECHNICAL ANALYSIS — {dt.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC")
print("=" * 64)

results = {}
for bar in ["15m", "1H", "4H", "1D"]:
    a = analyze(bar)
    results[bar] = a
    trend = "↑ UP" if a['ema20'] > a['ema50'] > a['ema200'] else ("↓ DOWN" if a['ema20'] < a['ema50'] < a['ema200'] else "↔ MIXED")
    pos_in_range = (a['last']-a['sup'])/(a['res']-a['sup'])*100
    print(f"\n[{bar}]  ${a['last']:.0f}   trend: {trend}")
    print(f"      RSI={a['rsi']:.1f}   ATR={a['atr']:.0f}   vol20%={a['vol_pct']:.2f}   vol_ratio={a['vol_ratio']:.2f}x")
    print(f"      vs EMA20: {a['vs20']:+.2f}%   vs EMA50: {a['vs50']:+.2f}%   vs EMA200: {a['vs200']:+.2f}%")
    print(f"      MACD: line={a['macd']:+.1f}  sig={a['macd_sig']:+.1f}  hist={a['macd_hist']:+.1f}")
    print(f"      50-bar range: ${a['sup']:.0f} ↔ ${a['res']:.0f}  ({pos_in_range:.0f}% of range)")

# Position summary
last = results["1H"]["last"]
pnl_usd = (last - ENTRY) * SIZE
pnl_pct = (last/ENTRY - 1)*100
to_tp = (TP - last)/last*100
to_sl = (last - SL)/last*100
print("\n" + "=" * 64)
print("  YOUR OPEN BTC POSITION")
print("=" * 64)
print(f"  Entry: ${ENTRY:.0f}   Current: ${last:.0f}")
print(f"  PnL:   ${pnl_usd:+.2f}  ({pnl_pct:+.2f}%)")
print(f"  TP:    ${TP:.0f}   ({to_tp:+.2f}% away)")
print(f"  SL:    ${SL:.0f}   ({to_sl:+.2f}% away)")
print(f"  R/R = 1 : {(TP-ENTRY)/(ENTRY-SL):.2f}")
