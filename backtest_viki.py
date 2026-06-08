#!/usr/bin/env python3
"""Backtest Viki — 15m TF, 9/21/50 EMA, 5% SL, trail TP after +7%. 20×, 2mo, compounding."""

import os, sys
import numpy as np
import pandas as pd

WORK_DIR = os.path.join(os.path.expanduser("~"), "multi_agent_bot")
CACHE_DIR = os.path.join(WORK_DIR, "backtest_data")
ENV_PATH = os.path.join(WORK_DIR, ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

UNIVERSE = [
    "SOL-USDT","TAO-USDT","TIA-USDT",
]
# Keep current settings: 5×, 7% SL, trail @ 3%, 1.5% trail distance
DAYS = 365
STARTING_BALANCE = 100.0
LEVERAGE = 10
RISK_FRACTION = 0.10
SL_PCT = 0.07        # 7% hard stop
TRAIL_ACTIVATE = 0.03  # 3% profit → activate trail
TRAIL_DISTANCE = 0.015  # trail 1.5% behind high/low water
MAX_HOLD_BARS = 384   # 4 days in 15m bars (96 × 4)

def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def simulate_trades(df, symbol):
    if len(df) < 60:
        return []
    c = df["close"]; h = df["high"]; l = df["low"]; v = df["volume"]; ts = df["ts"]
    e9 = ema(c,9); e21 = ema(c,21); e50 = ema(c,50)

    trades = []
    in_trade = None

    for i in range(52, len(df)):
        if any(pd.isna(x) for x in [e9.iloc[i],e21.iloc[i],e50.iloc[i],
                                     e9.iloc[i-1],e21.iloc[i-1]]):
            continue
        if c.iloc[i] <= 0:
            continue

        vol_ok = v.iloc[i] > 0 and not pd.isna(v.iloc[i])
        avg_v = v.iloc[i-20:i].mean() if i>=20 else v.iloc[:i].mean()
        v_ratio = v.iloc[i]/avg_v if avg_v>0 else 0
        vol_filter = v_ratio >= 0.8

        prev_diff = e9.iloc[i-1] - e21.iloc[i-1]
        cur_diff  = e9.iloc[i] - e21.iloc[i]
        bullish_x = prev_diff <= 0 and cur_diff > 0
        bearish_x = prev_diff >= 0 and cur_diff < 0
        e50_now = e50.iloc[i]
        entry_price = c.iloc[i]

        # ── Exit check ──
        if in_trade:
            side = in_trade["side"]
            bars_held = i - in_trade["entry_bar"]

            # Update high/low water
            if side == "long":
                in_trade["high_water"] = max(in_trade["high_water"], h.iloc[i])
            else:
                in_trade["low_water"] = min(in_trade["low_water"], l.iloc[i])

            # Check if trail activates
            if not in_trade["trail_active"]:
                if side == "long":
                    profit_pct = (in_trade["high_water"] - in_trade["entry"]) / in_trade["entry"]
                    if profit_pct >= TRAIL_ACTIVATE:
                        in_trade["trail_active"] = True
                        in_trade["trail_stop"] = in_trade["high_water"] * (1 - TRAIL_DISTANCE)
                else:
                    profit_pct = (in_trade["entry"] - in_trade["low_water"]) / in_trade["entry"]
                    if profit_pct >= TRAIL_ACTIVATE:
                        in_trade["trail_active"] = True
                        in_trade["trail_stop"] = in_trade["low_water"] * (1 + TRAIL_DISTANCE)

            # Update trail stop
            if in_trade["trail_active"]:
                if side == "long":
                    new_stop = in_trade["high_water"] * (1 - TRAIL_DISTANCE)
                    in_trade["trail_stop"] = max(in_trade["trail_stop"], new_stop)
                else:
                    new_stop = in_trade["low_water"] * (1 + TRAIL_DISTANCE)
                    in_trade["trail_stop"] = min(in_trade["trail_stop"], new_stop)

            # Determine effective stop
            if side == "long":
                hard_sl = in_trade["entry"] * (1 - SL_PCT)
                effective_sl = max(hard_sl, in_trade.get("trail_stop", hard_sl))
            else:
                hard_sl = in_trade["entry"] * (1 + SL_PCT)
                effective_sl = min(hard_sl, in_trade.get("trail_stop", hard_sl))

            exit_price = None; exit_reason = None

            if side == "long" and l.iloc[i] <= effective_sl:
                exit_price = effective_sl
                exit_reason = "TRAIL_STOP" if in_trade.get("trail_active") else "SL_HIT"
            elif side == "short" and h.iloc[i] >= effective_sl:
                exit_price = effective_sl
                exit_reason = "TRAIL_STOP" if in_trade.get("trail_active") else "SL_HIT"

            if bars_held >= MAX_HOLD_BARS:
                exit_price = c.iloc[i]; exit_reason = "TIMEOUT"

            if exit_price is not None:
                e = in_trade["entry"]; s = in_trade["side"]
                pnl_pct = (exit_price-e)/e if s=="long" else (e-exit_price)/e
                trades.append({
                    "symbol":symbol,"side":s,"entry":e,"exit":exit_price,
                    "pnl_pct":pnl_pct,"exit_reason":exit_reason,
                    "entry_bar":in_trade["entry_bar"],"exit_bar":i,
                    "bars_held":bars_held,"trailed":in_trade.get("trail_active",False),
                    "high_w":in_trade.get("high_water",e),"low_w":in_trade.get("low_water",e),
                    "entry_time":ts.iloc[in_trade["entry_bar"]],"exit_time":ts.iloc[i],
                })
                in_trade = None
                continue

        # ── Entry check ──
        if in_trade is None and vol_filter:
            if bullish_x and e9.iloc[i]>e50_now and e21.iloc[i]>e50_now:
                in_trade = {"side":"long","entry":entry_price,"entry_bar":i,
                            "high_water":entry_price,"low_water":entry_price,
                            "trail_active":False,"trail_stop":entry_price*(1-SL_PCT)}
            elif bearish_x and e9.iloc[i]<e50_now and e21.iloc[i]<e50_now:
                in_trade = {"side":"short","entry":entry_price,"entry_bar":i,
                            "high_water":entry_price,"low_water":entry_price,
                            "trail_active":False,"trail_stop":entry_price*(1+SL_PCT)}

    # Close open at end
    if in_trade:
        e=in_trade["entry"]; s=in_trade["side"]; xp=c.iloc[-1]
        pnl_pct = (xp-e)/e if s=="long" else (e-xp)/e
        trades.append({
            "symbol":symbol,"side":s,"entry":e,"exit":xp,
            "pnl_pct":pnl_pct,"exit_reason":"EOD_FORCED",
            "entry_bar":in_trade["entry_bar"],"exit_bar":len(df)-1,
            "bars_held":len(df)-1-in_trade["entry_bar"],
            "trailed":in_trade.get("trail_active",False),
            "high_w":in_trade.get("high_water",e),"low_w":in_trade.get("low_water",e),
            "entry_time":ts.iloc[in_trade["entry_bar"]],"exit_time":ts.iloc[-1],
        })
    return trades


def main():
    print("=" * 78)
    print("VIKI BACKTEST — 15m TF | 7% SL | Trail @ +3% (1.5%) | 10× | $100 | SOL/TAO/TIA | 1 Year")
    print("=" * 78)

    all_raw = []
    for sym in UNIVERSE:
        path = os.path.join(CACHE_DIR, f"{sym.replace('-','_')}_15m_365d.parquet")
        if not os.path.exists(path): continue
        df = pd.read_parquet(path).sort_values("ts").reset_index(drop=True)
        cutoff = df["ts"].max() - (DAYS*24*3600*1000)
        df = df[df["ts"]>=cutoff].copy()
        if len(df)<300: continue
        all_raw.extend(simulate_trades(df, sym))

    if not all_raw:
        print("NO TRADES"); return

    all_raw.sort(key=lambda t: t["entry_time"])

    balance = STARTING_BALANCE
    peak=balance; dd_pct=0
    wins=0; losses=0; be=0
    losers_row=0; max_losers_row=0
    trailed_wins=0; trailed_losses=0
    best_trade_pnl=0; worst_trade_pnl=0
    closed=[]

    for t in all_raw:
        margin = balance * RISK_FRACTION
        notional = margin * LEVERAGE
        pnl_usd = notional * t["pnl_pct"]
        balance += pnl_usd
        if balance <= 0: balance=0; break
        t["balance_after"]=balance; t["pnl_usd"]=pnl_usd; t["notional"]=notional
        closed.append(t)
        if t["pnl_pct"]>0.0001:
            wins+=1; losers_row=0
            if t["trailed"]: trailed_wins+=1
        elif t["pnl_pct"]<-0.0001:
            losses+=1; losers_row+=1; max_losers_row=max(max_losers_row,losers_row)
            if t["trailed"]: trailed_losses+=1
        else: be+=1; losers_row=0
        best_trade_pnl = max(best_trade_pnl, pnl_usd)
        worst_trade_pnl = min(worst_trade_pnl, pnl_usd)
        if balance>peak: peak=balance
        dd = (peak-balance)/peak*100 if peak>0 else 0
        dd_pct=max(dd_pct,dd)

    total = len(closed)
    wr = wins/total*100 if total else 0
    avg_win  = sum(t["pnl_usd"] for t in closed if t["pnl_pct"]>0.0001)/max(wins,1)
    avg_loss = sum(t["pnl_usd"] for t in closed if t["pnl_pct"]<-0.0001)/max(losses,1)
    avg_win_pct  = sum(t["pnl_pct"]*100 for t in closed if t["pnl_pct"]>0.0001)/max(wins,1)
    avg_loss_pct = sum(t["pnl_pct"]*100 for t in closed if t["pnl_pct"]<-0.0001)/max(losses,1)

    longs=[t for t in closed if t["side"]=="long"]
    shorts=[t for t in closed if t["side"]=="short"]

    by_reason={}
    for t in closed:
        r=t["exit_reason"]
        by_reason.setdefault(r,{"count":0,"pnl":0,"w":0,"l":0,"bars":0,"trailed":0})
        by_reason[r]["count"]+=1; by_reason[r]["pnl"]+=t["pnl_usd"]; by_reason[r]["bars"]+=t["bars_held"]
        if t["pnl_pct"]>0: by_reason[r]["w"]+=1
        elif t["pnl_pct"]<0: by_reason[r]["l"]+=1
        if t["trailed"]: by_reason[r]["trailed"]+=1

    by_sym={}
    for t in closed:
        s=t["symbol"]
        by_sym.setdefault(s,{"t":0,"w":0,"l":0,"pnl":0,"bars":0})
        by_sym[s]["t"]+=1; by_sym[s]["pnl"]+=t["pnl_usd"]; by_sym[s]["bars"]+=t["bars_held"]
        if t["pnl_pct"]>0: by_sym[s]["w"]+=1
        elif t["pnl_pct"]<0: by_sym[s]["l"]+=1

    weeks = max((closed[-1]["exit_time"]-closed[0]["entry_time"])/(7*24*3600*1000),1)
    avg_bars = sum(t["bars_held"] for t in closed)/total
    avg_hold_min = avg_bars * 15

    # R multiple (risk = SL_PCT × notional)
    risk_per_trade = SL_PCT * (STARTING_BALANCE * RISK_FRACTION * LEVERAGE)  # initial risk

    print(f"\n  {'Starting:':20s} ${STARTING_BALANCE:,.2f}")
    print(f"  {'Final:':20s} ${balance:,.2f}")
    print(f"  {'P&L:':20s} ${balance-STARTING_BALANCE:+,.2f} ({(balance/STARTING_BALANCE-1)*100:+.1f}%)")
    print(f"  {'Peak:':20s} ${peak:,.2f}")
    print(f"  {'Max DD:':20s} {dd_pct:.1f}%")
    print(f"  {'Weekly avg:':20s} ${(balance-STARTING_BALANCE)/weeks:+,.2f}")
    print(f"  {'Best trade:':20s} ${best_trade_pnl:+,.2f}")
    print(f"  {'Worst trade:':20s} ${worst_trade_pnl:+,.2f}")
    print(f"  ──────────────────────────────────────────")
    print(f"  {'Trades:':20s} {total}")
    print(f"  {'Win rate:':20s} {wr:.1f}% ({wins}W / {losses}L / {be}BE)")
    print(f"  {'Avg win:':20s} ${avg_win:+,.2f} ({avg_win_pct:+.3f}%)")
    print(f"  {'Avg loss:':20s} ${avg_loss:+,.2f} ({avg_loss_pct:+.3f}%)")
    print(f"  {'Max L streak:':20s} {max_losers_row}")
    print(f"  {'Avg hold:':20s} {avg_hold_min:.0f} min ({avg_bars:.1f} bars)")
    print(f"  {'Trades trailed:':20s} {trailed_wins+trailed_losses} ({trailed_wins}W / {trailed_losses}L)")
    print(f"  ──────────────────────────────────────────")
    lpnl=sum(t["pnl_usd"] for t in longs); spnl=sum(t["pnl_usd"] for t in shorts)
    lwr=sum(1 for t in longs if t["pnl_pct"]>0)/max(len(longs),1)*100
    swr=sum(1 for t in shorts if t["pnl_pct"]>0)/max(len(shorts),1)*100
    print(f"  Longs:  {len(longs):3d} | {lwr:.0f}% WR | ${lpnl:+,.2f}")
    print(f"  Shorts: {len(shorts):3d} | {swr:.0f}% WR | ${spnl:+,.2f}")

    print(f"\n  Exit breakdown:")
    for r in sorted(by_reason,key=lambda x:by_reason[x]["pnl"],reverse=True):
        d=by_reason[r]; wrd=d["w"]/max(d["count"],1)*100; ab=d["bars"]/max(d["count"],1)*15
        print(f"    {r:12s}: {d['count']:4d} trades | {d['w']}W/{d['l']}L | {wrd:.0f}% WR | ${d['pnl']:+,.2f} | avg {ab:.0f}min | {d['trailed']} trailed")

    print(f"\n  Best/Worst symbols:")
    for s in sorted(by_sym,key=lambda x:by_sym[x]["pnl"],reverse=True):
        d=by_sym[s]; wrs=d["w"]/max(d["t"],1)*100; ab=d["bars"]/max(d["t"],1)*15
        print(f"    {s:15s}: {d['t']:3d}t | {d['w']}W/{d['l']}L | {wrs:.0f}% WR | ${d['pnl']:+,.2f} | avg {ab:.0f}min")

    # Weekly P&L
    print(f"\n  Weekly P&L:")
    first_week_start = closed[0]["entry_time"]
    week_pnl = 0; week_num = 1; week_trades = 0
    for t in closed:
        if t["entry_time"] - first_week_start > week_num * 7*24*3600*1000:
            print(f"    Week {week_num}: ${week_pnl:+,.2f} ({week_trades} trades)")
            week_num += 1; week_pnl = 0; week_trades = 0
        week_pnl += t["pnl_usd"]; week_trades += 1
    if week_trades:
        print(f"    Week {week_num}: ${week_pnl:+,.2f} ({week_trades} trades)")

    # Trade log
    print(f"\n  First 5 trades:")
    for t in closed[:5]:
        print(f"    {t['symbol']:12s} {t['side']:5s} | entry ${t['entry']:.4f} exit ${t['exit']:.4f} | {t['pnl_pct']*100:+.3f}% | ${t['pnl_usd']:+,.2f} | {t['exit_reason']} | bal ${t['balance_after']:.2f}")
    print(f"  ...")
    print(f"  Last 5 trades:")
    for t in closed[-5:]:
        print(f"    {t['symbol']:12s} {t['side']:5s} | entry ${t['entry']:.4f} exit ${t['exit']:.4f} | {t['pnl_pct']*100:+.3f}% | ${t['pnl_usd']:+,.2f} | {t['exit_reason']} | bal ${t['balance_after']:.2f}")


if __name__=="__main__":
    main()
